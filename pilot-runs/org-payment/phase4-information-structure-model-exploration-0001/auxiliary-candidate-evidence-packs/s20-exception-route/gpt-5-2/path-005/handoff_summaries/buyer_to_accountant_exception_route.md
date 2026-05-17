# Buyer To Accountant Handoff Summary

Buyer action: `escalate`
Target role: `approver`
Game Master decision: `proceeds_with_note`

Intent:
Obtain explicit approver confirmation (approve/reject) or documented valid exception authority before any accounting handoff, preserving the recorded unresolved gaps.

Payload summary:
Escalate to approver referencing ER05: ticket has an exception-review tag but approval and exception authority fields are blank; request explicit approval decision or explicit delegation/exception authority documentation; note invoice and business reason are present but G001 explicit approval and G002 valid exception authority remain unresolved.

Risk flags:
Approval missing/unresolved (G001) could block payment processing., Exception authority missing/unresolved (G002) could block exception routing as authorization., Delay risk if approver cannot promptly clarify; however preserves control boundary by not inferring approval.

Source refs:
M001, M004, A003, A004, D004

Game Master state delta:
Buyer escalates unresolved approval or evidence gap back to approver.

This handoff is the accountant local packet. The Game Master retains global truth separately.
