# KPT Decision Engine v0.1 Architecture Note
## Reference Engine Architecture Final v0.1

Author: Kristjan Jõgi  
Status: Final v0.1  
Applies to: KPT 2.3

---

## 1. Purpose

This note defines the architecture of the first narrow working KPT reference engine.

The purpose of the engine is to prove that KPT can run as a real runtime decision layer, not only as a documentation standard.

The engine must demonstrate that a candidate output can be:

- evaluated before influence or execution;
- assigned a KPT decision state;
- linked to basis codes and rationale;
- converted into enforcement behavior;
- written into a trace object;
- handled differently for human-facing and action-facing routes.

This is a **reference engine**, not a production platform.

---

## 2. Design Goal

The goal of v0.1 is not breadth.  
The goal is a small, clear, inspectable proof of runtime behavior.

The engine should be able to show, end to end:

```text
candidate output -> KPT evaluation -> decision result -> trace -> enforcement outcome
```

The demo must make at least these KPT claims observable:

- output is not action;
- decision happens before influence;
- decision happens before execution;
- decision state is not enforcement action;
- trace exists for every evaluated candidate output;
- execution-relevant qualified outputs do not execute;
- blocked candidate plus safe replacement creates two traces.

---

## 3. Scope of v0.1

v0.1 should support only a narrow reference surface.

### In scope

- one normalized candidate-output input shape;
- one deterministic decision engine;
- one trace generator;
- one enforcement mapper;
- one human-facing route;
- one action-facing route;
- one set of canonical demo cases;
- one simple audit output view.

### Out of scope

- multi-tenant architecture;
- distributed tracing infrastructure;
- production authentication systems;
- UI dashboard;
- real external integrations;
- autonomous agent platform;
- policy-learning or model-based evaluator training.

---

## 4. Core Architectural Position

KPT Decision Engine sits between candidate output and downstream effect.

### Runtime position

```text
Upstream input
  -> Model / Agent
  -> Candidate output
  -> KPT Decision Engine
  -> Trace generation
  -> Enforcement boundary
  -> Human display and/or machine execution
```

This means the engine is not:

- the generator;
- the tool executor;
- the final application UI;
- the data store of record.

It is the **governance boundary**.

---

## 5. v0.1 Assumptions

v0.1 should stay intentionally narrow.

### Assumptions

- context is trusted input from the demo case;
- no live model call is required;
- no live tool execution is required;
- safe replacement text may be predefined in the demo case;
- epistemic sufficiency may be fixture-driven;
- safety and epistemic evaluation should be rule-based or fixture-driven, not model-dependent;
- the goal of v0.1 is to prove runtime architecture, not classifier intelligence.

These assumptions keep the implementation focused on KPT runtime behavior.

---

## 6. Primary Engine Responsibilities

The engine must perform the following responsibilities.

### 6.1 Normalize the candidate

Accept a controlled input object and normalize it into a governed candidate form.

### 6.2 Resolve evaluation context

Determine or accept:

- `zone`
- `profile`
- `deployment_mode`
- `execution_relevance`
- route type

### 6.3 Evaluate safety and weaponized form

Determine whether the candidate should be blocked under `refuse_help`.

### 6.4 Evaluate epistemic status

Determine whether the candidate is:

- sufficiently supported;
- uncertain and therefore qualified;
- insufficient for assertion.

### 6.5 Assign decision state

The engine must output only one of:

- `deliver`
- `qualify`
- `refuse_assert`
- `refuse_help`

### 6.6 Derive basis codes and qualification type

The engine must produce machine-readable basis logic.

### 6.7 Map enforcement

The engine must separate decision state from runtime treatment.

### 6.8 Emit trace

The engine must emit a trace object for every evaluated candidate output.

### 6.9 Enforce route outcome

The engine must visibly demonstrate different behavior for:

- human-facing route;
- action-facing route.

---

