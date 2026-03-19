# KPT Reference Middleware Specification
## Working Draft v0.1

Author: Kristjan Jõgi  
Status: Draft  
Applies to: KPT 2.3

---

## 1. Purpose

KPT Reference Middleware is a control-layer pattern for AI systems whose outputs may influence decisions or trigger external actions.

Its purpose is to ensure that:

- every governed candidate output is evaluated before influence or execution;
- every evaluation produces a decision state;
- execution-relevant outputs cannot bypass decisioning;
- trace emission happens before execution;
- enforcement action is downstream of decision state, not a substitute for it.

This middleware is not the model.  
This middleware is not the business workflow.  
This middleware is the governance boundary between candidate output and real-world effect.

---

## 2. Position in System Architecture

The reference middleware sits between:

- an upstream generation component; and
- a downstream display, tool, workflow, or action layer.

### High-Level Placement

```text
User/Input
  -> Application Context Builder
  -> Model/Agent
  -> Candidate Output
  -> KPT Middleware
  -> Enforcement Layer
  -> Display and/or Execution
```

KPT middleware receives a candidate output and decides whether that output may:

- be displayed as-is;
- be displayed with qualification;
- be blocked from assertion;
- be blocked from harmful assistance;
- be blocked from execution;
- be replaced by a separately evaluated safe alternative.

---

## 3. Core Architectural Principle

### Output Is Not Action

A model or agent may produce text, structured data, or a proposed tool invocation.

That proposal has no execution authority until KPT evaluation completes.

Therefore:

- generated content is only a candidate output;
- the candidate output must be evaluated;
- a decision state is assigned first;
- a trace is written;
- only then may downstream enforcement permit display or execution.

---

## 4. Scope of Governed Objects

The middleware should be able to evaluate at least the following object types.

### A. Natural-Language Response

Examples:

- answer to a user question;
- explanation;
- recommendation;
- instruction.

### B. Structured Response

Examples:

- JSON answer;
- classification result;
- extracted fields;
- risk summary.

### C. Execution-Relevant Proposal

Examples:

- tool call;
- API request;
- database write;
- email send proposal;
- workflow transition;
- file modification;
- transaction proposal.

### D. Safe Replacement Output

Examples:

- refusal;
- safer guidance;
- constrained reformulation after blocking an unsafe candidate.

**Important rule:** blocked candidate output and replacement output are separate evaluated objects and require separate traces.

---

## 5. Required Middleware Inputs

The reference middleware should receive a normalized evaluation payload.

### 5.1 Evaluation Payload

```yaml
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
```

---

## 6. Middleware Outputs

The middleware returns a decision object and triggers trace creation.

### 6.1 Decision Object

```yaml
decision_result:
  decision_state: "deliver | qualify | refuse_assert | refuse_help"
  basis_codes:
    - "EPI-UNCERTAIN"
    - "TMP-TIME-SENSITIVE"
  qualification_type: "time_sensitive"
  rationale: "Currentness is material and verification is insufficient for an unqualified answer."
  enforcement_action:
    display: "allow_with_qualification"
    execution: "block"
  trace_id: "generated-trace-id"
```

---

## 7. Decision Logic Responsibilities

The reference middleware must perform or orchestrate the following checks.

### A. Zone-Aware Evaluation

Determine required strictness based on governed context:

- critical;
- analytical;
- creative.

### B. Epistemic Sufficiency

Determine whether the candidate is:

- sufficiently supported;
- uncertain and therefore qualified;
- insufficient for assertion.

### C. Safety / Disallowed Help

Determine whether the candidate constitutes disallowed assistance.

### D. Weaponized Form Control

Detect formally compliant but functionally harmful outputs.

### E. Execution Relevance

Determine whether downstream action is possible or proposed.

### F. Qualification Derivation

If decision is `qualify`, derive `qualification_type` from basis-code families.

### G. Enforcement Mapping

Convert `decision_state` plus `execution_relevance` into downstream allow/block behavior.

### H. Trace Emission

Write trace before any execution-relevant commitment occurs.

---

## 8. Minimal Decision Algorithm

