# KPT 2.3 Final Technical Diagram Specification
## Technical Decision Flow Diagram Spec v1.0

Author: Kristjan Jõgi  
Status: Draft  
Applies to: KPT 2.3

---

## 1. Purpose

This document defines the final technical diagram specification for KPT 2.3.

The diagram is intended to show, in one view, how KPT governs AI candidate outputs from generation through decisioning, enforcement, tracing, and optional execution.

The diagram must make the following points visually unambiguous:

- output is not action;
- candidate output must pass through KPT before influence or execution;
- decision state and enforcement action are distinct;
- trace is emitted before execution-relevant commit;
- blocked candidate and safe replacement are separate evaluation objects;
- qualified execution-relevant outputs do not execute.

---

## 2. Diagram Goal

The final diagram should communicate the runtime governance architecture of KPT 2.3 to a technical reader in a single page.

It should be understandable to:

- technical founders;
- architects;
- governance engineers;
- investors with technical interest;
- implementation partners.

It should not look like a generic AI workflow image.
It should clearly show a control boundary.

---

## 3. Diagram Title

Recommended title:

**KPT 2.3 Runtime Decision Governance Flow**

Alternative acceptable title:

**KPT 2.3 Technical Decision Flow: Candidate Output, Decision, Enforcement, Trace, Execution**

---

## 4. Core Visual Thesis

The visual thesis of the diagram is:

**Model output has no execution authority until KPT assigns a decision, maps enforcement, and emits trace.**

This must be the central visual message.

---

## 5. Required Layout

Use a left-to-right primary flow.

### Recommended lane order

1. Input / Application Preparation
2. Generation Layer
3. KPT Governance Layer
4. Enforcement Layer
5. Display / Execution Targets
6. Trace Chain / Audit Layer

The KPT Governance Layer must be visually central and larger than the surrounding layers.

---

## 6. Required Top-Level Blocks

The diagram must contain the following top-level blocks.

### 6.1 Input Block

Label:

**User / Event / Upstream Request**

Purpose:
Represents the originating prompt, event, or system input.

### 6.2 Context Builder Block

Label:

**Application Context Builder**

Purpose:
Represents application-side context assembly before generation.

### 6.3 Model / Agent Block

Label:

**Model / Agent Runtime**

Purpose:
Represents the generator that produces the candidate output.

### 6.4 Candidate Output Block

Label:

**Candidate Output**

Subtitle or note:
`text | json | tool_call | mixed`

Purpose:
Represents the generated object before governance decision.

This block must be visually separated from execution targets to reinforce:
**candidate output != action**

### 6.5 KPT Governance Boundary Block

Label:

**KPT Middleware / Governance Boundary**

This is the most important block in the entire diagram.

It should contain internal sub-blocks.

Required internal sub-blocks:

- Normalizer
- Context Resolver
- Safety Evaluator
- Epistemic Evaluator
- Decision Resolver
- Enforcement Mapper
- Trace Emitter
- Policy Loader

This block should visually indicate that it is the decision boundary between model output and downstream effect.

### 6.6 Enforcement Layer Block

Label:

**Enforcement Layer**

Purpose:
Represents runtime consequences of KPT decision results.

Required outcomes:
- allow display
- allow display with qualification
- block original
- allow execution
- block execution

### 6.7 Output / Runtime Target Blocks

At minimum include:

- **User Display**
- **Tool / API / File / Workflow Execution**

These should be separated into distinct target blocks to show that display and execution are different downstream outcomes.

### 6.8 Trace Layer Block

Label:

**Append-Only / Tamper-Evident Trace Chain**

Purpose:
Represents trace persistence and auditability.

It should be visually positioned below or alongside the KPT governance layer, with a clear arrow from Trace Emitter to Trace Chain.

---

## 7. Required Internal Flow Inside KPT Block

Inside the KPT Governance Boundary, the sub-flow should be shown in this order:

1. Normalizer
2. Context Resolver
3. Execution Relevance Determination
4. Safety Evaluator
5. Epistemic Evaluator
6. Decision Resolver
7. Qualification Type Derivation
8. Enforcement Mapper
9. Trace Emitter

The order matters.

The diagram does not need to show every minor rule, but the ordering must imply:

- safety precedence;
- epistemic evaluation after safety checks;
- trace emission after decision and enforcement mapping;
- trace emission before execution.

---

## 8. Decision State Node

The diagram must include a distinct decision node showing the four KPT decision states:

- `deliver`
- `qualify`
- `refuse_assert`
- `refuse_help`

This may be shown as:
- a vertical list;
- a diamond split;
- or a decision panel inside the KPT block.

The decision-state node must visually connect to:
- enforcement mapping;
- trace emission.

Important:
Do not draw decision state as if it directly executes actions.
Decision state must feed enforcement, not replace it.

---

## 9. Enforcement Mapping Node

The diagram must visually show that enforcement action is downstream of decision state.

Recommended mini-mapping:

- `deliver` -> allow display; execution may be allowed
- `qualify` -> allow with qualification; execution blocked
- `refuse_assert` -> block original; execution blocked
- `refuse_help` -> block original; execution blocked

This can be shown either:
- inside the Enforcement Layer; or
- as a mapping table between Decision Resolver and Enforcement Layer.

The distinction must remain visually clear:
- decision = classification
- enforcement = runtime treatment

---

## 10. Trace Timing Rule

This must be explicitly shown in the diagram.

Required note near trace flow:

**Trace written before execution-relevant commit**

