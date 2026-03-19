# KPT 2.3 Document Authority Map

**Document date:** 2026-03-11  
**Status:** Current authority classification for this checkpoint bundle

## Normative sources

These are the contract-defining sources for this bundle:

- `schemas/evaluation-payload.schema.json`
- `schemas/decision-result.schema.json`
- `schemas/trace.schema.json`
- `docs/quickstart.md`
- `docs/conformance-methodology.md`
- `docs/decision-result-schema.md`
- `docs/trace-schema.md`
- `docs/basis-codes-registry.md`
- `docs/core-standard.md`

The epistemic humility axiom is normative in this bundle through `docs/core-standard.md` and `docs/quickstart.md`, not as a standalone contract file.

Interpretation rule:

- if runtime demo behavior conflicts with these sources, the normative sources win
- the only deliberate schema correction in this bundle is `previous_trace_hash: null` for genesis traces

## Informative sources

These explain, demonstrate, or operationalize the standard, but do not override the normative contract:

- `reference-engine/README.md`
- `reference-engine/GAP_REPORT.md`
- `reference-engine/run_demo.py.pseudocode`
- `docs/reference-middleware-spec.md`
- `docs/reference-middleware-pseudocode.md`
- `docs/kpt-engine-v0_1-architecture-note.md`
- `docs/epistemic-humility-axiom.md`
- `docs/diagrams/*`
- `tests/demo_cases*.yaml`
- `pdf-pack/*`
- `origin/*`
  - includes `origin/current/KPT_2_2_2_origin_story_ET_2026-02-25.pdf` as the preserved source text for the origin rationale
  - includes `origin/current/KPT_origin_to_standard_bridge_2026-03-11.md` as the continuity bridge into KPT 2.3 wording
- `artifacts/*`

## Internal demo-fixture contract

The following files intentionally retain a richer internal/demo fixture contract for comparison reporting:

- `reference-engine/demo_cases.yaml`
- `reference-engine/demo_cases_v0_1b_adversarial.yaml`
- `reference-engine/demo_cases_v0_1c_robustness.yaml`
- mirrored copies under `tests/`

These demo fixtures are not the canonical trace/decision output schema.
They drive runner comparisons and richer report-layer behavior.

## Release criterion

A checkpoint bundle should not be treated as contract-clean unless all three conditions hold:

1. examples validate as intended
2. generated decisions validate
3. generated traces validate
