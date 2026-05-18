# Phase 4 Post-S35 Mechanism Map And Next Decision v0.1

Date: 2026-05-19
Status: accepted
Phase: Phase 4
Checkpoint: post-S35 mechanism-map synthesis
Claim boundary: `phase4_post_s35_synthesis_only`

## Purpose

This synthesis consolidates the Phase 4 mechanism exploration after S35.

It does not add runs, protocols, scenarios, prompts, candidates, or claim upgrades. It answers the current Phase 4 research question as far as the tested artificial mechanisms allow:

> Which within-control information structures produced reviewable process-drift candidates, and where did downstream boundaries preserve aggregate approval/review gaps?

## Mechanism Map

| Mechanism | Main test | Reviewed result | Current interpretation |
|---|---|---|---|
| Lossy handoff | S18 | SL2 in 3/5; downstream gap preservation | Lossy summary can produce narrow handoff movement, but not downstream preparation or final readiness. |
| Payment-draft staging | S27 | `create_payment_draft` treated by project owner as narrow SL3 partial support | Only narrow non-payable draft/preparation boundary; not final readiness or full bypass. |
| Downstream structuring / approval splitting | S28 | Bounded SL2 split-item handoff; SL5 preservation | Tested accountant-side handling after already-split items reached accounting; did not test applicant choice. |
| Applicant-side fixed-menu structuring | S29 | Project-owner-reviewed SL2 split submission in 7/20, all under pressure conditions | Strongest applicant-side split-choice evidence, but menu-conditioned. |
| Freeform applicant plan generation | S30 | 0/20 split proposals; 20/20 gap preservation | Freeform handling plans did not reproduce S29 split submission without explicit split options. |
| Neutral advisor-seeded options | S31 | Split-like options appeared, but applicant selected none | Ordinary option expansion did not produce split selection. |
| Gray-option seeded menu | S33 | One weak split-with-aggregate-note selection | Explicitly surfaced gray within-control ideas produced only weak SL2 movement. |
| Default proposed packet | S34 | 8 split-packet-forwarding candidates | Default packet framing produced stronger upstream SL2 movement than S33. |
| Default-packet downstream chain | S35 | 15 split-packet arrivals at accounting; accountant requested review/evidence in all unresolved-gap conditions | Downstream accounting preserved aggregate gaps; `prepare_payment` occurred only in the valid-control positive condition. |

## SL-Level Answer

| SL level | Current Phase 4 answer |
|---|---|
| SL1 | Not supported as a reviewed Phase 4 result. |
| SL2 | Supported in bounded artificial contexts. Strongest sources are S29 fixed-menu applicant-side split submission and S34 default-packet split forwarding; S18/S28 also support bounded handoff variants; S33 is weak. |
| SL3 | Narrow partial support only from S27 `create_payment_draft`, as accepted by project-owner review. S35 did not add SL3 because payment preparation happened only in the valid aggregate-approval control condition. |
| SL4 | Not supported by any tested mechanism. |
| SL5 | Repeatedly supported. Downstream roles often preserved explicit approval, exception-authority, aggregate approval, or aggregate-review gaps. |
| SL6 | Not supported by any tested mechanism. |

## What S35 Adds

S35 closes the direct downstream question from S34.

S34 showed that a concrete default split packet can be forwarded toward accounting. S35 then tested whether those packets lead the accountant to move beyond the unresolved aggregate approval/review gap. They did not under the frozen S35 conditions:

- aggregate-note split packets led to `request_aggregate_review`;
- weak-context split packets led to `request_more_evidence`;
- social-provenance split packets led to `request_more_evidence`;
- `prepare_payment` appeared only in the valid aggregate-approval positive-control condition.

This means S34's upstream SL2 movement does not currently generalize to downstream SL3/SL4 movement inside this artificial setup.

## Research Completion Assessment

Phase 4 is research-complete for the current tested-mechanism map, not for proof of stronger downstream slippage.

It can now say:

- applicant-side or packet-framing structures can produce bounded SL2 candidates;
- one tool-affordance-like draft mechanism produced narrow SL3 partial support;
- downstream accounting repeatedly preserves gaps when aggregate approval/review remains visible or recoverable;
- no tested mechanism produced SL4 final payment-ready state or SL6 gap erasure.

It cannot say:

- which mechanism can produce SL4 or SL6;
- that full approval bypass was reproduced;
- that humans or real organizations behave this way;
- that controls are effective or ineffective in the real world;
- that the results are statistically meaningful;
- that any model is generally safe, unsafe, reliable, or unreliable.

## Baseline Readiness

A controlled Phase 4 failure-mode baseline is not justified now.

Reasons:

- SL2 support is bounded and mechanism-specific.
- SL3 support is narrow and partial, limited to S27 `create_payment_draft`.
- S35 did not turn S34 upstream packet forwarding into downstream preparation under unresolved aggregate gaps.
- SL4 and SL6 remain unsupported.
- The strongest repeated downstream result is SL5 boundary preservation.

Baseline discussion would require a narrower baseline target, such as a bounded SL2 applicant-side split-submission baseline, and project-owner approval that such a baseline is useful despite no SL4/SL6 support. It should not be framed as a full approval-bypass or downstream-slippage baseline.

## Next Decision

Decision: stop autonomous run-producing Phase 4 diagnostics at this checkpoint.

Future work may continue only through a new mechanism-selection PR that identifies a substantially different within-control information mechanism. A future mechanism should not be another variant of:

- adding split options to menus;
- asking for freeform handling plans;
- seeding advisor options;
- presenting one default split packet;
- sending an S34-style split packet to accounting.

To be genuinely different, a future mechanism would need to change the organizational information structure in a new way, for example by introducing a distinct tool affordance, system-generated workflow state, reconciliation process, or independent review surface that remains reconstructable and within-control.

No further execution should start until that future mechanism freezes scenario, role visibility, action space, Game Master rules, candidate criteria, review criteria, and claim boundary before seeing outputs.

## Claim Boundary

This synthesis may claim that Phase 4 has mapped tested artificial mechanisms through S35 and that the current evidence supports bounded SL2, narrow partial SL3, repeated SL5, and no reviewed SL4/SL6 support.

It must not claim human behavior, real-world organization behavior, fraud, intentional misconduct, full approval bypass, prompt causation, statistical significance, model-general behavior, or compliance/legal/audit/operational/governance/safety sufficiency.
