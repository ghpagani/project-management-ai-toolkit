# Project Management AI Toolkit

v0.1.0 — independent public preview. Original MIT-licensed code and guidance for project management, with deterministic CPM, EVM, ordinal risk and RACI review. No external dependencies or network calls in the engine. **Synthetic or explicitly authorized public data only. Not approved for sensitive institutional data.** A skill is not a security boundary.

Python 3.11+ (3.11–3.14 intended; see validation report for actual test environment). Use a supported, patched Python runtime. From the repository root, run `python -B -m unittest discover -s tests -v` and `python scripts/validate_package.py`. Create a private output folder outside the repository, then run:

```sh
python plugins/project-management-ai/skills/project-management-ai/scripts/review.py --input plugins/project-management-ai/skills/project-management-ai/examples/project.json --out /path/to/private/demo.json
```

The example is synthetic. JSON only, no free text. Monetary amounts use integer cents. The output filesystem must support hard links. No automatic uploads, approvals, changes or project certification. Read SECURITY.md and docs/INSTALL.md before installation. The host may be cloud-based even when Python is local to its execution environment.

See [Português](README.pt-BR.md), [data contract](plugins/project-management-ai/skills/project-management-ai/references/data-contract.md), [sources](docs/SOURCES.md), [threat model](docs/THREAT-MODEL.md), [institutional gates](docs/INSTITUTIONAL-GATES.md), [roadmap](ROADMAP.md) and [validation](docs/VALIDATION.md). No affiliation with PMI, PM4NGOs, EU or any employer.
