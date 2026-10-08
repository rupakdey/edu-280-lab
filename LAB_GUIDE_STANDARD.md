# Zscaler Web Lab Guide Design Standard

## Core Layout

- Use a wide, desktop-first layout matching the approved EDU-200/EDU-202 design.
- Provide persistent left-side course navigation.
- Provide global course search and a Quick Filter on the Course Index.
- Support light and dark modes.
- Display the floating Zscaler logo consistently.
- Hero/banner styling must match the approved reference design.
- Preserve the approved Course Introduction structure.
- Preserve the approved Experience Center Navigation section structure.
- Preserve the approved SDC checkpoint layout.
- SDC/preconfigured labs must be visually distinguished from hands-on configuration labs.
- Keep the author line and unofficial-learning-aid disclaimer consistent.

## Task Design

- Use simple numbered task steps. Never reproduce PDF nested numbering such as a/b/c or i/ii/iii.
- Treat the source PDF as a source of technical information, not as a layout or visual-design template.
- Rewrite instructions for clarity, brevity, and learner readability.
- Preserve all technically important configuration values.
- Use tables for dense configuration rather than long prose.
- End each task with a clear **Expected Result** block.
- Course-specific content may change; the approved design system must not change unless explicitly requested.

## Screenshots and Media

- Place each screenshot immediately after the step or instruction it illustrates.
- Never collect all screenshots at the bottom of a task.
- Treat source screenshots as configuration/reference evidence, not authoritative navigation maps.
- If a source screenshot shows legacy navigation, preserve the useful configuration view but use verified current Experience Center navigation; otherwise provide a Search Menu keyword.

## Navigation

- Prefer verified current Experience Center navigation.
- Provide Search Menu guidance for Zscaler policies, resources, and features when it improves usability.
- If a current navigation path cannot be verified, provide an appropriate Search Menu keyword rather than inventing a path.
- Navigation guidance should be concise and should not overwhelm the actual task instructions.

## Technical Explainers

- Add technical explainers only when they materially improve understanding of the task.
- Keep technical explainers concise and high-level.
- Prefer diagrams, object relationships, flows, and compact visual explanations over long blocks of prose.
- Keep technical context visually separate from the numbered hands-on instructions.
- Technical explainers should help learners understand **why** they are configuring something, not duplicate the configuration steps.

## Body Text Width

- Normal explanatory paragraphs beneath headings should use the full available content width unless the approved reference layout intentionally places them inside a column.
- Do not apply narrow `max-width` constraints to ordinary explanatory text.

## Screenshot Sizing

- Screenshots must not exceed two-thirds of the maximum guide content width.
- Images must never be enlarged beyond their native resolution.
- Images may scale down responsively when the available viewport or column is narrower than the image.
