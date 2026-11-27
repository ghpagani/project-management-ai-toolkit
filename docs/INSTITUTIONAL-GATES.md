# Institutional acceptance gates / Critérios de aceitação institucional

All gates below are PENDING. No PADF or other institutional data was used. A private personal repository is not an approved institutional environment.

1. Governance: written IT/security/privacy authorization, asset owner, data classification and use case, applicable country/jurisdiction analysis, IP ownership and retention/deletion policy.
2. Data flow: map model, tools, connectors, memory, logs, backups, caches, subprocesses, egress, regions and subprocessors; assess cross-border transfers, vendor terms and contracts. No confidential inputs to consumer cloud agents.
3. Isolation: approved endpoints; SSO/MFA; least privilege RBAC; tenant/project segregation; managed secrets; encryption in transit and at rest; isolated compute; deny-by-default egress; controlled exports. Test actual enforcement independently of prompts.
4. Assurance: threat modeling, independent code review, SAST, dependency/SBOM scanning, signed release provenance, adversarial tests, penetration test, DLP and incident-response exercise. Fix critical/high risks or document formal risk acceptance by authorized owners.
5. Pilot: synthetic/public only initially; benchmark accuracy and time saved; approval before expanding classification. No claims of legal compliance or zero risk. Re-evaluate on each release and host change.

PT-BR: todos os requisitos estão pendentes; a versão atual não implementa SSO, DLP, criptografia própria, segregação multiusuário ou controle de rede. A aprovação deve ser formal e acompanhada de evidências de testes. Dados de beneficiários, proteção, migração, salários e parceiros confidenciais não devem entrar nesta prévia.
