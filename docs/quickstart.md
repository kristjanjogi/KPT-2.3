# KPT 2.3 Quickstart
## Start Here in 10 Minutes

Author: Kristjan Jõgi  
Status: Draft  
Applies to: KPT 2.3  
Authority class: Normative minimum-contract guide

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

A candidate output may be:
- `qualify`

while enforcement may be:
- display allowed with qualification;
- execution blocked.

KPT does not treat those as the same thing.

---

## 5. The minimal KPT flow

```text
User/Input
  -> Model/Agent
  -> Candidate Output
  -> KPT Evaluation
  -> Decision State
  -> Enforcement Mapping
  -> Trace Written
  -> Display and/or Execution
```

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

Profile controls output-handling caution posture.

### Deployment mode
KPT uses:
- `General`
- `High-Assurance`

Deployment mode controls the overall assurance posture of the system.

Important:
- `zone` = governed context;
- `profile` = output-handling caution context;
- `deployment_mode` = assurance posture;
- `decision_state` = final output status.

---

## 9. The minimum evaluation object

A minimal KPT evaluation begins with a normalized payload.

Example:

```json
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
    "source_basis": ["model synthesis"],
    "verification_state": "unverified",
    "time_sensitivity": "medium"
  },
  "policy": {
    "policy_version": "kpt-2.3-core-v0.2",
    "engine_version": "kpt-mw-ref-v0.1"
  }
}
```

Reference schema:
- `schemas/evaluation-payload.schema.json`

---

## 10. The minimum decision result

Example:

```json
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
```

Reference schema:
- `schemas/decision-result.schema.json`

---

## 11. The minimum trace object

Example:

```json
{
  "trace_id": "trace_001",
  "timestamp": "2026-03-10T09:14:29Z",
  "input_ref": "req_001",
  "output_ref": "cand_001",
  "zone": "critical",
  "profile": "KPT-H",
  "deployment_mode": "High-Assurance",
  "decision_state": "qualify",
  "basis_codes": ["EPI-UNCERTAIN", "VER-REQUIRED"],
  "rationale": "Execution-relevant recommendation requires stronger verification before action.",
  "qualification_type": "verification_required",
  "execution_relevance": true,
  "enforcement_action": {
    "display": "allow_with_qualification",
    "execution": "block"
  },
  "policy_version": "kpt-2.3-core-v0.2",
  "engine_version": "kpt-mw-ref-v0.1",
  "previous_trace_hash": "prev_hash_here",
  "integrity_hash": "integrity_hash_here"
}
```

Reference schema:
- `schemas/trace.schema.json`

---

## 12. The rule that changes everything

For execution-relevant outputs:

**trace must be written before execution begins.**

This is one of the strongest KPT claims.

KPT is not only about evaluating outputs.
It is about controlling the boundary between:

- candidate output;
- and real-world effect.

---

## 13. Human path vs machine path

### Human path

```text
query -> model -> candidate output -> KPT -> trace -> display
```

Question being answered:

**Can this be shown?**

### Machine path

```text
query -> model -> candidate output -> KPT -> trace -> execution gate -> machine action
```

Question being answered:

**Can this be executed?**

---

## 14. One simple example

### Input
A user asks an assistant to send an operational message or trigger a real action.

### Candidate output
The model proposes:

> “Proceed with the database update now.”

### KPT handling
- `zone`: `critical`
- `profile`: `KPT-H`
- `deployment_mode`: `High-Assurance`
- execution relevance: `true`
- verification state: insufficient

### Result
- `decision_state`: `qualify`
- display may be allowed with qualification
- execution must be blocked
- trace must be written first

This shows a core KPT rule:

**qualified execution-relevant output does not execute.**

---

## 15. Safe replacement rule

If an original candidate output is blocked and a safe replacement is shown, KPT requires:

- one trace for the blocked candidate;
- one trace for the replacement output.

This is the dual-trace rule.

---

## 16. What KPT is not

KPT is not:

- a generic moderation layer;
- a promise that the model is always true;
- a logging system added after the fact;
- a tool that replaces domain experts;
- a shortcut for skipping system design.

It is a **decision-governance boundary**.

---

## 17. The fastest way to understand KPT

If you remember only five lines, remember these:

1. **Model output is not action.**
2. **Every governed output needs a decision before influence or execution.**
3. **Decision state is not enforcement action.**
4. **Trace before trust.**
5. **Execution-relevant qualified output does not execute.**

---

## 18. What to read next

If you want the shortest path through the repository, read in this order:

1. `README.md`
2. `docs/core-standard.md`
3. `docs/zone-assignment-guidance.md`
4. `docs/rationale-field-guidance.md`
5. `docs/reference-middleware-spec.md`
6. `docs/reference-middleware-pseudocode.md`
7. `schemas/evaluation-payload.schema.json`
8. `schemas/decision-result.schema.json`
9. `schemas/trace.schema.json`
10. `docs/conformance-methodology.md`

---

## 19. What to build first

If you are implementing KPT, start with this minimum stack:

- evaluation payload
- decision result
- trace object
- execution gate
- append-only trace write

If you are publishing KPT, strengthen this next:

- quickstart
- changelog
- self-attestation checklist
- reference demo

---

## 20. Recommended repository path

```text
docs/quickstart.md
```

---

## 21. One-line summary

KPT 2.3 is a runtime decision-governance standard that classifies AI candidate outputs before influence or execution, separates decision state from enforcement, and requires auditable trace emission before execution-relevant action.
