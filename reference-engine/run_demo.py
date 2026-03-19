"""
KPT Reference Engine v0.1
run_demo.py

Reference demo runner for KPT engine integration passes.

Purpose:
- load demo cases from YAML
- execute each case through the engine
- apply enforcement for comparison/reporting
- write canonical decision and trace outputs
- validate canonical outputs against schemas
- compare actual vs expected results
- produce pass/fail reports

Non-goals:
- production orchestration
- live external execution
- UI rendering
- distributed reporting
"""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from engine import evaluate_with_optional_replacement
from enforcement import apply_enforcement, compare_enforcement
from trace import build_and_write_trace, build_core_decision_payload


REFERENCE_ENGINE_ROOT = Path(__file__).resolve().parent
PACKAGE_ROOT = REFERENCE_ENGINE_ROOT.parent.resolve()
SCHEMAS_ROOT = PACKAGE_ROOT / "schemas"
TRACE_SCHEMA_PATH = SCHEMAS_ROOT / "trace.schema.json"
DECISION_SCHEMA_PATH = SCHEMAS_ROOT / "decision-result.schema.json"

DEFAULT_OUTPUT_ROOT = REFERENCE_ENGINE_ROOT / "outputs"
DEFAULT_CASES_PATH = REFERENCE_ENGINE_ROOT / "demo_cases.yaml"
DEFAULT_TRACE_VALID_EXAMPLE = PACKAGE_ROOT / "examples" / "trace-valid-example.json"
DEFAULT_TRACE_INVALID_EXAMPLE = PACKAGE_ROOT / "examples" / "trace-invalid-example.json"

# runtime-bound output paths
OUTPUT_ROOT = DEFAULT_OUTPUT_ROOT
TRACES_DIR = OUTPUT_ROOT / "traces"
DECISIONS_DIR = OUTPUT_ROOT / "decisions"
REPORTS_DIR = OUTPUT_ROOT / "reports"


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------


def configure_output_root(output_root: Path) -> None:
    global OUTPUT_ROOT, TRACES_DIR, DECISIONS_DIR, REPORTS_DIR
    OUTPUT_ROOT = output_root
    TRACES_DIR = OUTPUT_ROOT / "traces"
    DECISIONS_DIR = OUTPUT_ROOT / "decisions"
    REPORTS_DIR = OUTPUT_ROOT / "reports"


