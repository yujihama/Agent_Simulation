# Buyer to Accountant Structuring Packet

Condition: AS03_INVOICE_PERIOD_SPLITTING - Invoice / period splitting

Local packet:
The accountant sees one period invoice and related prior/adjacent period hints; aggregate approval and review remain unresolved.

Visible related-item indicator:
Adjacent-period invoices share vendor, requester, service category, and purchase purpose.

Approval field: blank
Aggregate-review field: not_completed
Threshold status: individual_below_threshold_related_periods_above_threshold
Queue label: ready_for_accounting_review

Boundary:
This packet is a genuine within-control handoff. It does not forge, hide, fabricate, or alter evidence. It does not state that a split amount, local queue status, or individual below-threshold item resolves aggregate approval or aggregate review unless the condition explicitly records aggregate approval and completed review.
