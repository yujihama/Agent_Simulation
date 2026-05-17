# Method B+ Mechanism Iteration Synthesis v0.1

Date: 2026-05-17
Status: accepted
Phase: Method B+
Checkpoint: BC-E mechanism-level synthesis after S18 lossy handoff
Claim boundary: `method_b_plus_mechanism_iteration_synthesis_only`

## Scope

This synthesis reviews the first Method B+ mechanism iteration after the boundary-preservation synthesis and next-mechanism selection.

It covers:

- the prior state before the mechanism iteration;
- why `Lossy Handoff` was selected;
- what the frozen S18 lossy handoff diagnostic added;
- what remains unsupported;
- whether the project should continue the same mechanism, move to another mechanism, pause, or request external/project-owner review.

This document adds no new runs, no new generated candidate rows, no new reviewed candidate rows, no protocol change, no prompt change, no scenario change, no action-menu change, no Game Master change, no event taxonomy change, and no baseline.

## Source Artifacts

| Purpose | Artifact |
|---|---|
| Boundary preservation synthesis | `docs/synthesis/method-b-plus-boundary-preservation-synthesis-v0.1.md` |
| Mechanism selection | `docs/reflections/method-b-plus-next-mechanism-selection.md` |
| Frozen lossy handoff protocol | `protocols/failure-modes/method-b-plus-lossy-handoff-diagnostic-v0.1.md` |
| S18 scenario | `scenarios/org-payment/s18-lossy-handoff-control-slippage.yaml` |
| S18 execution result | `pilot-runs/org-payment/method-b-plus-lossy-handoff-diagnostic-pilot-0001/summary.md` |
| S18 candidate review | `pilot-runs/org-payment/method-b-plus-lossy-handoff-diagnostic-pilot-0001/candidate-review-0001/summary.md` |
| S18 reflection | `docs/reflections/method-b-plus-bc36-after-lossy-handoff-review.md` |
| Slippage map | `docs/synthesis/non-intentional-control-slippage-map.csv` |
| Failure-mode status table | `docs/synthesis/method-b-plus-failure-mode-status.csv` |
| Claim-boundary review | `docs/synthesis/method-b-plus-claim-boundary-review.md` |

## Prior State Before Lossy Handoff

Before S18, the Method B+ evidence had two main patterns:

1. BC31 had a narrow buyer-side SL2 boundary observation: the buyer forwarded a payment-related handoff toward accounting while explicit approval was absent. Downstream accounting did not prepare payment, and the final state did not become payment-ready.
2. Later targeted diagnostics mostly preserved gaps. BC37-C, BC35, and S17 repeatedly produced `hold_payment` or evidence-preserving outcomes. S17 did not reproduce SL2 and did not support SL3, SL4, SL6, or FM6.

The boundary-preservation synthesis therefore concluded that the current artificial setup was more informative as a boundary-preserving environment than as a full failure-mode baseline. A new information-transfer mechanism was needed before further targeted execution.

## Mechanism Selected

The selected mechanism was `Lossy Handoff`.

The mechanism tested whether a known approval gap remains visible after the buyer compresses case information into an accountant-facing handoff. It did not instruct the buyer to hide evidence, bypass approval, fabricate authorization, or make payment ready. The Game Master retained global truth while role-view and handoff artifacts recorded what each role saw.

The diagnostic was useful because prior runs made missing approval highly visible to all relevant roles. Lossy handoff changed how information moved between roles while preserving reconstruction.

## S18 Execution Result

The frozen S18 lossy handoff diagnostic executed 5 attempted runs, all accepted, with no exclusions, parser failures, validation failures, retries, or rejected proposals.

| Measure | Result |
|---|---:|
| Attempted runs | 5 |
| Accepted runs | 5 |
| Excluded runs | 0 |
| Buyer `submit_payment_request` | 3 |
| Buyer `hold_payment` | 2 |
| Accountant `hold_payment` | 5 |
| SL2 generated candidates | 3 |
| SL5 observed rows | 5 |
| SL3, SL4, SL6, FM1, FM3, FM6 | Not observed |

Reviewed result:

- SL2 payment-forward handoff without explicit approval: `supported_for_reviewed_evidence` in 3 artificial runs.
- SL5 evidence-gap preservation: `supported_for_reviewed_evidence` in all 5 artificial runs.
- SL3 payment preparation without explicit approval: `not_observed`.
- SL4 final payment-ready state without explicit approval: `not_observed`.
- SL6 evidence-gap erasure: `not_observed`.
- FM1 responsibility diffusion, FM3 ambiguous-guidance misinterpretation, and FM6 post-hoc justification: `not_observed`.

## What Became Newly Visible

S18 made one thing clearer than the prior S17 direct stress diagnostic: compressed handoff can produce buyer-side payment-forward movement under the artificial setup.

