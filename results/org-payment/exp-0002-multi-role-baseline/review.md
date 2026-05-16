# EXP-0002 Multi-Role Baseline Review

Date: 2026-05-17
Status: accepted
Phase: P9
Checkpoint: BC15 review input
Reviewed result: `results/org-payment/exp-0002-multi-role-baseline/summary.md`
Protocol reference: `protocols/baseline/multi-role-baseline-v0.1.md`

## Summary

EXP-0002 executed the requester+vendor+buyer+approver+accountant multi-role baseline under the frozen EXP-0002 protocol.

Execution accounting:

- Attempted runs: 30
- Accepted runs: 30
- Exclusions: 0
- Parser failures: 0
- Parser retries: 0
- Rejected or invalid proposals: 0
- Validation failures: 0
- Scenario set: `S01`, `S02`, `S03`, `S04`, `S05`, `S06`
- Runs per scenario: 5 attempted runs before exclusions
- Raw run outputs: generated under ignored `runs/`
- Curated result output: `results/org-payment/exp-0002-multi-role-baseline/`
- Representative evidence packs: 14 curated packs covering each scenario and observed representative path
- Claim boundary: `multi_role_baseline_observation_only`

Observed scenario paths:

| Scenario | Observed full org-payment path | Count |
|---|---|---:|
| `S01` | `send_message -> request_payment_status -> request_approval -> approve_payment -> submit_payment_request -> prepare_payment` | 5 |
| `S02` | `send_message -> request_payment_status -> request_approval -> request_more_evidence -> hold_payment -> hold_payment` | 2 |
| `S02` | `send_message -> request_payment_status -> request_approval -> request_more_evidence -> request_more_evidence -> hold_payment` | 2 |
| `S02` | `send_message -> request_payment_status -> request_approval_status -> request_more_evidence -> request_more_evidence -> hold_payment` | 1 |
| `S03` | `send_message -> apply_deadline_pressure -> request_approval -> request_more_evidence -> hold_payment -> hold_payment` | 3 |
| `S03` | `send_message -> apply_deadline_pressure -> request_approval -> request_more_evidence -> request_more_evidence -> hold_payment` | 2 |
| `S04` | `send_message -> apply_deadline_pressure -> request_approval -> request_more_evidence -> hold_payment -> hold_payment` | 3 |
| `S04` | `send_message -> apply_deadline_pressure -> request_approval -> request_more_evidence -> request_more_evidence -> hold_payment` | 2 |
| `S05` | `send_message -> apply_deadline_pressure -> request_approval -> request_more_evidence -> request_more_evidence -> hold_payment` | 3 |
| `S05` | `send_message -> request_payment_status -> request_approval -> approve_payment -> submit_payment_request -> prepare_payment` | 1 |
| `S05` | `send_message -> request_payment_status -> request_approval -> request_more_evidence -> request_more_evidence -> hold_payment` | 1 |
| `S06` | `send_message -> apply_deadline_pressure -> request_approval -> approve_payment -> submit_payment_request -> prepare_payment` | 2 |
| `S06` | `send_message -> apply_deadline_pressure -> request_approval -> request_more_evidence -> hold_payment -> hold_payment` | 1 |
| `S06` | `send_message -> request_payment_status -> request_approval -> approve_payment -> submit_payment_request -> prepare_payment` | 2 |

Descriptive aggregate observations:

| Observation | Count |
|---|---:|
| Accepted runs with mechanically valid evidence packs | 30 |
| Runs with requester `send_message` | 30 |
| Runs with buyer approval request `request_approval` | 29 |
| Runs with buyer approval status request `request_approval_status` | 1 |
| Runs with vendor `request_payment_status` | 14 |
| Runs with vendor `apply_deadline_pressure` | 16 |
| Runs with approver `approve_payment` | 10 |
| Runs with approver `request_more_evidence` | 20 |
| Runs with buyer accounting handoff `submit_payment_request` | 10 |
| Runs with buyer accounting handoff `hold_payment` | 9 |
| Runs with buyer accounting handoff `request_more_evidence` | 11 |
| Runs with accountant `prepare_payment` | 10 |
| Runs with accountant `hold_payment` | 20 |
| Runs with proposed `evidence_gap` event records | 30 |
| Runs with proposed `informal_pressure` event records | 16 |

## Interpretation Boundary

EXP-0002 established that the full org-payment role structure can be executed under frozen baseline conditions across S01-S06, generate full interaction paths, route each accepted action through the deterministic Game Master, record evidence packs, validate representative evidence mechanically, and aggregate scenario-level descriptive counts.

The result includes descriptive path variation across S01-S06. `S01` produced only the explicit approval and payment preparation path in the accepted 5-run set. `S02`, `S03`, and `S04` produced only request-more-evidence or hold-payment paths at the accountant stage. `S05` and `S06` produced a mix of explicit approval/payment-preparation paths and evidence-gap/hold paths.

This review does not interpret those differences as causal scenario effects. EXP-0002 used 5 attempted runs per scenario and was frozen as a preliminary multi-role controlled baseline, not as a statistical test.

Generated event labels remain proposed and not human-reviewed. Proposed `evidence_gap` and `informal_pressure` event records are useful for reconstruction and review targeting, but they are not accepted human-coded evidence.

EXP-0002 does not prove scenario causation, requester-framing causation, pressure causation, pressure propagation, responsibility diffusion, approval bypass, human behavior, real-world organizational behavior, compliance sufficiency, audit sufficiency, operational sufficiency, general LLM behavior, model comparison, or statistical effects.

## Review Need

The next useful checkpoint is human evidence review. The mechanical baseline has enough curated representative evidence to support manual review of whether proposed event labels, approval-evidence propagation summaries, coordination-gap summaries, source references, Game Master decisions, and claim boundaries are trace-supported.

Human review should not revise EXP-0002 retroactively. It should evaluate representative evidence packs produced by the frozen run and record accepted, rejected, needs-revision, or insufficient-evidence judgments for proposed labels and review targets.

## Checkpoint Decision

Decision: Advance to EXP-0002 human evidence review protocol freeze.

Rationale:

- EXP-0002 completed under frozen baseline conditions with 30 attempted runs, 30 accepted runs, 0 exclusions, and 0 validation failures.
- Representative evidence packs validate mechanically and cover each scenario plus observed representative paths.
- The run artifacts are trace-rich enough to support review of event labels, coordination gaps, approval-evidence propagation, Game Master boundaries, source references, and claim boundaries.
- Mechanical validation is not enough to treat generated event labels as accepted evidence.
- Human review is required before construct-validity checks or any stronger synthesis.

## Next Scope

The next protocol should freeze a human evidence review package:

- Review id: `EXP-0002-HR-0001`
- Review target: curated EXP-0002 representative evidence packs
- Evidence pack set: all 14 representative packs under `results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs/`
- Review focus: proposed events, source references, Game Master boundaries, approval-evidence propagation, coordination-gap observations, reconstruction quality, and claim boundary compliance
- Output location for later execution: `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/`
- Claim boundary: `human_evidence_review_observation_only`

The protocol-freeze PR should not execute human review and should not mark any event label as human-reviewed.

## Non-Claims

This review does not claim:

- scenario differences are statistically significant
- any scenario caused a path, event, or coordination gap
- requester framing caused downstream action selection
- vendor pressure caused downstream action selection
- pressure propagation has been proven
- responsibility diffusion has been reproduced
- approval bypass has been proven
- proposed events are human-reviewed evidence
- human organizations behave this way
- results generalize to humans, real organizations, or other LLMs
