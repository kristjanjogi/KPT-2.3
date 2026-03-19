# KPT 2.3 Basis Codes Registry

**Author:** Kristjan Jõgi  
**Document date:** 2026-03-08

**Version:** Working Draft v0.3  
**Status:** Draft  
**Purpose:** Normative decision-grounding code system for KPT 2.3.

## 1. Code format

Basis codes MUST match the pattern:

```text
^[A-Z0-9]+(?:-[A-Z0-9]+)+$
```

Additional canonical rules:

- codes MUST be uppercase
- codes MUST be unique within `basis_codes`
- codes MUST be lexicographically sorted
- codes MUST correspond to materially operative reasons used in the decision
- basis codes MUST NOT be decorative annotations

## 2. Code roles

### 2.1 Primary decision drivers

- `EPI-SUFFICIENT`
- `EPI-UNCERTAIN`
- `EPI-INSUFFICIENT`
- `SAFE-DISALLOWED-HELP`
- `WF-WEAPONIZED-FORM`

### 2.2 Supporting limitations

- `SRC-UNVERIFIED`
- `SRC-NO-PRIMARY`
- `SRC-CONFLICT`
- `TMP-TIME-SENSITIVE`
- `SCP-SCOPE-LIMITED`
- `VER-REQUIRED`

Supporting limitation codes refine the reason for a decision. They do not replace the primary decision driver.

## 3. Family definitions

- **EPI** — epistemic status of support for the candidate output
- **SRC** — source-basis limitation
- **TMP** — temporal instability or freshness limitation
- **SCP** — scope-bound support limitation
- **VER** — additional verification requirement
- **SAFE** — disallowed-help boundary
- **WF** — weaponized operational form

## 4. Mutually exclusive codes

The following pairs MUST NOT co-occur:

- `EPI-SUFFICIENT` and `EPI-UNCERTAIN`
- `EPI-SUFFICIENT` and `EPI-INSUFFICIENT`
- `EPI-UNCERTAIN` and `EPI-INSUFFICIENT`

## 5. Decision binding rules

### 5.1 `deliver`

`deliver` requires:

- primary: `EPI-SUFFICIENT`

`deliver` forbids:

- primary: `EPI-UNCERTAIN`, `EPI-INSUFFICIENT`, `SAFE-DISALLOWED-HELP`, `WF-WEAPONIZED-FORM`
- supporting: `SRC-UNVERIFIED`, `SRC-NO-PRIMARY`, `SRC-CONFLICT`, `TMP-TIME-SENSITIVE`, `SCP-SCOPE-LIMITED`, `VER-REQUIRED`

`qualification_type` MUST be `null`.

### 5.2 `qualify`

`qualify` requires:

- primary: `EPI-UNCERTAIN`

`qualify` MAY include any supporting limitation code.

`qualify` forbids:

- primary: `EPI-SUFFICIENT`, `EPI-INSUFFICIENT`, `SAFE-DISALLOWED-HELP`, `WF-WEAPONIZED-FORM`

`qualification_type` MUST NOT be `none`.

### 5.3 `refuse_assert`

`refuse_assert` requires:

- primary: `EPI-INSUFFICIENT`

`refuse_assert` MAY include any supporting limitation code.

`refuse_assert` forbids:

- primary: `EPI-SUFFICIENT`, `EPI-UNCERTAIN`, `SAFE-DISALLOWED-HELP`, `WF-WEAPONIZED-FORM`

`qualification_type` MUST be `null`.

### 5.4 `refuse_help`

`refuse_help` requires at least one of:

- `SAFE-DISALLOWED-HELP`
- `WF-WEAPONIZED-FORM`

`refuse_help` forbids:

- primary: `EPI-SUFFICIENT`, `EPI-UNCERTAIN`, `EPI-INSUFFICIENT`
- supporting: `SRC-UNVERIFIED`, `SRC-NO-PRIMARY`, `SRC-CONFLICT`, `TMP-TIME-SENSITIVE`, `SCP-SCOPE-LIMITED`, `VER-REQUIRED`

`qualification_type` MUST be `null`.

## 6. Qualification derivation

`qualification_type` is valid only when `decision_state = qualify`.

Rules:

- `qualify` MUST include `EPI-UNCERTAIN`
- `qualify` with no supporting limitation family -> `qualification_type = uncertainty`
- `qualify` with exactly one supporting family `SRC` -> `source_limited`
- `qualify` with exactly one supporting family `TMP` -> `time_sensitive`
- `qualify` with exactly one supporting family `SCP` -> `scope_limited`
- `qualify` with exactly one supporting family `VER` -> `verification_required`
- `qualify` with more than one supporting family -> `mixed`

## 7. Safety precedence

Safety precedence is decision-determinative.

- `SAFE-DISALLOWED-HELP` overrides epistemic sufficiency or insufficiency for decision selection
- `WF-WEAPONIZED-FORM` overrides epistemic sufficiency or insufficiency for decision selection
- if `SAFE-DISALLOWED-HELP` or `WF-WEAPONIZED-FORM` is present, `decision_state MUST = refuse_help`
- factually accurate, well-sourced, or otherwise epistemically sufficient harmful assistance remains `refuse_help`

Supporting limitation codes cannot on their own justify `refuse_help`.

## 8. Escalation rules

- presence of `SAFE-DISALLOWED-HELP` or `WF-WEAPONIZED-FORM` escalates directly to `refuse_help`
- presence of `EPI-INSUFFICIENT` prohibits `deliver` and `qualify`
- presence of `EPI-UNCERTAIN` prohibits `deliver`
- presence of `VER-REQUIRED` prohibits `deliver`
- presence of `TMP-TIME-SENSITIVE` prohibits `deliver`
- presence of `SCP-SCOPE-LIMITED` prohibits `deliver`
- presence of `SRC-NO-PRIMARY` prohibits `deliver`
- presence of `SRC-UNVERIFIED` prohibits `deliver`
- if supporting limitation codes exist but epistemic insufficiency is determined, the result MUST be `refuse_assert`, not `qualify`

