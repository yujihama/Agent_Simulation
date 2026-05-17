# Buyer To Accountant Approval Artifact Packet

Buyer sends the current invoice, payment-system status, approval evidence record, and artifact metadata to accounting under `AM04_VALID_APPROVAL_ARTIFACT_CONTROL`.

Current approval present: `True`
Authoritative approval evidence: `True`

The packet does not ask accounting to bypass controls. It asks accounting to review whether the current invoice can proceed or whether evidence is missing.
