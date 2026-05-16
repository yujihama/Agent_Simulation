# EXP-0005 Expense Reimbursement Second-Domain Pilot

Protocol reference: `protocols/domain-expansion/expense-reimbursement-pilot-v0.1.md`
Scenario: `ER01`
Claim boundary: `second_domain_pilot_observation_only`

## Execution Accounting

| Field | Value |
|---|---:|
| Attempted runs | 5 |
| Accepted runs | 5 |
| Excluded runs | 0 |

Provider/model: `openai` / `gpt-4.1-mini`
Observed model versions: `gpt-4.1-mini-2025-04-14`

## Action Counts

- Employee: `request_approval`: 5
- Manager: `request_more_evidence`: 5
- Finance reviewer: `hold_payment`: 5

## Path Counts

- `request_approval -> request_more_evidence -> hold_payment`: 5

## Evidence Summaries

- Approval-evidence propagation summary: `finance_cited_manager_action_or_decision`: 5, `finance_preserved_gap_when_explicit_approval_absent`: 5
- Evidence-gap summary: `evidence_gap_event_proposed`: 5, `finance_held_payment`: 5, `manager_requested_more_evidence`: 5

## Representative Evidence

- `path-001`: [representative-evidence-packs/path-001](representative-evidence-packs/path-001); validation [representative-validation-outputs/path-001.md](representative-validation-outputs/path-001.md)

## Claim Boundary

Under the frozen EXP-0005 artificial expense-reimbursement protocol, second-domain pilot runs produced the recorded employee, manager, and finance reviewer action paths, parser outcomes, Game Master decisions, validation outcomes, approval-evidence observations, and evidence-gap observations.

This result is bounded to `second_domain_pilot_observation_only`. It does not support cross-domain generalization, statistical significance, causal claims, human behavior, real-world organization claims, compliance, legal, audit, operational sufficiency, model comparison, or general LLM behavior claims.

## Limitations

- artificial organization only
- second-domain pilot only
- expense reimbursement ER01 only
- 5 attempted runs before exclusions
- generated/proposed event labels are not human-reviewed coded evidence
- no cross-domain generalization claim
- no human behavior claim
- no general LLM behavior claim
- no real-world organization claim
- no compliance, legal, audit, or operational sufficiency claim
- no statistical significance claim
