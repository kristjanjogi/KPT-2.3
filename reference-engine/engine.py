"""
KPT Reference Engine v0.1
engine.py

Reference decision engine skeleton for KPT 2.3.

Purpose:
- evaluate canonical demo cases deterministically
- assign KPT decision_state
- derive basis_codes and qualification_type
- return stable decision results for enforcement and trace layers

Non-goals:
- live model calls
- retrieval
- production security
- autonomous execution
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class Context:
    zone: str
    profile: str
    deployment_mode: str
    execution_relevant: bool
    route_type: str
    user_visible: bool = True
    downstream_target: str = "display"


@dataclass
class SafetyResult:
    hit: bool
    basis_codes: List[str] = field(default_factory=list)
    rationale: str = ""
    reason: Optional[str] = None


@dataclass
class EpistemicResult:
    status: str  # EPI-SUFFICIENT | EPI-UNCERTAIN | EPI-INSUFFICIENT
    basis_codes: List[str] = field(default_factory=list)
    rationale: str = ""
    limitation_codes: List[str] = field(default_factory=list)


@dataclass
class DecisionResult:
    case_id: str
    candidate_id: str
    decision_state: str
    basis_codes: List[str]
    qualification_type: Optional[str]
    rationale: str
    enforcement_action: Dict[str, Any]
    context: Dict[str, Any]
    trace_count_expected: int = 1
    replacement_required: bool = False
    is_replacement: bool = False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def evaluate_candidate(case_payload: Dict[str, Any]) -> DecisionResult:
    """
    Evaluate one candidate payload and return a decision result.

    Ordered flow:
    1. normalize input
    2. resolve context
    3. evaluate safety
    4. if safety hit -> refuse_help
    5. else evaluate epistemic status
    6. resolve decision
    7. derive qualification type
    8. build decision result
    """
    normalized = normalize_candidate(case_payload)
    context = resolve_context(normalized)

    safety_result = evaluate_safety(normalized, context)
    if safety_result.hit:
        decision_state = "refuse_help"
        qualification_type = None
        basis_codes = safety_result.basis_codes.copy()
        rationale = safety_result.rationale or "Blocked due to safety precedence."
        return build_decision_result(
            normalized=normalized,
            context=context,
            decision_state=decision_state,
            basis_codes=basis_codes,
            qualification_type=qualification_type,
            rationale=rationale,
        )

    epistemic_result = evaluate_epistemic(normalized, context)
    decision_state = resolve_decision(epistemic_result)
    qualification_type = derive_qualification_type(epistemic_result, decision_state)

    basis_codes = list(dict.fromkeys(epistemic_result.basis_codes + epistemic_result.limitation_codes))
    rationale = epistemic_result.rationale or "Decision derived from epistemic evaluation."

    return build_decision_result(
        normalized=normalized,
        context=context,
        decision_state=decision_state,
        basis_codes=basis_codes,
        qualification_type=qualification_type,
        rationale=rationale,
    )


def evaluate_with_optional_replacement(case_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate primary candidate and, if required, evaluate replacement candidate separately.

    Returns:
    {
        "original_result": DecisionResult,
        "replacement_result": Optional[DecisionResult],
        "trace_count": int,
    }
    """
    primary = evaluate_candidate(case_payload)
    replacement_result: Optional[DecisionResult] = None

    if replacement_required(primary, case_payload):
        replacement_payload = build_replacement_payload(case_payload)
        replacement_result = evaluate_candidate(replacement_payload)
        replacement_result.is_replacement = True

    trace_count = 1 + (1 if replacement_result is not None else 0)

    return {
        "original_result": primary,
        "replacement_result": replacement_result,
        "trace_count": trace_count,
    }


# ---------------------------------------------------------------------------
# Normalization and context
# ---------------------------------------------------------------------------