## 7. Deterministic Engine Rule

v0.1 epistemic and safety evaluation should be rule-based or fixture-driven, not model-dependent.

The purpose of v0.1 is to prove that KPT runtime architecture works:

- candidate in;
- decision out;
- trace generated;
- enforcement separated;
- route behavior visibly different.

It is **not** intended to prove model-grade classifier intelligence.

---

## 8. Context Priority Rule

In v0.1, context fields should be accepted as provided by the demo case and not inferred dynamically unless the case explicitly tests derivation behavior.

This means:

- `zone`
- `profile`
- `deployment_mode`
- `execution_relevance`
- route type

should normally be treated as case-defined inputs.

This avoids introducing a second engine problem too early.

---

## 9. Required Input Shape

v0.1 should consume the existing normalized evaluation payload shape.

Reference artifact:
- `schemas/evaluation-payload.schema.json`

### Minimum top-level input fields

- `input_ref`
- `output_ref`
- `candidate_output`
- `context`
- `provenance`
- `policy`

### Required candidate identity fields for v0.1 demo work

In addition to the existing payload shape, the demo engine should support:

- `candidate_id`
- optional `parent_candidate_id`
- optional `replacement_for_trace_id`

These fields are especially useful for:

- blocked candidate plus safe replacement;
- candidate lineage;
- dual-trace visualization.

### Important candidate subfields

- `content`
- `content_type`

### Important context subfields

- `zone`
- `profile`
- `deployment_mode`
- `execution_relevant`
- `user_visible`
- `downstream_target`

---

## 10. Required Output Shapes

The engine must produce at least two primary output objects.

### 10.1 Decision result

Reference artifact:
- `schemas/decision-result.schema.json`

The result must include at least:

- `decision_state`
- `basis_codes`
- `qualification_type`
- `rationale`
- `enforcement_action`
- `trace_id`

### 10.2 Trace object

Reference artifact:
- `schemas/trace.schema.json`

The trace must include at least:

- `trace_id`
- `timestamp`
- `input_ref`
- `output_ref`
- `zone`
- `profile`
- `deployment_mode`
- `decision_state`
- `basis_codes`
- `rationale`
- `qualification_type`
- `execution_relevance`
- `enforcement_action`
- `policy_version`
- `engine_version`
- `previous_trace_hash`
- `integrity_hash`

---

## 11. Internal Engine Components

v0.1 should consist of the following modules.

### 11.1 Normalizer

Transforms raw demo input into the evaluation payload shape.

### 11.2 Context Resolver

Reads or derives:

- zone;
- profile;
- deployment mode;
- execution relevance;
- route type.

### 11.3 Safety Evaluator

Applies:

- `SAFE-DISALLOWED-HELP`
- `WF-WEAPONIZED-FORM`

This stage has precedence over epistemic sufficiency.

### 11.4 Epistemic Evaluator

Determines:

- `EPI-SUFFICIENT`
- `EPI-UNCERTAIN`
- `EPI-INSUFFICIENT`

and relevant supporting limitation codes.

### 11.5 Decision Resolver

Maps the evaluation result to one KPT decision state.

### 11.6 Qualification Resolver

Derives:

- `uncertainty`
- `time_sensitive`
- `source_limited`
- `scope_limited`
- `verification_required`
- `mixed`

### 11.7 Enforcement Mapper

Creates explicit runtime treatment.

### 11.8 Trace Emitter

Constructs and writes a trace object.

### 11.9 Demo Route Handler

Shows whether the evaluated candidate is:

- displayed to a human;
- blocked from display;
- sent to execution;
- blocked from execution.

---

## 12. Ordered Evaluation Flow

v0.1 should follow this order exactly.

```text
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
```

This order matters because it preserves:

- safety precedence;
- decision before influence;
- decision before execution;
- trace before execution.

---

## 13. Human-Facing Route

The human-facing route demonstrates governance of display.

