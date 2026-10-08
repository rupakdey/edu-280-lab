/*
 * Zscaler Web Lab Guide — course-neutral site behavior.
 *
 * A generated course may define window.LAB_GUIDE_COURSE before loading this
 * script. Course data should contain its title, labs, tasks, optional SDC
 * checkpoint, and optional explainer/search entries. This script never embeds
 * lab titles, task lists, or a course identifier from an individual course.
 *
 * See the configuration example accompanying this replacement file.
 */
(() => {
  "use strict";

  const scriptUrl = document.currentScript?.src || "";
  const logoUrl = scriptUrl
    ? new URL("../images/shared/zscaler-logo.svg", scriptUrl).href
    : "assets/images/shared/zscaler-logo.svg";

  const body = document.body;
  const raw = window.LAB_GUIDE_COURSE || {};
  const courseId = String(raw.id || body?.dataset.courseId || "Lab Guide");
  const courseTitle = String(raw.title || body?.dataset.courseTitle || courseId);
  const courseSubtitle = String(raw.subtitle || raw.edition || "Web Lab Guide");
  const storagePrefix = String(
    body?.dataset.storagePrefix || raw.storagePrefix ||
      courseId.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") ||
      "zscaler-lab-guide"
  );

  // The course data format is deliberately tolerant of task objects and the
  // older [number, title, href] arrays used by previous static guides.
  function toTask(task, labNumber, labHref) {
    const source = Array.isArray(task)
      ? { number: task[0], title: task[1], href: task[2] }
      : (task || {});
    let number = String(source.number || source.label || source.id || "");
    const id = String(source.id || "");
    if (/^task-\d+-\d+$/.test(number)) {
      number = number.replace(/^task-(\d+)-(\d+)$/, "$1.$2");
    }
    if (!number && /^task-\d+-\d+$/.test(id)) {
      number = id.replace(/^task-(\d+)-(\d+)$/, "$1.$2");
    }
    const fragment = /^\d+\.\d+$/.test(number)
      ? `task-${number.replace(".", "-")}`
      : (id || "");
    return {
      number,
      title: String(source.title || source.name || number || "Task"),
      href: String(source.href || (fragment ? `${labHref}#${fragment}` : labHref)),
      keywords: String(source.keywords || ""),
    };
  }

  function toLab(lab) {
    const number = Number(lab.number ?? lab.n ?? lab.lab ?? 0);
    const href = String(lab.href || `lab-${String(number).padStart(2, "0")}.html`);
    return {
      number,
      title: String(lab.title || `Lab ${number}`),
      href,
      sdc: Boolean(lab.sdc),
      optional: Boolean(lab.optional),
      keywords: String(lab.keywords || ""),
      tasks: Array.isArray(lab.tasks)
        ? lab.tasks.map((task) => toTask(task, number, href))
        : [],
      explainers: Array.isArray(lab.explainers) ? lab.explainers : [],
    };
  }

  const labs = (Array.isArray(raw.labs) ? raw.labs : [])
    .map(toLab)
    .filter((lab) => lab.number > 0);

  function normalizedCheckpoint() {
    const source = raw.sdcAccess ?? raw.sdc ?? null;
    if (!source || source === false) return null;
    if (source === true) {
      return { title: "SDC access checkpoint", href: "sdc-access.html" };
    }
    if (source.enabled === false) return null;
    return {
      title: String(source.title || "SDC access checkpoint"),
      href: String(source.href || "sdc-access.html"),
      beforeLab: Number(source.beforeLab || source.startLab || 0),
    };
  }

  const sdc = normalizedCheckpoint();
  const taskNumbers = [...new Set(labs.flatMap((lab) => lab.tasks.map((task) => task.number).filter(Boolean)))];
  const totalTasks = taskNumbers.length;

  const keyForTask = (number) => {
    let value = String(number || "");
    if (/^task-\d+-\d+$/.test(value)) {
      value = value.replace(/^task-(\d+)-(\d+)$/, "$1.$2");
    }
    return `${storagePrefix}-task-${value}`;
  };
  const themeKey = `${storagePrefix}-theme`;

  function getStored(key) {
    try { return localStorage.getItem(key); } catch { return null; }
  }
  function setStored(key, value) {
    try { localStorage.setItem(key, value); } catch { /* storage disabled */ }
  }

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (char) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    })[char]);
  }

  function safeHref(value) {
    const href = String(value || "#").trim();
    if (/^(https?:\/\/|\/\/|\.\.?\/|#)/i.test(href)) return escapeHtml(href);
    if (/^[\w.\-/]+(?:#[\w.\-]+)?$/.test(href)) return escapeHtml(href);
    return "#";
  }

  function pageName() {
    if (body?.dataset.page) return body.dataset.page;
    const filename = location.pathname.split("/").pop() || "index.html";
    return filename === "index.html" ? "home" : filename.replace(/\.html$/i, "");
  }

  function navLink(label, href, marker, active = false, extraClass = "") {
    return `<a class="nav-link ${extraClass}${active ? " active" : ""}" ` +
      `href="${safeHref(href)}"${active ? ' aria-current="page"' : ""}>` +
      `<span class="num">${escapeHtml(marker)}</span>` +
      `<span>${escapeHtml(label)}</span></a>`;
  }

  function renderNav() {
    const holder = document.getElementById("course-nav");
    if (!holder) return;
    const page = pageName();

    const startLinks = [
      navLink("Introduction", "index.html#overview", "⌂", page === "home"),
      navLink("Experience Center navigation", "index.html#navigation-guide", "↗"),
      navLink("Course index", "index.html#contents", "≡"),
    ];
    if (raw.labAccess) {
      const access = raw.labAccess === true ? {} : raw.labAccess;
      startLinks.push(navLink(
        access.title || "Lab access", access.href || "lab-access.html", "◎",
        page === "lab-access"
      ));
    }

    const sdcBefore = sdc
      ? (sdc.beforeLab || labs.find((lab) => lab.sdc)?.number || 0)
      : 0;
    const checkpoint = sdc
      ? `<div class="nav-label nav-label-sdc">Solutions Demo Center</div>` +
        navLink(sdc.title, sdc.href, "SDC", page === "sdc-access")
      : "";

    let checkpointInserted = false;
    const labLinks = labs.map((lab) => {
      const active = page === `lab-${String(lab.number).padStart(2, "0")}` ||
        page === `lab-${lab.number}`;
      let section = "";
      if (sdc && !checkpointInserted && sdcBefore && lab.number >= sdcBefore) {
        section += checkpoint;
        checkpointInserted = true;
      }

      section += navLink(
        `${lab.title}${lab.optional ? " (Optional)" : ""}`,
        lab.href,
        String(lab.number).padStart(2, "0"),
        active
      );
      if (lab.sdc) {
        // Keep the existing approved-design SDC badge on applicable labs.
        section = section.replace(/<\/a>$/, '<span class="nav-badge">SDC</span></a>');
      }
      if (active) {
        const explainerLinks = lab.explainers.map((explainer) =>
          navLink(
            explainer.title || "Technical context",
            explainer.href || (explainer.id ? `${lab.href}#${explainer.id}` : lab.href),
            "i"
          )
        ).join("");
        const taskLinks = lab.tasks.map((task) =>
          navLink(task.title, task.href, task.number)
        ).join("");
        if (explainerLinks || taskLinks) {
          section += `<div class="nav-sub">${explainerLinks}${taskLinks}</div>`;
        }
      }
      return section;
    }).join("");

    // Courses with an SDC checkpoint but no marked SDC lab can still display it.
    const finalCheckpoint = sdc && !checkpointInserted ? checkpoint : "";
    const progressMarkup = totalTasks
      ? `<div class="sidebar-footer"><div class="progress-card">` +
        `<div class="progress-row"><span>Course progress</span>` +
        `<span id="progress-label">0/${totalTasks} tasks</span></div>` +
        `<div class="progress-track"><div class="progress-bar" id="progress-bar"></div></div>` +
        `</div></div>`
      : "";

    holder.innerHTML = `<aside class="sidebar" aria-label="Course navigation">` +
      `<div class="brand"><img class="brand-mark" src="${escapeHtml(logoUrl)}" ` +
      `alt="Zscaler logo"><div class="brand-copy">` +
      `<strong>${escapeHtml(courseId)}</strong>` +
      `<span>${escapeHtml(courseSubtitle)}</span></div></div>` +
      `<div class="sidebar-scroll"><div class="nav-label">Start here</div>` +
      startLinks.join("") +
      (labs.length || sdc ? `<div class="nav-label">Hands-on labs</div>` : "") +
      labLinks + finalCheckpoint + `</div>${progressMarkup}</aside>`;
  }

  function applyTheme(theme) {
    const value = theme === "dark" ? "dark" : "light";
    document.documentElement.dataset.theme = value;
    setStored(themeKey, value);
    document.querySelectorAll("[data-theme-icon]").forEach((icon) => {
      icon.textContent = value === "dark" ? "☀" : "☾";
    });
    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
      button.setAttribute("aria-label", `Switch to ${value === "dark" ? "light" : "dark"} mode`);
    });
  }

  function initTheme() {
    let prefersDark = false;
    try { prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches; }
    catch { /* matchMedia not supported */ }
    const saved = getStored(themeKey);
    applyTheme(saved === "light" || saved === "dark"
      ? saved : (prefersDark ? "dark" : "light"));
    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
      button.addEventListener("click", () => applyTheme(
        document.documentElement.dataset.theme === "dark" ? "light" : "dark"
      ));
    });
  }

  function initCopy() {
    document.querySelectorAll("[data-copy]").forEach((button) => {
      button.addEventListener("click", async () => {
        const text = button.dataset.copy || "";
        const previous = button.textContent;
        try {
          if (!navigator.clipboard?.writeText) throw new Error("Clipboard not available");
          await navigator.clipboard.writeText(text);
          button.textContent = "Copied";
          window.setTimeout(() => { button.textContent = previous; }, 1200);
        } catch {
          // Selection remains possible when Clipboard API is unavailable.
          button.textContent = text;
          window.setTimeout(() => { button.textContent = previous; }, 2000);
        }
      });
    });
  }

  function updateProgress() {
    if (!totalTasks) return;
    const completed = taskNumbers.filter((number) => getStored(keyForTask(number)) === "1").length;
    const label = document.getElementById("progress-label");
    const bar = document.getElementById("progress-bar");
    if (label) label.textContent = `${completed}/${totalTasks} tasks`;
    if (bar) {
      bar.style.width = `${Math.round(100 * completed / totalTasks)}%`;
      bar.setAttribute("role", "progressbar");
      bar.setAttribute("aria-valuemin", "0");
      bar.setAttribute("aria-valuemax", String(totalTasks));
      bar.setAttribute("aria-valuenow", String(completed));
      bar.setAttribute("aria-label", "Course progress");
    }
  }

  function initTasks() {
    document.querySelectorAll("[data-task-check]").forEach((input) => {
      const key = keyForTask(input.dataset.taskCheck);
      input.checked = getStored(key) === "1";
      input.addEventListener("change", () => {
        setStored(key, input.checked ? "1" : "0");
        updateProgress();
      });
    });
    updateProgress();
  }

  function initLightbox() {
    const dialog = document.getElementById("image-modal");
    if (!dialog) return;
    const modalImage = dialog.querySelector("img");
    const caption = dialog.querySelector("[data-modal-caption]");
    if (!modalImage) return;

    document.querySelectorAll("[data-lightbox]").forEach((button) => {
      button.addEventListener("click", () => {
        const thumbnail = button.querySelector("img");
        if (!thumbnail) return;
        modalImage.src = thumbnail.currentSrc || thumbnail.src;
        modalImage.alt = thumbnail.alt || "Expanded screenshot";
        if (caption) caption.textContent = button.dataset.caption || thumbnail.alt || "";
        if (typeof dialog.showModal === "function" && !dialog.open) dialog.showModal();
      });
    });

    dialog.querySelector("[data-modal-close]")?.addEventListener("click", () => dialog.close());
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) dialog.close();
    });
  }

  function initMenu() {
    document.querySelectorAll("[data-menu-toggle]").forEach((button) => {
      button.addEventListener("click", () => {
        const open = body.classList.toggle("nav-open");
        button.setAttribute("aria-expanded", String(open));
      });
    });
    document.getElementById("course-nav")?.addEventListener("click", (event) => {
      if (event.target.closest("a")) body.classList.remove("nav-open");
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") body.classList.remove("nav-open");
    });
  }

  function searchEntries() {
    const items = [
      { label: "Introduction", href: "index.html#overview" },
      { label: "Experience Center navigation", href: "index.html#navigation-guide" },
      { label: "Course index", href: "index.html#contents" },
    ];
    if (raw.labAccess) {
      const access = raw.labAccess === true ? {} : raw.labAccess;
      items.push({ label: access.title || "Lab access", href: access.href || "lab-access.html" });
    }
    if (sdc) items.push({ label: sdc.title, href: sdc.href });
    labs.forEach((lab) => {
      items.push({ label: `Lab ${lab.number} — ${lab.title}`, href: lab.href, keywords: lab.keywords });
      lab.tasks.forEach((task) => items.push({
        label: `${task.number} ${task.title}`, href: task.href, keywords: task.keywords,
      }));
      lab.explainers.forEach((explainer) => items.push({
        label: explainer.title || "Technical context",
        href: explainer.href || (explainer.id ? `${lab.href}#${explainer.id}` : lab.href),
        keywords: explainer.keywords || "",
      }));
    });
    if (Array.isArray(raw.search)) {
      raw.search.forEach((entry) => {
        if (entry?.label && entry?.href) items.push(entry);
      });
    }
    return items;
  }

  function initSearch() {
    const input = document.getElementById("global-search-input");
    const results = document.getElementById("global-search-results");
    if (!input || !results) return;
    const entries = searchEntries();

    function hideResults() {
      results.hidden = true;
      results.classList.remove("open");
      input.setAttribute("aria-expanded", "false");
    }
    function renderResults() {
      const query = input.value.trim().toLocaleLowerCase();
      if (!query) {
        results.innerHTML = "";
        hideResults();
        return;
      }
      const hits = entries.filter((entry) =>
        `${entry.label} ${entry.keywords || ""}`.toLocaleLowerCase().includes(query)
      ).slice(0, 8);
      results.innerHTML = hits.length
        ? hits.map((entry) => `<a href="${safeHref(entry.href)}">${escapeHtml(entry.label)}</a>`).join("")
        : '<div class="search-empty">No matches</div>';
      results.hidden = false;
      results.classList.add("open");
      input.setAttribute("aria-expanded", "true");
    }

    results.hidden = true;
    input.setAttribute("aria-expanded", "false");
    input.addEventListener("input", renderResults);
    input.addEventListener("focus", renderResults);
    input.addEventListener("keydown", (event) => {
      if (event.key === "Escape") hideResults();
      if (event.key === "Enter") {
        const first = results.querySelector("a");
        if (first && !results.hidden) {
          event.preventDefault();
          window.location.href = first.href;
        }
      }
    });
    document.addEventListener("click", (event) => {
      if (!event.target.closest(".global-search")) hideResults();
    });
  }

  function initIndexFilter() {
    const input = document.getElementById("lab-filter");
    if (!input) return;
    input.addEventListener("input", () => {
      const query = input.value.trim().toLocaleLowerCase();
      document.querySelectorAll(".lab-card, .checkpoint-card").forEach((card) => {
        const searchable = `${card.textContent} ${card.dataset.keywords || ""}`.toLocaleLowerCase();
        card.style.display = !query || searchable.includes(query) ? "" : "none";
      });
    });
  }

  function initialize() {
    renderNav();
    initTheme();
    initCopy();
    initTasks();
    initLightbox();
    initMenu();
    initSearch();
    initIndexFilter();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true });
  } else {
    initialize();
  }
})();
