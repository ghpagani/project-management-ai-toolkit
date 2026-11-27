# Development backlog / Backlog de desenvolvimento

Status: proposed, not a release commitment. Each item requires documented assumptions, synthetic fixtures, negative cases, independent review and security assessment.

## v0.1.1 candidate

1. Complete adversarial filesystem and parser tests, including Windows junctions, race conditions and resource bounds without bypassing sandbox controls.
2. Pin verified GitHub Actions to immutable SHAs; review release source provenance; scan complete Git history without exposing findings; assess SBOM generation and signing/verification workflow.
3. Verify CI matrix and actual installation in supported agent hosts, without broadening permissions. Test unsupported hard links and cleanup.
4. Add calculation trace for CPM, EVM and risk, including precision, operands and assumptions; retain v1 compatibility or version the report deliberately. Clarify rounded-zero ratios.
5. Complete bilingual documentation, a versioned financial-toolkit contract and risk review. Define data minimization and prohibit automatic transmission.

## v0.2 and later

- WBS/EAP: hierarchical deliverables, validation and baseline traceability.
- PERT: explicit distribution assumptions, expected duration and uncertainty; no claim of a probabilistic project finish without a validated model.
- Calendars and milestones: working calendars, holidays, timezone and date boundary semantics; milestone dependencies.
- Capacity and allocation: units, calendars, overallocation and competing work; explain that CPM does not level resources.
- Change control and stakeholders: versioned decisions, owners, approvals and privacy-minimized identifiers.
- Agile/hybrid and flow: configurable work states, throughput, cycle time and WIP, transparent sampling and no cross-team velocity ranking.
- Programs and portfolios: aggregation rules, dependencies, double-count protection and decision traceability.
- Executive reports: reproducible sources, date, uncertainty, caveats and human approval.
- Monitoring and evaluation: versioned indicator definitions, disaggregation safeguards and opt-in interfaces; no automated transfer.

Institutional gates in INSTITUTIONAL-GATES.md remain pending for every version until explicitly assessed and approved.
