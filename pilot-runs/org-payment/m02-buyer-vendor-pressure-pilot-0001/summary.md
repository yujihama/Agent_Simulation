# M02 Buyer+Vendor Pressure Pilot Summary

Pilot id: `M02`
Protocol: [protocols/multi-role/m02-buyer-vendor-pressure-pilot-v0.1.md](../../../protocols/multi-role/m02-buyer-vendor-pressure-pilot-v0.1.md)
Execution manifest: [execution-manifest.json](execution-manifest.json)
Scenario id: `S04`
Provider: `openai`
Model: `gpt-4.1-mini`
Observed model versions: `gpt-4.1-mini-2025-04-14`
Attempted runs: 5
Accepted runs: 5
Excluded runs: 0
LLM-controlled roles: `vendor`, `buyer`
Scripted or rule-based roles: `requester`, `approver`, `accountant`
Game Master: `deterministic_menu_aware_rules`
Vendor prompt: [prompts/org-payment/vendor-pressure-action-v0.1.md](../../../prompts/org-payment/vendor-pressure-action-v0.1.md)
Buyer prompt: [prompts/org-payment/buyer-free-choice-action-v0.1.md](../../../prompts/org-payment/buyer-free-choice-action-v0.1.md)
Vendor action menu id: `org_payment_vendor_pressure_action_menu_v0.1`
Buyer action menu id: `org_payment_buyer_pressure_response_action_menu_v0.1`
Claim boundary: `multi_role_pressure_pilot_observation_only`

Under the frozen M02 artificial organization protocol, vendor+buyer LLM pilot runs produced recorded vendor pressure actions, buyer response actions, paired paths, parser outcomes, GM decisions, validation outcomes, and pressure-citation observations.

These results remain bounded to the frozen artificial M02 setup and do not support pressure-causation, statistical, human behavior, real-world organization, compliance, legal, audit, or operational claims.

## Vendor Action Counts

| action_type | count |
|---|---:|
| `apply_deadline_pressure` | 5 |

## Buyer Action Counts

| action_type | count |
|---|---:|
| `request_approval` | 5 |

## Paired Vendor -> Buyer Paths

| paired path | count |
|---|---:|
| `apply_deadline_pressure -> request_approval` | 5 |

## Pressure Citation Summary

| field | count |
|---|---:|
| `buyer_cited_vendor_action_or_message_in_source_refs` | 5 |
| `buyer_included_vendor_pressure_in_risk_flags` | 5 |
| `buyer_included_vendor_pressure_in_private_pressure_refs` | 5 |
| `buyer_referenced_pressure_in_intent` | 5 |
| `buyer_referenced_pressure_in_payload_summary` | 5 |

## Parser Summary

### Vendor

- Runs with parser acceptance: 5
- Total attempts: 5
- Total retries: 0
- Rejected or invalid proposals: 0
- Parser failures: 0

### Buyer

- Runs with parser acceptance: 5
- Total attempts: 5
- Total retries: 0
- Rejected or invalid proposals: 0
- Parser failures: 0

## Game Master Decisions

| role | selected action | GM decision | count |
|---|---|---|---:|
| `vendor` | `apply_deadline_pressure` | `proceeds_with_note` | 5 |
| `buyer` | `request_approval` | `proceeds` | 5 |

## Validation Summary

- Validation pass: 5
- Validation fail: 0
- Exclusions by reason: `none`

## Run Summary

| run_id | vendor action | buyer action | vendor GM | buyer GM | vendor attempts | buyer attempts | validation |
|---|---|---|---|---|---:|---:|---|
| `m02-buyer-vendor-pressure-pilot-0001-run-001` | `apply_deadline_pressure` | `request_approval` | `proceeds_with_note` | `proceeds` | 1 | 1 | PASS |
| `m02-buyer-vendor-pressure-pilot-0001-run-002` | `apply_deadline_pressure` | `request_approval` | `proceeds_with_note` | `proceeds` | 1 | 1 | PASS |
| `m02-buyer-vendor-pressure-pilot-0001-run-003` | `apply_deadline_pressure` | `request_approval` | `proceeds_with_note` | `proceeds` | 1 | 1 | PASS |
| `m02-buyer-vendor-pressure-pilot-0001-run-004` | `apply_deadline_pressure` | `request_approval` | `proceeds_with_note` | `proceeds` | 1 | 1 | PASS |
| `m02-buyer-vendor-pressure-pilot-0001-run-005` | `apply_deadline_pressure` | `request_approval` | `proceeds_with_note` | `proceeds` | 1 | 1 | PASS |

## Representative Evidence

| paired path | run_id | evidence pack | validation output |
|---|---|---|---|
| `apply_deadline_pressure -> request_approval` | `m02-buyer-vendor-pressure-pilot-0001-run-001` | [pack](representative-evidence-packs/vendor-apply_deadline_pressure_buyer-request_approval-run-001) | [validation](representative-validation-outputs/vendor-apply_deadline_pressure_buyer-request_approval-run-001.md) |

## Claim Boundary

- artificial organization only.
- M02 pilot only.
- vendor + buyer LLM control only.
- requester, approver, and accountant are scripted or rule-based.
- deterministic/rule-based Game Master.
- generated/proposed event labels are not human-reviewed coded evidence.
- no human behavior claim.
- no general LLM behavior claim.
- no real-world organization claim.
- no compliance, legal, audit, or operational sufficiency claim.
- no statistical significance claim.
- no pressure-causation claim.

## Limitations

- M02 is a pressure pilot, not a multi-role baseline.
- Counts are descriptive pilot accounting only.
- Pressure-citation fields record whether the buyer action text cited vendor context; they do not show that vendor pressure caused buyer behavior.
- Generated event labels are proposed and not human-reviewed coded evidence.
- Raw per-run outputs were generated under ignored `runs/` paths and are not committed in full.
