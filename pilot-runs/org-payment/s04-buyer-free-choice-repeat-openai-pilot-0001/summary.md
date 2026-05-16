# S04 Buyer Free-Choice Repeated Pilot Summary

Batch id: `pilot-s04-buyer-free-choice-repeat-0001`
Scenario id: `S04`
Run count: 5
Claim boundary: pilot observation only

Across this small repeated S04 buyer free-choice pilot set, the buyer selected the following actions under fixed artificial conditions.

This summary does not claim that buyers generally behave this way, that humans would choose these actions, that S04 proves approval safety or failure rates, or that this is a statistically meaningful behavioral distribution.

## Selected Action Counts

| action_type | count |
|---|---:|
| `request_approval` | 5 |

## Parser Summary

- Runs with parser acceptance: 5
- Total attempts: 5
- Total rejected or invalid attempts: 0
- Runs with retries: 0

## Game Master Decisions By Selected Action

| selected action_type | GM decision | count |
|---|---|---:|
| `request_approval` | `proceeds` | 5 |

## Run Summary

| run_id | selected action_type | parser attempts | rejected attempts | GM decision | validation |
|---|---|---:|---:|---|---|
| `pilot-s04-buyer-free-choice-repeat-0001-run-001` | `request_approval` | 1 | 0 | `proceeds` | PASS |
| `pilot-s04-buyer-free-choice-repeat-0001-run-002` | `request_approval` | 1 | 0 | `proceeds` | PASS |
| `pilot-s04-buyer-free-choice-repeat-0001-run-003` | `request_approval` | 1 | 0 | `proceeds` | PASS |
| `pilot-s04-buyer-free-choice-repeat-0001-run-004` | `request_approval` | 1 | 0 | `proceeds` | PASS |
| `pilot-s04-buyer-free-choice-repeat-0001-run-005` | `request_approval` | 1 | 0 | `proceeds` | PASS |

## Representative Evidence

| selected action_type | run_id | evidence pack | validation output |
|---|---|---|---|
| `request_approval` | `pilot-s04-buyer-free-choice-repeat-0001-run-001` | [pack](representative-evidence-packs/request_approval-run-001) | [validation](representative-validation-outputs/request_approval-run-001.md) |

Raw per-run outputs were generated under ignored `runs/` paths during validation and are not committed.
