# Epistemic Humility Axiom

**Author:** Kristjan Jõgi  
**Document date:** 2026-03-11  
**Status:** Informative interpretive note  
**Authority class:** Informative; normative force is carried by `docs/core-standard.md` and `docs/quickstart.md`

## 1. Short form

A KPT-governed system does not possess direct access to reality.
It operates only on representations: user input, retrieved artifacts, stored context, symbolic transformations, and model-mediated interpretations.
Those representations may be incomplete, outdated, inconsistent, misleading, adversarial, or false.
This applies not only to machine-generated material, but also to human-provided input.

Therefore, a governed system must not convert insufficiently grounded uncertainty into assertive output.
When truth conditions are not adequately supported, admissibility must dominate confidence.
Under KPT, that means the system should qualify, refuse unsupported assertion, or refuse harmful assistance as appropriate.

## 2. Why this matters in KPT

KPT is not built on the assumption that a model can simply "know" enough if it sounds fluent enough.
KPT begins from a stricter premise:

- outputs can influence belief, reliance, and action;
- influence without grounding creates bluffing risk;
- bluffing risk is a governance problem, not just a style problem.

That is why KPT separates:

- candidate output from real-world action;
- decision state from enforcement action;
- trace from post-hoc trust.

## 3. Operational consequence

This axiom is operationalized through the KPT decision states:

- `deliver` when the output is admissible as given;
- `qualify` when limitations, uncertainty, or missing grounding must remain visible;
- `refuse_assert` when the candidate would overstate what the support can bear;
- `refuse_help` when the candidate itself is harmful, disallowed, or weaponized.

The axiom therefore does not remain philosophical background.
It is a runtime requirement at the point where language can become influence or action.

## 4. Relationship to the origin story

The direct philosophical source for this note is the KPT 2.2.2 origin story, preserved in:

- `origin/current/KPT_2_2_2_origin_story_ET_2026-02-25.pdf`
- `origin/current/KPT_origin_to_standard_bridge_2026-03-11.md`

The origin story states the problem in broader epistemological language.
KPT 2.3 expresses the same intuition as a governance contract: when access to truth is limited, the system must not simulate certainty.

## 5. What this axiom does not say

This axiom does **not** require silence whenever uncertainty exists.
KPT still allows useful output under uncertainty, but only when the uncertainty is made explicit and the output remains admissible.

It also does **not** claim that humans have privileged direct access to reality.
The axiom is symmetrical: both human and model participants operate through representations and interpretation.
