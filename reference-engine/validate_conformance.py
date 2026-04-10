"""
Validate canonical examples and generated decision/trace outputs against the
KPT schemas.

This script is intended as a public conformance validation utility for the reference-engine surface.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

from jsonschema import Draft202012Validator, FormatChecker


REFERENCE_ENGINE_ROOT = Path(__file__).resolve().parent
PACKAGE_ROOT = REFERENCE_ENGINE_ROOT.parent.resolve()
SCHEMAS_ROOT = PACKAGE_ROOT / "schemas"
TRACE_SCHEMA_PATH = SCHEMAS_ROOT / "trace.schema.json"
DECISION_SCHEMA_PATH = SCHEMAS_ROOT / "decision-result.schema.json"

DEFAULT_OUTPUTS_ROOT = REFERENCE_ENGINE_ROOT / "outputs"
DEFAULT_JSON_REPORT = PACKAGE_ROOT / "CONFORMANCE_REPORT.json"
DEFAULT_MD_REPORT = PACKAGE_ROOT / "CONFORMANCE_REPORT.md"


def display_path(path: Path) -> str:
    path = path.resolve()
    try:
        return path.relative_to(PACKAGE_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def load_validator(schema_path: Path) -> Draft202012Validator:
    with schema_path.open("r", encoding="utf-8") as f:
        schema = json.load(f)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_json(path: Path, validator: Draft202012Validator) -> Dict[str, object]:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
    return {
        "file": display_path(path),
        "valid": len(errors) == 0,
        "error_count": len(errors),
        "errors": [
            {
                "message": err.message,
                "path": list(err.path),
                "schema_path": list(err.schema_path),
            }
            for err in errors
        ],
    }


def discover_files(root: Path, suffix: str) -> List[Path]:
    return sorted(root.rglob(suffix))


def build_report(outputs_root: Path) -> Dict[str, object]:
    trace_validator = load_validator(TRACE_SCHEMA_PATH)
    decision_validator = load_validator(DECISION_SCHEMA_PATH)

    trace_files = discover_files(outputs_root, "*.json")
    trace_files = [p for p in trace_files if p.parent.name == "traces"]
    decision_files = discover_files(outputs_root, "*.json")
    decision_files = [p for p in decision_files if p.parent.name == "decisions"]

    trace_results = [validate_json(path, trace_validator) for path in trace_files]
    decision_results = [validate_json(path, decision_validator) for path in decision_files]

    examples = []
    valid_trace = PACKAGE_ROOT / "examples" / "trace-valid-example.json"
    invalid_trace = PACKAGE_ROOT / "examples" / "trace-invalid-example.json"
    if valid_trace.exists():
        item = validate_json(valid_trace, trace_validator)
        item["expected_invalid"] = False
        examples.append(item)
    if invalid_trace.exists():
        item = validate_json(invalid_trace, trace_validator)
        item["expected_invalid"] = True
        examples.append(item)

    expected_valid_failed = [item["file"] for item in examples if not item.get("expected_invalid") and not item["valid"]]
    expected_invalid_passed = [item["file"] for item in examples if item.get("expected_invalid") and item["valid"]]

    report = {
        "trace_files_checked": len(trace_results),
        "decision_files_checked": len(decision_results),
        "invalid_trace_files": [item["file"] for item in trace_results if not item["valid"]],
        "invalid_decision_files": [item["file"] for item in decision_results if not item["valid"]],
        "examples_checked": len(examples),
        "expected_valid_examples_failed": expected_valid_failed,
        "expected_invalid_examples_passed": expected_invalid_passed,
        "trace_results": trace_results,
        "decision_results": decision_results,
        "example_results": examples,
    }
    report["pass"] = (
        len(report["invalid_trace_files"]) == 0
        and len(report["invalid_decision_files"]) == 0
        and len(expected_valid_failed) == 0
        and len(expected_invalid_passed) == 0
    )
    return report


def write_reports(report: Dict[str, object], json_path: Path, md_path: Path) -> None:
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md_lines = [
        "# Conformance Report",
        "",
        f"- Trace files checked: {report['trace_files_checked']}",
        f"- Decision files checked: {report['decision_files_checked']}",
        f"- Examples checked: {report['examples_checked']}",
        f"- Invalid trace files: {len(report['invalid_trace_files'])}",
        f"- Invalid decision files: {len(report['invalid_decision_files'])}",
        f"- Expected-valid examples failed: {len(report['expected_valid_examples_failed'])}",
        f"- Expected-invalid examples passed: {len(report['expected_invalid_examples_passed'])}",
        "",
        "## Result",
        "",
        f"- Overall pass: {'yes' if report['pass'] else 'no'}",
        "",
    ]

    if report["invalid_trace_files"]:
        md_lines.append("## Invalid trace files")
        md_lines.append("")
        for item in report["invalid_trace_files"]:
            md_lines.append(f"- `{item}`")
        md_lines.append("")

    if report["invalid_decision_files"]:
        md_lines.append("## Invalid decision files")
        md_lines.append("")
        for item in report["invalid_decision_files"]:
            md_lines.append(f"- `{item}`")
        md_lines.append("")

    if report["expected_valid_examples_failed"]:
        md_lines.append("## Expected-valid examples that failed")
        md_lines.append("")
        for item in report["expected_valid_examples_failed"]:
            md_lines.append(f"- `{item}`")
        md_lines.append("")

    if report["expected_invalid_examples_passed"]:
        md_lines.append("## Expected-invalid examples that passed unexpectedly")
        md_lines.append("")
        for item in report["expected_invalid_examples_passed"]:
            md_lines.append(f"- `{item}`")
        md_lines.append("")

    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate KPT canonical examples and generated outputs against schemas.")
    parser.add_argument("--outputs-root", type=Path, default=DEFAULT_OUTPUTS_ROOT)
    parser.add_argument("--json-report", type=Path, default=DEFAULT_JSON_REPORT)
    parser.add_argument("--md-report", type=Path, default=DEFAULT_MD_REPORT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(args.outputs_root)
    write_reports(report, args.json_report, args.md_report)
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
