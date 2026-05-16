# EXP-0002 Construct Validity Check 0001

Date: 2026-05-17
Status: completed for curated representative packs
Check id: `EXP-0002-CV-0001`
Protocol: `protocols/evaluation/construct-validity-check-v0.1.md`
Reviewed human evidence review: `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md`
Claim boundary: `construct_validity_check_observation_only`

## Boundary

This check covers the 14 curated, human-reviewed EXP-0002 representative evidence packs. It does not review all raw runs, change EXP-0002 results, change aggregate metrics, revise event taxonomy, revise metrics protocol, or add new model runs.

The check assesses whether selected constructs are supported for the reviewed representative-pack scope. It does not establish statistical significance, scenario causation, pressure causation, responsibility-diffusion proof, approval-bypass proof, human behavior, real-world organization behavior, compliance sufficiency, audit sufficiency, operational sufficiency, model comparison, or general LLM behavior.

## Construct Status Summary

| Construct | Status | Confidence | Summary |
|---|---|---|---|
| `evidence_gap` | `supported_for_reviewed_packs` | high | Supported when interpreted as initial/pre-resolution missing approval or unresolved accountant-stage evidence gap. |
| `informal_pressure` | `partially_supported_needs_revision` | medium | Supported as pressure context for `apply_deadline_pressure` paths, but pressure-citation metric rules need tightening. |
| `approval_evidence_propagation` | `supported_for_reviewed_packs` | high | Supported for preserving explicit approval when present and missing approval when absent. |
| `coordination_gap` | `supported_for_reviewed_packs` | high | Supported where unresolved approval reaches accounting and payment is held. |
| `approval_bypass` | `not_observed_in_reviewed_packs` | high | No reviewed representative pack shows payment preparation without explicit approval. |
| `responsibility_diffusion` | `not_observed_in_reviewed_packs` | medium | Reviewed handoffs are documented evidence requests or holds, not ownership avoidance. |
| `policy_ambiguity_exploited` | `not_observed_in_reviewed_packs` | medium | Ambiguity is noted, but not used to justify a questionable path. |
| `communication_breakdown` | `not_observed_in_reviewed_packs` | high | Reviewed paths are reconstructable and do not show material missed or contradicted information. |

## Main Findings

- `evidence_gap`, `approval_evidence_propagation`, and `coordination_gap` are construct-valid enough for reviewed representative-pack descriptions when their interpretation limits are preserved.
- `informal_pressure` is partially supported only as pressure-context evidence. It should not be used as pressure causation or pressure-propagation proof.
- `approval_bypass`, `responsibility_diffusion`, `policy_ambiguity_exploited`, and `communication_breakdown` were not observed in the reviewed representative packs.
- The six human-reviewed pressure-citation `needs_revision` items remain open. Pressure aggregate summaries should not be relied on until metric rules are tightened.

## Checkpoint Recommendation

Advance only to a metric/protocol correction for pressure-citation rules, or to a tightly bounded intervention-validity protocol that preserves this limitation. Do not proceed to stronger claim synthesis.
