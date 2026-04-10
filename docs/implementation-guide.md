# KPT 2.3 Implementation Guide

## Public Reference Guide v0.2

**Author:** Kristjan Jõgi  
**Status:** Public reference guide  
**Applies to:** KPT 2.3

---

## 1. Purpose

This guide explains how KPT 2.3 can be operationalized as a runtime decision-governance layer around AI systems.

It is intended for teams building systems where AI outputs may:
- influence decisions
- trigger external actions
- be displayed in governed contexts
- or be routed into tools, APIs, files, or workflows

This guide is a **public implementation reference**.

It is **not** a full runtime-core disclosure.

---

## 2. What KPT is and is not

### 2.1 What KPT is

KPT is a decision-governance layer that sits between candidate output and downstream effect.

It ensures that:
- governed outputs are evaluated before influence or execution
- each evaluated candidate output receives a decision state
- decision state is recorded independently from enforcement
- execution-relevant outputs are traced before execution

### 2.2 What KPT is not

KPT is not:
- the model
- the retrieval system
- the business workflow engine
- a generic moderation filter
- a logging layer added after the fact
- a guarantee of truth

---

## 3. Core implementation principle

### 3.1 Output is not action

In implementation terms, generated content must be treated as a candidate object with no execution authority by default.

That means:
- a model response is not yet an action
- a tool proposal is not yet permission
- structured output is not yet committed system state
- candidate output must first pass through KPT evaluation

### 3.2 Decision before effect

A system implementing KPT must not allow:
- direct execution from raw model output
- display of governed output before decision assignment where policy requires governance
- post-hoc trace creation for execution-relevant outputs

---

## 4. When to use KPT

KPT is most useful when outputs may affect real-world decisions or actions.

Typical use cases include:
- assistants that propose actions
- agents that call tools
- systems that generate operational recommendations
- systems that produce regulated or high-stakes guidance
- governance middleware for enterprise AI workflows
- human-in-the-loop review systems

KPT is less important for purely decorative or low-risk creative output, though the standard may still apply depending on deployment goals.

---

## 5. Minimum components

A public reference implementation will usually include:
- candidate output normalizer
- context resolver
- safety evaluator
- epistemic evaluator
- decision resolver
- enforcement mapper
- trace emitter
- execution gate

A stronger internal implementation may also include:
- policy registry
- version pinning
- trace chain verification
- replacement-output loop
- reviewer override layer
- conformance testing harness

---

## 6. Required inputs

A minimal implementation should be able to ingest a normalized evaluation object containing at least:
- input reference
- output reference
- candidate output content
- content type
- zone
- profile
- deployment mode
- execution relevance
- provenance / verification state
- policy version
- engine version

Reference artifact:
- `schemas/evaluation-payload.schema.json`

---

## 7. Required outputs

A minimal implementation should be able to produce:
- decision result object
- enforcement mapping
- trace object

Reference artifacts:
- `schemas/decision-result.schema.json`
- `schemas/trace.schema.json`

---

## 8. Deployment patterns

### 8.1 Inline middleware
KPT runs directly in the live request path.

Best for:
- immediate tool control
- strong execution gating
- synchronous assistant flows

### 8.2 Sidecar governance service
KPT runs as a separate service called by one or more applications.

Best for:
- centralized governance
- multi-product environments
- consistent tracing

### 8.3 Embedded library
KPT logic is packaged directly into application code.

Best for:
- prototypes
- demos
- early pilots

---

## 9. End-to-end runtime flow

A conformant implementation should follow this high-level order:

1. receive upstream input
2. build application context
3. generate candidate output
4. normalize candidate for governance
5. resolve governed context
6. determine execution relevance
7. evaluate safety
8. evaluate epistemic sufficiency
9. assign decision state
10. derive qualification type if needed
11. map enforcement action
12. emit trace
13. permit or block display and/or execution
14. optionally generate and re-evaluate safe replacement

This ordering is central to KPT.

---

## 10. Locked implementation rules

The implementation must support:
- `deliver`
- `qualify`
- `refuse_assert`
- `refuse_help`

It must also preserve these core rules:
- `qualify` includes `EPI-UNCERTAIN`
- `deliver` includes `EPI-SUFFICIENT` and no limitation or safety codes
- `refuse_assert` includes `EPI-INSUFFICIENT`
- `SAFE-DISALLOWED-HELP` or `WF-WEAPONIZED-FORM` => `refuse_help`
- safety precedence overrides epistemic sufficiency

Qualification handling should derive `qualification_type` from supporting limitation families.

---

## 11. Enforcement boundary

A conformant implementation must keep decision and enforcement separate.

### 11.1 Decision state
Decision state describes what the output is.

### 11.2 Enforcement action
Enforcement describes what the runtime does because of that status.

### 11.3 Minimum mappings
- `deliver` -> display allowed; execution may be allowed
- `qualify` -> display with qualification; execution blocked if execution-relevant
- `refuse_assert` -> original blocked; execution blocked
- `refuse_help` -> original blocked; execution blocked

---

## 12. Trace boundary

Every evaluated candidate output must produce its own trace.

For execution-relevant outputs:
- trace write must complete before downstream execution begins

If an original candidate is blocked and a safe replacement is produced:
1. original candidate receives a trace
2. replacement is treated as a new candidate output
3. replacement is separately evaluated
4. replacement receives its own trace

The replacement path must not collapse into the original trace.

Trace storage should be append-only or tamper-evident.

---

## 13. Policy and version pinning

An implementation should pin evaluation behavior to explicit versions.

Minimum version references:
- policy version
- engine version

Stronger implementations may also pin:
- basis code registry version
- conformance testpack version
- deployment profile version

---

## 14. Boundary note

This guide explains how to operationalize the public KPT contract.

It does not claim to disclose every internal runtime component, every internal proof surface, or every private implementation detail.
