# KPT 2.3 Core Standard

**Author:** Kristjan Jõgi  
**Document date:** 2026-03-08

**Version:** Public standard checkpoint  
**Status:** Public core standard  
**Positioning:** KPT is a standard for AI output decision governance.

## 0. Normative Language and Conformance

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as normative requirement terms.

A system is **KPT-conformant** only if observed behavior satisfies this standard at the level of:

- decision classification
- enforcement behavior
- trace generation
- temporal ordering

Documentation claims, post-hoc logging, or declared intent alone are insufficient to establish conformance.

Conformance is evaluated per governed candidate output unless a test case explicitly requires multi-trace behavior.

## 1. Preamble, Purpose, and Scope

KPT treats AI outputs as governed decision events rather than as automatically admissible responses or executable actions.

The purpose of KPT is to ensure that a candidate output is evaluated before it is allowed to:

- influence a human decision
- enter a downstream system
- become operational input
- participate in execution

KPT exists because many AI systems still treat model output as if it were merely text, even when that output can materially affect decisions, actions, or system behavior.

KPT governs the boundary between output generation and output admissibility.

KPT does not attempt to make models infallible. It assumes fallibility and introduces a runtime decision layer that classifies outputs before influence or execution.

### 1.1 Epistemic Humility Axiom

A KPT-governed system does not possess direct access to reality.
It operates only on representations: inputs, retrieved artifacts, stored context, and symbolic transformations.
Those representations MAY be incomplete, outdated, inconsistent, misleading, adversarial, or false, including when supplied by a human user.

A KPT-conformant implementation MUST NOT convert insufficiently grounded uncertainty into assertive output.
Where truth conditions are not sufficiently supported, the decision outcome MUST preserve that limitation.
Under this standard, the admissible outcomes for such cases are `qualify`, `refuse_assert`, or `refuse_help`, as appropriate to the governing basis.

This public standard focuses on the core decision-governance layer. It includes the minimum trace and conformance structures required to make the standard testable.

## 2. Terms and Definitions

### 2.1 Candidate Output
A candidate output is a generated output unit that is subject to KPT evaluation before display, reliance, or execution.

### 2.2 Governed Output
A governed output is a candidate output that falls within the decision scope of KPT.

### 2.3 Influence
Influence means any effect by which a candidate output may shape human judgment, downstream system state, or action selection.

### 2.4 Execution
Execution means any downstream use by which a candidate output becomes operational input, tool input, control input, or other action-bearing system input.

### 2.5 Decision State
Decision state is the normative classification assigned to a governed output under KPT.

### 2.6 Enforcement Action
Enforcement action is the system behavior applied because of the assigned decision state.

### 2.7 Zone
Zone is the runtime classification of the governed context under ZAT.

### 2.8 Profile
Profile classifies the output target context.

KPT 2.3 defines:
- `KPT-H` for human-facing outputs
- `KPT-A` for agent-facing outputs

### 2.9 Deployment Mode
Deployment mode classifies the assurance posture of the system.

KPT 2.3 defines:
- `General`
- `High-Assurance`

### 2.10 Qualification
Qualification is explicit boundedness, uncertainty marking, verification signaling, or other limiting treatment attached to a governed output under the `qualify` decision state.

### 2.11 Execution Relevance
Execution relevance indicates whether a candidate output may function as operational input.

Execution relevance is not execution permission.

### 2.12 Trace
A trace is the auditable decision record associated with a governed output.

### 2.13 Basis Codes
Basis codes are explicit normative decision-grounding codes that justify the assigned decision state.

### 2.14 Weaponized Form
Weaponized form is a materially operationalized form that turns content into disallowed or dangerous help through its structure, actionability, optimization, or operational use.

### 2.15 Safe Alternative
A safe alternative is a replacement output that does not materially advance a disallowed objective and is separately evaluated as its own candidate output.

## 3. Core Pipeline

A KPT-conformant implementation MUST evaluate each governed candidate output through a pipeline that preserves the distinction between classification, enforcement, and audit.

The minimum conceptual pipeline is:

1. assign zone
2. get applicable policy context
3. classify candidate output
4. determine enforcement action
5. build trace
6. durably write trace
7. permit display or execution only according to enforcement

The decision object and the enforcement object MUST remain distinct.

A governed output MUST receive a decision before it is allowed to influence or execute.

Where execution relevance is present, trace commit MUST occur before execution dispatch.

