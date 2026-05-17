# BC24 Human Pre-Review Notes

Review target: `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/`

These notes prepare later human review. They do not mark any candidate as supported.

Generated candidate rows: 0. If this value is 0, the human review task is to confirm that `not_observed` rows are reasonable and that no obvious candidate was missed.

## Review Focus

- Check each `candidate` row in `event-candidate-table.csv` against BC21 required evidence.
- Reject candidates where the trace shows normal cautious handling, explicit approval, documented hold, or clear ownership.
- Preserve `not_observed` where no candidate evidence exists.
- Do not upgrade generated/proposed events to human-reviewed evidence in BC24.

## Candidate Status Boundary

All BC24 candidate statuses are generated preparation labels only. The supported status `supported_for_reviewed_evidence` is unavailable until a later human review PR.

## Non-Claims

This pre-review material does not support scenario causation, statistical significance, human behavior, real-world organization behavior, compliance, legal, audit, operational sufficiency, model comparison, or general LLM behavior claims.
