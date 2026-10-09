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

## Navigation Verification and Switching

- On the Introduction page, explain how to find **Account Settings → Settings → New Navigation Experience**, where the option is available; show the approved shared screenshot with a caption identifying it as illustrative. Some tenants or rollout stages may no longer allow returning to Original Navigation, so never promise that both options are available.
- Prefer a currently documented **help.zscaler.com** product/resource path; also give the learner a **Search Menu** keyword and, when useful, a direct official-documentation link.
- Do not copy menu paths from the source PDF without checking current official documentation. If official documents conflict, explain the discrepancy, use a relevant recent product-specific page as the primary reference, and offer Search Menu as fallback. Never invent a path or claim the PDF breadcrumb is current.
- Include source URLs in the generated guide for traceability; learners' live UI and entitlements may differ.

## Source Lab Topology and VM Access

- When the source PDF provides a topology, include the original **source topology** prominently in **Environment at a Glance**, preserving interface names, addresses, subnet relationships, and routing/service paths. A simplified SVG may supplement it, but must not replace the source technical diagram.
- Allow technical topology figures to use the full guide content width, subject to native-resolution/no-upscaling rules for raster images.
- Immediately below the topology, add a **VM access/credentials table** if the source explicitly gives VM or gateway usernames/passwords. Distinguish console credentials, RDP credentials and session-provided logins. Clearly mark fields that the source does not specify; never infer credentials.
- Do not publish session-specific passwords, provisioning keys, activation codes, or user secrets; refer learners to their session email/assigned environment. Warn when a documented default password must be changed.

## Screenshot Height and Aspect Ratio

- Standard screenshots: maximum width **two-thirds of guide maximum content width** and maximum height **the smaller of 1,490 CSS pixels or 80vh**. Apply both constraints together without stretching; preserve the intrinsic aspect ratio.
- Never upscale raster screenshots above their native size. The lightbox may display a larger view within viewport limits.
- Topology diagrams are an explicit width/height exception; use a dedicated `.topology-figure` class instead of forcing network drawings into ordinary screenshot dimensions.

## Explainer Plan (Course-Controlled Technical Context)

- Each course must include `explainer-plan.yaml`, copied from `explainer-plan-template.yaml`. Read it before writing any lab or technical context. Its purpose is to control **where, why, and how deeply** technical explainers are added.
- `settings.generation: specified_only` is the default: render only `explainers` entries with `enabled: true`. Entries with `enabled: false` are suggestions and must not appear in HTML or course-data navigation. `suggest_additional_topics: true` permits suggestions in build notes, **not automatic insertion** in this mode.
- `specified_plus_auto` may add carefully justified context beyond enabled entries; document each added explainer and avoid unnecessary concepts in straightforward labs. Do not silently override explicit disabled entries.
- A `lab_intro` explainer appears after lab objectives and before the first task; a task-specific `before_steps` explainer (with `task: "N.M"`) appears immediately before that task's numbered steps. Never displace or duplicate the Expected Result.
- Each enabled explainer must have a stable `id` matching its rendered HTML anchor (`id="..."`) and the corresponding `course-data.js` `labs[].explainers[]` record, so sidebar and global search can find it. When changing a pre-existing explainer, revise rather than duplicating it.
- Recommended word ranges: `brief` 50–100, `standard` 150–250, `detailed` 250–400, subject to replacing prose with a useful diagram or table. Explain **what/why/how it relates to the exercise**, not click-by-click steps.
- Valid visual hints: `none`, `flow_diagram`, `architecture_diagram`, `comparison_table`, `sequence_diagram`, or `auto`. The builder should select a visual only when it improves clarity. Never manufacture unsupported product details.
- Cite relevant official Zscaler documentation when adding product-specific architecture or behavior; keep source-derived claims distinct from verified external explanations. The course PDF remains authoritative for lab steps and values.
- The YAML is **build-time input only**: do not load it in the browser. Validate it with `scripts/validate.py` and maintain its references as the course is built.

## Diagram Contrast and Explainer Substance

- Network topologies must remain readable in light **and** dark website modes. If a source PDF diagram has a dark background with low-contrast labels or paths, provide an accurate high-contrast redraw as the primary diagram; keep the original as a clearly labelled optional source reference.
- When redrawing topology, preserve documented interface names, subnet/host ranges, WAN paths and device roles. Label conceptual routes as conceptual; do not invent cabling. Review readability at normal browser zoom and when enlarged.
- A technical-explainer heading and image caption **alone do not constitute an explainer**. A standard explainer must describe the mechanism, reason for the architecture/policy, and exactly how the upcoming lab tests it. Use a worked traffic example, comparison, sequence or decision model where appropriate.
- Clearly distinguish a product-wide capability from the specific rule configured in the lab. In particular, /32 network-of-one endpoint isolation and a CIDR-based subnet Reject rule are related but not identical.
- Use a concise course-specific navigation subtitle (for example, “ZTB Lab Guide”), while retaining the independent/unofficial notice in the Introduction and footer.