### Question answered by this route

**Can the candidate output be shown to a person, and in what form?**

### Expected enforcement behavior

- `deliver` -> show
- `qualify` -> show with qualification
- `refuse_assert` -> block original; optionally show safe replacement
- `refuse_help` -> block original; optionally show safe replacement

### Demo requirement

At least one demo case must show:

- human-facing `deliver`
- human-facing `qualify`
- human-facing `refuse_assert`
- human-facing `refuse_help`

---

## 14. Action-Facing Route

The action-facing route demonstrates governance of execution.

### Question answered by this route

**Can the candidate output be allowed to trigger or enter execution?**

### Expected enforcement behavior

- `deliver` -> execution may be allowed
- `qualify` -> execution blocked
- `refuse_assert` -> execution blocked
- `refuse_help` -> execution blocked

### Demo requirement

At least one demo case must show:

- action-facing `deliver`
- action-facing `qualify` with display allowed but execution blocked
- action-facing `refuse_assert` or `refuse_help` with execution blocked

---

## 15. H Route and A Route Demonstration

The demo must visibly show two route families.

### H route

Human-facing handling path.

This is where KPT proves that governance matters even when nothing is executed automatically.

### A route

Action-facing handling path.

This is where KPT proves that candidate output cannot become runtime action without passing the governance boundary.

### Why this matters

The H/A distinction is one of KPT’s strongest practical differentiators.

Many systems only guard execution.  
KPT must show that it also governs influence.

---

## 16. Minimum Enforcement Contract

For v0.1, the enforcement layer should expose a minimal machine-readable contract.

### Required fields

- canonical core enforcement output: `display` / `execution`
- richer demo enforcement detail may additionally track internal/report-layer fields such as `display_mode`, `execution_mode`, and `replacement_required`
- `replacement_required`: `true | false`

This contract may be represented inside or alongside `enforcement_action`, as long as the mapping is explicit and stable.

### Required distinction

- `decision_state` = what the output is
- `enforcement_action` = what the system does because of that status

---

## 17. Trace Generation Requirements

Trace generation is mandatory for every evaluated candidate output.

### v0.1 minimum requirements

- one trace per evaluated candidate;
- unique `trace_id`;
- timestamp;
- explicit decision state;
- explicit basis codes;
- explicit enforcement action;
- append-only write behavior in the demo output directory;
- per-trace integrity hash;
- optional previous-trace linkage.

### Hash-chain rule for v0.1

v0.1 may use a simple append-only file log with per-trace integrity hash and optional previous-trace linkage.

Full tamper-evident chain behavior is preferred but not required for the first demo.

### Trace timing rule

For execution-relevant candidates:

**trace must be written before execution outcome is allowed to proceed**

### Dual-trace rule

If a blocked candidate is replaced with a safer response:

- original blocked candidate gets one trace;
- replacement candidate gets a second trace.

---

## 18. Enforcement Boundary Requirements

The demo must visibly separate:

- decision assignment;
- enforcement mapping;
- execution gate.

### Minimum visible outcomes

- `deliver` proceeds;
- `qualify` can remain visible but execution is blocked if execution-relevant;
- `refuse_assert` does not proceed;
- `refuse_help` does not proceed.

---

## 19. Canonical Demo Scenario Set

v0.1 should include a narrow but representative case set.

### Recommended minimum set

1. analytical human-facing deliver
2. analytical human-facing qualify
3. analytical human-facing refuse_assert
4. critical human-facing refuse_help
5. action-facing critical deliver
6. action-facing critical qualify with blocked execution
7. action-facing critical refuse_help
8. blocked candidate plus safe replacement with two traces

### Why this set is enough

This set proves:

- all four decision states;
- both route families;
- execution blocking for qualified machine-path outputs;
- dual-trace behavior.

---

## 20. Canonical Case Contract

Each demo case must define:

- `case_id`
- `route_type`
- `zone`
- `profile`
- `deployment_mode`
- `execution_relevant`
- candidate content
- expected `decision_state`
- expected `basis_codes`
- expected `qualification_type`
- expected enforcement outcome
- expected trace count

This is mandatory for v0.1 because canonical cases must constrain implementation behavior.

Without this contract, the engine builder may accidentally redefine the standard during implementation.

---

## 21. Expected Demo Outputs

v0.1 does not need a UI.

It should produce clear outputs such as:

- console summary;
- JSON files;
- trace files in a demo output folder;
- a simple audit report.

### Minimum visible fields

For each case, a reviewer should be able to see:

- input
- route
- zone
- profile
- deployment mode
- decision state
- basis codes
- qualification type
- enforcement action
- trace id
- whether display happened
- whether execution happened

---

## 22. Machine-Verifiable Success Rule

v0.1 is complete only if the engine output can be automatically checked against expected decision and enforcement outcomes for the canonical demo set.

This means the demo is not only viewable.  
It is also testable.

At minimum, the demo runner should be able to compare:

- actual decision state vs expected decision state;
- actual basis codes vs expected basis codes;
- actual qualification type vs expected qualification type;
- actual enforcement outcome vs expected enforcement outcome;
- actual trace count vs expected trace count.

---

## 23. Suggested Repository Layout for Engine Work

```text
reference-engine/
  README.md
  engine.py
  trace.py
  enforcement.py
  demo_cases.yaml
  run_demo.py
  outputs/
    traces/
    decisions/
    reports/
```

Alternative layout:

```text
engine/
  kpt_engine.py
  kpt_trace.py
  kpt_enforcement.py
examples/
  engine_demo_cases.yaml
outputs/
  engine_demo/
```

---

## 24. Suggested Implementation Style

v0.1 should be:

- deterministic-first;
- easy to inspect;
- easy to explain;
- easy to map back to the written standard;
- not dependent on hidden model reasoning;
- not dependent on live external APIs.

The first engine should look like a reference machine, not a product.

---

## 25. Standard Gap Capture

The engine work must produce a written gap list.

This is a required output of the implementation exercise.

### The gap list should capture

- unclear zone-assignment situations;
- weak or missing basis-code distinctions;
- unclear qualification derivation;
- unclear enforcement mappings;
- trace schema fields that need strengthening;
- H/A route ambiguities;
- candidate-splitting ambiguities;
- replacement-trace ambiguities.

### Why this matters

Building the engine is not just a demo exercise.  
It is also a standard-hardening exercise.

---

## 26. Non-Goals for v0.1

The reference engine should not try to prove:

- enterprise scalability;
- production security hardening;
- complete policy coverage for all domains;
- all possible integrations;
- autonomous agent orchestration.

It only needs to prove that:

- KPT logic can run;
- trace can be generated;
- enforcement can be separated from decision;
- human and action routes can be governed differently.

---

## 27. Success Criteria

v0.1 is successful if a reviewer can watch the demo and clearly see:

1. model output becomes candidate output;
2. KPT assigns a valid decision state;
3. basis codes explain the decision;
4. trace is created for the candidate;
5. route behavior differs for human vs machine pathways;
6. qualified execution-relevant output does not execute;
7. blocked candidate plus safe replacement creates two traces;
8. canonical demo cases pass automatic expected-output checks.

If those claims are visible, KPT moves from documented standard to demonstrated runtime layer.

---

## 28. Recommended Next Deliverables After This Note

After this architecture note, the next implementation deliverables should be:

1. `reference-engine/demo_cases.yaml`
2. `reference-engine/engine.py`
3. `reference-engine/trace.py`
4. `reference-engine/enforcement.py`
5. `reference-engine/run_demo.py`
6. `reference-engine/GAP_REPORT.md`

---

## 29. Recommended Repository Path

```text
docs/kpt-engine-v0_1-architecture-note.md
```
