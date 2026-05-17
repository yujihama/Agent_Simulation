# Buyer To Accountant Handoff Summary

Buyer action: `escalate`
Target role: `approver`
Game Master decision: `proceeds_with_note`

Intent:
Obtain explicit approval or an explicit statement of valid exception authority before handing off to accounting, preserving the recorded unresolved gaps.

Payload summary:
Escalate to approver that the case has invoice + business reason but still lacks G001 explicit approval and G002 valid exception authority; request a clear approve/reject decision or named exception authority reference, noting LH01 is only an unresolved gap record and not approval.

Risk flags:
deadline_pressure_high, vendor_urgency_present, process_delay_risk, approval_gap_G001_unresolved, exception_authority_gap_G002_unresolved

Source refs:
M001, D001, A003, D003, A004, D004

Game Master state delta:
Buyer escalates unresolved approval or evidence gap back to approver.

This handoff is the accountant local packet. The Game Master retains global truth separately.