### 8.1 Ordered Logic

The evaluation order should be:

1. normalize candidate output;
2. determine governed context;
3. determine execution relevance;
4. run safety and weaponized-form checks;
5. run epistemic sufficiency checks;
6. assign decision state;
7. derive qualification type if needed;
8. map enforcement action;
9. emit trace;
10. permit display and/or execution according to enforcement rules.

### 8.2 Precedence Rules

#### Safety Precedence

If `SAFE-DISALLOWED-HELP` or `WF-WEAPONIZED-FORM` applies:

- decision must be `refuse_help`;
- execution must be blocked;
- candidate output must not be displayed as requested.

#### Epistemic Refusal

If epistemic basis is insufficient for assertion:

- decision must be `refuse_assert`.

#### Qualification Rule

If output is admissible only with limits or uncertainty:

- decision must be `qualify`;
- `EPI-UNCERTAIN` must be present.

#### Clean Delivery

If output is sufficiently supported and no limiting or safety codes apply:

- decision may be `deliver`.

---

## 9. Enforcement Boundary

This is the critical runtime rule.

### 9.1 What KPT Decides

KPT decides:

- status of candidate output;
- admissibility of output form;
- whether qualification is required;
- whether execution may proceed.

### 9.2 What Enforcement Does

Enforcement does:

- display;
- hide;
- decorate with qualification;
- block tool call;
- block API submission;
- allow downstream commit;
- substitute safe alternative.

KPT and enforcement are distinct.

### Locked Distinction

- `decision_state` = what the output is;
- `enforcement_action` = what the system does because of that status.

---

## 10. Required Enforcement Mappings

### 10.1 Deliver

Typical outcome:

- display allowed;
- execution may be allowed if execution-relevant and policy permits.

```yaml
decision_state: "deliver"
enforcement_action:
  display: "allow"
  execution: "allow"
```

### 10.2 Qualify

#### Non-Execution-Relevant

- display allowed with qualification;
- no action execution.

#### Execution-Relevant

- display may be allowed with qualification;
- execution must be blocked.

```yaml
decision_state: "qualify"
enforcement_action:
  display: "allow_with_qualification"
  execution: "block"
```

### 10.3 Refuse Assert

- original candidate display blocked;
- execution blocked;
- optional safe alternative may be generated and separately evaluated.

### 10.4 Refuse Help

- original candidate display blocked;
- execution blocked;
- optional safe alternative may be generated and separately evaluated.

---

## 11. Trace Requirements at Middleware Level

Every evaluated candidate output must create a trace.

### 11.1 Minimum Required Trace Fields

```yaml
trace:
  trace_id: "uuid"
  timestamp: "ISO8601"
  input_ref: "input pointer"
  output_ref: "candidate pointer"
  zone: "critical"
  profile: "KPT-H"
  deployment_mode: "High-Assurance"
  decision_state: "qualify"
  basis_codes:
    - "EPI-UNCERTAIN"
    - "TMP-TIME-SENSITIVE"
  qualification_type: "time_sensitive"
  execution_relevance: true
  enforcement_action:
    display: "allow_with_qualification"
    execution: "block"
  rationale: "Currentness materially affects correctness and verification was insufficient."
  policy_version: "kpt-2.3-core-v0.2"
  engine_version: "kpt-mw-ref-v0.1"
  previous_trace_hash: "..."
  integrity_hash: "..."
```

### 11.2 Trace Timing Rule

For execution-relevant outputs:

- trace must exist before execution starts.

### 11.3 Dual-Trace Rule

If candidate output is blocked and a replacement is shown:

- candidate output gets one trace;
- replacement output gets a second trace.

---

## 12. Reference Runtime Flows

### 12.1 Normal Answer Flow

1. user asks a question;
2. application builds context;
3. model generates candidate answer;
4. KPT middleware evaluates;
5. decision = `deliver` / `qualify` / `refuse_assert` / `refuse_help`;
6. trace is emitted;
7. display layer follows enforcement rule.

### 12.2 Tool-Execution Flow

