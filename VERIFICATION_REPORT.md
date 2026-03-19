# VERIFICATION REPORT

Generated: 2026-03-11T18:17:56Z
Bundle root: `KPT_2_3_2026-03-11_v6_1`

## Verified results
- canonical v0.1: 8/8 passed
- adversarial v0.1b: 6/6 passed
- robustness v0.1c: 8/8 passed

## Conformance gate
- examples checked: 2
- trace files checked: 29
- decision files checked: 29
- overall pass: yes

## Notes
- This bundle re-ran the reference suites and conformance validator after adding the origin/axiom continuity documents.
- No schema or runtime decision contract was widened beyond the already accepted genesis-trace `previous_trace_hash = null` exception in v6.
- Markdown and JSON sources remain authoritative.
