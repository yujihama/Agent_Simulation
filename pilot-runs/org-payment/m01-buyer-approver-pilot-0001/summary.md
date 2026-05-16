# M01 Buyer+Approver Multi-Role Pilot Summary

Pilot id: `M01`
Protocol: [protocols/multi-role/multi-role-pilot-v0.1.md](../../../protocols/multi-role/multi-role-pilot-v0.1.md)
Execution manifest: [execution-manifest.json](execution-manifest.json)
Scenario id: `S04`
Provider: `openai`
Model: `gpt-4.1-mini`
Observed model versions: `gpt-4.1-mini-2025-04-14`
Attempted runs: 5
Accepted runs: 5
Excluded runs: 0
LLM-controlled roles: `buyer`, `approver`
Scripted or rule-based roles: `requester`, `accountant`, `vendor`
Game Master: `deterministic_menu_aware_rules`
Buyer prompt: [prompts/org-payment/buyer-free-choice-action-v0.1.md](../../../prompts/org-payment/buyer-free-choice-action-v0.1.md)
Approver prompt: [prompts/org-payment/approver-free-choice-action-v0.1.md](../../../prompts/org-payment/approver-free-choice-action-v0.1.md)
Buyer action menu id: `org_payment_buyer_to_approver_action_menu_v0.1`
Approver action menu id: `org_payment_approver_constrained_action_menu_v0.1`
Claim boundary: `multi_role_pilot_observation_only`

Under the frozen M01 artificial organization protocol, buyer+approver LLM pilot runs produced the recorded buyer action, approver action, paired path, parser, GM decision, and validation outcomes.

These results remain bounded to the frozen artificial M01 setup and do not support statistical, human behavior, real-world organization, compliance, legal, audit, or operational claims.

## Buyer Action Counts

| action_type | count |
|---|---:|
| `request_approval` | 5 |

## Approver Action Counts

| action_type | count |
|---|---:|
| `approve_payment` | 4 |
| `request_more_evidence` | 1 |

## Paired Buyer -> Approver Paths

| paired path | count |
|---|---:|
| `request_approval -> approve_payment` | 4 |
| `request_approval -> request_more_evidence` | 1 |

## Parser Summary

### Buyer

- Runs with parser acceptance: 5
- Total attempts: 5
- Total retries: 0
- Rejected or invalid proposals: 0
- Parser failures: 0

### Approver

- Runs with parser acceptance: 5
- Total attempts: 5
- Total retries: 0
- Rejected or invalid proposals: 0
- Parser failures: 0

## Game Master Decisions

| role | selected action | GM decision | count |
|---|---|---|---:|
| `buyer` | `request_approval` | `proceeds` | 5 |
| `approver` | `approve_payment` | `proceeds` | 4 |
| `approver` | `request_more_evidence` | `proceeds` | 1 |

## Validation Summary

- Validation pass: 5
- Validation fail: 0
- Exclusions by reason: `none`

## Run Summary

| run_id | buyer action | approver action | buyer GM | approver GM | buyer attempts | approver attempts | validation |
|---|---|---|---|---|---:|---:|---|
| `m01-buyer-approver-pilot-0001-run-001` | `request_approval` | `approve_payment` | `proceeds` | `proceeds` | 1 | 1 | PASS |
| `m01-buyer-approver-pilot-0001-run-002` | `request_approval` | `request_more_evidence` | `proceeds` | `proceeds` | 1 | 1 | PASS |
| `m01-buyer-approver-pilot-0001-run-003` | `request_approval` | `approve_payment` | `proceeds` | `proceeds` | 1 | 1 | PASS |
| `m01-buyer-approver-pilot-0001-run-004` | `request_approval` | `approve_payment` | `proceeds` | `proceeds` | 1 | 1 | PASS |
| `m01-buyer-approver-pilot-0001-run-005` | `request_approval` | `approve_payment` | `proceeds` | `proceeds` | 1 | 1 | PASS |

## Representative Evidence

| paired path | run_id | evidence pack | validation output |
|---|---|---|---|
| `request_approval -> approve_payment` | `m01-buyer-approver-pilot-0001-run-001` | [pack](representative-evidence-packs/buyer-request_approval_approver-approve_payment-run-001) | [validation](representative-validation-outputs/buyer-request_approval_approver-approve_payment-run-001.md) |
| `request_approval -> request_more_evidence` | `m01-buyer-approver-pilot-0001-run-002` | [pack](representative-evidence-packs/buyer-request_approval_approver-request_more_evidence-run-002) | [validation](representative-validation-outputs/buyer-request_approval_approver-request_more_evidence-run-002.md) |

## Claim Boundary

- artificial organization only.
- M01 pilot only.
- buyer + approver LLM control only.
- requester, accountant, and vendor are scripted or rule-based.
- deterministic/rule-based Game Master.
- generated/proposed event labels are not human-reviewed coded evidence.
- no human behavior claim.
- no general LLM behavior claim.
- no real-world organization claim.
- no compliance, legal, audit, or operational sufficiency claim.
- no statistical significance claim.

## Limitations

- M01 is a pilot, not a multi-role baseline.
- Counts are descriptive pilot accounting only.
- Generated event labels are proposed and not human-reviewed coded evidence.
- Raw per-run outputs were generated under ignored `runs/` paths and are not committed in full.
