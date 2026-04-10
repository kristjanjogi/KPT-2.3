# KPT Reference Middleware Pattern

## Public Reference Pattern v0.2

**Author:** Kristjan Jõgi  
**Status:** Draft  
**Applies to:** KPT 2.3

---

## 1. Purpose

This document describes **one public reference realization pattern** for KPT.

It is not the definition of KPT itself.

Its purpose is to show how a governance boundary can sit between:
- an upstream generation component
- a downstream display, tool, workflow, or action layer

The pattern exists to ensure that:
- every governed candidate output is evaluated before influence or execution
- every evaluation produces a decision state
- execution-relevant outputs cannot bypass decisioning
- trace emission happens before execution
- enforcement action is downstream of decision state, not a substitute for it

---

## 2. Position in system architecture

The reference middleware sits between:
- an upstream generation component
- a downstream display, tool, workflow, or action layer

### High-level placement

~~~text
User/Input -> Application Context Builder -> Model/Agent -> Candidate Output -> KPT Middleware -> Enforcement Layer -> Display and/or Execution
~~~

KPT middleware receives a candidate output and determines its admissibility status before downstream effect.

---

## 3. Core architectural principle

### Output is not action

A model or agent may produce text, structured data, or a proposed tool invocation.

That proposal has no execution authority until KPT evaluation completes.

Therefore:
- generated content is only a candidate output
- the candidate output must be evaluated
- a decision state is assigned first
- a trace is written
- only then may downstream enforcement permit display or execution

---

## 4. Scope of governed objects

The middleware should be able to evaluate at least the following object types.

### A. Natural-language response
Examples:
- answer to a user question
- explanation
- recommendation
- instruction

### B. Structured response
Examples:
- JSON answer
- classification result
- extracted fields
- risk summary

### C. Execution-relevant proposal
Examples:
- tool call
- API request
- database write
- email send proposal
- workflow transition
- file modification
- transaction proposal

### D. Safe replacement output
Examples:
- refusal
- safer guidance
- constrained reformulation after blocking an unsafe candidate

**Important rule:** blocked candidate output and replacement output are separate evaluated objects and require separate traces.

---

## 5. Required middleware inputs

The reference middleware should receive a normalized evaluation payload.

### 5.1 Evaluation payload

~~~yaml
evaluation_payload:
  input_ref: "pointer to prompt/request/event"
  output_ref: "pointer to candidate output"
  candidate_output:
    content: "raw candidate content or structured object"
    content_type: "text | json | tool_call | mixed"
  context:
    zone: "critical | analytical | creative"
    profile: "KPT-H | KPT-A"
    deployment_mode: "General | High-Assurance"
    execution_relevant: true
    user_visible: true
    downstream_target: "display | tool | api | file | mixed"
  provenance:
    source_basis:
      - "user input"
      - "retrieved sources"
      - "model synthesis"
    verification_state: "verified | partially_verified | unverified | not_applicable"
    time_sensitivity: "low | medium | high"
  policy:
    policy_version: "kpt-2.3-core-v0.2"
    engine_version: "kpt-mw-ref-v0.1"
~~~

---

## 6. Middleware outputs

The middleware returns a decision object and triggers trace creation.

### 6.1 Decision object

~~~yaml
decision_result:
  decision_state: "deliver | qualify | refuse_assert | refuse_help"
  basis_codes:
    - "EPI-UNCERTAIN"
    - "VER-REQUIRED"
  qualification_type: "verification_required"
  rationale: "Execution-relevant recommendation requires stronger verification before action."
  enforcement_action:
    display: "allow_with_qualification"
    execution: "block"
  trace_id: "generated-trace-id"
~~~

---

## 7. Decision logic responsibilities

The reference middleware must perform or orchestrate the following checks:

### A. Zone-aware evaluation
Determine required strictness based on governed context:
- critical
- analytical
- creative

### B. Epistemic sufficiency
Determine whether the candidate is:
- sufficiently supported
- uncertain and therefore qualified
- insufficient for assertion

### C. Safety / disallowed help
Determine whether the candidate constitutes disallowed assistance.

### D. Weaponized form control
Detect formally compliant but functionally harmful outputs.

### E. Execution relevance
Determine whether downstream action is possible or proposed.

### F. Qualification derivation
If decision is `qualify`, derive `qualification_type` from basis-code families.

### G. Enforcement mapping
Convert `decision_state` plus `execution_relevance` into downstream allow/block behavior.

### H. Trace emission
Write trace before any execution-relevant commitment occurs.

---

## 8. Minimal decision algorithm

### 8.1 Ordered logic

The evaluation order should be:

1. normalize candidate output
2. determine governed context
3. determine execution relevance
4. run safety and weaponized-form checks
5. run epistemic sufficiency checks
6. assign decision state
7. derive qualification type if needed
8. map enforcement action
9. emit trace
10. permit display and/or execution according to enforcement rules

### 8.2 Precedence rules

#### Safety precedence
If `SAFE-DISALLOWED-HELP` or `WF-WEAPONIZED-FORM` applies:
- decision must be `refuse_help`
- execution must be blocked
- candidate output must not be displayed as requested

#### Epistemic refusal
If epistemic basis is insufficient for assertion:
- decision must be `refuse_assert`

#### Qualification rule
If output is admissible only with limits or uncertainty:
- decision must be `qualify`
- `EPI-UNCERTAIN` must be present

#### Clean delivery
If output is sufficiently supported and no limiting or safety codes apply:
- decision may be `deliver`

---

## 9. Enforcement boundary

This is the critical runtime rule.

### 9.1 What KPT decides

KPT determines:
- status of candidate output
- admissibility of output form
- whether qualification is required
- whether the candidate is execution-blocked or execution-eligible under the mapped enforcement contract

KPT does **not** collapse that decision into the downstream act of displaying, dispatching, or committing.

### 9.2 What enforcement does

The downstream enforcement layer does things such as:
- display
- hide
- decorate with qualification
- block tool call
- block API submission
- allow downstream commit
- substitute safe alternative

### 9.3 Locked distinction

- `decision_state` = what the output is
- `enforcement_action` = what the system does because of that status

---

## 10. Required enforcement mappings

### 10.1 Deliver

Typical outcome:
- display allowed
- execution may be allowed if execution-relevant and route policy permits

~~~yaml
decision_state: "deliver"
enforcement_action:
  display: "allow"
  execution: "allow"
~~~

### 10.2 Qualify

#### Non-execution-relevant
- display allowed with qualification
- no action execution

#### Execution-relevant
- display may be allowed with qualification
- execution must be blocked

~~~yaml
decision_state: "qualify"
enforcement_action:
  display: "allow_with_qualification"
  execution: "block"
~~~

### 10.3 Refuse assert
- original candidate display blocked
- execution blocked
- optional safe alternative may be generated and separately evaluated

### 10.4 Refuse help
- original candidate display blocked
- execution blocked
- optional safe alternative may be generated and separately evaluated

---

## 11. Trace requirements at middleware level

Every evaluated candidate output must create a trace.

For execution-relevant outputs:
- trace must be written before downstream execution begins

If a blocked candidate is replaced:
- the blocked candidate gets its own trace
- the replacement gets its own trace

Trace is part of the governance boundary, not a cosmetic report layer.

---

## 12. Boundary note

This pattern is public by design.

It shows the shape of a KPT realization pattern without claiming to expose every internal runtime component or every private implementation detail.
