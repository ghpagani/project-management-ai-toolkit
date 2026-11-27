# Data contract v1 / Contrato de dados v1

UTF-8 JSON, maximum 1,000,000 bytes and 64 nested objects/arrays (the root container counts as one), exact fields as in `examples/project.json`. Delimiters inside strings do not count. No duplicate keys, floats, nulls in input, free text, URLs, names, dates of birth, coordinates, credentials, or arbitrary metadata. Unknown fields are rejected. IDs are opaque synthetic codes: P/T/R/U followed by 3–6 ASCII digits. They do not establish anonymization. The caller must verify the source and classification independently. Only `synthetic` or `public_authorized` are accepted. All four modules are required in v1.

Schedule: at least one task; maximum 2,000 tasks and 20,000 edges; integer durations 0–36,500 days (zero means milestone); finish-to-start dependencies with zero lag; a single abstract calendar starting at day zero. Unknown predecessors, duplicates and cycles are rejected. No dates, resource leveling, actual progress or multiple calendars.

EVM: currency BRL/USD/EUR; all monetary fields in integer minor units (centavos/cents), 0–100,000,000,000,000; BAC > 0; PV and EV <= BAC, AC may exceed BAC. All must be cumulative at one status date and one baseline, checked externally. No conversion between currencies. Undefined ratios return null. CPI/SPI rounded half-up to 4 decimal places; EAC rounded to the nearest minor unit from unrounded inputs.

Reports in v0.1.1 add calculation fields to the existing JSON output. Schedule traces contain durations, predecessors, successors and formulas; risk traces include the operands and threshold. EVM includes exact ratio numerators and denominators and `rounded_to_zero` flags. A displayed zero can represent a positive ratio; never use displayed ratios for intermediate calculations. EAC assumes future work continues at current cost efficiency and is not a guaranteed final cost. Consumers that reject unknown output fields must update. The input contract is unchanged apart from the explicit depth cap.

Relatórios v0.1.1 acrescentam memória de cálculo: duração e dependências, fatores e limite dos riscos, numeradores e denominadores exatos de CPI/SPI e indicadores de arredondamento para zero. O EAC pressupõe que a eficiência de custos atual continue; não é custo final garantido. Consumidores que rejeitam campos adicionais precisam ser atualizados. A entrada mantém o contrato anterior, com limite explícito de profundidade.

Risks: probability and impact ordinal 1–5; threshold 1–25; response_assigned boolean. High means product >= threshold. RACI: each task at most once; role IDs unique within task; R/A/C/I/RA allowed; exactly one A and at least one R recommended. Missing task assignments are flagged. Max 2,000 entries in each list. No names or free text in outputs. Reports are still potentially sensitive.

CLI returns 0 for a completed review (findings may exist), 2 for rejected input/known policy blocks, 3 for I/O or unsupported input. No overwrite. Hard-link-capable output filesystem required. Input and output folders must be trusted and access-controlled.

Optional `--format md --lang en|pt-BR` produces a localized Markdown report with machine-readable JSON calculation sections; use a new `.md` output. Default remains JSON with a `.json` output. JSON field names and formulas stay in English. Reports and their calculation operands can be sensitive and require the same protection as inputs.

Opcionalmente, `--format md --lang pt-BR` gera relatório Markdown com títulos e orientações em português e seções de cálculo em JSON; use um arquivo `.md` novo. O padrão continua JSON, com extensão `.json`. Os nomes dos campos e fórmulas permanecem em inglês. Relatórios e operandos podem ser sensíveis e requerem proteção equivalente à entrada.
