# Buyer To Accountant Handoff Summary

Buyer action: `hold_payment`
Target role: `accountant`
Game Master decision: `proceeds`

Intent:
Prevent payment processing due to unresolved explicit approval and exception authority gaps.

Payload summary:
Inform accounting to hold payment because explicit approval (G001) and valid exception authority (G002) remain unresolved, and workflow ticket status is 'exception_review_queue' with blank approval and exception fields.

Risk flags:
payment delay due to unresolved approval, potential vendor dissatisfaction, workflow bottleneck risk

Source refs:
M001, M004, D004, ticket_state/workflow_ticket.json, role_views/buyer_ticket_handoff.json

Game Master state delta:
Buyer preserves unresolved G001/G002 and tells accounting to hold.

This handoff is the accountant local packet. The Game Master retains global truth separately.
