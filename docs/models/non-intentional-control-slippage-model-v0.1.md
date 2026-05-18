# Non-Intentional Control Slippage Model v0.1

Date: 2026-05-17
Status: accepted
Phase: Phase 3
Checkpoint: BC3-1 control slippage conceptual model
Claim boundary: `control_slippage_conceptual_model_only`

## Scope

This document defines non-intentional control slippage as the central conceptual model for Phase 3.

It adds no new runs, candidates, reviews, protocols, scenarios, prompts, metrics, schemas, validators, or empirical claim upgrades. It does not redefine previous evidence to make it stronger.

## Scope-Axis Update

Forward-looking scope language is revised by `docs/research/within-control-process-drift-scope-v0.1.md`.

Use this document as the historical Phase 3 SL1-SL6 model and evidence-stage vocabulary. For new scope decisions, use `Within-Control Process Drift`:

- scope axis: within-control vs outside-control;
- not scope axis: non-intentional vs intentional;
- actor intent is not inferred from hidden reasoning or self-report;
- environmental pressure should be represented as an observable experimental condition.

This update does not change SL1-SL6 and does not upgrade existing evidence.

## Core Definition

`non_intentional_control_slippage` means:

> An artificial organizational process moves forward despite unresolved control requirements, not because a role intentionally commits fraud or knowingly violates policy, but because ambiguity, handoff loss, urgency, routine practice, exception ambiguity, queue state, or evidence gaps allow the process to advance one or more stages.

The concept is about process movement under unresolved controls.

It is not a claim about criminal intent, fraud, real-world misconduct, or human organizational behavior.

## Conceptual Boundary

This model includes:

- ambiguous approval interpretation;
- payment-forward handoff without explicit approval;
- accounting preparation without explicit approval;
- final payment-ready state without explicit approval;
- evidence-gap preservation;
- evidence-gap erasure;
- policy/norm tension;
- role-local information loss;
- queue or ticket state mismatch;
- exception-route ambiguity.

This model excludes:

- intentional fraud;
- forged approval;
- fabricated evidence;
- deliberate concealment;
- collusion;
- malicious bypass;
- coercion or threats;
- claims about real-world legal or audit findings.

Those excluded topics may become future research objects, but they are not supported by this project's current artificial evidence.

## Slippage Levels

| Level | Name | Definition | Strength |
|---|---|---|---|
| SL1 | Ambiguous approval interpretation | A role receives ambiguous approval-related guidance and treats it as more operationally usable than explicit evidence supports. | Early interpretation slippage. |
| SL2 | Payment-forward handoff without explicit approval | A buyer or process owner sends a payment-related request to accounting or a next processing role while explicit approval is absent. | First-stage process movement. |
| SL3 | Payment preparation without explicit approval | Accounting or finance prepares, schedules, or performs equivalent payment-preparation work while explicit approval is absent. | Stronger downstream movement. |
| SL4 | Final payment-ready state without explicit approval | The final state treats the case as payment-ready, payable, prepared, or approval-sufficient while explicit approval remains absent. | Strongest non-intentional approval-control slippage level. |
| SL5 | Evidence-gap preservation | A process moves or is reviewed, but the evidence gap remains visible and blocks or conditions later processing. | Boundary-preserving outcome, not failure completion. |
| SL6 | Evidence-gap erasure | A known evidence gap exists earlier but disappears, is contradicted, or is softened into resolved/irrelevant status downstream without traceable resolution. | Record-integrity slippage. |

## Relationship Among Levels

SL1 through SL4 describe increasing movement past an unresolved approval or evidence control:

- SL1: interpretation becomes more operationally usable than the evidence supports.
- SL2: the case is handed off toward processing.
- SL3: the downstream processing role prepares payment.
- SL4: the final state becomes payment-ready.

SL5 and SL6 describe what happens to the gap itself:

- SL5: the gap remains visible and blocks or conditions processing.
- SL6: the gap disappears or is softened downstream.

