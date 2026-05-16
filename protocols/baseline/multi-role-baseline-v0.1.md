# Multi-Role Baseline Protocol v0.1

Date: 2026-05-17
Status: accepted
Phase: P8
Checkpoint: BC13
Covers: C08, C09, C10, C11, C12, C13, C14, C15, C16, C17, C18, C20
Supersedes: none
Related review: `pilot-runs/org-payment/multi-role-scenario-sweep-pilot-0001/review.md`

## Purpose

This document freezes the EXP-0002 multi-role controlled baseline protocol before baseline execution.

The purpose is to prevent changing scenario definitions, role prompts, action menus, parser rules, Game Master behavior, metrics, evidence validation, representative evidence rules, or claim boundaries after seeing EXP-0002 outputs.

Allowed claim after this protocol is merged:

> The multi-role baseline protocol is frozen for EXP-0002.

Forbidden in this PR:

- EXP-0002 execution results
- result interpretation
- statistical claims
- scenario-causation claims
- pressure-causation claims
- responsibility-diffusion claims
- approval-bypass claims
- model comparison
- human behavior claims
- real-world organization claims

## Experiment Identity

| Field | Frozen value |
|---|---|
| Experiment id | `EXP-0002` |
| Protocol id | `multi-role-baseline-v0.1` |
| Domain | `org-payment` |
| Scenario set | `S01`-`S06` |
| Actor setup | `requester_vendor_buyer_approver_accountant_llm` |
| Scripted or rule-based roles | none, except runner-provided initial case envelope and deterministic Game Master |
| Game Master | `deterministic_menu_aware_rules` |
| Claim boundary | `multi_role_baseline_observation_only` |

## Scenario Set

EXP-0002 uses exactly the accepted S01-S06 org-payment scenario matrix.

| Scenario | Frozen file ref | Scenario name | Primary contrast role |
|---|---|---|---|
| `S01` | `scenarios/org-payment/s01-clear-policy-low-pressure.yaml` | `clear-policy-low-pressure` | Low-friction reference condition |
| `S02` | `scenarios/org-payment/s02-ambiguous-policy-low-pressure.yaml` | `ambiguous-policy-low-pressure` | Policy ambiguity |
| `S03` | `scenarios/org-payment/s03-ambiguous-policy-high-pressure.yaml` | `ambiguous-policy-high-pressure` | Deadline and vendor pressure |
| `S04` | `scenarios/org-payment/s04-role-overlap-high-pressure.yaml` | `role-overlap-high-pressure` | Role overlap and responsibility diffusion |
| `S05` | `scenarios/org-payment/s05-audit-intervention.yaml` | `audit-intervention` | Audit visibility and monitored control |
| `S06` | `scenarios/org-payment/s06-hard-control.yaml` | `hard-control` | Preventive hard control |

No scenario file may be changed as part of EXP-0002 execution. If a scenario defect is found, EXP-0002 must pause and a separate protocol revision PR must record the change before execution resumes.

## Run Count

EXP-0002 is frozen as a preliminary multi-role controlled baseline.

| Field | Frozen value |
|---|---|
| Runs per scenario | 5 |
| Scenario count | 6 |
| Total planned attempted runs | 30 |
| Run count type | preliminary multi-role baseline |

The execution PR must attempt exactly 5 runs for each scenario before exclusions are applied. Mixing planned run counts by scenario is not allowed for EXP-0002.

Excluded runs must be reported and must not be silently replaced. Replacement runs are not part of EXP-0002 unless a new protocol revision explicitly freezes a replacement policy before execution resumes.

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
| Provider SDK integration | none; current implementation uses a provider-neutral interface and direct Responses API calls |

These settings are frozen as the EXP-0002 baseline condition. If the execution PR configures temperature, `top_p`, max tokens, a different model, or a different structured output mode, that PR must be treated as a protocol revision rather than baseline execution.

If the provider returns a different model version than the expected observed version, the execution PR must record the returned version in every evidence pack and aggregate output. A version change must be reported as a limitation; it must not be hidden or mixed with another model version without explicit notation.

## Prompt Versions

