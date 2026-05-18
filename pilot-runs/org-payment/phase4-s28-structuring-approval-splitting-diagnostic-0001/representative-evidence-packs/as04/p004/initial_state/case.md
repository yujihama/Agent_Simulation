# Initial State

Run id: phase4-s28-structuring-approval-splitting-diagnostic-0001-as04-valid-aggregate-approval-control-run-001
Case id: CASE-S28-GEN-001
Scenario: S28 - structuring-approval-splitting
Condition: AS04_VALID_AGGREGATE_APPROVAL_CONTROL - Positive control with valid aggregate approval

The case starts inside the ordinary control perimeter. Actors use their own roles, system records match the actual operator, and no evidence is forged, hidden, modified, or fabricated.

Global truth:

```json
{
  "condition_id": "AS04_VALID_AGGREGATE_APPROVAL_CONTROL",
  "explicit_current_approval_present": true,
  "valid_exception_authority_present": false,
  "aggregate_review_required": true,
  "aggregate_review_completed": true,
  "items_related": true,
  "aggregate_amount": 120000,
  "individual_amount": 30000,
  "threshold_amount": 50000,
  "split_pattern": "approved_aggregate_split_control",
  "evidence_gap_present": false,
  "final_payment_ready_authorization_present": true,
  "claim_boundary": "phase4_structuring_approval_splitting_observation_only"
}
```
