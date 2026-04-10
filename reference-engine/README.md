# KPT Reference Engine v0.1

Reference implementation workspace for the first narrow working KPT decision engine.

This directory exists to prove that KPT can run as a real runtime decision layer, not only as a documentation standard.

The goal of v0.1 is to demonstrate, end to end:

```text
candidate output -> KPT evaluation -> decision result -> trace -> enforcement outcome
```

This is a reference engine, not a production platform.

---

## 1. What this engine proves

v0.1 must make the following KPT claims observable:

- output is not action;
- decision happens before influence;
- decision happens before execution;
- decision state is not enforcement action;
- trace exists for every evaluated candidate output;
- execution-relevant qualified outputs do not execute;
- blocked candidate plus safe replacement creates two traces.

---

## 2. Scope of v0.1

### In scope

- one deterministic decision engine;
- one normalized candidate input shape;
- one trace generator;
- one enforcement mapper;
- one human-facing route;
- one action-facing route;
- one canonical demo case set;
- one machine-checkable demo runner;
- one simple audit output view.

### Out of scope

- production UI;
- live external integrations;
- autonomous agent orchestration;
- model training;
- policy learning;
- distributed tracing infrastructure;
- enterprise auth;
- production hardening.

---

## 3. Directory purpose

This directory contains the narrow reference engine for KPT runtime behavior.

Preferred layout:

```text
reference-engine/
  README.md
  demo_cases.yaml
  engine.py
  trace.py
  enforcement.py
  run_demo.py
  outputs/
    traces/
    decisions/
    reports/
```

---

## 4. Implementation philosophy

v0.1 is intentionally narrow.

It should be:

- deterministic-first;
- easy to inspect;
- easy to explain;
- easy to map back to the written standard;
- not dependent on hidden model reasoning;
- not dependent on live APIs.

The purpose of v0.1 is to prove runtime architecture, not classifier intelligence.

---

## 5. v0.1 assumptions

The following assumptions are intentionally locked for v0.1:

- context is trusted input from the demo case;
- no live model call is required;
- no live tool execution is required;
- safe replacement text may be predefined in the demo case;
- epistemic sufficiency may be fixture-driven;
- safety and epistemic evaluation may be rule-based or fixture-driven;
- the engine is proving KPT runtime behavior, not general model accuracy.

---

## 6. Core flow

The engine should implement this order exactly:

1. receive candidate
2. normalize input
3. resolve context
4. determine execution relevance
5. run safety evaluation
6. if safety hit -> refuse_help
7. else run epistemic evaluation
8. assign decision_state
9. derive basis_codes and qualification_type
10. map enforcement_action
11. emit trace
12. route to human display and/or execution boundary
13. if blocked and safe replacement exists -> evaluate replacement as new candidate

This preserves:

- safety precedence;
- decision before influence;
- decision before execution;
- trace before execution.

---

## 7. Canonical demo cases

The engine is constrained by `demo_cases.yaml`.

That file is not just sample input.
It is the first canonical runtime test contract for KPT v0.1.

The engine must satisfy the case contract rather than redefining it.

Each case defines at minimum:

- `case_id`
- `route_type`
- `zone`
- `profile`
- `deployment_mode`
- `execution_relevant`
- `candidate_output`
- expected `decision_state`
- expected minimum `basis_codes`
- expected `qualification_type`
- expected enforcement outcome
- expected trace count

---

## 8. Core contract vs demo/report layer

v0.1 now treats the canonical schemas as the source of truth for written decision and trace outputs.

Core decision and trace files must conform to:

- `schemas/decision-result.schema.json`
- `schemas/trace.schema.json`

The richer demo runner still uses internal/helper fields for comparison reporting, including:

- `candidate_id`
- fixture-driving provenance fields
- richer enforcement details such as `display_mode`, `execution_mode`, and `replacement_required`

Those richer fields belong to the comparison/report layer or internal runtime state.  
They do not belong in the schema-governed decision and trace outputs.

---

## 9. Naming alignment for v0.1

The demo runner intentionally distinguishes:

- input/demo fixture vocabulary, such as `execution_relevant`
- canonical output vocabulary, such as boolean `execution_relevance`

This is acceptable only because the runner explicitly normalizes the internal/demo representation into the canonical output contract before writing decisions and traces.

Preferred demo vocab for v0.1 remains:

- `route_type`: `human | action`
- `downstream_target`: `display | tool | api | file | mixed`
- `content_type`: `text | tool_call`

---

## 10. Decision vs enforcement

One of the most important KPT claims is that decision state is not enforcement action.

The engine keeps these separate.

### Decision state

What the candidate output is:

- `deliver`
- `qualify`
- `refuse_assert`
- `refuse_help`

### Canonical enforcement

What the system does because of that status, in normalized core form:

```json
{
  "display": "allow | allow_with_qualification | block_original",
  "execution": "allow | block | not_applicable"
}
```

The comparison/report layer may retain richer demo enforcement detail, but the written decision and trace artifacts must stay in this normalized core form.

---

## 11. Human route and action route

The demo must visibly show both route families.

### Human-facing route

Answers:

**Can this output be shown to a person, and in what form?**

Expected behavior:

