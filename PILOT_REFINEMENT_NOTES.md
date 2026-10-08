# EDU-280 pilot refinements — 2026-10-09

This patch intentionally preserves the existing pilot page layout and all Lab 1 configuration values.

1. Introduction: adds the documented Account Settings navigation selector and reuse of the shared screenshot. The image includes a rollout notice that may be stale; no assertion is made that switching back to Original is always possible.
2. Source topology: extracts the original lab topology image from page 9 of the source PDF, displays it full-width in the Environment section, and retains the conceptual SVG in a secondary disclosure.
3. VM access table: directly under source topology, lists gateway console credentials (Lab 1), separate Windows RDP credentials (Lab 3), and indicates other Skytap VM credentials are not stated in the PDF. Session-specific passwords remain out of the guide.
4. Proportional screenshot bounds: no more than 1120px maximum width and min(1490px,80vh) maximum height for screenshots, with no upscaling; topology excepted.
5. Official navigation references: Sites path from https://help.zscaler.com/zero-trust-branch/adding-site; HA fallback from https://help.zscaler.com/zero-trust-branch/creating-zero-trust-branch-high-availability-cluster; ZPA provisioning keys path from https://help.zscaler.com/zpa/about-connector-provisioning-keys. Two official ZTB documents provide different top-level routes, so both are acknowledged rather than inventing a single universal UI path.

Maintain this repository as private because the source content is marked confidential.
