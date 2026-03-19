"""
KPT Reference Engine v0.1
enforcement.py

Reference enforcement layer skeleton for KPT 2.3.

Purpose:
- convert decision results into runtime treatment
- separate decision_state from enforcement behavior
- support human-facing and action-facing route handling
- expose a stable machine-readable enforcement outcome for demo verification

Non-goals:
- live tool execution
- production orchestration
- UI rendering
- distributed policy enforcement
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Optional


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def map_enforcement(
    decision_result: Any,
) -> Dict[str, Any]:
    """
    Convert a decision result into a stable enforcement contract.

    Expected input:
    - dataclass-like or dict-like decision result
    - must contain decision_state, context, and optional replacement_required

    Returns a machine-readable enforcement object.
    """
    decision = _normalize_decision_result(decision_result)

    decision_state = decision["decision_state"]
    context = decision["context"]

    route_type = context["route_type"]
    execution_relevant = context["execution_relevant"]
    replacement_required = decision.get("replacement_required", False)

    if decision_state == "deliver":
        return _map_deliver(
            route_type=route_type,
            execution_relevant=execution_relevant,
        )

    if decision_state == "qualify":
        return _map_qualify(
            route_type=route_type,
            execution_relevant=execution_relevant,
            qualification_type=decision.get("qualification_type"),
        )

    if decision_state == "refuse_assert":
        return _map_refusal(
            decision_state=decision_state,
            route_type=route_type,
            execution_relevant=execution_relevant,
            replacement_required=replacement_required,
        )

    if decision_state == "refuse_help":
        return _map_refusal(
            decision_state=decision_state,
            route_type=route_type,
            execution_relevant=execution_relevant,
            replacement_required=replacement_required,
        )

    raise ValueError(f"Unknown decision_state: {decision_state}")


def apply_enforcement(
    decision_result: Any,
    replacement_result: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Apply enforcement for demo/runtime inspection.

    This does not perform real execution.
    It returns a machine-readable outcome that tells the demo runner:

    - whether display happened
    - whether execution happened
    - whether replacement display happened
    - what final visible outcome the reviewer should see
    """
    decision = _normalize_decision_result(decision_result)
    enforcement = map_enforcement(decision)

    replacement = _normalize_decision_result(replacement_result) if replacement_result is not None else None

    display_happened = False
    execution_happened = False
    replacement_display_happened = False
    final_visible_mode = enforcement["display_mode"]

    if enforcement["display_allowed"]:
        display_happened = True

    if enforcement["execution_allowed"]:
        execution_happened = True

    if enforcement["replacement_required"] and replacement is not None:
        replacement_enforcement = map_enforcement(replacement)
        if replacement_enforcement["display_allowed"]:
            replacement_display_happened = True
            final_visible_mode = "replacement_only"

    return {
        "decision_state": decision["decision_state"],
        "enforcement_action": enforcement,
        "display_happened": display_happened,
        "execution_happened": execution_happened,
        "replacement_display_happened": replacement_display_happened,
        "final_visible_mode": final_visible_mode,
    }


def compare_enforcement(
    actual: Dict[str, Any],
    expected: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Compare actual enforcement outcome to expected enforcement contract.

    v0.1 comparison is exact for the small contract fields.
    """
    fields = [
        "display_allowed",
        "display_mode",
        "execution_allowed",
        "execution_mode",
        "replacement_required",
    ]

    actual_contract = actual["enforcement_action"]
    mismatches = []

    for field_name in fields:
        actual_value = actual_contract.get(field_name)
        expected_value = expected.get(field_name)
        if actual_value != expected_value:
            mismatches.append(
                {
                    "field": field_name,
                    "expected": expected_value,
                    "actual": actual_value,
                }
            )

    return {
        "pass": len(mismatches) == 0,
        "mismatches": mismatches,
    }


# ---------------------------------------------------------------------------
# Mapping functions
# ---------------------------------------------------------------------------


def _map_deliver(
    *,
    route_type: str,
    execution_relevant: bool,
) -> Dict[str, Any]:
    """
    Deliver means output may proceed.

    Human route:
    - visible in full
    - no execution

    Action route:
    - visible if user-visible path exists
    - execution may proceed if execution-relevant
    """
    execution_allowed = bool(route_type == "action" and execution_relevant)

    return {
        "display_allowed": True,
        "display_mode": "full",
        "execution_allowed": execution_allowed,
        "execution_mode": "allow" if execution_allowed else "not_applicable",
        "replacement_required": False,
    }


def _map_qualify(
    *,
    route_type: str,
    execution_relevant: bool,
    qualification_type: Optional[str],
) -> Dict[str, Any]:
    """
    Qualify means output may remain visible with qualification,
    but execution is blocked when execution-relevant.
    """
    if route_type == "action" and execution_relevant:
        return {
            "display_allowed": True,
            "display_mode": "qualified",
            "execution_allowed": False,
            "execution_mode": "block",
            "replacement_required": False,
            "qualification_type": qualification_type,
        }

    return {
        "display_allowed": True,
        "display_mode": "qualified",
        "execution_allowed": False,
        "execution_mode": "not_applicable",
        "replacement_required": False,
        "qualification_type": qualification_type,
    }


def _map_refusal(
    *,
    decision_state: str,
    route_type: str,
    execution_relevant: bool,
    replacement_required: bool,
) -> Dict[str, Any]:
    """
    Refusal states block original progression.

    Human route:
    - original blocked
    - safe replacement may be shown if required

    Action route:
    - execution blocked
    - display usually none
    """
    if route_type == "human":
        return {
            "display_allowed": False,
            "display_mode": "replacement_only" if replacement_required else "none",
            "execution_allowed": False,
            "execution_mode": "not_applicable",
            "replacement_required": replacement_required,
            "refusal_type": decision_state,
        }

    return {
        "display_allowed": False,
        "display_mode": "none",
        "execution_allowed": False,
        "execution_mode": "block" if execution_relevant or route_type == "action" else "not_applicable",
        "replacement_required": False,
        "refusal_type": decision_state,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _normalize_decision_result(decision_result: Any) -> Dict[str, Any]:
    """
    Accept dataclass or dict-like decision result and return a plain dict.
    """
    if decision_result is None:
        return {}

    if is_dataclass(decision_result):
        return asdict(decision_result)

    if isinstance(decision_result, dict):
        return decision_result

    raise TypeError("decision_result must be a dataclass instance, dict, or None")
