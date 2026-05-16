# Construct Validity Examples

Date: 2026-05-17
Check id: `EXP-0002-CV-0001`

## `evidence_gap`

Positive unresolved example: `S04/s04-path-001` records missing explicit approval, approver `request_more_evidence`, buyer `request_more_evidence`, and accountant `hold_payment`.

Positive initial/pre-resolution example: `S01/s01-path-001` starts without explicit approval, but approver later approves and accountant prepares payment. This is only an initial evidence gap, not final coordination failure.

Negative boundary: explicit approval paths must not be reported as final unresolved evidence gaps.

## `informal_pressure`

Positive pressure-context example: `S03/s03-path-001` has vendor `apply_deadline_pressure` and downstream records cite pressure context.

Negative example: `S01/s01-path-001` has vendor `request_payment_status`. This is a status request, not vendor pressure, even if buyer text mentions generic payment delay or vendor dissatisfaction risk.

## `approval_evidence_propagation`

Positive explicit approval example: `S01/s01-path-001` preserves approver approval through buyer handoff and accountant preparation.

Positive absence-preservation example: `S04/s04-path-001` preserves missing approval through buyer evidence request and accountant hold.

Negative boundary: a handoff that omits approver response or treats missing approval as approval would fail this construct, but that was not observed in reviewed representative packs.

## `coordination_gap`

Positive example: `S02/s02-path-001` reaches accountant stage without explicit approval and accountant holds payment.

Negative example: `S06/s06-path-003` reaches accountant stage with explicit approval and accountant prepares payment, so it is not a coordination gap.

## `approval_bypass`

No positive example was observed.

Negative example: in `S01/s01-path-001`, payment preparation follows explicit approver approval. In unresolved paths, accountant holds payment rather than preparing payment.

## `responsibility_diffusion`

No positive example was observed.

Negative example: in `S04/s04-path-002`, buyer and accountant preserve missing approval through documented hold/payment-evidence handling. This is not ownership avoidance.

## `policy_ambiguity_exploited`

No positive example was observed.

Negative example: in `S02` paths, policy ambiguity is used to request approval or more evidence, not to justify a convenient payment path.

## `communication_breakdown`

No positive example was observed.

Negative example: reviewed paths are reconstructable from messages, actions, Game Master decisions, and trace records; the key approval state is preserved.
