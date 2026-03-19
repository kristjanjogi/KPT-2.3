# Trace Stability and Replay Guidance
## KPT 2.3 Guidance Draft v0.1

Author: Kristjan Jõgi  
Status: Draft  
Applies to: KPT 2.3

---

## 1. Purpose

This document defines how KPT 2.3 should treat trace stability, replay, and audit reconstruction.

Its purpose is to prevent the trace layer from being reduced to a generic log store.

In KPT, trace is part of runtime governance. It is not merely historical telemetry.

This guidance exists to stabilize:

- trace object meaning;
- trace serialization assumptions;
- replay expectations;
- integrity-chain behavior;
- audit reconstruction requirements;
- conformance expectations for trace behavior.

---

## 2. Core Position

KPT trace is not only an audit log.

KPT trace is an auditable governance record for one evaluated candidate output.

That record must preserve enough structure to support:

- review of what was evaluated;
- review of what decision was assigned;
- review of why that decision was assigned;
- review of what enforcement treatment followed;
- review of whether execution was allowed or blocked;
- review of policy and engine versions used at the time of evaluation;
- review of ordering relative to execution.

---

## 3. Stability Goal

For KPT 2.3, trace stability should mean the following.

### 3.1 Structural stability

The trace object has a stable required field set and stable field meanings.

### 3.2 Semantic stability

The trace continues to represent one evaluated candidate output, not an arbitrary bundle of events.

### 3.3 Temporal stability

The trace remains tied to decision-before-execution ordering.

### 3.4 Integrity stability

The trace remains linkable into an append-only or tamper-evident chain.

### 3.5 Replay stability

The trace preserves enough information for audit reconstruction and defined forms of replay.

---

## 4. Trace Layers

A stable trace standard should be understood as multiple layers, not one feature.

### 4.1 Trace object schema layer

This defines the normalized structure of one trace object.

Reference artifact:
- `schemas/trace.schema.json`

### 4.2 Trace semantics layer

This defines what one trace means.

Locked meaning:
- one trace = one evaluated candidate output.

### 4.3 Temporal rule layer

This defines when trace must exist relative to downstream effect.

Locked rule:
- execution-relevant outputs must be traced before execution begins.

### 4.4 Integrity layer

This defines how traces are linked and protected against silent modification.

### 4.5 Replay and reconstruction layer

This defines what later review can reconstruct or reproduce from trace plus referenced artifacts.

### 4.6 Conformance layer

This defines how trace behavior is tested and verified.

---

## 5. Stable Meaning of a Trace

A KPT trace must represent exactly one evaluated candidate output.

That means a trace records:

- the candidate output reference;
- the governed context of evaluation;
- the assigned decision state;
- the supporting basis codes;
- the qualification type if applicable;
- the execution relevance of that candidate output;
- the mapped enforcement action;
- the policy and engine version;
- the concise rationale;
- integrity linkage information.

A trace must not collapse multiple independently evaluated candidates into one record.

---

## 6. Locked Trace Identity Rules

### 6.1 One trace per evaluated candidate output

Every evaluated candidate output must generate its own trace.

### 6.2 Blocked candidate plus replacement equals two traces

If an original candidate is blocked and a safe replacement is later shown, the original and replacement are separate candidates and must receive separate traces.

### 6.3 Decision state is not enforcement action

Both may appear in the trace, but they must remain distinct fields with distinct meanings.

### 6.4 Execution relevance is traceable

Whether the candidate was execution-relevant must be preserved in the trace.

---

## 7. Minimum Stable Trace Content

At minimum, a stable KPT trace should preserve:

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

Recommended extension fields already aligned with KPT 2.3:

- `profile`
- `deployment_mode`

These fields should be treated as stable KPT 2.3-compatible extensions, even where stricter requirement levels may be defined later.

---

## 8. Replay: Required Distinctions

The word replay should not be used loosely.

KPT should distinguish at least three different replay concepts.

### 8.1 Decision replay

Question:
Can the same evaluation input, under the same policy and engine conditions, be re-evaluated to test whether the decision result is reproduced?

This is the most relevant replay form for KPT runtime governance.

### 8.2 Audit reconstruction

Question:
Can a reviewer later reconstruct what was evaluated, which decision was assigned, which basis codes applied, and what enforcement followed?

This is mandatory for KPT trace usefulness.

### 8.3 Execution replay

Question:
Can the exact downstream action be replayed?

This is not a default KPT requirement.

KPT is primarily about decision governance, not mandatory reproduction of external side effects.

---

## 9. Required Replay Position for KPT 2.3

For KPT 2.3, the realistic required replay position should be:

### Required

- audit reconstruction;
- decision replay where sufficient referenced inputs are retained.

### Not required by default

- exact reproduction of external execution side effects;
- full environmental replay of downstream business systems.

This distinction is important so that trace requirements remain strong without becoming unrealistically broad.

---

## 10. Conditions for Meaningful Decision Replay

Decision replay is only meaningful when the relevant evaluation conditions are sufficiently pinned.

A strong decision replay posture should retain or reference:

- original evaluation payload or stable reference to it;
- original candidate output or stable reference to it;
- policy version;
- engine version;
- relevant provenance state;
- governing context including zone, profile, and deployment mode.

If these are not retained or stably referenceable, replay may degrade into partial reconstruction rather than true decision replay.

---

## 11. Audit Reconstruction Requirement

A stable KPT trace system must support audit reconstruction.

At minimum, a later reviewer should be able to answer:

