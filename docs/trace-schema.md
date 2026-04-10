# KPT 2.3 Trace Schema

**Author:** Kristjan Jõgi  
**Document date:** 2026-03-11  
**Version:** Public trace schema note v6  
**Status:** Normative explanatory document  
**Authority class:** Normative when read together with `schemas/trace.schema.json`

## 1. Canonical truth

For trace structure, the canonical source of truth is:

1. `schemas/trace.schema.json`
2. the minimum-contract language in `docs/quickstart.md`

If this prose conflicts with the runtime demo layer, the schema wins.

The only deliberate schema-side exception in the public schema surface is:

- `previous_trace_hash` MAY be `null` for a genesis trace record

## 2. Scope

A trace records one evaluated candidate output.

If an original candidate output is blocked and a safe replacement is evaluated, the replacement is a new candidate output and MUST receive:

- a new decision
- a new trace
- its own integrity hash

## 3. Required fields

The required trace fields are:

- `trace_id`
- `timestamp`
- `input_ref`
- `output_ref`
- `zone`
- `decision_state`
- `basis_codes`
- `rationale`
- `qualification_type`
- `execution_relevance`
- `enforcement_action`
- `policy_version`
- `engine_version`
- `previous_trace_hash`
- `integrity_hash`

Optional but recommended fields:

- `profile`
- `deployment_mode`

## 4. Canonical enums and field shapes

### 4.1 `decision_state`

- `deliver`
- `qualify`
- `refuse_assert`
- `refuse_help`

### 4.2 `qualification_type`

- `uncertainty`
- `time_sensitive`
- `source_limited`
- `scope_limited`
- `verification_required`
- `mixed`
- `null` when no qualification applies

### 4.3 `execution_relevance`

`execution_relevance` is a **boolean**:

- `true` = execution-relevant
- `false` = not execution-relevant

### 4.4 `enforcement_action`

`enforcement_action` is a two-field object:

```json
{
  "display": "allow | allow_with_qualification | block_original",
  "execution": "allow | block | not_applicable"
}
```

This trace contract is intentionally narrower than the richer demo/report enforcement layer.

## 5. Core invariants

### 5.1 Deliver

For `decision_state = deliver`:

- `basis_codes` MUST include `EPI-SUFFICIENT`
- `qualification_type` MUST be `null`
- `enforcement_action.display` MUST be `allow`
- `enforcement_action.execution` MAY be `allow` or `not_applicable`
- limitation and refusal-supporting codes MUST NOT appear

### 5.2 Qualify

For `decision_state = qualify`:

- `basis_codes` MUST include `EPI-UNCERTAIN`
- `qualification_type` MUST be one of the allowed non-null qualification enums
- `enforcement_action.display` MUST be `allow_with_qualification`
- `enforcement_action.execution` MUST be `block` or `not_applicable`

### 5.3 Refuse assert

For `decision_state = refuse_assert`:

- `basis_codes` MUST include `EPI-INSUFFICIENT`
- `qualification_type` MUST be `null`
- `enforcement_action.display` MUST be `block_original`
- `enforcement_action.execution` MUST be `block` or `not_applicable`

### 5.4 Refuse help

For `decision_state = refuse_help`:

- `basis_codes` MUST include `SAFE-DISALLOWED-HELP` or `WF-WEAPONIZED-FORM`
- `qualification_type` MUST be `null`
- `enforcement_action.display` MUST be `block_original`
- `enforcement_action.execution` MUST be `block` or `not_applicable`

## 6. Hashing and chaining

- `integrity_hash` is the SHA-256 hash of the full trace object excluding `integrity_hash`
- hash encoding is lowercase hexadecimal
- `previous_trace_hash` MUST equal the prior committed trace’s `integrity_hash`
- `previous_trace_hash = null` is allowed only for a genesis trace record

## 7. Core output vs richer report layer

The canonical trace contract is deliberately narrow.

Not part of the canonical trace object:

- demo-only extension blocks
- fixture-driving lineage metadata
- richer enforcement detail such as `display_mode`, `execution_mode`, or `replacement_required`

Those belong in comparison/report artifacts or internal runtime state, not in the schema-governed trace itself.

## 8. Conformance note

A schema-valid trace is necessary but not sufficient for full conformance.

Full conformance also depends on:

- decision correctness
- enforcement correctness
- trace-before-execution ordering
- basis-code and qualification consistency
- replacement-path handling where applicable
