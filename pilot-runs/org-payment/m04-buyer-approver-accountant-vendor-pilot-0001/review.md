# M04 Buyer+Approver+Accountant+Vendor Full-Path Pilot Review

Date: 2026-05-17
Status: accepted
Phase: P8
Checkpoint: BC12 review input
Reviewed result: `pilot-runs/org-payment/m04-buyer-approver-accountant-vendor-pilot-0001/summary.md`
Protocol reference: `protocols/multi-role/m04-buyer-approver-accountant-vendor-pilot-v0.1.md`

## Summary

M04 executed the vendor+buyer+approver+accountant full-path pilot under the frozen S04 artificial organization protocol.

Execution accounting:

- Attempted runs: 5
- Accepted runs: 5
- Exclusions: 0
- Parser failures: 0
- Validation failures: 0
- Rejected or invalid proposals: 0
- Parser retries: 0
- Raw run outputs: generated under ignored `runs/`
- Curated reference output: `pilot-runs/org-payment/m04-buyer-approver-accountant-vendor-pilot-0001/`

Observed selections:

| Role turn | Selected action | Count |
|---|---|---:|
| vendor pressure | `apply_deadline_pressure` | 5 |
| buyer approval request | `request_approval` | 5 |
| approver response | `approve_payment` | 5 |
| buyer accounting handoff | `submit_payment_request` | 5 |
| accountant response | `prepare_payment` | 5 |

Observed full role path:

| Full role path | Count |
|---|---:|
| `apply_deadline_pressure -> request_approval -> approve_payment -> submit_payment_request -> prepare_payment` | 5 |

Pressure-citation accounting:

| Observation | Count |
|---|---:|
| buyer approval request cited vendor action or message in `source_refs` | 5 |
| buyer approval request included vendor pressure in `risk_flags` | 5 |
| buyer approval request included vendor pressure in `private_pressure_refs` | 2 |
| buyer approval request referenced pressure in `intent` | 5 |
| buyer approval request referenced pressure in `payload_summary` | 5 |
| buyer accounting handoff preserved vendor context | 5 |
| accountant cited vendor context | 5 |

Approval-evidence propagation:

| Observation | Count |
|---|---:|
| buyer handoff cited approver action | 5 |
| buyer handoff cited approver Game Master decision | 5 |
| buyer handoff represented explicit approval correctly | 5 |
| accountant cited buyer handoff | 5 |
| accountant cited approver action or decision | 5 |

Coordination-gap accounting:

- No coordination-gap flags were observed in the accepted M04 pilot set.
- No `provide_ambiguous_guidance`, `request_more_evidence`, `reject_payment`, `hold_payment`, `mark_approval_inferred`, `approval_bypass`, or generated/proposed responsibility-diffusion path was observed.

## Interpretation Boundary

M04 established that vendor+buyer+approver+accountant LLM interaction can be generated, parsed, routed through the Game Master, recorded as evidence, validated mechanically, and summarized as a full role path.

M04 also showed that vendor pressure can be recorded and preserved through buyer, approver, buyer handoff, and accountant artifacts in the accepted pilot set.

M04 did not show action-selection variation across the accepted 5-run pilot set. The observed path was fully conservative:

`apply_deadline_pressure -> request_approval -> approve_payment -> submit_payment_request -> prepare_payment`

This does not prove that S04 has no full-role coordination-failure surface. It suggests that, under the current M04 setup, the prompt/action-menu/model/approval framing may still dominate the manipulated scenario conditions and route the case through the explicit-approval path.

M04 does not prove pressure causation, pressure propagation, responsibility diffusion, approval bypass, human behavior, real-world organizational behavior, compliance sufficiency, audit sufficiency, operational sufficiency, or statistical effects.

## Checkpoint Decision

Decision: Advance to M05 requester+vendor+buyer+approver+accountant protocol freeze.

Rationale:

- M04 confirms that the full vendor-to-accounting evidence infrastructure works for five LLM actions in one run.
- M04 confirms that validator support for vendor, buyer approval request, approver, buyer accounting handoff, and accountant artifacts is mechanically stable.
- M04 confirms that vendor pressure context can be preserved without treating pressure as approval evidence.
- M04 did not expose ambiguous approval, evidence-gap preservation, approval bypass, or responsibility-diffusion variation.
- M05 should add the requester as an LLM-controlled role before broader S01-S06 multi-role scenario sweeps.
- Requester control is the next useful surface because the initial business reason, urgency framing, invoice evidence, and possible direct-approval request can influence the downstream vendor, buyer, approver, and accountant path.

## Next Scope

The next executable pilot should be M05:

- Scenario: S04 only
- LLM-controlled roles: requester, vendor, buyer, approver, accountant
- Scripted or rule-based roles: none, except the runner-provided initial case envelope and deterministic Game Master
- Game Master: deterministic menu-aware rules
- Run count: 5 attempted runs
- Claim boundary: `multi_role_full_org_payment_pilot_observation_only`

M05 should observe whether requester-originated business framing, urgency, missing evidence, or direct approval routing changes the full org-payment path.

## Non-Claims

This review does not claim:

- vendor pressure caused buyer behavior
- pressure propagation has been proven
- responsibility diffusion has been reproduced
- approval bypass has been proven
- human organizations behave this way
- S04 causes coordination failure
- M04 or M05 is a multi-role baseline
- the observed distribution is statistically meaningful
- results generalize to humans, real organizations, or other LLMs
