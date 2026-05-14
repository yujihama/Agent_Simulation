# Trace Record Contract v0.1

Date: 2026-05-14
Status: accepted
Phase: P4
Step: P4/P5 data contracts and dry-run bundle
Covers: C05, C08, C12, C15, C16
Supersedes: none
Related ADR: ADR-0002, ADR-0003

## Purpose

A trace record is an ordered run-level record that lets reviewers reconstruct what happened across messages, action proposals, Game Master / Arbiter decisions, coded events, and state checkpoints.

Trace records are the spine of an evidence pack. They do not replace specialized message, action, decision, event, or metrics records.

This contract is a protocol-level artifact. It is not a JSON schema, production API, implementation code, or automated experiment harness.

## Required Fields

| Field | Meaning |
|---|---|
| `trace_id` | Stable identifier unique within the run. |
| `run_id` | Run or dry-run package identifier. |
| `turn` | Ordered sequence number. |
| `record_type` | `state`, `message`, `action`, `decision`, `event`, `metric`, or `review`. |
| `record_ref` | Identifier of the detailed record, if one exists. |
| `case_id` | Case affected by the trace entry. |
| `roles_involved` | Roles involved in the trace entry. |
| `summary` | Human-readable summary of what happened. |
| `source_artifact` | Evidence-pack artifact containing the detailed record. |

## Recommended Fields

| Field | Meaning |
|---|---|
| `state_before_ref` | Optional reference to prior state. |
| `state_after_ref` | Optional reference to resulting state. |
| `event_refs` | Coded events associated with this trace entry. |
| `review_flags` | Reconstruction or claim-boundary notes. |
| `human_authored` | Whether the record was manually authored for a dry run. |

## Record Ordering Rules

- `turn` order must be stable and sufficient for reconstruction.
- A trace entry may summarize another artifact, but the detailed artifact remains the source of record.
- State-changing action proposals should be followed by a Game Master / Arbiter decision before final state changes.
- Coded event trace entries should cite the action, message, or decision that supports the event.
- Review trace entries should not create new run facts; they should summarize reviewer work.

## Version Boundary

This contract is sufficient for paper dry runs and implementation planning. It does not define storage, timestamps, replay semantics, or a complete state model.
