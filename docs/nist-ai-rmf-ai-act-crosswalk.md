# NIST AI RMF + EU AI Act Crosswalk
## Operational crosswalk for KPT 2.3

Author: Kristjan Jõgi  
Status: Public working crosswalk for the KPT 2.3 standard surface  
Applies to: KPT 2.3 public standard layer

## 1. Purpose

This document provides an operational crosswalk between:

- the NIST AI Risk Management Framework (AI RMF); and
- the EU AI Act control families.

Its purpose is not to claim that KPT 2.3 replaces either framework.

Its purpose is to help readers understand where KPT 2.3 fits:

- as a runtime decision-governance standard;
- as an admissibility and trace layer;
- as a boundary control between candidate output and downstream influence or execution.

## 2. Important scope note

This is not legal advice.

This is not a one-to-one article-by-article legal compliance matrix.

It is an implementation-oriented crosswalk that maps:

- NIST AI RMF functions and control themes;
- EU AI Act control families and legal obligations; and
- the parts of that landscape where KPT 2.3 most naturally applies.

## 3. Why this crosswalk exists

KPT 2.3 is not intended to be a general-purpose replacement for:

- enterprise AI governance programs;
- broad risk management frameworks;
- legal compliance functions;
- model provider obligations; or
- business authorization systems.

KPT 2.3 is strongest when used as a narrower layer for:

- runtime admissibility classification;
- decision-state assignment before downstream effect;
- explicit separation between decision state and enforcement action; and
- auditable trace before execution-relevant commitment.

## 4. Timing and applicability note

As of 20 March 2026:

- the EU AI Act entered into force on 1 August 2024;
- prohibited AI practices and AI literacy obligations apply from 2 February 2025;
- governance rules and general-purpose AI model obligations apply from 2 August 2025;
- most high-risk AI system obligations apply from 2 August 2026; and
- certain high-risk AI systems embedded in regulated products have a longer transition period until 2 August 2027.

The NIST AI RMF is a voluntary risk-management framework organized around four functions:

- Govern
- Map
- Measure
- Manage

## 5. How to read this crosswalk

The practical reading model is:

- NIST AI RMF gives a broad risk-management structure;
- the EU AI Act gives legal control families and obligations;
- KPT 2.3 fits most naturally where systems need:
  - candidate-output classification,
  - admissibility decisions,
  - traceability,
  - execution-boundary control,
  - and human-oversight-compatible routing.

## 6. Unified control-family crosswalk

### 6.1 Governance and accountability

**NIST AI RMF**
- Govern

**EU AI Act**
- governance structure
- role-based obligations
- AI literacy
- post-market responsibility logic

**Operational control family**
- named owners
- approval and escalation paths
- accountability records
- AI literacy practices
- role separation for design, deployment, review, and incident handling

**KPT fit**
- partial and supportive

**How KPT contributes**
- defines a runtime decision boundary
- makes decision-state classification explicit
- creates trace records that support accountability reviews
- supports later audit and monitoring

**What KPT does not replace**
- enterprise governance program
- legal accountability framework
- management ownership structure

---

### 6.2 Use-case scoping and risk classification

**NIST AI RMF**
- Map
- Govern

**EU AI Act**
- prohibited practice screening
- high-risk classification
- transparency cases
- GPAI applicability assessment

**Operational control family**
- identify intended purpose
- classify the use case
- identify whether the system influences decisions or triggers execution
- determine whether the use case is prohibited, high-risk, transparency-relevant, GPAI-relevant, or outside those categories

**KPT fit**
- partial and strong at runtime boundary scoping

**How KPT contributes**
- forces explicit classification of governed candidate outputs
- helps distinguish display-only from execution-relevant paths
- helps separate low-risk handling from critical handling

**What KPT does not replace**
- full legal scope determination under the AI Act

---

### 6.3 Risk management lifecycle

**NIST AI RMF**
- Govern
- Map
- Measure
- Manage

**EU AI Act**
- risk management system for high-risk AI systems

**Operational control family**
- identify harms
- assess severity and likelihood
- define mitigations
- define residual-risk acceptance
- review changes over time

**KPT fit**
- partial and supportive

**How KPT contributes**
- provides a structured output-level decision layer
- helps convert epistemic insufficiency and safety concerns into explicit runtime states
- improves consistency in downstream treatment of risky outputs

**What KPT does not replace**
- full lifecycle risk management program
- enterprise risk register
- product safety case

---

### 6.4 Data and data governance

**NIST AI RMF**
- Map
- Measure

**EU AI Act**
- data and data governance requirements for high-risk AI systems

**Operational control family**
- provenance of data
- dataset relevance and quality
- representational limitations
- bias and coverage review
- alignment with privacy and data-governance requirements

**KPT fit**
- limited and indirect

**How KPT contributes**
- can reflect weak grounding or insufficient basis at output time
- can require qualification or refusal where support is insufficient

**What KPT does not replace**
- dataset governance
- data-quality engineering
- privacy compliance
- training data controls

---

### 6.5 Technical documentation, record-keeping, and traceability

**NIST AI RMF**
- Govern
- Measure
- Manage

**EU AI Act**
- technical documentation
- record-keeping
- information needed for traceability and review

**Operational control family**
- documented system design
- decision evidence
- versioning
- log retention
- traceability across model, policy, workflow, and deployment state

**KPT fit**
- strong

**How KPT contributes**
- one trace per evaluated candidate output
- explicit decision state
- basis codes
- enforcement treatment linkage
- policy version and engine version support
- clear distinction between blocked candidate and replacement candidate

**What KPT does not replace**
- complete technical file for AI Act conformity work
- product dossier management

---

### 6.6 Transparency and provision of information

