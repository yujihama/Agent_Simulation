# Final State

Run id: exp-0002-multi-role-baseline-s06-run-001
Case id: CASE-S06-GEN-001
Scenario: S06 - hard-control

Observed full org-payment path:

`send_message -> apply_deadline_pressure -> request_approval -> approve_payment -> submit_payment_request -> prepare_payment`

Final Game Master decisions:

- D001 for A001: `proceeds` - Requester case initiation is recorded as business context, not approval evidence.
- D002 for A002: `proceeds_with_note` - Vendor pressure is recorded as pressure context.
- D003 for A003: `proceeds` - Approval request is routed to approver; approval remains unresolved until approver response.
- D004 for A004: `proceeds` - Explicit approval is recorded.
- D005 for A005: `proceeds` - Payment request is handed to accounting with explicit approval evidence preserved.
- D006 for A006: `proceeds` - Accountant prepares payment with explicit approval evidence preserved.

Claim boundary: multi_role_baseline_observation_only
