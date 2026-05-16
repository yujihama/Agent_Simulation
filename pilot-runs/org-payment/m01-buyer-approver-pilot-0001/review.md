# M01 Buyer+Approver Pilot Review

Date: 2026-05-16
Status: accepted
Phase: P8
Checkpoint: BC9 next-scope decision
Reviewed result: `pilot-runs/org-payment/m01-buyer-approver-pilot-0001/`
Protocol reference: `protocols/multi-role/multi-role-pilot-v0.1.md`

## Summary

M01 established that buyer+approver LLM interaction can be generated, parsed, routed through the deterministic menu-aware Game Master, and recorded as mechanically valid evidence packs under the frozen artificial organization protocol.

M01 produced some approver-side variation, but no `provide_ambiguous_guidance` path was observed in the curated 5-run pilot.

M01 does not prove responsibility diffusion, human behavior, real-world organizational behavior, causal effects, or statistical effects.

## Run Accounting

| Field | Value |
|---|---:|
| Attempted runs | 5 |
| Accepted runs | 5 |
| Exclusions | 0 |
| Parser failures | 0 |
| Validation failures | 0 |
| Rejected or invalid proposals | 0 |

## Observed Action Counts

Buyer selected:

| Buyer action | Count |
|---|---:|
| `request_approval` | 5 |

Approver selected:

| Approver action | Count |
|---|---:|
| `approve_payment` | 4 |
| `request_more_evidence` | 1 |

Paired paths:

| Buyer -> approver path | Count |
|---|---:|
| `request_approval -> approve_payment` | 4 |
| `request_approval -> request_more_evidence` | 1 |

## Interpretation Boundary

The M01 observation is bounded to:

- artificial organization only
- M01 pilot only
- buyer + approver LLM control only
- requester, accountant, and vendor scripted or rule-based
- deterministic/rule-based Game Master
- generated/proposed event labels that are not human-reviewed coded evidence

M01 does not support:

- statistical significance claims
- human behavior claims
- real-world organization claims
- compliance, legal, audit, or operational sufficiency claims
- model comparison claims
- claims that responsibility diffusion has been reproduced

## Checkpoint Decision

Decision: Advance to M02 buyer+vendor pressure pilot protocol.

Rationale:

- M01 confirmed that multi-role evidence infrastructure works.
- Buyer remained conservative in earlier buyer-only runs and again selected `request_approval` in all M01 runs.
- Vendor pressure is a distinct social input that may affect buyer action selection, `risk_flags`, `source_refs`, `private_pressure_refs`, and justification language.
- M02 should test external pressure propagation before adding more internal roles.

The next useful surface is external pressure propagation: whether a vendor LLM can generate bounded organizational pressure and whether the buyer LLM records or responds to that pressure.

## Next Step

Freeze the M02 buyer+vendor pressure pilot protocol before execution.

M02 execution must happen in a later PR and must not be combined with this review/protocol-freeze checkpoint.
