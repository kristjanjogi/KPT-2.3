# Trace Schema

File: `schemas/trace.schema.json`

This schema defines the auditable trace object for one evaluated candidate output in KPT 2.3.

It exists to ensure that every governed candidate output can be recorded in a normalized, reviewable, and tamper-evident structure.

## Required top-level fields

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

## Recommended extension fields

The current schema also supports:

- `profile`
- `deployment_mode`

These reflect already accepted KPT 2.3 extensions and may become stronger requirements in stricter assurance tiers.

## Design intent

The trace object is not only a log record.

It is the audit object that captures:

- what was evaluated;
- under what governed context;
- what decision was assigned;
- what basis codes supported that decision;
- what runtime treatment followed;
- what policy and engine version produced the result;
- how the trace links into a tamper-evident chain.

## Locked distinctions preserved by the schema

- `decision_state` = what the output is
- `enforcement_action` = what the system does because of that status
- `execution_relevance` = whether the candidate output mattered for possible downstream execution
- `trace_id` = identifier of the evaluation record, not a policy result by itself

## Locked logic reflected in the schema

### `qualify`

- must include `EPI-UNCERTAIN`
- must include a non-null `qualification_type`
- display must be `allow_with_qualification`
- execution may not be `allow`

### `deliver`

- must include `EPI-SUFFICIENT`
- must not include limitation or safety basis codes
- may be the only decision state compatible with execution `"allow"`

### `refuse_assert`

- must include `EPI-INSUFFICIENT`
- `qualification_type` must be null
- display must be `block_original`

### `refuse_help`

- must include either `SAFE-DISALLOWED-HELP` or `WF-WEAPONIZED-FORM`
- `qualification_type` must be null
- display must be `block_original`

## Important notes

- This schema validates structure and selected decision invariants.
- It does not itself prove that trace-before-execution happened.
- It does not validate append-only storage implementation by itself.
- It does not replace conformance testing.
- It does not validate the truthfulness of the candidate output.

## Operational rule outside schema scope

A valid trace object is still not enough on its own.

For execution-relevant outputs, the runtime system must ensure that the trace is written before any downstream execution begins.

That temporal rule belongs to conformance and runtime behavior, not merely to JSON shape validation.

## Relationship to neighboring artifacts

This schema should be used together with:

- `schemas/evaluation-payload.schema.json`
- `schemas/decision-result.schema.json`
- trace schema documentation
- reference middleware specification
- reference middleware pseudocode
- conformance methodology

## Recommended repository path

```text
docs/trace-schema-schema.md
```