def normalize_candidate(case_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize demo case payload into a governed candidate shape.

    v0.1 is intentionally light-touch and fixture-driven.
    """
    required_top_level = [
        "case_id",
        "context",
        "candidate_output",
    ]
    for field_name in required_top_level:
        if field_name not in case_payload:
            raise ValueError(f"Missing required field: {field_name}")

    candidate_output = case_payload["candidate_output"]
    if "candidate_id" not in candidate_output:
        raise ValueError("Missing required candidate_output.candidate_id")

    return case_payload


def resolve_context(normalized: Dict[str, Any]) -> Context:
    """
    Read context exactly as supplied by the demo case.

    v0.1 does not attempt dynamic inference except where future cases
    explicitly test derivation behavior.
    """
    raw = normalized["context"]

    return Context(
        zone=raw["zone"],
        profile=raw["profile"],
        deployment_mode=raw["deployment_mode"],
        execution_relevant=raw["execution_relevant"],
        route_type=normalized.get("route_type", raw.get("route_type", "human")),
        user_visible=raw.get("user_visible", True),
        downstream_target=raw.get("downstream_target", "display"),
    )


# ---------------------------------------------------------------------------
# Safety evaluation
# ---------------------------------------------------------------------------


def evaluate_safety(normalized: Dict[str, Any], context: Context) -> SafetyResult:
    """
    Apply safety precedence.

    v0.1 uses fixture-driving heuristics and explicit content checks.
    This is not a production safety classifier.
    """
    candidate_output = normalized["candidate_output"]
    content = candidate_output.get("content", "")
    content_text = stringify_content(content).lower()

    # Extremely narrow v0.1 safety fixtures / heuristics
    if any(term in content_text for term in ["improvised explosive device", "build a bomb", "explosive device"]):
        return SafetyResult(
            hit=True,
            basis_codes=["SAFE-DISALLOWED-HELP"],
            rationale="Candidate requests or provides clearly disallowed harmful assistance.",
            reason="disallowed_help",
        )

    if any(term in content_text for term in ["mobilize with weapons", "ethnic minority neighborhood"]):
        return SafetyResult(
            hit=True,
            basis_codes=["SAFE-DISALLOWED-HELP"],
            rationale="Candidate contains targeted violent mobilization content.",
            reason="violent_targeting",
        )

    # Optional weaponized-form demo hook
    if normalized.get("provenance", {}).get("source_class") == "weaponized_form":
        return SafetyResult(
            hit=True,
            basis_codes=["WF-WEAPONIZED-FORM"],
            rationale="Candidate is treated as weaponized form under demo policy.",
            reason="weaponized_form",
        )

    return SafetyResult(hit=False)


# ---------------------------------------------------------------------------
# Epistemic evaluation
# ---------------------------------------------------------------------------


def evaluate_epistemic(normalized: Dict[str, Any], context: Context) -> EpistemicResult:
    """
    Determine epistemic status and supporting limitation codes.

    v0.1 is fixture-driven first, heuristic second.
    """
    provenance = normalized.get("provenance", {})
    source_class = provenance.get("source_class")
    primary_source_present = provenance.get("primary_source_present", False)
    verification_required = provenance.get("verification_required", False)
    conflicting_sources = provenance.get("conflicting_sources", False)
    time_sensitive = provenance.get("time_sensitive", False)
    scope_limited = provenance.get("scope_limited", False)
    combine_limitations = provenance.get("combine_limitations", False)

    def build_limitation_codes(*, include_source_gap: bool = False, include_verification: bool = False) -> List[str]:
        limitation_codes: List[str] = []
        if include_source_gap and not primary_source_present:
            limitation_codes.append("SRC-NO-PRIMARY")
        if include_verification and verification_required:
            limitation_codes.append("VER-REQUIRED")
        if conflicting_sources:
            limitation_codes.append("SRC-CONFLICT")
        if time_sensitive:
            limitation_codes.append("TMP-TIME-SENSITIVE")
        if scope_limited:
            limitation_codes.append("SCP-SCOPE-LIMITED")
        return list(dict.fromkeys(limitation_codes))

    # Fixture-driven priority
    if source_class in {"trusted_system_context", "safe_replacement_fixture", "provided_material_only"}:
        return EpistemicResult(
            status="EPI-SUFFICIENT",
            basis_codes=["EPI-SUFFICIENT"],
            rationale="Trusted system context is sufficient for this demo case.",
        )

    if source_class == "unsupported_assertion":
        return EpistemicResult(
            status="EPI-INSUFFICIENT",
            basis_codes=["EPI-INSUFFICIENT"],
            rationale="Assertion lacks sufficient support in the provided context.",
        )

    if source_class == "partial_sources":
        limitation_codes = build_limitation_codes(
            include_source_gap=True,
            include_verification=combine_limitations,
        )
        return EpistemicResult(
            status="EPI-UNCERTAIN",
            basis_codes=["EPI-UNCERTAIN"],
            limitation_codes=limitation_codes,
            rationale="The source set is incomplete for a fully supported assertion.",
        )

    if source_class == "ambiguous_instruction":
        limitation_codes = build_limitation_codes(
            include_source_gap=combine_limitations,
            include_verification=True,
        )
        return EpistemicResult(
            status="EPI-UNCERTAIN",
            basis_codes=["EPI-UNCERTAIN"],
            limitation_codes=limitation_codes,
            rationale="Execution-relevant instruction requires verification before admissibility.",
        )

    if source_class in {"conflicting_sources", "time_sensitive_partial"}:
        limitation_codes = build_limitation_codes(
            include_source_gap=True,
            include_verification=verification_required,
        )
        rationale_map = {
            "conflicting_sources": "The source packet contains unresolved conflict and cannot support a clean assertion.",
            "time_sensitive_partial": "The claim depends on time-sensitive context that is not sufficiently stabilized.",
        }
        return EpistemicResult(
            status="EPI-UNCERTAIN",
            basis_codes=["EPI-UNCERTAIN"],
            limitation_codes=limitation_codes,
            rationale=rationale_map.get(source_class, "The current evidence remains uncertain under demo policy."),
        )

    # Conservative fallback
    return EpistemicResult(
        status="EPI-INSUFFICIENT",
        basis_codes=["EPI-INSUFFICIENT"],
        rationale="No sufficient epistemic basis was recognized by the v0.1 evaluator.",
    )


# ---------------------------------------------------------------------------
# Decision and qualification resolution
# ---------------------------------------------------------------------------


def resolve_decision(epistemic_result: EpistemicResult) -> str:
    """
    Map epistemic result to final KPT decision state.
    """
    if epistemic_result.status == "EPI-SUFFICIENT":
        return "deliver"
    if epistemic_result.status == "EPI-UNCERTAIN":
        return "qualify"
    if epistemic_result.status == "EPI-INSUFFICIENT":
        return "refuse_assert"

    raise ValueError(f"Unknown epistemic status: {epistemic_result.status}")


def derive_qualification_type(epistemic_result: EpistemicResult, decision_state: str) -> Optional[str]:
    """
    Derive qualification type for qualified outputs.

    v0.1 uses a simple ordered mapping.
    """
    if decision_state != "qualify":
        return None

    codes = set(epistemic_result.limitation_codes)

    if len(codes) > 1:
        return "mixed"
    if "SRC-NO-PRIMARY" in codes:
        return "source_limited"
    if "VER-REQUIRED" in codes:
        return "verification_required"
    if "TMP-TIME-SENSITIVE" in codes:
        return "time_sensitive"
    if "SCP-SCOPE-LIMITED" in codes:
        return "scope_limited"

    return "uncertainty"


# ---------------------------------------------------------------------------
# Result construction
# ---------------------------------------------------------------------------


def build_decision_result(
    normalized: Dict[str, Any],
    context: Context,
    decision_state: str,
    basis_codes: List[str],
    qualification_type: Optional[str],
    rationale: str,
) -> DecisionResult:
    """
    Build a stable decision result object for downstream enforcement and trace layers.
    """
    candidate = normalized["candidate_output"]

    enforcement_action = build_enforcement_action(
        decision_state=decision_state,
        execution_relevant=context.execution_relevant,
        route_type=context.route_type,
        safe_replacement_present=has_safe_replacement(normalized),
    )

    return DecisionResult(
        case_id=normalized["case_id"],
        candidate_id=candidate["candidate_id"],
        decision_state=decision_state,
        basis_codes=basis_codes,
        qualification_type=qualification_type,
        rationale=rationale,
        enforcement_action=enforcement_action,
        context={
            "zone": context.zone,
            "profile": context.profile,
            "deployment_mode": context.deployment_mode,
            "execution_relevant": context.execution_relevant,
            "route_type": context.route_type,
            "downstream_target": context.downstream_target,
        },
        trace_count_expected=normalized.get("expected", {}).get("trace_count", 1),
        replacement_required=enforcement_action.get("replacement_required", False),
    )


def build_enforcement_action(
    decision_state: str,
    execution_relevant: bool,
    route_type: str,
    safe_replacement_present: bool,
) -> Dict[str, Any]:
    """
    Minimal enforcement mapping for v0.1.

    This is an engine-level fallback contract.
    The dedicated enforcement module may later own this mapping.
    """
    if decision_state == "deliver":
        return {
            "display_allowed": True,
            "display_mode": "full",
            "execution_allowed": bool(execution_relevant and route_type == "action"),
            "execution_mode": "allow" if (execution_relevant and route_type == "action") else "not_applicable",
            "replacement_required": False,
        }

    if decision_state == "qualify":
        return {
            "display_allowed": True,
            "display_mode": "qualified",
            "execution_allowed": False,
            "execution_mode": "block" if execution_relevant and route_type == "action" else "not_applicable",
            "replacement_required": False,
        }

    if decision_state in {"refuse_assert", "refuse_help"}:
        replacement_required_flag = safe_replacement_present and route_type == "human"
        return {
            "display_allowed": False,
            "display_mode": "replacement_only" if replacement_required_flag else "none",
            "execution_allowed": False,
            "execution_mode": "block" if route_type == "action" or execution_relevant else "not_applicable",
            "replacement_required": replacement_required_flag,
        }

    raise ValueError(f"Unknown decision_state: {decision_state}")


# ---------------------------------------------------------------------------
# Replacement handling
# ---------------------------------------------------------------------------


def replacement_required(primary_result: DecisionResult, case_payload: Dict[str, Any]) -> bool:
    """
    Determine whether a safe replacement path should be evaluated.
    """
    policy = case_payload.get("policy", {})
    allow_safe_replacement = policy.get("allow_safe_replacement", False)
    has_replacement = "safe_replacement" in policy

    return bool(
        primary_result.replacement_required
        and allow_safe_replacement
        and has_replacement
    )


def build_replacement_payload(case_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build a new payload for replacement evaluation.

    Replacement is treated as a new candidate, not a mutation of the original.
    """
    policy = case_payload.get("policy", {})
    replacement = policy.get("safe_replacement")
    if not replacement:
        raise ValueError("Replacement payload requested but no safe_replacement is defined.")

    replacement_payload = {
        **case_payload,
        "candidate_output": replacement,
        "provenance": {
            "source_class": "safe_replacement_fixture",
            "primary_source_present": True,
            "verification_required": False,
        },
        "policy": {
            "allow_safe_replacement": False,
        },
    }
    return replacement_payload


def has_safe_replacement(normalized: Dict[str, Any]) -> bool:
    """
    Check whether this case includes a safe replacement fixture.
    """
    return "safe_replacement" in normalized.get("policy", {})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def stringify_content(content: Any) -> str:
    """
    Convert candidate content into a lightweight comparable text form.
    """
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        return " ".join(f"{k}={v}" for k, v in content.items())
    return str(content)
