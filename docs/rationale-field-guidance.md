# KPT 2.3 Rationale Field Guidance
## Guidance v0.1

Author: Kristjan Jõgi  
Status: Draft  
Applies to: KPT 2.3

---

## 1. Purpose

This document defines how the `rationale` field should be written in KPT 2.3 traces and related decision objects.

The purpose of the rationale field is to provide a concise, audit-usable justification for why a specific decision state was assigned to a specific evaluated candidate output.

The rationale field exists to support:

- audit review;
- trace readability;
- conformance assessment;
- implementation debugging;
- human interpretation of basis-code-driven decisions.

The rationale field is not a place for hidden reasoning, chain-of-thought, or freeform narrative.

---

## 2. Core Rule

The rationale field must be a **concise audit justification**.

It must explain, in short natural language, why the assigned decision state follows from the relevant basis codes and governed context.

In KPT terms:

- basis codes carry the formal decision basis;
- rationale states the short human-readable justification;
- rationale does not replace basis codes;
- basis codes do not replace rationale.

---

## 3. What the Rationale Field Is

The rationale field is:

- short;
- decision-focused;
- reviewer-readable;
- tied to the evaluated candidate output;
- tied to the assigned decision state;
- suitable for trace and audit records.

A good rationale helps a reviewer answer:

- what was the main reason for this decision;
- why this decision state was chosen instead of a less restrictive or more restrictive alternative;
- whether the trace is internally coherent.

---

## 4. What the Rationale Field Is Not

The rationale field is not:

- chain-of-thought;
- internal hidden reasoning dump;
- speculative self-analysis;
- a full explanation of all model behavior;
- a replacement for the candidate output;
- a replacement for conformance evidence;
- a long narrative summary.

It must not become a backdoor for exposing internal reasoning or recreating the entire evaluation process in prose.

---

## 5. Required Properties

A conformant rationale should satisfy the following properties.

### 5.1 Decision-linked

It must clearly support the assigned `decision_state`.

### 5.2 Basis-linked

It must be coherent with the selected `basis_codes`.

### 5.3 Context-aware

Where relevant, it should reflect the governed context, especially if zone, execution relevance, or verification state materially affected the decision.

### 5.4 Concise

It should be as short as possible while still being intelligible.

### 5.5 Audit-usable

It should be understandable to a reviewer without requiring access to hidden internal reasoning.

### 5.6 Non-sensitive by design

It should avoid reproducing unnecessary sensitive, harmful, or disallowed content.

---

## 6. Required Content

A good rationale usually contains three elements.

### 6.1 Decision basis in plain language

Example pattern:

- sufficient support existed;
- support was uncertain;
- support was insufficient;
- content was disallowed.

### 6.2 Material limiting or governing factor

Example pattern:

- currentness mattered;
- source verification was incomplete;
- scope exceeded available support;
- content constituted harmful assistance.

### 6.3 Why the decision state followed

Example pattern:

- therefore qualified display only;
- therefore assertion blocked;
- therefore execution blocked;
- therefore harmful assistance refused.

Not every rationale must mechanically include all three clauses, but it should contain enough information to make the trace intelligible.

---

## 7. Prohibited Content

The rationale field must not contain:

- chain-of-thought;
- step-by-step hidden reasoning;
- internal deliberation transcripts;
- speculative claims not supported by the evaluation record;
- irrelevant commentary;
- emotional or rhetorical language;
- unnecessary repetition of harmful, hateful, or dangerous candidate content;
- unnecessary disclosure of private or identifying user details.

### 7.1 Chain-of-thought prohibition

The rationale may summarize a decision basis.
It may not reproduce full intermediate reasoning.

Allowed:

- "Candidate output lacked sufficient support for assertion in a critical context."

Not allowed:

- "First the system considered three competing interpretations, then ranked source confidence, then reasoned that..."

---

## 8. Length Guidance

The rationale should normally be:

- one sentence; or
- two short sentences where needed.

Recommended practical range:

- approximately 8 to 35 words in ordinary cases.

Acceptable longer range when necessary:

- up to roughly 45 words for mixed or execution-relevant edge cases.

Longer rationale text should be exceptional and justified by implementation needs.

The objective is not literary style.
The objective is compact audit usefulness.

---

## 9. Style Guidance

The rationale should be written in plain, neutral language.

Preferred style:

- factual;
- brief;
- non-dramatic;
- non-speculative;
- directly tied to the decision.

Preferred patterns:

- "Candidate output met sufficiency requirements for the governed context."
- "Currentness was material and verification was insufficient for an unqualified answer."
- "Candidate output lacked sufficient support for assertion in the governed context."
- "Candidate output constituted disallowed assistance and was blocked."

Avoid:

- vague language;
- legalistic overgrowth;
- persuasive or defensive tone;
- long subordinate clauses.

---

## 10. Relation to Basis Codes

The rationale must align with the basis codes.

### 10.1 Basis codes are primary formal drivers

The formal decision logic remains in the basis codes and decision-state rules.

### 10.2 Rationale is explanatory glue

