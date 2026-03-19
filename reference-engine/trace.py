"""
KPT Reference Engine v0.1
trace.py

Reference trace layer for KPT 2.3.

Purpose:
- build canonical trace objects for every evaluated candidate
- write append-only trace records for demo runs
- compute per-trace integrity hashes
- support optional previous-trace linkage

Non-goals:
- production tamper-proof storage
- distributed trace infrastructure
- cryptographic signing infrastructure
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Canonical core-contract helpers
# ---------------------------------------------------------------------------


def normalize_basis_codes(basis_codes: List[str]) -> List[str]:
    """Return unique lexicographically sorted basis codes."""
    return sorted(dict.fromkeys(basis_codes or []))


def build_core_enforcement_action(decision_result: Any) -> Dict[str, str]:
    """
    Convert richer demo/runtime enforcement state into the canonical core contract.

    Core contract:
    - display: allow | allow_with_qualification | block_original
    - execution: allow | block | not_applicable
    """
    decision = _normalize_decision_result(decision_result)
    decision_state = decision["decision_state"]

    display_map = {
        "deliver": "allow",
        "qualify": "allow_with_qualification",
        "refuse_assert": "block_original",
        "refuse_help": "block_original",
    }

    internal = decision.get("enforcement_action", {}) or {}
    execution = internal.get("execution_mode")
    if execution not in {"allow", "block", "not_applicable"}:
        context = decision.get("context", {}) or {}
        route_type = context.get("route_type")
        execution_relevant = bool(context.get("execution_relevant", False))
        if decision_state == "deliver":
            execution = "allow" if (route_type == "action" and execution_relevant) else "not_applicable"
        elif decision_state == "qualify":
            execution = "block" if (route_type == "action" and execution_relevant) else "not_applicable"
        else:
            execution = "block" if (route_type == "action" or execution_relevant) else "not_applicable"

    return {
        "display": display_map[decision_state],
        "execution": execution,
    }


def build_core_decision_payload(decision_result: Any, trace_id: str) -> Dict[str, Any]:
    """
    Build the normalized decision object that must conform to
    schemas/decision-result.schema.json.
    """
    decision = _normalize_decision_result(decision_result)
    return {
        "decision_state": decision["decision_state"],
        "basis_codes": normalize_basis_codes(decision.get("basis_codes", [])),
        "qualification_type": decision.get("qualification_type"),
        "rationale": decision["rationale"],
        "enforcement_action": build_core_enforcement_action(decision),
        "trace_id": trace_id,
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_trace_object(
    *,
    decision_result: Any,
    input_ref: str,
    output_ref: str,
    policy_version: str,
    engine_version: str,
    previous_trace_hash: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Build a canonical trace object from the decision result.

    Notes:
    - decision_result may be a dataclass or a plain dict
    - previous_trace_hash MAY be null for a genesis record
    - integrity_hash is computed after trace content is assembled
    """
    decision = _normalize_decision_result(decision_result)
    context = decision["context"]
    timestamp = _utc_now_iso()
    trace_id = _build_trace_id(
        case_id=decision.get("case_id", "unknown_case"),
        candidate_id=decision.get("candidate_id", "unknown_candidate"),
        timestamp=timestamp,
    )

    trace_obj: Dict[str, Any] = {
        "trace_id": trace_id,
        "timestamp": timestamp,
        "input_ref": input_ref,
        "output_ref": output_ref,
        "zone": context["zone"],
        "profile": context["profile"],
        "deployment_mode": context["deployment_mode"],
        "decision_state": decision["decision_state"],
        "basis_codes": normalize_basis_codes(decision.get("basis_codes", [])),
        "rationale": decision["rationale"],
        "qualification_type": decision.get("qualification_type"),
        "execution_relevance": bool(context["execution_relevant"]),
        "enforcement_action": build_core_enforcement_action(decision),
        "policy_version": policy_version,
        "engine_version": engine_version,
        "previous_trace_hash": previous_trace_hash,
        "integrity_hash": None,
    }

    trace_obj["integrity_hash"] = compute_trace_integrity_hash(trace_obj)
    return trace_obj


def write_trace(
    trace_obj: Dict[str, Any],
    traces_dir: str | Path,
) -> Path:
    """
    Append-only trace write for v0.1 demo output.

    Files are written in stable JSON form using sorted keys and compact separators
    so the on-disk payload matches the canonical contract closely.
    """
    traces_path = Path(traces_dir)
    traces_path.mkdir(parents=True, exist_ok=True)

    filename = f"{_safe_timestamp_for_filename(trace_obj['timestamp'])}__{trace_obj['trace_id']}.json"
    file_path = traces_path / filename

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(trace_obj, f, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    return file_path


def load_last_trace_hash(traces_dir: str | Path) -> Optional[str]:
    """
    Return the integrity_hash of the most recently written trace file.

    v0.1 uses this as a lightweight optional previous-trace linkage mechanism.
    """
    traces_path = Path(traces_dir)
    if not traces_path.exists():
        return None

    trace_files = sorted(traces_path.glob("*.json"))
    if not trace_files:
        return None

    latest = trace_files[-1]
    with latest.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    return payload.get("integrity_hash")


def build_and_write_trace(
    *,
    decision_result: Any,
    input_ref: str,
    output_ref: str,
    policy_version: str,
    engine_version: str,
    traces_dir: str | Path,
    previous_trace_hash: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convenience wrapper:
    - load optional previous trace hash
    - build canonical trace object
    - write trace
    - return trace object and file path metadata
    """
    previous_hash = previous_trace_hash if previous_trace_hash is not None else load_last_trace_hash(traces_dir)

    trace_obj = build_trace_object(
        decision_result=decision_result,
        input_ref=input_ref,
        output_ref=output_ref,
        policy_version=policy_version,
        engine_version=engine_version,
        previous_trace_hash=previous_hash,
    )

    file_path = write_trace(trace_obj, traces_dir)

    return {
        "trace": trace_obj,
        "file_path": str(file_path),
    }


# ---------------------------------------------------------------------------
# Integrity and hashing
# ---------------------------------------------------------------------------


def compute_trace_integrity_hash(trace_obj: Dict[str, Any]) -> str:
    """
    Compute deterministic integrity hash for a trace object.

    Rule:
    - exclude integrity_hash itself from the hash input
    - serialize deterministically
    """
    hash_input = {k: v for k, v in trace_obj.items() if k != "integrity_hash"}
    canonical = json.dumps(hash_input, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _normalize_decision_result(decision_result: Any) -> Dict[str, Any]:
    """Accept dataclass or dict-like decision result and return a plain dict."""
    if is_dataclass(decision_result):
        return asdict(decision_result)

    if isinstance(decision_result, dict):
        return decision_result

    raise TypeError("decision_result must be a dataclass instance or dict")


def _utc_now_iso() -> str:
    """Return UTC timestamp in ISO-8601 form with Z suffix."""
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _build_trace_id(case_id: str, candidate_id: str, timestamp: str) -> str:
    """
    Build a deterministic-ish human-readable trace id for demo use.

    v0.1 does not require UUID infrastructure.
    """
    raw = f"{case_id}|{candidate_id}|{timestamp}"
    short = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]
    return f"trace_{short}"


def _safe_timestamp_for_filename(timestamp: str) -> str:
    """Convert ISO timestamp to filesystem-friendly form."""
    return timestamp.replace(":", "-").replace(".", "_").replace("Z", "Z")