## 4. ZAT — Zone Assignment and Triage

KPT uses ZAT as runtime classification of the governed context.

KPT 2.3 defines three zones:

- `critical`
- `analytical`
- `creative`

Zone assignment MUST be performed at runtime.

Zone assignment MAY change during a session or pipeline.

If the zone changes, subsequent candidate outputs MUST be evaluated under the newly applicable zone.

Zone is distinct from profile and deployment mode.

- Zone classifies the governed context.
- Profile classifies the output target context.
- Deployment mode classifies the assurance posture of the system.

### 4.1 Zone meanings

`critical` applies where the governed output may materially affect safety, rights, health, legal position, financial position, execution, operational control, or other high-consequence outcomes.

`analytical` applies where the governed output is primarily explanatory, comparative, interpretive, or analytical, and is not principally creative or high-consequence by default.

`creative` applies where the governed output is primarily fictional, stylistic, artistic, or otherwise creative in a way that does not itself remove governance obligations.

### 4.2 Zone-assignment guidance

Zone assignment MUST be based on the governed context, not only on surface wording.

If a candidate output plausibly falls between `critical` and another zone, the implementation SHOULD assign `critical`.

Sensitive topic alone does not require `critical`, but material consequence potential does.

The same topic MAY fall into different zones in different runtime contexts.

## 5. Decision States

Each governed candidate output MUST receive exactly one of the following decision states:

- `deliver`
- `qualify`
- `refuse_assert`
- `refuse_help`

### 5.1 deliver
`deliver` means the candidate output is sufficiently supported for bounded delivery.

A `deliver` decision:
- MUST include `EPI-SUFFICIENT`
- MUST NOT include qualification semantics
- MUST NOT include limitation or safety-precedence basis codes

### 5.2 qualify
`qualify` means the candidate output may be delivered only with explicit qualification.

A `qualify` decision:
- MUST include `EPI-UNCERTAIN`
- MUST include `qualification_type != none`
- MAY include supporting limitation codes
- MUST NOT include safety-precedence basis codes
- MUST NOT be treated as executable as-is when execution relevance requires further verification

### 5.3 refuse_assert
`refuse_assert` means the candidate output lacks sufficient support for assertion.

A `refuse_assert` decision:
- MUST include `EPI-INSUFFICIENT`
- MUST have `qualification_type = none`
- MUST NOT be shown as the refused candidate output
- MUST NOT be executed

### 5.4 refuse_help
`refuse_help` means the candidate output is disallowed to provide.

A `refuse_help` decision:
- MUST be selected when safety-precedence basis applies
- MUST have `qualification_type = none`
- MUST NOT be shown as the refused candidate output
- MUST NOT be executed

## 6. Weaponized Form Control

KPT includes weaponized form control as a core requirement.

A candidate output MUST be classified under `refuse_help` when it is materially operationalized in weaponized form.

Operationalization, reframing, or rhetorical disguise MUST NOT be treated as a valid bypass of refusal.

Analytical, educational, or strategic framing does not by itself neutralize weaponized form.

A system MUST NOT downgrade a safety-governed candidate output to `qualify` or `refuse_assert` merely because the content is framed as analysis.

Weaponized form is a decision-governing condition, not a cosmetic wording issue.

## 7. Decision vs Enforcement

Decision state and enforcement action are distinct objects and MUST NOT be collapsed into one field or one implicit behavior.

- **Decision state** answers what the output is.
- **Enforcement action** answers what the system does because of that status.

A conformant implementation MUST be able to represent a governed output as, for example:

- qualified but visible
- visible but execution-blocked
- refused for assertion
- refused for help
- replaced by a separately evaluated safe alternative

A stricter deployment policy MAY strengthen enforcement.  
It MUST NOT weaken baseline enforcement required by the standard.

## 8. Output ≠ Action

KPT adopts the principle that output is not action.

A generated string, instruction candidate, recommendation, parameter set, or tool argument candidate MUST NOT be treated as equivalent to execution merely because it exists.

Before influence or execution, a governed candidate output MUST be:

1. evaluated
2. classified
3. enforced
4. traced

Execution relevance indicates that a candidate output may function as operational input.  
It does not by itself authorize execution.

This distinction is especially important in agent-facing and tool-using systems.

## 9. Profiles and Deployment Modes

KPT 2.3 defines two profiles:

- `KPT-H`
- `KPT-A`

KPT 2.3 defines two deployment modes:

- `General`
- `High-Assurance`

