# KPT Evaluator Flow Pseudocode
## Reference Middleware Pseudocode v0.1

Author: Kristjan Jõgi  
Status: Draft  
Applies to: KPT 2.3

---

## 1. Purpose

This pseudocode defines a reference evaluator flow for KPT middleware.

It is intended to show, at implementation level, how a governed candidate output moves through:

- normalization;
- context resolution;
- safety checks;
- epistemic checks;
- decision assignment;
- trace emission;
- enforcement mapping.

This is not production code.  
It is an implementation-oriented reference.

---

## 2. Top-Level Evaluate Function

```text
function evaluate_candidate(evaluation_payload):

    normalized = normalize_payload(evaluation_payload)

    context = resolve_context(normalized)
    policy = load_policy(normalized.policy.policy_version)

    execution_relevance = determine_execution_relevance(normalized, context)

    safety_result = evaluate_safety(normalized, context, policy)

    if safety_result.has_disallowed_help == true
       or safety_result.has_weaponized_form == true:

        decision_state = "refuse_help"
        basis_codes = build_safety_basis_codes(safety_result)
        qualification_type = null

        enforcement_action = map_enforcement(
            decision_state = decision_state,
            execution_relevance = execution_relevance
        )

        rationale = build_rationale(
            decision_state,
            basis_codes,
            context,
            safety_result = safety_result,
            epistemic_result = null
        )

        trace = emit_trace(
            normalized = normalized,
            context = context,
            decision_state = decision_state,
            basis_codes = basis_codes,
            qualification_type = qualification_type,
            execution_relevance = execution_relevance,
            enforcement_action = enforcement_action,
            rationale = rationale,
            policy = policy
        )

        return build_decision_result(
            decision_state,
            basis_codes,
            qualification_type,
            rationale,
            enforcement_action,
            trace.trace_id
        )

    epistemic_result = evaluate_epistemic(normalized, context, policy)

    if epistemic_result.status == "insufficient":
        decision_state = "refuse_assert"
        basis_codes = build_refuse_assert_basis_codes(epistemic_result)
        qualification_type = null

    else if epistemic_result.status == "uncertain":
        decision_state = "qualify"
        basis_codes = build_qualify_basis_codes(epistemic_result)

        if not contains(basis_codes, "EPI-UNCERTAIN"):
            basis_codes = prepend("EPI-UNCERTAIN", basis_codes)

        qualification_type = derive_qualification_type(basis_codes)

    else if epistemic_result.status == "sufficient":
        decision_state = "deliver"
        basis_codes = ["EPI-SUFFICIENT"]
        qualification_type = null

    else:
        decision_state = "qualify"
        basis_codes = ["EPI-UNCERTAIN", "SCP-SCOPE-LIMITED"]
        qualification_type = "mixed"

    enforcement_action = map_enforcement(
        decision_state = decision_state,
        execution_relevance = execution_relevance
    )

    rationale = build_rationale(
        decision_state,
        basis_codes,
        context,
        safety_result = null,
        epistemic_result = epistemic_result
    )

    trace = emit_trace(
        normalized = normalized,
        context = context,
        decision_state = decision_state,
        basis_codes = basis_codes,
        qualification_type = qualification_type,
        execution_relevance = execution_relevance,
        enforcement_action = enforcement_action,
        rationale = rationale,
        policy = policy
    )

    return build_decision_result(
        decision_state,
        basis_codes,
        qualification_type,
        rationale,
        enforcement_action,
        trace.trace_id
    )
```

---

## 3. Payload Normalization

```text
function normalize_payload(evaluation_payload):

    assert evaluation_payload.input_ref exists
    assert evaluation_payload.output_ref exists
    assert evaluation_payload.candidate_output exists

    normalized = new object

    normalized.input_ref = evaluation_payload.input_ref
    normalized.output_ref = evaluation_payload.output_ref
    normalized.content = evaluation_payload.candidate_output.content
    normalized.content_type = evaluation_payload.candidate_output.content_type

    normalized.context = evaluation_payload.context
    normalized.provenance = evaluation_payload.provenance
    normalized.policy = evaluation_payload.policy

    return normalized
```

---

## 4. Context Resolution

```text
function resolve_context(normalized):

    context = new object

    context.zone = normalized.context.zone
    context.profile = normalized.context.profile
    context.deployment_mode = normalized.context.deployment_mode
    context.user_visible = normalized.context.user_visible
    context.downstream_target = normalized.context.downstream_target

    if context.zone not in ["critical", "analytical", "creative"]:
        context.zone = "analytical"

    if context.profile not in ["KPT-H", "KPT-A"]:
        context.profile = "KPT-A"

    if context.deployment_mode not in ["General", "High-Assurance"]:
        context.deployment_mode = "General"

    return context
```

