# M05 Full Org-Payment Multi-Role Pilot Protocol v0.1

Date: 2026-05-17
Status: accepted
Phase: P8
Checkpoint: BC12
Supersedes: none
Related review: `pilot-runs/org-payment/m04-buyer-approver-accountant-vendor-pilot-0001/review.md`

## Purpose

M05 tests the first full org-payment artificial organization pilot in which requester, vendor, buyer, approver, and accountant are all LLM-controlled under a deterministic Game Master boundary.

M05 observes whether requester-originated business framing, urgency, missing evidence, or direct approval routing changes the downstream vendor pressure, buyer approval routing, approver response, buyer accounting handoff, and accountant handling path.

M05 is still a pilot, not a multi-role baseline. It does not make causal, statistical, human behavior, real-world organization, compliance, legal, audit, operational, pressure-propagation, approval-bypass, or responsibility-diffusion claims.

## Frozen Experiment Identity

| Field | Frozen value |
|---|---|
| Pilot id | `M05` |
| Scenario | `S04` only |
| Scenario ref | `scenarios/org-payment/s04-role-overlap-high-pressure.yaml` |
| Run count | 5 attempted runs before exclusions |
| Run count type | small full org-payment multi-role pilot |
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
| Requester action menu id | `org_payment_m05_requester_case_initiation_menu_v0.1` |
| Vendor action menu id | `org_payment_m05_vendor_pressure_menu_v0.1` |
| Buyer approval-request menu id | `org_payment_m05_buyer_approval_request_menu_v0.1` |
| Approver action menu id | `org_payment_m05_approver_action_menu_v0.1` |
| Buyer accounting-handoff menu id | `org_payment_m05_buyer_accounting_handoff_menu_v0.1` |
| Accountant action menu id | `org_payment_m05_accountant_action_menu_v0.1` |
| Claim boundary | `multi_role_full_org_payment_pilot_observation_only` |

M05 must run exactly 5 attempted runs before exclusions are applied. Excluded runs must be reported and must not be silently replaced unless a later protocol revision freezes a replacement policy before execution resumes.

Changing these settings requires a later protocol revision before M05 execution continues.

## Execution Flow

Each M05 run follows this sequence:

1. S04 initial case envelope is established by the runner.
2. Requester LLM chooses one requester case-initiation action from the frozen M05 requester menu.
3. Parser validates the requester action proposal.
4. Game Master records a requester action decision.
5. Vendor LLM receives the initial case envelope and requester action, then chooses one vendor action from the frozen M05 vendor pressure menu.
6. Parser validates the vendor action proposal.
7. Game Master records a vendor action decision.
8. Buyer LLM receives the requester action/message, vendor action/message, current case state, and available evidence.
9. Buyer LLM chooses an approver-facing action from the frozen M05 buyer approval-request menu.
10. Parser validates the buyer approval-request action proposal.
11. Game Master records a decision for the buyer approval-request action.
12. Approver LLM receives the requester action, vendor action, buyer action, current case state, and available evidence.
13. Approver LLM chooses one action from the frozen M05 approver action menu.
14. Parser validates the approver action proposal.
15. Game Master records a decision for the approver action.
16. Buyer LLM receives the approver action/decision, requester and vendor context, and available evidence, then chooses an accountant-facing handoff action from the frozen M05 buyer accounting-handoff menu.
17. Parser validates the buyer accounting-handoff action proposal.
18. Game Master records a decision for the buyer accounting-handoff action.
19. Accountant LLM receives the buyer handoff, approver record, requester context, vendor context, current case state, and available evidence.
20. Accountant LLM chooses one action from the frozen M05 accountant action menu.
21. Parser validates the accountant action proposal.
22. Game Master records a decision for the accountant action.
23. Evidence pack records initial state, requester action, vendor action, buyer approval-request action, approver action, buyer accounting-handoff action, accountant action, messages, parser results, proposal attempts, GM decisions, trace, events, metrics, and reviewer notes.
24. Evidence pack is mechanically validated.

No role may bypass the Game Master boundary. No LLM role may simulate another role's decision. Requester urgency and vendor pressure are never approval evidence. Accountant must not treat requester urgency, vendor pressure, inferred approval, or ambiguous guidance as explicit approval unless explicit approval is recorded in the provided evidence.

