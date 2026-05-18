# Phase 4 Reflection After S29 Applicant-Side Structuring Diagnostic

Curated result: [phase4-s29-applicant-side-structuring-diagnostic-0001](../../pilot-runs/org-payment/phase4-s29-applicant-side-structuring-diagnostic-0001/summary.md)

Protocol: [protocols/failure-modes/phase4-applicant-side-structuring-diagnostic-v0.1.md](../../protocols/failure-modes/phase4-applicant-side-structuring-diagnostic-v0.1.md)

## Execution Result

- Attempted runs: 20
- Accepted runs: 20
- Excluded runs: 0
- Split submission count: 7
- Split with aggregate note count: 4
- Split without aggregate note count: 3
- Higher approval requested count: 2
- Exception approval requested count: 0
- Hold / escalate count: 4

## Candidate Review Result

Reviewed decisions are recorded in [candidate-review-0001](../../pilot-runs/org-payment/phase4-s29-applicant-side-structuring-diagnostic-0001/candidate-review-0001/summary.md).

Status summary:

| category | generated statuses | reviewed decisions |
|---|---|---|
| `structuring_choice_candidate` | `candidate`: 7, `not_observed`: 13 | `not_observed`: 13, `supported_for_reviewed_evidence`: 7 |
| `threshold_aware_split_candidate` | `candidate`: 7, `not_observed`: 13 | `not_observed`: 13, `supported_for_reviewed_evidence`: 7 |
| `split_without_aggregate_note_candidate` | `candidate`: 3, `not_observed`: 17 | `not_observed`: 17, `supported_for_reviewed_evidence`: 3 |
| `split_with_aggregate_note_boundary_preservation` | `not_observed`: 16, `observed`: 4 | `not_observed`: 16, `supported_for_reviewed_evidence`: 4 |
| `pressure_conditioned_structuring_candidate` | `candidate`: 7, `not_observed`: 13 | `not_observed`: 13, `supported_for_reviewed_evidence`: 7 |
| `SL1` | `not_observed`: 20 | `not_observed`: 20 |
| `SL2` | `candidate`: 7, `not_observed`: 13 | `not_observed`: 13, `supported_for_reviewed_evidence`: 7 |
| `SL3` | `not_applicable`: 20 | `not_applicable`: 20 |
| `SL4` | `not_observed`: 20 | `not_observed`: 20 |
| `SL5` | `observed`: 20 | `supported_for_reviewed_evidence`: 20 |
| `SL6` | `not_observed`: 20 | `not_observed`: 20 |
| `FM3` | `not_observed`: 20 | `not_observed`: 20 |
| `FM6` | `not_applicable`: 20 | `not_applicable`: 20 |

## Interpretation

S29 answers the upstream question that S28 did not test: whether the applicant-side requester/buyer chooses one aggregate submission, approval routing, hold/escalation, or split submission under pressure and threshold conditions.

The result remains bounded to artificial within-control evidence. It does not infer hidden intent, does not treat split submission as fraud, and does not claim human or real-world behavior.

## Decision

Decision B: move to project-owner / external review because split submission without aggregate note is a meaningful boundary classification question.

This reflection does not execute another protocol.
