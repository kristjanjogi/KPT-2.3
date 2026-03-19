# KPT / KPV / VRA Suite Structure

**Author:** Kristjan Jõgi  
**Document date:** 2026-03-08

**Status:** Draft architectural note  
**Purpose:** Clarify the relationship between KPT, KPV, and VRA.

## 1. Core position

KPT 2.3 is the **core decision-governance standard**.

It answers the question:

> What must be true about an AI output before it is allowed to influence or execute?

KPT is therefore the foundation of the suite, not the entire suite.

## 2. KPT

**KPT** governs output admissibility.

It defines:

- zone assignment
- decision states
- basis-code grounding
- decision vs enforcement separation
- output ≠ action
- trace-before-trust requirements
- conformance methodology

KPT is the first public engineering release focus because it is the narrowest high-leverage layer and the most testable starting point.

## 3. KPV

**KPV** is the companion layer for verifiable trace integrity and audit evidence.

It answers the question:

> How is the decision record made durable, tamper-evident, reconstructable, and verifiable?

KPV is not the same thing as KPT decision logic.

In this release, KPT includes only the **minimum KPV footprint** needed to make decision governance testable:

- trace object
- integrity hash
- previous-trace linkage
- append-only / tamper-evident direction
- ordering requirements

Fuller KPV formalization remains deferred.

## 4. VRA

**VRA** is the companion layer for runtime risk appraisal and impact evaluation.

It answers the question:

> How much risk, consequence, or escalation pressure is attached to a governed output or execution path?

VRA is not identical to decision state.

Two outputs can share the same decision state while carrying different operational risk.  
VRA therefore remains architecturally distinct from KPT.

This release does not attempt to fully standardize VRA.

## 5. Why the suite remains modular

The suite is intentionally modular because the three layers answer different questions:

- **KPT** — what is the output's governance status?
- **KPV** — how is that status recorded and verified?
- **VRA** — what risk posture or escalation overlay should apply?

Combining all three into one monolithic first release would expand scope too quickly and weaken clarity.

## 6. Release posture for KPT 2.3

For the first public engineering release:

- **KPT** — included as the primary standard
- **KPV** — included only as a minimum trace-integrity footprint
- **VRA** — deferred as a later companion specification

## 7. Practical reading rule

A useful practical reading rule is:

- KPT decides
- KPV proves
- VRA escalates

## 8. Recommended public positioning

Use this framing in repository and release materials:

- **KPT is the core decision-governance standard**
- **KPV provides the verifiable audit-trace profile for governed outputs**
- **VRA provides the runtime risk-appraisal layer that can inform policy and enforcement strictness**

## 9. Roadmap implication

The current release should prioritize:

1. KPT core standard
2. KPT conformance artifacts
3. minimum KPV-compatible trace structure
4. later companion specs for fuller KPV and VRA formalization