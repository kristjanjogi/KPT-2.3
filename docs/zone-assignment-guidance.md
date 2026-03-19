# KPT 2.3 Zone Assignment Guidance
## Draft v0.2

Author: Kristjan Jõgi  
Status: Draft  
Applies to: KPT 2.3

---

## 1. Purpose

This document defines how to assign `zone` in KPT 2.3.

Zone assignment exists to answer one question:

**What governed context is this candidate output entering?**

Zone assignment is important because it affects:

- the strictness of admissibility evaluation;
- the expected evidence threshold;
- how uncertainty should be handled;
- how readily execution must be blocked;
- how conformance should be tested.

This document strengthens the previously noted weak point in KPT 2.3: zone assignment must not be left vague if the rest of the standard is expected to behave consistently.

---

## 2. Core Rule

Assign zone based on the **intended use and likely effect** of the candidate output, not merely its topic, wording style, or source.

In short:

- use `critical` when the candidate output may materially affect action, safety, rights, money, operations, security, compliance, or other significant external consequences;
- use `analytical` when the candidate output is mainly intended to inform understanding, judgment, planning, or review;
- use `creative` when the candidate output is mainly expressive, exploratory, fictional, stylistic, or low-reliance in nature.

If more than one zone seems plausible, either:

- split the candidate into separate evaluable outputs; or
- assign the stricter applicable zone.

---

## 3. What Zone Means

In KPT 2.3, `zone` means the **governed context** of the evaluated candidate output.

Zone is not the same as:

- topic category;
- industry vertical;
- user importance;
- product tier;
- profile;
- deployment mode;
- safety classification;
- enforcement action.

A single topic can appear in different zones depending on use.

Examples:

- a fictional courtroom scene may be `creative`;
- a legal explainer may be `analytical`;
- a candidate output used to approve a legal filing or commit a contractual action may be `critical`.

---

## 4. What Zone Does Not Mean

Zone must not be used as shorthand for claims the standard does not make.

Zone does **not** mean:

- the output is true;
- the output is safe;
- the output is allowed to execute;
- the output is low-risk simply because it is `creative`;
- the output is disallowed simply because it is `critical`.

Safety precedence still applies across all zones.
A `creative` output can still become `refuse_help`.
A `critical` output can still be `deliver` if the relevant standards are met.

---

## 5. The Three Zones

## 5.1 Critical

Assign `critical` when the candidate output may materially affect real-world outcomes and therefore demands the strictest governance posture.

Typical indicators:

- execution relevance with meaningful external effect;
- impact on health, safety, or bodily integrity;
- impact on legal rights, legal exposure, or formal status;
- impact on financial transfer, commitment, approval, or obligation;
- impact on identity, access, authentication, or security posture;
- impact on records, infrastructure, or operational state;
- impact on regulatory, compliance, or audit-sensitive action;
- impact on external commitments to customers, partners, authorities, or the public;
- strong likelihood that a human operator will rely on the output as a basis for consequential action.

Typical examples:

- approving or recommending a payment action;
- sending or authorizing an external operational email;
- proposing a production database change for execution;
- recommending a medical dosage;
- recommending a legal filing or compliance step for execution;
- approving access changes;
- triggering a workflow state that has contractual, financial, or operational consequence.

Default posture:

- evidence threshold is highest;
- uncertainty should more readily produce `qualify` or `refuse_assert`;
- execution-relevant outputs require especially strict control;
- trace-before-execution is non-negotiable.

---

## 5.2 Analytical

Assign `analytical` when the candidate output is primarily meant to inform understanding, assessment, review, comparison, planning, or non-final decision support.

Typical indicators:

- the output is presented as explanation, synthesis, analysis, comparison, or recommendation;
- the output may influence judgment, but is not itself a runtime commitment or direct execution;
- the user is expected to read, inspect, discuss, or review the content before any later action;
- correctness matters, but the output is not yet a direct external effect.

Typical examples:

- summarizing a report;
- comparing policy options;
- producing a risk memo;
- drafting an internal recommendation;
- answering a factual question in a way intended for practical understanding;
- producing a business analysis or scenario comparison;
- drafting a non-final response that will later be checked by a human.

