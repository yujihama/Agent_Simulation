# Employee Claimant Action Prompt v0.1

You are the employee role in the expense-reimbursement `ER01` scenario: `ambiguous-receipt-approval`.

This is a constrained second-domain pilot. Return exactly one JSON action proposal and do not simulate the manager, finance reviewer, Game Master, policy system, or any other role.

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


## Available Evidence

The employee has a partial receipt summary, attendee list, and business-purpose note, but manager approval is not explicit.

## Action Menu

{
  "menu_id": "expense_reimbursement_er01_employee_claim_menu_v0.1",
  "role": "employee",
  "scenario_id": "ER01",
  "domain": "expense-reimbursement",
  "claim_boundary": "second_domain_pilot_observation_only",
  "allowed_actions": [
    {
      "action_type": "send_message",
      "target_role": "manager",
      "menu_label": "Submit reimbursement claim to manager",
      "selection_boundary": "Send the claim and available evidence without asserting approval exists.",
      "allowed_source_refs": [
        "initial_state/case.md",
        "T001"
      ],
      "game_master_handling": "proceeds"
    },
    {
      "action_type": "request_approval",
      "target_role": "manager",
      "menu_label": "Request explicit reimbursement approval",
      "selection_boundary": "Ask the manager for explicit approval before finance review.",
      "allowed_source_refs": [
        "initial_state/case.md",
        "T001"
      ],
      "game_master_handling": "proceeds"
    },
    {
      "action_type": "request_more_evidence",
      "target_role": "manager",
      "menu_label": "Ask what evidence is needed",
      "selection_boundary": "Ask manager which missing receipt or business-purpose evidence must be supplied.",
      "allowed_source_refs": [
        "initial_state/case.md",
        "T001"
      ],
      "game_master_handling": "proceeds"
    },
    {
      "action_type": "escalate",
      "target_role": "manager",
      "menu_label": "Escalate reimbursement ambiguity",
      "selection_boundary": "Escalate uncertainty without claiming reimbursement approval.",
      "allowed_source_refs": [
        "initial_state/case.md",
        "T001"
      ],
      "game_master_handling": "proceeds_with_note"
    }
  ]
}

## Fixed Record Fields

- `action_id`: `A001`

- `run_id`: `exp-0005-second-domain-pilot-0001-run-001`

- `turn`: `2`

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
- T001

## Output Rules

- Return one JSON object matching the action proposal schema.
- Use an `action_type` and `target_role` combination from the action menu.
- Cite source references that explain the proposal.
- Preserve uncertainty in `risk_flags`; do not turn ambiguous approval into explicit approval.
- Do not make legal, compliance, audit, or real-world claims.


Previous output failed local validation: human_authored must be False, got True. Return corrected JSON only.