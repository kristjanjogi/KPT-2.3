# KPT 2.3 Implementation Guide
## Skeleton v0.1

Author: Kristjan Jõgi  
Status: Draft Skeleton  
Applies to: KPT 2.3

---

## 1. Purpose

This guide explains how to implement KPT 2.3 as a runtime decision-governance layer around AI systems.

It is intended for teams building systems where AI outputs may:

- influence decisions;
- trigger external actions;
- be displayed to users in governed contexts;
- be routed into tools, APIs, files, or workflows.

This guide does not define the standard itself.  
It explains how to operationalize the standard in real systems.

---

## 2. What KPT Is and Is Not

### 2.1 What KPT is

KPT is a decision-governance layer that sits between candidate output and downstream effect.

It ensures that:

- governed outputs are evaluated before influence or execution;
- each evaluated candidate output receives a decision state;
- decision state is recorded independently from enforcement;
- execution-relevant outputs are traced before execution.

### 2.2 What KPT is not

KPT is not:

- the model;
- the retrieval system;
- the business workflow engine;
- a generic moderation filter;
- a logging layer added after the fact;
- a guarantee of truth.

---

## 3. Core Implementation Principle

### 3.1 Output is not action

In implementation terms, generated content must be treated as a candidate object with no execution authority by default.

That means:

- a model response is not yet an action;
- a tool proposal is not yet a permission;
- structured output is not yet a committed system state;
- candidate output must first pass through KPT evaluation.

### 3.2 Decision before effect

A system implementing KPT must not allow:

- direct execution from raw model output;
- display of governed output before decision assignment where policy requires governance;
- post-hoc trace creation for execution-relevant outputs.

---

## 4. When to Use KPT

KPT is most useful when outputs may affect real-world decisions or actions.

Typical use cases include:

- assistants that propose actions;
- agents that call tools;
- systems that generate operational recommendations;
- systems that produce regulated or high-stakes guidance;
- governance middleware for enterprise AI workflows;
- human-in-the-loop review systems.

KPT is less important for purely decorative or low-risk creative output, though the standard may still apply depending on deployment goals.

---

## 5. Implementation Targets

This guide assumes implementation against one or more of the following targets:

- chat assistants;
- agent runtimes;
- API orchestration layers;
- workflow automation systems;
- internal enterprise governance gateways;
- human review frontends.

---

## 6. Minimum Components

A basic KPT implementation should include:

- candidate output normalizer;
- context resolver;
- safety evaluator;
- epistemic evaluator;
- decision resolver;
- enforcement mapper;
- trace emitter;
- execution gate.

A stronger implementation may also include:

- policy registry;
- version pinning;
- trace chain verification;
- replacement-output loop;
- reviewer override layer;
- conformance testing harness.

---

## 7. Required Inputs

A minimal implementation should be able to ingest a normalized evaluation object containing at least:

- input reference;
- output reference;
- candidate output content;
- content type;
- zone;
- profile;
- deployment mode;
- execution relevance;
- provenance / verification state;
- policy version;
- engine version.

Reference artifact:
- `schemas/evaluation-payload.schema.json`

---

## 8. Required Outputs

A minimal implementation should be able to produce:

- decision result object;
- enforcement mapping;
- trace object.

Reference artifacts:
- `schemas/decision-result.schema.json`
- `schemas/trace.schema.json`

---

## 9. Deployment Patterns

### 9.1 Inline middleware

KPT runs directly in the live request path.

Best for:
- immediate tool control;
- strong execution gating;
- synchronous assistant flows.

### 9.2 Sidecar governance service

KPT runs as a separate service called by one or more applications.

Best for:
- centralized governance;
- multi-product environments;
- consistent tracing.

### 9.3 Embedded library

KPT logic is packaged directly into application code.

Best for:
- prototypes;
- demos;
- early pilots.

---

## 10. End-to-End Runtime Flow

A conformant implementation should follow this high-level order:

1. receive upstream input;
2. build application context;
3. generate candidate output;
4. normalize candidate for governance;
5. resolve governed context;
6. determine execution relevance;
7. evaluate safety;
8. evaluate epistemic sufficiency;
9. assign decision state;
10. derive qualification type if needed;
11. map enforcement action;
12. emit trace;
13. permit or block display and/or execution;
14. optionally generate and re-evaluate safe replacement.

This ordering is central to KPT.

---

## 11. Decision Logic Implementation

### 11.1 Decision states

The implementation must support:

- `deliver`
- `qualify`
- `refuse_assert`
- `refuse_help`

### 11.2 Locked logic

The implementation must preserve:

