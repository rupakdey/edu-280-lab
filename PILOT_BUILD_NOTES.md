# EDU-280 Web Lab Guide — Pilot Package

## Scope and sources

This is the **pilot**, not the complete EDU-280 course. It is based on the user-provided *Zscaler Zero Trust Branch (EDU-280) Hands-on Lab Guide*, Rev. 2.3 (August 2026). The source PDF **is not included**.

- `index.html` — Introduction, course outcomes, current-navigation/search guidance, conceptual lab topology, Lab 0 access checkpoint, and **all nine numbered labs** listed in the index.
- `lab-01.html` — Source Lab 1 **Tasks 1.1–1.4 only**: create site, activate active/standby gateways, and configure site-level settings/ZPA App Connector. Source Tasks 1.5–1.9 are not built.
- Labs 2–9 — shown as **planned** in the index (Labs 7–9 clearly marked **optional**). No incomplete/fake lab pages are generated.
- `assets/js/course-data.js` — includes only the **published** Lab 1 in `labs[]`; planned labs are searchable via links to their Course Index anchors. Progress tracking therefore counts **four pilot tasks**, not the full course.
- `assets/images/course/` — one original, editable SVG conceptual topology diagram and contextual screenshots from the source PDF for the published tasks.

## Installation

On branch `pilot-intro-lab1` in `edu-280-web-lab-guide-v2`, extract the **updates-only** ZIP into the repository root, preserving paths. Add/commit `index.html`, `lab-01.html`, `assets/js/course-data.js`, the entire `assets/images/course/` directory, and this note. No existing `site.js`, `style.css`, validators, approved references, components, or `course.yaml` need replacing.

You can also open `index.html` locally to review the static guide. GitHub Pages preview/publishing should only be enabled when sharing/publication rights are settled.

## Validation and review

The unchanged repository validator v2 passed the assembled pilot with **0 errors / 0 warnings**. It validates structural integrity, not the full live UI or correctness of cloud configuration. Before considering the pilot approved, review it in a browser at desktop and mobile widths: layout, light/dark mode, sidebar, search, Quick Filter, task checkboxes, copy controls, lightbox, and the actual training tenant's current menu paths.

## Confidentiality and navigation

The source guide identifies itself as **Zscaler confidential/proprietary**. Keep the repository private and obtain any required authorization before publishing the adapted guide or embedded screenshots. Never commit actual POD passwords, activation codes, or App Connector provisioning keys. Source screenshots show older portal labels; the guide uses **Search Menu** when live navigation cannot be verified.

The topology is an explanatory diagram derived from the source scenario, not an authoritative port-by-port wiring specification. Values presented in the instructions come from the source text/screenshots; follow instructor guidance for any differences in your live POD.
