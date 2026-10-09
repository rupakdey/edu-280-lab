# EDU-280 — Labs 2–6 build notes

This update adds Labs 2–6 **and** completes source Lab 1 Tasks 1.5–1.9, because the segmentation/routing work assumes those LAN/WAN interfaces have been configured. The previously approved pilot shell, global styles and JavaScript are preserved.

- Course index and `assets/js/course-data.js` now publish Labs 1–6. Labs 7–9 remain visibly planned and optional.
- Lab 3 Tasks 3.3 and 3.4 are marked **optional within Lab 3**, in keeping with the source.
- Enabled explainers: Lab 2 macrosegmentation, Lab 4 microsegmentation, Lab 5 PBR, Lab 6 DNS. No extra Lab 3 explainer.
- Original PDF UI screenshots have been extracted as individual high-quality images and placed beside relevant instructions.
- New concept diagrams are course-specific editable SVGs; they illustrate concepts rather than being asserted as exact screenshots.
- Zscaler Help Portal guides are linked to navigation hints. New UI labels may vary; Search Menu remains the fallback.
- The lab source PDF was **not included** in the ZIP. Source content and screenshots are marked confidential; keep the repository private unless publication rights are confirmed.
- The PDF title for Lab 6.1 says redirect, but its policy action is **Override**. The HTML makes that distinction explicit.
- The PDF shows DHCP-assigned OT2 addresses and variable Adobe/CDN IPs. The HTML requires learners to observe their live addresses rather than copying examples.
- Gateway name formatting in the source varies (`gw-01` vs `gw-1`); use the actual gateway selections visible in your site when configuring PBR.

After installation, validate via `python -m pip install -r requirements-validation.txt` then `python scripts/validate.py --json-report validation-report.json`. Review rendered pages, screenshots and navigation in the browser before class release.
