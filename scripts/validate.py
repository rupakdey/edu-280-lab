#!/usr/bin/env python3
"""Validate a Zscaler Web Lab Guide repository.

Template-only mode validates the reusable design system.
Built-guide mode additionally validates root-level index.html, lab-*.html,
and sdc-access.html files.

Reference pages are visual examples. Missing links from reference/*.html to
other .html pages are intentionally ignored, but CSS/JS/images and same-page
anchors are still validated.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

CORE_FILES = [
    "AGENTS.md",
    "LAB_GUIDE_STANDARD.md",
    "QA_CHECKLIST.md",
    "README.md",
    ".gitignore",
    "course-template.yaml",
    "assets/css/style.css",
    "assets/js/site.js",
    "assets/js/course-data.js",
    "assets/images/shared/zscaler-logo.svg",
    "assets/images/shared/favicon.svg",
    "templates/index-template.html",
    "templates/lab-template.html",
    "templates/sdc-access-template.html",
    "reference/approved-index.html",
    "reference/approved-lab.html",
    "reference/approved-sdc-access.html",
    "scripts/validate.py",
    ".github/workflows/validate.yml",
]

COMPONENT_FILES = [
    "templates/components/task.html",
    "templates/components/screenshot.html",
    "templates/components/config-table.html",
    "templates/components/search-hint.html",
    "templates/components/expected-result.html",
    "templates/components/technical-explainer.html",
    "templates/components/warning-callout.html",
]

TEMPLATE_PLACEHOLDERS = {
    "templates/index-template.html": [
        "{{COURSE_ID}}", "{{COURSE_TITLE}}", "{{AUTHOR}}",
        "{{LAB_COUNT}}", "{{COURSE_INDEX_ITEMS}}",
    ],
    "templates/lab-template.html": [
        "{{COURSE_ID}}", "{{LAB_NUMBER}}", "{{LAB_TITLE}}",
        "{{LAB_DESCRIPTION}}", "{{TASK_SECTIONS}}",
    ],
    "templates/sdc-access-template.html": [
        "{{COURSE_ID}}", "{{SDC_START_LAB}}", "{{SDC_DESCRIPTION}}",
        "{{SDC_CREDENTIAL_DESCRIPTION}}", "{{SDC_LAB_CARDS}}",
    ],
}

NEUTRAL_FILES = [
    "assets/js/site.js",
    "assets/js/course-data.js",
    "templates/index-template.html",
    "templates/lab-template.html",
    "templates/sdc-access-template.html",
]

COURSE_ID_RE = re.compile(r"\bEDU-\d{3}\b|\bedu[-_]?\d{3}\b", re.I)
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")
LAB_FILE_RE = re.compile(r"lab-(\d+)\.html$", re.I)
TASK_ID_RE = re.compile(r"task-(\d+)-(\d+)$", re.I)


@dataclass
class Issue:
    severity: str
    message: str
    file: str = ""
    line: int = 0
    code: str = ""


class Collector:
    def __init__(self, root: Path):
        self.root = root
        self.issues: list[Issue] = []

    def relative(self, path):
        if not path:
            return ""
        p = Path(path)
        try:
            return p.resolve().relative_to(self.root.resolve()).as_posix()
        except Exception:
            return str(path)

    def error(self, message, path=None, line=0, code=""):
        self.issues.append(Issue("error", message, self.relative(path), line, code))

    def warning(self, message, path=None, line=0, code=""):
        self.issues.append(Issue("warning", message, self.relative(path), line, code))


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids: dict[str, list[int]] = {}
        self.classes: set[str] = set()
        self.references: list[tuple[str, str, int]] = []
        self.fragments: list[tuple[str, int]] = []
        self.images: list[tuple[str, int]] = []
        self.ol_types: list[tuple[str, int]] = []
        self.text_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        line, _ = self.getpos()
        attrs = {k.lower(): (v or "") for k, v in attrs}
        element_id = attrs.get("id", "").strip()
        if element_id:
            self.ids.setdefault(element_id, []).append(line)

        for cls in attrs.get("class", "").split():
            if cls:
                self.classes.add(cls)

        if tag.lower() == "ol":
            list_type = attrs.get("type", "").strip()
            if list_type:
                self.ol_types.append((list_type, line))

        if tag.lower() == "img":
            self.images.append((attrs.get("alt", "").strip(), line))

        if tag.lower() == "a":
            href = attrs.get("href", "").strip()
            if href:
                self.references.append(("href", href, line))
                if href.startswith("#") and len(href) > 1:
                    self.fragments.append((href[1:], line))

        if tag.lower() == "link":
            href = attrs.get("href", "").strip()
            if href:
                self.references.append(("href", href, line))

        if tag.lower() in {"img", "script", "source", "audio", "video"}:
            key = "poster" if tag.lower() == "video" and attrs.get("poster") else "src"
            value = attrs.get(key, "").strip()
            if value:
                self.references.append((key, value, line))

    def handle_data(self, data):
        value = data.strip()
        if value:
            self.text_parts.append(value)

    @property
    def text(self):
        return " ".join(self.text_parts)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_html(path: Path, collector: Collector):
    try:
        parser = PageParser()
        parser.feed(read_text(path))
        parser.close()
        return parser
    except Exception as exc:
        collector.error(f"Could not parse HTML: {exc}", path, code="html-parse")
        return None


def is_external_reference(value: str) -> bool:
    if not value or "{{" in value or value.startswith("//"):
        return True
    parsed = urlsplit(value)
    if parsed.scheme:
        return True
    return value.startswith(("mailto:", "tel:", "javascript:", "data:"))


def resolve_reference(root: Path, source: Path, value: str):
    if is_external_reference(value):
        return None
    parsed = urlsplit(value)
    raw_path = unquote(parsed.path)
    if not raw_path:
        return None
    if raw_path.startswith("/"):
        return (root / raw_path.lstrip("/")).resolve()
    return (source.parent / raw_path).resolve()


def validate_required_files(root: Path, collector: Collector):
    for relative in CORE_FILES + COMPONENT_FILES:
        path = root / relative
        if not path.exists():
            collector.error("Required repository file is missing.", path, code="required-file")
            continue
        if path.is_file() and path.stat().st_size == 0:
            collector.error("Required repository file is empty.", path, code="empty-file")


def validate_templates(root: Path, collector: Collector):
    required_assets = [
        "assets/css/style.css",
        "assets/js/site.js",
        "assets/js/course-data.js",
        "assets/images/shared/zscaler-logo.svg",
        "assets/images/shared/favicon.svg",
    ]
    for relative, placeholders in TEMPLATE_PLACEHOLDERS.items():
        path = root / relative
        if not path.exists():
            continue
        text = read_text(path)
        if len(text.strip()) < 500:
            collector.error("Canonical template is unexpectedly small.", path, code="template-small")
        for placeholder in placeholders:
            if placeholder not in text:
                collector.error(
                    f"Required template placeholder {placeholder} is missing.",
                    path,
                    code="template-placeholder",
                )
        for asset in required_assets:
            if asset not in text:
                collector.error(
                    f"Canonical asset reference is missing: {asset}",
                    path,
                    code="template-assets",
                )


# ---------------------------------------------------------------------
# Course-data integration (shared by template and generated guide)
# ---------------------------------------------------------------------

SCRIPT_TAG_RE = re.compile(r"<script\b[^>]*>", re.I | re.S)
SCRIPT_SRC_RE = re.compile(r"\bsrc\s*=\s*(['\"])(.*?)\1", re.I | re.S)


def validate_script_order(path: Path, collector: Collector):
    """Ensure deferred course data is loaded before deferred site behavior."""
    text = read_text(path)
    hits = {}
    for match in SCRIPT_TAG_RE.finditer(text):
        tag = match.group(0)
        src_match = SCRIPT_SRC_RE.search(tag)
        if not src_match:
            continue
        src = src_match.group(2)
        filename = urlsplit(src).path.rsplit("/", 1)[-1]
        if filename not in {"course-data.js", "site.js"}:
            continue
        hits.setdefault(filename, []).append((match.start(), tag))

    for name in ("course-data.js", "site.js"):
        if len(hits.get(name, [])) != 1:
            collector.error(
                f"Expected exactly one script reference to assets/js/{name}.",
                path, code="script-integration",
            )
            continue
        _, tag = hits[name][0]
        if not re.search(r"\bdefer(?:\s|=|>)", tag, re.I):
            collector.error(
                f"{name} must have the defer attribute.",
                path, code="script-defer",
            )
        if re.search(r"\basync(?:\s|=|>)", tag, re.I):
            collector.error(
                f"{name} must not use async; load order must be preserved.",
                path, code="script-async",
            )
        if urlsplit(SCRIPT_SRC_RE.search(tag).group(2)).path != f"assets/js/{name}":
            collector.error(
                f"Use root-relative-to-page script path assets/js/{name}.",
                path, code="script-path",
            )

    if all(len(hits.get(name, [])) == 1 for name in ("course-data.js", "site.js")):
        if hits["course-data.js"][0][0] > hits["site.js"][0][0]:
            collector.error(
                "course-data.js must appear before site.js.",
                path, code="script-order",
            )


class JsLiteralError(ValueError):
    pass


# A deliberately limited, safe JS literal parser. The course-data contract
# permits comments, unquoted object keys, trailing commas and JS booleans;
# it does NOT execute arbitrary JavaScript. No additional pip packages needed.
JS_TOKEN_RE = re.compile(
    r"(?P<space>\s+)|"
    r"(?P<comment>//[^\n]*|/\*[\s\S]*?\*/)|"
    r"(?P<string>\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')|"
    r"(?P<number>-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)|"
    r"(?P<ident>[A-Za-z_$][A-Za-z0-9_$]*)|"
    r"(?P<punct>[{}\[\]:,;])|"
    r"(?P<invalid>[\s\S])"
)


class JsLiteralParser:
    def __init__(self, text: str):
        self.tokens = []
        for match in JS_TOKEN_RE.finditer(text):
            kind = match.lastgroup
            if kind in ("space", "comment"):
                continue
            if kind == "invalid":
                raise JsLiteralError(f"Unsupported JavaScript token: {match.group()!r}")
            self.tokens.append((kind, match.group()))
        self.index = 0

    def peek(self):
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def take(self, expected=None):
        tok = self.peek()
        if tok is None:
            raise JsLiteralError("Unexpected end of course data")
        if expected is not None and tok[1] != expected:
            raise JsLiteralError(f"Expected {expected!r}, found {tok[1]!r}")
        self.index += 1
        return tok

    def value(self):
        tok = self.peek()
        if tok is None:
            raise JsLiteralError("Missing value")
        kind, value = tok
        if value == "{":
            return self.object()
        if value == "[":
            return self.array()
        self.take()
        if kind == "string":
            if value[0] == '"':
                return json.loads(value)
            import ast
            return ast.literal_eval(value)
        if kind == "number":
            return float(value) if any(c in value for c in ".eE") else int(value)
        if kind == "ident" and value in {"true", "false", "null"}:
            return {"true": True, "false": False, "null": None}[value]
        raise JsLiteralError(
            f"Unsupported value {value!r}; course-data.js must contain a plain object literal"
        )

    def object(self):
        self.take("{")
        result = {}
        while self.peek() and self.peek()[1] != "}":
            kind, name = self.take()
            if kind == "string":
                name = json.loads(name) if name[0] == '"' else __import__('ast').literal_eval(name)
            elif kind != "ident":
                raise JsLiteralError(f"Invalid object key: {name!r}")
            self.take(":")
            if name in result:
                raise JsLiteralError(f"Duplicate object key: {name}")
            result[name] = self.value()
            if self.peek() and self.peek()[1] == ",":
                self.take(",")
            elif self.peek() and self.peek()[1] != "}":
                raise JsLiteralError("Expected comma or closing brace")
        self.take("}")
        return result

    def array(self):
        self.take("[")
        result = []
        while self.peek() and self.peek()[1] != "]":
            result.append(self.value())
            if self.peek() and self.peek()[1] == ",":
                self.take(",")
            elif self.peek() and self.peek()[1] != "]":
                raise JsLiteralError("Expected comma or closing bracket")
        self.take("]")
        return result


def load_course_data(root: Path, collector: Collector):
    path = root / "assets/js/course-data.js"
    if not path.exists():
        return None
    text = read_text(path)
    match = re.search(r"\bwindow\s*\.\s*LAB_GUIDE_COURSE\s*=\s*", text)
    if not match:
        collector.error(
            "course-data.js must assign window.LAB_GUIDE_COURSE.",
            path, code="course-data-contract",
        )
        return None
    try:
        parsed = JsLiteralParser(text[match.end():]).value()
        if not isinstance(parsed, dict):
            raise JsLiteralError("Expected top-level object")
    except (JsLiteralError, ValueError, SyntaxError) as exc:
        collector.error(
            f"Could not parse course-data.js object: {exc}. "
            "Use plain JS object/array literals, not computed expressions.",
            path, code="course-data-parse",
        )
        return None
    return parsed


def validate_course_data_template(root: Path, collector: Collector, data):
    path = root / "assets/js/course-data.js"
    if data is None:
        return
    for field, placeholder in (
        ("id", "{{COURSE_ID}}"),
        ("title", "{{COURSE_TITLE}}"),
        ("storagePrefix", "{{STORAGE_PREFIX}}"),
    ):
        if data.get(field) != placeholder:
            collector.error(
                f"Template course-data.js must retain {field}: {placeholder!r}.",
                path, code="course-data-template",
            )
    if data.get("labs") != []:
        collector.error(
            "Reusable template course-data.js must have labs: [] (not a sample course).",
            path, code="course-data-template",
        )
    if data.get("search") != []:
        collector.error(
            "Reusable template course-data.js must have search: [].",
            path, code="course-data-template",
        )
    if data.get("sdcAccess") is not None:
        collector.error(
            "Reusable template course-data.js must use sdcAccess: null.",
            path, code="course-data-template",
        )


def validate_target_href(root: Path, href: str, collector: Collector, source: Path,
                         context: str, pages: dict):
    if not isinstance(href, str) or not href.strip():
        collector.error(f"{context}: href is missing.", source, code="course-data-href")
        return
    u = urlsplit(href)
    if u.scheme or u.netloc or href.startswith("/") or href.startswith("//"):
        collector.error(f"{context}: use a local relative href: {href}", source,
                        code="course-data-href")
        return
    target = (root / unquote(u.path or "index.html")).resolve()
    if not target.is_relative_to(root.resolve()):
        collector.error(f"{context}: path escapes repository: {href}", source,
                        code="course-data-href")
        return
    if not target.is_file():
        collector.error(f"{context}: target file does not exist: {href}", source,
                        code="course-data-href")
        return
    if u.fragment:
        if target not in pages:
            pages[target] = parse_html(target, collector)
        parser = pages[target]
        if parser and unquote(u.fragment) not in parser.ids:
            collector.error(f"{context}: missing anchor #{u.fragment} in {target.name}",
                            source, code="course-data-anchor")


def validate_generated_course_data(root: Path, collector: Collector, data):
    path = root / "assets/js/course-data.js"
    if data is None:
        return

    for field in ("id", "title", "storagePrefix"):
        value = data.get(field)
        if not isinstance(value, str) or not value.strip() or PLACEHOLDER_RE.search(value):
            collector.error(
                f"Generated course-data.js needs a real non-empty {field} value.",
                path, code="course-data-field",
            )
    if PLACEHOLDER_RE.search(read_text(path)):
        # Restrict this check to data values, not illustrative comments.
        if PLACEHOLDER_RE.search(json.dumps(data)):
            collector.error(
                "Generated course-data.js still contains unresolved data placeholders.",
                path, code="course-data-placeholder",
            )

    index = root / "index.html"
    if index.exists():
        index_text = read_text(index)
        for field, attribute in (("id", "data-course-id"), ("storagePrefix", "data-storage-prefix")):
            match = re.search(rf'{attribute}=["\']([^"\']+)["\']', index_text)
            if not match or match.group(1) != data.get(field):
                collector.error(
                    f"index.html {attribute} must match course-data.js {field}.",
                    index, code="course-data-page",
                )

    labs = data.get("labs")
    if not isinstance(labs, list) or not labs:
        collector.error(
            "Generated course-data.js must define at least one lab.",
            path, code="course-data-labs",
        )
        return
    pages = {}
    seen_nums, seen_lab_hrefs, seen_tasks = set(), set(), set()
    previous_num = 0
    for lab in labs:
        if not isinstance(lab, dict):
            collector.error("Each labs[] entry must be an object.", path,
                            code="course-data-lab")
            continue
        number = lab.get("number")
        if not isinstance(number, int) or isinstance(number, bool) or number < 1:
            collector.error(f"Invalid lab number: {number!r}.", path,
                            code="course-data-lab")
            continue
        if number in seen_nums:
            collector.error(f"Duplicate lab number {number}.", path,
                            code="course-data-lab")
        if number <= previous_num:
            collector.error(f"Labs must be ordered by ascending lab number: {number}.",
                            path, code="course-data-lab")
        previous_num = number
        seen_nums.add(number)
        title = lab.get("title")
        if not isinstance(title, str) or not title.strip():
            collector.error(f"Lab {number} needs a title.", path, code="course-data-lab")
        href = lab.get("href")
        expected = f"lab-{number:02d}.html"
        if href != expected:
            collector.error(f"Lab {number} href must be {expected!r}, found {href!r}.",
                            path, code="course-data-lab")
        if isinstance(href, str):
            if href in seen_lab_hrefs:
                collector.error(f"Duplicate lab href {href}.", path,
                                code="course-data-lab")
            seen_lab_hrefs.add(href)
            validate_target_href(root, href, collector, path, f"Lab {number}", pages)
        lab_page = root / expected
        if lab_page.exists():
            html = read_text(lab_page)
            for field, attr in (("id", "data-course-id"), ("storagePrefix", "data-storage-prefix")):
                match = re.search(rf'{attr}=["\']([^"\']+)["\']', html)
                if not match or match.group(1) != data.get(field):
                    collector.error(f"Lab {number} {attr} differs from course-data.js {field}.",
                                    lab_page, code="course-data-page")

        lab_expected_ids = set()
        lab_expected_checks = set()
        tasks = lab.get("tasks")
        if not isinstance(tasks, list) or not tasks:
            collector.error(f"Lab {number} needs at least one task definition.",
                            path, code="course-data-tasks")
            continue
        for task in tasks:
            if not isinstance(task, dict):
                collector.error(f"Lab {number} has non-object task entry.", path,
                                code="course-data-task")
                continue
            task_number = task.get("number")
            task_id = task.get("id")
            task_title = task.get("title")
            if not isinstance(task_number, str) or not re.fullmatch(rf"{number}\.[1-9]\d*", task_number):
                collector.error(f"Invalid task number {task_number!r} under Lab {number}.",
                                path, code="course-data-task")
                continue
            expected_id = f"task-{task_number.replace('.', '-')}"
            lab_expected_ids.add(expected_id)
            lab_expected_checks.add(task_number)
            if task_id != expected_id:
                collector.error(f"Task {task_number} id must be {expected_id}.", path,
                                code="course-data-task")
            if task_number in seen_tasks:
                collector.error(f"Duplicate task number {task_number}.", path,
                                code="course-data-task")
            seen_tasks.add(task_number)
            if not isinstance(task_title, str) or not task_title.strip():
                collector.error(f"Task {task_number} needs a title.", path,
                                code="course-data-task")
            task_href = task.get("href", f"{expected}#{expected_id}")
            if task_href != f"{expected}#{expected_id}":
                collector.error(f"Task {task_number} href must be {expected}#{expected_id}.",
                                path, code="course-data-task")
            validate_target_href(root, task_href, collector, path, f"Task {task_number}", pages)
            if lab_page.is_file():
                html = read_text(lab_page)
                check = re.search(rf'\bdata-task-check=["\']{re.escape(task_number)}["\']', html)
                if not check:
                    collector.error(
                        f"Task {task_number} has no matching data-task-check checkbox in {expected}.",
                        lab_page, code="course-data-progress",
                    )

        if lab_page.is_file():
            page_source = read_text(lab_page)
            defined_task_ids = set(re.findall(
                r'<section\b(?=[^>]*\bclass=["\'][^"\']*\btask\b)' 
                r'(?=[^>]*\bid=["\'](task-\d+-\d+)["\'])[^>]*>',
                page_source, re.I | re.S,
            ))
            for extra in sorted(defined_task_ids - lab_expected_ids):
                collector.error(
                    f"Task section {extra} exists in {expected} but is absent from course-data.js.",
                    lab_page, code="course-data-orphan-task",
                )
            actual_checks = set(re.findall(
                r'\bdata-task-check=["\']([^"\']+)["\']', page_source
            ))
            for extra in sorted(actual_checks - lab_expected_checks):
                collector.error(
                    f"Checkbox data-task-check={extra!r} is not defined in course-data.js.",
                    lab_page, code="course-data-orphan-progress",
                )

        explainers = lab.get("explainers", [])
        if not isinstance(explainers, list):
            collector.error(f"Lab {number} explainers must be an array.", path,
                            code="course-data-explainer")
            explainers = []
        for exp in explainers:
            if not isinstance(exp, dict):
                collector.error(f"Lab {number} has non-object explainer.", path,
                                code="course-data-explainer")
                continue
            exp_href = exp.get("href") or (f"{expected}#{exp['id']}" if exp.get("id") else expected)
            validate_target_href(root, exp_href, collector, path,
                                 f"Lab {number} explainer", pages)

    # Detect actual generated lab pages absent from course data.
    for lab_html in root.glob("lab-*.html"):
        if lab_html.name not in seen_lab_hrefs:
            collector.error(f"Generated lab page {lab_html.name} has no course-data.js entry.",
                            lab_html, code="course-data-orphan")

    for field in ("labAccess", "sdcAccess"):
        checkpoint = data.get(field)
        if checkpoint is None or checkpoint is False:
            continue
        if not isinstance(checkpoint, dict):
            collector.error(f"{field} must be null or an object.", path,
                            code="course-data-checkpoint")
            continue
        href = checkpoint.get("href", "")
        validate_target_href(root, href, collector, path, field, pages)
        if field == "sdcAccess":
            before = checkpoint.get("beforeLab")
            if not isinstance(before, int) or before not in seen_nums:
                collector.error("sdcAccess.beforeLab must name a defined lab number.",
                                path, code="course-data-checkpoint")
            else:
                for lab in labs:
                    if isinstance(lab, dict) and isinstance(lab.get("number"), int) and lab["number"] >= before and not lab.get("sdc"):
                        collector.warning(
                            f"Lab {lab['number']} is after the SDC checkpoint but lacks sdc: true.",
                            path, code="course-data-sdc-flag",
                        )

    if (root / "sdc-access.html").exists() and not data.get("sdcAccess"):
        collector.error("sdc-access.html exists but sdcAccess is null.",
                        path, code="course-data-checkpoint")
    if any(isinstance(l, dict) and l.get("sdc") for l in labs) and not data.get("sdcAccess"):
        collector.error("A lab is marked sdc: true without sdcAccess checkpoint.",
                        path, code="course-data-checkpoint")
    search = data.get("search", [])
    if not isinstance(search, list):
        collector.error("search must be an array.", path, code="course-data-search")
    else:
        for entry in search:
            if not isinstance(entry, dict) or not entry.get("label"):
                collector.error("Each search entry needs a label.", path,
                                code="course-data-search")
                continue
            validate_target_href(root, entry.get("href", ""), collector, path,
                                 f"Search entry {entry['label']}", pages)


def validate_components(root: Path, collector: Collector):
    for relative in COMPONENT_FILES:
        path = root / relative
        if path.exists() and len(read_text(path).strip()) < 40:
            collector.error(
                "Reusable component is empty or unexpectedly small.",
                path,
                code="component-small",
            )


def validate_course_neutrality(root: Path, collector: Collector, built: bool = False):
    files = [root / p for p in NEUTRAL_FILES if not (built and p == "assets/js/course-data.js")]
    component_dir = root / "templates" / "components"
    if component_dir.exists():
        files.extend(component_dir.glob("*.html"))

    for path in files:
        if not path.exists():
            continue
        text = read_text(path)
        for match in COURSE_ID_RE.finditer(text):
            line = text[:match.start()].count("\n") + 1
            collector.error(
                f"Reusable template/design file contains hard-coded course ID "
                f"{match.group(0)!r}. Use course data or a placeholder.",
                path,
                line,
                "hardcoded-course",
            )


def validate_html_references(
    root: Path,
    path: Path,
    collector: Collector,
    parser=None,
    ignore_missing_html=False,
):
    parser = parser or parse_html(path, collector)
    if parser is None:
        return

    for element_id, lines in parser.ids.items():
        if len(lines) > 1:
            collector.error(
                f"Duplicate HTML id {element_id!r}.",
                path,
                lines[1],
                "duplicate-id",
            )

    # Same-page anchors are always validated, including in reference pages.
    for fragment, line in parser.fragments:
        if fragment not in parser.ids:
            collector.error(
                f"Fragment link points to missing id #{fragment}.",
                path,
                line,
                "broken-fragment",
            )

    for kind, value, line in parser.references:
        target = resolve_reference(root, path, value)
        if target is None:
            continue

        # Reference pages are visual examples, not complete standalone courses.
        # They may intentionally link to lab-NN.html/index.html/sdc-access.html
        # pages that do not exist in the reusable template repository.
        # Skip only these cross-page HTML existence checks.
        parsed_ref = urlsplit(value)
        ref_path = unquote(parsed_ref.path)
        if ignore_missing_html and ref_path.lower().endswith(".html"):
            continue

        if value.startswith("/"):
            collector.warning(
                "Root-absolute URL may break on GitHub Pages project sites; "
                "prefer relative URLs.",
                path,
                line,
                "absolute-url",
            )

        if not target.exists():
            collector.error(
                f"Broken local {kind}: {value}",
                path,
                line,
                "broken-reference",
            )

    for alt, line in parser.images:
        if not alt:
            collector.warning(
                "Image has no useful alt text.",
                path,
                line,
                "missing-alt",
            )


def validate_reference_pages(root: Path, collector: Collector):
    reference_dir = root / "reference"
    if not reference_dir.exists():
        return
    for path in sorted(reference_dir.glob("*.html")):
        validate_html_references(
            root,
            path,
            collector,
            ignore_missing_html=True,
        )


def generated_pages(root: Path):
    pages = []
    for filename in ("index.html", "sdc-access.html"):
        path = root / filename
        if path.exists():
            pages.append(path)
    pages.extend(sorted(root.glob("lab-*.html")))
    return pages


def validate_course_manifest(root: Path, collector: Collector, built: bool):
    path = root / "course.yaml"
    if not path.exists():
        if built:
            collector.error(
                "Generated guide exists but course.yaml is missing.",
                path,
                code="course-manifest",
            )
        return

    text = read_text(path)
    if PLACEHOLDER_RE.search(text):
        collector.error(
            "course.yaml still contains unresolved placeholders.",
            path,
            code="course-placeholder",
        )

    for field in ("id:", "title:", "author:"):
        if not re.search(rf"(?m)^\s*{re.escape(field)}\s*\S+", text):
            collector.warning(
                f"course.yaml does not appear to define {field[:-1]!r}.",
                path,
                code="course-field",
            )


def validate_common_page(root: Path, path: Path, collector: Collector):
    text = read_text(path)
    parser = parse_html(path, collector)
    if parser is None:
        return None

    match = PLACEHOLDER_RE.search(text)
    if match:
        line = text[:match.start()].count("\n") + 1
        collector.error(
            f"Generated page contains unresolved placeholder {match.group(0)}.",
            path,
            line,
            "placeholder",
        )

    validate_html_references(root, path, collector, parser)

    required_shell = [
        'id="course-nav"',
        'id="global-search-input"',
        "data-theme-toggle",
        'class="floating-logo"',
        "assets/css/style.css",
        "assets/js/site.js",
        "assets/images/shared/zscaler-logo.svg",
    ]
    for snippet in required_shell:
        if snippet not in text:
            collector.error(
                f"Generated page is missing required design element: {snippet}",
                path,
                code="page-shell",
            )

    for list_type, line in parser.ol_types:
        if list_type.lower() in {"a", "i"}:
            collector.error(
                "Alphabetic or Roman ordered lists are not permitted for "
                "generated task instructions.",
                path,
                line,
                "pdf-numbering",
            )

    for forbidden in ("source-instructions", "source-step"):
        if forbidden in parser.classes:
            collector.error(
                f"Legacy PDF-mirroring class {forbidden!r} is not allowed.",
                path,
                code="pdf-layout",
            )

    return parser


def validate_index_page(root: Path, path: Path, collector: Collector):
    parser = validate_common_page(root, path, collector)
    if parser is None:
        return
    for element_id in ("overview", "navigation-guide", "contents", "lab-filter"):
        if element_id not in parser.ids:
            collector.error(
                f"Course index is missing required section #{element_id}.",
                path,
                code="index-structure",
            )
    if "Unofficial learning aid" not in parser.text:
        collector.error(
            "Course index is missing the unofficial learning-aid notice.",
            path,
            code="disclaimer",
        )


def extract_tasks(text: str):
    pattern = re.compile(
        r'<section\b[^>]*class=["\'][^"\']*\btask\b[^"\']*["\'][^>]*'
        r'id=["\']([^"\']+)["\'][^>]*>',
        re.I,
    )
    starts = list(pattern.finditer(text))
    tasks = []
    for index, match in enumerate(starts):
        start = match.start()
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        line = text[:start].count("\n") + 1
        tasks.append((match.group(1), text[start:end], line))
    return tasks


def validate_lab_page(root: Path, path: Path, collector: Collector):
    parser = validate_common_page(root, path, collector)
    if parser is None:
        return

    filename_match = LAB_FILE_RE.search(path.name)
    if not filename_match:
        collector.error("Lab filename must follow lab-NN.html.", path, code="lab-filename")
        return

    lab_number = int(filename_match.group(1))
    if "lab-hero" not in parser.classes:
        collector.error("Lab page is missing the approved .lab-hero.", path, code="lab-hero")
    if "page-nav" not in parser.classes:
        collector.error(
            "Lab page is missing Previous/Next navigation.",
            path,
            code="page-nav",
        )

    text = read_text(path)
    tasks = extract_tasks(text)
    if not tasks:
        collector.error(
            'Lab page contains no <section class="task"> sections.',
            path,
            code="tasks",
        )
        return

    seen = set()
    for task_id, block, line in tasks:
        if task_id in seen:
            collector.error(f"Duplicate task id {task_id}.", path, line, "task-id")
        seen.add(task_id)

        task_match = TASK_ID_RE.fullmatch(task_id)
        if not task_match:
            collector.error(
                f"Task id {task_id!r} must follow task-{lab_number}-1.",
                path,
                line,
                "task-id",
            )
        elif int(task_match.group(1)) != lab_number:
            collector.error(
                f"Task id {task_id!r} does not match Lab {lab_number}.",
                path,
                line,
                "task-id",
            )

        visible_text = re.sub(r"<[^>]+>", " ", block)
        visible_text = re.sub(r"\s+", " ", visible_text)
        if "expected result" not in visible_text.lower():
            collector.error(
                f"{task_id} is missing an Expected Result block.",
                path,
                line,
                "expected-result",
            )


def validate_sdc_page(root: Path, path: Path, collector: Collector):
    parser = validate_common_page(root, path, collector)
    if parser is None:
        return
    if "sdc-hero" not in parser.classes:
        collector.error(
            "SDC checkpoint is missing the approved .sdc-hero.",
            path,
            code="sdc-hero",
        )
    if "Sample only" not in parser.text:
        collector.warning(
            "SDC credential example is not visibly labelled 'Sample only'.",
            path,
            code="sdc-sample",
        )


def validate_generated_site(root: Path, collector: Collector):
    pages = generated_pages(root)
    if not pages:
        return

    index = root / "index.html"
    if not index.exists():
        collector.error(
            "Generated course pages exist but index.html is missing.",
            index,
            code="index",
        )
    else:
        validate_index_page(root, index, collector)

    for lab in sorted(root.glob("lab-*.html")):
        validate_lab_page(root, lab, collector)

    sdc = root / "sdc-access.html"
    if sdc.exists():
        validate_sdc_page(root, sdc, collector)


def validate_workflow(root: Path, collector: Collector):
    path = root / ".github" / "workflows" / "validate.yml"
    if not path.exists():
        return
    text = read_text(path)
    if "scripts/validate.py" not in text:
        collector.error(
            "GitHub Actions workflow does not execute scripts/validate.py.",
            path,
            code="workflow",
        )
    if "actions/checkout@" not in text:
        collector.error(
            "GitHub Actions workflow does not use actions/checkout.",
            path,
            code="workflow",
        )


def print_issues(issues: list[Issue]):
    github_actions = os.getenv("GITHUB_ACTIONS", "").lower() == "true"
    for issue in issues:
        location = issue.file
        if issue.line:
            location += f":{issue.line}"
        prefix = "ERROR" if issue.severity == "error" else "WARN "
        code = f" [{issue.code}]" if issue.code else ""
        print(f"{prefix} {location}{code}: {issue.message}")

        if github_actions:
            level = "error" if issue.severity == "error" else "warning"
            properties = []
            if issue.file:
                properties.append(f"file={issue.file}")
            if issue.line:
                properties.append(f"line={issue.line}")
            print(f"::{level} {','.join(properties)}::{issue.message}")


def write_json_report(path: Path, root: Path, issues: list[Issue]):
    payload = {
        "repository": str(root),
        "errors": sum(i.severity == "error" for i in issues),
        "warnings": sum(i.severity == "warning" for i in issues),
        "issues": [asdict(i) for i in issues],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Validate Zscaler Web Lab Guide repository."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures.",
    )
    parser.add_argument("--json-report", type=Path, default=None)
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.exists():
        print(f"Repository root does not exist: {root}", file=sys.stderr)
        return 2

    collector = Collector(root)
    built = bool(generated_pages(root))

    validate_required_files(root, collector)
    validate_templates(root, collector)
    validate_components(root, collector)
    validate_course_neutrality(root, collector, built)
    for relative in TEMPLATE_PLACEHOLDERS:
        template = root / relative
        if template.is_file():
            validate_script_order(template, collector)
    validate_reference_pages(root, collector)
    validate_workflow(root, collector)

    course_data = load_course_data(root, collector)
    if built:
        validate_generated_course_data(root, collector, course_data)
        for page in generated_pages(root):
            validate_script_order(page, collector)
    else:
        validate_course_data_template(root, collector, course_data)
    validate_course_manifest(root, collector, built)
    validate_generated_site(root, collector)

    collector.issues.sort(
        key=lambda item: (
            0 if item.severity == "error" else 1,
            item.file,
            item.line,
            item.code,
        )
    )

    print_issues(collector.issues)

    errors = sum(issue.severity == "error" for issue in collector.issues)
    warnings = sum(issue.severity == "warning" for issue in collector.issues)

    if args.json_report:
        report = args.json_report
        if not report.is_absolute():
            report = root / report
        write_json_report(report, root, collector.issues)

    mode = "built-guide + template" if built else "template-only"
    print()
    print(f"Validation mode: {mode}")
    print(f"Errors:   {errors}")
    print(f"Warnings: {warnings}")

    if errors:
        print("FAIL: fix validation errors before export.")
        return 1
    if args.strict and warnings:
        print("FAIL: strict mode treats warnings as errors.")
        return 1

    print("PASS with warnings." if warnings else "PASS: no validation issues found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