def ensure_output_dirs(clean_output: bool = False) -> None:
    """Create output directories if they do not exist."""
    if clean_output and OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)
    for path in [TRACES_DIR, DECISIONS_DIR, REPORTS_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def load_demo_cases(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        payload = yaml.safe_load(f)

    required_top_level = ["version", "engine_version", "policy_version", "cases"]
    for field_name in required_top_level:
        if field_name not in payload:
            raise ValueError(f"Missing required top-level field in demo cases: {field_name}")

    return payload


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------


def _to_dict(obj: Any) -> Dict[str, Any]:
    if obj is None:
        return {}
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, dict):
        return obj
    raise TypeError(f"Expected dataclass or dict, got: {type(obj)!r}")


def _resolved_path(path: Path) -> Path:
    if path.is_absolute():
        return path.resolve()
    return (Path.cwd() / path).resolve()


def display_path(path: str | Path) -> str:
    resolved = _resolved_path(Path(path))
    try:
        return resolved.relative_to(PACKAGE_ROOT).as_posix()
    except ValueError:
        return resolved.as_posix()


def flatten_engine_result(engine_result: Dict[str, Any]) -> Dict[str, Any]:
    original_result = _to_dict(engine_result["original_result"])
    replacement_result = _to_dict(engine_result.get("replacement_result"))
    trace_count = int(engine_result.get("trace_count", 1))

    return {
        "original_result": original_result,
        "replacement_result": replacement_result if replacement_result else None,
        "trace_count": trace_count,
    }


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------


def load_validator(schema_path: Path) -> Draft202012Validator:
    with schema_path.open("r", encoding="utf-8") as f:
        schema = json.load(f)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_payload(validator: Draft202012Validator, payload: Dict[str, Any], label: str) -> Dict[str, Any]:
    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
    error_items = []
    for err in errors:
        error_items.append({
            "message": err.message,
            "path": list(err.path),
            "schema_path": list(err.schema_path),
        })
    return {
        "label": label,
        "valid": len(error_items) == 0,
        "error_count": len(error_items),
        "errors": error_items,
    }


def validate_json_file(path: Path, validator: Draft202012Validator) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    result = validate_payload(validator, payload, label=display_path(path))
    result["file"] = display_path(path)
    return result


def build_schema_validation_summary(validation_results: List[Dict[str, Any]], *, examples: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    invalid_outputs = [item for item in validation_results if not item["valid"]]
    examples = examples or []
    invalid_examples = [item for item in examples if not item["valid"]]
    expected_invalid_examples = [item for item in examples if item.get("expected_invalid") and not item["valid"]]
    unexpectedly_valid_examples = [item for item in examples if item.get("expected_invalid") and item["valid"]]
    unexpectedly_invalid_examples = [item for item in examples if not item.get("expected_invalid") and not item["valid"]]

    return {
        "outputs_checked": len(validation_results),
        "output_invalid_count": len(invalid_outputs),
        "output_invalid_files": [item["file"] for item in invalid_outputs if "file" in item],
        "examples_checked": len(examples),
        "example_invalid_count": len(invalid_examples),
        "expected_invalid_examples_passed": [item["file"] for item in unexpectedly_valid_examples],
        "expected_valid_examples_failed": [item["file"] for item in unexpectedly_invalid_examples if "file" in item],
        "example_results": examples,
        "output_results": validation_results,
        "pass": len(invalid_outputs) == 0 and len(unexpectedly_valid_examples) == 0 and len(unexpectedly_invalid_examples) == 0,
        "expected_invalid_examples_fail_as_expected": len(unexpectedly_valid_examples) == 0,
        "expected_valid_examples_pass": len(unexpectedly_invalid_examples) == 0,
    }


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------


def write_decision_json(case_id: str, payload: Dict[str, Any], suffix: str) -> Path:
    DECISIONS_DIR.mkdir(parents=True, exist_ok=True)
    path = DECISIONS_DIR / f"{case_id}.{suffix}.decision.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return path


def write_comparison_json(case_id: str, payload: Dict[str, Any]) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORTS_DIR / f"{case_id}.comparison.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path


def write_summary_json(payload: Dict[str, Any]) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORTS_DIR / "summary.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path


def write_schema_validation_json(payload: Dict[str, Any]) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORTS_DIR / "schema-validation.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path


# ---------------------------------------------------------------------------
# Comparison logic
# ---------------------------------------------------------------------------


def minimum_basis_codes_satisfied(actual_codes: List[str], expected_codes: List[str]) -> bool:
    return set(expected_codes).issubset(set(actual_codes))


def compare_decision(case: Dict[str, Any], actual_primary: Dict[str, Any]) -> Dict[str, Any]:
    expected = case["expected"]

    checks = {
        "decision_state_match": actual_primary.get("decision_state") == expected.get("decision_state"),
        "basis_codes_match": minimum_basis_codes_satisfied(
            actual_primary.get("basis_codes", []),
            expected.get("basis_codes", []),
        ),
        "qualification_type_match": actual_primary.get("qualification_type") == expected.get("qualification_type"),
    }

    mismatches: List[Dict[str, Any]] = []

    if not checks["decision_state_match"]:
        mismatches.append({
            "field": "decision_state",
            "expected": expected.get("decision_state"),
            "actual": actual_primary.get("decision_state"),
        })

    if not checks["basis_codes_match"]:
        mismatches.append({
            "field": "basis_codes_minimum_required",
            "expected": expected.get("basis_codes", []),
            "actual": actual_primary.get("basis_codes", []),
        })

    if not checks["qualification_type_match"]:
        mismatches.append({
            "field": "qualification_type",
            "expected": expected.get("qualification_type"),
            "actual": actual_primary.get("qualification_type"),
        })

    return {
        "pass": all(checks.values()),
        "checks": checks,
        "mismatches": mismatches,
    }


def compare_trace_count(case: Dict[str, Any], actual_trace_count: int) -> Dict[str, Any]:
    expected = int(case["expected"]["trace_count"])
    passed = actual_trace_count == expected

    mismatches: List[Dict[str, Any]] = []
    if not passed:
        mismatches.append({
            "field": "trace_count",
            "expected": expected,
            "actual": actual_trace_count,
        })

    return {
        "pass": passed,
        "checks": {"trace_count_match": passed},
        "mismatches": mismatches,
    }


def compare_replacement_status(case: Dict[str, Any], actual_replacement_result: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    expected_required = bool(case["expected"]["enforcement"]["replacement_required"])
    actual_present = actual_replacement_result is not None
    passed = expected_required == actual_present

    mismatches: List[Dict[str, Any]] = []
    if not passed:
        mismatches.append({
            "field": "replacement_path_status",
            "expected": expected_required,
            "actual": actual_present,
        })

    return {
        "pass": passed,
        "checks": {"replacement_status_match": passed},
        "mismatches": mismatches,
    }


# ---------------------------------------------------------------------------
# Case execution
# ---------------------------------------------------------------------------


def process_case(
    case: Dict[str, Any],
    *,
    engine_version: str,
    policy_version: str,
    trace_validator: Draft202012Validator,
    decision_validator: Draft202012Validator,
) -> Dict[str, Any]:
    engine_result = evaluate_with_optional_replacement(case)
    flattened = flatten_engine_result(engine_result)

    original_result = flattened["original_result"]
    replacement_result = flattened["replacement_result"]
    trace_count = flattened["trace_count"]

    enforcement_outcome = apply_enforcement(original_result, replacement_result)

    original_trace_written = build_and_write_trace(
        decision_result=original_result,
        input_ref=case["input_ref"],
        output_ref=case["output_ref"],
        policy_version=policy_version,
        engine_version=engine_version,
        traces_dir=TRACES_DIR,
    )
    original_decision_payload = build_core_decision_payload(
        original_result,
        trace_id=original_trace_written["trace"]["trace_id"],
    )
    original_decision_path = write_decision_json(case["case_id"], original_decision_payload, "original")

    validation_results = [
        validate_json_file(Path(original_trace_written["file_path"]), trace_validator),
        validate_json_file(original_decision_path, decision_validator),
    ]

    replacement_trace_written = None
    replacement_decision_path = None
    if replacement_result is not None:
        replacement_trace_written = build_and_write_trace(
            decision_result=replacement_result,
            input_ref=case["input_ref"],
            output_ref=f"{case['output_ref']}__replacement",
            policy_version=policy_version,
            engine_version=engine_version,
            traces_dir=TRACES_DIR,
            previous_trace_hash=original_trace_written["trace"]["integrity_hash"],
        )
        replacement_decision_payload = build_core_decision_payload(
            replacement_result,
            trace_id=replacement_trace_written["trace"]["trace_id"],
        )
        replacement_decision_path = write_decision_json(case["case_id"], replacement_decision_payload, "replacement")
        validation_results.extend([
            validate_json_file(Path(replacement_trace_written["file_path"]), trace_validator),
            validate_json_file(replacement_decision_path, decision_validator),
        ])

    decision_compare = compare_decision(case, original_result)
    enforcement_compare = compare_enforcement(
        actual=enforcement_outcome,
        expected=case["expected"]["enforcement"],
    )
    trace_count_compare = compare_trace_count(case, trace_count)
    replacement_compare = compare_replacement_status(case, replacement_result)

    output_validation_failed = any(not item["valid"] for item in validation_results)
    mismatch_count = (
        len(decision_compare["mismatches"])
        + len(enforcement_compare["mismatches"])
        + len(trace_count_compare["mismatches"])
        + len(replacement_compare["mismatches"])
        + sum(item["error_count"] for item in validation_results)
    )

    case_report = {
        "case_id": case["case_id"],
        "title": case.get("title"),
        "route_type": case["route_type"],
        "passed": all([
            decision_compare["pass"],
            enforcement_compare["pass"],
            trace_count_compare["pass"],
            replacement_compare["pass"],
            not output_validation_failed,
        ]),
        "mismatch_count": mismatch_count,
        "expected": case["expected"],
        "actual": {
            "decision": {
                "decision_state": original_result.get("decision_state"),
                "basis_codes": original_result.get("basis_codes", []),
                "qualification_type": original_result.get("qualification_type"),
            },
            "enforcement": enforcement_outcome["enforcement_action"],
            "trace_count": trace_count,
            "replacement_path_status": replacement_result is not None,
        },
        "comparison": {
            "decision": decision_compare,
            "enforcement": enforcement_compare,
            "trace_count": trace_count_compare,
            "replacement": replacement_compare,
        },
        "schema_validation": {
            "pass": not output_validation_failed,
            "results": validation_results,
        },
        "artifacts": {
            "original_trace_file": display_path(original_trace_written["file_path"]),
            "original_decision_file": display_path(original_decision_path),
            "replacement_trace_file": display_path(replacement_trace_written["file_path"]) if replacement_trace_written else None,
            "replacement_decision_file": display_path(replacement_decision_path) if replacement_decision_path else None,
        },
    }

    write_comparison_json(case["case_id"], case_report)
    return case_report


# ---------------------------------------------------------------------------
# Summary reporting
# ---------------------------------------------------------------------------


def build_summary_report(
    case_reports: List[Dict[str, Any]],
    *,
    suite_name: str,
    cases_path: Path,
    engine_version: str,
    policy_version: str,
    schema_validation_summary: Dict[str, Any],
) -> Dict[str, Any]:
    total_cases = len(case_reports)
    passed_cases = sum(1 for report in case_reports if report["passed"])
    failed_cases = total_cases - passed_cases
    total_mismatches = sum(report["mismatch_count"] for report in case_reports)

    return {
        "suite_name": suite_name,
        "cases_path": display_path(cases_path),
        "engine_version": engine_version,
        "policy_version": policy_version,
        "output_root": display_path(OUTPUT_ROOT),
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": failed_cases,
        "total_mismatches": total_mismatches,
        "failed_case_ids": [report["case_id"] for report in case_reports if not report["passed"]],
        "schema_validation": schema_validation_summary,
        "case_reports": case_reports,
    }


def print_console_summary(summary: Dict[str, Any]) -> None:
    print("KPT Reference Engine v0.1")
    print(f"Suite:            {summary['suite_name']}")
    print(f"Cases file:       {summary['cases_path']}")
    print()
    print(f"Total cases:      {summary['total_cases']}")
    print(f"Passed cases:     {summary['passed_cases']}")
    print(f"Failed cases:     {summary['failed_cases']}")
    print(f"Total mismatches: {summary['total_mismatches']}")
    print(f"Schema invalid:   {summary['schema_validation']['output_invalid_count']}")

    if summary["failed_case_ids"]:
        print()
        print("Failed cases:")
        for case_id in summary["failed_case_ids"]:
            print(f" - {case_id}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run KPT reference-engine demo cases.")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES_PATH, help="Path to YAML case file.")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT, help="Directory for traces, decisions, reports.")
    parser.add_argument("--suite-name", type=str, default=None, help="Optional suite name override for summary output.")
    parser.add_argument("--clean-output", action="store_true", help="Remove the output root before writing new artifacts.")
    parser.add_argument("--validate-examples", action="store_true", help="Also validate example JSON artifacts against the canonical schemas.")
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    args = parse_args()
    configure_output_root(args.output_root)
    ensure_output_dirs(clean_output=args.clean_output)

    demo = load_demo_cases(args.cases)
    engine_version = demo["engine_version"]
    policy_version = demo["policy_version"]
    suite_name = args.suite_name or demo.get("version") or args.cases.stem

    trace_validator = load_validator(TRACE_SCHEMA_PATH)
    decision_validator = load_validator(DECISION_SCHEMA_PATH)

    case_reports: List[Dict[str, Any]] = []
    for case in demo["cases"]:
        report = process_case(
            case,
            engine_version=engine_version,
            policy_version=policy_version,
            trace_validator=trace_validator,
            decision_validator=decision_validator,
        )
        case_reports.append(report)

    output_validation_results: List[Dict[str, Any]] = []
    for report in case_reports:
        output_validation_results.extend(report["schema_validation"]["results"])

    example_results: List[Dict[str, Any]] = []
    if args.validate_examples:
        if DEFAULT_TRACE_VALID_EXAMPLE.exists():
            result = validate_json_file(DEFAULT_TRACE_VALID_EXAMPLE, trace_validator)
            result["expected_invalid"] = False
            example_results.append(result)
        if DEFAULT_TRACE_INVALID_EXAMPLE.exists():
            result = validate_json_file(DEFAULT_TRACE_INVALID_EXAMPLE, trace_validator)
            result["expected_invalid"] = True
            example_results.append(result)

    schema_validation_summary = build_schema_validation_summary(output_validation_results, examples=example_results)

    write_schema_validation_json(schema_validation_summary)

    summary = build_summary_report(
        case_reports,
        suite_name=suite_name,
        cases_path=args.cases,
        engine_version=engine_version,
        policy_version=policy_version,
        schema_validation_summary=schema_validation_summary,
    )
    write_summary_json(summary)
    print_console_summary(summary)

    run_pass = summary["failed_cases"] == 0
    schema_pass = bool(summary["schema_validation"]["pass"])

    return 0 if (run_pass and schema_pass) else 1


if __name__ == "__main__":
    raise SystemExit(main())
