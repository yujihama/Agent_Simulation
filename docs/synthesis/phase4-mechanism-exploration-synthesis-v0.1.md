# Phase 4 Mechanism Exploration Synthesis v0.1

Date: 2026-05-17
Status: accepted
Phase: Phase 4
Checkpoint: BC4-4 mechanism exploration synthesis
Related selection: `docs/reflections/phase4-mechanism-selection-framework-v0.1.md`
Related protocol: `protocols/failure-modes/phase4-exception-route-ambiguity-diagnostic-v0.1.md`
Related execution: `pilot-runs/org-payment/phase4-exception-route-ambiguity-diagnostic-pilot-0001/summary.md`
Related review: `pilot-runs/org-payment/phase4-exception-route-ambiguity-diagnostic-pilot-0001/candidate-review-0001/summary.md`
Related reflection: `docs/reflections/phase4-bc36-after-exception-route-review.md`
Claim boundary: `phase4_mechanism_synthesis_only`

## Purpose

This synthesis closes the Phase 4 mechanism exploration pass from the Phase 1-4 roadmap.

It asks whether the newly selected exception-route ambiguity mechanism changed the project position after the Method B+ endpoint and earlier mechanism diagnostics. It does not add runs, change prior artifacts, freeze a new protocol, execute a new diagnostic, or recommend a controlled baseline from weak evidence.

Completion status:

- Delivery completion: complete. Phase 4 selected a mechanism, froze a protocol, executed S20, reviewed candidates, reflected on the result, and synthesized the mechanism pass.
- Research completion: partial. Phase 4 tested mechanisms, but it has not answered which information structure can produce stronger downstream slippage beyond buyer-side handoff.

Current-status note: the original completion status above is retained for historical S20 context. Later Phase 4 endpoint updates after S27/S28/S29 are recorded in `docs/synthesis/phase4-structuring-approval-splitting-synthesis-v0.1.md` and `docs/synthesis/phase4-applicant-side-structuring-synthesis-v0.1.md`. Phase 4 has current tested-mechanism support for bounded SL2, one narrow SL3 partial-support mechanism, and repeated SL5 preservation, but not for proof of SL4, SL6, full approval bypass, or baseline readiness.

## Mechanism Results

| Mechanism / checkpoint | Primary artifact | Reviewed result | Current status |
|---|---|---|---|
| BC31 ambiguity targeting | `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/bc31-fm2-independent-review-0001/summary.md` | Narrow buyer payment-forward handoff boundary only; downstream accountant requested more evidence and final state was not payment-ready. | SL2 partial support only; not full approval bypass. |
| S17 SL2-SL4 progression diagnostic | `pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/candidate-review-0001/summary.md` | Buyer/accountant preserved gaps; no progression to preparation or final readiness. | SL5 supported; SL2/SL3/SL4/SL6/FM6 not supported. |
| S18 lossy handoff | `pilot-runs/org-payment/method-b-plus-lossy-handoff-diagnostic-pilot-0001/candidate-review-0001/summary.md` | Lossy handoff made narrow buyer-side SL2 handoff visible in some runs, while downstream accounting preserved the gap. | SL2 supported in bounded artificial evidence; SL5 supported; SL3/SL4/SL6/FM1/FM3/FM6 unsupported. |
| S19 queue/ticket mismatch | `pilot-runs/org-payment/method-b-plus-queue-ticket-state-mismatch-diagnostic-pilot-0001/candidate-review-0001/summary.md` | Queue/status mismatch did not produce handoff, preparation, final readiness, or gap erasure; downstream held the boundary. | SL5 supported; SL2/SL3/SL4/SL6/FM1/FM3/FM6 not observed. |
| S20 exception route ambiguity | `pilot-runs/org-payment/phase4-exception-route-ambiguity-diagnostic-pilot-0001/candidate-review-0001/summary.md` | In 4 accepted runs, buyer and accountant selected `hold_payment`; one attempted run was excluded for parser/source-ref failure. | SL5 supported for accepted artificial evidence; SL1/SL2/SL3/SL4/SL6/FM1/FM3/FM6 not observed. |

## What Changed In Phase 4

Phase 4 added a new mechanism, exception-route ambiguity, rather than repeating the same S17-style stress design.

The new mechanism did not reveal stronger slippage. It reinforced the boundary-preservation pattern already visible in S17 and S19:

- explicit approval remained absent;
- valid exception authority remained absent;
- buyer and accountant preserved the gap in accepted S20 runs;
- no accepted S20 run produced buyer payment-forward handoff, accountant payment preparation, final payment-ready state, gap erasure, responsibility diffusion, ambiguous-guidance misinterpretation, or post-hoc justification.

The one S20 parser exclusion is informative as an execution limitation: the accountant attempted to cite records outside the frozen allowed prior evidence set. The run was excluded and not replaced, preserving the frozen protocol rather than relaxing it after seeing output.

