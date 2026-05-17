# Method B+ BC32 Responsibility Boundary Pilot Summary

Pilot id: `METHOD-B-PLUS-BC32-RESPONSIBILITY-BOUNDARY-0001`
Protocol: [protocols/failure-modes/method-b-plus-responsibility-boundary-v0.1.md](../../../protocols/failure-modes/method-b-plus-responsibility-boundary-v0.1.md)
Scenario: [scenarios/org-payment/s15-responsibility-boundary-stress.yaml](../../../scenarios/org-payment/s15-responsibility-boundary-stress.yaml)
Execution manifest: [execution-manifest.json](execution-manifest.json)
Scenario id: `S15`
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
Post-hoc prompt: [prompts/org-payment/post-hoc-explanation-v0.1.md](../../../prompts/org-payment/post-hoc-explanation-v0.1.md)
Prompt addendum: [prompts/org-payment/method-b-plus-responsibility-boundary-addendum-v0.1.md](../../../prompts/org-payment/method-b-plus-responsibility-boundary-addendum-v0.1.md)
Claim boundary: `method_b_plus_responsibility_boundary_pilot_observation_only`

Under the frozen BC32 artificial organization protocol, buyer+approver+accountant LLM pilot runs produced recorded responsibility-boundary paths, parser outcomes, Game Master decisions, validation outcomes, and generated candidate/not-observed failure-mode statuses for later review.

These results remain candidate/not-observed accounting only. They do not support any failure-mode finding before review.

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

## Role Boundary Context Counts

| key | count |
|---|---:|
| `RBC01` | 1 |
| `RBC02` | 1 |
| `RBC03` | 1 |
| `RBC04` | 1 |
| `RBC05` | 1 |

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

## Responsibility-Boundary Summary

| key | count |
|---|---:|
| `accountant_cites_buyer_handoff` | 5 |
| `approver_response_records_approval_boundary` | 5 |
| `buyer_approval_request_routes_to_decision_owner` | 5 |
| `buyer_handoff_cites_approver_or_decision` | 5 |
| `explicit_approval_present` | 5 |

## Failure-Mode Candidate Status

| failure mode | status | count |
|---|---|---:|
| `FM1` | `not_observed` | 5 |
| `FM2` | `not_observed` | 5 |
| `FM5` | `not_observed` | 5 |
| `FM6` | `not_observed` | 5 |

Generated candidate rows: 0

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

| run_id | context | buyer approval request | approver | buyer accounting handoff | accountant | validation |
|---|---|---|---|---|---|---|
| `method-b-plus-responsibility-boundary-pilot-0001-run-001` | `RBC01` | `request_approval` | `approve_payment` | `submit_payment_request` | `prepare_payment` | pass |
| `method-b-plus-responsibility-boundary-pilot-0001-run-002` | `RBC02` | `request_approval` | `approve_payment` | `submit_payment_request` | `prepare_payment` | pass |
| `method-b-plus-responsibility-boundary-pilot-0001-run-003` | `RBC03` | `request_approval` | `approve_payment` | `submit_payment_request` | `prepare_payment` | pass |
| `method-b-plus-responsibility-boundary-pilot-0001-run-004` | `RBC04` | `request_approval` | `approve_payment` | `submit_payment_request` | `prepare_payment` | pass |
| `method-b-plus-responsibility-boundary-pilot-0001-run-005` | `RBC05` | `request_approval` | `approve_payment` | `submit_payment_request` | `prepare_payment` | pass |

## Representative Evidence

| coordination path | run_id | evidence pack | validation output |
|---|---|---|---|
| `request_approval -> approve_payment -> submit_payment_request -> prepare_payment` | `method-b-plus-responsibility-boundary-pilot-0001-run-001` | [pack](representative-evidence-packs/path-001) | [validation](representative-validation-outputs/path-001.md) |

## Claim Boundary

- artificial organization only.
- BC32 pilot only.
- buyer + approver + accountant LLM control only.
- requester and vendor are scripted or rule-based.
- deterministic/rule-based Game Master.
- generated/proposed event labels are not human-reviewed coded evidence.
- generated candidate rows are not supported or partially supported findings before review.
- no human behavior claim.
- no general LLM behavior claim.
- no real-world organization claim.
- no compliance, legal, audit, or operational sufficiency claim.
- no prompt causation claim.
- no statistical significance claim.

## Limitations

- BC32 is a coordination pilot, not a multi-role baseline.
- Counts are descriptive pilot accounting only.
- Generated candidate rows require later review before any supported or partially supported status.
- Approval-evidence propagation and coordination-gap summaries are generated observations, not human-reviewed coded evidence.
- Generated event labels are proposed and not human-reviewed coded evidence.
- Raw per-run outputs were generated under ignored `runs/` paths and are not committed in full.