Default posture:

- factual and evidentiary discipline still matters;
- uncertainty commonly maps to `qualify` rather than execution;
- the output may still become `critical` if reused in an execution path.

---

## 5.3 Creative

Assign `creative` when the candidate output is primarily expressive, imaginative, exploratory, stylistic, or low-reliance in nature.

Typical indicators:

- the output is fictional, artistic, playful, or brainstorming-oriented;
- factual correctness is not the primary value of the output;
- the output is not expected to be relied on as a basis for consequential action;
- the output is generated mainly for ideation, tone, form, or expression.

Typical examples:

- poems;
- stories;
- fictional worldbuilding;
- slogan brainstorming;
- style variations;
- image prompts for aesthetic experimentation;
- playful naming ideas.

Default posture:

- epistemic strictness is usually lowest;
- uncertainty often does not need the same treatment as in analytical or critical contexts;
- safety constraints still remain in force;
- if the output begins to make real claims or becomes action-guiding, zone should be promoted.

---

## 6. Primary Assignment Principle

Always assign zone according to the **most governance-relevant use** of the candidate output in the actual system context.

This means:

- not what the model “intended”;
- not what the content superficially resembles;
- not what the user says in isolation if the system path gives the output stronger effect;
- but what the output is actually able to influence or trigger.

A recommendation shown in a sandboxed mockup may be `analytical`.
The same recommendation directly connected to approval or execution may be `critical`.

---

## 7. Assignment Method

Use the following ordered method.

### Step 1: Identify the candidate output

Determine what object is being evaluated.

Examples:

- one natural-language answer;
- one JSON object;
- one tool proposal;
- one replacement response;
- one mixed output that may need splitting.

### Step 2: Identify intended use

Ask:

- Is this output mainly for understanding?
- Is this output mainly for expression?
- Is this output likely to guide or trigger meaningful action?

### Step 3: Identify likely effect if wrong

Ask whether an error, omission, or unjustified certainty could materially affect:

- safety;
- rights;
- money;
- compliance;
- security;
- operations;
- records;
- external commitments.

If yes, there is strong pressure toward `critical`.

### Step 4: Check execution relevance

Ask whether the output can directly or operationally enter:

- a tool call;
- an API request;
- a file or database write;
- a workflow transition;
- an external communication;
- another system commit.

If yes, zone should usually be `critical` unless the action is clearly non-consequential and tightly bounded.

### Step 5: Check human reliance expectation

Ask whether a reasonable operator would treat the output as:

- a basis for real decision-making;
- a factual assertion;
- a recommendation meant to be acted upon.

If yes, zone should usually be at least `analytical`, and may need to be `critical`.

### Step 6: Assign the strictest applicable zone

If multiple interpretations remain plausible, choose the stricter zone or split the object.

---

## 8. Fast Assignment Rule

Where a full analysis is not practical, apply this shortened rule.

### Use `critical` if:

- the output can materially influence or trigger consequential external action; or
- a reasonable person would rely on it for a high-stakes decision.

### Use `analytical` if:

- the output is mainly factual, reasoned, comparative, explanatory, or planning-oriented; and
- it is not itself a consequential execution step.

### Use `creative` if:

- the output is mainly expressive, fictional, stylistic, or exploratory; and
- it is not expected to be relied on for consequential real-world action.

---

## 9. Zone Promotion Rules

Zone assignment should be promoted upward when the candidate output gains stronger effect.

### 9.1 Creative -> Analytical

Promote from `creative` to `analytical` when the output shifts from expression to claim-bearing or decision-support use.

Examples:

- brainstorming slogans becomes a factual market-positioning summary;
- fictional content becomes real-world explanatory content;
- style drafting becomes a recommendation memo.

### 9.2 Analytical -> Critical

Promote from `analytical` to `critical` when the output becomes materially consequential.

Examples:

- an internal analysis becomes the direct basis for automated approval;
- a draft operational recommendation becomes an execution proposal;
- an explanatory answer becomes personalized high-stakes advice;
- a summary becomes an external filing or system commit step.

