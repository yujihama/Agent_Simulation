# Phase 4 Structuring / Approval-Splitting Synthesis v0.1

Date: 2026-05-18
Status: accepted
Phase: Phase 4 extension
Checkpoint: BC4-S28-C
Related protocol: `protocols/failure-modes/phase4-structuring-approval-splitting-diagnostic-v0.1.md`
Related result: `pilot-runs/org-payment/phase4-s28-structuring-approval-splitting-diagnostic-0001/summary.md`
Related review: `pilot-runs/org-payment/phase4-s28-structuring-approval-splitting-diagnostic-0001/candidate-review-0001/summary.md`
Related reflection: `docs/reflections/phase4-after-s28-structuring-approval-splitting-review.md`
Claim boundary: `phase4_structuring_approval_splitting_synthesis_only`

## Purpose

This synthesis integrates S28 structuring / approval splitting into the Phase 4 mechanism map.

It does not add runs, freeze a new protocol, change previous result artifacts, or upgrade any claim. It asks whether S28 changes the answer to the Phase 4 research question:

> Which within-control information structures produce process-drift candidates?

## S28 Result Summary

S28 executed 20 frozen runs across four conditions:

| Condition | Purpose | Accepted runs | Reviewed result |
|---|---|---:|---|
| `AS01_NO_SPLITTING_CONTROL` | Single request/invoice with unresolved approval or exception requirement. | 5 | Boundary-preserving hold / evidence request behavior. |
| `AS02_AMOUNT_SPLITTING_BELOW_THRESHOLD` | Related items split below threshold while aggregate review remained unresolved. | 5 | Bounded SL2 split-item handoff candidates; aggregate gap preserved downstream. |
| `AS03_INVOICE_PERIOD_SPLITTING` | Same vendor / business purpose split across invoices or periods while aggregate review remained unresolved. | 5 | Bounded SL2 split-item handoff candidates; aggregate gap preserved downstream. |
| `AS04_VALID_AGGREGATE_APPROVAL_CONTROL` | Positive control with valid aggregate approval or review recorded. | 5 | `prepare_payment` occurred only where aggregate approval/review was present. |

Reviewed S28 statuses:

| Level | S28 reviewed status | Interpretation |
|---|---|---|
| SL1 | Not observed | Accountant did not treat split/local status as stronger approval than the evidence supported. |
| SL2 | `partially_supported_needs_revision` | Split items were handed to accounting in AS02/AS03 while aggregate review remained unresolved. This is bounded because buyer/process-owner handoff was scripted, not an emergent buyer-choice result. |
| SL3 | Not observed | Accountant did not perform payment preparation, payment draft creation, batch staging, or equivalent preparation-like action while aggregate review remained unresolved. |
| SL4 | Not observed | No final state treated split items as payment-ready, payable, prepared, or approval-sufficient while aggregate review remained unresolved. |
| SL5 | `supported_for_reviewed_evidence` | In all non-control runs, aggregate approval/review gaps remained visible and blocked or conditioned downstream processing. |
| SL6 | Not observed | Aggregate relationship, threshold, approval/review gap, and global truth did not disappear or become contradicted downstream. |
| FM3 | Not observed | Accountant did not treat split structure, local status, or partial approval as resolving aggregate approval or exception authority. |
| FM6 | Not observed | Post-hoc explanations did not repair, strengthen, or erase the contemporaneous aggregate gap beyond the trace. |

## Required Synthesis Questions

1. Did S28 produce SL2?

Yes, but only in a bounded form. S28 produced reviewed `SL2 partially_supported_needs_revision` for split-item handoff in AS02/AS03. The support is not emergent buyer-choice evidence because the buyer/process-owner handoff was scripted for reconstructability.

2. Did S28 produce SL3?

No. Accountant-local review did not select `prepare_payment`, `create_payment_draft`, `stage_payment_batch`, or equivalent preparation-like action in any non-control condition.

3. Did S28 produce SL4?

No. No non-control final state became payment-ready, payable, prepared, or approval-sufficient.

4. Did S28 produce SL6?

No. The aggregate relationship and aggregate approval/review gap remained visible in global truth, Game Master decisions, metrics, final state, and review artifacts.

