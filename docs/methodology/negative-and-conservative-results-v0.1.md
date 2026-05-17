# Negative And Conservative Results Methodology v0.1

Date: 2026-05-17
Status: accepted
Phase: Phase 2
Checkpoint: BC2-3 negative and conservative result methodology
Claim boundary: `negative_conservative_result_methodology_only`

## Scope

This document defines how the project should handle negative, not-observed, rejected, and conservative boundary-preserving results.

It adds no new runs, candidates, reviews, protocols, scenarios, prompts, metrics, schemas, validators, or result claims. It does not reinterpret prior evidence beyond existing reviewed boundaries.

## Principle

Negative and conservative results are first-class research outputs.

In this project, a run that does not produce approval bypass, responsibility diffusion, evidence-gap erasure, or another target pattern can still answer a research question. It may show that under the frozen artificial conditions:

- a role held payment;
- a role requested more evidence;
- a Game Master decision preserved a gap;
- a final state did not become payment-ready;
- a generated candidate was rejected in review;
- a target was not observed in the reviewed scope.

Those outcomes should be preserved, not hidden.

## Result Categories

| Category | Meaning | How to report |
|---|---|---|
| `not_observed` | The target pattern did not appear in the bounded run set or reviewed scope. | Report denominator, scope, and review level; do not claim absence generally. |
| `reviewed_rejected` | A generated or proposed candidate was checked and did not satisfy the criterion. | Cite source refs and counter-evidence; do not treat it as support. |
| `needs_revision` | The artifact, metric, or criterion is too ambiguous for stable interpretation. | Record defect and do not upgrade until revised and re-reviewed. |
| `partially_supported_needs_revision` | A narrow part is supported but the broader label is not. | State supported and unsupported portions separately. |
| `boundary_preservation` | The process preserved an approval/evidence/control gap instead of advancing through it. | Treat as an artificial-system observation; do not claim real-world control effectiveness. |
| `conservative_action_pattern` | Roles selected hold, request-evidence, or escalation rather than payment-forward actions. | Report as behavior under the artificial setup, not model-general safety. |

## Not Observed Is Not Proof Of Absence

`not_observed` means:

> The reviewed artifacts did not show the target under the frozen conditions and reviewed scope.

It does not mean:

> The target cannot happen.

Every not-observed statement should preserve:

- scenario or protocol scope;
- run count or reviewed artifact scope;
- review level;
- target definition;
- any visibility or action-menu conditions;
- whether source artifacts were mechanically validated.

## Boundary Preservation Is Not Real-World Control Effectiveness

Boundary-preserving outcomes can be useful. For example, when an accountant holds payment because explicit approval is absent, that is a meaningful artificial-system result.

But the project must not convert that into:

- "real controls work";
- "LLMs are safe";
- "approval bypass will not happen";
- "the organization is compliant";
- "the model is reliable in production."

The correct claim is narrower:

> Under the frozen artificial setup, the reviewed artifacts preserved the approval or evidence gap rather than advancing past it.

## Why Conservative Results Matter

Conservative results help the project:

- identify which artificial design features keep gaps visible;
- avoid repeatedly chasing a desired failure;
- distinguish weak handoff movement from stronger downstream slippage;
- decide when a baseline is not justified;
- select genuinely different future mechanisms;
- improve claim discipline.

Method B+ is the main example. It found narrow buyer-side SL2 handoff in limited conditions, but repeatedly preserved downstream gaps at the accounting and final-state stages. That result is not a failure of the project. It is a boundary-preservation finding.

## Reporting Requirements

When reporting negative or conservative results, include:

- protocol or scenario reference;
- attempted and accepted run counts when applicable;
- reviewed artifact scope;
- review status and review level;
- target status by subtype or failure mode;
- source or table references;
- claim boundary;
- what can be said;
- what remains unsupported;
- next decision.

Do not report:

- unsupported absence claims;
- hidden candidate rows;
- only positive-looking outcomes;
- aggregate counts without scope;
- conservative outcomes as model safety or real-world control claims.

## Examples From Current Evidence

| Evidence area | Conservative or negative result | Correct use |
|---|---|---|
| S17 control-slippage progression | Buyer and accountant selected `hold_payment`; SL5 gap preservation was supported; SL2/SL3/SL4/SL6/FM6 were not observed. | Shows boundary preservation under S17 artificial conditions. |
| S18 lossy handoff | SL2 buyer handoff appeared in 3 of 5 runs, but accountant held payment and final state did not become payment-ready. | Separates first-stage handoff from downstream preparation/readiness. |
| S19 queue/ticket mismatch | Buyer and accountant selected `hold_payment`; SL5 supported; SL2/SL3/SL4/SL6 not observed. | Treats queue/ticket mismatch as a useful negative diagnostic. |
| BC28/BC31/BC37-C/BC35 FM6 reviews | Generated FM6 candidates were reviewed rejected or not observed. | Prevents heuristic post-hoc flags from becoming supported FM6 findings. |
| EXP-0002 human review | Some pressure-citation metric checks were marked `needs_revision`. | Preserves metric limitation instead of forcing acceptance. |

## Baseline Gate

A controlled failure-mode baseline should not be frozen merely because:

- a target was searched for repeatedly;
- a generated candidate exists;
- a narrow partial observation exists;
- a conservative result is frustrating;
- a stronger result would be more interesting.

A baseline requires a protocol-defined target with enough reviewed support to justify repeated measurement. If the current evidence mainly shows boundary preservation, the correct next step is synthesis, review, or a new mechanism-selection PR, not baseline execution.

## STOP Conditions

Stop or revise if a document:

- treats not observed as proof of absence;
- hides conservative outcomes;
- treats boundary preservation as real-world control effectiveness;
- upgrades rejected candidates into findings;
- collapses SL2 handoff into SL3 preparation or SL4 final readiness;
- treats validator pass as claim support;
- describes proxy review as independent human validation;
- claims statistical significance without a frozen statistical protocol.

## BC2-3 OK Condition Review

| Condition | Status |
|---|---|
| Conservative results are explicitly organized. | OK. |
| SL5 evidence-gap preservation is treated as meaningful. | OK. |
| Not observed is separated from proof of absence. | OK. |
| Future mechanism selection can use conservative results. | OK. |
| Boundary preservation is not treated as real-world control effectiveness. | OK. |
| SL5 is not confused with SL3 or SL4. | OK. |

## Checkpoint Decision

Decision: BC2-3 negative and conservative result methodology is complete.

Proceed to Phase 2 synthesis after recording the boundary-preservation pattern summary.
