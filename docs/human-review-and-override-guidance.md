# KPT 2.3 Human Review and Override Guidance
## Working Guidance v0.1

Author: Kristjan Jõgi  
Status: Draft  
Applies to: KPT 2.3

---

## 1. Purpose

This document explains how human review and human override should work in systems implementing KPT 2.3.

Its purpose is to preserve KPT’s core runtime logic while allowing real systems to include:

- reviewer checkpoints;
- human approval gates;
- escalation paths;
- override handling;
- review-based re-evaluation.

This document is guidance for implementation and governance design.
It does not replace the KPT core standard.

---

## 2. Core Position

Human review is compatible with KPT.

Human review does **not** replace KPT decisioning.

The baseline rule remains:

- candidate output must be evaluated;
- decision state must be assigned;
- trace must be written;
- only then may downstream display or execution proceed according to enforcement and local policy.

Human review is therefore a downstream or adjacent governance step, not a substitute for the original decision record.

---

## 3. Locked Distinctions

Any implementation using human review must preserve the following distinctions.

### 3.1 Model output vs human action

- model output is a candidate output;
- human action is a separate governance or operational act.

### 3.2 Decision state vs human judgment

- `decision_state` describes the evaluated status of the candidate output;
- reviewer judgment describes what a human decides to do next.

### 3.3 Decision state vs enforcement action

- `decision_state` = what the output is;
- `enforcement_action` = what the system does because of that status.

### 3.4 Original trace vs review record

- the original KPT evaluation trace records the candidate evaluation;
- the review record records subsequent human inspection, approval, escalation, or override behavior.

A later human action must not erase or rewrite the original KPT decision trace.

---

## 4. Human Review Is Not a Bypass

Human review must not be used as a loophole that removes KPT from the runtime path.

The following are non-conformant patterns:

- direct model-output-to-execution because "a human will look at it later";
- post-hoc review after execution-relevant output already committed;
- replacing the original KPT decision with an untraced reviewer conclusion;
- allowing reviewer discretion to silently undo core decision logic with no new record.

Human review may strengthen governance.
It must not weaken decision-before-effect.

---

## 5. Recommended Position in Runtime Flow

The recommended pattern is:

```text
Candidate Output
  -> KPT Evaluation
  -> KPT Decision Result
  -> KPT Trace Written
  -> Human Review Gate (if policy requires)
  -> Final Enforcement / Display / Execution Outcome
```

This ordering preserves:

- decision before influence;
- decision before execution;
- trace before execution;
- separation between automated classification and later human action.

---

## 6. What Human Review May Examine

A reviewer may be shown some or all of the following:

- candidate output;
- normalized context;
- decision state;
- basis codes;
- qualification type;
- rationale;
- source or evidence references;
- execution relevance;
- proposed enforcement action;
- downstream target;
- prior related traces or lineage.

Reviewer access should be limited to what is necessary for safe, auditable judgment.

---

## 7. When Human Review Should Be Required

Human review should be considered when one or more of the following apply:

- zone is `critical`;
- deployment mode is `High-Assurance`;
- candidate output is execution-relevant;
- output would affect finance, operations, rights, safety, access, or external commitments;
- decision result is `qualify` in a context where uncertainty matters materially;
- decision result is `refuse_assert` and a business process requires escalation rather than immediate termination;
- policy requires approval before external action;
- output is destined for a regulated or highly sensitive workflow.

### 7.1 Strong default guidance

Recommended default posture:

- `critical` + execution-relevant -> human review strongly recommended;
- `critical` + `High-Assurance` + execution-relevant -> human approval should normally be required before execution;
- `analytical` -> selective review based on policy and downstream effect;
- `creative` -> usually review only for policy, brand, safety, or publication reasons.

---

## 8. Human Review Outcomes

Human review should produce a clearly recorded outcome.

Recommended outcome classes:

- confirm automated result;
- request more evidence;
- request re-evaluation with new information;
- request safe replacement;
- escalate to higher authority;
- deny execution;
- approve execution where policy requires human sign-off and KPT already permits execution;
- issue separate human-originated action.

These outcomes should be explicit and auditable.

---

## 9. Human Approval vs Human Override

These should be treated as different things.

### 9.1 Human approval

