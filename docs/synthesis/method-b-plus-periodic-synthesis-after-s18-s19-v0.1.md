# Method B+ Periodic Synthesis After S18/S19 v0.1

Date: 2026-05-17
Status: accepted
Phase: Method B+
Checkpoint: periodic synthesis after two mechanism diagnostics
Claim boundary: `method_b_plus_periodic_synthesis_after_s18_s19_only`

## Scope

This synthesis reviews the Method B+ mechanism work after two post-boundary-preservation diagnostics:

- S18 lossy handoff control-slippage diagnostic;
- S19 queue/ticket state mismatch control-slippage diagnostic.

It asks whether these mechanism iterations justify another targeted execution, a controlled failure-mode baseline, a broader synthesis, or a pause.

This document adds no new runs, no new generated candidate rows, no new reviewed candidate rows, no protocol change, no prompt change, no scenario change, no action-menu change, no Game Master change, no event taxonomy change, and no baseline.

## Source Artifacts

| Purpose | Artifact |
|---|---|
| Boundary preservation synthesis | `docs/synthesis/method-b-plus-boundary-preservation-synthesis-v0.1.md` |
| Next mechanism selection | `docs/reflections/method-b-plus-next-mechanism-selection.md` |
| S17 control-slippage progression result | `pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/summary.md` |
| S17 candidate review | `pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/candidate-review-0001/summary.md` |
| S18 lossy handoff protocol | `protocols/failure-modes/method-b-plus-lossy-handoff-diagnostic-v0.1.md` |
| S18 lossy handoff result | `pilot-runs/org-payment/method-b-plus-lossy-handoff-diagnostic-pilot-0001/summary.md` |
| S18 candidate review | `pilot-runs/org-payment/method-b-plus-lossy-handoff-diagnostic-pilot-0001/candidate-review-0001/summary.md` |
| S18 mechanism synthesis | `docs/synthesis/method-b-plus-mechanism-iteration-synthesis-v0.1.md` |
| S19 queue/ticket protocol | `protocols/failure-modes/method-b-plus-queue-ticket-state-mismatch-diagnostic-v0.1.md` |
| S19 queue/ticket result | `pilot-runs/org-payment/method-b-plus-queue-ticket-state-mismatch-diagnostic-pilot-0001/summary.md` |
| S19 candidate review | `pilot-runs/org-payment/method-b-plus-queue-ticket-state-mismatch-diagnostic-pilot-0001/candidate-review-0001/summary.md` |
| S19 reflection | `docs/reflections/method-b-plus-bc36-after-queue-ticket-state-mismatch-review.md` |
| Current Method B+ synthesis | `docs/synthesis/method-b-plus-iterative-targeting-synthesis-v0.1.md` |
| Failure-mode status table | `docs/synthesis/method-b-plus-failure-mode-status.csv` |
| Slippage map | `docs/synthesis/non-intentional-control-slippage-map.csv` |
| Claim-boundary review | `docs/synthesis/method-b-plus-claim-boundary-review.md` |

## Why This Synthesis Is Needed

The Method B+ plan requires a periodic synthesis after several BC cycles so that the project does not keep running small variants of the same diagnostic after repeated conservative outcomes.

The immediate trigger is S19. S18 produced useful SL2 buyer-side handoff support, but accountant-side controls preserved the gap. S19 tested a different mechanism, queue/ticket state mismatch, and produced only boundary preservation. The project therefore needs a checkpoint-level decision before any new targeted mechanism is frozen.

## Cross-Mechanism Result Summary

| Source | Mechanism | Buyer-side movement | Accountant-side movement | Reviewed support | Unsupported targets |
|---|---|---|---|---|---|
| BC31 | Ambiguous approval targeting | One buyer payment-forward handoff without explicit approval. | Accountant requested more evidence. | Narrow SL2 partial support plus SL5 preservation. | SL3, SL4, full approval bypass. |
| S17 | Direct SL2-SL4 progression stress | Buyer selected `hold_payment` in all accepted runs. | Accountant selected `hold_payment` in all accepted runs. | SL5 preservation. | SL2, SL3, SL4, SL6, FM6. |
| S18 | Lossy handoff | Buyer selected `submit_payment_request` in 3 of 5 accepted runs. | Accountant selected `hold_payment` in all accepted runs. | SL2 in 3 reviewed artificial runs; SL5 in all 5. | SL3, SL4, SL6, FM1, FM3, FM6. |
| S19 | Queue/ticket state mismatch | Buyer selected `hold_payment` in all accepted runs. | Accountant selected `hold_payment` in all accepted runs. | SL5 preservation. | SL2, SL3, SL4, SL6, FM1, FM3, FM6. |

## What Is Now Clearer

S18 clarified that information compression can move the artificial case to a buyer-side handoff boundary. This is useful because it shows a repeatable distinction between "the buyer forwards the case" and "accounting prepares payment."

S19 clarified a different point: a readiness-like ticket state was not enough, under the frozen S19 setup, to displace missing approval and exception evidence. Both buyer and accountant preserved the boundary.

Together, S18 and S19 strengthen a narrower conclusion:

- Method B+ can make SL2 appear under some information-transfer conditions.
- The downstream accounting boundary has remained intact in every reviewed S17, S18, and S19 run.
- The current artifacts do not support SL3 payment preparation, SL4 final payment readiness, SL6 evidence-gap erasure, FM1 responsibility diffusion, FM3 ambiguous-guidance misinterpretation, or FM6 post-hoc justification.

## Boundary-Preservation Pattern

The repeated conservative pattern should be treated as an informative artificial-environment result, not hidden as a failed attempt.

Across the recent Method B+ diagnostics:

- roles often choose `hold_payment` when explicit approval or exception authority is unresolved;
- accountant-side actions preserve evidence gaps even when buyer handoff or ticket state could have created pressure to continue;
- Game Master decisions keep global truth separate from role-local interpretations;
- final states do not silently convert incomplete approval evidence into payment readiness;
- post-hoc explanations do not repair or erase the gap under reviewed criteria.

This does not prove that real controls work. It shows that the current artificial design is better at preserving explicit approval gaps than at producing stronger non-intentional slippage.

## Mechanism Assessment

### Lossy Handoff

Lossy handoff was useful. It produced reviewed SL2 support in S18 and should remain the strongest Method B+ mechanism for buyer-side payment-forward movement.

It did not produce stronger slippage because the accountant still preserved the approval gap. Repeating S18 as-is would likely add more SL2/SL5 accounting rather than a qualitatively new result.

### Queue/Ticket State Mismatch

Queue/ticket state mismatch was useful as a negative diagnostic. It tested a readiness-like workflow signal and found that the frozen setup still preserved the approval gap.

It did not add SL2, SL3, SL4, or SL6 support. Repeating S19 as-is would likely add more boundary-preservation rows rather than a new mechanism-level insight.

## Baseline Readiness

Method B+ is not ready for a controlled failure-mode baseline.

Reasons:

- no full failure-mode support exists;
- SL2 support remains buyer-side only and does not extend to SL3 or SL4;
- S17 and S19 did not reproduce SL2;
- S18 reproduced SL2 only under lossy handoff and still preserved the accounting boundary;
- stronger targets remain unsupported or reviewed rejected;
- a baseline from SL2 alone would overstate the evidence.

## Checkpoint Decision

Decision: pause targeted Method B+ execution and do not freeze another mechanism immediately.

Recommended next checkpoint: claim-hardening or project-owner review of the Method B+ endpoint before any further mechanism.

Rationale:

- two mechanism iterations have now been completed after the boundary-preservation synthesis;
- the strongest positive signal is still narrow SL2 plus downstream SL5 preservation;
- the newest mechanism, S19, produced only SL5;
- further execution risks chasing stronger slippage without a new research justification;
- the project should first record that Method B+ currently supports boundary-preservation and narrow handoff observations, not a controlled failure-mode baseline.

Acceptable next paths after this synthesis:

1. Prepare a Method B+ endpoint / claim-hardening synthesis that states the current Method B+ evidence limit.
2. Request project-owner or external human review of the narrow SL2 support if stronger reviewed status is needed.
3. Design a substantially new mechanism only after a fresh mechanism-selection PR explains why it is not another S17/S18/S19 variant.

This synthesis does not execute any of those paths.

## OK / STOP Condition Review

| Condition | Status |
|---|---|
| It clearly states whether the mechanisms added new evidence. | OK. S18 added SL2 evidence; S19 added only SL5 preservation. |
| It does not treat no-observed results as failure. | OK. S19 is recorded as useful negative diagnostic evidence. |
| It identifies the next decision. | OK. Pause targeted execution and perform claim-hardening or review before more mechanisms. |
| It does not recommend a baseline from weak or unreviewed candidates. | OK. No baseline is recommended. |
| It does not hide conservative outcomes. | OK. Boundary preservation is the central result. |
| It does not treat artificial behavior as human behavior. | OK. All claims remain artificial-system-only. |
| It does not ignore prior negative results. | OK. BC31, S17, S18, and S19 are compared directly. |

STOP conditions are not triggered for this synthesis PR because it does not add execution and does not overclaim the evidence. A STOP condition is triggered for immediate further targeted execution: the project should not proceed to another run-producing diagnostic until a new mechanism-selection rationale is recorded.

## Allowed Claim

This synthesis may claim that, after S18 and S19, Method B+ has reviewed artificial-evidence support for narrow SL2 buyer handoff under lossy handoff and repeated SL5 evidence-gap preservation, while SL3, SL4, SL6, FM1, FM3, and FM6 remain unsupported.

## Forbidden Claims

This synthesis does not claim:

- full approval bypass was reproduced;
- accountant payment preparation without explicit approval occurred;
- final payment-ready state without explicit approval occurred;
- evidence-gap erasure occurred;
- responsibility diffusion occurred;
- ambiguous-guidance misinterpretation occurred;
- post-hoc justification occurred;
- lossy handoff or ticket-state mismatch caused any behavior;
- the model is generally safe, unsafe, robust, or unstable;
- humans or real organizations behave this way;
- the result is statistically meaningful;
- the artifacts prove a real control deficiency;
- the artifacts provide compliance, legal, audit, or operational sufficiency.
