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
