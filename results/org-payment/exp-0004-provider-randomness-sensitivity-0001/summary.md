# EXP-0004 Provider-Randomness Sensitivity Summary

Protocol reference: `protocols/evaluation/exp-0004-provider-randomness-sensitivity-v0.1.md`
Baseline comparator: `results/org-payment/exp-0002-multi-role-baseline/aggregate.json`
Claim boundary: `provider_randomness_sensitivity_observation_only`

## Execution Accounting

| Field | Value |
|---|---:|
| Attempted runs | 12 |
| Accepted runs | 12 |
| Excluded runs | 0 |

Provider/model: `openai` / `gpt-4.1-mini`
Observed model versions: `gpt-4.1-mini-2025-04-14`

## EXP-0002 Comparison

| Scenario | EXP-0002 accepted | EXP-0004 accepted | Descriptive status | New paths in EXP-0004 |
|---|---:|---:|---|---|
| `S01` | 5 | 2 | `same_path_set_observed` | `none` |
| `S02` | 5 | 2 | `subset_of_baseline_paths_observed` | `none` |
| `S03` | 5 | 2 | `same_path_set_observed` | `none` |
| `S04` | 5 | 2 | `overlap_with_new_sensitivity_path` | `send_message -> apply_deadline_pressure -> request_approval -> approve_payment -> submit_payment_request -> prepare_payment` |
| `S05` | 5 | 2 | `subset_of_baseline_paths_observed` | `none` |
| `S06` | 5 | 2 | `overlap_with_new_sensitivity_path` | `send_message -> apply_deadline_pressure -> request_approval -> request_more_evidence -> request_more_evidence -> hold_payment` |

Detailed path counts are recorded in `aggregate.json` and `comparison-table.csv`.
Committed full representative evidence packs are limited to 2 selected packs so this execution PR remains reviewable. The aggregate and execution manifest still account for all attempted and accepted runs.

## Claim Boundary

EXP-0004 is a small provider-randomness repeat-run sensitivity check. It keeps model, prompts, action menus, scenarios, parser rules, metrics, and deterministic Game Master behavior fixed. It does not support model comparison, prompt comparison, action-menu comparison, Game Master strictness comparison, scenario wording comparison, statistical significance, causal claims, human behavior claims, real-world organization claims, compliance, legal, audit, operational sufficiency claims, or general LLM behavior claims.

## Limitations

- provider-randomness sensitivity observation only
- 2 attempted runs per scenario before exclusions
- small-n descriptive comparison against EXP-0002 only
- committed full representative evidence packs are capped at 2 selected packs to keep the execution PR reviewable
- model, prompts, action menus, scenario wording, parser rules, metrics, and Game Master behavior are held fixed
- provider default randomness is not explicitly seeded or controlled
- no statistical significance claim
- no causal claim
- no model comparison claim
- no prompt sensitivity claim
- no action-menu sensitivity claim
- no Game Master strictness sensitivity claim
- no scenario wording sensitivity claim
- no human behavior or real-world organization claim