**NIST AI RMF**
- Govern
- Map

**EU AI Act**
- transparency obligations
- information provided to deployers and users
- operational limitations and intended purpose communication

**Operational control family**
- describe intended use
- disclose relevant limitations
- communicate required review conditions
- provide instructions for safe deployment or interpretation

**KPT fit**
- moderate

**How KPT contributes**
- gives structured output states such as deliver, qualify, refuse_assert, and refuse_help
- supports explicit uncertainty and limitation signaling
- improves consistency in qualified output handling

**What KPT does not replace**
- all user-facing transparency obligations
- all disclosure and documentation obligations under law

---

### 6.7 Human oversight

**NIST AI RMF**
- Govern
- Manage

**EU AI Act**
- human oversight requirements for high-risk AI systems

**Operational control family**
- define human review points
- define override authority
- define escalation paths
- define when systems may not pass directly into execution

**KPT fit**
- strong

**How KPT contributes**
- formalizes decision before influence
- formalizes decision before execution
- separates decision state from enforcement action
- supports routing into review or qualified display instead of direct execution

**What KPT does not replace**
- staffing, training, or operational oversight design as a whole

---

### 6.8 Accuracy, robustness, safety, and cybersecurity

**NIST AI RMF**
- Measure
- Manage

**EU AI Act**
- robustness
- accuracy
- cybersecurity

**Operational control family**
- benchmark expected performance
- test misuse and abuse cases
- assess security of execution-relevant paths
- evaluate resilience to manipulation and failure

**KPT fit**
- partial

**How KPT contributes**
- can prevent weakly supported candidate outputs from moving into effect
- can support refusal or qualification in safety-relevant contexts
- can support runtime boundary discipline for execution-relevant systems

**What KPT does not replace**
- model evaluation suite
- cybersecurity engineering
- adversarial testing program
- robustness certification work

---

### 6.9 Post-market monitoring and incident response

**NIST AI RMF**
- Measure
- Manage

**EU AI Act**
- post-market monitoring
- incident handling
- corrective action logic

**Operational control family**
- production monitoring
- incident intake
- rollback and containment
- corrective action tracking
- periodic review of drift and misuse

**KPT fit**
- strong as evidence support, not as full monitoring platform

**How KPT contributes**
- trace records support incident reconstruction
- explicit decision states support downstream analysis
- execution-boundary traces can support post-incident review

**What KPT does not replace**
- monitoring platform
- incident response playbooks
- formal reporting duties

---

### 6.10 Prohibited practices and AI literacy

**NIST AI RMF**
- Govern

**EU AI Act**
- prohibited AI practices
- AI literacy obligations

**Operational control family**
- screen out disallowed uses
- train staff on system capabilities and limits
- define escalation when a use case is disallowed or unclear

**KPT fit**
- moderate

**How KPT contributes**
- can help operationalize runtime refusal states
- supports explicit refusal paths for disallowed assistance
- supports trace for disallowed or blocked outputs

**What KPT does not replace**
- legal screening for prohibited practices
- organization-wide literacy program

---

### 6.11 General-purpose AI provider obligations

**NIST AI RMF**
- Govern
- Map
- Manage

**EU AI Act**
- GPAI obligations
- systemic-risk GPAI obligations where applicable

**Operational control family**
- provider documentation
- transparency and copyright compliance
- safety and security obligations for systemic-risk models

**KPT fit**
- usually indirect

**How KPT contributes**
- KPT may be used downstream by deployers or integrators
- KPT can complement, but not replace, provider obligations

**What KPT does not replace**
- GPAI provider compliance program
- model-provider obligations under the AI Act

## 7. KPT-specific fit summary

KPT 2.3 is strongest in the following crosswalk zones:

- runtime admissibility classification
- decision-state assignment before downstream effect
- traceability at candidate-output level
- execution-boundary discipline
- human-oversight-compatible routing
- support for post-incident review through structured trace

KPT 2.3 is weaker, or intentionally not a replacement, in the following zones:

- full enterprise AI governance
- full legal classification under the EU AI Act
- full data governance and privacy programs
- provider-side GPAI obligations
- broad model evaluation and cybersecurity programs
- complete conformity-assessment or certification operations

## 8. Practical implementation reading

A practical way to use this crosswalk is:

1. Use the EU AI Act to determine the legal class of the system or use case.
2. Use NIST AI RMF to structure organizational governance, risk mapping, measurement, and management.
3. Use KPT 2.3 where candidate outputs need runtime admissibility decisions before they influence humans or trigger execution.
4. Use KPT trace and decision-state structure as a supporting control for documentation, oversight, and post-market review.

## 9. Non-claims

This document does not claim that:

- KPT 2.3 alone satisfies the EU AI Act;
- KPT 2.3 alone satisfies NIST AI RMF;
- KPT 2.3 is a substitute for legal review;
- KPT 2.3 is a substitute for full risk management;
- KPT 2.3 is a substitute for provider obligations, product safety work, or certification.

This document claims only that KPT 2.3 can be mapped coherently into the broader control landscape and is especially well suited to the runtime admissibility and trace boundary between candidate output and downstream effect.

## 10. Sources

Official sources used for this crosswalk:

- NIST AI Risk Management Framework overview:
  https://www.nist.gov/itl/ai-risk-management-framework

- NIST AI RMF Core and Playbook resources:
  https://airc.nist.gov/airmf-resources/airmf/
  https://airc.nist.gov/airmf-resources/playbook/
  https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook

- NIST AI RMF 1.0 publication:
  https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf

- EU AI Act overview and timeline:
  https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
  https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act
  https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers

- Official EU legal text:
  https://eur-lex.europa.eu/legal-content/FR-EN/TXT/?uri=CELEX:32024R1689
