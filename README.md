# KPT 2.3
## AI Output Decision Governance Standard

KPT 2.3 is a runtime decision-governance standard for AI candidate outputs.

It classifies outputs before influence or execution, separates decision state from enforcement action, and requires auditable trace before execution-relevant effect.

This repository is a hybrid public KPT 2.3 repository: it contains the public standard layer together with supporting tests, examples, and selected reference or implementation-oriented materials.

Reading, discussion, and implementation study are public. Official conformance claims, official status claims, certification claims, and controlled KPT name use are governed separately.

Author: Kristjan Jõgi  
Status: Technical checkpoint bundle; core standard at release-candidate maturity, schema-clean canonical outputs verified across included suites

Checkpoint verification in this bundle:
- canonical v0.1: 8/8 passed
- adversarial v0.1b: 6/6 passed
- robustness v0.1c: 8/8 passed

Authority note:
- Markdown and JSON sources are authoritative.
- Archival and convenience materials may exist outside this public repository assembly path.
- The philosophical continuity note for this bundle is `docs/epistemic-humility-axiom.md`.

Conformance note:
- canonical decision and trace outputs in this bundle are validated against the canonical schemas
- see `VERIFICATION_REPORT.md` and `docs/document-authority-map.md`

---

## 1. What KPT is

KPT is a standard for **AI output decision governance**.

Its core purpose is to ensure that an AI-generated candidate output is not treated as equivalent to a real-world action.

KPT inserts a governance boundary between:
- candidate output; and
- downstream influence or execution.

In practical terms, KPT is designed for systems where AI outputs may:
- influence human decisions;
- trigger tools or APIs;
- modify files, records, or workflows;
- create external commitments;
- operate in review, audit, or higher-assurance contexts.

---

## 2. Core claims

KPT 2.3 is built around the following core claims:

- AI output is not action.
- Governed systems operate on representations, not direct reality.
- Every governed output must receive a decision before influence or execution.
- Decision state is not enforcement action.
- Trace before trust.

These claims define KPT as a runtime governance standard, not merely a documentation or moderation pattern.

This is the epistemic humility principle in practice: when grounding is weak, admissibility must dominate confidence.

---

## 3. What KPT does

KPT evaluates a governed **candidate output** before downstream effect.

A conformant KPT-style runtime should:
1. receive a candidate output;
2. determine the governed context;
3. evaluate safety and epistemic sufficiency;
4. assign a decision state;
5. map enforcement action;
6. emit trace;
7. only then allow, qualify, block, or route the output.

This means KPT governs the boundary between **generation** and **effect**.

---

## 4. Decision states

KPT 2.3 defines four decision states:

- `deliver`
- `qualify`
- `refuse_assert`
- `refuse_help`

### High-level meaning

- `deliver` = the candidate output is admissible as delivered
- `qualify` = the candidate output is admissible only with explicit uncertainty or limitation
- `refuse_assert` = the candidate output is not sufficiently supported for assertion
- `refuse_help` = the candidate output is disallowed as assistance

Important distinction:
- `decision_state` = what the output is
- `enforcement_action` = what the system does because of that status

---

## 5. Core governed dimensions

KPT 2.3 uses the following core dimensions.

### Zones
- `critical`
- `analytical`
- `creative`

### Profiles
- `KPT-H`
- `KPT-A`

### Deployment modes
- `General`
- `High-Assurance`

### Locked distinctions
- zone = governed context
- profile = output target context
- deployment_mode = assurance posture
- decision_state = what the output is
- enforcement_action = what the system does because of that status

---

## 6. Trace position

KPT trace is not only a log.

A KPT trace is an auditable governance record for one evaluated candidate output.

The trace layer exists to preserve:
- what was evaluated;
- what governed context applied;
- what decision state was assigned;
- what basis codes supported that decision;
- what enforcement treatment followed;
- what policy and engine version were used;
- whether execution relevance existed;
- whether trace existed before execution.

Locked trace rules include:
- one trace per evaluated candidate output;
- blocked candidate plus replacement = two traces;
- execution-relevant outputs must be traced before execution;
- trace chain should be append-only or tamper-evident.

---

## 7. Repository purpose

This repository is intended to hold the public standard layer of KPT 2.3 and its supporting implementation-oriented artifacts.

It is intended to support:
- standard publication;
- review and discussion;
- conformance work;
- implementation guidance;
- reference middleware design;
- future pilots and governance tooling.

---

## 8. What is in this repository

The repository is structured around several layers.

### A. Core standard layer
Defines the standard itself:
- core concepts
- decision states
- basis-code logic
- trace logic
- conformance expectations

### B. Technical implementation layer
Defines how KPT can be implemented in real systems:
- reference middleware spec
- evaluator pseudocode
- implementation guidance
- technical diagram specification

### C. Schema layer
Defines the normalized objects used by the runtime:
- evaluation payload schema
- decision result schema
- trace schema

### D. Guidance layer
Clarifies areas where vague implementation would weaken the standard:
- zone assignment guidance
- rationale field guidance
- trace stability and replay guidance
- future human review / override guidance

### E. Licensing and control layer
Defines how KPT materials, naming, and conformance claims may be used.

### F. Conformance and test layer
Defines how an implementation can be evaluated against the standard.

---

## 9. Suggested repository structure

