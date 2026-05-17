# Method B+ Iterative Targeting Synthesis v0.1

Date: 2026-05-17
Status: accepted
Phase: Method B+
Checkpoint: iterative targeting synthesis updated after BC31 FM2 independent review
Claim boundary: `method_b_plus_iterative_synthesis_only`

## Scope

This synthesis integrates the Method B+ iterative targeting work through the S17 SL2-SL4 control-slippage progression diagnostic execution and review. It asks what the project can currently say about targeted failure-mode observability in artificial org-payment runs after repeated protocol-freeze, execution, review, and reflection cycles.

This synthesis does not add new LLM execution, new scenarios, prompt changes, action-menu changes, Game Master changes, event taxonomy changes, metric changes, human-review judgments, or statistical analysis.

## Source Artifacts

| Area | Primary inputs |
|---|---|
| Failure-mode definitions | `protocols/failure-modes/failure-mode-taxonomy-v0.1.md` |
| Control-slippage taxonomy, protocol, and S17 diagnostic | `protocols/failure-modes/non-intentional-control-slippage-taxonomy-v0.1.md`; `docs/synthesis/non-intentional-control-slippage-map.csv`; `docs/reflections/method-b-plus-bc36-after-bc31-fm2-independent-review.md`; `protocols/failure-modes/method-b-plus-control-slippage-progression-diagnostic-v0.1.md`; `scenarios/org-payment/s17-control-slippage-progression-diagnostic.yaml`; `prompts/org-payment/method-b-plus-control-slippage-progression-addendum-v0.1.md`; `pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/summary.md`; `pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/candidate-review-0001/summary.md`; `docs/reflections/method-b-plus-bc36-after-slippage-progression-review.md` |
| Lossy handoff mechanism diagnostic | `docs/synthesis/method-b-plus-boundary-preservation-synthesis-v0.1.md`; `docs/reflections/method-b-plus-next-mechanism-selection.md`; `protocols/failure-modes/method-b-plus-lossy-handoff-diagnostic-v0.1.md`; `scenarios/org-payment/s18-lossy-handoff-control-slippage.yaml`; `prompts/org-payment/method-b-plus-lossy-handoff-addendum-v0.1.md`; `pilot-runs/org-payment/method-b-plus-lossy-handoff-diagnostic-pilot-0001/summary.md`; `pilot-runs/org-payment/method-b-plus-lossy-handoff-diagnostic-pilot-0001/candidate-review-0001/summary.md`; `docs/reflections/method-b-plus-bc36-after-lossy-handoff-review.md` |
| Queue/ticket state mismatch diagnostic | `docs/synthesis/method-b-plus-mechanism-iteration-synthesis-v0.1.md`; `protocols/failure-modes/method-b-plus-queue-ticket-state-mismatch-diagnostic-v0.1.md`; `scenarios/org-payment/s19-queue-ticket-state-mismatch-control-slippage.yaml`; `prompts/org-payment/method-b-plus-queue-ticket-state-mismatch-addendum-v0.1.md`; `pilot-runs/org-payment/method-b-plus-queue-ticket-state-mismatch-diagnostic-pilot-0001/summary.md`; `pilot-runs/org-payment/method-b-plus-queue-ticket-state-mismatch-diagnostic-pilot-0001/candidate-review-0001/summary.md`; `docs/reflections/method-b-plus-bc36-after-queue-ticket-state-mismatch-review.md` |
| Method B baseline synthesis | `docs/synthesis/method-b-synthesis-v0.1.md`; `docs/synthesis/method-b-failure-mode-status.csv` |
| BC28 FM6 review | `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/fm6-candidate-review-0001/summary.md` |
| BC31 ambiguity targeting | `protocols/failure-modes/method-b-plus-ambiguity-interpretation-v0.1.md`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/summary.md`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/ambiguity-candidate-review-0001/summary.md`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/bc31-fm2-independent-review-0001/summary.md` |
| BC37-C approval-bypass stress | `protocols/failure-modes/method-b-plus-approval-bypass-stress-v0.1.md`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/summary.md`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/candidate-review-0001/summary.md` |
| BC32 responsibility boundary | `protocols/failure-modes/method-b-plus-responsibility-boundary-v0.1.md`; `pilot-runs/org-payment/method-b-plus-responsibility-boundary-pilot-0001/summary.md`; `docs/reflections/method-b-plus-bc36-after-bc32-execution.md` |
| BC35 evidence-gap diagnostic | `protocols/failure-modes/method-b-plus-evidence-gap-erasure-diagnostic-v0.1.md`; `pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/summary.md`; `pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/candidate-review-0001/summary.md`; `docs/reflections/method-b-plus-bc36-after-bc35-review.md` |

## Synthesis Summary

Method B+ successfully exercised the intended iterative loop:

1. Freeze a targeted protocol before execution.
2. Execute a bounded artificial pilot.
3. Review generated candidates before support.
4. Reflect before selecting the next checkpoint.

The work improved the project's ability to make narrow, reviewable distinctions among generated candidates, rejected candidates, partial support, and not-observed outcomes. It did not produce a fully supported Method B+ failure-mode finding.

The strongest reviewed signal remains one narrow BC31 FM2 boundary observation: a buyer sent a payment request toward accounting while explicit approval was absent, but the accountant requested more evidence and the final state did not become payment-ready. A second-pass proxy review independently re-read the source evidence and confirmed the same partial-support boundary. This is now better described as a narrow non-intentional control slippage observation: SL2 buyer payment-forward handoff without explicit approval plus SL5 downstream evidence-gap preservation. It is not full approval-bypass support.

Subsequent stress and diagnostic pilots were mechanically valid but conservative:

- BC37-C: buyer/accountant held payment in all runs; FM6 candidates were reviewed and rejected.
- BC32: approver approved in all runs; no generated FM1/FM2/FM5/FM6 candidates.
- BC35: buyer/accountant held payment in all runs; G001/G002 remained visible; FM6 candidates were reviewed and rejected.
- S17 SL2-SL4 progression diagnostic: buyer/accountant held payment in all runs; SL2, SL3, SL4, SL6, and FM6 were not observed; SL5 evidence-gap preservation was supported for the reviewed artificial evidence.
- S18 lossy handoff diagnostic: buyer selected `submit_payment_request` in 3 runs and `hold_payment` in 2 runs; accountant selected `hold_payment` in all runs; SL2 and SL5 were supported for reviewed artificial evidence, while SL3, SL4, SL6, FM1, FM3, and FM6 were not observed.
- S19 queue/ticket state mismatch diagnostic: buyer and accountant selected `hold_payment` in all runs despite readiness-like ticket states; SL5 was supported for reviewed artificial evidence, while SL2, SL3, SL4, SL6, FM1, FM3, and FM6 were not observed.

The repeated conservative outcomes are informative. They show that the current artificial setup, prompts, action menus, and deterministic Game Master can preserve approval and evidence boundaries. They do not prove that the failure modes are absent generally.

## Failure-Mode Status

The compact status table is [method-b-plus-failure-mode-status.csv](method-b-plus-failure-mode-status.csv).

| Failure mode | Current Method B+ status | Plain-language meaning |
|---|---|---|
| FM1 responsibility diffusion | `not_observed_in_targeted_scope` | BC32, S18, and S19 did not show roles blurring responsibility in a way that satisfied the generated candidate criteria. |
| FM2 approval bypass | `supported_sl2_control_slippage_boundary_observation_without_sl3_or_sl4` | BC31 partially supports a narrow SL2 buyer handoff concern, and S18 supports three reviewed SL2 buyer handoff observations. S17 did not reproduce SL2, and no Method B+ artifact supports SL3 accountant preparation or SL4 final payment readiness without approval. |
| FM3 ambiguous guidance misinterpretation | `reviewed_rejected_or_not_observed` | The BC31 ambiguous-guidance candidate was reviewed and rejected; S18 and S19 did not generate FM3 support. |
| FM4 pressure normalization | `not_directly_targeted_in_method_b_plus_iteration` | Method B+ did not run a dedicated pressure-normalization target after the earlier Method B synthesis. |
| FM5 evidence-gap erasure | `not_observed_in_targeted_scope_with_repeated_gap_preservation` | BC35, S17, S18, and S19 preserved G001/G002-style gaps in their accepted runs; no SL6 support exists. |
| FM6 post-hoc justification | `reviewed_rejected_across_generated_method_b_plus_candidates` | Generated FM6 candidates from BC28, BC31, BC37-C, and BC35 were reviewed and rejected in their reviewed artificial evidence scopes. |

## What Method B+ Can Claim

| Claim level | Claim | Evidence | Boundary |
|---|---|---|---|
| `workflow_claim` | Method B+ implemented an iterative freeze-execute-review-reflect workflow for targeted failure-mode diagnostics. | BC31, BC37-C, BC32, and BC35 artifacts. | Workflow and artifact claim only. |
| `partial_boundary_observation` | BC31 contains one partially supported non-intentional control slippage observation: SL2 buyer handoff without explicit approval plus SL5 evidence-gap preservation. | `METHOD-B-PLUS-BC31-REVIEW-0001`; `METHOD-B-PLUS-BC31-FM2-INDEPENDENT-REVIEW-0001`; `non-intentional-control-slippage-map.csv`. | Narrow reviewed artificial evidence only; not full approval bypass, SL3 preparation, SL4 payment readiness, or independent multi-reviewer human validation. |
| `reviewed_rejection_claim` | Generated FM6 candidate rows in Method B+ reviewed scopes were rejected. | BC28, BC31, BC37-C, and BC35 candidate reviews. | Rejection applies only to reviewed candidate rows. |
| `negative_diagnostic_observation` | BC37-C, BC32, BC35, S17, and S19 produced conservative or boundary-preserving paths under their frozen protocols. | Curated pilot summaries, candidate reviews, and reflections. | Not evidence that failure modes are absent generally. |
| `next_step_decision` | After S17, targeted execution should pause for synthesis or external/project-owner review of the BC31 boundary if stronger status is needed. | BC36 reflection after S17. | Research-planning claim only. |

## What Method B+ Cannot Claim

Method B+ cannot claim that:

- human society has been reproduced;
- real organizations would behave similarly;
- responsibility diffusion, approval bypass, ambiguous guidance misinterpretation, pressure normalization, evidence-gap erasure, or post-hoc justification has been proven;
- the BC31 partial handoff observation is a full approval-bypass finding;
- the BC31 partial handoff observation supports SL3 payment preparation or SL4 final payment-ready state;
- S17 or S19 disproves SL2, SL3, SL4, SL6, or FM6 generally;
- generated candidates are support before review;
- rejected FM6 candidates prove FM6 is absent generally;
- prompt wording caused conservative or candidate outcomes;
- the model has a general behavioral pattern;
- results are statistically meaningful;
- the artifacts provide compliance, legal, audit, or operational sufficiency.

## Review Scope

All Method B+ candidate reviews in this synthesis are delegated reviews by Codex under project-owner authorization unless otherwise stated. The BC31 FM2 partial-support row now has a Codex independent second-pass proxy review, which is useful for internal claim control and candidate triage. It is still not independent multi-reviewer human validation and carries no inter-rater reliability claim.

The reviewed candidate/support boundary is still useful:

- generated candidates are not treated as support;
- reviewed rejected candidates remain rejected;
- the single BC31 partial support is explicitly narrow and reframed as control slippage rather than upgraded into full failure-mode support, even after second-pass confirmation.

## Interpretation

The current evidence suggests a design pattern, not a behavioral law: the artificial setup tends to preserve approval and evidence boundaries when the protocol makes missing approval, missing evidence, or hold options explicit. That pattern is a property of these artificial runs and artifacts. It should be treated as a constraint on future experimental design, not as evidence about humans or real organizations.

The main research value of Method B+ is therefore methodological:

- it shows which failure-mode candidates can be generated and reviewed;
- it shows that many generated candidates are false positives when the action itself is conservative;
- it shows that handoff/preparation/final-state distinctions matter for approval-bypass claims;
- it shows that evidence-gap preservation must be tracked explicitly across actions, Game Master decisions, final state, metrics, and post-hoc explanations.

## Recommended Next Options

Do not freeze a Method B+ controlled baseline from the current evidence. The only stronger reviewed support remains narrow SL2 buyer handoff support from BC31 and S18, both paired with downstream gap preservation. Later targeted pilots, including S17 and S19, did not extend it to accounting preparation or final payment readiness.

Useful next options are:

1. Pause targeted execution and update the broader project synthesis to reflect that S17 and S19 produced conservative boundary preservation and S18 produced SL2 only.
2. Freeze an external or project-owner human-review protocol for the BC31 partial FM2/SL2 observation if stronger reviewed-evidence status is needed.
3. Design a genuinely new mechanism only if the next research question can be frozen before execution without chasing the S17 conservative result.
4. Run a second-domain post-hoc diagnostic only after freezing post-hoc explanation requirements that the earlier expense-reimbursement pilot lacked.

## Checkpoint Decision

Checkpoint decision: do not proceed to a Method B+ baseline yet.

Rationale:

- no fully supported Method B+ failure-mode finding exists;
- generated FM6 candidates have repeatedly failed review;
- the only partial support is too narrow for baseline execution, even after second-pass proxy confirmation;
- S17 and S19 produced no SL2, SL3, SL4, SL6, or FM6 support and supported only SL5 gap preservation;
- S18 produced SL2 but no SL3, SL4, SL6, FM1, FM3, or FM6 support;
- additional targeted execution should pause until a periodic synthesis records what the mechanism iterations have and have not added.

## Claim Boundary

This synthesis supports only bounded artificial-system and workflow claims about the Method B+ evidence currently committed to this repository.

It does not claim human behavior, real-world organization behavior, prompt causation, model-general behavior, statistical significance, compliance sufficiency, legal sufficiency, audit sufficiency, operational sufficiency, or completed social-chaos pseudo-reproduction.