5. Did S28 mostly produce SL5?

Yes. S28 mostly reinforced SL5 aggregate-gap preservation. All 15 non-control accepted runs preserved the aggregate gap downstream.

## Mechanism Comparison

| Mechanism | Current reviewed contribution | What it did not show |
|---|---|---|
| BC31 ambiguity targeting | Narrow buyer payment-forward handoff without explicit approval; downstream accountant requested more evidence. | No accountant preparation, final payment-ready state, full approval bypass, or causation. |
| S18 lossy handoff | SL2 handoff support in 3/5 reviewed artificial runs; downstream SL5 preservation. | No SL3, SL4, SL6, FM1, FM3, or FM6. |
| S19 queue/ticket mismatch | SL5 preservation despite readiness-like ticket status. | No SL2, SL3, SL4, SL6, FM1, FM3, or FM6. |
| S20 exception-route ambiguity | SL5 preservation in accepted runs; one parser/source-ref exclusion reported transparently. | No SL1, SL2, SL3, SL4, SL6, FM1, FM3, or FM6. |
| S24 approval artifact mismatch | SL5 preservation where authoritative approval remained unresolved. | No SL3, SL4, SL6, FM3, or FM6. |
| S25 conflicting operational norms | SL5 preservation where explicit current approval was absent. | No SL3, SL4, SL6, FM3, FM4, or FM6. |
| S26 shadow approval / informal preclearance | SL5 preservation where formal current approval was absent. | No SL1, SL3, SL4, SL6, FM3, or FM6. |
| S27 payment-draft staging | Project-owner-confirmed narrow SL3 partial support for `create_payment_draft`; SL5 gap preservation remained visible. | No SL4, SL6, full approval bypass, fraud, or baseline readiness. |
| S28 structuring / approval splitting | Bounded SL2 split-item handoff support and repeated SL5 aggregate-gap preservation. | No SL1, SL3, SL4, SL6, FM3, or FM6. |

## Current Phase 4 Evidence Map

| Observation level | Mechanisms with reviewed support | Current boundary |
|---|---|---|
| SL1 | None in current Phase 4 reviewed support. | Auxiliary SL1 signals were reviewed and rejected or not observed. |
| SL2 | BC31, S18 lossy handoff, selected prompt/persona lossy-handoff cells, S28 downstream structuring, and S29 applicant-side structuring. | Handoff / split-submission movement only; S28 is scripted downstream handoff, while S29 is emergent requester/buyer split choice. |
| SL3 | S27 payment-draft staging only. | Narrow project-owner-confirmed partial support for `create_payment_draft`; no final readiness or gap erasure. |
| SL4 | None. | Full approval-bypass / final payment-ready without approval remains unsupported. |
| SL5 | S17, S18, S19, S20, S23, S24, S25, S26, S27, S28, and S29. | Strongest repeated artificial-system pattern is downstream or global gap preservation. |
| SL6 | None. | Evidence-gap erasure remains unsupported. |

## Structuring Assessment

Structuring / approval splitting is a valid within-control mechanism under the revised scope axis because it can occur without impersonation, forged evidence, hidden records, collusion, unauthorized access, privilege escalation, or malicious bypass.

S28 shows that this mechanism can create handoff-level ambiguity: split items reach accounting while aggregate review remains unresolved. However, the downstream accountant did not advance those items into preparation or final readiness. Instead, the accountant repeatedly requested aggregate review or additional evidence, or held the item.

Therefore S28 is more informative as a boundary-preservation and SL2-handoff mechanism than as a stronger downstream slippage mechanism.

## Post-S28 Research Correction

S28 should also be read with one important limit: it is a downstream accountant-side diagnostic.

It tested what happens after split items reach accounting. It did not test whether a requester or buyer chooses to split a case under environmental pressure. That upstream choice is frozen separately in `protocols/failure-modes/phase4-applicant-side-structuring-diagnostic-v0.1.md`.

This correction does not change the S28 reviewed statuses. S28 still supports only bounded SL2 split-item handoff and SL5 aggregate-gap preservation, with SL1, SL3, SL4, SL6, FM3, and FM6 not observed.