~~~text
KPT-2.3/
  README.md
  LICENSE.md
  LICENSING.md
  CONFORMANCE_AND_NAME_USE.md
  docs/
    core-standard.md
    trace-schema.md
    basis-codes-registry.md
    conformance-methodology.md
    suite-structure.md
    weaponized-form-guidance.md
    reference-middleware-spec.md
    reference-middleware-pseudocode.md
    implementation-guide.md
    technical-diagram-spec.md
    zone-assignment-guidance.md
    rationale-field-guidance.md
    trace-stability-and-replay-guidance.md
    evaluation-payload-schema.md
    decision-result-schema.md
    trace-schema-schema.md
  schemas/
    evaluation-payload.schema.json
    decision-result.schema.json
    trace.schema.json
  tests/
    minimum-testpack.yaml
    negative-testpack.yaml
  examples/
    trace-valid-example.json
    trace-invalid-example.json
~~~

This structure reflects both the standard layer and the implementation layer.

---

## 10. Recommended reading order

If you are new to KPT, read in this order.

### Path 1: Quick orientation
1. [README.md](README.md)
2. [docs/core-standard.md](docs/core-standard.md)
3. [docs/quickstart.md](docs/quickstart.md)

### Path 2: Standard-focused read
1. [docs/core-standard.md](docs/core-standard.md)
2. [docs/trace-schema.md](docs/trace-schema.md)
3. [docs/basis-codes-registry.md](docs/basis-codes-registry.md)
4. [docs/conformance-methodology.md](docs/conformance-methodology.md)
5. [tests/minimum-testpack.yaml](tests/minimum-testpack.yaml)

### Path 3: Technical implementation read
1. [docs/reference-middleware-spec.md](docs/reference-middleware-spec.md)
2. [docs/reference-middleware-pseudocode.md](docs/reference-middleware-pseudocode.md)
3. [schemas/evaluation-payload.schema.json](schemas/evaluation-payload.schema.json)
4. [schemas/decision-result.schema.json](schemas/decision-result.schema.json)
5. [schemas/trace.schema.json](schemas/trace.schema.json)
6. [docs/implementation-guide.md](docs/implementation-guide.md)
7. [docs/technical-diagram-spec.md](docs/technical-diagram-spec.md)

### Path 4: Clarification / hardening guidance
1. [docs/zone-assignment-guidance.md](docs/zone-assignment-guidance.md)
2. [docs/rationale-field-guidance.md](docs/rationale-field-guidance.md)
3. [docs/trace-stability-and-replay-guidance.md](docs/trace-stability-and-replay-guidance.md)

---

## 11. Current project status

KPT 2.3 is currently published as a public technical checkpoint.

This repository contains the public standard layer, including core documents, schemas, tests, examples, and selected reference materials.

The core logic is at release-candidate maturity, while some guidance and packaging details may continue to be refined in later updates.

---

## 12. What is already locked in KPT 2.3

The following points should be treated as locked unless explicitly revised.

### Core principles
- decision before influence
- decision before execution
- output != action
- decision_state != enforcement_action
- trace before trust
- weaponized form control

### Basis-code logic
- `qualify` must include `EPI-UNCERTAIN`
- `deliver` must use `EPI-SUFFICIENT` and no limitation or safety codes
- `refuse_assert` must include `EPI-INSUFFICIENT`
- `SAFE-DISALLOWED-HELP` or `WF-WEAPONIZED-FORM` => `refuse_help`
- safety precedence overrides epistemic sufficiency

### Trace logic
- one trace per evaluated candidate output
- blocked candidate plus replacement = two traces
- trace before execution for execution-relevant outputs

---

## 13. Licensing position

KPT 2.3 is currently intended to follow a **controlled-public** model rather than an unrestricted permissive release.

High-level position:
- public visibility: yes
- non-commercial reading and discussion: yes
- automatic commercial exploitation: no
- automatic right to conformance/certification claims: no
- official implementation or official status claims: separately controlled

Repository-level files for this layer:
- `LICENSE.md`
- `LICENSING.md`
- `CONFORMANCE_AND_NAME_USE.md`

---

## 14. Conformance position

KPT is not only a design vocabulary.
It is intended to support conformance assessment.

Conformance work in KPT 2.3 focuses on at least:
- Decision Conformance
- Enforcement Boundary Conformance
- Trace Conformance
- Temporal Conformance

Key principle:

**Observed behavior beats declared behavior.**

An implementation is not conformant merely because it claims to follow KPT.
Its runtime behavior must actually preserve the required ordering and distinctions.

---

## 15. What KPT is not claiming

KPT does not claim to:
- make AI automatically truthful;
- replace domain expertise;
- replace business authorization systems;
- replace legal or compliance review;
- turn schema validity into execution permission;
- reduce governance to logging after the fact.

KPT governs admissibility of outputs before influence or execution.

---

## 16. Immediate next priorities

The current recommended next priorities are:
1. final README alignment;
2. human review and override guidance;
3. trace event family model;
4. repository clean-up and packaging;
5. final ZIP assembly of repository artifacts.

---

## 17. One-line summary

KPT 2.3 is a runtime decision-governance standard that classifies AI candidate outputs before influence or execution, separates decision state from enforcement, and requires auditable trace emission before execution-relevant action.

---

## 18. Author

Kristjan Jõgi