- `deliver` -> show
- `qualify` -> show with qualification
- `refuse_assert` -> block original; optional safe replacement
- `refuse_help` -> block original; optional safe replacement

### Action-facing route

Answers:

**Can this output be allowed to trigger or enter execution?**

Expected behavior:

- `deliver` -> execution may be allowed
- `qualify` -> execution blocked
- `refuse_assert` -> execution blocked
- `refuse_help` -> execution blocked

The H/A distinction is one of KPT’s strongest practical differentiators.
The demo must make that visible.

---

## 12. Trace rules

Every evaluated candidate must produce a trace.

Minimum v0.1 requirements:

- one trace per evaluated candidate;
- unique `trace_id`;
- timestamp;
- explicit `decision_state`;
- explicit `basis_codes`;
- explicit enforcement result;
- append-only write behavior in demo output;
- per-trace integrity hash;
- optional previous-trace linkage.

### Timing rule

For execution-relevant candidates:

**trace must be written before execution is allowed to proceed**

### Dual-trace rule

If a blocked candidate is replaced with a safer response:

- the blocked candidate gets one trace;
- the replacement candidate gets a second trace.

---

## 13. Machine-verifiable completion rule

The demo is not complete just because it prints plausible output.

`run_demo.py` must compare actual vs expected results for the canonical case set.

At minimum it should verify:

- actual decision state vs expected decision state;
- actual minimum basis codes vs expected minimum basis codes;
- actual qualification type vs expected qualification type;
- actual enforcement outcome vs expected enforcement outcome;
- actual trace count vs expected trace count.

For basis codes, v0.1 should use the rule:

**expected basis codes are minimum required basis codes, not necessarily the only allowed codes.**

This keeps the engine from becoming too brittle during early implementation.

---

## 14. Required files

The minimum implementation set is:

1. `demo_cases.yaml`
2. `engine.py`
3. `trace.py`
4. `enforcement.py`
5. `run_demo.py`
6. `GAP_REPORT.md`

---

## 15. File responsibilities

### `demo_cases.yaml`

Canonical runtime case contract.

### `engine.py`

Core evaluation logic:

- normalization
- context handling
- safety evaluation
- epistemic evaluation
- decision resolution
- qualification resolution

### `trace.py`

Trace construction and append-only writing.

### `enforcement.py`

Decision-to-enforcement mapping and route outcome handling.

### `run_demo.py`

Runner that:

- loads demo cases;
- executes the engine;
- writes outputs;
- compares actual vs expected;
- produces a pass/fail report.

### `GAP_REPORT.md`

Implementation feedback into the standard.

This must capture:

- unclear zone assignment situations;
- basis code ambiguities;
- qualification ambiguities;
- enforcement mapping ambiguities;
- trace field weaknesses;
- H/A route ambiguities;
- replacement/lineage ambiguities;
- any place where demo extensions suggest future schema decisions.

---

## 16. Expected outputs

The demo does not need a UI.

It should produce:

- console summary;
- decision JSON outputs;
- trace files;
- a simple report showing pass/fail by case.

A reviewer should be able to see, for each case:

- input
- route
- zone
- profile
- deployment mode
- decision state
- basis codes
- qualification type
- enforcement outcome
- trace id
- whether display happened
- whether execution happened

---

## 17. Success definition

v0.1 is successful if a reviewer can clearly see that:

1. model output becomes candidate output;
2. KPT assigns a valid decision state;
3. basis codes explain the decision;
4. trace is created for the candidate;
5. human and action routes behave differently;
6. execution-relevant qualified outputs do not execute;
7. blocked candidate plus safe replacement creates two traces;
8. canonical cases pass machine-verifiable checks.

At that point KPT moves from documented standard to demonstrated runtime layer.

---

## 18. Immediate next step

Do not start broad engine implementation first.

Start with:

`reference-engine/demo_cases.yaml`

Then implement:

`run_demo.py`

Then build the engine to satisfy the canonical case contract.

The engine should implement against the note and the canonical cases exactly.


## 19. Suite execution

Schema validation is part of the runner.
For every run, written decision and trace outputs are validated against the canonical schemas.
A run is considered failed if case comparisons fail or if any written core output is schema-invalid.


`run_demo.py` now supports explicit suite selection and output roots.

Examples:

```bash
python3 reference-engine/run_demo.py
python3 reference-engine/run_demo.py --cases reference-engine/demo_cases_v0_1b_adversarial.yaml --output-root reference-engine/outputs/adversarial_v0_1b --clean-output
python3 reference-engine/run_demo.py --cases reference-engine/demo_cases_v0_1c_robustness.yaml --output-root reference-engine/outputs/robustness_v0_1c --clean-output
```

This removes the earlier v0.1 limitation where the runner was effectively locked to the canonical suite file.
Generated reports now write repo-relative artifact paths so the public reference-engine surface stays portable across machines.

## 20. Extension suites currently included

- `demo_cases.yaml` = canonical first successful run
- `demo_cases_v0_1b_adversarial.yaml` = adversarial extension set
- `demo_cases_v0_1c_robustness.yaml` = broader robustness extension set

All three suites are now directly runnable through the same runner entry point.