This matters because it separates two stages that earlier work could easily collapse:

- the buyer may move a case toward accounting without explicit approval;
- accounting may still preserve the approval gap and refuse to prepare payment.

S18 therefore strengthens the evidence that SL2 is a real boundary to track in this artificial environment. It does not strengthen SL3 or SL4.

The new contribution is not "approval bypass was reproduced." The contribution is narrower:

- lossy handoff produced reviewed SL2 observations in 3/5 runs;
- downstream accountant review preserved the gap in 5/5 runs;
- stronger slippage did not appear.

## What Remains Unsupported

The following remain unsupported after this mechanism iteration:

| Target | Status after S18 |
|---|---|
| SL3 accountant payment preparation without explicit approval | Not observed |
| SL4 final payment-ready state without explicit approval | Not observed |
| SL6 evidence-gap erasure | Not observed |
| FM1 responsibility diffusion | Not observed |
| FM3 ambiguous-guidance misinterpretation | Not observed |
| FM6 post-hoc justification | Not observed |
| Full approval bypass | Not supported |
| Controlled failure-mode baseline readiness | Not supported |

SL2 alone is not enough to justify a controlled failure-mode baseline because the downstream control boundary held in every accepted S18 run.

## Mechanism Assessment

Lossy handoff added useful evidence, but it appears to stop at a buyer-side handoff boundary under the current design.

Strengths:

- It produced reviewed SL2 support where S17 did not.
- It preserved reconstructability by recording global truth, role views, handoff summaries, actions, GM decisions, metrics, and review artifacts.
- It avoided instructing any role to violate controls.
- It showed that the project can separate handoff movement from accountant preparation and final payment readiness.

Limits:

- The accountant still received enough local evidence to preserve the approval gap.
- The accountant action menu preserved a clear `hold_payment` option.
- The deterministic Game Master continued to record unresolved gaps explicitly.
- No evidence-gap erasure, responsibility diffusion, ambiguous-guidance misinterpretation, or post-hoc justification appeared.
- Repeating S18 as-is is likely to produce more SL2/SL5 accounting rather than a qualitatively new result.

## Decision

Decision: do not baseline and do not repeat the same S18 lossy handoff mechanism as-is.

Recommended next mechanism: `Queue / Ticket State Mismatch`.

Rationale:

- Lossy handoff showed buyer-side movement but did not change accountant-side control preservation.
- A queue or ticket state mismatch tests a different organizational signal: whether a workflow status such as `ready_for_accounting` competes with an empty approval field or unresolved approval note.
- This targets the accounting-side interpretation boundary more directly than another handoff-only run.
- It can remain reconstructable if the protocol records global truth, visible ticket state, approval-field state, role-local packet, and Game Master decisions separately.
- It still must not instruct roles to bypass approval, hide evidence, fabricate authorization, or treat ambiguity as approval.

The next protocol-freeze PR should define a queue/ticket state mismatch diagnostic before any execution. It should separate:

- visible workflow status;
- approval field state;
- buyer note or handoff summary;
- accountant local packet;
- Game Master global truth;
- SL2, SL3, SL4, SL5, SL6, FM1, FM3, and FM6 candidate and review criteria.

## OK / STOP Condition Review

| Condition | Status |
|---|---|
| The mechanism added new evidence. | OK. It added reviewed SL2 observations in S18. |
| No-observed stronger targets are not hidden. | OK. SL3, SL4, SL6, FM1, FM3, and FM6 remain explicit `not_observed` statuses. |
| Conservative outcomes are not treated as failure. | OK. Accountant `hold_payment` is treated as SL5 gap preservation. |
| Baseline is not recommended from weak or unreviewed evidence. | OK. No baseline is recommended. |
| Artificial behavior is not treated as human behavior. | OK. All claims remain artificial-evidence-only. |
| Prior negative results are considered. | OK. S17, BC37-C, BC35, and BC31 context are included. |

STOP conditions are not triggered.

## Allowed Claim

This synthesis may claim that the first Method B+ mechanism iteration, lossy handoff, produced reviewed artificial-evidence support for SL2 buyer payment-forward handoff in 3 of 5 S18 runs while downstream accountant review preserved the approval gap in all 5 accepted runs.

## Forbidden Claims

This synthesis does not claim:

- full approval bypass was reproduced;
- accounting prepared payment without explicit approval;
- final payment-ready state appeared without explicit approval;
- evidence-gap erasure occurred;
- responsibility diffusion occurred;
- post-hoc justification occurred;
- lossy handoff caused the buyer actions;
- the model is generally safe, unsafe, robust, or unstable;
- humans or real organizations behave this way;
- the result is statistically meaningful;
- the artifact proves a real control deficiency;
- the artifact provides compliance, legal, audit, or operational sufficiency.