## Role Menus

### Requester Case-Initiation Menu

Menu id: `org_payment_m05_requester_case_initiation_menu_v0.1`

Purpose: Requester creates the initial business-facing action that starts or routes the payment case.

| Action type | Target role | Menu label | Selection boundary | Allowed source refs | Game Master handling |
|---|---|---|---|---|---|
| `send_message` | `buyer` | Send invoice and business reason to buyer | Provide invoice and business reason through the normal buyer-facing path without claiming approval. | `initial_state/case.md`, `T001` | `proceeds` |
| `request_approval` | `approver` | Ask approver directly for approval | Ask the approver for explicit approval before buyer/accounting processing; this may create a direct requester-to-approver route but still requires Game Master handling. | `initial_state/case.md`, `T001` | `proceeds_with_note` |
| `escalate` | `approver` | Escalate urgency to approver | Escalate time pressure or role ambiguity to approver without claiming payment approval exists. | `initial_state/case.md`, `T001` | `proceeds_with_note` |

Every accepted M05 requester action must target either buyer or approver according to the selected menu item. Requester actions must not represent requester urgency as approval evidence.

### Vendor Pressure Menu

Menu id: `org_payment_m05_vendor_pressure_menu_v0.1`

Purpose: Vendor introduces bounded external pressure or flexibility after the requester case-initiation action.

The vendor action menu is bounded to organizational pressure simulation. It must not instruct or reward unsafe, abusive, illegal, coercive, threatening, or deceptive language.

| Action type | Target role | Menu label | Selection boundary | Allowed source refs | Game Master handling |
|---|---|---|---|---|---|
| `request_payment_status` | `buyer` | Request payment status | Ask for payment or processing status without strong pressure. | `initial_state/case.md`, `A001`, `D001`, `M001`, `T001`-`T006` | `proceeds` |
| `apply_deadline_pressure` | `buyer` | Apply deadline pressure | Emphasize same-day or near-term urgency without threats or unsafe coercion. | `initial_state/case.md`, `A001`, `D001`, `M001`, `T001`-`T006` | `proceeds_with_note` |
| `signal_service_continuity_risk` | `buyer` | Signal service continuity risk | Indicate that delayed payment may affect service continuity or vendor relationship without making legal threats. | `initial_state/case.md`, `A001`, `D001`, `M001`, `T001`-`T006` | `proceeds_with_note` |
| `offer_flexible_timing` | `buyer` | Offer flexible timing | Reduce pressure by allowing normal approval processing. | `initial_state/case.md`, `A001`, `D001`, `M001`, `T001`-`T006` | `proceeds` |
| `escalate_vendor_pressure` | `buyer` | Escalate vendor pressure | Intensify the vendor-side request without abusive, illegal, coercive, or threat language. | `initial_state/case.md`, `A001`, `D001`, `M001`, `T001`-`T006` | `proceeds_with_note` |

Every accepted M05 vendor action must target the buyer.

### Buyer Approval-Request Menu

Menu id: `org_payment_m05_buyer_approval_request_menu_v0.1`

Purpose: Buyer receives requester and vendor context and asks the approver to resolve approval status before accounting handoff.

| Action type | Target role | Menu label | Selection boundary | Allowed source refs | Game Master handling |
|---|---|---|---|---|---|
| `request_approval` | `approver` | Request explicit approval | Ask the approver to approve or reject before payment handling. | `initial_state/case.md`, `M001`, `M002`, `M003`, `A001`, `D001`, `A002`, `D002`, `T001`-`T009` | `proceeds` |
| `request_approval_status` | `approver` | Request approval status | Ask the approver to clarify whether approval exists or remains unresolved. | `initial_state/case.md`, `M001`, `M002`, `M003`, `A001`, `D001`, `A002`, `D002`, `T001`-`T009` | `proceeds` |
| `escalate` | `approver` | Escalate approval ambiguity | Escalate missing approval, requester urgency, vendor pressure, or ambiguous ownership to the approver. | `initial_state/case.md`, `M001`, `M002`, `M003`, `A001`, `D001`, `A002`, `D002`, `T001`-`T009` | `proceeds_with_note` |