- what input triggered evaluation;
- what candidate output was evaluated;
- what governed context applied;
- what decision was assigned;
- what basis codes supported that decision;
- whether the candidate was execution-relevant;
- what enforcement treatment followed;
- which policy and engine version were active;
- where the trace sat in the trace chain.

If these questions cannot be answered, the trace layer is incomplete.

---

## 12. Temporal Stability Rule

This is one of the most important trace rules.

For execution-relevant outputs:

- trace must be written before execution begins;
- post-hoc logging is non-conformant;
- execution-before-trace is a hard failure against KPT temporal logic.

This rule is not optional.

It is what makes trace part of governance rather than an after-the-fact note.

---

## 13. Integrity Chain Guidance

KPT trace should support append-only or tamper-evident storage.

### 13.1 Required minimum integrity posture

A trace should include:

- an identifier for the current trace;
- a reference or hash link to the previous trace;
- an integrity hash for the current trace.

### 13.2 Why integrity matters

Without integrity linkage, a trace store may still function as a log, but it provides weaker trust for governance and later review.

### 13.3 Scope of current guidance

KPT 2.3 currently stabilizes the need for integrity linkage, but does not yet fully lock the exact canonical hashing method.

That remains a further hardening target.

---

## 14. Canonical Serialization Gap

One important stability gap still exists.

KPT should later define a canonical serialization rule for trace hashing and integrity verification.

That rule should specify:

- which fields are included in the hashed form;
- field ordering;
- string normalization expectations;
- null-handling expectations;
- whether derived fields are included or excluded;
- how extensions are treated.

Until such a rule is locked, integrity fields are meaningful but not yet fully standardized across independent implementations.

---

## 15. Event Family Guidance

KPT should distinguish between trace object types or event families over time.

At present, the core trace model is centered on:

- candidate output evaluation.

Future strong implementations may also separately trace:

- safe replacement generation;
- human override events;
- execution attempt;
- execution commit;
- trace verification events.

For KPT 2.3, the minimum required family is still the candidate evaluation trace.

That should remain the normative center.

---

## 16. Audit Log vs KPT Trace

A generic audit log is not automatically a KPT trace system.

A generic audit log may record:

- timestamps;
- user actions;
- tool calls;
- system events.

A KPT trace system must additionally preserve:

- one-trace-per-candidate meaning;
- decision state;
- basis codes;
- qualification type;
- execution relevance;
- enforcement mapping;
- policy pinning;
- integrity linkage;
- temporal relation to execution.

So the correct framing is:

**KPT trace may use an audit log substrate, but KPT trace is semantically stronger than ordinary audit logging.**

---

## 17. Operational Requirements for Stable Trace Systems

A more mature KPT trace implementation should support operational capabilities such as:

- append-only write discipline or equivalent tamper-evident control;
- export of trace records for review;
- filtering by trace_id, decision_state, zone, policy_version, and time range;
- chain verification;
- archive and retention behavior;
- recovery of referenced evaluation objects where policy allows.

Not all of these must be fully standardized in KPT 2.3, but they describe the operational direction for stable trace deployments.

---

## 18. Privacy and Redaction Guidance

Trace stability must not be confused with unlimited raw-data retention.

A stable trace system may still need controlled handling of:

- personal data;
- regulated data;
- confidential business data;
- secrets contained in candidate outputs or referenced inputs.

The trace model should therefore prefer stable references where full raw payload storage is inappropriate.

Important:
Redaction or reference-based storage must not destroy the ability to preserve conformance-relevant meaning.

---

## 19. Conformance-Relevant Trace Assertions

A trace system claiming KPT-aligned behavior should satisfy at minimum:

- one trace per evaluated candidate output;
- blocked candidate plus replacement yields two traces;
- decision state recorded independently from enforcement action;
- execution relevance recorded;
- execution-relevant traces written before execution begins;
- policy and engine version recorded;
- integrity linkage present;
- rationale present as concise audit justification.

---

## 20. Known Stability Gaps Still Open

The following areas remain legitimate hardening targets.

### 20.1 Canonical hash specification

Exact hashing and serialization rules are not yet fully locked.

### 20.2 Replay protocol definition

A fuller statement is still needed for how independent implementations should perform replay tests.

### 20.3 Event family expansion

It is still open whether override, execution attempt, and execution commit should be standardized as related trace families in a stronger version.

### 20.4 Trace operational profile

Retention, export, verification, and archive rules may need a more explicit operational profile document.

### 20.5 Dedicated trace conformance pack

A stronger future release should likely include trace-specific conformance tests.

---

## 21. Recommended KPT Positioning Language

When describing KPT externally, a stronger and more accurate statement is:

**KPT trace is not just an audit log. It is a decision-trace governance record that preserves evaluation meaning, temporal ordering, enforcement linkage, and integrity context for each candidate output.**

A shorter acceptable form is:

**KPT provides decision-trace governance, not just logging.**

---

## 22. Practical Standardization Goal for the Next Phase

The next phase of trace stabilization should aim to lock:

1. canonical serialization and integrity hashing rules;
2. replay terminology and minimum replay expectations;
3. a trace operational profile;
4. dedicated trace conformance tests;
5. optional future trace event-family expansion.

---

## 23. Relationship to Neighboring Artifacts

This document should stay aligned with:

- `docs/trace-schema.md`
- `docs/conformance-methodology.md`
- `docs/reference-middleware-spec.md`
- `docs/reference-middleware-pseudocode.md`
- `schemas/evaluation-payload.schema.json`
- `schemas/decision-result.schema.json`
- `schemas/trace.schema.json`

---

## 24. Recommended Repository Path

```text
docs/trace-stability-and-replay-guidance.md
```
