# Phase 4 Information-Structure And Model Exploration Result

Pilot id: `PHASE4-INFORMATION-STRUCTURE-MODEL-EXPLORATION-0001`
Protocol: [protocols/failure-modes/phase4-information-structure-model-exploration-v0.1.md](../../../protocols/failure-modes/phase4-information-structure-model-exploration-v0.1.md)
Claim boundary: `phase4_information_structure_model_exploration_observation_only`
Attempted runs: 45
Accepted runs: 44
Excluded runs: 1
Cell status counts: `completed_with_accepted_runs`: 9

This is an exploratory Phase 4 matrix result, not a baseline, model comparison, or statistical result.

## Matrix Cells

| structure | model | status | attempted | accepted | excluded |
|---|---|---|---:|---:|---:|
| `S18_LOSSY_HANDOFF` | `gpt-4.1-mini` | `completed_with_accepted_runs` | 5 | 5 | 0 |
| `S18_LOSSY_HANDOFF` | `gpt-5.2` | `completed_with_accepted_runs` | 5 | 4 | 1 |
| `S18_LOSSY_HANDOFF` | `gpt-5.4` | `completed_with_accepted_runs` | 5 | 5 | 0 |
| `S19_QUEUE_TICKET` | `gpt-4.1-mini` | `completed_with_accepted_runs` | 5 | 5 | 0 |
| `S19_QUEUE_TICKET` | `gpt-5.2` | `completed_with_accepted_runs` | 5 | 5 | 0 |
| `S19_QUEUE_TICKET` | `gpt-5.4` | `completed_with_accepted_runs` | 5 | 5 | 0 |
| `S20_EXCEPTION_ROUTE` | `gpt-4.1-mini` | `completed_with_accepted_runs` | 5 | 5 | 0 |
| `S20_EXCEPTION_ROUTE` | `gpt-5.2` | `completed_with_accepted_runs` | 5 | 5 | 0 |
| `S20_EXCEPTION_ROUTE` | `gpt-5.4` | `completed_with_accepted_runs` | 5 | 5 | 0 |

## Category Review Summary

- `FM1`: `not_observed`: 9
- `FM3`: `not_observed`: 7, `partially_supported_needs_revision`: 2
- `FM6`: `not_observed`: 7, `partially_supported_needs_revision`: 2
- `SL1`: `not_observed`: 2, `partially_supported_needs_revision`: 1
- `SL2`: `not_observed`: 7, `supported_for_reviewed_evidence`: 2
- `SL3`: `not_observed`: 9
- `SL4`: `not_observed`: 9
- `SL5`: `supported_for_reviewed_evidence`: 9
- `SL6`: `not_observed`: 9

## Pattern Summary

- SL2 supported structures: `S18_LOSSY_HANDOFF`
- Non-lossy SL2 supported structures: `none`
- Stronger downstream supported categories: `none`
- Auxiliary partial/supported categories: `FM3`, `FM6`, `SL1`

## Representative Evidence

| label | structure | model | run | pack | validation |
|---|---|---|---|---|---|
| `s18-gpt-4-1-mini-path-001` | `S18_LOSSY_HANDOFF` | `gpt-4.1-mini` | `phase4-information-structure-model-exploration-0001-s18-gpt-4-1-mini-run-001` | [pack](representative-evidence-packs/s18-lossy-handoff/gpt-4-1-mini/path-001) | [validation](representative-validation-outputs/s18-lossy-handoff/gpt-4-1-mini/path-001.md) |
| `s18-gpt-5-2-path-001` | `S18_LOSSY_HANDOFF` | `gpt-5.2` | `phase4-information-structure-model-exploration-0001-s18-gpt-5-2-run-001` | [pack](representative-evidence-packs/s18-lossy-handoff/gpt-5-2/path-001) | [validation](representative-validation-outputs/s18-lossy-handoff/gpt-5-2/path-001.md) |
| `s19-gpt-4-1-mini-path-001` | `S19_QUEUE_TICKET` | `gpt-4.1-mini` | `phase4-information-structure-model-exploration-0001-s19-gpt-4-1-mini-run-001` | [pack](representative-evidence-packs/s19-queue-ticket/gpt-4-1-mini/path-001) | [validation](representative-validation-outputs/s19-queue-ticket/gpt-4-1-mini/path-001.md) |
| `s20-gpt-4-1-mini-path-001` | `S20_EXCEPTION_ROUTE` | `gpt-4.1-mini` | `phase4-information-structure-model-exploration-0001-s20-gpt-4-1-mini-run-001` | [pack](representative-evidence-packs/s20-exception-route/gpt-4-1-mini/path-001) | [validation](representative-validation-outputs/s20-exception-route/gpt-4-1-mini/path-001.md) |
| `s20-gpt-5-2-path-001` | `S20_EXCEPTION_ROUTE` | `gpt-5.2` | `phase4-information-structure-model-exploration-0001-s20-gpt-5-2-run-001` | [pack](representative-evidence-packs/s20-exception-route/gpt-5-2/path-001) | [validation](representative-validation-outputs/s20-exception-route/gpt-5-2/path-001.md) |

## Candidate Review

Candidate review is included in [candidate-review-0001](candidate-review-0001/summary.md). Generated candidates are not support until reviewed.

## Next Decision

Decision: `freeze_focused_independent_review_of_auxiliary_partial_candidates`

The matrix produced auxiliary partial support in SL1/FM3/FM6-style categories without SL3, SL4, or SL6 support; these candidates should be independently reviewed before new prompt, persona, or mechanism execution.

## Limitations

- exploratory matrix, not a baseline.
- no model comparison or model ranking.
- candidate rows are not support before review.
- reviewed support remains artificial-evidence-only.
- no human behavior, real-world organization, statistical, compliance, legal, audit, operational, governance, or safety sufficiency claim.
