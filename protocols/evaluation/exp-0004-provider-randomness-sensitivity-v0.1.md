# EXP-0004 Provider-Randomness Sensitivity Protocol v0.1

Date: 2026-05-17
Status: accepted
Phase: P9
Checkpoint: BC18
Covers: C10, C11, C12, C14, C16, C18, C20
Supersedes: none
Related baseline: `protocols/baseline/multi-role-baseline-v0.1.md`
Related stress test: `results/org-payment/exp-0003-intervention-validity-stress-test-0001/summary.md`

## Purpose

This document freezes the first BC18 sensitivity analysis before execution.

EXP-0004 tests one sensitivity axis only: provider-side randomness and run-to-run variation under the same artificial organization setup. It does not change model, prompts, action menus, scenario wording, Game Master rules, event taxonomy, metrics definitions, or claim boundaries.

Allowed claim after this protocol is merged:

> The EXP-0004 provider-randomness sensitivity protocol is frozen.

Forbidden in this PR:

- EXP-0004 execution results
- model comparison
- prompt variants
- action-menu variants
- Game Master strictness variants
- scenario wording variants
- temperature or seed claims beyond recording provider defaults
- causal claims
- statistical significance claims
- human behavior claims
- real-world organization claims

## Experiment Identity

| Field | Frozen value |
|---|---|
| Experiment id | `EXP-0004` |
| Protocol id | `exp-0004-provider-randomness-sensitivity-v0.1` |
| Sensitivity axis | provider randomness / repeat-run stability |
| Baseline comparator | `EXP-0002` |
| Scenario set | `S01`-`S06` |
| Runs per scenario | 2 |
| Total planned attempted runs | 12 |
| Claim boundary | `provider_randomness_sensitivity_observation_only` |

## Frozen Conditions

EXP-0004 must keep the following fixed from EXP-0002:

| Item | Frozen value |
|---|---|
| Provider | `openai` |
| Model | `gpt-4.1-mini` |
| Model version | record returned `response_metadata.model_version` |
| Temperature | not explicitly configured; provider default |
| `top_p` | not explicitly configured; provider default |
| Max tokens | not explicitly configured |
| Structured output mode | OpenAI Responses API JSON schema mode |
| Prompt refs | same as EXP-0002 |
| Action menu ids | same as EXP-0002 |
| Scenario files | same S01-S06 files as EXP-0002 |
| Game Master | `deterministic_menu_aware_rules` |
| Parser retry rule | maximum 2 attempts per LLM action |
| Event taxonomy | `protocols/evaluation/event-taxonomy-v0.1.md` |
| Pressure-citation correction | `protocols/evaluation/pressure-citation-metric-correction-v0.1.md` |

The only intended difference from EXP-0002 is that fresh provider calls are made at a later time under unchanged configuration.

## Frozen Inputs and References

EXP-0004 must compare against:

- `results/org-payment/exp-0002-multi-role-baseline/aggregate.json`
- `results/org-payment/exp-0002-multi-role-baseline/scenario-summary.csv`
- `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md`
- `results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/summary.md`
- `results/org-payment/exp-0003-intervention-validity-stress-test-0001/summary.md`

EXP-0004 execution must produce new evidence packs; it must not rewrite EXP-0002 artifacts.

## Execution Requirements

The execution PR must:

- attempt exactly 2 runs per scenario before exclusions;
- write raw outputs under ignored `runs/`;
- commit only curated artifacts under `results/org-payment/exp-0004-provider-randomness-sensitivity-0001/`;
- record attempted, accepted, and excluded runs;
- record provider/model/observed model version;
- validate each accepted evidence pack mechanically;
- preserve proposal attempts, parser results, Game Master decisions, trace, events, metrics, reviewer notes, and reconstruction checklist;
- record representative evidence packs, at least one per scenario and one per observed full path where practical;
- compare EXP-0004 action paths and scenario summaries against EXP-0002 descriptively.

## Measures

EXP-0004 may report:

- selected full org-payment path counts by scenario;
- role-turn action counts by scenario;
- proposed event counts by scenario;
- corrected pressure-context summary by scenario;
- approval-evidence propagation summary by scenario;
- coordination-gap summary by scenario;
- validation pass/fail counts;
- parser retry/rejected proposal counts;
- path overlap with EXP-0002 by scenario;
- newly observed paths not present in EXP-0002;
- EXP-0002 paths not observed in EXP-0004.

EXP-0004 must not report p-values, confidence intervals, formal effect sizes, or statistical significance.

## Comparison Rules

EXP-0004 compares 2 fresh runs per scenario against 5 EXP-0002 runs per scenario. Because the run counts differ and are small:

- comparisons are descriptive only;
- absence of a path in EXP-0004 is not evidence that the path disappeared;
- presence of a new path is a sensitivity observation, not a general model behavior claim;
- high variation must reduce claim strength, not be hidden;
- exact repeatability must not be generalized beyond this model/prompt/provider setup.

## Non-Goals

EXP-0004 must not add:

- a second model;
- prompt variant execution;
- action-menu variant execution;
- Game Master strictness variants;
- scenario wording variants;
- temperature sweeps;
- multi-provider comparison;
- human review;
- real-world behavior claims;
- statistical claims.

Future sensitivity protocols may freeze those axes separately.

## Claim Boundary

Allowed claim for the execution PR:

> Under the frozen EXP-0004 artificial organization protocol, a small provider-randomness repeat set was generated and compared descriptively with EXP-0002 to record run-to-run stability or variation under unchanged model, prompt, menu, scenario, parser, and Game Master conditions.

Required limitations:

- artificial organization only;
- provider-randomness sensitivity only;
- 2 runs per scenario;
- no model comparison;
- no prompt comparison;
- no action-menu comparison;
- no Game Master strictness comparison;
- no scenario wording comparison;
- no statistical significance claim;
- no human behavior claim;
- no real-world organization claim;
- no compliance, legal, audit, or operational sufficiency claim;
- no causal claim.

## Required Validation for Execution PR

The EXP-0004 execution PR must run:

- `python -m unittest discover -s tests`
- `python -m compileall -q src tests scripts`
- representative EXP-0004 evidence pack validation
- selected existing EXP-0002 representative evidence pack validation
- selected Markdown local links check
- `git diff --check`
- `git ls-files runs`
- curated-artifact scan for `OPENAI_API_KEY`, `sk-`, and `raw_response`

## Checkpoint Target

After EXP-0004 execution:

- BC18 has one isolated sensitivity axis completed;
- fresh runs are mechanically valid;
- EXP-0004 is compared descriptively with EXP-0002;
- robustness or fragility is reported honestly under strict limitations;
- the project can decide whether to add another isolated sensitivity axis, proceed to second-domain planning, or pause for review.
