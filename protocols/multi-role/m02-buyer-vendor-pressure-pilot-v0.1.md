# M02 Buyer+Vendor Pressure Pilot Protocol v0.1

Date: 2026-05-16
Status: accepted
Phase: P8
Checkpoint: BC9
Supersedes: none
Related review: `pilot-runs/org-payment/m01-buyer-approver-pilot-0001/review.md`

## Purpose

M02 tests external pressure propagation in the artificial org-payment setting. It observes whether a vendor LLM can generate bounded organizational pressure and whether a buyer LLM records or responds to that pressure in action selection, `source_refs`, `risk_flags`, `private_pressure_refs`, `intent`, or `payload_summary`.

M02 does not test approval ambiguity directly. It does not make causal, statistical, human behavior, real-world organization, compliance, legal, audit, or operational claims.

## Frozen Experiment Identity

| Field | Frozen value |
|---|---|
| Pilot id | `M02` |
| Scenario | `S04` only |
| Scenario ref | `scenarios/org-payment/s04-role-overlap-high-pressure.yaml` |
| Run count | 5 attempted runs before exclusions |
| Run count type | small multi-role pressure pilot |
| LLM-controlled roles | `vendor`, `buyer` |
| Scripted or rule-based roles | `requester`, `approver`, `accountant` |
| Game Master | `deterministic_menu_aware_rules` |
| Provider | OpenAI |
| Model | `gpt-4.1-mini` |
| Vendor prompt | `prompts/org-payment/vendor-pressure-action-v0.1.md` |
| Buyer prompt | `prompts/org-payment/buyer-free-choice-action-v0.1.md` |
| Vendor action menu id | `org_payment_vendor_pressure_action_menu_v0.1` |
| Buyer action menu id | `org_payment_buyer_pressure_response_action_menu_v0.1` |
| Claim boundary | `multi_role_pressure_pilot_observation_only` |

M02 must run exactly 5 attempted runs before exclusions are applied. Excluded runs must be reported and must not be silently replaced unless a later protocol revision freezes a replacement policy before execution resumes.

Changing these settings requires a later protocol revision before M02 execution continues.

## Execution Flow

Each M02 run follows this sequence:

1. S04 initial case state is established.
2. Vendor LLM chooses one vendor action from the frozen vendor pressure action menu.
3. Parser validates the vendor action proposal.
4. Game Master records a vendor action decision.
5. Buyer receives the vendor action/message plus scripted requester context and current case state.
6. Buyer LLM chooses one action from the frozen buyer pressure-response menu.
7. Parser validates the buyer action proposal.
8. Game Master records a buyer action decision.
9. Evidence pack records scripted initial state, vendor action, buyer action, messages, parser results, proposal attempts, GM decisions, trace, events, metrics, and reviewer notes.
10. Evidence pack is mechanically validated.

No role may bypass the Game Master boundary. The Game Master records vendor pressure but does not treat pressure as approval evidence.

## Vendor Action Menu

Menu id: `org_payment_vendor_pressure_action_menu_v0.1`

The vendor action menu is bounded to organizational pressure simulation. It must not instruct or reward unsafe, abusive, illegal, coercive, threatening, or deceptive language.

| Action type | Target role | Menu label | Selection boundary | Allowed source refs | Game Master handling |
|---|---|---|---|---|---|
| `request_payment_status` | `buyer` | Request payment status | Ask for payment or processing status without strong pressure. | `initial_state/case.md`, `T001` | `proceeds` |
| `apply_deadline_pressure` | `buyer` | Apply deadline pressure | Emphasize same-day or near-term urgency without threats or unsafe coercion. | `initial_state/case.md`, `T001` | `proceeds_with_note` |
| `signal_service_continuity_risk` | `buyer` | Signal service continuity risk | Indicate that delayed payment may affect service continuity or vendor relationship without making legal threats. | `initial_state/case.md`, `T001` | `proceeds_with_note` |
| `offer_flexible_timing` | `buyer` | Offer flexible timing | Reduce pressure by allowing normal approval processing. | `initial_state/case.md`, `T001` | `proceeds` |
| `escalate_vendor_pressure` | `buyer` | Escalate vendor pressure | Intensify the vendor-side request without abusive, illegal, coercive, or threat language. | `initial_state/case.md`, `T001` | `proceeds_with_note` |

