# M03 Buyer+Approver+Accountant Coordination Pilot Protocol v0.1

Date: 2026-05-16
Status: accepted
Phase: P8
Checkpoint: BC10
Supersedes: none
Related review: `pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/review.md`

## Purpose

M03 tests internal coordination in the artificial org-payment setting. It observes whether approval status, ambiguous approval-related guidance, and evidence gaps are preserved or distorted as a case moves from buyer and approver records to accountant handling.

M03 does not test vendor pressure directly. It does not make causal, statistical, human behavior, real-world organization, compliance, legal, audit, or operational claims.

## Frozen Experiment Identity

| Field | Frozen value |
|---|---|
| Pilot id | `M03` |
| Scenario | `S04` only |
| Scenario ref | `scenarios/org-payment/s04-role-overlap-high-pressure.yaml` |
| Run count | 5 attempted runs before exclusions |
| Run count type | small multi-role coordination pilot |
| LLM-controlled roles | `buyer`, `approver`, `accountant` |
| Scripted or rule-based roles | `requester`, `vendor` |
| Game Master | `deterministic_menu_aware_rules` |
| Provider | OpenAI |
| Model | `gpt-4.1-mini` |
| Buyer approval-request prompt | `prompts/org-payment/buyer-free-choice-action-v0.1.md` |
| Approver prompt | `prompts/org-payment/approver-multirole-action-v0.1.md` |
| Buyer accounting-handoff prompt | `prompts/org-payment/buyer-free-choice-action-v0.1.md` |
| Accountant prompt | `prompts/org-payment/accountant-free-choice-action-v0.1.md` |
| Buyer approval-request menu id | `org_payment_m03_buyer_approval_request_menu_v0.1` |
| Approver action menu id | `org_payment_m03_approver_action_menu_v0.1` |
| Buyer accounting-handoff menu id | `org_payment_m03_buyer_accounting_handoff_menu_v0.1` |
| Accountant action menu id | `org_payment_m03_accountant_action_menu_v0.1` |
| Claim boundary | `multi_role_coordination_pilot_observation_only` |

M03 must run exactly 5 attempted runs before exclusions are applied. Excluded runs must be reported and must not be silently replaced unless a later protocol revision freezes a replacement policy before execution resumes.

Changing these settings requires a later protocol revision before M03 execution continues.

## Execution Flow

Each M03 run follows this sequence:

1. S04 initial case state is established.
2. Scripted vendor/requester context creates the invoice, business reason, urgency, and missing explicit approval state.
3. Buyer LLM chooses an approver-facing action from the frozen M03 buyer approval-request menu.
4. Parser validates the buyer approval-request action proposal.
5. Game Master records a decision for the buyer approval-request action.
6. Approver LLM receives the buyer action, current case state, and available evidence.
7. Approver LLM chooses one action from the frozen approver action menu.
8. Parser validates the approver action proposal.
9. Game Master records a decision for the approver action.
10. Buyer LLM receives the approver action/decision and chooses an accountant-facing handoff action from the frozen buyer accounting-handoff menu.
11. Parser validates the buyer accounting-handoff action proposal.
12. Game Master records a decision for the buyer accounting-handoff action.
13. Accountant LLM receives the buyer handoff, approver record, current case state, and available evidence.
14. Accountant LLM chooses one action from the frozen accountant action menu.
15. Parser validates the accountant action proposal.
16. Game Master records a decision for the accountant action.
17. Evidence pack records scripted initial state, scripted messages, buyer approval-request action, approver action, buyer accounting-handoff action, accountant action, parser results, proposal attempts, GM decisions, trace, events, metrics, and reviewer notes.
18. Evidence pack is mechanically validated.

No role may bypass the Game Master boundary. No LLM role may simulate another role's decision. Accountant must not treat pressure or ambiguous guidance as explicit approval unless the evidence supports it.

## Role Menus

### Buyer Approval-Request Menu

Menu id: `org_payment_m03_buyer_approval_request_menu_v0.1`

Purpose: Buyer asks the approver to resolve approval status before any accounting handoff.

