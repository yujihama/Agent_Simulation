# Event Record Contract v0.1

Date: 2026-05-14
Status: accepted
Phase: P4
Step: P4/P5 data contracts and dry-run bundle
Covers: C13, C15, C16, C17, C18, C20
Supersedes: none
Related ADR: ADR-0001, ADR-0002, ADR-0003

## Purpose

An event record captures a coded observation from Event Taxonomy v0.1 and links it back to the evidence that supports the label.

The event record is review evidence, not proof of real-world behavior.

This contract is a protocol-level artifact. It is not a JSON schema, production API, implementation code, automated detector, or statistical result.

## Required Fields

| Field | Meaning |
|---|---|
| `event_id` | Stable identifier unique within the run. |
| `run_id` | Run or dry-run package identifier. |
| `taxonomy_version` | Event taxonomy version used. |
| `event_type` | Event type from the taxonomy. |
| `turn_start` | First turn associated with the event. |
| `turn_end` | Last turn associated with the event. |
| `roles_involved` | Roles involved in or affected by the event. |
| `severity` | Severity level from Event Taxonomy v0.1. |
| `confidence` | High, medium, or low reviewer confidence. |
| `description` | Human-readable event summary. |
| `source_refs` | Message, action, decision, trace, or state records supporting the event. |
| `coded_by` | Human reviewer, LLM-assisted suggestion, or manual dry-run author. |
| `review_status` | Proposed, accepted, revised, rejected, or disputed. |

## Recommended Fields

| Field | Meaning |
|---|---|
| `alternative_labels` | Plausible labels considered and rejected or left open. |
| `claim_use_limit` | Maximum claim class the event may support. |
| `notes_on_ambiguity` | Why the label may be uncertain. |
| `human_authored` | Whether the event was manually authored for a dry run. |

## Contract Rules

- Every event must cite source evidence.
- Low-confidence events should not support strong claims.
- LLM-assisted labels must remain proposed until a human reviewer accepts or revises them.
- Event records should preserve ambiguity rather than collapsing it into certainty.
- Event records should not introduce facts that are absent from the trace.

## Version Boundary

This contract is sufficient for paper dry runs and implementation planning. It does not define a classifier, inter-rater reliability threshold, or automated event extraction.