Human approval means a human confirms a path that KPT and local policy already permit, or a policy requires a human sign-off before the allowed action proceeds.

Example:
- KPT decision = `deliver`
- enforcement_action.execution = `allow`
- local policy still requires supervisor approval before committing external action

This is an approval gate, not necessarily an override.

### 9.2 Human override

Human override means a human changes downstream treatment relative to the automated enforcement outcome.

Example:
- automated result would display a qualified answer;
- reviewer blocks display pending more evidence.

Overrides must be logged as separate human acts.

---

## 10. Limits on Human Override

Not every automated outcome should be directly overridable in the same way.

### 10.1 `deliver`

Possible human actions:

- confirm;
- delay;
- request more evidence;
- deny execution under stricter business policy;
- require escalation.

### 10.2 `qualify`

Possible human actions:

- confirm qualified display;
- request more evidence;
- trigger re-evaluation with better verification;
- deny downstream use;
- escalate.

**Important rule:**
If a candidate output is execution-relevant and `qualify` blocked execution, a reviewer should not simply flip the same evaluated candidate to executable with no new basis.

The preferred paths are:

- add evidence and re-evaluate as a new governed candidate; or
- issue a separately recorded human-originated action outside the original candidate’s automatic execution path.

### 10.3 `refuse_assert`

Possible human actions:

- confirm refusal;
- request more evidence;
- request reformulation;
- generate or request a safe replacement;
- escalate to expert review.

A reviewer should not silently convert `refuse_assert` into unqualified automated display or execution for the same unsupported candidate with no new evidence.

### 10.4 `refuse_help`

Possible human actions:

- confirm refusal;
- supply safe alternative guidance;
- escalate under formal exception handling where allowed by policy;
- record incident or abuse handling.

A reviewer must not use override to surface disallowed harmful assistance as if KPT approved it.

---

## 11. Recommended Rule for Execution-Relevant Cases

For execution-relevant outputs, use the following default rule:

### 11.1 Automated execution may proceed only if:

- KPT permits execution; and
- trace has already been written; and
- any required human approval gate has been satisfied.

### 11.2 If KPT blocks execution:

A reviewer should normally choose one of these instead of directly forcing execution of the same blocked candidate:

- request new evidence;
- request revised candidate generation;
- trigger re-evaluation;
- issue a separate human-originated action;
- deny or terminate the action.

This preserves the integrity of the original KPT decision.

---

## 12. Review and Override Recording

Human review should be logged in a separate review or override record linked to the original KPT trace.

At minimum, the review record should capture:

- reviewed trace reference;
- reviewer role or identifier;
- timestamp;
- review outcome;
- whether an override occurred;
- rationale for the human decision;
- any new evidence references;
- whether re-evaluation was requested;
- whether execution was approved, denied, or escalated.

### 12.1 Current standard note

The current base KPT trace schema defines the core candidate-evaluation trace.
A fuller event-family model for review and override events should be standardized separately.

Until that model is finalized, implementations should still preserve linked records rather than collapsing reviewer actions into the original trace object.

---

## 13. Recommended Review Record Shape

Illustrative example:

```yaml
review_record:
  review_id: "uuid"
  reviewed_trace_id: "trace-123"
  reviewer_role: "supervisor"
  timestamp: "2026-03-09T12:00:00Z"
  outcome: "request_re_evaluation"
  override_applied: false
  human_rationale: "Additional verification is required before any external commitment."
  evidence_refs:
    - "doc-44"
  next_step: "re_evaluate"
```

This is guidance, not yet a locked base schema.

---

## 14. Re-Evaluation After Review

A reviewer may improve the evidence or context and then request re-evaluation.

Recommended pattern:

1. original candidate is evaluated by KPT;
2. original trace is written;
3. reviewer inspects result;
4. reviewer adds evidence, clarification, or constraints;
5. system creates a new candidate or updated governed payload;
6. KPT evaluates again;
7. a new trace is written.

This is preferable to retroactively rewriting the original decision.

---

## 15. Safe Replacement After Review

If a reviewer requests a safe replacement:

- the blocked original remains recorded as blocked;
- the replacement is treated as a new candidate output;
- the replacement receives a separate evaluation;
- the replacement receives a separate trace.

This preserves the dual-trace rule.

---

## 16. Zone-Aware Review Guidance

