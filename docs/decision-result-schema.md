# KPT 2.3 Decision Result Schema

File: `schemas/decision-result.schema.json`

**Author:** Kristjan Jõgi  
**Status:** Normative explanatory note  
**Authority class:** Normative explanatory document when read together with the schema file.

This schema defines the normalized decision object used by a KPT-aligned decision layer or reference middleware pattern after evaluating a candidate output.

It exists to ensure that decision assignment, enforcement mapping, and trace linkage are represented in a consistent structure.

## Required top-level fields

- `decision_state`
- `basis_codes`
- `enforcement_action`
- `trace_id`

## Optional but strongly expected fields

- `qualification_type`
- `rationale`

In practice:

- `qualification_type` is required for `qualify`
- `rationale` should be present for operational decisions in governed contexts, and is explicitly required by this schema for `qualify`, `refuse_assert`, and `refuse_help`

## Design intent

The schema preserves several KPT 2.3 distinctions:

- `decision_state` describes what the output is
- `enforcement_action` describes what the system does because of that status
- `trace_id` links the result to an already written evaluation trace
- schema validity does not itself authorize execution

It is also intentionally narrower than the richer report layer used by the public reference engine.
Report artifacts may contain more detail, but schema-governed decision outputs must stay in this normalized shape.

## Locked logic reflected in the schema

### `deliver`

- must include `EPI-SUFFICIENT`
- must not include limitation or safety basis codes
- may be the only decision that permits execution `"allow"`

### `qualify`

- must include `EPI-UNCERTAIN`
- must include `qualification_type`
- display must be `allow_with_qualification`

### `refuse_assert`

- must include `EPI-INSUFFICIENT`
- display must be `block_original`

### `refuse_help`

- must include either `SAFE-DISALLOWED-HELP` or `WF-WEAPONIZED-FORM`
- display must be `block_original`

## Important notes

- This schema validates structure and some decision invariants.
- It does not evaluate truthfulness, safety, or epistemic sufficiency by itself.
- It does not replace trace validation.
- It does not encode execution relevance directly; that belongs in the trace and evaluation context.
- A valid decision result must still be paired with trace-before-execution behavior in the runtime system.

## Relationship to neighboring artifacts

This schema should be used together with:

- `schemas/evaluation-payload.schema.json`
- `docs/trace-schema.md`
- `docs/reference-middleware-spec.md`
- `docs/reference-middleware-pseudocode.md`

## Recommended repository path

```text
docs/decision-result-schema.md
```
