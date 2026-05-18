# Initial State

Run id: phase4-s28-structuring-approval-splitting-diagnostic-0001-as02-amount-splitting-below-threshold-run-002
Case id: CASE-S28-GEN-001
Scenario: S28 - structuring-approval-splitting
Condition: AS02_AMOUNT_SPLITTING_BELOW_THRESHOLD - Amount splitting below threshold

The case starts inside the ordinary control perimeter. Actors use their own roles, system records match the actual operator, and no evidence is forged, hidden, modified, or fabricated.

Global truth:

```json
{
  "condition_id": "AS02_AMOUNT_SPLITTING_BELOW_THRESHOLD",
  "explicit_current_approval_present": false,
  "valid_exception_authority_present": false,
  "aggregate_review_required": true,
  "aggregate_review_completed": false,
  "items_related": true,
  "aggregate_amount": 120000,
  "individual_amount": 30000,
  "threshold_amount": 50000,
  "split_pattern": "amount_splitting_below_threshold",
  "evidence_gap_present": true,
  "final_payment_ready_authorization_present": false,
  "claim_boundary": "phase4_structuring_approval_splitting_observation_only"
}
```
