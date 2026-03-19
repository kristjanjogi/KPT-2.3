# KPT 2.3 Trace Event Family Model
## Draft v0.1

Author: Kristjan Jõgi  
Status: Draft  
Applies to: KPT 2.3

---

## 1. Purpose

This document defines a trace event family model for KPT 2.3.

Its purpose is to clarify that KPT trace is not only a single JSON object format, but a governed family of related runtime events that together support:

- auditability;
- decision reconstruction;
- temporal conformance;
- execution accountability;
- replacement-output lineage;
- human review and override traceability.

This model extends the KPT trace discussion beyond a standalone decision trace without weakening the core rule:

**one evaluated candidate output -> one trace object**

---

## 2. Why an Event Family Model Is Needed

A stable trace schema alone is necessary but not sufficient for a mature runtime governance standard.

A decision trace records one evaluated candidate output. But real systems may also involve:

- safe replacement generation;
- human review;
- reviewer override;
- attempted execution;
- committed execution;
- blocked execution;
- later verification or chain checking.

If these events are not modeled clearly, systems tend to collapse distinct actions into a single log row or lose important ordering information.

KPT should avoid that failure mode.

---

## 3. Relationship to the Core Trace Object

The KPT trace object remains the primary audit object for one evaluated candidate output.

Reference artifact:
- `schemas/trace.schema.json`

The event family model does not replace that trace object.
It adds a runtime model around it.

### Locked rule

- Every evaluated candidate output must produce its own trace.
- Non-evaluation events must not be used as substitutes for candidate evaluation traces.

This means:

- a human review record is not a replacement for an evaluation trace;
- an execution commit record is not a replacement for an evaluation trace;
- an override record is not a replacement for an evaluation trace.

---

## 4. Core Design Principles

### 4.1 Evaluation trace remains primary

The candidate-evaluation trace is the anchor event.
Other events attach to it but do not replace it.

### 4.2 Temporal order matters

The family model must preserve runtime order, especially for execution-relevant systems.

### 4.3 Decision state is not enforcement action

The event family model must not collapse:

- what the output was; and
- what the system later did.

### 4.4 Replacement is lineage, not mutation

A safe replacement is a new candidate output, not a rewrite of the blocked original.

### 4.5 Override is additive, not destructive

A reviewer or downstream system may create a later event, but must not erase or silently rewrite the original KPT decision trace.

### 4.6 Execution must be observable

If the system is execution-relevant, attempted and committed execution should be represented explicitly rather than inferred.

---

## 5. Event Family Overview

The recommended KPT trace event family consists of the following event types.

### Required or core-conditional families

1. Candidate Evaluation Event
2. Safe Replacement Evaluation Event

### Recommended operational families

3. Human Review Event
4. Override Action Event
5. Execution Attempt Event
6. Execution Commit Event
7. Execution Block Event
8. Trace Verification Event

Not every implementation needs every operational event family at first.
But the model should reserve room for them.

---

## 6. Candidate Evaluation Event

### Status
Core and required.

### Meaning
Represents one KPT evaluation of one candidate output.

### Function
This is the normative event produced when the middleware assigns:

- `decision_state`
- `basis_codes`
- `qualification_type`
- `enforcement_action`
- `trace_id`

### Required rule

Every evaluated candidate output must produce exactly one candidate evaluation trace object.

### Reference semantics

This event is the runtime realization of:

- `schemas/decision-result.schema.json`
- `schemas/trace.schema.json`

### Typical trigger

- model produces a candidate answer;
- agent proposes a tool call;
- system generates a structured candidate object.

---

## 7. Safe Replacement Evaluation Event

### Status
Core conditional.
Required when a blocked candidate is replaced with a separately evaluated safe alternative.

### Meaning
Represents KPT evaluation of the replacement candidate.

### Critical rule

Blocked candidate + replacement candidate = two evaluation traces.

### Why this matters

Without a separate replacement evaluation event, the system would lose:

- what was originally blocked;
- what was later allowed or qualified;
- whether the replacement itself met KPT requirements.

### Recommended linkage

A replacement event should be linked to the blocked original through explicit lineage fields in implementation or surrounding metadata.