### 16.1 Critical

Recommended posture:

- strongest human review expectation;
- strongest audit requirement;
- strong preference for approval gates in execution-relevant flows;
- stronger reviewer competence and escalation requirements.

### 16.2 Analytical

Recommended posture:

- review when uncertainty, scope limits, or external impact justify it;
- routine display may not need review;
- execution-relevant cases may still require selective approval.

### 16.3 Creative

Recommended posture:

- review usually optional;
- stronger review where policy, safety, publication, or brand constraints apply.

---

## 17. Profile and Deployment Guidance

### 17.1 KPT-H

Recommended posture:

- more review triggers;
- lower tolerance for silent automation;
- more explicit reviewer logging;
- stronger approval requirements in sensitive cases.

### 17.2 KPT-A

Recommended posture:

- review based more on materiality and workflow need;
- lighter defaults where downstream effect is low.

### 17.3 General

Recommended posture:

- practical review only where it materially improves safety or correctness.

### 17.4 High-Assurance

Recommended posture:

- human review gates should be more common;
- reviewer identity and rationale should be logged consistently;
- override rules should be narrow, explicit, and testable.

---

## 18. Conformance-Relevant Expectations

A system using human review should be treated as stronger if it satisfies the following:

- original KPT decision is preserved even when a reviewer later acts;
- reviewer action is separately recorded;
- review does not bypass trace-before-execution;
- execution-relevant blocked candidates do not execute merely because of silent reviewer intervention;
- re-evaluation produces a new trace;
- safe replacement after review produces a new trace.

---

## 19. Non-Conformant Patterns

The following patterns should be treated as non-conformant or strongly discouraged:

- reviewer action with no audit record;
- deleting or overwriting the original KPT trace;
- using human review as a justification for skipping KPT;
- allowing `qualify` execution to proceed with no re-evaluation or separate human-originated act;
- converting `refuse_help` into displayed harmful assistance;
- post-hoc approval after execution already occurred;
- treating the reviewer’s action as if it were the original decision state.

---

## 20. Examples

### 20.1 Critical execution-relevant `deliver`

- KPT decision = `deliver`
- execution is allowed by automated enforcement
- local policy requires supervisor approval
- supervisor approves
- execution proceeds

This is a human approval gate layered on top of an already allowed path.

### 20.2 Execution-relevant `qualify`

- KPT decision = `qualify`
- execution blocked
- reviewer sees missing verification
- reviewer requests additional evidence
- system re-evaluates with new evidence
- new decision and new trace are produced

This is the preferred pattern.

### 20.3 `refuse_assert`

- KPT decision = `refuse_assert`
- reviewer determines the question is answerable with a narrower scope
- reviewer requests a constrained reformulation
- replacement candidate is generated
- replacement candidate is separately evaluated and traced

### 20.4 `refuse_help`

- KPT decision = `refuse_help`
- reviewer confirms block
- system displays safe alternative guidance
- safe alternative is separately evaluated if generated as a candidate output

---

## 21. Implementation Notes

Implementations should avoid placing reviewer logic inside hidden business workflow branches that are invisible to the governance record.

A good implementation makes it possible to answer later:

- what the original KPT decision was;
- whether a human reviewed it;
- what the reviewer did;
- whether new evidence was added;
- whether re-evaluation occurred;
- whether execution was blocked, approved, or denied.

---

## 22. Relationship to Other Artifacts

This guidance should remain aligned with:

- `docs/core-standard.md`
- `docs/trace-schema.md`
- `docs/conformance-methodology.md`
- `docs/reference-middleware-spec.md`
- `docs/reference-middleware-pseudocode.md`
- `docs/zone-assignment-guidance.md`
- `docs/rationale-field-guidance.md`
- `docs/trace-stability-and-replay-guidance.md`
- `schemas/evaluation-payload.schema.json`
- `schemas/decision-result.schema.json`
- `schemas/trace.schema.json`

---

## 23. Recommended Future Companion Artifact

A logical next companion document is:

```text
docs/trace-event-family-model.md
```

That document should define how candidate-evaluation traces relate to:

- review events;
- override events;
- execution attempts;
- execution commits;
- safe replacement lineage.

---

## 24. Recommended Repository Path

```text
docs/human-review-and-override-guidance.md
```
