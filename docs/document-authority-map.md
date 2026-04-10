# KPT 2.3 Public Repo Authority Map

**Document date:** 2026-04-10  
**Status:** Current authority classification for the public repo

---

## 1. Purpose

This file explains which public repo materials define the KPT 2.3 public contract, which materials are explanatory, and which materials are historical, companion, or example surfaces.

This map governs the **public repo claim surface**. It does not imply that the public repo is a full implementation disclosure.

---

## 2. Normative public sources

These are the primary public contract-defining sources for KPT 2.3 in this repo:

- `docs/core-standard.md`
- `docs/quickstart.md`
- `docs/conformance-methodology.md`
- `docs/decision-result-schema.md`
- `docs/trace-schema.md`
- `docs/basis-codes-registry.md`
- `schemas/evaluation-payload.schema.json`
- `schemas/decision-result.schema.json`
- `schemas/trace.schema.json`

If another public file conflicts with these sources, these sources win.

---

## 3. Informative public sources

These explain, demonstrate, compare, or operationalize the standard, but do not override the normative public contract:

- `docs/implementation-guide.md`
- `docs/reference-middleware-spec.md`
- `docs/reference-middleware-pseudocode.md`
- `docs/kpt-engine-v0_1-architecture-note.md`
- `docs/epistemic-humility-axiom.md`
- `docs/diagrams/*`
- `examples/*`
- `reference-engine/*`
- `tests/demo_cases*.yaml`

These materials are informative even when they are technically useful.

---

## 4. Historical, origin, and companion materials

These preserve lineage, companion context, or historical rationale. They are public, but they are not the core public contract surface:

- `origin/*`
- `origin/current/*`
- historical checkpoint or release notes
- reconstructed audit companions
- archive-style or appendix-style materials

These materials may help explain continuity, but they must not be read as a substitute for the normative public sources.

---

## 5. Interpretation rule

Use this order when reading the public repo:

1. normative public sources
2. informative public sources
3. historical / origin / companion materials

Do not treat examples, checkpoint notes, or companion artifacts as stronger than the public standard.

---

## 6. Repo-boundary rule

The public repo is:
- a claim surface
- a category surface
- a vocabulary surface
- an authorship surface
- a protection surface

The public repo is not:
- a complete internal implementation dump
- a complete private proof pack
- a full runtime-core disclosure
- a production-complete platform export