---

## 5. Execution Relevance

```text
function determine_execution_relevance(normalized, context):

    if normalized.context.execution_relevant == true:
        return true

    if normalized.content_type == "tool_call":
        return true

    if context.downstream_target in ["tool", "api", "file", "mixed"]:
        return true

    return false
```

---

## 6. Safety Evaluation

```text
function evaluate_safety(normalized, context, policy):

    result = new object
    result.has_disallowed_help = false
    result.has_weaponized_form = false
    result.codes = []

    if matches_disallowed_help(normalized.content, context, policy):
        result.has_disallowed_help = true
        result.codes.append("SAFE-DISALLOWED-HELP")

    if matches_weaponized_form(normalized.content, context, policy):
        result.has_weaponized_form = true
        result.codes.append("WF-WEAPONIZED-FORM")

    return result
```

---

## 7. Epistemic Evaluation

```text
function evaluate_epistemic(normalized, context, policy):

    result = new object
    result.status = "sufficient"
    result.codes = []

    verification_state = normalized.provenance.verification_state
    time_sensitivity = normalized.provenance.time_sensitivity

    if verification_state == "unverified":
        result.status = "uncertain"
        result.codes.append("SRC-UNVERIFIED")

    if verification_state == "partially_verified":
        if result.status != "insufficient":
            result.status = "uncertain"

    if time_sensitivity == "high":
        if result.status == "sufficient":
            result.status = "uncertain"
        result.codes.append("TMP-TIME-SENSITIVE")

    if exceeds_scope(normalized.content, context, policy):
        if result.status == "sufficient":
            result.status = "uncertain"
        result.codes.append("SCP-SCOPE-LIMITED")

    if requires_verification_before_assertion(normalized.content, context, policy):
        if result.status == "sufficient":
            result.status = "uncertain"
        result.codes.append("VER-REQUIRED")

    if context.zone == "critical" and verification_state == "unverified":
        result.status = "insufficient"

    if lacks_minimum_support(normalized.content, context, policy):
        result.status = "insufficient"
        result.codes.append("EPI-INSUFFICIENT")

    if result.status == "sufficient":
        result.codes = ["EPI-SUFFICIENT"]

    return result
```

---

## 8. Basis Code Builders

```text
function build_safety_basis_codes(safety_result):

    codes = []

    for code in safety_result.codes:
        codes.append(code)

    return unique(codes)
```

```text
function build_refuse_assert_basis_codes(epistemic_result):

    codes = ["EPI-INSUFFICIENT"]

    for code in epistemic_result.codes:
        if code != "EPI-SUFFICIENT":
            codes.append(code)

    return unique(codes)
```

```text
function build_qualify_basis_codes(epistemic_result):

    codes = ["EPI-UNCERTAIN"]

    for code in epistemic_result.codes:
        if code != "EPI-SUFFICIENT":
            codes.append(code)

    return unique(codes)
```

---

## 9. Qualification Type Derivation

```text
function derive_qualification_type(basis_codes):

    supporting_families = []

    if contains(basis_codes, "TMP-TIME-SENSITIVE"):
        supporting_families.append("time_sensitive")

    if contains_any(basis_codes, ["SRC-UNVERIFIED", "SRC-NO-PRIMARY"]):
        supporting_families.append("source_limited")

    if contains(basis_codes, "SCP-SCOPE-LIMITED"):
        supporting_families.append("scope_limited")

    if contains(basis_codes, "VER-REQUIRED"):
        supporting_families.append("verification_required")

    if length(supporting_families) == 0:
        return "uncertainty"

    if length(supporting_families) == 1:
        return supporting_families[0]

    return "mixed"
```

---

## 10. Enforcement Mapping

```text
function map_enforcement(decision_state, execution_relevance):

    action = new object

    if decision_state == "deliver":
        action.display = "allow"
        action.execution = execution_relevance ? "allow" : "not_applicable"
        return action

    if decision_state == "qualify":
        action.display = "allow_with_qualification"
        action.execution = execution_relevance ? "block" : "not_applicable"
        return action

    if decision_state == "refuse_assert":
        action.display = "block_original"
        action.execution = execution_relevance ? "block" : "not_applicable"
        return action

    if decision_state == "refuse_help":
        action.display = "block_original"
        action.execution = execution_relevance ? "block" : "not_applicable"
        return action

    action.display = "block_original"
    action.execution = execution_relevance ? "block" : "not_applicable"
    return action
```