The rationale explains the decision in natural language for audit and review.

### 10.3 Inconsistency is non-conformant

If the rationale says one thing but the basis codes imply another, the trace is defective.

Examples:

- `qualify` with `EPI-UNCERTAIN` should not have a rationale claiming full certainty.
- `refuse_assert` with `EPI-INSUFFICIENT` should not have a rationale claiming sufficient support.
- `refuse_help` with safety codes should not have a rationale framed as mere uncertainty.

---

## 11. Relation to Decision State

The rationale must fit the assigned decision state.

### 11.1 `deliver`

A `deliver` rationale should state that the candidate output met sufficiency requirements for the governed context.

It may optionally mention why no limiting or safety conditions applied.

### 11.2 `qualify`

A `qualify` rationale should state that the candidate output was admissible only with explicit uncertainty or limitation.

It should usually mention the material limitation family, such as:

- time sensitivity;
- source limitation;
- scope limitation;
- verification requirement.

### 11.3 `refuse_assert`

A `refuse_assert` rationale should state that the candidate output lacked sufficient support for assertion.

It should not be phrased as if the output were simply mildly uncertain.

### 11.4 `refuse_help`

A `refuse_help` rationale should state that the candidate output constituted disallowed assistance or weaponized form.

It should not reduce a safety refusal to mere epistemic insufficiency.

---

## 12. Relation to Enforcement Action

The rationale explains why the decision was assigned.

It may mention an enforcement consequence where that consequence is materially tied to the decision, especially for execution-relevant outputs.

However, the rationale must not collapse decision state into enforcement action.

Preferred:

- "Currentness was material and verification was insufficient for an unqualified answer; execution remained blocked."

Not preferred:

- "Execution was blocked, therefore the decision was qualify."

The decision comes first.
The enforcement consequence follows from it.

---

## 13. Relation to Zone, Profile, and Deployment Mode

The rationale does not need to restate all context fields in every case.

It should mention context only where context materially explains the decision.

Examples:

- critical-zone sufficiency threshold;
- execution-relevant output under `qualify`;
- higher-assurance verification requirement;
- creative output demoted or promoted due to execution relevance.

Good use of context:

- "Candidate output lacked sufficient support for assertion in a critical context."
- "Verification remained incomplete for a High-Assurance execution-relevant output."

Poor use of context:

- "The zone was analytical, the profile was KPT-A, and the deployment mode was General."

The rationale should not become a dump of metadata already present elsewhere in the trace.

---

## 14. Authoritative Location Rule

The authoritative audit record is the trace.

Therefore:

- the trace object should always contain a rationale;
- lightweight surfaced decision objects may omit rationale in limited implementations only if the authoritative trace still contains it;
- stricter implementations should include rationale in both trace and surfaced decision result.

This rule keeps audit completeness anchored in the trace even if interface-level responses are minimized.

---

## 15. Decision-State-Specific Guidance

### 15.1 Deliver rationale patterns

Good patterns:

- "Candidate output met sufficiency requirements for the governed context."
- "Support was sufficient and no limitation or safety conditions applied."

Bad patterns:

- "Looks probably fine."
- "The system felt confident."
- "Allowed because nothing seemed wrong."

### 15.2 Qualify rationale patterns

Good patterns:

- "Currentness was material and verification was insufficient for an unqualified answer."
- "Candidate output was admissible only with source-related uncertainty."
- "Scope exceeded available support, so only qualified display was allowed."

Bad patterns:

- "This is true but maybe not fully true."
- "The model had mixed feelings."
- "Qualified because we preferred caution."

### 15.3 Refuse_assert rationale patterns

Good patterns:

- "Candidate output lacked sufficient support for assertion in the governed context."
- "Verification requirements were not met for assertion."

Bad patterns:

- "We were not fully comfortable."
- "This might be wrong."
- "Blocked because it did not seem ideal."

### 15.4 Refuse_help rationale patterns

Good patterns:

- "Candidate output constituted disallowed assistance and was blocked."
- "Candidate output matched weaponized harmful form and was refused."

Bad patterns:

- "This answer felt unsafe somehow."
- "The tone was questionable."
- "We chose not to provide more detail."

---

## 16. Qualification-Type Guidance

Where `decision_state = qualify`, the rationale should usually cohere with `qualification_type`.

Examples:

### 16.1 `uncertainty`
- "Candidate output was admissible only with explicit uncertainty."

### 16.2 `time_sensitive`
- "Currentness was material and available verification was insufficient for an unqualified answer."

### 16.3 `source_limited`
- "Candidate output was admissible only with source-related limitation."

### 16.4 `scope_limited`
- "Candidate output exceeded the supported scope and required qualification."

### 16.5 `verification_required`
- "Further verification was required before assertion or execution."

### 16.6 `mixed`
- "Candidate output was admissible only with mixed source, scope, or currentness limitations."

The rationale does not need to repeat the exact code names.
It should express the limiting family in readable language.

---

## 17. Execution-Relevant Outputs

