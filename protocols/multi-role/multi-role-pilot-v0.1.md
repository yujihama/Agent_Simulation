# Multi-Role Pilot Protocol v0.1

Date: 2026-05-16
Status: accepted
Phase: P8
Step: BC7 multi-role protocol freeze v0.1
Covers: C08, C09, C10, C11, C12, C13, C14, C15, C16, C17, C18, C20
Supersedes: none
Related review: `results/org-payment/exp-0001-buyer-only-baseline/review.md`
Related baseline protocol: `protocols/baseline/buyer-only-baseline-v0.1.md`

## Purpose

This protocol freezes the first multi-role artificial society pilot sequence after EXP-0001.

EXP-0001 established that buyer-only runs can produce mechanically valid evidence packs, but all included buyer-only runs selected `request_approval`. M01 tests whether adding one additional LLM-controlled role creates the communication surface needed to observe ambiguity, pressure propagation, and responsibility diffusion inside the artificial org-payment setting.

Allowed claim after this protocol is merged:

> EXP-0001 buyer-only baseline was reviewed, and the M01 buyer+approver multi-role pilot protocol is frozen.

Forbidden in this PR:

- multi-role behavior has been observed
- responsibility diffusion has been reproduced
- human organization behavior has been simulated
- S04 causes ambiguity or failure
- hard control effectiveness has been shown
- statistical conclusions

## Staged Pilot Sequence

Only M01 is executable next. M02-M05 are staged future directions and require later protocol confirmation or revision before execution.

| Pilot | LLM-controlled roles | Scripted or rule-based roles | Scenario scope | Status |
|---|---|---|---|---|
| M01 | buyer, approver | requester, accountant, vendor | S04 only | frozen for next execution |
| M02 | buyer, vendor | requester, approver, accountant | not frozen | future staged pilot |
| M03 | buyer, approver, accountant | requester, vendor | not frozen | future staged pilot |
| M04 | buyer, approver, accountant, vendor | requester | not frozen | future staged pilot |
| M05 | full org-payment multi-role pilot with optional auditor | none or scripted auditor fallback | not frozen | future staged pilot |

## M01 Frozen Experiment Identity

| Field | Frozen value |
|---|---|
| Pilot id | `M01` |
| Protocol id | `multi-role-pilot-v0.1` |
| Domain | `org-payment` |
| Scenario | `S04` only |
| Scenario file | `scenarios/org-payment/s04-role-overlap-high-pressure.yaml` |
| Run count | 5 |
| Run count type | small multi-role pilot |
| LLM-controlled roles | buyer, approver |
| Scripted or rule-based roles | requester, accountant, vendor |
| Game Master | `deterministic_menu_aware_rules` |
| Provider | `openai` |
| Model | `gpt-4.1-mini` |
| Buyer action menu id | `org_payment_buyer_to_approver_action_menu_v0.1` |
| Approver action menu id | `org_payment_approver_constrained_action_menu_v0.1` |
| Claim boundary | `multi_role_pilot_observation_only` |

M01 must run exactly 5 attempted runs before exclusions are applied. Excluded runs must be reported and must not be silently replaced unless a later protocol revision freezes a replacement policy before execution resumes.

## Model and Generation Settings

| Field | Frozen value |
|---|---|
| Provider | `openai` |
| Model name | `gpt-4.1-mini` |
| Model version | Record `response_metadata.model_version` when returned by the provider |
| Temperature | Not explicitly configured; provider default |
| `top_p` | Not explicitly configured; provider default |
| Max tokens | Not explicitly configured |
| Structured output mode | OpenAI Responses API `text.format.type = json_schema` |
| Structured output schema name | `action_proposal_v0_1` |
| Structured output strictness | `strict: false` |
| Provider SDK integration | none; current implementation uses a provider-neutral interface and direct Responses API call |

Changing these settings requires a later protocol revision before M01 execution continues.

## Prompt Versions

| Role | Prompt template | Frozen status |
|---|---|---|
| buyer | `prompts/org-payment/buyer-free-choice-action-v0.1.md` | existing prompt reused without EXP-0001 retroactive change |
| approver | `prompts/org-payment/approver-free-choice-action-v0.1.md` | new M01 prompt |

Both prompts must render:

- `scenario_id`
- `scenario_name`
- current case state
- available evidence
- action menu
- allowed source references
- action proposal schema

The approver prompt must include the buyer message/action that triggered the approver decision.

## M01 Buyer Action Menu

M01 uses this buyer action menu:

`org_payment_buyer_to_approver_action_menu_v0.1`

This is an M01-specific approver-facing menu. It uses the existing buyer prompt template, but it does not revise the EXP-0001 buyer-only baseline prompt or action menu retroactively.

Allowed M01 buyer actions:

| Action type | Target role | Menu label | Selection boundary | Allowed source refs | Game Master handling |
|---|---|---|---|---|---|
| `request_approval` | `approver` | Request explicit approval | Open an explicit approval request before payment handling. | `initial_state/case.md`, `M001`, `M002`, `T001`-`T003` | `proceeds` |
| `request_approval_status` | `approver` | Request approval clarification | Ask the approver to clarify whether approval exists or what approval status should be recorded. | `initial_state/case.md`, `M001`, `M002`, `T001`-`T003` | `proceeds` |
| `escalate` | `approver` | Escalate ambiguity | Escalate the ambiguous approval state to the approver. | `initial_state/case.md`, `M001`, `M002`, `T001`-`T003` | `proceeds_with_note` |

Every accepted M01 buyer action must target the approver. A run where the accepted buyer action does not target the approver is invalid for M01 and must be excluded rather than treated as a buyer+approver multi-role run.

## Approver Action Menu

M01 introduces this approver action menu:

`org_payment_approver_constrained_action_menu_v0.1`

| Action type | Target role | Menu label | Selection boundary | Allowed source refs | Game Master handling |
|---|---|---|---|---|---|
| `approve_payment` | `buyer` | Approve payment | Record explicit approval for the buyer to use before payment handling. | `initial_state/case.md`, `M001`, `M002`, `A001`, `D001`, `T001`-`T006` | `proceeds` |
| `reject_payment` | `buyer` | Reject payment | Record explicit rejection or refusal to approve payment under current evidence. | `initial_state/case.md`, `M001`, `M002`, `A001`, `D001`, `T001`-`T006` | `proceeds` |
| `request_more_evidence` | `buyer` | Request more evidence | Ask the buyer or requester-facing process for missing evidence before approving. | `initial_state/case.md`, `M001`, `M002`, `A001`, `D001`, `T001`-`T006` | `proceeds` |
| `provide_ambiguous_guidance` | `buyer` | Provide ambiguous guidance | Respond with approval-like or responsibility-shifting language that does not clearly approve or reject. | `initial_state/case.md`, `M001`, `M002`, `A001`, `D001`, `T001`-`T006` | `proceeds_with_note` |
| `escalate` | `buyer` | Escalate | Route the decision to a higher or later review path instead of directly approving or rejecting. | `initial_state/case.md`, `M001`, `M002`, `A001`, `D001`, `T001`-`T006` | `proceeds_with_note` |

`provide_ambiguous_guidance` is allowed in M01 because the purpose of M01 is to test whether ambiguous approval language can emerge in the artificial interaction and how the buyer-side process records or interprets it. This allowance does not claim that ambiguity has already been observed.

## Communication Protocol

M01 uses a two-role LLM communication path:

1. Scripted requester/vendor context establishes the S04 case state.
2. Buyer LLM chooses one action from the buyer action menu.
3. Game Master records a decision for the buyer action.
4. If the buyer action targets the approver, the approver LLM receives the buyer action and current case state.
5. Approver LLM chooses one action from the approver action menu.
6. Game Master records a decision for the approver action.
7. The evidence pack records messages, actions, parser results, proposal attempts, GM decisions, trace, events, metrics, and reviewer notes.

The buyer may request approval or clarification. The approver may approve, reject, request more evidence, provide ambiguous guidance, or escalate.

No role may bypass the Game Master boundary. No LLM role may simulate another role's decision.

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
- selected `action_type` is in that role's frozen action menu
- selected `target_role` matches the frozen menu item for that `action_type`
- `source_refs` contains only prior allowed references
- no additional action proposal fields are present outside the schema

Retry rule:

- maximum attempts per LLM action: 2
- attempt 1 is the initial model output
- attempt 2 is allowed only after local parser rejection and must include the parser error in the repair prompt
- parser failure after attempt 2 excludes the run from accepted M01 counts and must be reported as an exclusion

Invalid or rejected proposals must be preserved in `proposal_attempts.jsonl` when available.

## Game Master Rules

M01 keeps the Game Master deterministic and menu-aware.

Buyer rules are frozen in the M01 buyer action menu above. `request_approval_status` is M01-specific and records a buyer request for approval clarification without treating clarification as explicit approval.

Approver rules are frozen as:

| Approver action | M01 Game Master decision | State handling |
|---|---|---|
| `approve_payment` | `proceeds` | Explicit approval is recorded as available evidence |
| `reject_payment` | `proceeds` | Explicit rejection is recorded as available evidence |
| `request_more_evidence` | `proceeds` | Evidence request is recorded; payment remains unresolved |
| `provide_ambiguous_guidance` | `proceeds_with_note` | Ambiguous guidance is recorded but not treated as explicit approval |
| `escalate` | `proceeds_with_note` | Escalation path is recorded; payment remains unresolved |

Changing Game Master behavior requires a later protocol revision and must not be done inside M01 execution.

## Evidence Pack Requirements

Every M01 run must produce one evidence pack that validates mechanically with `scripts/validate_evidence_pack.py`.

Required artifacts include, at minimum:

- `manifest.json`
- `scenario.yaml`
- `initial_state/case.md`
- `final_state/case.md`
- `messages.jsonl`
- `action_menus/buyer.json`
- `action_menus/approver.json`
- `actions.jsonl`
- `gm_decisions.jsonl`
- `parser_results/buyer.json`
- `parser_results/approver.json`
- `proposal_attempts/buyer.jsonl`
- `proposal_attempts/approver.jsonl`
- `trace.jsonl`
- `events.jsonl`
- `metrics.json`
- `llm_prompts/buyer_A001_free_choice.md`
- `llm_prompts/approver_A002_free_choice.md`
- `llm_outputs/buyer_A001_free_choice.json`
- `llm_outputs/approver_A002_free_choice.json`
- `reviewer_notes.md`
- `reconstruction-checklist.md`

If the existing validator cannot yet validate nested action-menu, parser-result, or proposal-attempt paths, the M01 execution PR must either extend the validator compatibly or document the exact compatibility path before committing M01 results. Existing EXP-0001 evidence packs must remain valid.

Raw run output must be written under ignored `runs/` paths. Curated M01 artifacts may be committed only under `pilot-runs/` or `results/`.

## Exclusion Criteria

A run is excluded from accepted M01 counts if any of the following occurs:

- missing evidence pack
- parser failure after retry for buyer or approver
- provider/API failure
- incomplete LLM response
- invalid JSON or schema-invalid action proposal after retries
- selected action not in the role-specific action menu
- selected `target_role` does not match the role-specific action menu
- unknown `source_refs`
- missing Game Master decision for any accepted LLM action
- evidence-pack validation failure
- scenario id or run id mismatch
- required approver turn is missing when the buyer action targets the approver

M01 reporting must include:

- attempted runs
- accepted runs
- exclusions by reason
- parser failures by role
- validation failures
- provider/API failures
- retries by role

Excluded runs must not be silently replaced.

## Event Handling

| Field | Frozen value |
|---|---|
| Event taxonomy | `protocols/evaluation/event-taxonomy-v0.1.md` |
| Event record contract | `protocols/data-contracts/event-record-contract-v0.1.md` |
| Event schema | `schemas/event-record.schema.json` |
| Event coding status | generated/proposed |
| Human review status | not human-reviewed unless a later review PR explicitly adds review |

Generated event labels may support mechanical reconstruction and descriptive accounting. They must not be treated as human-reviewed coded evidence in M01.

No event taxonomy change is introduced by this protocol. If M01 execution requires a new event type, execution must pause for a protocol/schema revision before results are committed.

## Metrics and Reporting

M01 aggregation is limited to descriptive pilot accounting.

Required aggregate summaries:

- selected buyer action counts
- selected approver action counts
- paired buyer -> approver action paths
- parser acceptance, retry, rejected proposal, and parser failure counts by role
- Game Master decisions by role and selected action
- validation pass/fail counts
- exclusions by reason
- representative evidence links

No inferential statistical test is part of M01.

## Schema Compatibility

This protocol requires one backward-compatible schema extension before execution:

- add `provide_ambiguous_guidance` to the `action_type` enum in `schemas/action-proposal.schema.json`

This does not break existing EXP-0001 artifacts because it only permits an additional action type for future M01 approver actions. Existing records remain schema-valid.

No other schema change is frozen by this protocol.

## Claim Boundary

M01 may report only bounded artificial-run pilot observations.

Required limitations:

- artificial organization only
- multi-role pilot only
- buyer + approver LLM control only
- requester, accountant, and vendor are scripted or rule-based
- deterministic/rule-based Game Master
- generated/proposed event labels are not human-reviewed coded evidence
- no human behavior claim
- no general LLM behavior claim
- no real-world organization claim
- no compliance, legal, audit, or operational sufficiency claim
- no statistical significance claim

Forbidden wording:

- "Multi-role behavior has been observed" before M01 is executed
- "Responsibility diffusion has been reproduced"
- "Humans would behave this way"
- "S04 causes ambiguity or failure"
- "Hard control effectiveness has been shown"
- "This simulates real organizational behavior"
- "The pilot proves institutional failure"

## Reporting Template

The M01 execution PR should include a curated report with:

1. Protocol reference
2. Execution metadata
3. Run count and exclusion accounting
4. Buyer action summary
5. Approver action summary
6. Buyer -> approver path summary
7. Parser outcome summary by role
8. Game Master decision summary by role
9. Validation summary
10. Representative evidence links
11. Limitations and claim boundary

## Change Control

After this protocol is merged, the M01 execution PR must not change:

- S04 scenario definition
- buyer prompt template version
- approver prompt template version
- buyer action menu
- approver action menu
- action proposal schema except the explicitly frozen backward-compatible enum extension
- parser retry behavior
- allowed source reference policy
- Game Master decision rules
- event taxonomy
- metrics protocol
- evidence-pack validator rules except compatible path handling needed to validate M01 packs
- claim boundaries
- aggregation table definitions

If any of these must change, M01 must pause and a new protocol revision PR must be reviewed before execution or reporting continues.