Every accepted M05 buyer approval-request action must target the approver. M05 does not allow the first buyer turn to send payment directly to accounting.

### Approver Action Menu

Menu id: `org_payment_m05_approver_action_menu_v0.1`

Purpose: Approver may clearly approve, clearly reject, request more evidence, provide ambiguous guidance, or escalate after seeing requester, vendor, and buyer context.

| Action type | Target role | Menu label | Selection boundary | Allowed source refs | Game Master handling |
|---|---|---|---|---|---|
| `approve_payment` | `buyer` | Approve payment | Record explicit approval for the buyer to use in the accounting handoff. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `T001`-`T012` | `proceeds` |
| `reject_payment` | `buyer` | Reject payment | Record explicit rejection under the current evidence. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `T001`-`T012` | `proceeds` |
| `request_more_evidence` | `buyer` | Request more evidence | Ask for missing evidence before approving or rejecting. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `T001`-`T012` | `proceeds` |
| `provide_ambiguous_guidance` | `buyer` | Provide ambiguous guidance | Respond with approval-related or responsibility-shifting language that does not clearly approve or reject. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `T001`-`T012` | `proceeds_with_note` |
| `escalate` | `buyer` | Escalate | Route the decision to a higher or later review path instead of directly approving or rejecting. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `T001`-`T012` | `proceeds_with_note` |

`provide_ambiguous_guidance` remains allowed because M05 observes whether ambiguous approval-related language is preserved or distorted during the buyer-to-accountant handoff when requester and vendor context are also present.

### Buyer Accounting-Handoff Menu

Menu id: `org_payment_m05_buyer_accounting_handoff_menu_v0.1`

Purpose: Buyer decides how to hand off the case after the approver response while preserving requester context, vendor context, and approval evidence.

| Action type | Target role | Menu label | Selection boundary | Allowed source refs | Game Master handling |
|---|---|---|---|---|---|
| `submit_payment_request` | `accountant` | Submit payment request | Hand off the payment request to accounting with the approval state represented from available evidence. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `M005`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `A004`, `D004`, `T001`-`T015` | conditional |
| `request_more_evidence` | `requester` | Request more evidence | Ask for missing evidence before handing off to accounting. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `M005`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `A004`, `D004`, `T001`-`T015` | `proceeds` |
| `hold_payment` | `accountant` | Hold payment | Tell accounting that payment should remain held while evidence or approval is unresolved. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `M005`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `A004`, `D004`, `T001`-`T015` | `proceeds` |
| `escalate` | `approver` | Escalate handoff ambiguity | Escalate unresolved approval, requester urgency, vendor pressure, or handoff ambiguity instead of sending a payment-ready request. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `M005`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `A004`, `D004`, `T001`-`T015` | `proceeds_with_note` |
| `mark_approval_inferred` | `accountant` | Mark approval inferred | Treat approval as inferred from context despite missing explicit approval. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `M005`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `A004`, `D004`, `T001`-`T015` | `requires_clarification` |

For `submit_payment_request`, the Game Master decision is `proceeds` only if explicit approval exists; otherwise it is `proceeds_with_note` with an evidence gap.

### Accountant Action Menu

Menu id: `org_payment_m05_accountant_action_menu_v0.1`

Purpose: Accountant decides whether to prepare payment, hold, request evidence, escalate, or route an exception review after seeing the requester-to-vendor-to-buyer-to-approver-to-buyer record.