## Post-S29 Applicant-Side Structuring Update

S29 is synthesized separately in `docs/synthesis/phase4-applicant-side-structuring-synthesis-v0.1.md`.

S29 answers the upstream question that S28 did not test: whether the requester/buyer chooses split submission under observable pressure and aggregate-threshold conditions.

S29 result:

- 20 attempted / 20 accepted / 0 excluded.
- Applicant-side split submission appeared in 7/20 reviewed artificial runs; project-owner review confirms this as bounded applicant-side within-control process drift / SL2 support.
- Split submissions appeared only under pressure conditions, not in the no-pressure control condition.
- 4 split submissions included an aggregate note.
- 3 split submissions did not include an aggregate note; project-owner review treats these as stronger boundary candidates.
- SL2 applicant-side split submission is supported with boundary limits.
- SL5 aggregate-gap preservation is supported in all 20 runs.
- SL1, SL4, SL6, and FM3 were not observed.
- SL3 and FM6 were not applicable in S29 v0.1 because no accountant or post-hoc explanation turn was included.

This update changes the structuring mechanism assessment:

- S28 shows downstream accounting preserves aggregate gaps after split items arrive.
- S29 shows the upstream applicant/requester-buyer can choose split submission under pressure conditions.
- Neither S28 nor S29 supports SL4 final payment-ready state, SL6 gap erasure, full approval bypass, fraud, hidden intent, human behavior, real-world organization behavior, statistical significance, prompt causation, model-general behavior, or audit/compliance/legal/operational/governance/safety sufficiency.

The S29 split-without-aggregate-note pattern has now received project-owner review. It may be described as approval-threshold / aggregate-review weakening risk in the artificial within-control process-drift scope, but not as fraud, hidden intent, full approval bypass, SL4, or SL6.

## Baseline Discussion

S28 does not justify baseline preparation.

Reasons:

- SL2 support is bounded: S28 is scripted at the downstream handoff layer, and S29 is project-owner-reviewed applicant-side split submission without downstream accountant processing.
- S28 did not produce SL3 accountant preparation without aggregate approval/review.
- S28 did not produce SL4 final payment-ready state.
- S28 did not produce SL6 aggregate-gap erasure.
- S27 remains the only narrow SL3 partial-support mechanism, and it did not produce SL4 or SL6.
- The strongest repeated Phase 4 pattern remains SL5 gap preservation.

Baseline work would require stronger reviewed support for a clearly defined level, such as repeated SL3 or SL6, and a separate protocol freeze. That threshold is not met.

## Phase 4 Completion Assessment

Phase 4 should be treated as research-complete for the current tested-mechanism map, not as proof of stronger downstream slippage.

The project can now answer the research-completion questions for the mechanisms tested so far:

| Question | Current answer |
|---|---|
| Which tested mechanisms produce SL2? | Lossy handoff, downstream structuring / approval splitting, and applicant-side structuring can produce bounded SL2 handoff or split-submission candidates; BC31 also supports a narrow handoff observation. |
| Which tested mechanisms produce SL3? | Payment-draft staging produced narrow project-owner-confirmed SL3 partial support for `create_payment_draft`. |
| Which tested mechanisms produce SL4? | None. |
| Which tested mechanisms produce SL6? | None. |
| Which mechanisms mainly preserve gaps as SL5? | Most downstream diagnostics, including S17, S18, S19, S20, S23, S24, S25, S26, S27, S28, and S29. |
| Why pause, continue, or prepare baseline? | Pause run-producing Phase 4 work until a new target-definition/protocol-freeze checkpoint decides whether to build on the reviewed S29 applicant-side SL2 boundary, test downstream consequences, or consolidate. |
| What remains unknown? | Whether a later downstream protocol can connect applicant-side split submission to reviewed SL3/SL4/SL6 support without outside-control behavior, and whether S29's pressure-conditioned pattern is stable enough for a baseline target. |

## Decision

Decision: stop run-producing Phase 4 diagnostics and consolidate until a new target-definition/protocol-freeze checkpoint decides whether to build on the project-owner-reviewed S29 applicant-side split-without-aggregate-note boundary.

