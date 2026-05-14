# Claim Boundaries v0.1

Date: 2026-05-14
Status: accepted
Phase: P3
Step: P3 evaluation protocol bundle
Covers: C16, C18, C20
Supersedes: none
Related ADR: ADR-0001, ADR-0002, ADR-0003

## Purpose

Claim Boundaries v0.1 defines how this project should phrase observations, patterns, hypotheses, claims, and limitations from artificial organization runs.

The goal is to keep reporting aligned with evidence quality and to avoid presenting LLM-generated behavior as direct proof about human society.

## Statement Classes

| Class | Meaning | Minimum support |
|---|---|---|
| Observation | Something visible in a specific run. | Traceable evidence pack reference. |
| Pattern | A repeated observation across runs or scenario conditions. | Multiple reviewed runs or a documented dry-run set. |
| Hypothesis | A plausible explanation or research direction suggested by patterns. | Pattern evidence plus explicit uncertainty. |
| Claim | A bounded conclusion supported by reviewed evidence and protocol checks. | Reviewed evidence, metrics, limitations, and appropriate comparison. |
| Limitation | Something the evidence cannot support. | Clear statement of missing evidence, scope, or validity gap. |

## Permitted Early Reporting

Before repeated dry runs and review reliability checks exist, reporting should stay at the level of:

- protocol readiness
- scenario design rationale
- single-run observations
- dry-run reconstruction findings
- candidate patterns clearly marked as exploratory
- limitations and next validation steps

## Not Permitted

The project must not claim that artificial-run output directly proves:

- how real employees, managers, auditors, or vendors behave
- that a real organization would experience the same failure
- that a model is socially accurate in general
- that a policy or control is legally or operationally sufficient
- that metrics establish real-world causal effects without additional validation

## Claim Strength Rules

| Wording strength | Use when | Avoid when |
|---|---|---|
| "In this run..." | A single evidence pack supports the statement. | Discussing broader tendencies. |
| "Across these reviewed runs..." | Multiple reviewed runs show the same pattern. | Review or reconstruction is incomplete. |
| "This suggests..." | Evidence motivates a hypothesis but does not establish it. | The statement is presented as settled. |
| "This supports the bounded claim that..." | Evidence, comparison, review, and limitations are all documented. | The claim extends beyond the artificial organization. |
| "This does not show..." | A limitation or non-claim must be explicit. | The statement is used to hide missing evidence. |

## Required Claim Context

Any report that includes patterns, hypotheses, or claims should state:

- scenario ids
- run ids or run set
- protocol versions
- event taxonomy version
- metrics version
- evidence pack version
- human review status
- known missing evidence
- whether the statement concerns artificial-run behavior only

## Ethics and Misuse Boundary

Artificial organization runs may be useful for hypothesis generation, protocol testing, and controlled comparison of simulated institutional conditions. They are not a substitute for empirical human-subject research, legal review, compliance review, or organizational audit.

Reports should avoid language that could be used to:

- profile real workers or groups
- justify surveillance or punitive controls without external evidence
- sell a compliance guarantee
- imply that LLM agents faithfully represent human populations
- obscure the role of model choice, prompt design, and Game Master decisions

## Version Boundary

Claim Boundaries v0.1 is sufficient for early review and dry-run reporting. It should be revisited after the first reconstructed dry runs and before baseline experiment results are reported.