| Action type | Target role | Menu label | Selection boundary | Allowed source refs | Game Master handling |
|---|---|---|---|---|---|
| `request_approval` | `approver` | Request explicit approval | Ask the approver to approve or reject before payment handling. | `initial_state/case.md`, `M001`, `M002`, `T001`-`T004` | `proceeds` |
| `request_approval_status` | `approver` | Request approval status | Ask the approver to clarify whether approval exists or remains unresolved. | `initial_state/case.md`, `M001`, `M002`, `T001`-`T004` | `proceeds` |
| `escalate` | `approver` | Escalate approval ambiguity | Escalate missing approval or ambiguous ownership to the approver. | `initial_state/case.md`, `M001`, `M002`, `T001`-`T004` | `proceeds_with_note` |

Every accepted M03 buyer approval-request action must target the approver.

### Approver Action Menu

Menu id: `org_payment_m03_approver_action_menu_v0.1`

Purpose: Approver may clearly approve, clearly reject, request more evidence, provide ambiguous guidance, or escalate.

| Action type | Target role | Menu label | Selection boundary | Allowed source refs | Game Master handling |
|---|---|---|---|---|---|
| `approve_payment` | `buyer` | Approve payment | Record explicit approval for the buyer to use in the accounting handoff. | `initial_state/case.md`, `M001`, `M002`, `A001`, `D001`, `T001`-`T006` | `proceeds` |
| `reject_payment` | `buyer` | Reject payment | Record explicit rejection under the current evidence. | `initial_state/case.md`, `M001`, `M002`, `A001`, `D001`, `T001`-`T006` | `proceeds` |
| `request_more_evidence` | `buyer` | Request more evidence | Ask for missing evidence before approving or rejecting. | `initial_state/case.md`, `M001`, `M002`, `A001`, `D001`, `T001`-`T006` | `proceeds` |
| `provide_ambiguous_guidance` | `buyer` | Provide ambiguous guidance | Respond with approval-related or responsibility-shifting language that does not clearly approve or reject. | `initial_state/case.md`, `M001`, `M002`, `A001`, `D001`, `T001`-`T006` | `proceeds_with_note` |
| `escalate` | `buyer` | Escalate | Route the decision to a higher or later review path instead of directly approving or rejecting. | `initial_state/case.md`, `M001`, `M002`, `A001`, `D001`, `T001`-`T006` | `proceeds_with_note` |

`provide_ambiguous_guidance` is allowed because M03 tests whether ambiguous approval-related language is preserved or distorted during the buyer-to-accountant handoff.

### Buyer Accounting-Handoff Menu

Menu id: `org_payment_m03_buyer_accounting_handoff_menu_v0.1`

Purpose: Buyer decides how to hand off the case after the approver response.

| Action type | Target role | Menu label | Selection boundary | Allowed source refs | Game Master handling |
|---|---|---|---|---|---|
| `submit_payment_request` | `accountant` | Submit payment request | Hand off the payment request to accounting with the approval state represented from available evidence. | `initial_state/case.md`, `M001`, `M002`, `M003`, `A001`, `D001`, `A002`, `D002`, `T001`-`T009` | conditional |
| `request_more_evidence` | `requester` | Request more evidence | Ask for missing evidence before handing off to accounting. | `initial_state/case.md`, `M001`, `M002`, `M003`, `A001`, `D001`, `A002`, `D002`, `T001`-`T009` | `proceeds` |
| `hold_payment` | `accountant` | Hold payment | Tell accounting that payment should remain held while evidence or approval is unresolved. | `initial_state/case.md`, `M001`, `M002`, `M003`, `A001`, `D001`, `A002`, `D002`, `T001`-`T009` | `proceeds` |
| `escalate` | `approver` | Escalate handoff ambiguity | Escalate unresolved approval or handoff ambiguity instead of sending a payment-ready request. | `initial_state/case.md`, `M001`, `M002`, `M003`, `A001`, `D001`, `A002`, `D002`, `T001`-`T009` | `proceeds_with_note` |
| `mark_approval_inferred` | `accountant` | Mark approval inferred | Treat approval as inferred from context despite missing explicit approval. | `initial_state/case.md`, `M001`, `M002`, `M003`, `A001`, `D001`, `A002`, `D002`, `T001`-`T009` | `requires_clarification` |