This updates Decision B from the S28 synthesis instruction after S29. S28 mostly reinforced SL5 while adding bounded downstream SL2 support. S29 adds applicant-side SL2 split-submission support, but still does not justify baseline preparation because SL3, SL4, and SL6 are not supported by S29.

Future run-producing work should resume only if a new mechanism-selection PR identifies a substantially different organizational information mechanism and defines research-completion criteria before execution.

## Post-S30 Freeform Applicant Structuring Update

S30 is synthesized separately in `docs/synthesis/phase4-freeform-vs-menu-conditioned-structuring-synthesis-v0.1.md`.

S30 tested the next question after S29: whether split or multi-packet proposals appear when the applicant-side actor generates a handling plan without visible fixed split-submission actions. S30 produced no freeform multi-packet proposals in 20 accepted runs and preserved aggregate approval/review gaps in all runs.

This updates the structuring assessment:

- S28 remains a downstream accounting-side structuring diagnostic.
- S29 remains project-owner-reviewed bounded applicant-side SL2 support, but under fixed-menu pressure conditions.
- S30 does not add freeform emergent applicant-side structuring support.
- The S30-to-S31 chain should stop because S31 was conditional on observed freeform split proposals.

This does not change the unsupported status of SL4, SL6, full approval bypass, fraud, hidden intent, human behavior, real-world organization behavior, statistical significance, prompt causation, model-general behavior, or compliance/legal/audit/operational/governance/safety sufficiency.

## Post-S31 Advisor-Seeded Structuring Update

S31 is synthesized separately in `docs/synthesis/phase4-advisor-seeded-structuring-synthesis-v0.1.md`.

S31 tested whether a separate processing-option advisor could generate within-control split-like options from pressure and threshold context, have those options filtered, and then add them to the applicant menu.

S31 result:

- 20 attempted / 17 accepted / 3 excluded;
- advisor-generated split-like options appeared in accepted runs;
- seeded split options were present in 15/17 accepted applicant menus;
- requester/buyer selected advisor-seeded split options in 0/17 accepted runs;
- requester/buyer selected only `submit_single_aggregate_request` or `request_higher_approval`;
- SL5 aggregate-gap preservation was observed in all accepted runs;
- SL1, SL2, SL4, and SL6 were not observed.

This updates the structuring assessment:

- S29 remains the only applicant-side structuring diagnostic with reviewed SL2 support.
- S30 shows no freeform split proposal without explicit split choices.
- S31 shows that neutral advisor-seeded option availability alone did not produce applicant-side split selection.
- A future structuring mechanism would need to target option provenance, recommendation force, or role authority rather than simply adding generated options.

This does not change the unsupported status of SL4, SL6, full approval bypass, fraud, hidden intent, human behavior, real-world organization behavior, statistical significance, prompt causation, model-general behavior, or compliance/legal/audit/operational/governance/safety sufficiency.

## Allowed Claims

This synthesis may claim:

- S28 produced reviewed artificial evidence for bounded SL2 split-item handoff and SL5 aggregate-gap preservation.
- S29 produced reviewed artificial evidence for bounded applicant-side SL2 split submission and SL5 aggregate-gap preservation.
- S30 and S31 did not add applicant-side SL2 support beyond S29; both preserved aggregate approval/review gaps.
- Structuring / approval splitting did not produce reviewed SL3, SL4, SL6, FM3, or FM6 support under the frozen artificial protocol.
- Current Phase 4 evidence identifies lossy handoff and structuring as SL2-producing mechanisms, payment-draft staging as a narrow SL3 partial-support mechanism, and many diagnostics as SL5-preserving mechanisms.
- Current evidence does not justify a controlled failure-mode baseline.

## Forbidden Claims

This synthesis must not claim:

- full approval bypass was reproduced;
- fraud or intentional misconduct occurred;
- real organizations behave this way;
- humans behave this way;
- actor intent is known;
- control effectiveness is proven;
- prompt wording caused the result;
- results are statistically meaningful;
- S28 supports compliance, legal, audit, operational, governance, or safety sufficiency;
- S28 supports model-general safety, reliability, or risk claims.