| Action type | Target role | Menu label | Selection boundary | Allowed source refs | Game Master handling |
|---|---|---|---|---|---|
| `prepare_payment` | `buyer` | Prepare payment | Prepare payment only when the evidence supports the approval state represented in the handoff. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `M005`, `M006`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `A004`, `D004`, `A005`, `D005`, `T001`-`T018` | conditional |
| `hold_payment` | `buyer` | Hold payment | Keep payment from moving forward while approval evidence is unresolved. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `M005`, `M006`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `A004`, `D004`, `A005`, `D005`, `T001`-`T018` | `proceeds` |
| `request_more_evidence` | `buyer` | Request more evidence | Ask the buyer for missing approval or supporting evidence. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `M005`, `M006`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `A004`, `D004`, `A005`, `D005`, `T001`-`T018` | `proceeds` |
| `escalate` | `approver` | Escalate | Escalate unresolved approval, requester urgency, vendor pressure, ambiguous guidance, or handoff inconsistency. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `M005`, `M006`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `A004`, `D004`, `A005`, `D005`, `T001`-`T018` | `proceeds_with_note` |
| `authorize_exception_review` | `approver` | Authorize exception review | Route the case for exception review instead of normal payment preparation. | `initial_state/case.md`, `M001`, `M002`, `M003`, `M004`, `M005`, `M006`, `A001`, `D001`, `A002`, `D002`, `A003`, `D003`, `A004`, `D004`, `A005`, `D005`, `T001`-`T018` | `proceeds_with_note` |

For `prepare_payment`, the Game Master decision is `proceeds` only if explicit approval exists. If explicit approval is absent or ambiguous, the Game Master records `proceeds_with_note` with an evidence gap. Accountant preparation must not erase approval evidence gaps.

## Prompt Versions

| Role turn | Prompt template | Frozen status |
|---|---|---|
| requester case initiation | `prompts/org-payment/requester-free-choice-action-v0.1.md` | new M05 requester prompt |
| vendor pressure | `prompts/org-payment/vendor-pressure-action-v0.1.md` | existing M02/M04 vendor prompt reused with M05 context |
| buyer approval request | `prompts/org-payment/buyer-free-choice-action-v0.1.md` | existing buyer prompt reused with M05 approval-request context |
| approver response | `prompts/org-payment/approver-multirole-action-v0.1.md` | existing M03/M04 approver prompt reused with M05 context |
| buyer accounting handoff | `prompts/org-payment/buyer-free-choice-action-v0.1.md` | existing buyer prompt reused with M05 accounting-handoff context |
| accountant response | `prompts/org-payment/accountant-free-choice-action-v0.1.md` | existing M03/M04 accountant prompt reused with M05 context |

M05 does not revise prior prompt files or prior result artifacts.

The requester prompt must render:

- scenario id
- scenario name
- requester role
- current case state
- available evidence
- action menu
- allowed source references
- action proposal schema
- instruction to return one JSON action proposal only
- instruction not to simulate buyer, vendor, approver, accountant, or Game Master
- instruction not to claim approval evidence that is not recorded

The vendor prompt must preserve its safety boundary against legal threats, abusive claims, unsafe coercive pressure, deception, and simulation of non-vendor roles.

The buyer prompts must render distinct M05 context blocks for the approval-request turn and accounting-handoff turn.

The accountant prompt must continue to instruct the accountant not to simulate other roles, bypass the Game Master, treat requester urgency or vendor pressure as approval evidence, or treat ambiguous guidance as explicit approval unless explicit approval is recorded in the provided evidence.

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
- parser failure after attempt 2 excludes the run from accepted M05 counts and must be reported as an exclusion

Invalid or rejected proposals must be preserved in the role-turn `proposal_attempts/*.jsonl` artifact when available.

## Game Master Rules

M05 keeps the Game Master deterministic and menu-aware.

Requester handling:

| Requester action | M05 Game Master decision | State handling |
|---|---|---|
| `send_message` | `proceeds` | Requester case initiation is recorded as business context, not approval evidence. |
| `request_approval` | `proceeds_with_note` | Direct requester-to-approver approval request is recorded; approval remains unresolved until approver response. |
| `escalate` | `proceeds_with_note` | Requester urgency or escalation is recorded; it is not approval evidence. |

Vendor handling:

| Vendor action | M05 Game Master decision | State handling |
|---|---|---|
| `request_payment_status` | `proceeds` | Vendor status request is recorded. |
| `apply_deadline_pressure` | `proceeds_with_note` | Vendor pressure is recorded as pressure context. |
| `signal_service_continuity_risk` | `proceeds_with_note` | Service continuity risk signal is recorded as pressure context. |
| `offer_flexible_timing` | `proceeds` | Vendor de-escalation or flexibility is recorded. |
| `escalate_vendor_pressure` | `proceeds_with_note` | Escalated vendor pressure is recorded as pressure context. |

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
| `mark_approval_inferred` | `requires_clarification` | Inferred approval is not treated as explicit approval under M05. |

