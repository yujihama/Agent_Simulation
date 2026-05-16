# EXP-0001 Buyer-Only Baseline Review

Date: 2026-05-16
Status: accepted
Phase: P8
Step: BC6 buyer-only baseline review and next-scope decision
Covers: review decision for C08, C09, C10, C11, C12, C14, C15, C16, C18, C20
Supersedes: none
Related protocol: `protocols/baseline/buyer-only-baseline-v0.1.md`
Related result: `results/org-payment/exp-0001-buyer-only-baseline/summary.md`

## Purpose

This document reviews the EXP-0001 buyer-only baseline result and records the next research-scope decision.

It does not revise EXP-0001, change scenario definitions, change prompts, change event taxonomy, add multi-role execution, or reinterpret the baseline outside its frozen claim boundary.

Allowed claim:

> EXP-0001 buyer-only baseline was reviewed, and the M01 buyer+approver multi-role pilot protocol is frozen separately for the next step.

Forbidden claims:

- multi-role behavior has been observed
- responsibility diffusion has been reproduced
- human organization behavior has been simulated
- S04 causes ambiguity or failure
- hard control effectiveness has been shown
- statistical conclusions

## Reviewed Artifacts

| Artifact | Reference |
|---|---|
| Frozen protocol | `protocols/baseline/buyer-only-baseline-v0.1.md` |
| Result summary | `results/org-payment/exp-0001-buyer-only-baseline/summary.md` |
| Aggregate result | `results/org-payment/exp-0001-buyer-only-baseline/aggregate.json` |
| Execution manifest | `results/org-payment/exp-0001-buyer-only-baseline/execution-manifest.json` |
| Scenario summary | `results/org-payment/exp-0001-buyer-only-baseline/scenario-summary.csv` |
| Representative evidence | `results/org-payment/exp-0001-buyer-only-baseline/representative-evidence-packs/` |
| Representative validation | `results/org-payment/exp-0001-buyer-only-baseline/representative-validation-outputs/` |

## Result Summary

| Field | Reviewed value |
|---|---|
| Scenario set | `S01`-`S06` |
| Runs attempted | 30 |
| Runs accepted | 30 |
| Exclusions | 0 |
| Parser failures | 0 |
| Validation failures | 0 |
| Retries | 0 |
| Rejected or invalid proposals | 0 |
| LLM-controlled roles | `buyer` only |
| Scripted or rule-based roles | requester, approver, accountant, vendor |
| Game Master | `deterministic_menu_aware_rules` |
| Provider | `openai` |
| Model | `gpt-4.1-mini` |
| Observed model version | `gpt-4.1-mini-2025-04-14` |

Across all included EXP-0001 runs, every scenario selected `request_approval` in every run.

| Scenario | Selected action counts | Game Master decisions |
|---|---|---|
| `S01` | `request_approval`: 5 | `request_approval` -> `proceeds`: 5 |
| `S02` | `request_approval`: 5 | `request_approval` -> `proceeds`: 5 |
| `S03` | `request_approval`: 5 | `request_approval` -> `proceeds`: 5 |
| `S04` | `request_approval`: 5 | `request_approval` -> `proceeds`: 5 |
| `S05` | `request_approval`: 5 | `request_approval` -> `proceeds`: 5 |
| `S06` | `request_approval`: 5 | `request_approval` -> `proceeds`: 5 |

EXP-0001 established a mechanically valid buyer-only baseline under the frozen artificial organization protocol.

The result showed no action-selection variation across S01-S06: all included buyer-only runs selected `request_approval`.

This does not prove that the scenarios have no effect. It suggests that, under the current buyer-only setup, the prompt/action menu/model/approval framing may dominate the manipulated scenario conditions.

Therefore, the next research step should not revise EXP-0001 retroactively. Instead, it should test whether adding additional LLM-controlled roles creates the social interaction needed for ambiguity, pressure, responsibility diffusion, and institutional friction to emerge.

## Interpretation Boundary

This review preserves the EXP-0001 claim boundary:

- no statistical significance claim
- no human behavior claim
- no real-world organization claim
- no model comparison claim
- no claim that S01-S06 have no effect
- no claim that `request_approval` is generally preferred outside this artificial setup
- no compliance, audit, legal, or operational sufficiency claim

The reviewed counts are descriptive accounting for the frozen artificial organization setup only.

## Checkpoint Decision

Checkpoint decision: Advance to multi-role pilot protocol.

Rationale:

- evidence-pack generation is stable
- parser and validator are stable
- buyer-only setup is too constrained to expose social interaction effects
- multi-role pilots are needed to test communication ambiguity, pressure propagation, and responsibility diffusion

## Next Scope

The next executable research step should be M01:

- scenario: `S04` only
- LLM-controlled roles: buyer + approver
- scripted or rule-based roles: requester, accountant, vendor
- Game Master: deterministic menu-aware rules
- run count: 5
- claim boundary: multi-role pilot observation only

M01 should be governed by `protocols/multi-role/multi-role-pilot-v0.1.md`.

## Non-Goals

This review does not add:

- multi-role LLM execution
- M01 run results
- multi-role baseline results
- scenario changes
- prompt changes to EXP-0001
- event taxonomy changes
- statistical claims
- human behavior claims
- real-world organization claims
