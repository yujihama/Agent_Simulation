# M02 Buyer+Vendor Pressure Pilot Review

Date: 2026-05-16
Status: accepted
Phase: P8
Checkpoint: BC10
Protocol reference: `protocols/multi-role/m02-buyer-vendor-pressure-pilot-v0.1.md`
Reviewed result: `pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/aggregate.json`

## Summary

M02 established that vendor pressure can be generated, parsed, routed through the Game Master, recorded as evidence, and cited by the buyer under the frozen artificial org-payment pressure pilot protocol.

M02 showed pressure-citation behavior in all included runs. It did not show buyer action-selection variation: the buyer selected `request_approval` in all included runs.

This review does not claim that vendor pressure caused buyer behavior. It does not claim pressure propagation in human organizations. It does not make statistical, human behavior, real-world organization, compliance, legal, audit, or operational claims.

## Protocol Reference

| Field | Value |
|---|---|
| Protocol | `protocols/multi-role/m02-buyer-vendor-pressure-pilot-v0.1.md` |
| Pilot id | `M02` |
| Scenario | `S04` |
| LLM-controlled roles | `vendor`, `buyer` |
| Scripted or rule-based roles | `requester`, `approver`, `accountant` |
| Game Master | `deterministic_menu_aware_rules` |
| Provider/model | OpenAI `gpt-4.1-mini` |
| Claim boundary | `multi_role_pressure_pilot_observation_only` |

## Execution Accounting

| Measure | Count |
|---|---:|
| Attempted runs | 5 |
| Accepted runs | 5 |
| Exclusions | 0 |
| Parser failures | 0 |
| Validation failures | 0 |
| Rejected or invalid proposals | 0 |

## Observed Actions

### Vendor

| action_type | count |
|---|---:|
| `apply_deadline_pressure` | 5 |

### Buyer

| action_type | count |
|---|---:|
| `request_approval` | 5 |

### Paired Paths

| paired path | count |
|---|---:|
| `apply_deadline_pressure -> request_approval` | 5 |

## Pressure-Citation Accounting

| Field | Count |
|---|---:|
| Buyer cited vendor action/message in `source_refs` | 5 |
| Buyer included vendor pressure in `risk_flags` | 5 |
| Buyer included vendor pressure in `private_pressure_refs` | 5 |
| Buyer referenced pressure in `intent` | 5 |
| Buyer referenced pressure in `payload_summary` | 5 |

## Interpretation

M02 is a valid pressure pilot result. Vendor pressure was generated and recorded, and buyer responses cited that pressure in the action proposal fields tracked by the frozen protocol.

M02 does not show that vendor pressure changed buyer action selection. The buyer selected `request_approval` in all included runs, matching the conservative buyer pattern observed in earlier buyer-only and multi-role pilots.

The next useful surface is internal coordination: whether approval status, ambiguous guidance, or evidence gaps are preserved or distorted when the case moves from buyer and approver records to accountant handling.

## Checkpoint Decision

Decision: Advance to M03 buyer+approver+accountant coordination pilot protocol.

Rationale:

- EXP-0001 showed buyer-only baseline stability.
- M01 showed buyer+approver multi-role execution works.
- M02 showed external vendor pressure can be captured and cited, but buyer action remained conservative.
- M03 should test the next institutional boundary: whether approval evidence and unresolved gaps are correctly transmitted to accounting.
- M03 is needed before expanding to full org-payment multi-role simulation.

## Claim Boundary

This review is limited to M02 pressure-pilot review and next-scope selection.

It does not claim:

- vendor pressure caused buyer behavior
- pressure propagation has been proven
- responsibility diffusion has been reproduced
- human organizations behave this way
- S04 causes risky behavior
- this is a multi-role baseline
- this proves institutional failure
- this is statistically meaningful
- this generalizes to humans or real organizations