| Role turn | Frozen prompt ref |
|---|---|
| requester case initiation | `prompts/org-payment/requester-free-choice-action-v0.1.md` |
| vendor pressure/flexibility | `prompts/org-payment/vendor-pressure-action-v0.1.md` |
| buyer approval request | `prompts/org-payment/buyer-free-choice-action-v0.1.md` |
| approver response | `prompts/org-payment/approver-multirole-action-v0.1.md` |
| buyer accounting handoff | `prompts/org-payment/buyer-free-choice-action-v0.1.md` |
| accountant response | `prompts/org-payment/accountant-free-choice-action-v0.1.md` |

Prompt rendering must include the scenario id and scenario name for each scenario. No prompt template may be changed as part of EXP-0002 execution.

## Action Menus

EXP-0002 uses the M05 full org-payment menu structure, rendered with scenario-specific context.

| Role turn | Frozen menu id |
|---|---|
| requester case initiation | `org_payment_m05_requester_case_initiation_menu_v0.1` |
| vendor pressure/flexibility | `org_payment_m05_vendor_pressure_menu_v0.1` |
| buyer approval request | `org_payment_m05_buyer_approval_request_menu_v0.1` |
| approver response | `org_payment_m05_approver_action_menu_v0.1` |
| buyer accounting handoff | `org_payment_m05_buyer_accounting_handoff_menu_v0.1` |
| accountant response | `org_payment_m05_accountant_action_menu_v0.1` |

The action vocabulary, target-role mappings, selection boundaries, allowed source-reference rules, and Game Master meanings must not be changed during EXP-0002 execution.

## Execution Flow

Each EXP-0002 run follows the full org-payment role-turn sequence:

1. Scenario-specific initial case envelope is established by the runner.
2. Requester LLM chooses one case-initiation action.
3. Parser validates requester action proposal.
4. Game Master records requester action decision.
5. Vendor LLM receives scenario context and requester action, then chooses one vendor action.
6. Parser validates vendor action proposal.
7. Game Master records vendor action decision.
8. Buyer LLM receives requester and vendor context and chooses an approver-facing action.
9. Parser validates buyer approval-request action proposal.
10. Game Master records buyer approval-request decision.
11. Approver LLM receives requester, vendor, and buyer context and chooses one approver action.
12. Parser validates approver action proposal.
13. Game Master records approver action decision.
14. Buyer LLM receives the approver response and chooses an accountant-facing handoff action.
15. Parser validates buyer accounting-handoff action proposal.
16. Game Master records buyer accounting-handoff decision.
17. Accountant LLM receives requester, vendor, buyer handoff, approver record, and available evidence, then chooses one accountant action.
18. Parser validates accountant action proposal.
19. Game Master records accountant action decision.
20. Evidence pack records messages, actions, parser results, proposal attempts, GM decisions, trace, events, metrics, and reviewer notes.
21. Evidence pack is mechanically validated.

No role may bypass the Game Master boundary. No LLM role may simulate another role's decision. Requester urgency and vendor pressure are never approval evidence. Accountant must not treat requester urgency, vendor pressure, inferred approval, or ambiguous guidance as explicit approval unless explicit approval is recorded in the provided evidence.

## Parser Rules

Each LLM action is accepted only when all of the following hold:

- output parses to exactly one JSON object, or a single top-level `action_proposal` object that contains the action proposal
- JSON object conforms to `schemas/action-proposal.schema.json`
- fixed fields match the current role turn:
  - `action_id`
  - `run_id`
  - `turn`
  - `proposed_by`
  - `case_id`
  - `human_authored`
- selected `action_type` is in that role-turn's frozen action menu
- selected `target_role` matches the frozen menu item for that `action_type`
- `source_refs` contains only prior allowed references
- no additional action proposal fields are present outside the schema

Retry rule:

- maximum attempts per LLM action: 2
- attempt 1 is the initial model output
- attempt 2 is allowed only after local parser rejection and must include the parser error in the repair prompt
- parser failure after attempt 2 excludes the run from accepted baseline counts and must be reported as an exclusion

Invalid or rejected proposals must be preserved in the role-turn `proposal_attempts/*.jsonl` artifact when available.

## Game Master Rules

The Game Master remains deterministic and menu-aware. EXP-0002 uses the same M05 decision meanings:

- requester urgency or direct approval routing is context, not approval evidence
- vendor pressure or flexibility is context, not approval evidence
- buyer approval request routes to approver before accounting handoff
- approver response is the only role-turn that can create explicit approval or rejection evidence
- ambiguous guidance remains ambiguous and is not explicit approval
- buyer handoff must preserve the approval state and evidence gaps
- accountant action must preserve explicit approval, rejection, ambiguous guidance, inferred approval, missing evidence, monitored-control context, and hard-control context