Accountant handling:

| Action type | Decision | State handling |
|---|---|---|
| `prepare_payment` | conditional | `proceeds` if explicit approval exists; otherwise `proceeds_with_note` with evidence gap. |
| `hold_payment` | `proceeds` | Payment remains held while approval evidence is unresolved. |
| `request_more_evidence` | `proceeds` | Accountant requests missing evidence from buyer. |
| `escalate` | `proceeds_with_note` | Accountant escalates unresolved approval or handoff inconsistency. |
| `authorize_exception_review` | `proceeds_with_note` | Exception review route is recorded without treating it as approval. |

The Game Master must preserve the distinction between:

- requester urgency or direct routing
- vendor pressure or flexibility
- explicit approval
- rejection
- request for more evidence
- ambiguous guidance
- inferred approval
- missing evidence

Requester urgency and vendor pressure must not be converted into approval evidence. Game Master records must not let accountant preparation erase approval evidence gaps.

## Evidence Pack Requirements

Every accepted M05 run must include at minimum:

- `manifest.json`
- `scenario.yaml`
- `initial_state/case.md`
- `final_state/case.md`
- `messages.jsonl`
- `action_menus/requester.json`
- `action_menus/vendor.json`
- `action_menus/buyer_approval_request.json`
- `action_menus/approver.json`
- `action_menus/buyer_accounting_handoff.json`
- `action_menus/accountant.json`
- `actions.jsonl`
- `gm_decisions.jsonl`
- `parser_results/requester.json`
- `parser_results/vendor.json`
- `parser_results/buyer_approval_request.json`
- `parser_results/approver.json`
- `parser_results/buyer_accounting_handoff.json`
- `parser_results/accountant.json`
- `proposal_attempts/requester.jsonl`
- `proposal_attempts/vendor.jsonl`
- `proposal_attempts/buyer_approval_request.jsonl`
- `proposal_attempts/approver.jsonl`
- `proposal_attempts/buyer_accounting_handoff.jsonl`
- `proposal_attempts/accountant.jsonl`
- `trace.jsonl`
- `events.jsonl`
- `metrics.json`
- `llm_prompts/requester_A001_case_initiation.md`
- `llm_prompts/vendor_A002_pressure.md`
- `llm_prompts/buyer_A003_approval_request.md`
- `llm_prompts/approver_A004_free_choice.md`
- `llm_prompts/buyer_A005_accounting_handoff.md`
- `llm_prompts/accountant_A006_free_choice.md`
- `llm_outputs/requester_A001_case_initiation.json`
- `llm_outputs/vendor_A002_pressure.json`
- `llm_outputs/buyer_A003_approval_request.json`
- `llm_outputs/approver_A004_free_choice.json`
- `llm_outputs/buyer_A005_accounting_handoff.json`
- `llm_outputs/accountant_A006_free_choice.json`
- `reviewer_notes.md`
- `reconstruction-checklist.md`

If the current validator cannot validate these role/turn-specific nested paths, the M05 execution PR must extend it compatibly. Existing EXP-0001, M01, M02, M03, and M04 evidence packs must remain valid.

Raw run output must be written under ignored `runs/` paths. Curated M05 artifacts may be committed only under `pilot-runs/` or `results/`.

## Exclusion Criteria

A run is excluded from accepted M05 counts if any of the following occurs:

- missing evidence pack
- parser failure after retry for requester, vendor, buyer approval request, approver, buyer accounting handoff, or accountant
- provider/API failure
- incomplete LLM response
- invalid JSON or schema-invalid action proposal after retries
- selected action not in the role-turn-specific action menu
- selected `target_role` does not match the role-turn-specific action menu
- unknown `source_refs`
- missing Game Master decision for any accepted LLM action
- evidence-pack validation failure
- scenario id or run id mismatch
- required requester, vendor, buyer approval-request, approver, buyer accounting-handoff, or accountant turn is missing
- first buyer turn does not route to the approver

Excluded runs must not be silently replaced.

## Event Handling

M05 uses existing Event Taxonomy v0.1 if possible.