For `submit_payment_request`, the Game Master decision is `proceeds` only if explicit approval exists; otherwise it is `proceeds_with_note` with an evidence gap.

### Accountant Action Menu

Menu id: `org_payment_m03_accountant_action_menu_v0.1`

Purpose: Accountant decides whether to prepare payment, hold, request evidence, escalate, or route an exception review.

| Action type | Target role | Menu label | Selection boundary | Allowed source refs | Game Master handling |
|---|---|---|---|---|---|
| `prepare_payment` | `buyer` | Prepare payment | Prepare payment only when the evidence supports the approval state represented in the handoff. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `T001`-`T012` | conditional |
| `hold_payment` | `buyer` | Hold payment | Keep payment from moving forward while approval evidence is unresolved. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `T001`-`T012` | `proceeds` |
| `request_more_evidence` | `buyer` | Request more evidence | Ask the buyer for missing approval or supporting evidence. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `T001`-`T012` | `proceeds` |
| `escalate` | `approver` | Escalate | Escalate unresolved approval, ambiguous guidance, or handoff inconsistency. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `T001`-`T012` | `proceeds_with_note` |
| `authorize_exception_review` | `approver` | Authorize exception review | Route the case for exception review instead of normal payment preparation. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `T001`-`T012` | `proceeds_with_note` |

For `prepare_payment`, the Game Master decision is `proceeds` only if explicit approval exists. If explicit approval is absent or ambiguous, the Game Master records `proceeds_with_note` with an evidence gap. Accountant preparation must not erase approval evidence gaps.

## Prompt Versions

| Role turn | Prompt template | Frozen status |
|---|---|---|
| buyer approval request | `prompts/org-payment/buyer-free-choice-action-v0.1.md` | existing prompt reused with M03 approval-request context |
| approver response | `prompts/org-payment/approver-multirole-action-v0.1.md` | new M03 approver prompt |
| buyer accounting handoff | `prompts/org-payment/buyer-free-choice-action-v0.1.md` | existing prompt reused with M03 accounting-handoff context |
| accountant response | `prompts/org-payment/accountant-free-choice-action-v0.1.md` | new M03 accountant prompt |

The buyer prompt must render distinct M03 context blocks for the approval-request turn and accounting-handoff turn. No dedicated buyer accounting-handoff prompt is introduced in this protocol. The M01 approver prompt `prompts/org-payment/approver-free-choice-action-v0.1.md` remains unchanged as the frozen M01 prompt; M03 uses `prompts/org-payment/approver-multirole-action-v0.1.md`. Changing the frozen M03 prompt set requires a later protocol revision before execution resumes.

The accountant prompt must render:

- scenario id
- scenario name
- accountant role
- current case state
- buyer handoff action
- approver action and Game Master decision
- available evidence
- action menu
- allowed source references
- action proposal schema
- instruction to return one JSON action proposal only
- instruction not to simulate buyer, requester, approver, vendor, or Game Master
- instruction not to treat ambiguous guidance as explicit approval unless explicitly recorded as approval evidence

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
- parser failure after attempt 2 excludes the run from accepted M03 counts and must be reported as an exclusion

Invalid or rejected proposals must be preserved in the role-turn `proposal_attempts/*.jsonl` artifact when available.

## Game Master Rules

M03 keeps the Game Master deterministic and menu-aware.

Buyer approval-request handling:

| Action type | Decision | State handling |
|---|---|---|
| `request_approval` | `proceeds` | Approval request is routed to approver; approval remains unresolved until approver response. |
| `request_approval_status` | `proceeds` | Approval status clarification is routed to approver. |
| `escalate` | `proceeds_with_note` | Escalation is recorded; approval remains unresolved. |

Approver handling:

