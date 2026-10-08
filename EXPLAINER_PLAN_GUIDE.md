# Choosing Technical Explainers

Edit **`explainer-plan.yaml`** in each course repository. The reusable template
contains **`explainer-plan-template.yaml`**; copy it when starting a new course.

## Simple workflow

1. Add a topic under `explainers:` and give it a unique lowercase `id`.
2. Set `lab: N` (and optionally `task: "N.M"`).
3. Choose `placement: lab_intro` or `placement: before_steps` (task only).
4. Choose `depth: brief | standard | detailed` and a visual type.
5. List the points to explain under `cover:`. Avoid click-by-click steps.
6. Set `enabled: true` to include it; keep `enabled: false` for suggestions.
7. Build/update that lab. The builder must update the rendered HTML anchor and
   matching `assets/js/course-data.js` `labs[].explainers[]` link.
8. Run GitHub Actions > Validate Lab Guide and review the rendered HTML.

No `site.js` changes are needed. YAML is not loaded by the browser.

## Controls

- `generation: specified_only` (default) generates **only enabled** entries.
- `suggest_additional_topics: true` allows suggestions in build notes; it does
  not auto-insert explainers in specified_only mode.
- `generation: specified_plus_auto` permits justified additional explainers,
  but explicitly disabled topics must not be silently inserted.
- `depth: brief` ~50–100 words; `standard` ~150–250; `detailed` ~250–400.
  Visuals can replace prose where they communicate better.
- `visual:` `none`, `flow_diagram`, `architecture_diagram`,
  `comparison_table`, `sequence_diagram`, `auto`.
- Place whole-lab content after objectives; place task-level content before
  numbered task steps. Always finish each hands-on task with Expected Result.
- Topics can refer to future labs listed in `course.yaml` even before their
  generated HTML pages exist. Once published, enabled items must match HTML
  and navigation anchors.

## Example: enabling an existing suggested topic

In the EDU-280 plan, change this value under the Lab 5 PBR topic:

    enabled: false

into:

    enabled: true

When Lab 5 is built, the builder includes the PBR context and gives it the
stable `id: pbr-context` in HTML and `course-data.js`. An enabled topic for a
lab that has not been published yet remains a build instruction, not a broken
link.

## Task-specific example

    - id: policy-evaluation-context
      enabled: true
      lab: 4
      task: "4.2"
      topic: Policy evaluation order
      placement: before_steps
      depth: standard
      visual: flow_diagram
      cover:
        - Why policy order matters
        - How conflicting conditions are evaluated
        - What behavior the learner should test

Check the actual source lab's task number before using this example.

## Validator dependency

Local setup, once:

    python3 -m pip install -r requirements-validation.txt
    python3 scripts/validate.py --json-report validation-report.json

GitHub Actions installs the same dependency automatically. It checks plan
syntax, valid fields, duplicates, lab/task references, enabled/disabled rules,
and consistency with published explainer anchors and course-data entries.
