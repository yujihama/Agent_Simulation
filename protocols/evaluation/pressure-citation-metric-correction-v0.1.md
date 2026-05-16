# Pressure-Citation Metric Correction v0.1

Date: 2026-05-17
Status: accepted
Phase: P9
Step: pressure-citation metric correction
Covers: C14, C16, C18, C20
Supersedes: none
Related protocol: `protocols/evaluation/metrics-v0.1.md`, `protocols/evaluation/construct-validity-check-v0.1.md`

## Purpose

This document records a forward-looking correction to pressure-citation metric rules.

EXP-0002 human evidence review and construct-validity review found that several `pressure_citation_flags` records overcounted pressure on paths where the vendor selected `request_payment_status`. Those records preserved vendor context, but the vendor action was a routine status request rather than a pressure action. Generic language about payment delay, vendor relationship, or vendor dissatisfaction must not be treated as vendor pressure by itself.

This correction does not rewrite frozen EXP-0002 result artifacts. The historical EXP-0002 aggregate, human review, and construct-validity outputs remain the record of what was generated and reviewed. Future generated metrics must use the corrected rules below.

## Corrected Rule

Pressure-citation metrics must distinguish vendor context from vendor pressure.

Vendor pressure is positive only when at least one of the following is true:

- the vendor action type is one of:
  - `apply_deadline_pressure`
  - `signal_service_continuity_risk`
  - `escalate_vendor_pressure`
- the vendor action/message contains explicit pressure wording such as deadline, urgency, same-day handling, service-continuity risk, or escalation.

Vendor pressure is negative when:

- the vendor action type is `request_payment_status` and no independent explicit pressure wording is present;
- the vendor action type is `offer_flexible_timing`;
- downstream buyer or accountant text only mentions generic payment delay, vendor relationship, vendor dissatisfaction, or vendor context.

## Metric Field Interpretation

The following fields may be true on a `request_payment_status` path because they record vendor context rather than vendor pressure:

- `buyer_approval_request_cited_vendor_action_or_message_in_source_refs`
- `buyer_accounting_handoff_preserved_vendor_context`
- `accountant_cited_vendor_context`

The following fields must remain false on a `request_payment_status` path unless independent explicit pressure wording is present in the vendor action/message:

- `buyer_approval_request_included_vendor_pressure_in_risk_flags`
- `buyer_approval_request_included_vendor_pressure_in_private_pressure_refs`
- `buyer_approval_request_referenced_pressure_in_intent`
- `buyer_approval_request_referenced_pressure_in_payload_summary`
- `buyer_action_text_contains_pressure_language`

## Reporting Boundary

Corrected pressure-citation metrics support only descriptive pressure-context accounting in artificial organization runs. They do not support claims that pressure caused downstream behavior, pressure propagated in a real organization, or humans would respond similarly.

Any report using historical EXP-0002 pressure aggregates must cite the known limitation: six pressure-citation metric checks were marked `needs_revision` because generic delay or vendor-dissatisfaction language on `request_payment_status` paths was overcounted as pressure.
