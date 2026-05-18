# Phase 4 Freeform vs Menu-Conditioned Structuring Synthesis v0.1

Date: 2026-05-18
Status: accepted
Phase: Phase 4 extension
Checkpoint: BC4-S30 synthesis
Related S29 protocol: `protocols/failure-modes/phase4-applicant-side-structuring-diagnostic-v0.1.md`
Related S29 result: `pilot-runs/org-payment/phase4-s29-applicant-side-structuring-diagnostic-0001/summary.md`
Related S29 project-owner review: `pilot-runs/org-payment/phase4-s29-applicant-side-structuring-diagnostic-0001/project-owner-review-0001/summary.md`
Related S30 protocol: `protocols/failure-modes/phase4-freeform-applicant-structuring-diagnostic-v0.1.md`
Related S30 result: `pilot-runs/org-payment/phase4-s30-freeform-applicant-structuring-diagnostic-0001/summary.md`
Related S30 review: `pilot-runs/org-payment/phase4-s30-freeform-applicant-structuring-diagnostic-0001/candidate-review-0001/summary.md`
Related S30 reflection: `docs/reflections/phase4-after-s30-freeform-applicant-structuring-review.md`
Claim boundary: `phase4_freeform_vs_menu_structuring_synthesis_only`

## Purpose

This synthesis compares the two applicant-side structuring diagnostics:

- S29 tested a fixed action menu where split-submission choices were visible.
- S30 tested freeform submission-plan generation without visible split-submission actions.

It adds no runs, protocols, scenarios, prompts, candidates, or claim upgrades. It decides whether S30 justifies moving into S31 multi-role structuring-chain execution and updates the Phase 4 tested-mechanism map.

## Core Comparison

| Question | S29 fixed-menu diagnostic | S30 freeform diagnostic |
|---|---|---|
| Actor task | Choose one action from a frozen menu. | Generate a structured submission / handling plan. |
| Visible split option | Yes. `submit_split_requests_with_aggregate_note` and `submit_split_requests_without_aggregate_note` were explicit choices. | No. The prompt did not show split-submission choices and did not ask for splitting. |
| Attempted / accepted | 20 / 20. | 20 / 20. |
| Pressure conditions | No pressure, deadline, queue/volume, compound pressure plus prior practice. | Same pressure-condition structure. |
| Split / multi-packet outcome | 7/20 split submissions, all under pressure conditions. | 0/20 freeform multi-packet proposals. |
| Main conservative outcome | Holds, single aggregate requests, or aggregate-note preservation. | Single aggregate submission or higher-approval / aggregate-review plans. |
| SL2 | Project-owner-reviewed bounded support in 7/20. | Not observed. |
| SL5 | Supported in 20/20. | Supported in 20/20. |
| SL6 | Not observed. | Not observed. |

## S29 Finding

S29 supports a bounded applicant-side within-control process-drift finding:

- requester/buyer selected split submission in 7 of 20 accepted artificial runs;
- split submission appeared in 7 of 15 pressure-condition runs and 0 of 5 no-pressure runs;
- 4 split submissions preserved aggregate context with an aggregate note;
- 3 split submissions did not include an aggregate note and were treated by project-owner review as stronger boundary candidates;
- aggregate approval/review gaps stayed visible in all runs.

This supports bounded SL2 applicant-side split-submission evidence and SL5 aggregate-gap preservation. It does not support SL3, SL4, SL6, full approval bypass, fraud, hidden intent, human behavior, real-world behavior, statistical significance, prompt causation, model-general behavior, or compliance/legal/audit/operational/governance/safety sufficiency.

## S30 Finding

S30 did not reproduce the S29 split-submission pattern when the explicit split actions were removed from the visible choice structure.

Observed S30 result:

- 20 attempted / 20 accepted / 0 excluded;
- 0 freeform multi-packet proposals;
- 9 single aggregate submission plans;
- 11 higher approval / aggregate review plans;
- all 20 runs preserved aggregate approval/review gaps;
- SL1, SL2, and SL6 were not observed.

S30 therefore supports a bounded artificial observation that, under the frozen S30 prompt and role-visible context, requester/buyer generated plans preserved aggregate controls rather than proposing split submission. This is not a proof that freeform actors never split, that prompt wording caused the difference, or that real people or organizations behave this way.

## What The Comparison Shows

The S29/S30 comparison suggests that the observed applicant-side split behavior is sensitive to the structure of the actor task in the current artificial setup:

- when split submission is a visible fixed action, it can be selected under pressure conditions;
- when the actor must generate its own handling plan without split actions in a menu, no split or multi-packet proposal appeared in the 20-run S30 diagnostic;
- both designs preserved aggregate approval/review gaps in global truth, Game Master, final-state, metrics, and review artifacts.