Minimum practical linkage idea:

- original `trace_id`
- replacement `trace_id`
- shared lineage group or relation metadata

---

## 8. Human Review Event

### Status
Recommended when human review is used.

### Meaning
Represents the fact that a human reviewer inspected a governed case.

### It should record

- that review occurred;
- who or what role reviewed it;
- what object was reviewed;
- what the review outcome was.

### It must not do

It must not overwrite or replace the original KPT evaluation trace.

### Purpose

This event preserves accountability for human-in-the-loop systems without collapsing reviewer activity into model decisioning.

---

## 9. Override Action Event

### Status
Recommended when human or system override exists.

### Meaning
Represents a later action that changes downstream treatment relative to the original decision result.

Examples:

- a reviewer permits display after earlier block;
- a reviewer prevents execution that would otherwise have been allowed;
- a downstream control layer blocks action after a prior `deliver`.

### Locked rule

Override is a later governance/runtime action.
It is not a retroactive change to the original decision state.

### Therefore

The original decision trace remains intact.
The override action must be recorded as a separate event.

---

## 10. Execution Attempt Event

### Status
Recommended for execution-relevant implementations.

### Meaning
Represents an attempted downstream action after decisioning and enforcement routing.

Examples:

- tool invocation attempt;
- API call attempt;
- file write attempt;
- workflow transition attempt.

### Why it matters

Execution attempt is not the same as execution success.

If KPT wants strong audit reconstruction, it is useful to know:

- that execution was attempted;
- what trace it depended on;
- whether the attempt was permitted or blocked.

### Relationship to trace-before-execution

Where execution is allowed, the originating candidate evaluation trace must already exist before this event occurs.

---

## 11. Execution Commit Event

### Status
Recommended for execution-relevant implementations.

### Meaning
Represents successful downstream commitment of an external action.

Examples:

- tool call completed;
- API request accepted;
- database state changed;
- message actually sent;
- workflow stage committed.

### Why it matters

A system may attempt execution but fail before commit.
A mature audit model should preserve this distinction.

### Locked rule

Execution commit is not inferred from `decision_state`.
It must be represented explicitly if execution actually occurred.

---

## 12. Execution Block Event

### Status
Recommended for execution-relevant implementations.

### Meaning
Represents a blocked downstream execution path.

Examples:

- `qualify` result blocks tool execution;
- `refuse_assert` blocks action;
- `refuse_help` blocks action;
- downstream gate blocks execution despite earlier candidate generation.

### Why it matters

This event can make operational audit clearer by showing that:

- the system did not merely fail to act;
- it actively blocked execution because governance required it.

---

## 13. Trace Verification Event

### Status
Optional but recommended for stronger assurance environments.

### Meaning
Represents later verification of trace chain integrity or audit record consistency.

Examples:

- integrity hash verification;
- append-only chain validation;
- export/package verification.

### Why it matters

This event helps separate:

- runtime decisioning; from
- later audit verification activity.

---

## 14. Minimum Stable Family for Near-Term Standardization

For near-term KPT trace stabilization, the minimum family that should be conceptually locked is:

1. Candidate Evaluation Event
2. Safe Replacement Evaluation Event
3. Execution Attempt Event
4. Execution Commit Event
5. Override Action Event

Reason:

- candidate evaluation anchors the standard;
- safe replacement preserves lineage;
- execution attempt and commit preserve runtime consequence;
- override preserves human/system intervention traceability.

Other families may be recommended without being mandatory in early versions.

---

## 15. Recommended Event Ordering Rules

The following ordering rules should hold.

### 15.1 Evaluation before display or execution treatment

Candidate evaluation must happen before governed display or execution routing.

### 15.2 Trace before execution attempt

For execution-relevant outputs, the evaluation trace must be written before execution attempt.

### 15.3 Attempt before commit

Execution commit must not appear unless an attempt path exists, even if the attempt event is implicit in a simpler implementation.

### 15.4 Blocked original before replacement evaluation

If a candidate is blocked and replaced, the blocked candidate trace must exist before the replacement is evaluated.

### 15.5 Original decision before override

An override event cannot logically precede the original decision trace it modifies in downstream effect.

---