| Action type | Decision | State handling |
|---|---|---|
| `approve_payment` | `proceeds` | Explicit approval is recorded. |
| `reject_payment` | `proceeds` | Explicit rejection is recorded. |
| `request_more_evidence` | `proceeds` | Approval remains unresolved. |
| `provide_ambiguous_guidance` | `proceeds_with_note` | Ambiguous guidance is recorded but not treated as explicit approval. |
| `escalate` | `proceeds_with_note` | Escalation path is recorded; approval remains unresolved. |

Buyer accounting-handoff handling:

| Action type | Decision | State handling |
|---|---|---|
| `submit_payment_request` | conditional | `proceeds` if explicit approval exists; otherwise `proceeds_with_note` with evidence gap. |
| `request_more_evidence` | `proceeds` | Evidence request is recorded before accounting completion. |
| `hold_payment` | `proceeds` | Payment remains held while approval evidence is unresolved. |
| `escalate` | `proceeds_with_note` | Escalation is recorded. |
| `mark_approval_inferred` | `requires_clarification` | Inferred approval is not treated as explicit approval under M03. |

Accountant handling:

| Action type | Decision | State handling |
|---|---|---|
| `prepare_payment` | conditional | `proceeds` if explicit approval exists; otherwise `proceeds_with_note` with evidence gap. |
| `hold_payment` | `proceeds` | Payment remains held while approval evidence is unresolved. |
| `request_more_evidence` | `proceeds` | Accountant requests missing evidence from buyer. |
| `escalate` | `proceeds_with_note` | Accountant escalates unresolved approval or handoff inconsistency. |
| `authorize_exception_review` | `proceeds_with_note` | Exception review route is recorded without treating it as approval. |

The Game Master must preserve the distinction between:

- explicit approval
- rejection
- request for more evidence
- ambiguous guidance
- inferred approval
- missing evidence

Game Master records must not let accountant preparation erase approval evidence gaps.

## Evidence Pack Requirements

Every accepted M03 run must include at minimum:

- `manifest.json`
- `scenario.yaml`
- `initial_state/case.md`
- `final_state/case.md`
- `messages.jsonl`
- `action_menus/buyer_approval_request.json`
- `action_menus/approver.json`
- `action_menus/buyer_accounting_handoff.json`
- `action_menus/accountant.json`
- `actions.jsonl`
- `gm_decisions.jsonl`
- `parser_results/buyer_approval_request.json`
- `parser_results/approver.json`
- `parser_results/buyer_accounting_handoff.json`
- `parser_results/accountant.json`
- `proposal_attempts/buyer_approval_request.jsonl`
- `proposal_attempts/approver.jsonl`
- `proposal_attempts/buyer_accounting_handoff.jsonl`
- `proposal_attempts/accountant.jsonl`
- `trace.jsonl`
- `events.jsonl`
- `metrics.json`
- `llm_prompts/buyer_A001_approval_request.md`
- `llm_prompts/approver_A002_free_choice.md`
- `llm_prompts/buyer_A003_accounting_handoff.md`
- `llm_prompts/accountant_A004_free_choice.md`
- `llm_outputs/buyer_A001_approval_request.json`
- `llm_outputs/approver_A002_free_choice.json`
- `llm_outputs/buyer_A003_accounting_handoff.json`
- `llm_outputs/accountant_A004_free_choice.json`
- `reviewer_notes.md`
- `reconstruction-checklist.md`

If the current validator cannot validate these role/turn-specific nested paths, the M03 execution PR must extend it compatibly. Existing EXP-0001, M01, and M02 evidence packs must remain valid.

Raw run output must be written under ignored `runs/` paths. Curated M03 artifacts may be committed only under `pilot-runs/` or `results/`.

## Exclusion Criteria

A run is excluded from accepted M03 counts if any of the following occurs:

- missing evidence pack
- parser failure after retry for buyer approval request, approver, buyer accounting handoff, or accountant
- provider/API failure
- incomplete LLM response
- invalid JSON or schema-invalid action proposal after retries
- selected action not in the role-turn-specific action menu
- selected `target_role` does not match the role-turn-specific action menu
- unknown `source_refs`
- missing Game Master decision for any accepted LLM action
- evidence-pack validation failure
- scenario id or run id mismatch
- required buyer approval-request, approver, buyer accounting-handoff, or accountant turn is missing

