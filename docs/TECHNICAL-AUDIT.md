# Technical audit / Auditoria técnica

2026-11-27; scope: local v0.1.0 commit e1ca09c, Windows, Python 3.12.10. This is an initial independent review, not a completed certification or independent penetration test.

The forward/backward CPM equations match the stated finish-to-start, zero-lag, single-calendar model. A synthetic diamond with two critical branches and a disconnected shorter terminal returns duration 6 and float 4 for the shorter terminal. Existing tests reject cycles, unknown, self and duplicate dependencies. Dates, actual progress, resource constraints and critical-path enumeration are outside the model.

EVM uses integer minor units and Decimal with half-up rounding. BAC=3, PV=2, EV=2, AC=1 gives CPI 2.0000, EAC 2, ETC 1 and VAC 1; the exact EAC is 1.5. EAC uses unrounded operands. At the supported extreme BAC=AC=10^14, EV=1, the exact EAC is 10^28; displayed CPI rounds to 0.0000 despite being positive. Consumers must not derive EAC from displayed CPI. The interpretation of a forecast is conditional on a valid baseline and the stated assumption; zero EV or AC yields no forecast. SV is monetary, not a time delay.

Risk thresholds are inclusive; RACI counts RA in both roles and flags multiple accountable roles. Both depend on user-supplied assertions, not evidence of ownership, response effectiveness or decision authority.

The candidate adds schedule and risk operands and EVM ratio fractions, formulas and rounding warnings. It retains the original fields but strict consumers may reject additional output fields. Optional Markdown reports provide English or Portuguese headings and guidance; calculation sections use the stable English JSON field names. Installation in an actual agent, release integrity provenance, concurrency under hostile directories and full cross-platform CI remain unverified. No numerical defect was demonstrated by these cases; this is not an exhaustive proof.
