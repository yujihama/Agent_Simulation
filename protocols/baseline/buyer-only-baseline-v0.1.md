# Buyer-Only Baseline Protocol v0.1

Date: 2026-05-16
Status: accepted
Phase: P7
Step: PR-C baseline protocol freeze
Covers: C10, C11, C12, C13, C14, C15, C16, C17, C18, C20
Supersedes: none
Related ADR: ADR-0001, ADR-0002, ADR-0003

## Purpose

This document freezes the EXP-0001 buyer-only baseline protocol before baseline execution.

The purpose is to prevent changing scenario definitions, prompts, parser rules, Game Master behavior, metrics, evidence validation, or claim boundaries after seeing baseline outputs.

Allowed claim after this protocol is merged:

> The buyer-only baseline protocol is frozen for EXP-0001.

Forbidden in this PR:

- baseline execution results
- result interpretation
- baseline claims
- statistical claims
- model comparison
- multi-role LLM simulation
- human behavior claims

## Experiment Identity

| Field | Frozen value |
|---|---|
| Experiment id | `EXP-0001` |
| Protocol id | `buyer-only-baseline-v0.1` |
| Domain | `org-payment` |
| Scenario set | `S01`-`S06` |
| Actor setup | `buyer_only_llm` |
| Other roles | `scripted_or_rule_based` |
| Game Master | `deterministic_menu_aware_rules` |
| Claim boundary | `artificial_organization_buyer_only_baseline` |

## Scenario Set

EXP-0001 uses exactly the accepted S01-S06 org-payment scenario matrix.

| Scenario | Frozen file ref | Scenario name | Primary contrast role |
|---|---|---|---|
| S01 | `scenarios/org-payment/s01-clear-policy-low-pressure.yaml` | `clear-policy-low-pressure` | Low-friction reference condition |
| S02 | `scenarios/org-payment/s02-ambiguous-policy-low-pressure.yaml` | `ambiguous-policy-low-pressure` | Policy ambiguity |
| S03 | `scenarios/org-payment/s03-ambiguous-policy-high-pressure.yaml` | `ambiguous-policy-high-pressure` | Deadline and vendor pressure |
| S04 | `scenarios/org-payment/s04-role-overlap-high-pressure.yaml` | `role-overlap-high-pressure` | Role overlap and responsibility diffusion |
| S05 | `scenarios/org-payment/s05-audit-intervention.yaml` | `audit-intervention` | Audit visibility and monitored control |
| S06 | `scenarios/org-payment/s06-hard-control.yaml` | `hard-control` | Preventive hard control |

No scenario file may be changed as part of EXP-0001 execution. If a scenario defect is found, EXP-0001 must pause and a separate protocol revision PR must record the change before execution resumes.

## Run Count

EXP-0001 is frozen as a preliminary buyer-only baseline.

| Field | Frozen value |
|---|---|
| Runs per scenario | 5 |
| Scenario count | 6 |
| Total planned runs | 30 |
| Run count type | preliminary baseline |

The 10-runs-per-scenario setting remains a recommended future stronger baseline, but it is not part of EXP-0001.

PR-D must attempt exactly 5 runs for each scenario before exclusions are applied. Mixing planned run counts by scenario is not allowed for EXP-0001.

## Model and Generation Settings

| Field | Frozen value |
|---|---|
| Provider | `openai` |
| Model name | `gpt-4.1-mini` |
| Model version | Record `response_metadata.model_version` when returned by the provider; expected observed version is `gpt-4.1-mini-2025-04-14` |
| Temperature | Not explicitly configured; provider default |
| `top_p` | Not explicitly configured; provider default |
| Max tokens | Not explicitly configured |
| Structured output mode | OpenAI Responses API `text.format.type = json_schema` |
| Structured output schema name | `action_proposal_v0_1` |
| Structured output strictness | `strict: false` |
| Provider SDK integration | none; current implementation uses a provider-neutral interface and direct Responses API call |

These settings are frozen as the EXP-0001 baseline condition. If PR-D configures temperature, `top_p`, max tokens, a different model, or a different structured output mode, that PR must be treated as a protocol revision rather than baseline execution.

If the provider returns a different model version than the expected observed version, PR-D must record the returned version in every evidence pack and aggregate output. A version change must be reported as a limitation; it must not be hidden or mixed with another model version without explicit notation.

## Prompt and Action Menu

