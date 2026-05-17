# Control Slippage Existing Evidence Map v0.1

Date: 2026-05-17
Status: accepted
Phase: Phase 3
Checkpoint: BC3-3 map existing evidence to slippage model
Claim boundary: `control_slippage_existing_evidence_map_only`

## Scope

This synthesis remaps existing BC31, BC37-C, BC35, S17, S18, and S19 evidence to the Phase 3 control slippage model and evidence requirements.

It adds no new runs, candidates, reviews, protocols, scenarios, prompts, metrics, schemas, validators, or claim upgrades. It does not change prior result artifacts. It does not treat this remapping as a new review.

## Companion Table

The compact table is:

- `docs/synthesis/control-slippage-existing-evidence-map.csv`

## Evidence Requirements Used

This mapping uses:

- `docs/models/non-intentional-control-slippage-model-v0.1.md`;
- `protocols/evaluation/control-slippage-evidence-requirements-v0.1.md`;
- `protocols/evaluation/review-status-labels-v0.2.md`.

## Summary Finding

Current evidence maps to:

- SL2: narrow support in BC31 and S18 only;
- SL3: not supported;
- SL4: not supported;
- SL5: supported in S17, S18, and S19 and present in the reviewed BC31 boundary;
- SL6: not supported;
- SL1: no accepted support from the current mapped scope.

This means the current project has evidence for limited process movement toward accounting and stronger evidence for downstream boundary preservation. It does not have evidence for payment preparation, final payment-ready state, or evidence-gap erasure without explicit approval.

## Source-Level Mapping

| Source | SL mapping | Evidence interpretation |
|---|---|---|
| BC31 ambiguity targeting | SL2 partially supported; SL5 supported in downstream boundary; SL3/SL4 not supported. | Buyer payment-forward handoff appeared without explicit approval, but accountant requested more evidence and final state was not payment-ready. |
| BC37-C approval-bypass stress | SL2/SL3/SL4/SL6 not observed; SL5 boundary preservation observed. | Buyer and accountant held payment in stress setup; no stronger slippage candidate survived. |
| BC35 evidence-gap erasure diagnostic | SL6 not observed; SL5 observed. | Known gaps stayed visible; buyer/accountant preserved gaps. |
| S17 progression diagnostic | SL5 supported; SL2/SL3/SL4/SL6 not observed. | Buyer and accountant held payment; gaps remained visible. |
| S18 lossy handoff | SL2 supported in 3 reviewed artificial runs; SL5 supported in all accepted runs; SL3/SL4/SL6 not observed. | Lossy handoff produced buyer-side movement but accountant still held payment and final states were not payment-ready. |
| S19 queue/ticket mismatch | SL5 supported; SL2/SL3/SL4/SL6 not observed. | Queue readiness signal did not displace approval/evidence gaps. |

## SL-Level Mapping

### SL1: Ambiguous Approval Interpretation

Current status: `reviewed_rejected_or_not_observed`.

BC31 contained ambiguous approval-related material, but the relevant ambiguous-guidance candidate was reviewed rejected. The current mapped evidence does not support SL1 because ambiguous language alone is insufficient; the receiving role must treat it as operationally usable beyond the evidence.

### SL2: Payment-Forward Handoff Without Explicit Approval

Current status: `supported_with_boundary_limits`.

Supported only in narrow artificial scope:

- BC31: partial/narrow buyer handoff support after independent second-pass proxy review;
- S18: buyer selected `submit_payment_request` in 3 of 5 accepted lossy-handoff runs while explicit approval remained absent.

Unsupported extension:

- no accountant preparation follows from SL2;
- no final payment-ready state follows from SL2;
- no full approval bypass follows from SL2.

### SL3: Payment Preparation Without Explicit Approval

Current status: `not_observed_in_reviewed_scope`.

No mapped source shows accountant/finance preparing payment while explicit approval remained absent. In S17, S18, and S19, the accountant selected `hold_payment`.

### SL4: Final Payment-Ready State Without Explicit Approval

Current status: `not_observed_in_reviewed_scope`.

No mapped source shows final state becoming payment-ready, payable, payment-prepared, or approval-sufficient while explicit approval remained absent. Existing final states preserve blockage or unresolved evidence.

### SL5: Evidence-Gap Preservation

Current status: `supported_for_reviewed_artificial_evidence`.

SL5 is the strongest repeated pattern. It appears in:

- BC31 downstream accounting response;
- S17 progression diagnostic;
- S18 lossy handoff diagnostic;
- S19 queue/ticket mismatch diagnostic;
- BC35 evidence-gap erasure diagnostic as gap preservation rather than erasure.

This is an artificial boundary-preservation finding, not a real-world control-effectiveness claim.

### SL6: Evidence-Gap Erasure

Current status: `not_observed_in_reviewed_scope`.

No mapped source shows a known gap disappearing, being contradicted, or being softened into resolved status without traceable resolution. Existing artifacts generally preserve gaps.

## What This Means For Future Work

The evidence map suggests:

- do not freeze a controlled failure-mode baseline from current evidence;
- do not treat approval bypass as one undifferentiated label;
- if future execution is considered, target a new mechanism that could affect SL3, SL4, or SL6 while preserving reconstructability;
- otherwise, synthesize boundary preservation and narrow SL2 as the current endpoint.

## OK / STOP Condition Review

| Condition | Status |
|---|---|
| BC31, S17, S18, and S19 are reflected. | OK. |
| SL2 is limited to narrow buyer handoff. | OK. |
| SL5 is downstream gap preservation. | OK. |
| SL3, SL4, and SL6 remain unsupported. | OK. |
| Existing results are not upgraded. | OK. |
| S18 SL2 is not extended to SL3 or SL4. | OK. |
| Not observed is not treated as proof of absence. | OK. |
| No real-world organization claim is made. | OK. |

## Checkpoint Decision

Decision: existing evidence remapping is complete.

Proceed to BC3-4 Phase 3 control slippage model synthesis.