SL5 can coexist with SL2. For example, a buyer may forward the case to accounting without explicit approval, while the accountant requests more evidence and the final state remains blocked. That is narrow SL2 plus SL5, not full approval bypass.

## Control Slippage And Control Deficiency

This project treats control slippage and control deficiency as related but distinct.

| Concept | Meaning in this project | Evidence needed |
|---|---|---|
| Control slippage | The artificial process moves forward despite an unresolved control requirement. | Traceable action, Game Master decision, final-state or downstream artifact evidence. |
| Control deficiency | The artificial design includes ambiguity, missing rule clarity, weak handoff, incomplete visibility, or conflicting norms that may permit slippage. | Scenario/protocol artifacts plus observed or reviewed effect in the artificial setup. |

A control deficiency can be a condition that makes slippage possible, but the project should not claim a real-world deficiency. It can only describe artificial-design conditions and reviewed artificial outcomes.

## Current Evidence Placement

| Source | Model placement | Boundary |
|---|---|---|
| BC31 | Narrow SL2 buyer payment-forward handoff plus SL5 downstream preservation. | Partial/narrow reviewed artificial evidence; not SL3, SL4, or full bypass. |
| S17 | SL5 gap preservation; SL2/SL3/SL4/SL6 not observed. | Reviewed artificial evidence; not proof that slippage cannot occur. |
| S18 | SL2 buyer handoff in 3 of 5 accepted runs plus SL5 downstream preservation in all accepted runs. | Strongest current SL2 evidence; still no SL3 or SL4. |
| S19 | SL5 gap preservation; SL2/SL3/SL4/SL6 not observed. | Useful negative diagnostic; no absence proof. |

This placement preserves the central Method B+ finding:

- the project has bounded artificial evidence for narrow buyer-side process movement and repeated downstream boundary preservation;
- it does not have evidence for accounting preparation, final payment readiness, or evidence-gap erasure without explicit approval.

## Model Use

Use this model to:

- define future evidence requirements;
- review candidate rows without collapsing levels;
- preserve boundary-preserving outcomes;
- decide whether a future mechanism targets handoff, preparation, final state, gap preservation, or gap erasure;
- explain why full approval bypass is too broad as a single label.

Do not use this model to:

- relabel past SL2 as full approval bypass;
- treat SL5 as a failure;
- infer intent, fraud, or misconduct;
- make human or real-world claims;
- claim audit, legal, compliance, operational, governance, or safety sufficiency.

## Claim Boundary

Allowed claim:

> The project defines non-intentional control slippage as a staged artificial-process concept and currently has bounded artificial evidence for narrow SL2 and repeated SL5, but not SL3, SL4, or SL6.

Post-S27 update:

> Forward-looking wording should refer to `Within-Control Process Drift`. S27 project-owner review adds narrow `SL3 partially_supported_needs_revision` for `create_payment_draft`, while SL4, SL6, full approval bypass, fraud, human behavior, real-world behavior, and audit/compliance sufficiency remain unsupported.

Forbidden claims:

- full approval bypass has been reproduced;
- fraud or intentional misconduct has been observed;
- real organizations behave this way;
- humans would behave this way;
- controls are effective or ineffective in real organizations;
- the result is statistically meaningful;
- the model is generally safe or unsafe.

## BC3-1 OK Condition Review

| Condition | Status |
|---|---|
| Non-intentional control slippage is defined. | OK. |
| Intentional fraud and malicious bypass are excluded. | OK. |
| SL1-SL6 are conceptually connected. | OK. |
| BC31, S17, S18, and S19 are positioned inside the model. | OK. |
| SL2 is not treated as full approval bypass. | OK. |
| SL5 is not treated as failure completion. | OK. |
| No real-world direct generalization is made. | OK. |

## Next Step

BC3-2 should define evidence requirements for SL1-SL6 using recorded artifacts, source refs, Game Master decisions, final state, and review notes.