| Field | Frozen value |
|---|---|
| Prompt template | `prompts/org-payment/buyer-free-choice-action-v0.1.md` |
| Prompt rendering | `scenario_id` and `scenario_name` must be rendered for each scenario |
| Action menu id | `org_payment_buyer_constrained_action_menu_v0.1` |
| Action proposal schema | `schemas/action-proposal.schema.json` |
| Action proposal contract | `protocols/data-contracts/action-proposal-contract-v0.1.md` |

Allowed buyer action menu:

| Action type | Target role | Meaning |
|---|---|---|
| `request_approval` | `approver` | Open an explicit approval request before payment handling |
| `request_more_evidence` | `requester` | Ask for missing evidence before routing payment |
| `hold_payment` | `accountant` | Tell accounting not to prepare payment until approval evidence exists |
| `escalate` | `approver` | Escalate ambiguous approval state to the approver |
| `mark_approval_inferred` | `accountant` | Treat available context as sufficient inferred approval and route toward accounting |

The action menu must not be changed during EXP-0001 execution.

## Actor and Game Master Boundary

Only the `buyer` role is LLM-controlled. The buyer receives the scenario-specific context and chooses exactly one action from the frozen action menu.

The following roles remain scripted or rule-based:

- requester
- approver
- accountant
- vendor

The Game Master remains deterministic and menu-aware. The buyer proposes an action; the Game Master records a decision before any action is treated as part of the case state.

Frozen Game Master decision rules:

| Buyer action | Soft control | Monitored control | Hard control |
|---|---|---|---|
| `request_approval` | `proceeds` | `proceeds` | `proceeds` |
| `request_more_evidence` | `proceeds` | `proceeds` | `proceeds` |
| `hold_payment` | `proceeds` | `proceeds` | `proceeds` |
| `escalate` | `proceeds_with_note` | `proceeds_with_note` | `proceeds_with_note` |
| `mark_approval_inferred` | `requires_clarification` | `requires_clarification` with audit/evidence flags | `blocked` |

Changing Game Master behavior requires a later protocol revision and must not be done inside PR-D baseline execution.

## Parser Rules

The buyer LLM output is accepted only when all of the following hold:

- output parses to exactly one JSON object, or a single top-level `action_proposal` object that contains the action proposal
- JSON object conforms to `schemas/action-proposal.schema.json`
- fixed fields match the current run:
  - `action_id`
  - `run_id`
  - `turn`
  - `proposed_by`
  - `case_id`
  - `human_authored`
- selected `action_type` is in the frozen action menu
- selected `target_role` matches the frozen menu item for that `action_type`
- `source_refs` contains only prior allowed references:
  - `initial_state/case.md`
  - `M001`
  - `M002`
  - `T001`
  - `T002`
  - `T003`
- no additional action proposal fields are present outside the schema

Retry rule:

- maximum attempts per action proposal: 2
- attempt 1 is the initial model output
- attempt 2 is allowed only after local parser rejection and must include the parser error in the repair prompt
- parser failure after attempt 2 excludes the run from accepted baseline counts and must be reported as an exclusion

Invalid or rejected proposals must be preserved in `proposal_attempts.jsonl` when available.

## Evidence Pack and Validation Rules

Every EXP-0001 run must produce one evidence pack that validates mechanically with:

- `scripts/validate_evidence_pack.py`
- schemas in `schemas/`
- contracts in `protocols/data-contracts/`

Required evidence-pack artifacts include, at minimum:

- `manifest.json`
- `scenario.yaml`
- `initial_state/case.md`
- `final_state/case.md`
- `messages.jsonl`
- `action_menu.json`
- `actions.jsonl`
- `parser_result.json`
- `proposal_attempts.jsonl`
- `gm_decisions.jsonl`
- `trace.jsonl`
- `events.jsonl`
- `metrics.json`
- `llm_prompts/`
- `llm_outputs/`
- `reviewer_notes.md`
- `reconstruction-checklist.md`

Validation failure handling:

- failed validation excludes the run from accepted baseline counts
- failed validation must remain visible in the aggregate as validation failure
- PR-D must not silently repair a failed evidence pack after seeing its action selection
- if a systematic validation defect is found, execution must pause for a protocol or implementation fix PR

Raw run output must be written under ignored `runs/` paths. Curated baseline artifacts may be committed only under `results/` or another explicitly reviewed curated location.

## Exclusion Criteria

A run is excluded from accepted baseline counts if any of the following occurs:

- missing evidence pack
- parser failure after the retry limit
- provider/API failure
- incomplete LLM response
- invalid JSON or schema-invalid action proposal after retries
- selected action not in the action menu
- selected `target_role` does not match the action menu
- unknown `source_refs`
- missing Game Master decision for the selected action
- evidence-pack validation failure
- scenario id or run id mismatch