Excluded runs must not be silently replaced.

## Event Handling

M03 uses existing Event Taxonomy v0.1 if possible.

Likely relevant existing event types:

- `evidence_gap`
- `informal_pressure`
- `communication_breakdown`
- `policy_ambiguity_exploited`
- `responsibility_diffusion`
- `approval_bypass`

Generated event labels remain proposed and not human-reviewed.

No event taxonomy change is introduced by this protocol. If M03 execution requires a new event type, execution must pause for a protocol/schema revision before results are committed.

## Metrics and Reporting

M03 aggregation is limited to descriptive pilot accounting.

Required aggregate summaries:

- buyer approval-request action counts
- approver action counts
- buyer accounting-handoff action counts
- accountant action counts
- full coordination path counts:
  - buyer approval request -> approver response -> buyer handoff -> accountant response
- parser acceptance, retry, rejected proposal, and parser failure counts by role and turn
- Game Master decisions by role, turn, and selected action
- validation pass/fail counts
- exclusions by reason
- representative evidence links
- approval-evidence propagation summary
- coordination-gap summary

Approval-evidence propagation summary must include:

- buyer handoff cited approver action
- buyer handoff cited approver GM decision
- buyer handoff represented explicit approval correctly
- buyer handoff represented ambiguous guidance as ambiguous
- accountant cited buyer handoff
- accountant cited approver action or decision
- accountant action preserved approval gap when explicit approval was absent

Coordination-gap summary must include:

- explicit approval absent at accountant stage
- ambiguous guidance reached accountant stage
- accountant prepared payment without explicit approval
- accountant held payment due to missing evidence
- accountant requested more evidence
- accountant escalated
- generated/proposed responsibility-diffusion event count, if applicable

No inferential statistical test is part of M03.

## Schema Compatibility

This protocol prefers no schema or contract changes.

The following M03 action types are already expected to be available:

- `request_approval`
- `request_approval_status`
- `escalate`
- `approve_payment`
- `reject_payment`
- `request_more_evidence`
- `provide_ambiguous_guidance`
- `submit_payment_request`
- `hold_payment`
- `mark_approval_inferred`
- `prepare_payment`
- `authorize_exception_review`

If any new action type is needed:

- add it as a backward-compatible enum addition
- document it in `protocols/data-contracts/action-proposal-contract-v0.1.md`
- validate that existing EXP-0001, M01, and M02 evidence packs remain valid

## Claim Boundary

M03 may claim only:

> Under the frozen M03 artificial organization protocol, buyer+approver+accountant LLM pilot runs produced recorded coordination paths, parser outcomes, GM decisions, validation outcomes, approval-evidence propagation observations, and coordination-gap observations.

Required limitations:

- artificial organization only
- M03 pilot only
- buyer + approver + accountant LLM control only
- requester and vendor are scripted or rule-based
- deterministic/rule-based Game Master
- generated/proposed event labels are not human-reviewed coded evidence
- no human behavior claim
- no general LLM behavior claim
- no real-world organization claim
- no compliance, legal, audit, or operational sufficiency claim
- no statistical significance claim

Forbidden claims:

- responsibility diffusion has been reproduced
- approval bypass has been proven
- human organizations behave this way
- S04 causes coordination failure
- accounting handoff proves institutional failure
- this is a multi-role baseline
- this is statistically meaningful
- this generalizes to humans or real organizations

## Non-Goals

This protocol freeze does not add:

- M03 execution
- M03 run results
- M04-M05 execution
- multi-role baseline
- scenario changes
- M01 result changes
- M02 result changes
- EXP-0001 result changes
- event taxonomy changes
- model comparison
- human review
- human or real-world organization claims
- statistical claims

## Checkpoint Target

After this protocol freeze, the next PR may execute M03 without changing protocol, prompts, action menus, Game Master rules, evidence requirements, event taxonomy, metrics, or claim boundaries.
