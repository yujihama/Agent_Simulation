# M05 Full Org-Payment Multi-Role Pilot Review

Date: 2026-05-17
Status: accepted
Phase: P8
Checkpoint: BC12 review input
Reviewed result: `pilot-runs/org-payment/m05-full-org-payment-pilot-0001/summary.md`
Protocol reference: `protocols/multi-role/m05-full-org-payment-pilot-v0.1.md`

## Summary

M05 executed the first full org-payment pilot under the frozen S04 artificial organization protocol with requester, vendor, buyer, approver, and accountant all LLM-controlled through constrained role-turn menus.

Execution accounting:

- Attempted runs: 5
- Accepted runs: 5
- Exclusions: 0
- Parser failures: 0
- Parser retries: 0
- Rejected or invalid proposals: 0
- Validation failures: 0
- Raw run outputs: generated under ignored `runs/`
- Curated reference output: `pilot-runs/org-payment/m05-full-org-payment-pilot-0001/`

Observed selections:

| Role turn | Selected action | Count |
|---|---|---:|
| requester case initiation | `send_message` | 5 |
| vendor pressure | `apply_deadline_pressure` | 5 |
| buyer approval request | `request_approval` | 5 |
| approver response | `approve_payment` | 2 |
| approver response | `request_more_evidence` | 3 |
| buyer accounting handoff | `submit_payment_request` | 2 |
| buyer accounting handoff | `hold_payment` | 3 |
| accountant response | `prepare_payment` | 2 |
| accountant response | `hold_payment` | 3 |

Observed full org-payment paths:

| Full path | Count |
|---|---:|
| `send_message -> apply_deadline_pressure -> request_approval -> approve_payment -> submit_payment_request -> prepare_payment` | 2 |
| `send_message -> apply_deadline_pressure -> request_approval -> request_more_evidence -> hold_payment -> hold_payment` | 3 |

Descriptive accounting:

| Observation | Count |
|---|---:|
| requester sent buyer-facing message | 5 |
| vendor selected pressure action | 5 |
| buyer approval request cited vendor action or message in `source_refs` | 5 |
| buyer accounting handoff preserved vendor context | 5 |
| accountant cited vendor context | 5 |
| explicit approval absent at accountant stage | 3 |
| accountant held payment due to missing evidence | 3 |

## Interpretation Boundary

M05 established that full requester+vendor+buyer+approver+accountant LLM interaction can be generated, parsed, routed through the deterministic Game Master, recorded as evidence, validated mechanically, and summarized as full org-payment paths.

M05 produced two observed paths in the accepted 5-run pilot set. The variation occurred at the approver, buyer accounting-handoff, and accountant stages:

- explicit approval path: `approve_payment -> submit_payment_request -> prepare_payment`
- evidence-gap path: `request_more_evidence -> hold_payment -> hold_payment`

M05 did not observe requester action variation, vendor action variation, buyer approval-request variation, ambiguous approval guidance, approval bypass, or generated/proposed responsibility-diffusion paths.

M05 does not prove that requester framing, vendor pressure, S04 conditions, or any scenario variable caused the observed paths. It does not prove pressure propagation, responsibility diffusion, approval bypass, human behavior, real-world organizational behavior, compliance sufficiency, audit sufficiency, operational sufficiency, general LLM behavior, or statistical effects.

## Checkpoint Decision

Decision: Advance to BC12 multi-role scenario sweep pilot protocol.

Rationale:

- M05 confirms that full org-payment evidence infrastructure works for five LLM-controlled roles in one scenario.
- M05 confirms that requester, vendor, buyer, approver, buyer handoff, and accountant artifacts can be mechanically validated.
- M05 produced some downstream path variation after the approver response, while preserving claim boundaries.
- S04-only execution cannot distinguish whether path variation is scenario-specific or driven by the shared prompt/action-menu/model framing.
- A small S01-S06 pilot sweep is the next useful step before any multi-role baseline protocol.

## Next Scope

The next executable pilot should be a scenario sweep:

- Scenario set: S01-S06
- Role structure: M05 full org-payment role structure
- Runs per scenario: 3 attempted runs before exclusions
- Total attempted runs: 18
- LLM-controlled roles: requester, vendor, buyer, approver, accountant
- Game Master: deterministic menu-aware rules
- Provider/model: OpenAI `gpt-4.1-mini`
- Claim boundary: `multi_role_scenario_sweep_pilot_observation_only`

The scenario sweep should observe whether path distributions, event candidates, and coordination-gap observations can be generated and compared descriptively across S01-S06 without statistical, causal, human behavior, or real-world claims.

## Non-Claims

This review does not claim:

- requester framing caused downstream action selection
- vendor pressure caused buyer, approver, or accountant behavior
- pressure propagation has been proven
- responsibility diffusion has been reproduced
- approval bypass has been proven
- S04 caused the observed path split
- human organizations behave this way
- M05 or the next sweep is a multi-role baseline
- the observed distribution is statistically meaningful
- results generalize to humans, real organizations, or other LLMs