1. agent proposes tool call;
2. proposal enters KPT middleware as candidate output;
3. KPT evaluates content and execution relevance;
4. trace is emitted;
5. only an allowed decision/enforcement combination may pass to tool runner;
6. tool runner executes or blocks.

### 12.3 Safe Replacement Flow

1. harmful or insufficient candidate is blocked;
2. system generates safe alternative;
3. safe alternative is treated as a new candidate output;
4. second KPT evaluation occurs;
5. second trace is emitted;
6. safe alternative is displayed if admissible.

---

## 13. Integration Modes

The middleware should support at least three deployment patterns.

### 13.1 Inline Synchronous Middleware

Used when:

- live user interaction;
- immediate tool calls;
- strong execution control is needed.

Best suited for:

- assistants;
- agent runtimes;
- internal governance gateways.

### 13.2 Sidecar Service

Separate decision service called by application backend.

Best suited for:

- multi-model environments;
- multiple products sharing one governance service;
- centralized tracing.

### 13.3 Embedded Library

KPT logic packaged into application runtime.

Best suited for:

- simple pilots;
- demos;
- local testing.

---

## 14. Reference Interfaces

### 14.1 Evaluate Endpoint

```text
POST /kpt/evaluate
```

Input:

- normalized evaluation payload.

Output:

- decision result;
- trace metadata;
- enforcement instruction.

### 14.2 Trace Write Interface

```text
POST /kpt/trace
```

May be internal-only if evaluate writes trace automatically.

### 14.3 Policy Registry Interface

```text
GET /kpt/policy/current
GET /kpt/basis-codes/current
```

Used to pin evaluation behavior to explicit versions.

---

## 15. Minimal Internal Modules

A reference middleware implementation should include the following modules.

### 15.1 Normalizer

Converts raw output into governed candidate form.

### 15.2 Context Resolver

Resolves zone, profile, deployment mode, and execution relevance.

### 15.3 Safety Evaluator

Checks disallowed help and weaponized form.

### 15.4 Epistemic Evaluator

Checks sufficiency, uncertainty, and limitation basis.

### 15.5 Decision Resolver

Assigns `decision_state` and `qualification_type`.

### 15.6 Enforcement Mapper

Maps decision result to downstream actions.

### 15.7 Trace Emitter

Writes append-only or tamper-evident trace.

### 15.8 Policy Loader

Pins rules to declared policy versions.

---

## 16. Non-Goals

The reference middleware does not attempt to:

- guarantee model truthfulness;
- replace domain expertise;
- perform all retrieval itself;
- define business workflow semantics;
- replace authentication or authorization systems;
- replace application safety policies outside output governance.

It governs admissibility of outputs before influence or execution.

---

## 17. First Canonical Demo Scenario

The best first demo should be:

### Agent Proposes External Action Under Uncertainty

Scenario:

- user asks assistant to perform a financial or operational action;
- agent builds a plan;
- agent proposes a tool or API call;
- KPT evaluates the proposal;
- uncertainty or insufficient verification exists;
- execution is blocked;
- user receives a qualified or refusal-form response;
- trace is shown.

### Why This Is the Right First Demo

It demonstrates:

- output != action;
- decision before execution;
- `qualify` does not authorize execution;
- trace before commit;
- KPT’s distinction from surface-level moderation.

---

## 18. Conformance-Relevant Assertions

A middleware implementation claiming alignment with this specification should satisfy at minimum:

- one trace per evaluated candidate output;
- dual-trace behavior for blocked candidate plus safe replacement;
- trace-before-execution for execution-relevant outputs;
- safety precedence over epistemic sufficiency;
- `qualify` includes `EPI-UNCERTAIN`;
- execution-relevant `qualify` blocks execution;
- decision state is recorded independently from enforcement action.

---

## 19. File Placement Recommendation

Recommended repository path:

```text
docs/reference-middleware-spec.md
```

---

## 20. Next Artifact

The next recommended artifact is a pseudocode evaluator flow defining:

- request normalization;
- decision sequencing;
- precedence handling;
- trace creation;
- enforcement mapping;
- safe replacement loop.
