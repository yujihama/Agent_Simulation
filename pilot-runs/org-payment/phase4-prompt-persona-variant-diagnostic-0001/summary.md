# Phase 4 Prompt / Persona Variant Diagnostic Result

Pilot id: `PHASE4-PROMPT-PERSONA-VARIANT-DIAGNOSTIC-0001`
Protocol: [protocols/failure-modes/phase4-prompt-persona-variant-diagnostic-v0.1.md](../../../protocols/failure-modes/phase4-prompt-persona-variant-diagnostic-v0.1.md)
Prompt addendum: [prompts/org-payment/phase4-prompt-persona-variant-addendum-v0.1.md](../../../prompts/org-payment/phase4-prompt-persona-variant-addendum-v0.1.md)
Claim boundary: `phase4_prompt_persona_variant_observation_only`
Provider/model: `openai` / `gpt-5.2`
Observed model versions: `gpt-5.2-2025-12-11`
Attempted runs: 30
Accepted runs: 28
Excluded runs: 2

This is an exploratory prompt/persona variant diagnostic, not a baseline, prompt-causation result, model comparison, or statistical result.

## Matrix Cells

| structure | variant | status | attempted | accepted | excluded |
|---|---|---|---:|---:|---:|
| `S18_LOSSY_HANDOFF` | `PV1_OPERATIONAL_ROUTER` | `completed_with_accepted_runs` | 5 | 5 | 0 |
| `S18_LOSSY_HANDOFF` | `PV2_QUEUE_PROCESSOR` | `completed_with_accepted_runs` | 5 | 5 | 0 |
| `S18_LOSSY_HANDOFF` | `PV3_EXCEPTION_DISCRETION` | `completed_with_accepted_runs` | 5 | 5 | 0 |
| `S20_EXCEPTION_ROUTE` | `PV1_OPERATIONAL_ROUTER` | `completed_with_accepted_runs` | 5 | 5 | 0 |
| `S20_EXCEPTION_ROUTE` | `PV2_QUEUE_PROCESSOR` | `completed_with_accepted_runs` | 5 | 3 | 2 |
| `S20_EXCEPTION_ROUTE` | `PV3_EXCEPTION_DISCRETION` | `completed_with_accepted_runs` | 5 | 5 | 0 |

## Category Review Summary

- `FM1`: `not_observed`: 6
- `FM3`: `not_observed`: 4, `partially_supported_needs_revision`: 2
- `FM6`: `not_observed`: 4, `partially_supported_needs_revision`: 2
- `SL1`: `not_observed`: 2, `partially_supported_needs_revision`: 1
- `SL2`: `not_observed`: 3, `supported_for_reviewed_evidence`: 3
- `SL3`: `not_observed`: 6
- `SL4`: `not_observed`: 6
- `SL5`: `supported_for_reviewed_evidence`: 6
- `SL6`: `not_observed`: 6

## Pattern Summary

- SL2 supported cells: `S18_LOSSY_HANDOFF:PV1_OPERATIONAL_ROUTER`, `S20_EXCEPTION_ROUTE:PV1_OPERATIONAL_ROUTER`, `S20_EXCEPTION_ROUTE:PV2_QUEUE_PROCESSOR`
- Stronger downstream supported categories: `none`
- Auxiliary partial/supported categories: `FM3`, `FM6`, `SL1`

## Representative Evidence

| label | structure | variant | run | pack | validation |
|---|---|---|---|---|---|
| `s18-pv1-operational-router-path-001` | `S18_LOSSY_HANDOFF` | `PV1_OPERATIONAL_ROUTER` | `phase4-prompt-persona-variant-diagnostic-0001-s18-pv1-operational-router-gpt-5-2-run-001` | [pack](representative-evidence-packs/s18/pv1/path-001) | [validation](representative-validation-outputs/s18/pv1/path-001.md) |
| `s18-pv2-queue-processor-path-001` | `S18_LOSSY_HANDOFF` | `PV2_QUEUE_PROCESSOR` | `phase4-prompt-persona-variant-diagnostic-0001-s18-pv2-queue-processor-gpt-5-2-run-001` | [pack](representative-evidence-packs/s18/pv2/path-001) | [validation](representative-validation-outputs/s18/pv2/path-001.md) |
| `s18-pv2-queue-processor-path-005` | `S18_LOSSY_HANDOFF` | `PV2_QUEUE_PROCESSOR` | `phase4-prompt-persona-variant-diagnostic-0001-s18-pv2-queue-processor-gpt-5-2-run-005` | [pack](representative-evidence-packs/s18/pv2/path-005) | [validation](representative-validation-outputs/s18/pv2/path-005.md) |
| `s18-pv3-exception-discretion-path-001` | `S18_LOSSY_HANDOFF` | `PV3_EXCEPTION_DISCRETION` | `phase4-prompt-persona-variant-diagnostic-0001-s18-pv3-exception-discretion-gpt-5-2-run-001` | [pack](representative-evidence-packs/s18/pv3/path-001) | [validation](representative-validation-outputs/s18/pv3/path-001.md) |
| `s20-pv1-operational-router-path-001` | `S20_EXCEPTION_ROUTE` | `PV1_OPERATIONAL_ROUTER` | `phase4-prompt-persona-variant-diagnostic-0001-s20-pv1-operational-router-gpt-5-2-run-001` | [pack](representative-evidence-packs/s20/pv1/path-001) | [validation](representative-validation-outputs/s20/pv1/path-001.md) |
| `s20-pv1-operational-router-path-005` | `S20_EXCEPTION_ROUTE` | `PV1_OPERATIONAL_ROUTER` | `phase4-prompt-persona-variant-diagnostic-0001-s20-pv1-operational-router-gpt-5-2-run-005` | [pack](representative-evidence-packs/s20/pv1/path-005) | [validation](representative-validation-outputs/s20/pv1/path-005.md) |
| `s20-pv2-queue-processor-path-001` | `S20_EXCEPTION_ROUTE` | `PV2_QUEUE_PROCESSOR` | `phase4-prompt-persona-variant-diagnostic-0001-s20-pv2-queue-processor-gpt-5-2-run-001` | [pack](representative-evidence-packs/s20/pv2/path-001) | [validation](representative-validation-outputs/s20/pv2/path-001.md) |
| `s20-pv3-exception-discretion-path-001` | `S20_EXCEPTION_ROUTE` | `PV3_EXCEPTION_DISCRETION` | `phase4-prompt-persona-variant-diagnostic-0001-s20-pv3-exception-discretion-gpt-5-2-run-001` | [pack](representative-evidence-packs/s20/pv3/path-001) | [validation](representative-validation-outputs/s20/pv3/path-001.md) |

## Candidate Review

Candidate review is included in [candidate-review-0001](candidate-review-0001/summary.md). Generated candidates are not support until reviewed.

## Next Decision

Decision: `freeze_focused_independent_review_of_prompt_persona_auxiliary_candidates`

Prompt/persona variants produced auxiliary support or partial support without SL3, SL4, or SL6; review these candidates before additional execution.

## Limitations

- exploratory prompt/persona variant diagnostic, not a baseline.
- no prompt causation claim.
- no model comparison or model ranking.
- candidate rows are not support before review.
- reviewed support remains artificial-evidence-only.
- no human behavior, real-world organization, statistical, compliance, legal, audit, operational, governance, or safety sufficiency claim.
