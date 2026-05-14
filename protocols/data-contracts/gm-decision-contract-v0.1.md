# Game Master Decision Contract v0.1

Date: 2026-05-14
Status: accepted
Phase: P4
Step: P4/P5 data contracts and dry-run bundle
Covers: C06, C09, C12, C15, C16
Supersedes: none
Related ADR: ADR-0002, ADR-0003

## Purpose

A Game Master / Arbiter decision records how a proposed action is interpreted under world state, institution rules, scenario conditions, and control mode.

The decision is the authoritative bridge between actor proposal and state change. It should preserve both the outcome and the reason a reviewer can inspect later.

This contract is a protocol-level artifact. It is not a JSON schema, production API, implementation code, or automated rule engine.

## Decision Values

| Value | Meaning |
|---|---|
| `proceeds` | The action is accepted and may affect state. |
| `proceeds_with_note` | The action proceeds but a review-relevant note is recorded. |
| `requires_clarification` | The action cannot be decided without more information. |
| `rejected` | The action is not accepted under current state or policy. |
| `blocked` | Hard control or an explicit boundary prevents the action. |

## Required Fields

| Field | Meaning |
|---|---|
| `decision_id` | Stable identifier unique within the run. |
| `run_id` | Run or dry-run package identifier. |
| `turn` | Ordered turn or sequence number. |
| `action_id` | Action proposal being decided. |
| `decision` | One of the decision values above. |
| `control_mode` | Soft, monitored, or hard control. |
| `rule_refs` | Policy, norm, scenario, or ODD-Social references used in the decision. |
| `rationale` | Human-readable explanation of why the decision was made. |
| `state_delta_summary` | Summary of state changes, if any. |
| `evidence_refs` | Source records supporting the decision. |
| `review_flags` | Events or concerns a reviewer should inspect. |

## Recommended Fields

| Field | Meaning |
|---|---|
| `missing_evidence` | Required evidence absent at decision time. |
| `alternative_decision` | Plausible alternate outcome if policy or control mode differed. |
| `state_after_ref` | Reference to resulting state snapshot or trace record. |
| `human_authored` | Whether the decision was manually authored for a dry run. |

## Contract Rules

- Every payment-relevant accepted action should have a Game Master / Arbiter decision.
- Decisions must not hide evidence gaps; missing approval, rationale, or escalation should remain visible.
- Soft control can allow questionable action, but the decision should still record the concern.
- Monitored control should create an audit or review flag when relevant.
- Hard control should record the rule or boundary that blocked the action.

## Version Boundary

This contract is sufficient for paper dry runs and implementation planning. It does not define a rule engine, state transition implementation, or schema validation.
