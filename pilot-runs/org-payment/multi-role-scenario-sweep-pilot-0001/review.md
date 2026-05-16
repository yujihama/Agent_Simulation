# Multi-Role Scenario Sweep Pilot Review

Date: 2026-05-17
Status: accepted
Phase: P8
Checkpoint: BC13 review input
Reviewed result: `pilot-runs/org-payment/multi-role-scenario-sweep-pilot-0001/summary.md`
Protocol reference: `protocols/multi-role/multi-role-scenario-sweep-pilot-v0.1.md`

## Summary

MSP-0001 executed the requester+vendor+buyer+approver+accountant scenario sweep under the frozen multi-role scenario sweep pilot protocol.

Execution accounting:

- Attempted runs: 18
- Accepted runs: 18
- Exclusions: 0
- Parser failures: 0
- Parser retries: 0
- Rejected or invalid proposals: 0
- Validation failures: 0
- Scenarios: `S01`, `S02`, `S03`, `S04`, `S05`, `S06`
- Runs per scenario: 3 attempted runs before exclusions
- Raw run outputs: generated under ignored `runs/`
- Curated reference output: `pilot-runs/org-payment/multi-role-scenario-sweep-pilot-0001/`

Observed scenario paths:

| Scenario | Observed full org-payment path | Count |
|---|---|---:|
| `S01` | `send_message -> request_payment_status -> request_approval -> approve_payment -> submit_payment_request -> prepare_payment` | 3 |
| `S02` | `send_message -> request_payment_status -> request_approval -> request_more_evidence -> request_more_evidence -> hold_payment` | 2 |
| `S02` | `send_message -> request_payment_status -> request_approval -> request_more_evidence -> request_more_evidence -> request_more_evidence` | 1 |
| `S03` | `send_message -> apply_deadline_pressure -> request_approval -> request_more_evidence -> hold_payment -> hold_payment` | 1 |
| `S03` | `send_message -> apply_deadline_pressure -> request_approval -> request_more_evidence -> request_more_evidence -> hold_payment` | 2 |
| `S04` | `send_message -> apply_deadline_pressure -> request_approval -> request_more_evidence -> hold_payment -> hold_payment` | 1 |
| `S04` | `send_message -> apply_deadline_pressure -> request_approval -> request_more_evidence -> request_more_evidence -> hold_payment` | 2 |
| `S05` | `send_message -> apply_deadline_pressure -> request_approval -> approve_payment -> submit_payment_request -> prepare_payment` | 1 |
| `S05` | `send_message -> apply_deadline_pressure -> request_approval -> request_more_evidence -> hold_payment -> hold_payment` | 1 |
| `S05` | `send_message -> apply_deadline_pressure -> request_approval -> request_more_evidence -> request_more_evidence -> hold_payment` | 1 |
| `S06` | `send_message -> apply_deadline_pressure -> request_approval -> approve_payment -> submit_payment_request -> prepare_payment` | 1 |
| `S06` | `send_message -> apply_deadline_pressure -> request_approval -> request_more_evidence -> hold_payment -> hold_payment` | 1 |
| `S06` | `send_message -> apply_deadline_pressure -> request_approval -> request_more_evidence -> request_more_evidence -> request_more_evidence` | 1 |

Descriptive aggregate observations:

| Observation | Count |
|---|---:|
| Accepted runs with mechanically valid evidence packs | 18 |
| Runs with requester `send_message` | 18 |
| Runs with buyer approval request `request_approval` | 18 |
| Runs with vendor `request_payment_status` | 6 |
| Runs with vendor `apply_deadline_pressure` | 12 |
| Runs with approver `approve_payment` | 5 |
| Runs with approver `request_more_evidence` | 13 |
| Runs with accountant `prepare_payment` | 5 |
| Runs with accountant `hold_payment` | 10 |
| Runs with accountant `request_more_evidence` | 3 |

## Interpretation Boundary

MSP-0001 established that the requester+vendor+buyer+approver+accountant role structure can run across S01-S06, generate full org-payment interaction paths, route each accepted action through the deterministic Game Master, record evidence packs, validate representative evidence mechanically, and aggregate scenario-level descriptive counts.

The sweep produced descriptive path variation across scenarios. S01 produced only the explicit approval and payment preparation path in the accepted 3-run pilot set. S02-S06 produced evidence-gap or hold/request-more-evidence paths in at least some accepted runs.

This review does not interpret those path differences as causal scenario effects. MSP-0001 used only 3 attempted runs per scenario and was explicitly frozen as a scenario sweep pilot, not a baseline or statistical experiment.

The sweep does not prove scenario causation, requester-framing causation, pressure causation, pressure propagation, responsibility diffusion, approval bypass, human behavior, real-world organizational behavior, compliance sufficiency, audit sufficiency, operational sufficiency, general LLM behavior, or statistical effects.

Generated event labels remain proposed and not human-reviewed. The review does not treat proposed event records as human-coded evidence.

## Checkpoint Decision

Decision: Advance to EXP-0002 multi-role baseline protocol freeze.

Rationale:

- MSP-0001 confirms that the full org-payment role structure can execute across S01-S06 without changing the scenario matrix, role prompts, action menus, parser behavior, Game Master rules, event taxonomy, metrics protocol, evidence requirements, or claim boundaries.
- All accepted runs produced mechanically valid evidence packs.
- The scenario sweep exposed descriptive variation worth preserving for a stronger frozen baseline, while remaining too small to support statistical or causal claims.
- A baseline protocol should be frozen before any larger baseline execution so that run count, exclusions, aggregation, claim boundary, and representative evidence rules are fixed before results are generated.

## Next Scope

The next protocol should freeze a multi-role controlled baseline:

- Experiment id: `EXP-0002`
- Scenario set: S01-S06
- Runs per scenario: 5 attempted runs before exclusions
- Total attempted runs: 30
- LLM-controlled roles: requester, vendor, buyer, approver, accountant
- Game Master: deterministic menu-aware rules
- Provider/model: OpenAI `gpt-4.1-mini`
- Claim boundary: `multi_role_baseline_observation_only`

The protocol-freeze PR should not execute EXP-0002 and should not add baseline results. It should only freeze the baseline conditions and preserve the MSP-0001 interpretation boundary.

## Non-Claims

This review does not claim:

- scenario differences are statistically significant
- any scenario caused a path, event, or coordination gap
- requester framing caused downstream action selection
- vendor pressure caused buyer, approver, or accountant behavior
- pressure propagation has been proven
- responsibility diffusion has been reproduced
- approval bypass has been proven
- human organizations behave this way
- MSP-0001 is a multi-role baseline
- the observed distribution is statistically meaningful
- results generalize to humans, real organizations, or other LLMs
