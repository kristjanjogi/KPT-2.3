# KPT 2.3 Quickstart

## Start Here in 10 Minutes

**Author:** Kristjan Jõgi  
**Status:** Public quickstart guide  
**Applies to:** KPT 2.3  
**Authority class:** Normative minimum-contract guide

---

## 1. What KPT is

KPT is a standard for **AI output decision governance**.

Its core idea is simple:

**Model output is not action.**

A model may generate a response, recommendation, or tool proposal, but that output should not automatically be treated as:
- a reliable assertion;
- a safe instruction;
- an approved action;
- or an executable system command.

KPT inserts a governance step between **candidate output** and **real-world effect**.

This document describes the **public standard layer** of KPT. It does **not** disclose a full runtime-core implementation.

KPT begins from an epistemic humility rule:
- the system operates on representations, not direct reality;
- those representations may be incomplete or wrong;
- therefore weak grounding must not be turned into confident assertion.

In practice, that means KPT uses `qualify`, `refuse_assert`, or `refuse_help` where support is not strong enough for an unqualified `deliver`.

---

## 2. The core problem KPT solves

Most AI systems can already generate outputs.

The real problem begins one step later:
- Can this answer be shown to the user as-is?
- Does it need qualification?
- Is it too weak to assert?
- Is it harmful or weaponized?
- Can it trigger a tool, API, file change, or workflow?

KPT exists to answer those questions **before influence or execution**.

---

## 3. The four decision states

Every governed candidate output must receive one of these four decision states:
- `deliver`
- `qualify`
- `refuse_assert`
- `refuse_help`

### `deliver`
The output is admissible as-is.

### `qualify`
The output may be shown, but only with explicit uncertainty, limitation, or caution.

### `refuse_assert`
The output is not strong enough to present as an assertion.

### `refuse_help`
The output itself would be harmful, disallowed, or weaponized.

---

## 4. The single most important distinction

KPT separates:
- **decision state** = what the output is;
- **enforcement action** = what the system does because of that status.

This is a core design rule.

Example:
- a candidate output may be `qualify`;
- enforcement may still allow display with qualification;
- execution may still be blocked.

KPT does not treat those as the same thing.

---

## 5. The minimal KPT flow

~~~text
User/Input -> Model/Agent -> Candidate Output -> KPT Evaluation -> Decision State -> Enforcement Mapping -> Trace Written -> Display and/or Execution
~~~

This means:
1. the model generates a candidate output;
2. the candidate is evaluated;
3. a KPT decision is assigned;
4. enforcement is mapped;
5. trace is written;
6. only then may the output be shown or executed.

---

## 6. Two core principles to remember

### Decision before influence
If the output may shape belief, judgment, or reliance, it should be evaluated first.

### Decision before execution
If the output may trigger a tool, API, file change, workflow, or other external action, it must be evaluated first.

---

## 7. The three zones

KPT assigns a `zone` based on the **governed context** of the output.

### `critical`
Use when the output may materially affect safety, rights, money, operations, compliance, or external consequence.

### `analytical`
Use when the output is mainly for explanation, comparison, assessment, planning, or review.

### `creative`
Use when the output is mainly expressive, fictional, stylistic, or low-reliance.

Important:
- zone is not topic;
- zone is not profile;
- zone is not decision state.

---

## 8. The other two axes

### Profile
KPT uses:
- `KPT-H`
- `KPT-A`

Profile classifies the output target context.

### Deployment mode
KPT uses:
- `General`
- `High-Assurance`

Deployment mode controls the overall assurance posture of the system.

Important:
- `zone` = governed context;
- `profile` = output target context;
- `deployment_mode` = assurance posture;
- `decision_state` = final output status.

---

## 9. The minimum evaluation object

A minimal KPT evaluation begins with a normalized payload.

Example:

~~~json
{
  "input_ref": "req_001",
  "output_ref": "cand_001",
  "candidate_output": {
    "content": "You should send the payment now.",
    "content_type": "text"
  },
  "context": {
    "zone": "critical",
    "profile": "KPT-H",
    "deployment_mode": "High-Assurance",
    "execution_relevant": true,
    "user_visible": true,
    "downstream_target": "tool"
  },
  "provenance": {
    "source_basis": ["model_synthesis"],
    "verification_state": "unverified",
    "time_sensitivity": "medium"
  },
  "policy": {
    "policy_version": "kpt-2.3-core-v0.2",
    "engine_version": "kpt-mw-ref-v0.1"
  }
}
~~~

Reference schema:
- `schemas/evaluation-payload.schema.json`

---

## 10. The minimum decision result

Example:

~~~json
{
  "decision_state": "qualify",
  "basis_codes": ["EPI-UNCERTAIN", "VER-REQUIRED"],
  "qualification_type": "verification_required",
  "rationale": "Execution-relevant recommendation requires stronger verification before action.",
  "enforcement_action": {
    "display": "allow_with_qualification",
    "execution": "block"
  },
  "trace_id": "trace_001"
}
~~~

Reference schema:
- `schemas/decision-result.schema.json`

---

## 11. The minimum trace idea

A trace is not cosmetic logging.

A trace is part of the governance boundary.

At minimum, a KPT trace binds together:
- the evaluated candidate output;
- the decision state;
- the basis codes;
- the qualification status;
- the enforcement action;
- the policy version;
- the engine version.

Reference schema:
- `schemas/trace.schema.json`

---

## 12. What this quickstart is for

This quickstart is for understanding:
- what KPT governs;
- why output is not action;
- why decision must precede influence and execution;
- and how the minimum public contract hangs together.

It is not a full product manual, not a complete internal architecture disclosure, and not a substitute for the core standard.

---

## 13. Read next

Recommended order:
1. `docs/core-standard.md`
2. `docs/decision-result-schema.md`
3. `docs/trace-schema.md`
4. `docs/basis-codes-registry.md`
5. `docs/implementation-guide.md`
6. `docs/reference-middleware-spec.md`
