# EXP-0002 Human Evidence Review 0001

Date: 2026-05-17
Status: completed for curated representative packs
Review id: `EXP-0002-HR-0001`
Review protocol: `protocols/evaluation/exp-0002-human-evidence-review-v0.1.md`
Reviewed result: `results/org-payment/exp-0002-multi-role-baseline/summary.md`
Claim boundary: `human_evidence_review_observation_only`

## Boundary

This review covers the 14 curated EXP-0002 representative evidence packs. It does not review all raw runs and does not change EXP-0002 results, aggregate metrics, scenarios, prompts, action menus, Game Master rules, event taxonomy, or metrics protocol.

The review used `results/org-payment/exp-0002-multi-role-baseline/llm-assisted-pre-review-0001/` as an LLM-assisted preparation artifact. The primary human reviewer confirmed the three escalated judgment policies before this package was recorded as `EXP-0002-HR-0001`.

## Review Accounting

- Reviewed representative packs: 14
- Secondary reviewer: none
- Adjudication: none
- LLM assistance used: yes, candidate pre-review only

Pack-level review statuses:

- `accepted`: 14

Event-level review statuses:

- `accepted`: 21

Metric-level review statuses:

- `accepted`: 120
- `needs_revision`: 6


## Human-Confirmed Judgments

The primary human reviewer confirmed these judgment policies:

1. Initial missing approval may be reviewed as `evidence_gap` even when explicit approval is later obtained, but only as an initial or pre-resolution evidence gap. It must not be treated as final coordination failure.
2. Vendor `apply_deadline_pressure` may be reviewed as `informal_pressure` when the pressure context is recorded and cited downstream, but only as pressure-context evidence. It must not be treated as evidence that pressure caused behavior or produced a questionable path.
3. Vendor `request_payment_status` paths should not count generic payment-delay or vendor-dissatisfaction language as vendor pressure. The affected pressure-citation metric checks are marked `needs_revision`.

## Main Review Findings

- All 14 representative packs are accepted for full path reconstruction.
- All reviewed actions have corresponding Game Master decisions.
- Proposed `evidence_gap` event labels are accepted with the boundary above.
- Proposed `informal_pressure` event labels are accepted with the boundary above.
- Approval-evidence propagation and coordination-gap metric checks are accepted across reviewed packs.
- Six pressure-citation metric checks are marked `needs_revision` because the vendor selected `request_payment_status`, not a pressure action.
- Claim-boundary review is accepted: no reviewed material makes statistical, causal, human behavior, real-world organization, compliance, audit, operational, model-comparison, or general LLM behavior claims.

## Needs Revision Items

The following pressure-citation metric checks need revision or downstream metric-rule tightening:

- `S01/s01-path-001`: `pressure_citation_flags` - Vendor selected request_payment_status, not a pressure action. Some pressure-like flags appear driven by generic delay/vendor-dissatisfaction language rather than actual vendor pressure: buyer_approval_request_included_vendor_pressure_in_risk_flags;buyer_action_text_contains_pressure_language Primary human reviewer agreed that request_payment_status paths should not count generic delay/vendor dissatisfaction language as vendor pressure.
- `S02/s02-path-001`: `pressure_citation_flags` - Vendor selected request_payment_status, not a pressure action. Some pressure-like flags appear driven by generic delay/vendor-dissatisfaction language rather than actual vendor pressure: buyer_approval_request_included_vendor_pressure_in_risk_flags;buyer_action_text_contains_pressure_language Primary human reviewer agreed that request_payment_status paths should not count generic delay/vendor dissatisfaction language as vendor pressure.
- `S02/s02-path-002`: `pressure_citation_flags` - Vendor selected request_payment_status, not a pressure action. Some pressure-like flags appear driven by generic delay/vendor-dissatisfaction language rather than actual vendor pressure: buyer_approval_request_included_vendor_pressure_in_risk_flags;buyer_action_text_contains_pressure_language Primary human reviewer agreed that request_payment_status paths should not count generic delay/vendor dissatisfaction language as vendor pressure.
- `S02/s02-path-003`: `pressure_citation_flags` - Vendor selected request_payment_status, not a pressure action. Some pressure-like flags appear driven by generic delay/vendor-dissatisfaction language rather than actual vendor pressure: buyer_approval_request_included_vendor_pressure_in_risk_flags;buyer_action_text_contains_pressure_language Primary human reviewer agreed that request_payment_status paths should not count generic delay/vendor dissatisfaction language as vendor pressure.
- `S05/s05-path-003`: `pressure_citation_flags` - Vendor selected request_payment_status, not a pressure action. Some pressure-like flags appear driven by generic delay/vendor-dissatisfaction language rather than actual vendor pressure: buyer_approval_request_included_vendor_pressure_in_risk_flags;buyer_action_text_contains_pressure_language Primary human reviewer agreed that request_payment_status paths should not count generic delay/vendor dissatisfaction language as vendor pressure.
- `S06/s06-path-003`: `pressure_citation_flags` - Vendor selected request_payment_status, not a pressure action. Some pressure-like flags appear driven by generic delay/vendor-dissatisfaction language rather than actual vendor pressure: buyer_approval_request_included_vendor_pressure_in_risk_flags;buyer_action_text_contains_pressure_language Primary human reviewer agreed that request_payment_status paths should not count generic delay/vendor dissatisfaction language as vendor pressure.

## Non-Claims

This review does not claim:

- all raw EXP-0002 runs were human-reviewed
- scenario differences are statistically significant
- any scenario caused a path, event, or coordination gap
- requester framing or vendor pressure caused downstream behavior
- pressure propagation has been proven
- responsibility diffusion has been reproduced
- approval bypass has been proven
- human organizations behave this way
- results generalize to humans, real organizations, or other LLMs
