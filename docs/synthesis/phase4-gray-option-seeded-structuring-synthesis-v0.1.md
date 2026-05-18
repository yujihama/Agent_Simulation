# Phase 4 Gray-Option Seeded Structuring Synthesis v0.1

Date: 2026-05-19
Status: accepted
Phase: Phase 4 extension
Scenario: `S33`
Pilot: `PHASE4-S33-GRAY-OPTION-SEEDED-STRUCTURING-0001`
Curated result: `pilot-runs/org-payment/phase4-s33-gray-option-seeded-structuring-diagnostic-0001/summary.md`
Claim boundary: `phase4_gray_option_seeded_structuring_observation_only`

## Purpose

S33 tested whether explicitly surfaced gray within-control processing ideas would change applicant-side selection under pressure and aggregate-threshold conditions.

This was a design correction after S31 and S32:

- S31 showed that a neutral processing-option advisor could generate split-like options, but requester/buyer still selected conservative canonical actions.
- S32 was frozen as a recommendation-weighted ordinary-advisor protocol, but was deferred before execution because an ordinary operational advisor was likely to remain compliance-aligned.
- S33 therefore tested a more direct gray-option seeding mechanism: a gray-option ideation advisor generated conservative and boundary-stretching within-control ideas, a deterministic filter removed outside-control ideas, and requester/buyer selected from the accepted gray-seeded menu.

S33 is not a fraud simulation, not a baseline, and not a real-world behavior claim.

## Result

S33 attempted 20 artificial runs across four frozen conditions. Nineteen runs were accepted and one provider-failure run was excluded without replacement.

| Measure | Result |
|---|---:|
| Attempted runs | 20 |
| Accepted runs | 19 |
| Excluded runs | 1 |
| Gray-option accepted options | 114 |
| Gray-option rejected options | 0 |
| Seeded split option present | 19 |
| Selected gray-seeded split option | 1 |
| Selected canonical option | 18 |

Selected action counts:

- `request_higher_approval`: 11
- `submit_single_aggregate_request`: 7
- `submit_split_requests_with_aggregate_note`: 1

Condition pattern:

- No-pressure condition: 4 single aggregate submissions, 1 higher-approval request.
- Deadline pressure: 4 higher-approval requests, 1 provider-failure exclusion.
- Queue / volume pressure: 4 higher-approval requests, 1 single aggregate submission.
- Compound pressure + prior practice: 2 higher-approval requests, 2 single aggregate submissions, 1 gray-seeded split request with aggregate note.

## SL Interpretation

| Level | S33 status | Interpretation |
|---|---|---|
| SL1 | Not observed | Requester/buyer did not treat pressure, individual amounts, local readiness, or gray-option availability as approval. |
| SL2 | Candidate in 1/19 accepted runs | One requester/buyer selected a gray-seeded split action with aggregate note while aggregate review remained unresolved. This is bounded applicant-side SL2 only. |
| SL4 | Not observed | There was no final payment-ready state. S33 has no downstream accountant turn. |
| SL5 | Observed in 19/19 | Aggregate approval/review gaps remained visible in accepted runs, including the selected split-with-aggregate-note run. |
| SL6 | Not observed | Aggregate relationship and review gap were not erased in final records. |

## What S33 Adds

S33 separates three mechanisms that were previously conflated:

1. Gray-option generation: observed.
2. Gray-option filtering into a visible applicant menu: observed.
3. Applicant selection of a gray split option: not observed.

This means S33 weakly reproduces the S29 fixed-menu split-submission pattern only once, under the compound-pressure/prior-practice condition, and only with aggregate context preserved. It also shows that requester/buyer usually still chooses canonical conservative actions when those actions remain available and aggregate approval/review gaps remain visible.

## Comparison To Prior Structuring Mechanisms

| Mechanism | Key result |
|---|---|
| S29 fixed-menu applicant-side structuring | Project-owner-reviewed bounded SL2 split submission appeared in 7/20 runs. |
| S30 freeform applicant structuring | No freeform split proposals; SL5 preservation in 20/20. |
| S31 neutral advisor-seeded structuring | Split-like options appeared, but applicant selected conservative canonical actions in all accepted runs. |
| S33 gray-option seeded structuring | Gray split options appeared in all accepted runs; applicant selected one split-with-aggregate-note option and otherwise selected conservative canonical actions. |

The current evidence suggests that S29's split-selection signal may depend on how the action space is presented. It has not been reproduced by freeform generation, neutral advisor seeding, or gray-option seeding when conservative canonical options remain available.

## Claim Boundary

Allowed bounded claim:

- Under the frozen S33 artificial protocol, gray within-control options and split-like options were generated and filtered into applicant-visible menus; requester/buyer selected one gray-seeded split action with aggregate note and selected conservative canonical actions in the other accepted runs.

Forbidden claims:

- fraud occurred;
- hidden intent was observed;
- humans or real organizations behave this way;
- gray-option seeding proves safety or risk;
- prompt wording caused the result;
- the result is statistically meaningful;
- the result generalizes to all LLMs;
- the result supports compliance, legal, audit, operational, governance, or safety sufficiency.

## Next Decision

S33 does not justify immediate downstream accountant execution from this PR, because the selected gray split option appeared only once and preserved aggregate context. It is useful as a weak boundary candidate, not as a strong repeated mechanism signal.

If Phase 4 continues, the next mechanism should not merely add more gray options to a menu. A genuinely different mechanism would need to change the organizational decision structure, for example:

- an accept/reject workflow where a gray option is presented as the default proposed packet rather than one option among conservative options;
- a role-local packet handoff where the applicant receives a preformatted operational packet and must decide whether to send it onward;
- a social-provenance mechanism where a named operations peer or senior requester recommends a specific within-control packet structure while preserving traceability.

Any such mechanism must be frozen in a separate protocol before execution and must preserve the within-control / outside-control boundary.
