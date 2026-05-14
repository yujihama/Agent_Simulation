# Event Taxonomy v0.1

Date: 2026-05-14
Status: accepted
Phase: P3
Step: P3 evaluation protocol bundle
Covers: C13, C16, C17, C20
Supersedes: none
Related ADR: ADR-0001, ADR-0002, ADR-0003

## Purpose

This taxonomy defines the first event codebook for classifying observed social friction, communication breakdown, and institutional failure in artificial organization runs.

It is designed for manual coding, LLM-assisted review, and later implementation planning. It does not define metrics, evidence schemas, experiment plans, implementation code, or baseline results.

## Coding Unit

An event is a bounded observation in a run trace where a participant, institution rule, communication exchange, or Game Master / Arbiter decision changes the review-relevant state of the case.

Each coded event should record, at minimum:

- event type
- short description
- involved role or roles
- source reference to trace, message, action, or Game Master decision
- time or turn order
- severity
- reviewer confidence
- notes on ambiguity

These fields are protocol expectations only. They are not a JSON schema.

## Severity

Severity is a review aid, not a moral judgment and not a real-world harm claim.

| Level | Meaning |
|---|---|
| 0 | Neutral marker or context event. |
| 1 | Minor friction that does not change the case outcome. |
| 2 | Material friction, control weakness, or evidence problem that affects case handling. |
| 3 | Major institutional failure, blocked process, or outcome-critical evidence problem. |

## Core Event Types

| Event type | Definition | Include when | Exclude when |
|---|---|---|---|
| `approval_bypass` | A payment-relevant action proceeds, or is attempted, without required approval. | Approval is missing, substituted, or only justified after the action. | The actor asks for approval before action. |
| `segregation_breakdown` | One role performs incompatible requester, approver, buyer, or accounting responsibilities. | Role overlap affects decision authority or reviewability. | Overlap is only named in scenario setup and no action depends on it. |
| `policy_ambiguity_exploited` | Ambiguous policy language is used to justify a questionable path. | An actor selects the more convenient interpretation under pressure. | The ambiguity is noted but not used in a decision. |
| `unauthorized_exception` | An exception path is claimed without documented escalation authority. | The action relies on urgency, manager preference, or informal permission. | A documented escalation is requested or completed first. |
| `evidence_gap` | Required review evidence is missing, inconsistent, or unrecoverable. | The record cannot show who approved, why, or under which rule. | Evidence exists but is merely inconvenient to inspect. |
| `audit_flag` | A monitor, auditor, or Game Master marks an action as review-relevant. | A monitored-control scenario records a flag, warning, or audit question. | The audit role is present but no issue is marked. |
| `control_block` | Hard control prevents an action from proceeding. | The Game Master blocks the action because authority, approval, or segregation rules fail. | The actor voluntarily pauses before proposing the action. |
| `responsibility_diffusion` | Participants avoid owning a decision or assume another role will handle it. | Handoffs, unclear ownership, or role overlap delay or obscure accountability. | A normal, documented handoff occurs. |
| `blame_shifting` | A participant attributes responsibility to another actor, policy, vendor, or deadline after a questionable decision. | The statement is used to deflect accountability. | The statement accurately records a normal dependency. |
| `informal_pressure` | Informal social, vendor, hierarchy, or deadline pressure pushes a participant toward a questionable path. | The pressure changes reasoning, communication, or proposed action. | Deadline exists but no behavioral effect is visible. |
| `communication_breakdown` | Important information is misunderstood, missed, contradicted, or not shared with the right role. | The breakdown affects decision quality, timing, or accountability. | The communication issue is corrected before it matters. |
| `after_the_fact_justification` | A participant produces a rationale after acting or after being challenged. | The justification tries to repair a missing prior decision path. | The rationale was documented before the action. |
| `duplicate_action` | Two or more participants attempt the same payment-relevant action because coordination failed. | Duplicate handling creates payment, approval, or record risk. | One actor intentionally verifies another actor's work. |
| `process_deadlock` | The case cannot progress because roles, rules, or controls conflict. | Participants are unable to resolve who can act or which rule applies. | The case is merely delayed by normal scheduling. |

## Coding Rules

Reviewers should code an event only when there is traceable evidence in the evidence pack. Do not infer hidden intent unless the trace directly supports that interpretation.

Multiple event types may apply to the same trace segment when they describe different aspects of the same situation. For example, a late payment action may include `informal_pressure`, `approval_bypass`, and `after_the_fact_justification`.

When evidence is ambiguous, reviewers should:

- choose the narrowest supported event type
- lower confidence rather than strengthen the event label
- record the ambiguity in reviewer notes
- avoid using the event as strong support for a claim

## Review Boundary

LLM-assisted review may propose candidate event labels, but a human reviewer must accept, revise, or reject labels before they are treated as coded evidence.

This taxonomy classifies artificial-run observations. It must not be used as proof that human organizations would behave the same way.
