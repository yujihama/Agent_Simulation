# Construct Validity Limitations

Date: 2026-05-17
Check id: `EXP-0002-CV-0001`

## Scope Limits

- The check covers 14 curated representative evidence packs, not all raw EXP-0002 runs.
- The check relies on the primary human review recorded in `human-review-0001`; no secondary reviewer or inter-rater reliability assessment exists.
- The check does not revise EXP-0002 results, aggregate metrics, event taxonomy, or metrics protocol.

## Metric Limits

Six pressure-citation metric checks remain `needs_revision`. These occur where the vendor selected `request_payment_status`, but generic payment-delay or vendor-dissatisfaction language appears to have been counted as pressure language.

Until metric rules are tightened:

- pressure-citation aggregate counts should not be treated as fully construct-valid
- `request_payment_status` paths should not be used as positive pressure examples
- `informal_pressure` should be reported only as pressure-context evidence when explicit pressure action or wording exists

## Claim Limits

This check does not support:

- statistical significance
- scenario causation
- requester-framing causation
- pressure causation
- pressure-propagation proof
- responsibility-diffusion proof
- approval-bypass proof
- human behavior claims
- real-world organization claims
- compliance, legal, audit, or operational sufficiency claims
- model comparison or general LLM behavior claims

## Next Step

Before intervention validity or pressure-focused reporting relies on pressure summaries, add a metric/protocol correction that narrows pressure-citation rules to explicit pressure actions or explicit pressure wording.
