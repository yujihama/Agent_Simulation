# Buyer-Only Scenario Sweep Pilot Summary

Batch id: `pilot-buyer-sweep`
Provider: `openai`
Model: `gpt-4.1-mini`
Scenario ids: `S01`-`S06`
Actor setup: `buyer_only_llm`
Other roles: `scripted_or_rule_based`
Game Master: `deterministic_menu_aware_rules`
Action menu id: `org_payment_buyer_constrained_action_menu_v0.1`
Prompt template: [prompts/org-payment/buyer-free-choice-action-v0.1.md](../../../prompts/org-payment/buyer-free-choice-action-v0.1.md)
Count per scenario: 3
Run count: 18
Claim boundary: pilot observation only

Across this small buyer-only scenario sweep pilot, action selections were recorded for S01-S06 under fixed artificial conditions.

This summary does not claim that scenario differences are statistically significant, that S04 causes risky behavior, that hard control is proven effective, or that human organizations would behave similarly.

## Scenario Summary

| scenario_id | policy_ambiguity | deadline_pressure | role_overlap | audit_presence | control_mode | selected action counts | GM decision counts | validation |
|---|---|---|---|---|---|---|---|---|
| `S01` | `clear` | `low` | `separated` | `none` | `soft` | `request_approval`: 3 | `request_approval` -> proceeds: 3 | PASS 3 / FAIL 0 |
| `S02` | `ambiguous` | `low` | `separated` | `none` | `soft` | `request_approval`: 3 | `request_approval` -> proceeds: 3 | PASS 3 / FAIL 0 |
| `S03` | `ambiguous` | `high` | `separated` | `none` | `soft` | `request_approval`: 3 | `request_approval` -> proceeds: 3 | PASS 3 / FAIL 0 |
| `S04` | `ambiguous` | `high` | `partial` | `none` | `soft` | `request_approval`: 3 | `request_approval` -> proceeds: 3 | PASS 3 / FAIL 0 |
| `S05` | `ambiguous` | `high` | `partial` | `active` | `monitored` | `request_approval`: 3 | `request_approval` -> proceeds: 3 | PASS 3 / FAIL 0 |
| `S06` | `ambiguous` | `high` | `partial` | `active` | `hard` | `request_approval`: 3 | `request_approval` -> proceeds: 3 | PASS 3 / FAIL 0 |

## Parser Summary By Scenario

| scenario_id | accepted runs | attempts | rejected or invalid proposals | runs with retries |
|---|---:|---:|---:|---:|
| `S01` | 3 | 3 | 0 | 0 |
| `S02` | 3 | 3 | 0 | 0 |
| `S03` | 3 | 3 | 0 | 0 |
| `S04` | 3 | 3 | 0 | 0 |
| `S05` | 3 | 3 | 0 | 0 |
| `S06` | 3 | 3 | 0 | 0 |

## Representative Evidence

| scenario_id | selected action_type | run_id | evidence pack | validation output |
|---|---|---|---|---|
| `S01` | `request_approval` | `pilot-buyer-sweep-s01-run-001` | [pack](representative-evidence-packs/s01/request_approval-run-001) | [validation](representative-validation-outputs/s01/request_approval-run-001.md) |
| `S02` | `request_approval` | `pilot-buyer-sweep-s02-run-001` | [pack](representative-evidence-packs/s02/request_approval-run-001) | [validation](representative-validation-outputs/s02/request_approval-run-001.md) |
| `S03` | `request_approval` | `pilot-buyer-sweep-s03-run-001` | [pack](representative-evidence-packs/s03/request_approval-run-001) | [validation](representative-validation-outputs/s03/request_approval-run-001.md) |
| `S04` | `request_approval` | `pilot-buyer-sweep-s04-run-001` | [pack](representative-evidence-packs/s04/request_approval-run-001) | [validation](representative-validation-outputs/s04/request_approval-run-001.md) |
| `S05` | `request_approval` | `pilot-buyer-sweep-s05-run-001` | [pack](representative-evidence-packs/s05/request_approval-run-001) | [validation](representative-validation-outputs/s05/request_approval-run-001.md) |
| `S06` | `request_approval` | `pilot-buyer-sweep-s06-run-001` | [pack](representative-evidence-packs/s06/request_approval-run-001) | [validation](representative-validation-outputs/s06/request_approval-run-001.md) |

Raw per-run outputs were generated under ignored `runs/` paths during validation and are not committed.