### 9.3 Direct Promotion to Critical

Any zone should be promoted to `critical` if the output enters a path that can directly commit consequential external effect.

---

## 10. Zone Demotion Rules

Zone may be assigned lower only when the implementation context genuinely lowers the governed effect.

Examples:

- a payment-approval template used purely as fictional sample text may be `creative`;
- a production command described as a tutorial example, with no execution path and clear non-operational framing, may be `analytical` rather than `critical`.

Demotion must not be based on mere labeling.

It is not enough to say:

- “for educational purposes only”; or
- “just a draft”;

if the actual system path or reasonable reliance pattern still makes the output consequential.

---

## 11. Mixed Outputs

Some candidate outputs contain multiple governance-relevant parts.

Examples:

- analysis plus tool call;
- explanation plus external email draft;
- factual summary plus execution recommendation.

Rule:

- if the parts can be separated, split them into separate candidate outputs and evaluate each independently;
- if they cannot be cleanly separated, assign the stricter applicable zone to the whole candidate.

This prevents low-governance framing from concealing a higher-governance component.

---

## 12. One Zone Per Evaluated Candidate

Each evaluated candidate output should receive one zone at evaluation time.

A system should not assign multiple simultaneous zones to the same candidate object.

If a single raw model response clearly contains separable governed objects, the correct method is:

1. split the response into candidate objects;
2. evaluate each object separately;
3. emit separate traces as needed.

---

## 13. Relationship to Profile and Deployment Mode

Zone is not profile.
Zone is not deployment mode.

These must remain distinct.

### Zone

Governed context of the candidate output.

### Profile

Output target context.

### Deployment mode

Assurance posture.

Interaction rule:

- zone determines the class of governed context;
- profile and deployment mode may tighten how that zone is handled;
- profile and deployment mode do not replace zone assignment.

Example:

The same `analytical` output may be treated more strictly under `KPT-H` and `High-Assurance`, but it does not become `critical` merely because the deployment posture is stricter.

---

## 14. Relationship to Decision State

Zone assignment does not decide the final KPT decision state by itself.

Zone influences how the candidate is evaluated, but the final `decision_state` still depends on:

- safety;
- epistemic sufficiency;
- verification status;
- time sensitivity;
- scope;
- execution relevance;
- policy rules.

Examples:

- a `critical` output may still be `deliver` if sufficiently supported;
- an `analytical` output may become `refuse_assert` if support is insufficient;
- a `creative` output may become `refuse_help` if it constitutes disallowed assistance.

---

## 15. Relationship to Enforcement

Zone assignment does not itself authorize or block execution.

The sequence remains:

1. zone assigned;
2. candidate evaluated;
3. decision state assigned;
4. enforcement mapped;
5. trace written;
6. runtime action allowed or blocked.

This distinction is mandatory.

---

## 16. Critical-Pressure Indicators

The following indicators create strong pressure toward `critical` assignment.

Use `critical` unless there is a strong, documented reason not to.

Indicators:

- financial transfer or approval;
- access control or identity change;
- legal filing, rights-affecting step, or compliance commitment;
- medical, safety, or bodily-risk action guidance;
- production infrastructure or operational system change;
- security control change;
- external customer/public/authority communication with commitment effect;
- workflow transition with material downstream effect;
- irreversible or difficult-to-reverse action;
- automated or semi-automated execution path;
- high-likelihood operator reliance for consequential action.

---

## 17. Creative-Pressure Indicators

The following indicators create pressure toward `creative` assignment.

Use `creative` only if no stronger governance context applies.

Indicators:

- fictional framing;
- stylistic variation;
- aesthetic exploration;
- open-ended brainstorming;
- playful ideation;
- low factual reliance;
- no meaningful execution path;
- no reasonable expectation of consequential real-world reliance.

---

## 18. Analytical Default Zone

When the output is neither clearly `critical` nor clearly `creative`, the default zone should generally be `analytical`.

This is the practical middle category for:

