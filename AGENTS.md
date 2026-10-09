# Zscaler Web Lab Guide Builder Instructions

Before changing or generating any course content:

1. Read LAB_GUIDE_STANDARD.md completely.
2. Read QA_CHECKLIST.md completely.
3. Treat templates/ and assets/css/style.css as the canonical design system.
4. Do not redesign the site unless the user explicitly requests a design change.
5. Treat the source PDF as a source of technical facts, screenshots,
   configuration values, task intent and expected outcomes — NOT as a
   visual/layout template.
6. Rewrite instructions for clarity and brevity.
7. Use the approved numbered-step task pattern.
8. Place each screenshot immediately after the instruction it illustrates.
9. Treat source screenshots as configuration/reference evidence, not authoritative
   navigation maps. If a screenshot shows legacy navigation, preserve the useful
   configuration view but use verified current Experience Center navigation;
   otherwise provide a Search Menu keyword.
10. Do not invent product paths, settings, values or expected results.
11. Run the complete QA checklist before export.

## Source of Truth / Precedence

When building or modifying a guide, follow this order of authority:

1. LAB_GUIDE_STANDARD.md
2. reference/
3. templates/
4. assets/css/style.css and assets/js/site.js
5. Source course PDF

The source PDF is authoritative for:
- technical content
- task intent
- screenshots
- configuration values
- expected outcomes

The source PDF is NOT authoritative for:
- visual design
- page layout
- numbering style
- screenshot placement
- navigation presentation
- instructional writing style

If the PDF conflicts with this repository's design system,
the repository design system wins.

## Mandatory reusable refinements

- Read the Navigation Verification, Source Lab Topology/VM Access, and Screenshot Height sections of LAB_GUIDE_STANDARD.md.
- Use current help.zscaler.com product pages to substantiate a documented resource/policy route; provide a Search Menu fallback, identify conflicting documentation, and link sources.
- When present, place the original source topology in the Environment section, with any explicit VM credentials table immediately below. Do not infer credentials.
- Keep standard screenshots within 2/3 guide width and min(1490px,80vh) height at natural aspect ratio; allow full-width source topology diagrams.

## Course-Specific Explainer Plan (Mandatory)

- Read `explainer-plan.yaml` (generated course) or `explainer-plan-template.yaml` (reusable template) before drafting a lab. If a new course lacks its plan, copy the template with `explainers: []`; do not invent an explainer list.
- Treat `enabled: true` entries as approved content requirements; `enabled: false` entries are suggestions only and must not be rendered or added to search/navigation.
- Use `placement: lab_intro` after objectives and before tasks, or `placement: before_steps` for the named task (`task: "N.M"`). Reuse `templates/components/technical-explainer.html` and preserve the standard task structure.
- Match each explainer's stable YAML `id` with the HTML `id` and `assets/js/course-data.js` link. Reuse already-published explainers rather than duplicating them.
- `specified_only` is the default: recommendations belong in build notes for user review, never auto-inserted. Follow the depth and visual preferences in the plan and the design standard.


## Concept-First Technical Context and Verified Navigation (Mandatory)

- Treat a technical-explainer request as a **teaching requirement**, not a request for a diagram caption. Open with a plain-language definition of the technology/policy, then explain the operational problem it solves, its decision/enforcement mechanism, and its real-life consequences. Only after that map the concept to the exact lab task and its validation.
- For `standard` and `detailed` explainers, use meaningful subsections (e.g., **What it is**, **Why it matters**, **How it works**, **How this lab demonstrates it**) and a worked example or comparison. An explainer that consists chiefly of exercise-specific settings does not satisfy the requirement.
- For policies, distinguish **policy intent**, **matching criteria**, **action**, **enforcement point**, **operational tradeoffs**, and **what the test actually proves**. Do not conflate a DNS Override with Redirect or a routing policy with a firewall permit rule.
- Documentation links and configuration breadcrumbs must be checked against the **relevant action and current product-specific article**, not merely an article about the same product. Write a **complete breadcrumb**, starting with the product root (e.g. **Zero Trust Branch → Resources → Objects**), rather than an abbreviated menu suffix. Link directly to the article used to verify the breadcrumb.
- For each actionable navigation element, provide both the verified path and a **Search Menu** keyword. If documentation conflicts, prefer the newer article that explicitly states the full path; if still uncertain, label the path as potentially version-dependent instead of inventing certainty.
- Perform a course-wide navigation audit before publication, including asset discovery, object management, site policy tabs, firewall policy screens, and routing policy screens; validate the page/document match, not just URL reachability.
- Treat the source PDF as authoritative for exercise values and intended outcomes, while official help.zscaler.com material provides externally verified product background and navigation. Distinguish lab-specific observations from general product capabilities.