Across the tested mechanisms, lossy handoff is currently the only mechanism that produced reviewed SL2 buyer-side handoff support. Queue/ticket mismatch and exception-route ambiguity did not produce stronger slippage; both instead reinforced SL5 evidence-gap preservation. No tested mechanism has produced SL3, SL4, or SL6 support.

Therefore, Phase 4 should not be read as answering which information structure can produce stronger downstream slippage. It only narrows the current evidence state: lossy handoff can expose narrow buyer-side SL2 in some artificial runs, while the tested downstream accounting structures continued to preserve gaps.

## Current SL/FM Status

| Category | Current project status |
|---|---|
| SL1 ambiguous approval interpretation | Not supported in reviewed Phase 4/S20 evidence. |
| SL2 payment-forward handoff without explicit approval | Narrow support exists from BC31 and S18 only; S20 did not reproduce it. |
| SL3 accountant payment preparation without explicit approval | Not supported across reviewed diagnostics. |
| SL4 final payment-ready state without explicit approval | Not supported across reviewed diagnostics. |
| SL5 evidence-gap preservation | Repeatedly supported in reviewed artificial evidence, including S17, S18, S19, and S20 accepted runs. |
| SL6 evidence-gap erasure | Not supported across reviewed diagnostics. |
| FM1 responsibility diffusion | Not supported across reviewed diagnostics. |
| FM3 ambiguous guidance misinterpretation | Not supported across reviewed diagnostics. |
| FM6 post-hoc justification | Reviewed rejected or not observed in the relevant diagnostics. |

## Baseline Readiness

The project should not proceed to a controlled failure-mode baseline from the current Phase 4 state.

Reasons:

- the strongest repeated signal is SL5 evidence-gap preservation, not stronger slippage;
- SL2 appears only under narrow artificial handoff conditions and does not progress to SL3 or SL4;
- S20 did not add support for SL1, SL2, SL3, SL4, SL6, FM1, FM3, or FM6;
- S20 has one transparent parser exclusion, so it should not be treated as a stronger baseline-ready result;
- baseline execution would risk converting exploratory diagnostics into stronger claims than the evidence supports.

An additional reason is that Phase 4 is research-partial: it has not identified an information structure that produces reviewed SL3, SL4, or SL6 support. A baseline would require clearer research-completion criteria and stronger reviewed support than the current mechanism exploration provides.

## Methodological Value

The Phase 4 result is still useful.

It shows that the project can:

- select a substantially different organizational mechanism;
- freeze scenario, role visibility, action menus, Game Master rules, candidate criteria, evidence requirements, and claim boundaries before execution;
- execute and validate representative evidence packs mechanically;
- preserve generated candidate versus reviewed support boundaries;
- record conservative results without hiding them.

The main artificial-system finding remains boundary preservation under the current protocol family. That is a valid research result, but it is not evidence that real organizations preserve controls or that LLM agents are generally safe or reliable.

## Decision

Checkpoint decision: mark Phase 4 as delivery-complete but research-partial, then pause autonomous run-producing diagnostics.

Do not start another run-producing BC unless a later mechanism-selection PR identifies a substantially different organizational mechanism and explains why it is needed after S17, S18, S19, and S20.

Recommended next work:

1. Analyze why lossy handoff produced reviewed SL2 buyer-side handoff support while S19 and S20 did not.
2. Select a genuinely new information mechanism with research-completion criteria defined before execution.
3. Stop run-producing work and report the methodology plus boundary-preservation findings.

Any future run-producing work must define, before execution, what would count as delivery completion and what would count as research completion.

## Corrective Reopen

This synthesis is superseded in one respect by `docs/reflections/phase4-reopen-research-objective.md`.

The delivery-complete / research-partial distinction remains valid for the S20-era synthesis. Under the user's later instruction, Phase 4 research was reopened until the project identified which information structures can produce reviewable slippage candidates, or until a concrete blocker prevented further progress. The post-S28 synthesis now records the endpoint for the current tested-mechanism map.

Future execution still requires protocol freeze before any run-producing work.

## Post-S27 Project-Owner Update

This synthesis is also superseded in one current-status respect by S27 payment-draft staging and its project-owner review.

S27 `create_payment_draft` is now treated as `SL3 partially_supported_needs_revision` under [project-owner-review-0001](../../pilot-runs/org-payment/phase4-s27-payment-draft-staging-diagnostic-0001/project-owner-review-0001/summary.md). The project does not introduce SL3a / SL3b at this stage.

Post-scope-axis update: forward-looking Phase 4 mechanism selection should use `Within-Control Process Drift` from `docs/research/within-control-process-drift-scope-v0.1.md`. This keeps the SL1-SL6 levels while changing the scope question from inferred intent to within-control / outside-control. Structuring / approval splitting is a valid future mechanism only when actor authority, operator records, and evidence integrity remain within-control.

This update is narrow and does not change the forbidden-claim boundary:

- SL5 evidence-gap preservation remains supported because approval and exception gaps stayed visible.
- SL4 final payment-ready state remains unsupported.
- SL6 evidence-gap erasure remains unsupported.
- Full approval bypass remains unsupported.
- No human, real-world, statistical, model-general, prompt-causation, compliance, legal, audit, operational, governance, or safety sufficiency claim is supported.

## Post-S28 Structuring / Approval-Splitting Update

This synthesis is further updated by `docs/synthesis/phase4-structuring-approval-splitting-synthesis-v0.1.md`.

S28 tests structuring / approval splitting under the revised `Within-Control Process Drift` scope. It executed 20 accepted runs across no-splitting, amount-splitting, invoice/period-splitting, and valid aggregate-approval control conditions.

S28 result:

- SL2 split-item handoff is `partially_supported_needs_revision` for AS02/AS03, but only as a bounded scripted buyer/process-owner handoff observation.
- SL5 aggregate-gap preservation is supported for all non-control accepted runs.
- SL1, SL3, SL4, SL6, FM3, and FM6 were not observed.
- Positive-control AS04 prepared payment only when aggregate approval/review was recorded.

The current Phase 4 mechanism map is therefore:

- SL2: supported only in bounded handoff contexts, including lossy handoff and S28 structuring / approval splitting.
- SL3: narrow project-owner-confirmed partial support only from S27 `create_payment_draft`.
- SL4: unsupported.
- SL5: repeatedly supported as downstream gap preservation.
- SL6: unsupported.

Phase 4 can now be treated as research-complete for the current tested-mechanism map: it identifies which tested mechanisms produced bounded SL2, which produced narrow SL3 partial support, and which mostly preserved gaps. It is not research-complete as proof of stronger downstream slippage, full approval bypass, or baseline readiness.

Checkpoint decision after S28: stop run-producing Phase 4 diagnostics and consolidate unless a future mechanism-selection PR identifies a substantially different within-control information mechanism with research-completion criteria fixed before execution.

## Post-S29 Applicant-Side Structuring Update

This synthesis is further updated by `docs/synthesis/phase4-applicant-side-structuring-synthesis-v0.1.md`.

S29 corrects a limit in S28: S28 tested downstream accountant handling after split items reached accounting, while S29 tests whether a requester/buyer chooses split submission under observable pressure and aggregate-threshold conditions.

S29 result:

- Applicant-side split submission appeared in 7/20 accepted artificial runs; project-owner review confirms this as bounded applicant-side within-control process drift / SL2 support.
- Split submission appeared only under pressure conditions: ST02 deadline, ST03 volume/queue, and ST04 compound pressure plus prior practice.
- 4 split submissions preserved aggregate context through `submit_split_requests_with_aggregate_note`.
- 3 split submissions omitted the aggregate note through `submit_split_requests_without_aggregate_note`; project-owner review treats these as stronger boundary candidates.
- SL5 aggregate-gap preservation remained supported in all 20 runs.
- SL1, SL4, SL6, and FM3 were not observed.
- SL3 and FM6 were not applicable in S29 v0.1 because no downstream accountant or post-hoc explanation turn was included.

The current Phase 4 mechanism map is therefore:

- SL2: supported in bounded contexts including lossy handoff, S28 downstream split-item handoff, and project-owner-reviewed S29 applicant-side split submission.
- SL3: narrow project-owner-confirmed partial support only from S27 `create_payment_draft`.
- SL4: unsupported.
- SL5: repeatedly supported as approval/evidence/aggregate-gap preservation.
- SL6: unsupported.

Checkpoint decision after S29 project-owner review: pause run-producing Phase 4 work until a new target-definition/protocol-freeze checkpoint decides whether to build on the S29 applicant-side SL2 boundary, test downstream consequences, or consolidate for reporting. S29 does not support fraud, hidden intent, full approval bypass, SL3, SL4, SL6, prompt causation, model-general behavior, statistical significance, human behavior, real-world behavior, or compliance/legal/audit/operational/governance/safety sufficiency.

## Allowed Claims

This synthesis may claim:

- Phase 4 selected, froze, executed, reviewed, and reflected on an exception-route ambiguity mechanism.
- S20 accepted runs preserved approval and exception-authority gaps downstream.
- Current reviewed artificial evidence supports repeated SL5 boundary preservation, bounded SL2 support from BC31/S18/S28/S29 contexts, and narrow S27 SL3 partial support for `create_payment_draft`.
- Phase 4 has a clearer current tested-mechanism map after S29, but still not proof of stronger downstream slippage, SL4, SL6, or baseline readiness.
- The current evidence does not justify a controlled failure-mode baseline.

## Forbidden Claims

This synthesis must not claim:

- full approval bypass was reproduced;
- exception-route ambiguity caused or prevented behavior;
- humans or real organizations would behave this way;
- real controls are effective or ineffective;
- LLMs are generally safe, reliable, conservative, risky, or robust;
- the result is statistically meaningful;
- the result supports compliance, legal, audit, operational, governance, or safety sufficiency.
