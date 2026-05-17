# Method B Synthesis Protocol v0.1

Date: 2026-05-17
Status: accepted
Phase: Method B
Checkpoint: BC30
Covers: C16, C17, C18, C19, C20
Claim boundary: `method_b_synthesis_only`

## Purpose

This protocol freezes the inputs, evidence levels, and claim boundaries for the BC30 Method B synthesis.

Method B asks whether higher-friction artificial-organization scenarios, multi-turn traces, post-hoc explanations, and reviewable evidence packs make responsibility diffusion, approval bypass, ambiguous guidance misinterpretation, pressure-normalization, evidence-gap erasure, or post-hoc justification more observable than the earlier baseline path.

This synthesis is a review and interpretation checkpoint. It does not execute new LLM runs, change scenarios, change prompts, change action menus, change Game Master rules, change event taxonomy, change metrics, or change review criteria.

## Frozen Inputs

| Area | Frozen source |
|---|---|
| Failure-mode taxonomy | `protocols/failure-modes/failure-mode-taxonomy-v0.1.md` |
| High-friction scenario design | `scenarios/org-payment/high-friction-scenario-matrix.md` |
| Multi-turn and post-hoc design | `protocols/failure-modes/multi-turn-memory-justification-pilot-v0.1.md` |
| Targeted Method B execution | `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/aggregate.json` |
| Targeted Method B review | `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/failure-mode-review-0001/summary.md` |
| Baseline decision | `protocols/failure-modes/failure-mode-baseline-decision-v0.1.md` |
| Baseline execution status | `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/failure-mode-review-0001/baseline-execution-status.md` |
| Diagnostic sensitivity protocol | `protocols/failure-modes/failure-mode-diagnostic-sensitivity-v0.1.md` |
| Diagnostic sensitivity execution | `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/aggregate.json` |
| Second-domain transfer review | `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/method-b-transfer-review-0001/summary.md` |

## Evidence Levels

| Evidence level | Meaning |
|---|---|
| `supported` | Human-reviewed or explicitly accepted review evidence supports the failure-mode label within the reviewed scope. |
| `partially_supported` | Review evidence supports part of the label but records material unresolved gaps. |
| `generated_candidate` | Automated or generated classifier material flagged a possible row before review. |
| `reviewed_not_observed` | A reviewed evidence subset did not satisfy the failure-mode evidence requirements. |
| `not_assessable` | Required artifacts are absent, so the failure mode cannot be assessed in that source. |
| `needs_review` | Candidate material exists but cannot be upgraded without a separate review. |

## Synthesis Rules

- Generated candidate labels must not be upgraded to `supported`.
- BC28 FM6 candidate rows must remain pre-review candidate material.
- BC29 second-domain review must not be treated as cross-domain validation.
- Not-observed labels must not be interpreted as proof that a failure mode is absent in general.
- No failure mode may be reported as human-reviewed support unless the reviewed source and reviewer scope are named.
- The term "pseudo-reproduction" may only mean bounded artificial-system candidate observability, not reproduction of human society or real organizations.

## Forbidden Claims

This synthesis must not claim:

- human society has been reproduced;
- real organizations would behave similarly;
- any Method B failure mode has been proven;
- BC28 prompt framing caused FM6 candidates;
- org-payment findings transfer to expense reimbursement;
- scenario differences are statistically or causally meaningful;
- the model is generally safe, unsafe, robust, or unstable;
- the artifacts provide compliance, legal, audit, or operational sufficiency.

## Checkpoint Target

BC30 should decide what Method B currently supports, what remains only candidate material, what was not observed, and what must be reviewed or redesigned before stronger claims can be made.
