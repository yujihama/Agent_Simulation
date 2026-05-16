# EXP-0005 Expense Reimbursement Second-Domain Pilot Review

Date: 2026-05-17
Status: accepted
Phase: P10
Checkpoint: BC20 synthesis input
Reviewed result: `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/summary.md`
Protocol reference: `protocols/domain-expansion/expense-reimbursement-pilot-v0.1.md`

## Summary

EXP-0005 executed the frozen expense-reimbursement second-domain pilot for `ER01`.

Execution accounting:

- Attempted runs: 5
- Accepted runs: 5
- Exclusions: 0
- Parser failures: 0
- Validation failures: 0
- Scenario: `ER01`
- LLM roles: `employee`, `manager`, `finance_reviewer`
- Game Master: `deterministic_menu_aware_rules`
- Claim boundary: `second_domain_pilot_observation_only`

Observed path:

| Path | Count |
|---|---:|
| `request_approval -> request_more_evidence -> hold_payment` | 5 |

Observed descriptive summaries:

- Employee selected `request_approval` in all included runs.
- Manager selected `request_more_evidence` in all included runs.
- Finance reviewer selected `hold_payment` in all included runs.
- Representative evidence pack validation: PASS.
- Approval-evidence propagation summary records finance citing manager action or decision in all included runs.
- Evidence-gap summary records proposed evidence-gap event, manager request for more evidence, and finance hold in all included runs.

## Interpretation Boundary

EXP-0005 established that the existing action-proposal, parser, Game Master decision, trace, evidence-pack, validator, and aggregate-reporting structure can produce a mechanically valid second-domain pilot artifact for an expense-reimbursement scenario.

EXP-0005 does not establish cross-domain generalization. It uses one scenario, one run set, one model, one prompt set, and one deterministic Game Master structure. It is a transfer pilot, not a second-domain baseline.

Generated event labels remain proposed and not human-reviewed. The result does not support statistical, causal, human behavior, real-world organization, compliance, legal, audit, operational sufficiency, model comparison, or general LLM behavior claims.

## Checkpoint Decision

Decision: Advance to BC20 social-chaos claim synthesis protocol freeze.

Rationale:

- Org-payment has baseline, human review, construct-validity, intervention, and sensitivity artifacts.
- EXP-0005 provides one bounded second-domain transfer pilot.
- The project now has enough staged evidence to synthesize what can and cannot be claimed.
- The synthesis must preserve failures and limitations: stable paths, small samples, generated events, limited human review, one second-domain pilot, and no real-world validation.

## Next Scope

The next protocol should freeze BC20 synthesis inputs, claim levels, excluded claims, and output artifacts before writing the synthesis.

The synthesis should not add new runs, revise scenarios, revise metrics, revise event taxonomy, or upgrade generated/proposed event labels to human-reviewed evidence.

## Non-Claims

This review does not claim:

- expense reimbursement validates org-payment findings
- the project generalizes across domains
- ER01 is representative of expense reimbursement
- event labels are human-reviewed for EXP-0005
- human organizations behave this way
- real-world institutional failures can be predicted
