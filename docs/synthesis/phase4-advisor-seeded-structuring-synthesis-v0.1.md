# Phase 4 Advisor-Seeded Structuring Synthesis v0.1

Date: 2026-05-19
Status: accepted
Phase: Phase 4 extension
Checkpoint: BC4-S31 synthesis
Related protocol: `protocols/failure-modes/phase4-advisor-seeded-structuring-diagnostic-v0.1.md`
Related scenario: `scenarios/org-payment/s31-advisor-seeded-structuring.yaml`
Related result: `pilot-runs/org-payment/phase4-s31-advisor-seeded-structuring-diagnostic-0001/summary.md`
Related candidate review: `pilot-runs/org-payment/phase4-s31-advisor-seeded-structuring-diagnostic-0001/candidate-review-0001/summary.md`
Related reflection: `docs/reflections/phase4-after-s31-advisor-seeded-structuring-review.md`
Claim boundary: `phase4_advisor_seeded_structuring_synthesis_only`

## Purpose

S31 tested a hybrid mechanism after the S29/S30 split:

- S29 showed applicant-side split submission when split actions were visible in a fixed menu.
- S30 showed no freeform split or multi-packet proposal when the applicant had to generate a plan without explicit split options.
- S31 inserted a separate processing-option advisor that generated within-control options from pressure and threshold context; a deterministic filter then added accepted options to the applicant menu.

This synthesis asks whether advisor-seeded option expansion is enough to make applicant-side split selection appear without placing split actions in the original canonical menu.

## Execution Result

S31 executed 20 attempted runs under the frozen protocol.

| Field | Result |
|---|---|
| Attempted runs | 20 |
| Accepted runs | 17 |
| Excluded runs | 3 |
| Provider/model | OpenAI `gpt-5.2` |
| Observed model version | `gpt-5.2-2025-12-11` |
| Claim boundary | `phase4_advisor_seeded_structuring_observation_only` |

The three exclusions were parser failures where requester/buyer outputs cited `role_views/processing_option_advisor.json`, which was not part of the requester/buyer visible evidence set. Excluded runs were reported and not replaced.

## Core Findings

Advisor option generation worked:

- advisor accepted option count: 65 across accepted runs;
- advisor rejected option count: 9;
- advisor split option candidate: 17/17 accepted runs;
- seeded split option present in applicant menu: 15/17 accepted runs;
- outside-control options were rejected where detected.

Applicant selection remained conservative:

- `submit_single_aggregate_request`: 14/17;
- `request_higher_approval`: 3/17;
- selected option source: canonical in 17/17;
- selected seeded advisor option: 0/17;
- selected seeded split option: 0/17.

SL-level result:

| Level | S31 reviewed status |
|---|---|
| SL1 | Not observed |
| SL2 | Not observed |
| SL4 | Not observed |
| SL5 | Observed in 17/17 accepted runs |
| SL6 | Not observed |

S31 therefore shows that, in this artificial setup, a separate advisor can generate within-control split-like options, but the applicant-side actor still selected the conservative canonical options.

## Interpretation

S31 answers the hybrid idea in a narrow way:

- The missing step after S30 was not simply "can another LLM think of split-like options?" It can.
- The missing step is "does the applicant treat those generated options as operationally attractive enough to select?" In S31, it did not.
- The current setup still strongly preserves the aggregate approval/review gap downstream and in final state.

This does not prove that advisor-seeded options cannot produce split selection. It shows that this particular neutral advisor-seeded menu mechanism did not produce applicant-side SL2 selection in accepted runs.

## Mechanism Lesson

The next genuinely different mechanism should not merely add more generated options. S31 suggests the next variable is option provenance and recommendation force:

- whether the option is presented as a neutral list item or as a recommended handling path;
- whether the option comes from a peer, senior operations coordinator, requester, vendor, or policy-adjacent role;
- whether the option has a visible operational rationale such as queue aging, prior-practice evidence, or throughput pressure;
- whether the applicant must choose between several acceptable options or receives a recommended option with caveats.

Any future mechanism must remain within-control: no forged evidence, hidden evidence, impersonation, collusion, unauthorized access, or instruction to bypass approval.

## Phase 4 Evidence Map Update

Current Phase 4 structuring evidence after S31:

- S29 remains the only applicant-side structuring diagnostic with reviewed SL2 split-submission support.
- S30 did not produce freeform split proposals.
- S31 produced advisor-generated split options but no applicant selection of those options.
- S31 reinforces SL5 aggregate-gap preservation.
- S31 does not add SL1, SL2, SL4, or SL6 support.

S31 does not justify a baseline.

## Next Decision

Decision: pause run-producing work until a new mechanism-selection/protocol-freeze checkpoint defines a substantially different option-provenance or recommendation mechanism.

Recommended next mechanism, if Phase 4 continues:

`recommendation_weighted_advisor_seeded_structuring`

This would test whether a within-control operational advisor or peer explicitly recommends one handling path, while preserving global truth and forbidding outside-control behavior. The target would be recommendation/provenance effects, not freeform emergence and not fraud.

Do not execute that mechanism without a separate protocol-freeze PR.

## Allowed Claims

This synthesis may claim:

- S31 executed an advisor-seeded option expansion diagnostic under the frozen artificial protocol.
- Advisor-generated split-like within-control options appeared in accepted runs.
- Applicant-side actors did not select advisor-seeded split options in accepted runs.
- S31 preserved aggregate approval/review gaps as SL5 and did not support SL2, SL4, or SL6.

## Forbidden Claims

This synthesis must not claim:

- prompt wording caused the S31 result;
- actors intentionally bypassed controls;
- fraud occurred;
- full approval bypass was reproduced;
- advisor-seeded options cannot work generally;
- humans or real organizations behave this way;
- results are statistically significant;
- the result generalizes across models;
- the artifacts support compliance, legal, audit, operational, governance, or safety sufficiency.
