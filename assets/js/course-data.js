/*
 * Zscaler Web Lab Guide — reusable course-data template.
 *
 * This is configuration, not site behavior. Keep the structure and replace
 * placeholders and sample-free empty arrays when generating a real course.
 * Source the factual content from the course guide / course manifest.
 *
 * Load order (on EVERY generated page):
 *   <script src="assets/js/course-data.js" defer></script>
 *   <script src="assets/js/site.js" defer></script>
 *
 * Do not use async: site.js must see LAB_GUIDE_COURSE before it initializes.
 *
 * Contract with assets/js/site.js:
 * - Lab numbers are positive integers. A lab's href points to lab-NN.html.
 * - Task numbers are dotted strings (e.g. "1.1"). Task anchor IDs should
 *   be task-1-1, task-1-2, etc., matching the section in the HTML.
 * - The checkbox data-task-check uses the dotted number (e.g. "1.1").
 * - Provide every real lab/task for complete sidebar/search/progress behavior.
 * - A course without SDC sets sdcAccess to null and sdc to false/omitted.
 * - Avoid putting passwords, tokens, or personal account details in this file.
 */

window.LAB_GUIDE_COURSE = {
  // Replace these values when generating an actual course.
  id: "{{COURSE_ID}}",
  title: "{{COURSE_TITLE}}",
  subtitle: "{{COURSE_EDITION}}",
  storagePrefix: "{{STORAGE_PREFIX}}",

  // Optional getting-started checkpoint. For a section on the index page:
  //   { title: "Lab Access", href: "index.html#lab-access" }
  // For a separate access page:
  //   { title: "Lab Access", href: "lab-access.html" }
  // Keep null if the course has no distinct access checkpoint.
  labAccess: null,

  // Optional SDC checkpoint; set null if no SDC is used.
  // When required, use:
  //   { title: "SDC access checkpoint", href: "sdc-access.html", beforeLab: 11 }
  // Mark applicable labs below with sdc: true.
  sdcAccess: null,

  // Populate one object for EACH actual numbered lab, ordered as in the course.
  // These are schema illustrations ONLY, not a real course or required values:
  //
  // {
  //   number: 1,
  //   title: "Example lab title",
  //   href: "lab-01.html",
  //   optional: false,
  //   sdc: false,
  //   keywords: "alternative terms for global search",
  //   tasks: [
  //     {
  //       number: "1.1",
  //       id: "task-1-1",
  //       title: "Example task title",
  //       href: "lab-01.html#task-1-1",
  //       keywords: "useful alternate search terms"
  //     }
  //   ],
  //   explainers: [
  //     {
  //       id: "context-sample",
  //       title: "Concept overview",
  //       href: "lab-01.html#context-sample",
  //       keywords: "architecture workflow"
  //     }
  //   ]
  // }
  labs: [],

  // Optional extra global-search items that are not already labs/tasks/explainers:
  // { label: "Environment topology", href: "index.html#environment", keywords: "network diagram" }
  search: []
};
