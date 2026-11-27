# Decisions / Decisões

- Preserve v0.1.0 contracts and offline engine while reviewing; do not label an unfinished audit as v0.1.1.
- Treat model instructions and declared classification as guidance, not authorization, DLP or a sandbox. Trusted filesystem and egress restrictions are deployment prerequisites.
- Keep formulas and examples original; link third-party references instead of incorporating proprietary or noncommercial text under MIT.
- Prefer future versioned module contracts and explicit local transfer, subject to separate security review. SBOM and signing require a release identity and a verifiable distribution process; checksums alone are not signatures.
- SBOM: the builder creates a reproducible CycloneDX 1.5 file inventory per archive and adds its hash to SHA256SUMS. Its scope is archive members only: it does not inventory Python, OS, CI actions, build tools or transitive platform components, and does not establish provenance. Schema validation by an independent tool remains pending. Signing/attestation requires a controlled identity, verification instructions and independent validation; neither is implemented.