Valid combinations include:

- `KPT-H-General`
- `KPT-H-High-Assurance`
- `KPT-A-General`
- `KPT-A-High-Assurance`

Profile, deployment mode, and zone are distinct dimensions.

Profile classifies the output target context.  
Deployment mode classifies the assurance posture.  
Zone classifies the runtime governed context.

Profile and deployment mode SHOULD be recorded in trace when determinable.

For stronger conformance tiers:
- agent-facing traces MUST record `profile`
- high-assurance traces MUST record `deployment_mode`

## 10. Audit Trace

Each governed candidate output MUST produce a traceable decision event.

The trace MUST bind together:
- the evaluated candidate output
- the decision state
- the basis codes
- the qualification status
- the execution relevance
- the enforcement action
- the policy and engine versions

At minimum, a trace object MUST include:

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

The trace MUST be associated with exactly one evaluated candidate output.

If a blocked candidate output is replaced with refusal text or a safe alternative, the replacement MUST receive a new decision and a new trace.

Trace is not a cosmetic log.  
Trace is part of the governance boundary.

### 10.1 Integrity and chaining
Trace integrity SHOULD be tamper-evident.

Where implemented, `previous_trace_hash` and `integrity_hash` SHOULD support append-only or equivalent tamper-evident chaining.

Trace chain order is authoritative.  
Timestamp alone is insufficient to prove correct execution ordering.

### 10.2 Rationale
`rationale` MUST be audit-suitable.

`rationale` MUST be concise, MUST NOT be empty, and MUST NOT exceed 512 characters.

`rationale` MUST summarize the operative reason for the decision in plain audit language.

`rationale` MUST NOT be used as unrestricted chain-of-thought disclosure, MUST NOT expose sensitive hidden reasoning, and MUST NOT include operationally disallowed content.

## 11. Basis Codes

Decision states MUST be grounded in explicit basis codes.

KPT 2.3 defines the following basis-code families:

- `EPI` — epistemic status
- `SRC` — source limitation
- `TMP` — temporal limitation
- `SCP` — scope limitation
- `VER` — verification requirement
- `SAFE` — disallowed help
- `WF` — weaponized form

### 11.1 Primary decision drivers
The following are primary decision drivers:

- `EPI-SUFFICIENT`
- `EPI-UNCERTAIN`
- `EPI-INSUFFICIENT`
- `SAFE-DISALLOWED-HELP`
- `WF-WEAPONIZED-FORM`

### 11.2 Supporting limitations
The following are supporting limitation codes:

- `SRC-UNVERIFIED`
- `SRC-NO-PRIMARY`
- `TMP-TIME-SENSITIVE`
- `SCP-SCOPE-LIMITED`
- `VER-REQUIRED`

Supporting limitation codes refine a decision.  
They do not replace the primary decision driver.

### 11.3 Basis-code grammar
Basis codes:
- MUST be uppercase
- MUST be unique
- MUST be lexicographically sorted
- MUST correspond to materially operative reasons

The following pairs are mutually exclusive:
- `EPI-SUFFICIENT` and `EPI-UNCERTAIN`
- `EPI-SUFFICIENT` and `EPI-INSUFFICIENT`
- `EPI-UNCERTAIN` and `EPI-INSUFFICIENT`

### 11.4 Qualification derivation
`qualification_type` is valid only when `decision_state = qualify`.

For `qualify`:
- `EPI-UNCERTAIN` MUST be present
- if no supporting limitation family is present, `qualification_type = uncertainty`
- if exactly one supporting limitation family is present, `qualification_type` MUST match that family
- if more than one supporting limitation family is present, `qualification_type = mixed`

### 11.5 Safety precedence
If `SAFE-DISALLOWED-HELP` or `WF-WEAPONIZED-FORM` is present, `decision_state MUST = refuse_help`.

Safety precedence overrides epistemic sufficiency, uncertainty, or insufficiency for decision selection.

Factually accurate or well-supported harmful assistance remains `refuse_help`.

### 11.6 Extensions
Implementations MAY define extension basis codes under the reserved `X-*` namespace.

Extension codes:
- MUST NOT replace required standard basis codes
- MUST NOT override core decision grammar
- MUST NOT satisfy conformance requirements that depend on standard codes
- SHOULD use issuer-prefixed names such as `X-ORG-CODE`
- MAY refine audit context or organization-specific policy overlays

