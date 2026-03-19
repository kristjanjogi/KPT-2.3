# Weaponized Form Guidance

**Author:** Kristjan Jõgi  
**Document date:** 2026-03-08

**Status:** Companion guidance note  
**Purpose:** Provide high-level implementation guidance and test families for weaponized-form control without changing the core normative standard.

## 1. Scope

This document does not redefine the core standard.

It provides implementation-facing guidance for recognizing when a candidate output crosses from merely discussing a topic into a materially operationalized form that must be governed under `refuse_help`.

## 2. Practical heuristic categories

The following patterns are strong signals of weaponized form when they materially advance a disallowed objective:

- **operationalization** — content is structured for direct use rather than general explanation
- **stepwise conversion** — content is turned into ordered actions, procedure, workflow, or deployment sequence
- **optimization for harm** — content is framed to improve effectiveness, scale, reach, targeting, or persuasion for harmful purposes
- **mobilization support** — content assists organizing, coordinating, escalating, or enabling harmful intergroup action
- **execution adjacency** — content can be passed directly into tools, agents, or operational processes

No single heuristic is sufficient in every case. The governing question is whether the candidate output is materially operationalized in a harmful or disallowed direction.

## 3. Reframing is not neutralization

The following framings do not, by themselves, neutralize weaponized form:

- "for analysis"
- "for education"
- "for strategy"
- "for awareness"
- "for historical realism"

If the resulting output remains practically usable for disallowed help, the correct decision remains `refuse_help`.

## 4. Topic sensitivity is not enough

Sensitive subject matter alone is not weaponized form.

For example, neutral historical analysis of religious or ethnic conflict is not automatically disallowed.

The relevant boundary is practical operationalization, not topic labels alone.

## 5. Recommended test families

Implementations should include canonical tests for:

- explicit incitement against a protected group
- hostility optimization framed as messaging strategy
- operational preparation of one group against another
- propaganda copy intended to legitimize violence
- benign historical or analytical treatment of the same topic
- unsupported allegations about protected groups presented as fact
- blocked-output replacement behavior

These families are reflected in the positive and negative fixture packs.

## 6. Governance rule of thumb

A useful rule of thumb is:

> If the output becomes more directly usable for harmful execution, coordination, targeting, or escalation, governance should become stricter, not looser.

## 7. Implementation note

A robust implementation should not rely on a single keyword detector. It should evaluate:

- the structure of the output
- the intended use implied by the request and runtime context
- execution relevance
- whether the content becomes materially more actionable than neutral analysis

## 8. Conformance note

The core standard remains normative. This guidance exists to help implementations, test designers, and reviewers apply the standard consistently.