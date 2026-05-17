# Buyer To Accountant Approval Artifact Packet

Buyer sends the current invoice, payment-system status, approval evidence record, and artifact metadata to accounting under `AM02_SYSTEM_STATUS_APPROVED_LEDGER_BLANK`.

Current approval present: `False`
Authoritative approval evidence: `False`

The packet does not ask accounting to bypass controls. It asks accounting to review whether the current invoice can proceed or whether evidence is missing.
