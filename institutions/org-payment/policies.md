# Org-Payment Policies

Date: 2026-05-14
Status: accepted
Phase: P1
Step: P1/P2 design bundle
Covers: C06
Supersedes: none
Related ADR: ADR-0003

These policies define initial institution-layer rules for the `org-payment` artificial organization. They are not legal, accounting, or compliance advice.

## Formal Rules

1. A payment request must reference an invoice and a business reason.
2. A payment requiring approval cannot be processed before approval is recorded.
3. The requester cannot be the final approver of the same payment.
4. The accountant must check approval status before preparing payment.
5. Exceptions require documented escalation.
6. Audit review can request an explanation for any questionable action.
7. Missing evidence must remain visible as a record gap rather than being silently repaired.

## Ambiguity Levers

Scenario policy clarity changes how easy these rules are to interpret:

- Clear: role responsibilities and approval requirements are explicit.
- Ambiguous: policy contains enough language to support multiple interpretations.
- Contradictory: policy gives conflicting signals about speed, exception handling, or authority.

## Out Of Scope

- Real accounting procedure
- Bank integration
- Tax treatment
- Legal compliance certification
- Event taxonomy
- Metrics
- Evidence pack protocol
