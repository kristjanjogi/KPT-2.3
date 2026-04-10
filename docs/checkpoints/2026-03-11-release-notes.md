# RELEASE NOTES

## KPT 2.3 Technical Checkpoint Bundle v6.1 — 2026-03-11

Bundle name:
- `KPT_2_3_2026-03-11_v6_1`

This bundle includes:
- the documented KPT 2.3 standard
- schema and guidance layers
- licensing and conformance control files
- a working reference-engine v0.1
- verified suite outputs for canonical, adversarial v0.1b, and robustness v0.1c cases
- schema-clean written decision and trace outputs
- an explicit conformance report for examples and generated outputs
- an explicit origin-to-standard bridge for the epistemic humility principle

## Verified suite results
- canonical v0.1: 8/8 passed
- adversarial v0.1b: 6/6 passed
- robustness v0.1c: 8/8 passed

## Conformance result
- expected-valid example traces: pass
- expected-invalid example traces: fail as expected
- generated trace outputs: 29/29 valid
- generated decision outputs: 29/29 valid

## v6.1 changes
- preserved the uploaded KPT 2.2.2 origin story PDF inside `origin/current/`
- added `docs/epistemic-humility-axiom.md`
- added `origin/current/KPT_origin_to_standard_bridge_2026-03-11.md`
- made the epistemic humility principle explicit in `docs/core-standard.md`
- added the same minimum-contract explanation to `docs/quickstart.md`
- clarified the authority map so the axiom is normative through the standard and quickstart, not by a separate contract file
- refreshed package metadata for the v6.1 documentation checkpoint

This remains a technical checkpoint bundle, not a production release.

Markdown and JSON sources are authoritative.
PDF-pack, origin materials, and signing-history artifacts are retained as archival convenience materials.
