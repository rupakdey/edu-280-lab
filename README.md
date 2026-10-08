# zscaler-web-lab-guide-template


See [EXPLAINER_PLAN_GUIDE.md](EXPLAINER_PLAN_GUIDE.md) for the full explainer-plan editing reference.

## Choosing technical explainers

Before generating a course, copy `explainer-plan-template.yaml` to `explainer-plan.yaml` in the **course repository**. Add one entry per concept; set `enabled: true` only for contexts you want learners to see. Use `lab: 4, placement: lab_intro` for a whole-lab explanation or `lab: 4, task: "4.2", placement: before_steps` for context directly before a task. Specify an `id`, `topic`, `depth`, `visual` and short `cover` list. An `enabled: false` entry stays a suggestion only.

Set `settings.generation` to `specified_only` (default) so no unrequested explainers are inserted. The builder must create the HTML explainer using `templates/components/technical-explainer.html`, then add a matching `labs[].explainers[]` link in `assets/js/course-data.js`. YAML is **not a browser asset**. When an explainer is already present in the published guide, update it rather than duplicating it.

Run `python -m pip install -r requirements-validation.txt` once locally, then `python scripts/validate.py --json-report validation-report.json` to check the plan. GitHub Actions installs the same dependency automatically.