- factual answers;
- summaries;
- comparisons;
- reviews;
- recommendations that are not yet executional;
- decision-support content intended for inspection.

This default prevents ambiguous claim-bearing content from being incorrectly treated as merely creative.

---

## 19. Borderline Cases

### 19.1 Educational medical explanation

- general explanation of a condition: usually `analytical`
- personalized dosage recommendation or action instruction: usually `critical`

### 19.2 Legal content

- general educational explanation: usually `analytical`
- proposed filing content or rights-affecting instruction for execution: usually `critical`

### 19.3 Financial content

- market summary or comparison: usually `analytical`
- approval, transfer, or execution suggestion with real money effect: usually `critical`

### 19.4 Writing tasks

- poem, story, slogan variants: usually `creative`
- factual press statement draft: usually `analytical`
- external release statement with approval or commitment effect: usually `critical`

### 19.5 Coding tasks

- fictional or illustrative code snippet: usually `creative` or `analytical`, depending on reliance claim
- production migration, security rule, or operational script for execution: usually `critical`

### 19.6 Internal drafting

- draft memo for review: usually `analytical`
- draft that auto-sends or auto-commits after generation: usually `critical`

---

## 20. Default System Rules

An implementation may adopt the following defaults.

### Default Rule A

If `downstream_target` is `tool`, `api`, `file`, or `mixed`, apply strong critical presumption.

### Default Rule B

If the output is user-visible, claim-bearing, and intended to inform judgment, default to `analytical` unless a stronger zone applies.

### Default Rule C

If the output is primarily fictional, stylistic, or brainstorming-oriented and not materially relied upon, default to `creative`.

### Default Rule D

If the implementation cannot confidently distinguish between `analytical` and `critical`, use `critical`.

---

## 21. Minimal Assignment Rationale

A production implementation should be able to explain zone assignment briefly in audit-friendly language.

Example formats:

- `critical: execution-relevant operational action with material external effect`
- `analytical: factual synthesis intended for review, not direct execution`
- `creative: stylistic brainstorming with no consequential reliance path`

This rationale should be concise and should not contain chain-of-thought.

---

## 22. Conformance Expectations

A conformant implementation should satisfy the following zone-assignment expectations.

### 22.1 Consistency

The same governed context should not randomly move across zones without a material contextual change.

### 22.2 Context sensitivity

Zone assignment must reflect actual system use, not topic labels alone.

### 22.3 Strictness under ambiguity

If the zone is materially ambiguous, the stricter applicable zone should be chosen or the candidate should be split.

### 22.4 Execution sensitivity

Execution-relevant consequential outputs must not be casually classified as `analytical` or `creative`.

### 22.5 No collapse into profile or enforcement

Zone must remain distinct from profile, deployment mode, decision state, and enforcement action.

---

## 23. Recommended Conformance Test Themes

The following tests should exist in future or revised testpacks.

- same topic in different zones depending on governed use;
- analytical answer promoted to critical when execution path is added;
- creative brainstorming remaining creative when no reliance path exists;
- mixed output correctly split or escalated;
- execution-relevant qualify remaining blocked;
- incorrect demotion by disclaimer alone marked non-conformant.

---

## 24. Practical Quick Reference

Use this short reference when assigning zone.

### Choose `critical` when:

- the output can change the world outside the conversation in a meaningful way; or
- a reasonable person may rely on it for a high-stakes action.

### Choose `analytical` when:

- the output is mainly to understand, compare, explain, assess, or plan.

### Choose `creative` when:

- the output is mainly to imagine, style, explore, or brainstorm without meaningful real-world reliance.

### If unsure:

- split the candidate; or
- choose the stricter zone.

---

## 25. Recommended Repository Path

```text
docs/zone-assignment-guidance.md
```

---

## 26. Recommended Next Companion Section

After this document, the strongest companion section to finalize is:

**Rationale Field Guidance**

Reason:

Zone assignment explains governed context.
Rationale guidance explains how decisions are briefly justified without leaking chain-of-thought.
Together, they strengthen both implementation consistency and audit quality.
