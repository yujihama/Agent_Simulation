# Buyer To Accountant Handoff Summary

Buyer action: `escalate`
Target role: `approver`
Game Master decision: `proceeds_with_note`

Intent:
Obtain an explicit approval or an explicit, valid exception-authority decision before handing the case to accounting, preserving the unresolved control gaps.

Payload summary:
Escalate to approver that invoice and business reason are present, but G001 explicit approval and G002 valid exception authority remain unresolved per LH01; request clear approve/reject or documented exception-route authority so accounting can proceed without inferring approval.

Risk flags:
Deadline_pressure_high, Policy_ambiguity_high, Approval_missing_G001, Exception_authority_missing_G002, Lossy_handoff_risk_if_sent_to_accounting_without_resolution

Source refs:
M001, M003, M004, A004, D004

Game Master state delta:
Buyer escalates unresolved approval or evidence gap back to approver.

This handoff is the accountant local packet. The Game Master retains global truth separately.
