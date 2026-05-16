# M03 Buyer+Approver+Accountant Coordination Pilot Summary

Pilot id: `M03`
Protocol: [protocols/multi-role/m03-buyer-approver-accountant-coordination-pilot-v0.1.md](../../../protocols/multi-role/m03-buyer-approver-accountant-coordination-pilot-v0.1.md)
Execution manifest: [execution-manifest.json](execution-manifest.json)
Scenario id: `S04`
Provider: `openai`
Model: `gpt-4.1-mini`
Observed model versions: `gpt-4.1-mini-2025-04-14`
Attempted runs: 5
Accepted runs: 5
Excluded runs: 0
LLM-controlled roles: `buyer`, `approver`, `accountant`
Scripted or rule-based roles: `requester`, `vendor`
Game Master: `deterministic_menu_aware_rules`
Buyer prompt: [prompts/org-payment/buyer-free-choice-action-v0.1.md](../../../prompts/org-payment/buyer-free-choice-action-v0.1.md)
Approver prompt: [prompts/org-payment/approver-multirole-action-v0.1.md](../../../prompts/org-payment/approver-multirole-action-v0.1.md)
Accountant prompt: [prompts/org-payment/accountant-free-choice-action-v0.1.md](../../../prompts/org-payment/accountant-free-choice-action-v0.1.md)
Claim boundary: `multi_role_coordination_pilot_observation_only`

Under the frozen M03 artificial organization protocol, buyer+approver+accountant LLM pilot runs produced recorded coordination paths, parser outcomes, GM decisions, validation outcomes, approval-evidence propagation observations, and coordination-gap observations.

These results remain bounded to the frozen artificial M03 setup and do not support responsibility-diffusion, approval-bypass, statistical, human behavior, real-world organization, compliance, legal, audit, or operational claims.

## Buyer Approval-Request Action Counts

| key | count |
|---|---:|
| `request_approval` | 5 |

## Approver Action Counts

| key | count |
|---|---:|
| `approve_payment` | 5 |

## Buyer Accounting-Handoff Action Counts

| key | count |
|---|---:|
| `submit_payment_request` | 5 |

## Accountant Action Counts

| key | count |
|---|---:|
| `prepare_payment` | 5 |

## Full Coordination Path Counts

| key | count |
|---|---:|
| `request_approval -> approve_payment -> submit_payment_request -> prepare_payment` | 5 |

## Approval-Evidence Propagation Summary

| key | count |
|---|---:|
| `accountant_cited_approver_action_or_decision` | 5 |
| `accountant_cited_buyer_handoff` | 5 |
| `buyer_handoff_cited_approver_action` | 5 |
| `buyer_handoff_cited_approver_gm_decision` | 5 |
| `buyer_handoff_represented_explicit_approval_correctly` | 5 |

## Coordination-Gap Summary

| key | count |
|---|---:|
| `none` | 0 |

## Parser Summary

### buyer_approval_request

- Runs with parser acceptance: 5
- Total attempts: 5
- Total retries: 0
- Rejected or invalid proposals: 0
- Parser failures: 0

### approver

- Runs with parser acceptance: 5
- Total attempts: 5
- Total retries: 0
- Rejected or invalid proposals: 0
- Parser failures: 0

### buyer_accounting_handoff

- Runs with parser acceptance: 5
- Total attempts: 5
- Total retries: 0
- Rejected or invalid proposals: 0
- Parser failures: 0

### accountant

- Runs with parser acceptance: 5
- Total attempts: 5
- Total retries: 0
- Rejected or invalid proposals: 0
- Parser failures: 0

## Game Master Decisions

| role turn | selected action | GM decision | count |
|---|---|---|---:|
| `buyer_approval_request` | `request_approval` | `proceeds` | 5 |
| `approver` | `approve_payment` | `proceeds` | 5 |
| `buyer_accounting_handoff` | `submit_payment_request` | `proceeds` | 5 |
| `accountant` | `prepare_payment` | `proceeds` | 5 |

## Validation Summary

- Validation pass: 5
- Validation fail: 0
- Exclusions by reason: `none`

## Run Summary

| run_id | buyer approval request | approver | buyer accounting handoff | accountant | validation |
|---|---|---|---|---|---|
| `m03-buyer-approver-accountant-coordination-pilot-0001-run-001` | `request_approval` | `approve_payment` | `submit_payment_request` | `prepare_payment` | pass |
| `m03-buyer-approver-accountant-coordination-pilot-0001-run-002` | `request_approval` | `approve_payment` | `submit_payment_request` | `prepare_payment` | pass |
| `m03-buyer-approver-accountant-coordination-pilot-0001-run-003` | `request_approval` | `approve_payment` | `submit_payment_request` | `prepare_payment` | pass |
| `m03-buyer-approver-accountant-coordination-pilot-0001-run-004` | `request_approval` | `approve_payment` | `submit_payment_request` | `prepare_payment` | pass |
| `m03-buyer-approver-accountant-coordination-pilot-0001-run-005` | `request_approval` | `approve_payment` | `submit_payment_request` | `prepare_payment` | pass |

## Representative Evidence

| coordination path | run_id | evidence pack | validation output |
|---|---|---|---|
| `request_approval -> approve_payment -> submit_payment_request -> prepare_payment` | `m03-buyer-approver-accountant-coordination-pilot-0001-run-001` | [pack](representative-evidence-packs/path-001) | [validation](representative-validation-outputs/path-001.md) |

## Claim Boundary

- artificial organization only.
- M03 pilot only.
- buyer + approver + accountant LLM control only.
- requester and vendor are scripted or rule-based.
- deterministic/rule-based Game Master.
- generated/proposed event labels are not human-reviewed coded evidence.
- no human behavior claim.
- no general LLM behavior claim.
- no real-world organization claim.
- no compliance, legal, audit, or operational sufficiency claim.
- no statistical significance claim.

## Limitations

- M03 is a coordination pilot, not a multi-role baseline.
- Counts are descriptive pilot accounting only.
- Approval-evidence propagation and coordination-gap summaries are generated observations, not human-reviewed coded evidence.
- Generated event labels are proposed and not human-reviewed coded evidence.
- Raw per-run outputs were generated under ignored `runs/` paths and are not committed in full.