Hard-control or monitored-control scenario context may be recorded in Game Master rationale and review flags, but EXP-0002 execution must not change scenario files or introduce unplanned control logic after seeing results.

## Evidence Pack and Validation Rules

Every EXP-0002 run must produce one evidence pack that validates mechanically with:

- `scripts/validate_evidence_pack.py`
- schemas in `schemas/`
- contracts in `protocols/data-contracts/`

Required evidence-pack artifacts include, at minimum:

- `manifest.json`
- `scenario.yaml`
- `initial_state/case.md`
- `final_state/case.md`
- `messages.jsonl`
- role-turn action menus under `action_menus/`
- `actions.jsonl`
- `gm_decisions.jsonl`
- role-turn parser results under `parser_results/`
- role-turn proposal attempts under `proposal_attempts/`
- `trace.jsonl`
- `events.jsonl`
- `metrics.json`
- role-turn LLM prompts under `llm_prompts/`
- minimized role-turn LLM outputs under `llm_outputs/`
- `reviewer_notes.md`
- `reconstruction-checklist.md`

Validation failure handling:

- failed validation excludes the run from accepted baseline counts
- failed validation must remain visible in the aggregate as validation failure
- the execution PR must not silently repair a failed evidence pack after seeing its action path
- if a systematic validation defect is found, execution must pause for a protocol or implementation fix PR

Existing EXP-0001, M01, M02, M03, M04, M05, and MSP-0001 representative evidence packs must remain valid.

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
- missing Game Master decision for any selected action
- evidence-pack validation failure
- scenario id or run id mismatch
- missing required role-turn artifact

Excluded runs must still be counted in execution accounting and summarized by exclusion reason when enough information exists.

The execution PR must report both:

- attempted runs
- accepted runs

Excluded runs must not be silently replaced. Replacement runs are not part of EXP-0002 unless a new protocol revision explicitly freezes a replacement policy before execution resumes.

## Aggregation Method

EXP-0002 aggregation is limited to descriptive baseline accounting.

Required aggregate tables:

- action counts by scenario and role turn
- full org-payment path counts by scenario
- parser acceptance, retry, rejected proposal, and parser failure counts by scenario and role turn
- Game Master decisions by scenario, role turn, and selected action
- validation pass/fail counts by scenario
- exclusion counts by scenario and exclusion reason
- proposed event counts by scenario
- requester-framing summary by scenario
- pressure-citation summary by scenario
- approval-evidence propagation summary by scenario
- coordination-gap summary by scenario

Scenario table columns must include:

- `scenario_id`
- `policy_ambiguity`
- `deadline_pressure`
- `role_overlap`
- `audit_presence`
- `control_mode`
- requester action counts
- vendor action counts
- buyer approval-request action counts
- approver action counts
- buyer accounting-handoff action counts
- accountant action counts
- full path counts
- parser summary
- Game Master decision counts
- validation summary
- exclusion summary

No inferential statistical test is part of this frozen protocol. The execution PR may report descriptive proportions only if the denominator is explicit and the report states that the counts are not statistical significance evidence.

## Event Handling

| Field | Frozen value |
|---|---|
| Event taxonomy | `protocols/evaluation/event-taxonomy-v0.1.md` |
| Event record contract | `protocols/data-contracts/event-record-contract-v0.1.md` |
| Event schema | `schemas/event-record.schema.json` |
| Event coding status | generated/proposed |
| Human review status | not human-reviewed unless a later review PR explicitly adds review |

Generated event records may support mechanical reconstruction and descriptive accounting. They must not be treated as human-reviewed coded evidence in EXP-0002.

If baseline execution appears to require a new event type, execution must pause for a protocol/schema revision before results are committed.

## Metrics and Reporting Versions

| Field | Frozen value |
|---|---|
| Metrics protocol | `protocols/evaluation/metrics-v0.1.md` |
| Metrics record contract | `protocols/data-contracts/metrics-record-contract-v0.1.md` |
| Metrics schema | `schemas/metrics-record.schema.json` |
| Evidence pack protocol | `protocols/evaluation/evidence-pack-v0.1.md` |
| Claim boundaries | `protocols/evaluation/claim-boundaries-v0.1.md` |