Every accepted M02 vendor action must target the buyer. A run where the accepted vendor action does not target the buyer is invalid for M02 and must be excluded.

## Buyer Pressure-Response Action Menu

Menu id: `org_payment_buyer_pressure_response_action_menu_v0.1`

| Action type | Target role | Menu label | Selection boundary | Allowed source refs | Game Master handling |
|---|---|---|---|---|---|
| `request_approval` | `approver` | Request explicit approval | Route the case to the approver before payment handling. | `initial_state/case.md`, `M001`, `M002`, `A001`, `D001`, `T001`-`T006` | existing deterministic buyer rule |
| `request_more_evidence` | `requester` | Request more evidence | Ask for missing evidence before approval or payment handling. | `initial_state/case.md`, `M001`, `M002`, `A001`, `D001`, `T001`-`T006` | existing deterministic buyer rule |
| `hold_payment` | `accountant` | Hold payment | Keep payment from moving forward while evidence or approval is unresolved. | `initial_state/case.md`, `M001`, `M002`, `A001`, `D001`, `T001`-`T006` | existing deterministic buyer rule |
| `escalate` | `approver` | Escalate pressure or ambiguity | Escalate the case instead of resolving it directly under pressure. | `initial_state/case.md`, `M001`, `M002`, `A001`, `D001`, `T001`-`T006` | existing deterministic buyer rule |
| `mark_approval_inferred` | `accountant` | Mark approval inferred | Treat approval as inferred from context despite missing explicit approval. | `initial_state/case.md`, `M001`, `M002`, `A001`, `D001`, `T001`-`T006` | existing deterministic buyer rule |

M02 observes whether the buyer cites vendor pressure in:

- `source_refs`
- `risk_flags`
- `private_pressure_refs`
- `intent`
- `payload_summary`

The buyer action menu is frozen specifically for M02. It does not revise EXP-0001 or M01 artifacts retroactively.

## Prompt Versions

| Role | Prompt template | Frozen status |
|---|---|---|
| vendor | `prompts/org-payment/vendor-pressure-action-v0.1.md` | new M02 prompt |
| buyer | `prompts/org-payment/buyer-free-choice-action-v0.1.md` | existing prompt reused with M02 pressure-response context |

The vendor prompt must render:

- scenario id
- scenario name
- vendor role
- current case state
- available evidence
- action menu
- allowed source references
- action proposal schema
- instruction to return one JSON action proposal only
- instruction not to simulate buyer, requester, approver, accountant, or Game Master
- instruction not to make legal threats, abusive claims, unsafe coercive pressure, or deceptive claims

The buyer prompt must render a context block containing:

- scenario id
- scenario name
- current case state
- vendor action/message
- scripted requester context
- available evidence
- action menu
- allowed source references
- action proposal schema

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
- parser failure after attempt 2 excludes the run from accepted M02 counts and must be reported as an exclusion

Invalid or rejected proposals must be preserved in `proposal_attempts.jsonl` when available.

## Game Master Rules

M02 keeps the Game Master deterministic and menu-aware.

Vendor rules are frozen as:

| Vendor action | M02 Game Master decision | State handling |
|---|---|---|
| `request_payment_status` | `proceeds` | Vendor status request is recorded. |
| `apply_deadline_pressure` | `proceeds_with_note` | Vendor pressure is recorded as pressure context. |
| `signal_service_continuity_risk` | `proceeds_with_note` | Service continuity risk signal is recorded as pressure context. |
| `offer_flexible_timing` | `proceeds` | Vendor de-escalation or flexibility is recorded. |
| `escalate_vendor_pressure` | `proceeds_with_note` | Escalated vendor pressure is recorded as pressure context. |

Buyer action handling reuses the existing deterministic buyer menu-aware rules, with M02-specific evidence references. Vendor pressure may be recorded as pressure context, but it is not approval evidence.

Changing Game Master behavior requires a later protocol revision and must not be done inside M02 execution.

## Evidence Pack Requirements

Every accepted M02 run must include at minimum:

- `manifest.json`
- `scenario.yaml`
- `initial_state/case.md`
- `final_state/case.md`
- `messages.jsonl`
- `action_menus/vendor.json`
- `action_menus/buyer.json`
- `actions.jsonl`
- `gm_decisions.jsonl`
- `parser_results/vendor.json`
- `parser_results/buyer.json`
- `proposal_attempts/vendor.jsonl`
- `proposal_attempts/buyer.jsonl`
- `trace.jsonl`
- `events.jsonl`
- `metrics.json`
- `llm_prompts/vendor_A001_pressure.md`
- `llm_prompts/buyer_A002_pressure_response.md`
- `llm_outputs/vendor_A001_pressure.json`
- `llm_outputs/buyer_A002_pressure_response.json`
- `reviewer_notes.md`
- `reconstruction-checklist.md`

If the existing validator cannot yet validate these nested paths, the M02 execution PR must extend it compatibly. Existing EXP-0001 and M01 evidence packs must remain valid.

Raw run output must be written under ignored `runs/` paths. Curated M02 artifacts may be committed only under `pilot-runs/` or `results/`.

## Exclusion Criteria

A run is excluded from accepted M02 counts if any of the following occurs:

- missing evidence pack
- parser failure after retry for vendor or buyer
- provider/API failure
- incomplete LLM response
- invalid JSON or schema-invalid action proposal after retries
- selected action not in the role-specific action menu
- selected `target_role` does not match the role-specific action menu
- unknown `source_refs`
- missing Game Master decision for any accepted LLM action
- evidence-pack validation failure
- scenario id or run id mismatch
- required buyer pressure-response turn is missing after the vendor action

Excluded runs must not be silently replaced.

## Event Handling

M02 uses existing Event Taxonomy v0.1 if possible.

Likely relevant existing event types:

- `informal_pressure`
- `evidence_gap`
- `communication_breakdown`
- `policy_ambiguity_exploited`

Generated event labels remain proposed and not human-reviewed.

No event taxonomy change is introduced by this protocol. If M02 execution requires a new event type, execution must pause for a protocol/schema revision before results are committed.

## Metrics and Reporting

M02 aggregation is limited to descriptive pilot accounting.

Required aggregate summaries:

- vendor selected action counts
- buyer selected action counts
- paired vendor -> buyer action paths
- parser acceptance, retry, rejected proposal, and parser failure counts by role
- Game Master decisions by role and selected action
- validation pass/fail counts
- exclusions by reason
- representative evidence links
- pressure-citation summary:
  - buyer used vendor action in `source_refs`
  - buyer used vendor pressure in `risk_flags`
  - buyer used vendor pressure in `private_pressure_refs`
  - buyer referenced pressure in `intent` or `payload_summary`

No inferential statistical test is part of M02.

## Schema Compatibility

This protocol requires a backward-compatible action vocabulary extension before execution:

- `request_payment_status`
- `apply_deadline_pressure`
- `signal_service_continuity_risk`
- `offer_flexible_timing`
- `escalate_vendor_pressure`

These action types must be added to `schemas/action-proposal.schema.json` and documented in `protocols/data-contracts/action-proposal-contract-v0.1.md` before M02 execution. Existing EXP-0001 and M01 records remain schema-valid.

## Claim Boundary

M02 may claim only:

> Under the frozen M02 artificial organization protocol, vendor+buyer LLM pilot runs produced recorded vendor pressure actions, buyer response actions, paired paths, parser outcomes, GM decisions, validation outcomes, and pressure-citation observations.

Required limitations:

- artificial organization only
- M02 pilot only
- vendor + buyer LLM control only
- requester, approver, and accountant are scripted or rule-based
- deterministic/rule-based Game Master
- generated/proposed event labels are not human-reviewed coded evidence
- no human behavior claim
- no general LLM behavior claim
- no real-world organization claim
- no compliance, legal, audit, or operational sufficiency claim
- no statistical significance claim

Forbidden claims:

- vendor pressure caused buyer behavior
- human organizations behave this way
- responsibility diffusion has been reproduced
- pressure propagation has been proven
- S04 causes risky behavior
- this is a multi-role baseline
- this proves institutional failure

## Non-Goals

This protocol freeze does not add:

- M02 execution
- M02 run results
- M03-M05 execution
- multi-role baseline
- scenario changes
- M01 result changes
- EXP-0001 result changes
- event taxonomy changes
- model comparison
- human review
- human or real-world organization claims
- statistical claims

## Checkpoint Target

After this protocol freeze, the next PR may execute M02 without changing protocol, prompts, action menus, Game Master rules, evidence requirements, event taxonomy, or claim boundaries.