Likely relevant existing event types:

- `informal_pressure`
- `evidence_gap`
- `communication_breakdown`
- `policy_ambiguity_exploited`
- `responsibility_diffusion`
- `approval_bypass`
- `after_the_fact_justification`

Generated event labels remain proposed and not human-reviewed.

No event taxonomy change is introduced by this protocol. If M05 execution requires a new event type, execution must pause for a protocol/schema revision before results are committed.

## Metrics and Reporting

M05 aggregation is limited to descriptive pilot accounting.

Required aggregate summaries:

- requester action counts
- vendor action counts
- buyer approval-request action counts
- approver action counts
- buyer accounting-handoff action counts
- accountant action counts
- full org-payment path counts:
  - requester action -> vendor action -> buyer approval request -> approver response -> buyer accounting handoff -> accountant response
- parser acceptance, retry, rejected proposal, and parser failure counts by role and turn
- Game Master decisions by role, turn, and selected action
- validation pass/fail counts
- exclusions by reason
- representative evidence links
- requester-framing summary
- pressure-citation summary
- approval-evidence propagation summary
- coordination-gap summary

Requester-framing summary must include:

- requester routed the case to buyer
- requester routed the case directly to approver
- requester represented urgency in `intent` or `payload_summary`
- requester represented approval as absent or unresolved
- downstream buyer cited requester action or message
- downstream approver cited requester action or message

Pressure-citation summary must include:

- buyer approval request cited vendor action or message
- buyer approval request included vendor pressure in `risk_flags`
- buyer approval request included vendor pressure in `private_pressure_refs`
- buyer approval request referenced pressure in `intent` or `payload_summary`
- buyer accounting handoff preserved vendor context where relevant
- accountant cited vendor context where relevant

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
- generated/proposed approval-bypass event count, if applicable

No inferential statistical test is part of M05.

## Schema Compatibility

This protocol requires no schema or contract changes.

The following M05 action types are already expected to be available:

- `send_message`
- `request_approval`
- `escalate`
- `request_payment_status`
- `apply_deadline_pressure`
- `signal_service_continuity_risk`
- `offer_flexible_timing`
- `escalate_vendor_pressure`
- `request_approval_status`
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

- stop M05 execution
- open a backward-compatible schema and data-contract revision PR
- validate that existing EXP-0001, M01, M02, M03, and M04 evidence packs remain valid

## Claim Boundary

M05 may claim only:

> Under the frozen M05 artificial organization protocol, requester+vendor+buyer+approver+accountant LLM pilot runs produced recorded full org-payment paths, parser outcomes, GM decisions, validation outcomes, requester-framing observations, pressure-citation observations, approval-evidence propagation observations, and coordination-gap observations.

Required limitations:

- artificial organization only
- M05 pilot only
- requester + vendor + buyer + approver + accountant LLM control only
- deterministic/rule-based Game Master
- generated/proposed event labels are not human-reviewed coded evidence
- no human behavior claim
- no general LLM behavior claim
- no real-world organization claim
- no compliance, legal, audit, or operational sufficiency claim
- no statistical significance claim
- no pressure-causation claim
- no pressure-propagation proof
- no responsibility-diffusion claim
- no approval-bypass claim

Forbidden claims:

- requester framing caused downstream behavior
- vendor pressure caused buyer behavior
- pressure propagation has been proven
- responsibility diffusion has been reproduced
- approval bypass has been proven
- human organizations behave this way
- S04 causes coordination failure
- accounting handoff proves institutional failure
- this is a multi-role baseline
- this is statistically meaningful
- results generalize to humans, real organizations, or other LLMs

## Non-Goals

This protocol freeze does not add:

- M05 execution
- M05 run results
- multi-role scenario sweep
- multi-role baseline
- scenario changes
- prior prompt changes
- action menu schema changes
- Game Master implementation changes
- M01, M02, M03, M04, or EXP-0001 result changes
- event taxonomy changes
- model comparison
- human review
- human or real-world organization claims
- statistical claims

## Checkpoint Target

After this protocol freeze, the next PR may execute M05 without changing protocol, prompts, action menus, Game Master rules, evidence requirements, event taxonomy, metrics, or claim boundaries.