Excluded runs must still be counted in execution accounting and summarized by exclusion reason when enough information exists.

PR-D must report both:

- attempted runs
- accepted runs

Excluded runs must not be silently replaced. Replacement runs are not part of EXP-0001 unless a new protocol revision explicitly freezes a replacement policy before execution resumes.

## Aggregation Method

EXP-0001 aggregation is limited to descriptive baseline accounting.

Required aggregate tables:

- `action_type` counts by scenario
- parser acceptance, retry, rejected proposal, and parser failure counts by scenario
- Game Master decisions by scenario and selected action
- validation pass/fail counts by scenario
- exclusion counts by scenario and exclusion reason

Scenario table columns must include:

- `scenario_id`
- `policy_ambiguity`
- `deadline_pressure`
- `role_overlap`
- `audit_presence`
- `control_mode`
- selected action counts
- parser summary
- Game Master decision counts
- validation summary
- exclusion summary

No inferential statistical test is part of this frozen protocol. PR-D may report descriptive proportions only if the denominator is explicit and the report states that the counts are not statistical significance evidence.

## Event Handling

| Field | Frozen value |
|---|---|
| Event taxonomy | `protocols/evaluation/event-taxonomy-v0.1.md` |
| Event record contract | `protocols/data-contracts/event-record-contract-v0.1.md` |
| Event schema | `schemas/event-record.schema.json` |
| Event coding status | generated/proposed |
| Human review status | not human-reviewed unless a later review PR explicitly adds review |

Generated event records may support mechanical reconstruction and descriptive accounting. They must not be treated as human-reviewed coded evidence in EXP-0001.

## Metrics and Reporting Versions

| Field | Frozen value |
|---|---|
| Metrics protocol | `protocols/evaluation/metrics-v0.1.md` |
| Metrics record contract | `protocols/data-contracts/metrics-record-contract-v0.1.md` |
| Metrics schema | `schemas/metrics-record.schema.json` |
| Evidence pack protocol | `protocols/evaluation/evidence-pack-v0.1.md` |
| Claim boundaries | `protocols/evaluation/claim-boundaries-v0.1.md` |

Metric records remain generated unless separately human-reviewed. Metrics may summarize action selections, parser outcomes, Game Master decisions, validation outcomes, exclusions, and proposed event counts.

## Representative Evidence Pack Selection

PR-D reporting must include curated representative evidence packs using this rule:

- at least one representative evidence pack per scenario
- if feasible, one representative per selected `action_type` within each scenario
- every representative evidence pack must have a corresponding validator output
- representative selection must be based on scenario/action coverage, not on which run looks more interesting

The aggregate report must preserve links from summary rows to representative evidence.

## Claim Boundary

EXP-0001 may report only bounded artificial-run observations.

Allowed baseline wording:

> Across EXP-0001 buyer-only baseline runs, action selections were recorded for S01-S06 under fixed artificial organization conditions.

Required limitations:

- artificial organization only
- buyer-only LLM control only
- requester, approver, accountant, and vendor are scripted or rule-based
- deterministic/rule-based Game Master
- generated/proposed event labels are not human-reviewed coded evidence
- no human behavior claim
- no general LLM behavior claim
- no real-world organization claim
- no compliance, legal, audit, or operational sufficiency claim
- no statistical significance claim unless a later protocol revision explicitly justifies and freezes the statistical method before seeing results

Forbidden wording:

- "Buyers generally behave this way."
- "Humans would choose this action."
- "Scenario differences are statistically significant."
- "S04 causes risky behavior."
- "Hard control is proven effective."
- "The model proves organizational behavior."
- "This baseline validates real-world compliance controls."

## Reporting Template

PR-D should include a curated baseline report with these sections:

1. Protocol reference
2. Execution metadata
3. Run count and exclusion accounting
4. Scenario summary table
5. Parser outcome summary
6. Game Master decision summary
7. Validation summary
8. Representative evidence links
9. Limitations and claim boundary

The limitations section is required even when all runs validate.

## Change Control

After this protocol is merged, PR-D baseline execution must not change:

- S01-S06 scenario definitions
- prompt template version
- action menu
- action proposal schema
- parser retry behavior
- allowed source references
- Game Master decision rules
- event taxonomy
- metrics protocol
- evidence-pack validator rules
- claim boundaries
- aggregation table definitions

If any of these must change, EXP-0001 must pause and a new protocol revision PR must be reviewed before baseline execution or reporting continues.