A visual lock, gate, or sequencing marker is strongly recommended between:
- Trace Emitter
- Execution Target

The viewer should immediately understand that execution cannot happen first.

---

## 11. Execution Gate

The diagram must include an explicit runtime gate before execution targets.

Label:

**Execution Gate**

Purpose:
Shows that downstream tool/API/file/workflow execution occurs only if:
- enforcement permits execution;
- trace has already been emitted.

This block is critical because it distinguishes KPT from surface-level moderation.

---

## 12. Safe Replacement Loop

The diagram must show an optional secondary path for safe replacement.

Required path:

1. candidate output receives `refuse_assert` or `refuse_help`
2. system generates safe replacement candidate
3. replacement returns to Candidate Output or directly back into KPT evaluation
4. replacement is separately evaluated
5. replacement receives its own trace

Required annotation:

**Blocked candidate + replacement = two traces**

This should not dominate the diagram, but it must be visible.

---

## 13. Required Named Fields or Callouts

The diagram should include concise callouts for these KPT-specific ideas:

### Callout A
**Output != Action**

### Callout B
**Decision before influence**

### Callout C
**Decision before execution**

### Callout D
**Decision state != enforcement action**

### Callout E
**Trace before trust**

### Callout F
**Execution-relevant qualify does not execute**

Not all callouts must be large.
Some may be placed as side notes.

---

## 14. Required Artifacts Referenced by Diagram

The diagram should be consistent with the following existing artifacts:

- `docs/reference-middleware-spec.md`
- `docs/reference-middleware-pseudocode.md`
- `schemas/evaluation-payload.schema.json`
- `schemas/decision-result.schema.json`
- `schemas/trace.schema.json`

The diagram should not introduce contradictory logic.

---

## 15. Visual Hierarchy

The visual hierarchy should emphasize:

### Highest emphasis
- KPT Governance Boundary
- Decision State
- Execution Gate
- Trace Chain

### Medium emphasis
- Candidate Output
- Enforcement Layer

### Lower emphasis
- Input
- Context Builder
- Model / Agent

This matters because the value of KPT is not “model in, answer out.”
The value is the governance boundary.

---

## 16. Recommended Color Logic

The exact palette is flexible, but the visual semantics should be stable.

Recommended semantics:

- neutral color for input, context, and model blocks
- highlighted color for KPT Governance Boundary
- distinct caution color for `qualify`
- distinct block color for `refuse_assert` and `refuse_help`
- stable audit color for trace chain
- neutral/positive flow color for allowed paths

Do not rely only on color.
Arrows, labels, and gate markers must also communicate the meaning.

---

## 17. Arrow Rules

Use arrows deliberately.

### Required arrow meanings

- solid forward arrows for primary runtime flow
- gated arrow into execution target
- feedback loop arrow for safe replacement
- side arrow from Trace Emitter to Trace Chain
- no direct arrow from Candidate Output to Execution Target

This last rule is mandatory.

The absence of a direct candidate-to-execution arrow is one of the most important visual claims.

---

## 18. Minimum Diagram Content

At minimum, the final diagram must show:

- input
- context builder
- model/agent
- candidate output
- KPT block with internal evaluators
- decision states
- enforcement layer
- execution gate
- user display target
- execution target
- trace emitter
- append-only trace chain
- safe replacement loop

If any of these are missing, the diagram is incomplete.

---

## 19. Suggested Diagram Structure

Recommended structure in text form:

```text
User / Event / Upstream Request
  -> Application Context Builder
  -> Model / Agent Runtime
  -> Candidate Output
  -> KPT Middleware / Governance Boundary
       -> Normalizer
       -> Context Resolver
       -> Execution Relevance Determination
       -> Safety Evaluator
       -> Epistemic Evaluator
       -> Decision Resolver
       -> Qualification Type Derivation
       -> Enforcement Mapper
       -> Trace Emitter
  -> Enforcement Layer
       -> User Display
       -> Execution Gate
            -> Tool / API / File / Workflow Execution

Trace Emitter
  -> Append-Only / Tamper-Evident Trace Chain

Blocked candidate
  -> Safe Replacement Candidate
  -> Re-enter KPT evaluation
  -> Second trace
```

---

## 20. Explicit Visual Non-Goals

The final diagram should not:

- look like a generic LLM application diagram;
- imply that moderation alone is the mechanism;
- imply that trace is written after execution;
- imply that decision state is the same as enforcement action;
- imply that qualified outputs may execute;
- imply that blocked candidate and replacement share one trace;
- overcomplicate the visual with too many code-level details.

---

## 21. Diagram Caption

Recommended caption under the figure:

**KPT 2.3 inserts a governance boundary between candidate output and downstream effect. Every governed output is classified before influence or execution, linked to an auditable trace, and only then allowed, qualified, blocked, or routed to safe replacement.**

---

## 22. Companion Short Version for README or Deck

If a shorter summary is needed next to the diagram:

**KPT 2.3 governs the point between AI output and real-world effect. Candidate outputs do not execute directly. They are evaluated, assigned a decision state, mapped to enforcement, and traced before any execution-relevant commit.**

---

## 23. Recommended Repository Path

```text
docs/appendix/technical-diagram-spec.md
```

---

## 24. Recommended Next Use

This specification can now be used to create:

- a clean technical architecture figure for the repo;
- an investor-safe technical system visual;
- a slide version for advisory or pilot conversations;
- a future implementation diagram aligned to KPT middleware behavior.