Base conformance ignores extension-code semantics unless a fixture or profile explicitly enables extension-aware evaluation.

## 12. Enforcement Baseline

KPT defines a baseline enforcement mapping.

The canonical core enforcement object is:

```json
{
  "display": "allow | allow_with_qualification | block_original",
  "execution": "allow | block | not_applicable"
}
```

This core contract governs the evaluated candidate output itself.  
Richer demo/report-layer fields MAY exist outside the canonical decision and trace outputs, but they do not replace the core contract.

### 12.1 deliver
For `deliver`:

- `enforcement_action.display = allow`
- `enforcement_action.execution = allow` only when the output is execution-relevant and the route actually enters execution
- otherwise `enforcement_action.execution = not_applicable`

A stricter deployment mode MAY add additional controls.  
It MUST NOT weaken conformance requirements elsewhere.

### 12.2 qualify
For `qualify`:

- `enforcement_action.display = allow_with_qualification`

If `execution_relevance = false`:
- `enforcement_action.execution = not_applicable`

If `execution_relevance = true` for an execution-capable route:
- `enforcement_action.execution = block`

### 12.3 refuse_assert
For `refuse_assert`:

- `enforcement_action.display = block_original` for the refused candidate output
- `enforcement_action.execution = block` or `not_applicable` depending on route and execution relevance

### 12.4 refuse_help
For `refuse_help`:

- `enforcement_action.display = block_original` for the refused candidate output
- `enforcement_action.execution = block` or `not_applicable` depending on route and execution relevance

If a safe alternative is provided, it MUST be separately evaluated and separately traced.

## 13. Temporal Requirements

A conformant implementation MUST satisfy decision-before-action ordering.

If a candidate output is execution-relevant:
- decision MUST exist before execution dispatch
- trace MUST be durably written before execution dispatch

Post-hoc trace logging is non-conformant.

If a blocked candidate output is followed by a replacement output:
- the blocked candidate MUST be traced first
- the replacement MUST be evaluated separately
- the replacement MUST receive its own trace

Trace collapse between blocked and replacement outputs is non-conformant.

## 14. Minimal Conformance Requirements

A system is minimally conformant with KPT 2.3 only if it satisfies all of the following:

1. It assigns a valid zone at runtime.
2. It assigns exactly one decision state to each governed candidate output.
3. It keeps decision state and enforcement action distinct.
4. It grounds decisions in valid basis codes.
5. It applies qualification rules consistently.
6. It enforces safety precedence.
7. It emits trace records containing all required core trace fields.
8. It satisfies decision-before-action ordering.
9. It blocks execution where required by the standard.
10. It does not collapse blocked and replacement outputs into one trace record when both occur.

A system is non-conformant if it:
- treats post-hoc logging as sufficient
- allows qualified execution-relevant output to execute as-is
- displays refused candidate outputs as allowed candidate outputs
- violates safety precedence
- omits required trace fields
- substitutes documentation claims for observed conformant behavior

## 15. Conformance Tiers

### 15.1 Baseline Conformance
Baseline conformance requires:
- all required core trace fields
- valid decision grammar
- valid enforcement mapping
- valid temporal ordering
- passing canonical positive and negative fixtures

### 15.2 Enhanced Conformance
Enhanced conformance adds stronger expectations for:
- direct auditability
- trace consistency
- recommended trace extensions such as `profile` and `deployment_mode`

### 15.3 Agent Conformance
Agent conformance requires:
- correct handling of execution-relevant outputs
- `profile` present on agent-facing traces

### 15.4 High-Assurance Conformance
High-Assurance conformance requires:
- stronger temporal evidence
- `deployment_mode` present on high-assurance traces
- no critical enforcement failures

### 15.5 Agent + High-Assurance Conformance
Agent + High-Assurance conformance requires:
- all agent-facing and high-assurance requirements
- zero tolerance for critical failures involving:
  - safety-precedence violations
  - missing trace before execution
  - execution of qualified execution-relevant outputs without required blocking

## 16. Summary

KPT 2.3 is a standard for AI output decision governance.

It introduces a runtime layer that classifies candidate outputs before they are allowed to influence or execute.

Its core principles are:

- AI output is not action.
- Every governed output must receive a decision before influence or execution.
- Decision state is not enforcement action.
- Trace before trust.

KPT does not solve every problem in AI safety, robustness, or risk.  
It governs a specific boundary: the point at which model output becomes admissible, relied upon, or executable.

That boundary is where KPT operates.