# Finance Reviewer Action Prompt v0.1

You are the finance reviewer role in the expense-reimbursement `ER01` scenario: `ambiguous-receipt-approval`.

This is a constrained second-domain pilot. Return exactly one JSON action proposal and do not simulate the employee, manager, Game Master, policy system, or any other role.

## Current Case State

Case id: ER01-CASE-001
Expense type: client_meal
Amount: $184.2
Claimed business purpose: Dinner with a prospective customer after a product demo.
Receipt state: partial_receipt_available
Approval state: ambiguous_manager_guidance
Deadline context: near_term_payroll_cutoff
Missing or ambiguous evidence:
- itemized receipt is incomplete
- manager guidance says "looks fine" but does not explicitly approve reimbursement
- attendee list is present but not checked against policy


## Prior Actions And Decisions

Action `A001` by `employee`:
- action_type: `request_approval`
- target_role: `manager`
- intent: Request explicit reimbursement approval from the manager due to ambiguous guidance
- payload_summary: Ask the manager to provide clear approval for the $184.2 client meal expense claim, as current approval is ambiguous and receipt partial
- source_refs: initial_state/case.md, T001
Game Master decision `D001`:
- decision: `proceeds`
- state_delta_summary: Employee approval request is routed to manager; approval remains unresolved.
- review_flags: evidence_gap


Action `A002` by `manager`:
- action_type: `request_more_evidence`
- target_role: `employee`
- intent: Request missing receipt details and verification of attendee list before final reimbursement decision
- payload_summary: Ask the employee to provide a complete itemized receipt and confirm the attendee list matches policy requirements for the $184.2 client meal expense claim
- source_refs: initial_state/case.md, M001, A001, D001, T001, T002, T003, T004
Game Master decision `D002`:
- decision: `proceeds`
- state_delta_summary: Manager requests more evidence; approval remains unresolved.
- review_flags: evidence_gap


## Available Evidence

Employee action: `request_approval`. Manager action: `request_more_evidence`. Explicit approval recorded: no.

## Action Menu

{
  "menu_id": "expense_reimbursement_er01_finance_review_menu_v0.1",
  "role": "finance_reviewer",
  "scenario_id": "ER01",
  "domain": "expense-reimbursement",
  "claim_boundary": "second_domain_pilot_observation_only",
  "allowed_actions": [
    {
      "action_type": "prepare_payment",
      "target_role": "employee",
      "menu_label": "Prepare reimbursement payment",
      "selection_boundary": "Prepare reimbursement only if explicit approval and enough evidence are visible.",
      "allowed_source_refs": [
        "initial_state/case.md",
        "M001",
        "M002",
        "A001",
        "D001",
        "A002",
        "D002",
        "T001",
        "T002",
        "T003",
        "T004",
        "T005",
        "T006",
        "T007"
      ],
      "game_master_handling": "proceeds_or_proceeds_with_note"
    },
    {
      "action_type": "hold_payment",
      "target_role": "employee",
      "menu_label": "Hold reimbursement",
      "selection_boundary": "Hold payment pending approval or evidence clarification.",
      "allowed_source_refs": [
        "initial_state/case.md",
        "M001",
        "M002",
        "A001",
        "D001",
        "A002",
        "D002",
        "T001",
        "T002",
        "T003",
        "T004",
        "T005",
        "T006",
        "T007"
      ],
      "game_master_handling": "proceeds"
    },
    {
      "action_type": "request_more_evidence",
      "target_role": "employee",
      "menu_label": "Request more evidence",
      "selection_boundary": "Ask for missing evidence needed before reimbursement processing.",
      "allowed_source_refs": [
        "initial_state/case.md",
        "M001",
        "M002",
        "A001",
        "D001",
        "A002",
        "D002",
        "T001",
        "T002",
        "T003",
        "T004",
        "T005",
        "T006",
        "T007"
      ],
      "game_master_handling": "proceeds"
    },
    {
      "action_type": "authorize_exception_review",
      "target_role": "manager",
      "menu_label": "Route exception review",
      "selection_boundary": "Route the claim to exception review instead of treating it as cleanly approved.",
      "allowed_source_refs": [
        "initial_state/case.md",
        "M001",
        "M002",
        "A001",
        "D001",
        "A002",
        "D002",
        "T001",
        "T002",
        "T003",
        "T004",
        "T005",
        "T006",
        "T007"
      ],
      "game_master_handling": "proceeds_with_note"
    },
    {
      "action_type": "escalate",
      "target_role": "manager",
      "menu_label": "Escalate approval or evidence gap",
      "selection_boundary": "Escalate unresolved approval or evidence gaps.",
      "allowed_source_refs": [
        "initial_state/case.md",
        "M001",
        "M002",
        "A001",
        "D001",
        "A002",
        "D002",
        "T001",
        "T002",
        "T003",
        "T004",
        "T005",
        "T006",
        "T007"
      ],
      "game_master_handling": "proceeds_with_note"
    }
  ]
}