- `qualify` includes `EPI-UNCERTAIN`
- `deliver` includes `EPI-SUFFICIENT` and no limitation/safety codes
- `refuse_assert` includes `EPI-INSUFFICIENT`
- `SAFE-DISALLOWED-HELP` or `WF-WEAPONIZED-FORM` => `refuse_help`
- safety precedence overrides epistemic sufficiency

### 11.3 Qualification derivation

The implementation should derive `qualification_type` from supporting limitation families.

---

## 12. Enforcement Boundary Implementation

A conformant implementation must keep decision and enforcement separate.

### 12.1 Decision state

Decision state describes what the output is.

### 12.2 Enforcement action

Enforcement describes what the runtime does because of that status.

### 12.3 Minimum mappings

- `deliver` -> display allowed; execution may be allowed
- `qualify` -> display with qualification; execution blocked if execution-relevant
- `refuse_assert` -> original blocked; execution blocked
- `refuse_help` -> original blocked; execution blocked

---

## 13. Trace Implementation

### 13.1 One trace per evaluated candidate output

Every evaluated candidate output must produce its own trace.

### 13.2 Trace before execution

For execution-relevant outputs, trace write must complete before downstream execution begins.

### 13.3 Dual-trace rule

Blocked candidate plus safe replacement requires two traces.

### 13.4 Trace storage goal

Trace storage should be append-only or tamper-evident.

---

## 14. Policy and Version Pinning

An implementation should pin evaluation behavior to explicit versions.

Minimum version references:

- policy version;
- engine version.

Stronger implementations may also pin:

- basis code registry version;
- conformance testpack version;
- deployment profile version.

---

## 15. Zone Assignment Guidance

This section should later define practical guidance for assigning:

- `critical`
- `analytical`
- `creative`

This is currently a patch target and should be expanded in a future revision.

---

## 16. Profile and Deployment Mode Guidance

This section should later define practical implementation guidance for:

- `KPT-H`
- `KPT-A`
- `General`
- `High-Assurance`

It should explain:
- when stricter defaults apply;
- where evidence thresholds change;
- where operational controls differ.

---

## 17. Rationale Field Guidance

The rationale field should be:

- concise;
- audit-oriented;
- readable by reviewers;
- non-speculative.

It must not include:
- hidden reasoning;
- chain-of-thought;
- unnecessary narrative detail.

This section should later include allowed and disallowed examples.

---

## 18. Safe Replacement Handling

When an original candidate is blocked:

1. original candidate receives a trace;
2. safe replacement may be generated;
3. replacement is treated as a new candidate output;
4. replacement is separately evaluated;
5. replacement receives its own trace.

The replacement path must not collapse into the original trace.

---

## 19. Human Review and Override

This section should later define:

- when human review is inserted;
- whether reviewers may override display;
- whether reviewers may override execution;
- how overrides are traced;
- how reviewer actions are distinguished from model decisions.

Important:
human review does not erase the original KPT decision record.

---

## 20. Failure Modes and Non-Conformance

This section should later define implementation failures such as:

- execution before trace;
- qualify without `EPI-UNCERTAIN`;
- post-hoc logging instead of trace-before-action;
- safety hit not resulting in `refuse_help`;
- direct model-output-to-tool execution path;
- blocked candidate and replacement sharing one trace.

---

## 21. Minimum Conformance Checklist

A practical implementation checklist should later verify:

- decision assigned before downstream effect;
- enforcement separated from decision state;
- trace written per evaluated candidate output;
- trace-before-execution behavior for execution-relevant outputs;
- safe replacement produces second trace;
- decision invariants hold across all four decision states.

---

## 22. Example Implementation Walkthroughs

This section should later include walkthroughs for:

- ordinary analytical answer;
- execution-relevant qualified answer;
- harmful request refusal;
- insufficient-support refusal;
- blocked candidate plus safe replacement;
- agent tool-call proposal under uncertainty.

---

## 23. Recommended File Relationships

This guide should remain aligned with:

- `docs/core-standard.md`
- `docs/trace-schema.md`
- `docs/basis-codes-registry.md`
- `docs/conformance-methodology.md`
- `docs/reference-middleware-spec.md`
- `docs/reference-middleware-pseudocode.md`
- `schemas/evaluation-payload.schema.json`
- `schemas/decision-result.schema.json`
- `schemas/trace.schema.json`

---

## 24. Non-Goals of This Guide

This guide does not attempt to:

- standardize one programming language;
- prescribe one database;
- prescribe one UI;
- replace product-specific safety design;
- replace legal, compliance, or domain review.

It is an implementation guide for the KPT governance boundary.

---

## 25. Recommended Next Expansions

The next sections to fully write should be:

1. Zone Assignment Guidance
2. Rationale Field Guidance
3. Human Review and Override
4. Example Implementation Walkthroughs
5. Minimum Conformance Checklist

---

## 26. Recommended Repository Path

```text
docs/implementation-guide.md
```
