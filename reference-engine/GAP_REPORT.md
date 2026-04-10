# Reference Engine Status Note

## Current public reference-engine status

Public suite results currently shown in this repo:
- canonical v0.1 (`demo_cases.yaml`): 8/8 passed
- adversarial v0.1b (`demo_cases_v0_1b_adversarial.yaml`): 6/6 passed
- robustness v0.1c (`demo_cases_v0_1c_robustness.yaml`): 8/8 passed

## What this reference-engine surface currently demonstrates

The public reference engine currently demonstrates that:
- written decision outputs align with the public decision schema
- written trace outputs align with the public trace schema
- runner validation checks generated outputs against those schemas
- public example fixtures are intended to validate or fail exactly as documented
- `previous_trace_hash` may be `null` for genesis traces under the current public schema

## What this surface does not claim

This reference-engine surface does not claim:
- full runtime-core disclosure
- production persistence
- signing or cryptographic attestation
- authentication or authorization enforcement
- production execution gating
- open-ended robustness proof
- complete internal enforcement disclosure

## Current limitations

Current limitations of the public reference engine include:
- deterministic-first and fixture-driven behavior
- intentionally narrow safety heuristics
- rule-bounded epistemic evaluation
- comparison and report logic that is still demo-oriented
- demo fixture YAMLs that remain a runner contract, not the canonical output schema
- finite suite coverage that should not be read as proof of general robustness

## Interpretation rule

Read this file as a public status note for the reference-engine surface.

It is not a claim that the public repo exposes the full implementation, the full proof machinery, or a production-complete platform.
