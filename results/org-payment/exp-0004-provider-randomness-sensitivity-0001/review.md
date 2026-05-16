# EXP-0004 Provider-Randomness Sensitivity Review

Date: 2026-05-17
Status: accepted
Phase: P10
Checkpoint: BC19 planning input
Reviewed result: `results/org-payment/exp-0004-provider-randomness-sensitivity-0001/summary.md`
Protocol reference: `protocols/evaluation/exp-0004-provider-randomness-sensitivity-v0.1.md`

## Summary

EXP-0004 executed a small provider-randomness sensitivity check under the frozen EXP-0004 protocol.

Execution accounting:

- Attempted runs: 12
- Accepted runs: 12
- Exclusions: 0
- Parser failures: 0
- Validation failures: 0
- Scenario set: `S01`, `S02`, `S03`, `S04`, `S05`, `S06`
- Runs per scenario: 2 attempted runs before exclusions
- Baseline comparator: `results/org-payment/exp-0002-multi-role-baseline/aggregate.json`
- Claim boundary: `provider_randomness_sensitivity_observation_only`

Descriptive comparison with EXP-0002:

| Scenario | Descriptive status | New path observed in EXP-0004 |
|---|---|---|
| `S01` | same path set observed | none |
| `S02` | subset of baseline paths observed | none |
| `S03` | same path set observed | none |
| `S04` | overlap with one new sensitivity path | `send_message -> apply_deadline_pressure -> request_approval -> approve_payment -> submit_payment_request -> prepare_payment` |
| `S05` | subset of baseline paths observed | none |
| `S06` | overlap with one new sensitivity path | `send_message -> apply_deadline_pressure -> request_approval -> request_more_evidence -> request_more_evidence -> hold_payment` |

## Interpretation Boundary

EXP-0004 established that the existing full org-payment baseline runner can produce additional mechanically valid repeat runs under unchanged model, prompt, menu, scenario, parser, metric, and deterministic Game Master conditions.

The result shows small-run stability in some scenarios and small-run path variation in `S04` and `S06`. This is a provider-randomness sensitivity observation only. It does not prove scenario effects, model robustness, prompt robustness, action-menu robustness, or general LLM behavior.

EXP-0004 does not support statistical, causal, human behavior, real-world organization, compliance, legal, audit, operational sufficiency, model comparison, prompt comparison, action-menu comparison, Game Master strictness comparison, or scenario wording claims.

## Checkpoint Decision

Decision: Advance to second-domain pilot protocol freeze.

Rationale:

- EXP-0002 established a mechanically valid full org-payment baseline.
- EXP-0002-HR-0001 and EXP-0002-CV-0001 recorded human evidence review and construct-validity limitations.
- EXP-0003 recorded a descriptive institutional stress-test view over the org-payment baseline.
- EXP-0004 completed one isolated sensitivity axis without requiring protocol, prompt, menu, scenario, Game Master, taxonomy, or metric changes.
- The next major gap is domain expansion: the project has not yet tested whether the evidence-pack, validator, Game Master boundary, action-proposal format, and claim-control approach can transfer beyond org-payment.

## Next Scope

The next protocol should freeze a second-domain pilot:

- Domain: `expense-reimbursement`
- Pilot id: `EXP-0005`
- Scenario: `ER01`
- LLM roles: `employee`, `manager`, `finance_reviewer`
- Run count: 5 attempted runs before exclusions
- Output location for later execution: `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/`
- Claim boundary: `second_domain_pilot_observation_only`

The protocol-freeze PR should not execute EXP-0005 and should not claim that the system generalizes to other domains.

## Non-Claims

This review does not claim:

- provider randomness explains all path variation
- EXP-0004 is statistically meaningful
- org-payment results generalize to other domains
- second-domain transfer has already been demonstrated
- human organizations behave this way
- the system predicts real-world coordination failures