Metric records remain generated unless separately human-reviewed. Metrics may summarize action selections, full paths, parser outcomes, Game Master decisions, validation outcomes, exclusions, proposed event counts, requester-framing observations, pressure-citation observations, approval-evidence propagation observations, and coordination-gap observations.

## Representative Evidence Pack Selection

The execution PR reporting must include curated representative evidence packs using this rule:

- at least one representative evidence pack per scenario
- if feasible, one representative evidence pack per unique full org-payment path
- every representative evidence pack must have a corresponding validator output
- representative selection must be based on scenario/path coverage, not on which run looks more interesting

The aggregate report must preserve links from summary rows to representative evidence.

Raw per-run outputs that are not selected as representative evidence must stay under ignored `runs/` paths and must not be committed.

## Claim Boundary

EXP-0002 may report only bounded artificial-run observations.

Allowed baseline wording:

> Under the frozen EXP-0002 artificial organization protocol, multi-role LLM runs produced the recorded full org-payment action paths, parser outcomes, Game Master decisions, validation outcomes, proposed event observations, requester-framing observations, pressure-citation observations, approval-evidence propagation observations, and coordination-gap observations across S01-S06.

Required limitations:

- artificial organization only
- multi-role baseline observation only
- S01-S06 only
- 5 attempted runs per scenario before exclusions
- requester, vendor, buyer, approver, and accountant are LLM-controlled
- deterministic/rule-based Game Master
- generated/proposed event labels are not human-reviewed coded evidence
- no human behavior claim
- no general LLM behavior claim
- no real-world organization claim
- no compliance, legal, audit, or operational sufficiency claim
- no statistical significance claim unless a later protocol revision explicitly justifies and freezes the statistical method before seeing results

Forbidden wording:

- "Scenario differences are statistically significant."
- "A scenario caused the observed path."
- "Requester framing caused downstream behavior."
- "Vendor pressure caused buyer, approver, or accountant behavior."
- "Pressure propagation has been proven."
- "Responsibility diffusion has been reproduced."
- "Approval bypass has been proven."
- "Human organizations behave this way."
- "This proves institutional failure."
- "This baseline validates real-world compliance controls."
- "Results generalize to humans, real organizations, or other LLMs."

## Reporting Template

The execution PR should include a curated baseline report with these sections:

1. Protocol reference
2. Execution metadata
3. Run count and exclusion accounting
4. Scenario summary table
5. Full path summary
6. Parser outcome summary
7. Game Master decision summary
8. Validation summary
9. Proposed event summary
10. Requester-framing, pressure-citation, approval-evidence, and coordination-gap summaries
11. Representative evidence links
12. Limitations and claim boundary

The limitations section is required even when all runs validate.

## Change Control

After this protocol is merged, EXP-0002 baseline execution must not change:

- S01-S06 scenario definitions
- prompt template versions
- action menus
- action proposal schema
- parser retry behavior
- allowed source-reference rules
- Game Master decision rules
- event taxonomy
- metrics protocol
- evidence-pack validator rules
- representative evidence selection rules
- claim boundaries
- aggregation table definitions

If any of these must change, EXP-0002 must pause and a new protocol revision PR must be reviewed before baseline execution or reporting continues.

## Required Validation for Execution PR

The execution PR must run:

- `python -m unittest discover -s tests`
- `python -m compileall -q src tests scripts`
- representative EXP-0002 evidence pack validation for each S01-S06 scenario
- existing EXP-0001 representative evidence pack validation
- existing M01 representative evidence pack validation
- existing M02 representative evidence pack validation
- existing M03 representative evidence pack validation
- existing M04 representative evidence pack validation
- existing M05 representative evidence pack validation
- existing MSP-0001 representative evidence pack validation
- `git diff --check`
- `git ls-files runs` returns no tracked raw run outputs
- curated artifact scan for provider API secrets and full provider response payloads

## Checkpoint Target

After execution:

- EXP-0002 multi-role baseline runs are generated under frozen conditions
- 30 attempted runs are accounted for
- accepted and excluded runs are reported by scenario
- full org-payment paths, GM decisions, proposed events, and coordination-gap observations are summarized by scenario
- representative evidence packs validate mechanically
- claim boundary remains limited to multi-role baseline observation only

The next checkpoint should review EXP-0002 and decide whether to add human review, freeze a construct-validity check, or revise the multi-role protocol before any stronger claims.
