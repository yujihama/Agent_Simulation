# Multi-Role Scenario Sweep Pilot Protocol v0.1

Date: 2026-05-17
Status: accepted
Phase: P8
Checkpoint: BC12
Supersedes: none
Related review: `pilot-runs/org-payment/m05-full-org-payment-pilot-0001/review.md`

## Purpose

This protocol freezes the first org-payment multi-role scenario sweep pilot before execution.

The sweep extends the frozen M05 full org-payment role structure from S04 to S01-S06. It observes whether the same requester+vendor+buyer+approver+accountant setup can generate, validate, and descriptively aggregate multi-role paths under the existing scenario matrix.

This is a pilot sweep, not a multi-role baseline. It does not support statistical, causal, human behavior, real-world organization, compliance, legal, audit, operational, pressure-propagation, approval-bypass, responsibility-diffusion, or general LLM behavior claims.

## Frozen Experiment Identity

| Field | Frozen value |
|---|---|
| Sweep id | `MSP-0001` |
| Scenario set | `S01`, `S02`, `S03`, `S04`, `S05`, `S06` |
| Scenario refs | `scenarios/org-payment/s01-clear-policy-low-pressure.yaml`; `scenarios/org-payment/s02-ambiguous-policy-low-pressure.yaml`; `scenarios/org-payment/s03-ambiguous-policy-high-pressure.yaml`; `scenarios/org-payment/s04-role-overlap-high-pressure.yaml`; `scenarios/org-payment/s05-audit-intervention.yaml`; `scenarios/org-payment/s06-hard-control.yaml` |
| Runs per scenario | 3 attempted runs before exclusions |
| Total planned attempted runs | 18 |
| Run count type | small multi-role scenario sweep pilot |
| LLM-controlled roles | `requester`, `vendor`, `buyer`, `approver`, `accountant` |
| Scripted or rule-based roles | none, except runner-provided initial case envelope and deterministic Game Master |
| Game Master | `deterministic_menu_aware_rules` |
| Provider | OpenAI |
| Model | `gpt-4.1-mini` |
| Requester prompt | `prompts/org-payment/requester-free-choice-action-v0.1.md` |
| Vendor prompt | `prompts/org-payment/vendor-pressure-action-v0.1.md` |
| Buyer approval-request prompt | `prompts/org-payment/buyer-free-choice-action-v0.1.md` |
| Approver prompt | `prompts/org-payment/approver-multirole-action-v0.1.md` |
| Buyer accounting-handoff prompt | `prompts/org-payment/buyer-free-choice-action-v0.1.md` |
| Accountant prompt | `prompts/org-payment/accountant-free-choice-action-v0.1.md` |
| Role menu structure | M05 full org-payment role menus, rendered with scenario-specific context |
| Claim boundary | `multi_role_scenario_sweep_pilot_observation_only` |

The sweep must attempt exactly 3 runs per scenario before exclusions are applied. Excluded runs must be reported and must not be silently replaced unless a later protocol revision freezes a replacement policy before execution resumes.

Changing these settings requires a later protocol revision before scenario sweep execution continues.

## Execution Flow

Each scenario run follows the M05 role-turn sequence:

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

## Scenario Set

The sweep uses the existing S01-S06 scenario matrix without modification.

| Scenario | Scenario ref | Frozen use in sweep |
|---|---|---|
| `S01` | `scenarios/org-payment/s01-clear-policy-low-pressure.yaml` | clear-policy / low-pressure comparison point |
| `S02` | `scenarios/org-payment/s02-ambiguous-policy-low-pressure.yaml` | ambiguous-policy / low-pressure comparison point |
| `S03` | `scenarios/org-payment/s03-ambiguous-policy-high-pressure.yaml` | ambiguous-policy / high-pressure comparison point |
| `S04` | `scenarios/org-payment/s04-role-overlap-high-pressure.yaml` | role-overlap / high-pressure comparison point |
| `S05` | `scenarios/org-payment/s05-audit-intervention.yaml` | monitored-control comparison point |
| `S06` | `scenarios/org-payment/s06-hard-control.yaml` | hard-control comparison point |

This protocol does not revise scenario definitions, scenario contrasts, event taxonomy, metrics protocol, or action proposal schema.

## Role Menus

The sweep reuses the M05 full org-payment role menu structure:

- requester case-initiation menu
- vendor pressure/flexibility menu
- buyer approval-request menu
- approver response menu
- buyer accounting-handoff menu
- accountant response menu

Menu items are rendered with scenario-specific context and scenario-specific allowed source references. The execution PR may use scenario-aware menu ids derived from the M05 menu structure, but it must not change the action vocabulary, target roles, parser constraints, or Game Master meanings without a separate protocol revision.

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
- parser failure after attempt 2 excludes the run from accepted sweep counts and must be reported as an exclusion

Invalid or rejected proposals must be preserved in the role-turn `proposal_attempts/*.jsonl` artifact when available.

## Game Master Rules

The Game Master remains deterministic and menu-aware. The sweep uses the same M05 decision meanings:

- requester urgency or direct approval routing is context, not approval evidence
- vendor pressure or flexibility is context, not approval evidence
- buyer approval request routes to approver before accounting handoff
- approver response is the only role-turn that can create explicit approval or rejection evidence
- ambiguous guidance remains ambiguous and is not explicit approval
- buyer handoff must preserve the approval state and evidence gaps
- accountant action must preserve explicit approval, ambiguous guidance, inferred approval, missing evidence, and hard-control or monitored-control context

Hard-control or monitored-control scenario context may be recorded in Game Master rationale and review flags, but execution must not change scenario files or introduce unplanned control logic after seeing results.

## Evidence Pack Requirements

Every accepted run must include at minimum:

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

Existing EXP-0001, M01, M02, M03, M04, and M05 representative evidence packs must remain valid.

Raw run output must be written under ignored `runs/` paths. Curated scenario sweep artifacts may be committed only under `pilot-runs/` or `results/`.

## Event Handling

The sweep uses existing Event Taxonomy v0.1 only.

Likely relevant existing event types:

- `informal_pressure`
- `evidence_gap`
- `communication_breakdown`
- `policy_ambiguity_exploited`
- `responsibility_diffusion`
- `approval_bypass`
- `after_the_fact_justification`
- `control_block`

Generated event labels remain proposed and not human-reviewed.

No event taxonomy change is introduced by this protocol. If sweep execution requires a new event type, execution must pause for a protocol/schema revision before results are committed.

## Metrics and Reporting

The aggregate report must include:

- sweep id
- protocol ref
- scenario set
- runs per scenario
- attempted, accepted, and excluded runs by scenario
- provider, model, and observed model versions
- prompt refs
- action menu ids or menu structure refs
- action counts by scenario and role turn
- full path counts by scenario
- parser acceptance, retry, rejected proposal, and parser failure counts by scenario and role turn
- Game Master decisions by scenario, role turn, and selected action
- validation pass/fail counts by scenario
- exclusions by scenario and reason
- proposed event counts by scenario
- requester-framing summary by scenario
- pressure-citation summary by scenario
- approval-evidence propagation summary by scenario
- coordination-gap summary by scenario
- representative evidence links, at least one per scenario
- claim boundary
- limitations

No inferential statistics are permitted in this pilot sweep. The aggregate may describe observed counts under fixed artificial conditions, but it must not describe scenario differences as statistically significant or causal.

## Claim Boundary

Allowed claim:

Under the frozen multi-role scenario sweep pilot protocol, requester+vendor+buyer+approver+accountant LLM pilot runs produced recorded full org-payment paths, parser outcomes, GM decisions, validation outcomes, proposed event observations, requester-framing observations, pressure-citation observations, approval-evidence propagation observations, and coordination-gap observations across S01-S06.

Required limitations:

- artificial organization only
- scenario sweep pilot only
- not a multi-role baseline
- S01-S06 only
- 3 attempted runs per scenario before exclusions
- requester + vendor + buyer + approver + accountant LLM-controlled
- deterministic/rule-based Game Master
- generated/proposed event labels are not human-reviewed coded evidence
- no human behavior claim
- no general LLM behavior claim
- no real-world organization claim
- no compliance, legal, audit, or operational sufficiency claim
- no statistical significance claim
- no scenario-causation claim

Forbidden claims:

- scenario differences are statistically significant
- a scenario caused a path, event, or coordination gap
- requester framing caused downstream behavior
- vendor pressure caused buyer, approver, or accountant behavior
- pressure propagation has been proven
- responsibility diffusion has been reproduced
- approval bypass has been proven
- human organizations behave this way
- this is a multi-role baseline
- this proves institutional failure
- results generalize to humans, real organizations, or other LLMs

## Non-Goals

This protocol does not add:

- scenario changes
- prompt changes
- action proposal schema changes
- event taxonomy changes
- metrics protocol changes
- model comparison
- human review
- multi-role baseline results
- statistical claims
- human behavior claims
- real-world organization claims

## Required Validation for Execution PR

The execution PR must run:

- `python -m unittest discover -s tests`
- `python -m compileall -q src tests scripts`
- representative scenario sweep evidence pack validation for each S01-S06 scenario
- existing EXP-0001 representative evidence pack validation
- existing M01 representative evidence pack validation
- existing M02 representative evidence pack validation
- existing M03 representative evidence pack validation
- existing M04 representative evidence pack validation
- existing M05 representative evidence pack validation
- `git diff --check`
- `git ls-files runs` returns no tracked raw run outputs
- curated artifact scan for `OPENAI_API_KEY`, `sk-`, and `raw_response`

## Checkpoint Target

After execution:

- S01-S06 multi-role pilot runs are generated under the frozen role structure
- 18 attempted runs are accounted for
- accepted/excluded runs are reported by scenario
- action paths, GM decisions, proposed events, and coordination-gap observations are summarized by scenario
- representative evidence packs validate mechanically
- claim boundary remains limited to scenario sweep pilot observation only

The next checkpoint should review the sweep and decide whether to freeze a multi-role baseline protocol, revise the role/menu surface, or add a human review checkpoint before baseline execution.
