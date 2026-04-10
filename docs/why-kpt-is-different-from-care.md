# Why KPT Occupies a Different Governance Locus from CARE-Like Models

## Strategic Positioning Note v0.2

**Author:** Kristjan Jõgi  
**Status:** Draft  
**Applies to:** KPT 2.3

---

## 1. Purpose

This note explains why KPT should not be read as merely another runtime-governance concept in generic safety language.

Its key distinction is structural:

**KPT governs candidate-output admissibility before influence or execution.**

That is a different governance locus from models whose center of gravity is mainly:
- execution legitimacy
- authority verification
- control-surface enforcement
- post-decision runtime control

This note is a **positioning clarification**, not a benchmark claim and not a proof that KPT is universally superior.

---

## 2. The short version

A CARE-like model may mainly ask:

**“Is this action legitimate to execute?”**

KPT mainly asks:

**“Is this candidate output admissible before it is allowed to influence anyone or anything?”**

That places KPT earlier in the consequential chain.

---

## 3. Why that difference matters

Many important failures happen before a tool call or API execution:
- unsupported claims are presented as authoritative
- uncertain recommendations are delivered as if they are firm conclusions
- manipulative or weaponized framing is handed to a human user
- harmful help is displayed even if no tool is triggered
- a user relies on weak output and acts on it manually

KPT is built to govern that earlier boundary.

---

## 4. KPT’s center of gravity

KPT starts from the proposition that:

**AI output is not action.**

Therefore generated output must first be treated as a **candidate output**.

That candidate output is then evaluated before influence or execution through:
- zone assignment
- profile
- deployment mode
- safety evaluation
- epistemic sufficiency
- decision state assignment
- enforcement mapping
- trace emission

This makes KPT an **output decision-governance model**.

---

## 5. What this means in practice

KPT makes several distinctions explicit:
- `deliver`
- `qualify`
- `refuse_assert`
- `refuse_help`

It also keeps these separate:
- `decision_state` = what the output is
- `enforcement_action` = what the runtime does because of that status

That matters because a weakly supported output and a harmful output are not the same thing, even if both are blocked from execution.

---

## 6. Where CARE-like models may still be stronger

This note is not a dismissal of CARE-like runtime governance models.

They may still be stronger in downstream areas such as:
- authority verification detail
- execution-legitimacy proof
- invariants over live operational state
- rollback design
- state-integrity proof after action
- cryptographic or systems-level execution attestations

Those are valuable capabilities.

---

## 7. The right way to read the difference

The cleanest reading is not:

**“KPT is already proven stronger.”**

The cleaner reading is:

**“KPT governs an earlier boundary.”**

That earlier boundary is the admissibility boundary between candidate output and consequential path.

---

## 8. Stack interpretation

KPT can be understood as governing an earlier layer in a broader runtime-governance stack:

1. candidate output is generated
2. KPT determines admissibility before influence or execution
3. downstream control layers may then govern execution legitimacy, authority, state integrity, or post-action proof

That is a separation-of-locus claim, not a total-stack claim.

---

## 9. Bottom line

KPT’s strongest public distinction is this:

- output != action
- decision before influence
- decision before execution

That is the category language this note is intended to protect.
