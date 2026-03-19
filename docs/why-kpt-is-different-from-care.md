# Why KPT Is Different from CARE-Like Runtime Governance Models
## Strategic Positioning Note v0.1

Author: Kristjan Jõgi  
Status: Draft  
Applies to: KPT 2.3

---

## 1. Purpose

This note explains why KPT is not merely another runtime-governance concept and why it may be stronger than CARE-like models in one specific sense:

**KPT governs candidate-output admissibility before influence or execution.**

That is a different control position from models that focus mainly on execution legitimacy, authority verification, and post-decision runtime control.

---

## 2. The Short Version

A CARE-like model mainly asks:

**“Is this action legitimate to execute?”**

KPT mainly asks:

**“Is this candidate output admissible before it is allowed to influence anyone or anything?”**

This places KPT earlier in the control chain.

---

## 3. Why That Difference Matters

Many dangerous or governance-relevant failures happen **before** execution:

- unsupported claims are presented as authoritative;
- uncertain recommendations are delivered as if they are firm conclusions;
- manipulative or weaponized framing is handed to a human user;
- a harmful response is shown even if no API call is triggered;
- a system user relies on misleading output and acts on it manually.

A runtime model focused mainly on execution legitimacy may miss or under-govern this layer.

KPT is built specifically to govern that earlier boundary.

---

## 4. CARE-Like Models: Their Center of Gravity

CARE-like runtime governance models are usually strongest in areas such as:

- semantic admissibility of operational action;
- authority verification;
- execution legitimacy;
- control-surface enforcement;
- invariant enforcement;
- state integrity;
- audit and provenance after or around runtime action.

This is a serious and useful layer.

But its center of gravity is still:

**How execution becomes controlled and provable.**

---

## 5. KPT’s Center of Gravity

KPT’s center of gravity is different.

It starts from the proposition that:

**AI output is not action.**

Therefore the generated output must first be treated as a **candidate output**.

That candidate output is then evaluated before influence or execution through:

- zone assignment;
- profile;
- deployment mode;
- safety evaluation;
- epistemic sufficiency;
- decision state assignment;
- enforcement mapping;
- trace emission.

This produces a much earlier governance decision.

---

## 6. KPT’s Strongest Distinction

KPT’s strongest distinction is that it formalizes:

**decision before influence**  
and  
**decision before execution**

That means the model output does not get to travel downstream merely because it exists.

It must first be classified.

This is why KPT is not just an execution-control model.

It is an **output decision-governance model**.

---

## 7. Why KPT May Be Stronger

KPT may be stronger than CARE-like models in at least five important ways.

### 7.1 It governs human impact, not only machine execution

A harmful output does not need to call a tool to matter.

A human may:
- believe it;
- rely on it;
- repeat it;
- use it to justify action;
- use it to escalate conflict;
- use it to make real-world decisions.

KPT treats that as governance-relevant.

This is a major strength because many real failures happen through display and reliance, not only through automation.

### 7.2 It separates epistemic failure from harmful-help failure

KPT does not collapse everything into “allow” vs “block.”

It distinguishes:

- `deliver`
- `qualify`
- `refuse_assert`
- `refuse_help`

This is extremely important.

It allows the system to say:

- the output is good enough to deliver;
- the output is usable only with explicit limitation;
- the output is not sufficiently supported for assertion;
- the output is harmful or weaponizable and must be blocked.

This is more precise, more auditable, and more testable than a simple pass/fail gate.

### 7.3 It separates decision state from enforcement action

Many systems blur these together.

KPT keeps them distinct:

- `decision_state` = what the output is
- `enforcement_action` = what the runtime does because of that status

This matters because it makes the system easier to:
- audit;
- test;
- replay;
- dispute;
- and explain.

A blocked output and a weakly supported output are not the same thing, even if both ultimately fail to execute.

KPT captures that distinction explicitly.

### 7.4 It formalizes qualification as a first-class state

Most governance systems are much better at “yes” and “no” than at “yes, but only under limits.”

KPT formalizes this middle state through `qualify`.

This matters in real systems because many outputs are not:
- fully good,
- fully false,
- or fully prohibited.

They are admissible only with:
- uncertainty markers;
- scope limits;
- verification requirements;
- time-sensitivity warnings;
- source limitations.

KPT has a place for that.

### 7.5 It turns output governance into a standard, not only a concept

KPT is not just a diagram or a principle.

It is being structured as a standard with:

- core decision logic;
- trace schema;
- basis code registry;
- conformance methodology;
- test packs;
- schema artifacts;
- implementation guidance;
- middleware specification;
- pseudocode reference flow.

That makes it much easier to operationalize, validate, and contest.

---

## 8. What CARE-Like Models May Still Do Better

This comparison is not a dismissal of CARE-like models.

They may still be stronger in some downstream runtime areas, such as:

- authority verification details;
- execution legitimacy proof;
- invariants over live operational state;
- rollback design;
- state-integrity proofs after action;
- cryptographic or systems-level execution attestations.

These are valuable capabilities.

In fact, they may fit well as a later layer in a broader stack.

But they do not replace the earlier KPT question:

**Should this candidate output have been allowed to influence anything in the first place?**

---

## 9. The Stack Relationship

The cleanest way to see the relationship is this:

### KPT layer
Governs candidate-output admissibility before influence or execution.

### CARE-like layer
Governs legitimacy and integrity of execution once an action path is being considered or taken.

That means the two are not necessarily enemies.

But KPT sits earlier.

This is why the strongest positioning line is:

**KPT sits one layer earlier in the control chain.**

---

## 10. Strategic Positioning Language

Useful positioning lines:

### Option A
**CARE-like models focus on proving execution legitimacy.  
KPT focuses on deciding output admissibility before any influence or execution is allowed.**

### Option B
**KPT is not only an execution-control model. It is a decision-boundary standard for candidate outputs.**

### Option C
**Before execution legitimacy, there must be output admissibility. That is where KPT begins.**

### Option D
**KPT governs the moment between model output and real-world consequence.**

---

## 11. Why This Matters Commercially

This distinction is not just theoretical.

It matters because many buyers, regulators, and operators still lack a clean answer to:

- how outputs are classified before use;
- how uncertainty is handled before action;
- how harmful assistance is blocked before handoff;
- how traces are created before execution;
- how the same system governs both display and machine pathways.

KPT gives a cleaner answer to these questions than architectures that begin closer to execution only.

That may make KPT especially strong as:

- a standard;
- an advisory method;
- a runtime middleware layer;
- a conformance layer;
- a control-plane component for AI systems.

---

## 12. Final One-Sentence Conclusion

**CARE-like models focus on controlling whether execution is legitimate.  
KPT focuses on controlling whether candidate output is admissible before influence or execution is allowed at all.**

---

## 13. Recommended Repository Path

```text
docs/why-kpt-is-different-from-care.md
```
