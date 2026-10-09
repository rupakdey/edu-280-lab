# EDU-280 targeted refinements

Updates the files only as listed in this package. Apply to edu-280-web-lab-guide-v2 / pilot-intro-lab1.

- `index.html`: readable light-background network topology as primary, original source topology retained behind a comparison disclosure, and substantial HA/VRRP/WAN architecture explanation.
- `lab-01.html`: expanded HA explainer and mechanism description.
- `lab-02.html`: clear macrosegmentation context including real subnet ranges and Drop/Skip evaluation.
- `lab-04.html`: detailed microsegmentation explanation showing how network-of-one /32 enables intra-VLAN gateway enforcement; compares the Lab 4 actual /24-to-/24 Reject match to Lab 2. Airgap-Lite and Airgap+ exceptions identified.
- `assets/images/course/ztb-readable-lab-topology.svg`: new high-contrast detailed vector diagram retaining source attributes; conceptual connections are labelled as such.
- `assets/images/course/lab04-microsegmentation.svg`: improved visual comparison diagram.
- `assets/js/course-data.js` and `course.yaml`: sidebar subtitle now `ZTB Lab Guide`. Unofficial guide disclaimer remains in page.
- `explainer-plan.yaml`: recorded deepened HA/macro/micro contexts.
- Standard and checklist updated to require readable diagrams and substantive, product-specific explainers.

No other labs or scripts are modified. No confidential source PDF is included. Retain private repository visibility.
After uploading, run GitHub Actions > Validate Lab Guide and visually review index, lab 01, 02, 04 in both themes.