---

## 11. Rationale Builder

```text
function build_rationale(decision_state, basis_codes, context, safety_result, epistemic_result):

    if decision_state == "refuse_help":
        return "Candidate output constituted disallowed assistance or weaponized form and was blocked."

    if decision_state == "refuse_assert":
        return "Candidate output lacked sufficient support for assertion in the governed context."

    if decision_state == "qualify":
        return "Candidate output was admissible only with explicit uncertainty or limitation."

    if decision_state == "deliver":
        return "Candidate output met sufficiency requirements for the governed context."

    return "Decision assigned under fallback evaluator path."
```

Constraint:
- rationale must be concise;
- rationale must support auditability;
- rationale must not contain chain-of-thought.

---

## 12. Trace Emission

```text
function emit_trace(
    normalized,
    context,
    decision_state,
    basis_codes,
    qualification_type,
    execution_relevance,
    enforcement_action,
    rationale,
    policy
):

    trace = new object

    trace.trace_id = generate_trace_id()
    trace.timestamp = current_timestamp_iso8601()
    trace.input_ref = normalized.input_ref
    trace.output_ref = normalized.output_ref
    trace.zone = context.zone
    trace.profile = context.profile
    trace.deployment_mode = context.deployment_mode
    trace.decision_state = decision_state
    trace.basis_codes = basis_codes
    trace.qualification_type = qualification_type
    trace.execution_relevance = execution_relevance
    trace.enforcement_action = enforcement_action
    trace.rationale = rationale
    trace.policy_version = policy.version
    trace.engine_version = policy.engine_version
    trace.previous_trace_hash = get_previous_trace_hash()
    trace.integrity_hash = compute_integrity_hash(trace)

    write_trace_append_only(trace)

    return trace
```

Required rule:
- for execution-relevant outputs, `write_trace_append_only(trace)` must complete before any downstream execution begins.

---

## 13. Safe Replacement Loop

```text
function evaluate_with_optional_replacement(evaluation_payload):

    first_result = evaluate_candidate(evaluation_payload)

    if first_result.decision_state in ["deliver", "qualify"]:
        return first_result

    if first_result.decision_state in ["refuse_assert", "refuse_help"]:
        replacement_candidate = generate_safe_replacement(evaluation_payload, first_result)

        if replacement_candidate is null:
            return first_result

        replacement_payload = clone_as_new_candidate(
            original_payload = evaluation_payload,
            replacement_candidate = replacement_candidate
        )

        second_result = evaluate_candidate(replacement_payload)

        return {
            original_result: first_result,
            replacement_result: second_result
        }
```

Required rule:
- original blocked candidate gets its own trace;
- replacement candidate gets a second trace.

---

## 14. Execution Gate

```text
function execution_gate(decision_result, proposed_action):

    if decision_result.enforcement_action.execution == "allow":
        return execute(proposed_action)

    if decision_result.enforcement_action.execution == "block":
        return blocked_execution_response(decision_result.trace_id)

    return no_execution_required(decision_result.trace_id)
```

Critical rule:
- no tool, API, file, or workflow commit may occur unless enforcement explicitly permits execution after trace emission.

---

## 15. Reference Failure Conditions

The evaluator should be treated as non-conformant if any of the following occur:

- execution happens before trace write;
- `qualify` is assigned without `EPI-UNCERTAIN`;
- safety codes are present but decision is not `refuse_help`;
- execution-relevant `qualify` is allowed to execute;
- blocked candidate and replacement output share a single trace;
- decision state is inferred from enforcement after the fact rather than assigned before action.

---

## 16. Minimal End-to-End Flow Summary

```text
candidate output
  -> normalize
  -> resolve context
  -> determine execution relevance
  -> evaluate safety
  -> if safety hit: refuse_help
  -> else evaluate epistemics
  -> assign deliver / qualify / refuse_assert
  -> derive qualification_type
  -> map enforcement
  -> emit trace
  -> allow display and/or execution only per enforcement
  -> if blocked and replacement generated: start second evaluation cycle
```

---

## 17. Recommended Repository Placement

```text
docs/reference-middleware-pseudocode.md
```

---

## 18. Next Technical Artifact

The next recommended artifact after this pseudocode is one of:

- a JSON schema for the evaluation payload and decision result;
- a trace JSON schema aligned to KPT 2.3 trace requirements;
- a final technical diagram showing evaluator, enforcement boundary, trace store, and execution gate.
