# Social Chaos Claim Synthesis Limitations

Date: 2026-05-17
Status: accepted
Protocol: `protocols/synthesis/social-chaos-claim-synthesis-v0.1.md`

## Scope Limits

- The project studies artificial organizations, not human society directly.
- The primary executed domain is org-payment.
- The second domain is limited to one expense-reimbursement pilot scenario, ER01.
- The artifacts use fixed protocols, prompts, action menus, parser rules, metrics, and deterministic Game Master handling for each frozen execution.

## Evidence Limits

- EXP-0002 has 30 accepted org-payment baseline runs, with 5 attempted runs per S01-S06 scenario.
- EXP-0002 human review covers 14 curated representative packs, not all raw runs.
- EXP-0002 human review has one primary reviewer, no secondary reviewer, no adjudication, and no inter-rater reliability claim.
- EXP-0003 adds no new LLM execution.
- EXP-0004 has 12 accepted repeat runs and tests only provider randomness under fixed conditions.
- EXP-0005 has 5 accepted ER01 runs and no human review.

## Construct Limits

- `evidence_gap`, `approval_evidence_propagation`, and `coordination_gap` are supported only for reviewed EXP-0002 representative-pack descriptions.
- `informal_pressure` is partially supported as pressure-context evidence only.
- Pressure context must not be interpreted as pressure causation.
- `approval_bypass`, `responsibility_diffusion`, `policy_ambiguity_exploited`, and `communication_breakdown` were not observed in reviewed EXP-0002 representative packs.
- Generated/proposed event labels outside reviewed scope remain generated/proposed only.

## Method Limits

- The Game Master is deterministic and rule-based; this supports traceability but does not represent all possible institutional adjudication.
- LLM action choices are constrained by prompt templates and action menus.
- Provider randomness is not explicitly seeded or fully controlled.
- There is no model comparison.
- There is no prompt sensitivity test.
- There is no action-menu sensitivity test.
- There is no Game Master strictness sensitivity test.
- There is no scenario-wording sensitivity test.

## Statistical Limits

- No inferential statistical tests are performed.
- No statistical significance claim is supported.
- Counts are denominator-explicit descriptive counts only.
- Small repeated-run pilots and sensitivity checks should not be treated as behavioral distributions.

## External Validity Limits

- No human behavior claim is supported.
- No real-world organization claim is supported.
- No compliance, legal, audit, operational, safety, or governance sufficiency claim is supported.
- No prediction of real institutional failure is supported.
- No cross-domain generalization claim is supported.
- No general LLM behavior claim is supported.

## Reporting Limits

- The synthesis can summarize what happened in committed artificial-system artifacts.
- The synthesis can state hypotheses for future validation.
- The synthesis cannot upgrade generated labels, pilot observations, or descriptive contrasts into real-world conclusions.
- Future reports must preserve the EXP-0002 pressure-citation correction when discussing vendor context and vendor pressure.
