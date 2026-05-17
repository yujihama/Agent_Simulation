# Control Slippage vs Fraud

Date: 2026-05-17
Status: accepted
Phase: Phase 3
Checkpoint: BC3-1 control slippage conceptual model
Claim boundary: `control_slippage_vs_fraud_only`

## Scope

This document distinguishes non-intentional control slippage from fraud, malicious bypass, and intentional misconduct.

It adds no new runs, candidates, reviews, protocols, scenarios, prompts, metrics, schemas, validators, or empirical claim upgrades.

## Short Distinction

| Area | Non-intentional control slippage | Fraud or malicious bypass |
|---|---|---|
| Intent | No required intent to deceive or violate. | Deception, concealment, collusion, or knowing violation is central. |
| Mechanism | Ambiguity, handoff loss, role-local information, routine practice, exception ambiguity, queue state, or evidence gaps. | Forgery, fabricated evidence, hidden manipulation, concealment, collusion, or coercive misuse. |
| Evidence focus | Process movement despite unresolved controls. | Proof of intentional deceptive action or fraudulent representation. |
| Current project scope | In scope for artificial modeling. | Out of scope for current evidence. |
| Claim boundary | Artificial-system and review-limited. | Would require separate fraud-indicator protocols and stronger evidence. |

## Why The Distinction Matters

The project studies how an artificial organizational process can move forward without anyone being instructed to commit wrongdoing.

That is different from studying fraud. A buyer handing a case to accounting with unresolved approval is not evidence that the buyer intended to deceive. An accountant holding payment because approval is absent is not fraud evidence. A final state preserving a gap is a boundary-preserving result, not misconduct.

Conflating these concepts would create two problems:

- it would overclaim current artificial evidence;
- it would make future review depend on inferred intent rather than visible artifacts.

## Included In Control Slippage

The control-slippage model may include cases where:

- approval language is ambiguous;
- a handoff summary weakens a known gap;
- a role sees only local context;
- a queue state says ready while approval fields are blank;
- exception routing is unclear;
- informal norms conflict with written policy;
- a known gap is preserved downstream;
- a known gap is erased downstream.

These are process and evidence phenomena. They do not require a claim about bad intent.

## Excluded From Current Scope

The current model excludes:

- forged approvals;
- fabricated invoices;
- knowingly false statements;
- hidden side agreements;
- collusion among roles;
- deliberate concealment of missing approval;
- coercive or abusive pressure;
- real-world fraud, legal, or compliance determinations.

If future work studies these, it must freeze a separate protocol before execution and define fraud-indicator evidence requirements. It must not reuse control-slippage evidence as fraud evidence.

## Evidence Standard Difference

| Claim type | Minimum evidence direction |
|---|---|
| SL2 buyer handoff | Action and GM decision show handoff while explicit approval is absent. |
| SL3 accountant preparation | Accountant/finance action and GM/final-state evidence show preparation while explicit approval is absent. |
| SL6 gap erasure | Earlier gap and downstream omission/contradiction are both visible in artifacts. |
| Fraud or intentional misconduct | Visible evidence of deception, fabrication, concealment, collusion, or knowing violation under a fraud-specific protocol. |

The current repository has evidence for some slippage-boundary observations. It does not have evidence for fraud.

## Audit-Practice Connection With Boundary

The vocabulary is meant to be legible to audit and control readers because it distinguishes:

- missing approval;
- handoff;
- payment preparation;
- final readiness;
- evidence preservation;
- evidence erasure.

However, the project does not provide audit assurance. It does not assess a real entity, real transaction, real control design, or legal compliance. It provides artificial artifacts that can help frame hypotheses and review methods.

## STOP Conditions

Stop or revise if future work:

- treats non-intentional slippage as fraud;
- infers malicious intent from a conservative or ambiguous artifact;
- claims real-world control deficiency from artificial evidence;
- uses hidden chain-of-thought as intent evidence;
- upgrades SL2 handoff into fraud or full approval bypass;
- treats boundary preservation as proof that fraud or slippage cannot occur.

## Checkpoint Decision

Decision: control slippage and fraud are separated for Phase 3.

Future Phase 3 evidence requirements should define SL1-SL6 using visible artifacts and should not require or infer intent unless a separate fraud-focused protocol is frozen.