For execution-relevant outputs, the rationale should make sense in a trace that may later be reviewed against runtime behavior.

Where relevant, it may mention that execution could not proceed under the assigned decision.

Examples:

- "Verification remained insufficient for an execution-relevant unqualified decision."
- "Candidate output was admissible only with uncertainty; execution therefore remained blocked."

The rationale should still center on the decision basis, not on the operational consequence alone.

---

## 18. Safe Replacement Cases

If an original candidate output is blocked and a safe replacement is generated:

- the original trace needs its own rationale;
- the replacement trace needs its own rationale;
- the two rationales should not be collapsed into one statement.

Example:

### Original blocked candidate
- "Candidate output constituted disallowed assistance and was blocked."

### Replacement candidate
- "Replacement output provided safe high-level guidance without disallowed operational detail."

This distinction is important for the two-trace rule.

---

## 19. Human Review and Override Context

Where human review exists, the rationale should still describe the KPT decision basis for the evaluated candidate output.

It should not be rewritten into a reviewer-opinion field unless the implementation explicitly defines a separate override record.

Recommended separation:

- KPT rationale = why the system assigned the decision;
- reviewer note = why a human later confirmed, modified, or escalated handling.

The two should not be merged casually.

---

## 20. Minimal Rationale Template

A practical template is:

**[candidate/admissibility status] + [material reason] + [decision consequence]**

Examples:

- "Candidate output met sufficiency requirements for the governed context."
- "Currentness was material and verification was insufficient for an unqualified answer."
- "Candidate output lacked sufficient support for assertion in the governed context."
- "Candidate output constituted disallowed assistance and was blocked."

This is usually enough.

---

## 21. Good vs Poor Rationale Comparison

### Good

- specific enough to audit;
- short enough to scan;
- consistent with basis codes;
- consistent with decision state;
- does not reveal hidden reasoning.

### Poor

- vague or hand-wavy;
- inconsistent with codes;
- overly long;
- defensive or rhetorical;
- chain-of-thought-like;
- overloaded with repeated metadata.

---

## 22. Conformance Expectations

An implementation should be treated as non-conformant or weakly conformant if any of the following occur repeatedly.

### 22.1 Missing rationale in authoritative trace

If the trace is meant to be the authoritative audit object and rationale is absent, trace quality is defective.

### 22.2 Rationale inconsistent with basis codes

If the natural-language rationale contradicts the basis codes, the record is defective.

### 22.3 Rationale inconsistent with decision state

If the rationale sounds like `qualify` but the trace says `deliver`, or similar mismatches exist, the record is defective.

### 22.4 Rationale contains chain-of-thought

If the rationale includes hidden intermediate reasoning or a reasoning transcript, the record is non-conformant.

### 22.5 Rationale used as post-hoc patch

If the rationale appears to be invented after enforcement or execution rather than recorded as part of the decision event, the record is non-conformant.

---

## 23. Example Rationales by Case Type

### 23.1 Ordinary deliver

- "Candidate output met sufficiency requirements for the governed context."

### 23.2 Analytical qualify, time-sensitive

- "Currentness was material and verification was insufficient for an unqualified answer."

### 23.3 Execution-relevant qualify

- "Further verification was required before any execution-relevant unqualified decision."

### 23.4 Refuse_assert

- "Candidate output lacked sufficient support for assertion in the governed context."

### 23.5 Refuse_help

- "Candidate output constituted disallowed assistance and was blocked."

### 23.6 Mixed qualification

- "Candidate output was admissible only with mixed source and scope limitations."

---

## 24. Example Invalid Rationales

The following examples should be treated as invalid or poor-quality rationale text.

- "The system thought deeply and concluded this was probably okay."
- "After considering several hidden factors and ranking them internally, the best answer was..."
- "This was blocked because we did not like it."
- "The model was unsure about many things and had a long internal debate."
- "The content was maybe true in some sense but we were kind of cautious about it."

These fail because they are vague, chain-of-thought-like, or not audit-usable.

---

## 25. Implementation Recommendations

Implementations should:

- keep rationale generation templated or bounded where possible;
- validate rationale against decision state and basis codes;
- keep rationale length constrained;
- avoid quoting raw harmful candidate content;
- store rationale in the trace before execution-relevant commit;
- test rationale quality in conformance and negative testpacks.

Stronger implementations may use policy-side linting rules for rationale text.

---

## 26. Recommended Validation Rules

A validator or test harness should check at minimum that:

- rationale exists in the authoritative trace;
- rationale is non-empty;
- rationale is short;
- rationale is coherent with `decision_state`;
- rationale is coherent with `basis_codes`;
- rationale does not obviously include chain-of-thought markers;
- rationale does not misstate enforcement as the primary basis of the decision.

---

## 27. Future Expansion Points

Later revisions may add:

- bounded character limits by deployment mode;
- stricter rationale requirements for High-Assurance;
- multilingual rationale guidance;
- reviewer override rationale rules;
- rationale lint categories for conformance testing.

---

## 28. Recommended Repository Path

```text
docs/rationale-field-guidance.md
```