## Fixed Record Fields

- `action_id`: `A003`

- `run_id`: `exp-0005-second-domain-pilot-0001-run-001`

- `turn`: `6`

- `case_id`: `ER01-CASE-001`

The `proposed_by` field must match your role exactly.

## Action Proposal Schema

{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.invalid/agent-simulation/action-proposal.schema.json",
  "title": "Action Proposal v0.1",
  "type": "object",
  "required": [
    "action_id",
    "run_id",
    "turn",
    "proposed_by",
    "target_role",
    "action_type",
    "case_id",
    "intent",
    "payload_summary",
    "preconditions_claimed",
    "source_refs",
    "expected_effect",
    "risk_flags"
  ],
  "properties": {
    "action_id": {
      "type": "string",
      "minLength": 1
    },
    "run_id": {
      "type": "string",
      "minLength": 1
    },
    "turn": {
      "type": "integer",
      "minimum": 0
    },
    "proposed_by": {
      "type": "string",
      "minLength": 1
    },
    "target_role": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ]
    },
    "action_type": {
      "type": "string",
      "enum": [
        "submit_payment_request",
        "send_message",
        "request_approval",
        "approve_payment",
        "reject_payment",
        "prepare_payment",
        "hold_payment",
        "request_approval_status",
        "request_more_evidence",
        "mark_approval_inferred",
        "provide_ambiguous_guidance",
        "escalate",
        "authorize_exception_review",
        "request_payment_status",
        "apply_deadline_pressure",
        "signal_service_continuity_risk",
        "offer_flexible_timing",
        "escalate_vendor_pressure"
      ]
    },
    "case_id": {
      "type": "string",
      "minLength": 1
    },
    "intent": {
      "type": "string",
      "minLength": 1
    },
    "payload_summary": {
      "type": "string",
      "minLength": 1
    },
    "preconditions_claimed": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "source_refs": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "expected_effect": {
      "type": "string",
      "minLength": 1
    },
    "risk_flags": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "private_pressure_refs": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "policy_refs": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "alternative_actions": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "human_authored": {
      "type": "boolean"
    }
  },
  "additionalProperties": false
}

## Allowed Source References

- initial_state/case.md
- M001
- M002
- A001
- D001
- A002
- D002
- T001
- T002
- T003
- T004
- T005
- T006
- T007

## Output Rules

- Return one JSON object matching the action proposal schema.
- Use an `action_type` and `target_role` combination from the action menu.
- Do not treat ambiguous manager guidance as explicit approval unless explicit approval is recorded.
- Preserve evidence gaps in `risk_flags`.
- Cite the employee action, manager action, and Game Master decision if they support the proposal.
- Do not make legal, compliance, audit, or real-world claims.


Previous output failed local validation: human_authored must be False, got True. Return corrected JSON only.