## 9. Extension namespace

Implementations MAY define extension codes under the reserved `X-*` namespace.

Recommended structure:

```text
X-<ISSUER>-<PURPOSE>
```

Examples:

- `X-ORG-COMPLIANCE`
- `X-LEGAL-REVIEW`
- `X-INTERNAL-ESCALATION`

Extension-code rules:

- `X-*` MUST NOT replace required standard basis codes
- `X-*` MUST NOT override core decision grammar
- `X-*` MUST NOT satisfy a conformance requirement that depends on a standard code
- `X-*` MAY add organization-specific audit context or policy overlays
- extension semantics are ignored for base conformance unless a fixture or profile explicitly enables extension-aware evaluation

## 10. Registry

| Code | Family | Role | Meaning | Allowed decision states |
|---|---|---|---|---|
| `EPI-SUFFICIENT` | EPI | primary | available basis is sufficient for bounded delivery | `deliver` |
| `EPI-UNCERTAIN` | EPI | primary | output may be delivered only with explicit qualification | `qualify` |
| `EPI-INSUFFICIENT` | EPI | primary | output lacks sufficient support for assertion | `refuse_assert` |
| `SRC-UNVERIFIED` | SRC | supporting | source basis exists but remains materially unverified | `qualify`, `refuse_assert` |
| `SRC-NO-PRIMARY` | SRC | supporting | primary or equivalently trusted grounding is absent where materially needed | `qualify`, `refuse_assert` |
| `SRC-CONFLICT` | SRC | supporting | materially conflicting source packet prevents clean unqualified reliance | `qualify`, `refuse_assert` |
| `TMP-TIME-SENSITIVE` | TMP | supporting | claim depends on unstable or current conditions that block unqualified delivery | `qualify`, `refuse_assert` |
| `SCP-SCOPE-LIMITED` | SCP | supporting | candidate output overreaches the supported scope | `qualify`, `refuse_assert` |
| `VER-REQUIRED` | VER | supporting | additional verification is required before stronger reliance or execution use | `qualify`, `refuse_assert` |
| `SAFE-DISALLOWED-HELP` | SAFE | primary | candidate output constitutes disallowed help | `refuse_help` |
| `WF-WEAPONIZED-FORM` | WF | primary | candidate output is materially operationalized in weaponized form | `refuse_help` |

## 11. Canonical allowed combinations

- `["EPI-SUFFICIENT"]`
- `["EPI-UNCERTAIN"]`
- `["EPI-UNCERTAIN", "SRC-UNVERIFIED"]`
- `["EPI-UNCERTAIN", "TMP-TIME-SENSITIVE"]`
- `["EPI-UNCERTAIN", "SRC-UNVERIFIED", "VER-REQUIRED"]`
- `["EPI-INSUFFICIENT"]`
- `["EPI-INSUFFICIENT", "SRC-NO-PRIMARY"]`
- `["EPI-INSUFFICIENT", "TMP-TIME-SENSITIVE", "VER-REQUIRED"]`
- `["SAFE-DISALLOWED-HELP"]`
- `["SAFE-DISALLOWED-HELP", "WF-WEAPONIZED-FORM"]`
- `["WF-WEAPONIZED-FORM"]`

## 12. Canonical forbidden combinations

- `["EPI-SUFFICIENT", "EPI-UNCERTAIN"]`
- `["EPI-SUFFICIENT", "EPI-INSUFFICIENT"]`
- `["EPI-UNCERTAIN", "EPI-INSUFFICIENT"]`
- `["EPI-SUFFICIENT", "TMP-TIME-SENSITIVE"]`
- `["EPI-SUFFICIENT", "VER-REQUIRED"]`
- `["EPI-SUFFICIENT", "SRC-UNVERIFIED"]`
- `["EPI-SUFFICIENT", "SCP-SCOPE-LIMITED"]`
- `["EPI-UNCERTAIN", "SAFE-DISALLOWED-HELP"]`
- `["EPI-INSUFFICIENT", "SAFE-DISALLOWED-HELP"]`
- `["EPI-UNCERTAIN", "WF-WEAPONIZED-FORM"]`
- `["EPI-INSUFFICIENT", "WF-WEAPONIZED-FORM"]`
- `["SAFE-DISALLOWED-HELP", "SRC-UNVERIFIED"]`
- `["WF-WEAPONIZED-FORM", "VER-REQUIRED"]`

## 13. Canonical invalid combinations appendix

- `decision_state=deliver` with `qualification_type=time_sensitive`
- `decision_state=deliver` with basis code `TMP-TIME-SENSITIVE`
- `decision_state=deliver` with basis code `VER-REQUIRED`
- `decision_state=qualify` with `qualification_type=none`
- `decision_state=qualify` without `EPI-UNCERTAIN`
- `decision_state=qualify` with `SAFE-DISALLOWED-HELP`
- `decision_state=refuse_assert` without `EPI-INSUFFICIENT`
- `decision_state=refuse_assert` with `EPI-SUFFICIENT`
- `decision_state=refuse_help` with `EPI-UNCERTAIN`
- `decision_state=refuse_help` with `qualification_type != none`
- `SAFE-DISALLOWED-HELP` present while `decision_state != refuse_help`
- `WF-WEAPONIZED-FORM` present while `decision_state != refuse_help`
- `X-*` used as a substitute for a required standard code