## 16. Replay and Reconstruction by Event Family

Different event families support different replay goals.

### 16.1 Candidate Evaluation Event
Supports:

- decision replay;
- audit reconstruction.

### 16.2 Safe Replacement Evaluation Event
Supports:

- lineage reconstruction;
- replacement audit.

### 16.3 Human Review and Override Events
Supports:

- reviewer accountability;
- later governance reconstruction.

### 16.4 Execution Attempt and Commit Events
Supports:

- operational reconstruction;
- action-path verification;
- commit confirmation.

### Important clarification

KPT should distinguish:

- decision replay;
- audit reconstruction;
- execution replay.

These are related but not identical goals.

---

## 17. Recommended Common Metadata Across Event Families

The exact schema for every operational event family is not yet locked.
However, implementations should strongly consider a common event envelope.

Recommended common fields:

- `event_id`
- `event_type`
- `timestamp`
- `actor_type`
- `actor_ref`
- `origin_trace_id`
- `related_trace_id`
- `lineage_group_id`
- `policy_version`
- `engine_version`

### Notes

- `origin_trace_id` links the event back to the relevant candidate evaluation trace.
- `related_trace_id` is especially useful for replacement or override relationships.
- `lineage_group_id` can group all events related to one governed case.

This is guidance, not yet a normative schema requirement.

---

## 18. What Must Not Be Collapsed

The event family model should explicitly prevent these collapses.

### 18.1 Evaluation and execution

Do not treat execution as if it were part of the evaluation trace itself.

### 18.2 Original and replacement

Do not treat a safe replacement as an in-place edit to the blocked candidate.

### 18.3 Decision and override

Do not treat override as if it changed history.

### 18.4 Attempt and commit

Do not assume that attempted execution means successful commit.

### 18.5 Review and approval

Do not treat review presence alone as approval or execution authorization.

---

## 19. Example Event Sequences

### 19.1 Ordinary non-execution analytical answer

1. candidate evaluation event
2. display outcome

### 19.2 Execution-relevant deliver flow

1. candidate evaluation event (`deliver`)
2. trace write
3. execution attempt event
4. execution commit event

### 19.3 Execution-relevant qualify flow

1. candidate evaluation event (`qualify`)
2. trace write
3. execution block event
4. optional qualified display

### 19.4 Blocked candidate with safe replacement

1. candidate evaluation event (`refuse_assert` or `refuse_help`)
2. blocked original outcome
3. replacement candidate created
4. replacement evaluation event
5. second trace written
6. replacement displayed if admissible

### 19.5 Human override flow

1. original candidate evaluation event
2. human review event
3. override action event
4. downstream display or execution treatment per override policy

---

## 20. Conformance Relevance

The event family model should influence future conformance expectations.

At minimum, a stronger trace conformance profile should test whether:

- every candidate evaluation generated a trace;
- blocked candidate plus replacement produced two traces;
- execution-relevant actions were preceded by trace write;
- override did not erase original decision trace;
- execution commit was not fabricated from decision state alone.

---

## 21. What Is Already Strong vs What Is Still Open

### Already strong in current KPT work

- one trace per evaluated candidate output;
- blocked candidate plus replacement equals two traces;
- decision state separated from enforcement action;
- execution relevance is explicit;
- trace before execution is a core rule;
- append-only or tamper-evident trace chain direction exists.

### Still open for future standardization

- canonical event-type naming;
- common event envelope schema;
- lineage identifier rules;
- export/import representation;
- retention and redaction rules;
- verification event schema;
- conformance tiers for operational event families.

---

## 22. Recommended Standardization Path

A practical path forward is:

### Phase 1
Lock the event family model conceptually.

### Phase 2
Define a common event envelope for non-evaluation operational events.

### Phase 3
Define trace verification and export guidance.

### Phase 4
Add event-family-specific conformance tests.

This allows KPT trace to mature without destabilizing the already strong evaluation trace core.

---

## 23. Recommended Repository Path

```text
docs/trace-event-family-model.md
```

---

## 24. One-Line Summary

KPT trace is not only a schema for one decision record; it is a family model for evaluation, replacement, override, and execution-related events that together preserve governance, timing, and audit lineage.
