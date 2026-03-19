# GAP REPORT

## Current checkpoint status
- canonical v0.1 (`demo_cases.yaml`): 8/8 passed
- adversarial v0.1b (`demo_cases_v0_1b_adversarial.yaml`): 6/6 passed
- robustness v0.1c (`demo_cases_v0_1c_robustness.yaml`): 8/8 passed

## Contract status
This bundle aligns the written decision and trace outputs with the canonical schemas.

Implemented in this bundle:
- trace outputs use only schema-governed core fields
- decision outputs use only schema-governed core fields and include `trace_id`
- runner validates written outputs against the decision and trace schemas
- examples are intended to validate/fail exactly as documented
- `previous_trace_hash` now allows `null` for genesis traces

## Remaining limitations
- deterministic-first and fixture-driven
- safety heuristics remain intentionally narrow
- epistemic evaluation remains rule/fixture bounded
- richer internal/demo enforcement still exists in the comparison/report layer
- demo fixture YAMLs are still an internal runner contract, not the canonical output schema
- no production persistence, signing, auth, or execution gate
- finite suite coverage does not prove open-ended robustness
