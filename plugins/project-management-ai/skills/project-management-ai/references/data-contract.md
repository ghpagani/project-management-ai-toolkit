# Data contract v1 / Contrato de dados v1

UTF-8 JSON, maximum 1,000,000 bytes, exact fields as in `examples/project.json`. No duplicate keys, floats, nulls in input, free text, URLs, names, dates of birth, coordinates, credentials, or arbitrary metadata. Unknown fields are rejected. IDs are opaque synthetic codes: P/T/R/U followed by 3–6 ASCII digits. They do not establish anonymization. The caller must verify the source and classification independently. Only `synthetic` or `public_authorized` are accepted. All four modules are required in v1.

Schedule: at least one task; maximum 2,000 tasks and 20,000 edges; integer durations 0–36,500 days (zero means milestone); finish-to-start dependencies with zero lag; a single abstract calendar starting at day zero. Unknown predecessors, duplicates and cycles are rejected. No dates, resource leveling, actual progress or multiple calendars.

EVM: currency BRL/USD/EUR; all monetary fields in integer minor units (centavos/cents), 0–100,000,000,000,000; BAC > 0; PV and EV <= BAC, AC may exceed BAC. All must be cumulative at one status date and one baseline, checked externally. No conversion between currencies. Undefined ratios return null. CPI/SPI rounded half-up to 4 decimal places; EAC rounded to the nearest minor unit from unrounded inputs.

Risks: probability and impact ordinal 1–5; threshold 1–25; response_assigned boolean. High means product >= threshold. RACI: each task at most once; role IDs unique within task; R/A/C/I/RA allowed; exactly one A and at least one R recommended. Missing task assignments are flagged. Max 2,000 entries in each list. No names or free text in outputs. Reports are still potentially sensitive.

CLI returns 0 for a completed review (findings may exist), 2 for rejected input/known policy blocks, 3 for I/O or unsupported input. No overwrite. Hard-link-capable output filesystem required. Input and output folders must be trusted and access-controlled.
