# Threat model / Modelo de ameaças

Assets: input records, project budgets, schedules, identities, outputs, repository history, credentials and host context. Trust boundaries: user → host/LLM → local engine → private filesystem; build → CI → downloadable ZIP. Host/LLM, OS and deployment policy are outside the engine boundary.

| Threat / Ameaça | Implemented mitigation / Mitigação | Residual risk / Risco residual |
|---|---|---|
| Prompt injection | strict numeric schema; no free-text documents; no agent execution in core | host may read instructions before validation; isolate intake |
| Data disclosure | no network code; no raw input echoes; public/synthetic gate | false declarations, numeric covert channels, model context and outputs |
| Filesystem overwrite | exclusive hard-link publication; new output required | parent-directory races, links/junctions, crash remnants; trusted directory needed |
| Parser/resource abuse | byte, row, edge and numeric bounds; reject duplicate keys | process-level quotas/timeouts still needed |
| Supply chain | stdlib only, allowlisted ZIPs, checksums | Python/OS/CI actions and release account compromise; signatures and SBOM pending |
| Access control | no service or shared database | host ACLs, tenant isolation, SSO, encryption not implemented |
| Wrong decisions | deterministic formulas, explicit limitations | bad baseline, missing evidence, misuse of metrics |

No threat is considered eliminated. Threat tests use synthetic markers only. Do not weaken sandbox or egress controls. Institutional deployment requires a separate architecture review and independent assessment.