This is a design-sensitivity observation, not a causal claim. The current artifacts do not isolate whether the difference comes from menu affordance, prompt framing, model behavior, pressure intensity, role construction, or their combination.

## S31 Trigger Check

S31 was defined as a multi-role structuring-chain diagnostic to be used if S30 produced freeform split-proposal candidates.

S30 produced no freeform split-proposal candidates.

Decision: do not proceed to S31 from S30. Running S31 now would require changing the trigger condition or manually injecting split plans, which would be a new mechanism-selection/protocol-freeze decision rather than a continuation of the S30 path.

## Current Phase 4 Mechanism Map

| Observation level | Current support after S30 | Boundary |
|---|---|---|
| SL1 | Not supported in current Phase 4 reviewed evidence. | No reviewed finding that an actor treated local/split/pressure status as removing approval requirements. |
| SL2 | Supported in bounded contexts: BC31, S18 lossy handoff, S28 downstream split-item handoff, and S29 fixed-menu applicant-side split submission. | Handoff or split-submission movement only; S30 did not reproduce SL2 without explicit split choices. |
| SL3 | Narrow project-owner-confirmed partial support from S27 `create_payment_draft`. | Draft creation only; no final payment-ready state and gaps remained visible. |
| SL4 | Not supported. | No tested mechanism produced final payment-ready or approval-sufficient state without required approval/review. |
| SL5 | Repeatedly supported, including S17-S20, S23-S30. | Strongest repeated artificial-system pattern is approval/evidence/aggregate-gap preservation. |
| SL6 | Not supported. | No tested mechanism erased or contradicted the approval/evidence/aggregate gap downstream. |

## Baseline Readiness

S30 does not justify baseline preparation.

Reasons:

- S30 did not produce freeform SL2 split proposals;
- S29 SL2 remains meaningful but fixed-menu-conditioned;
- S27 SL3 remains narrow partial support only;
- SL4 and SL6 remain unsupported;
- S31 was conditional on S30 split proposals and should not be executed under the current chain;
- a baseline would risk converting task-design-sensitive exploratory evidence into stronger claims than the project can support.

Baseline discussion would require a separate target-definition checkpoint, project-owner confirmation of the target level, and a frozen baseline protocol. That threshold is not met by S30.

## Phase 4 Completion Assessment

Phase 4 should now be treated as research-complete for the tested mechanism map through S30, with a specific limitation:

- the project has identified information structures that can produce bounded SL2 under artificial conditions: lossy handoff, downstream split-item handoff, and fixed-menu applicant-side split submission;
- it has identified one narrow SL3 partial-support mechanism: S27 payment-draft staging through `create_payment_draft`;
- it has not identified a tested mechanism that produces SL4 or SL6;
- S30 shows that applicant-side structuring does not appear in this freeform generation setup without explicit split action choices;
- the dominant repeated result remains SL5 gap preservation.

This is sufficient to pause autonomous run-producing Phase 4 work and consolidate, not sufficient to claim stronger downstream slippage or baseline readiness.

## Future Work Boundary

Future run-producing work should resume only if a new mechanism-selection PR defines a substantially different information mechanism or target question.

Examples of genuinely different future questions include:

- a protocol that explicitly studies menu affordances as the mechanism, without calling it freeform emergence;
- a downstream protocol seeded from project-owner-reviewed S29 split-without-aggregate-note cases, with a clear target-definition checkpoint;
- an aggregate-information degradation diagnostic where omitted role-local fields are frozen as scenario variants and global truth remains reconstructable.

Any such work must freeze protocol, role-visible context, candidate rules, review criteria, and claim boundary before execution.

## Allowed Claims

This synthesis may claim:

- S29 produced project-owner-reviewed bounded applicant-side SL2 split-submission support under fixed-menu pressure conditions.
- S30 did not produce freeform split or multi-packet proposals without explicit split action choices.
- Both S29 and S30 preserved aggregate approval/review gaps as SL5.
- The tested evidence suggests fixed choice structure is an important artificial-design factor for applicant-side split submission in this project.
- S31 should not proceed from S30 because its trigger condition was not met.

## Forbidden Claims

This synthesis must not claim:

- prompt wording caused the difference between S29 and S30;
- actors intentionally bypassed controls;
- fraud occurred;
- full approval bypass was reproduced;
- freeform actors or real applicants would never split requests;
- humans or real organizations behave this way;
- results are statistically significant;
- the result generalizes across models;
- the artifacts support compliance, legal, audit, operational, governance, or safety sufficiency.

## Checkpoint Decision

Decision: stop the S30-to-S31 execution path and consolidate Phase 4.

No additional autonomous run-producing BC should start from S30. If execution resumes, it must begin with a new mechanism-selection or target-definition checkpoint rather than by treating S31 as already authorized.
