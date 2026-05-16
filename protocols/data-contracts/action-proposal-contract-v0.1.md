# Action Proposal Contract v0.1

Date: 2026-05-14
Status: accepted
Phase: P4
Step: P4/P5 data contracts and dry-run bundle
Covers: C08, C09, C10, C12, C15
Supersedes: none
Related ADR: ADR-0002, ADR-0003

## Purpose

An action proposal is the record by which an actor asks the Game Master / Arbiter to change case state, request information, communicate, escalate, approve, reject, or process a payment-relevant step.

The actor proposes. The Game Master / Arbiter decides. An action proposal must not directly mutate world state.

This contract is a protocol-level artifact. It is not a JSON schema, production API, implementation code, or experiment harness.

## Required Fields

| Field | Meaning |
|---|---|
| `action_id` | Stable identifier unique within the run. |
| `run_id` | Run or dry-run package identifier. |
| `turn` | Ordered turn or sequence number. |
| `proposed_by` | Actor or role making the proposal. |
| `target_role` | Optional role expected to receive, approve, or act on the proposal. |
| `action_type` | Controlled action name, such as `request_approval`, `prepare_payment`, or `send_message`. |
| `case_id` | Payment case or scenario case affected by the proposal. |
| `intent` | Actor-facing reason for proposing the action. |
| `payload_summary` | Human-readable summary of the requested action. |
| `preconditions_claimed` | Preconditions the actor believes are satisfied. |
| `source_refs` | Trace, message, or prior decision references that explain the proposal. |
| `expected_effect` | State change or communication effect the actor expects. |
| `risk_flags` | Known uncertainty, policy ambiguity, evidence gap, or authority concern. |

## Recommended Fields

| Field | Meaning |
|---|---|
| `private_pressure_refs` | Optional references to pressure or incentive signals. |
| `policy_refs` | Policy or norm references used by the actor. |
| `alternative_actions` | Other actions the actor considered or could have chosen. |
| `human_authored` | Whether the proposal was manually authored for a dry run. |

## Action Type Guidance

Early org-payment action types may include:

- `submit_payment_request`
- `send_message`
- `request_approval`
- `approve_payment`
- `reject_payment`
- `prepare_payment`
- `hold_payment`
- `request_approval_status`
- `request_more_evidence`
- `mark_approval_inferred`
- `provide_ambiguous_guidance`
- `escalate`
- `authorize_exception_review`
- `request_payment_status`
- `apply_deadline_pressure`
- `signal_service_continuity_risk`
- `offer_flexible_timing`
- `escalate_vendor_pressure`

The list is intentionally open for v0.1. New action types should be documented in later protocol or schema work before implementation depends on them.

The vendor pressure action types are backward-compatible additions for the frozen M02 buyer+vendor pressure pilot protocol. They support bounded organizational pressure simulation only and do not authorize unsafe, abusive, illegal, coercive, deceptive, or threatening language.

## Contract Rules

- An action proposal must be reviewable without inspecting hidden actor state.
- The proposal should cite the message, trace, or decision that motivated it.
- The proposal should expose uncertainty instead of silently assuming authority or evidence.
- Payment-relevant actions must be decided by a Game Master / Arbiter decision record before they affect state.
- Manual dry-run proposals must be marked as human-authored in the run manifest or action record.

## Version Boundary

This contract is sufficient for paper dry runs and implementation planning. It does not specify provider-specific LLM prompts, adapter interfaces, automated validation, or a complete action vocabulary.
