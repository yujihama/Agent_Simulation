# Phase 4 S34 Default Proposed Packet Structuring Synthesis v0.1

Checkpoint: after S34 execution and proxy candidate review

Primary result artifact: `pilot-runs/org-payment/phase4-s34-default-proposed-packet-structuring-diagnostic-0001/summary.md`

Claim boundary: `phase4_default_proposed_packet_structuring_observation_only`

## Result Summary

S34 tested whether replacing a gray-option menu with one concrete default proposed packet changes requester/buyer adoption of split packet handling.

Execution result:

- attempted runs: 20
- accepted runs: 20
- excluded runs: 0
- model: OpenAI `gpt-5.2`
- observed model version: `gpt-5.2-2025-12-11`
- default proposed packets accepted by deterministic filter: 20
- default split packet present: 15
- applicant accepted default packet unchanged: 5
- split packet forwarded: 8
- SL2 candidate: 8
- SL5 gap preservation: 20
- SL4: not observed
- SL6: not observed

Selected requester/buyer actions:

- `revise_to_single_aggregate_request`: 11
- `accept_default_packet`: 5
- `revise_with_aggregate_note`: 4

## Interpretation

S34 produced a stronger split-forwarding signal than S33, but it still mainly reinforced boundary preservation.

The key difference from S33 is decision structure. In S33, gray split options were added to a menu and requester/buyer selected one split option in 19 accepted runs. In S34, a concrete proposed packet was presented as the default, and split packet forwarding appeared in 8 of 20 accepted runs. This suggests the default-packet mechanism is more promising than gray-option menu expansion for producing bounded applicant-side SL2 candidates.

However, requester/buyer still did not generally accept the default unchanged. Most responses revised the packet toward a single aggregate request or added aggregate notes. Aggregate approval/review gaps remained visible in every accepted run.

## SL Status

| Level | S34 status | Boundary |
|---|---|---|
| SL1 | candidate in 2/20 | Proxy-reviewed artificial evidence only; no hidden intent or human claim. |
| SL2 | candidate in 8/20 | Split packet forwarding while aggregate approval/review remained unresolved. |
| SL4 | not observed | No final payment-ready state without aggregate approval/review. |
| SL5 | observed in 20/20 | Aggregate approval/review gap remained visible and conditioned the process. |
| SL6 | not observed | No aggregate relationship or approval/review gap erasure. |

S34 does not include an accountant turn, so it does not test SL3 directly.

## Mechanism Assessment

Default proposed packet structuring is more informative than neutral or gray option seeding because it changes the applicant-side decision from choosing among options to reviewing a concrete proposed packet. It produced repeated SL2 candidates, especially where split packets were the proposed default.

It still does not justify a controlled failure-mode baseline because:

- SL2 remains applicant-side and bounded;
- no accountant-side preparation is tested in S34;
- no SL4 or SL6 support appears;
- SL5 preservation remains dominant;
- the support is proxy-reviewed artificial evidence, not project-owner or external human review.

## Next Decision

Do not proceed directly to baseline.

Recommended next step, if Phase 4 continues, is a separately frozen downstream-chain diagnostic that starts from reviewed S34 split-forwarding artifacts and tests whether accountant-side handling preserves, weakens, or erases aggregate approval/review gaps.

That next protocol must be frozen before execution and must preserve:

- within-control / outside-control boundary;
- role-local views;
- global truth;
- candidate/support separation;
- no fraud, hidden-intent, human behavior, real-world behavior, statistical, prompt-causation, model-general, or audit/compliance sufficiency claim.
