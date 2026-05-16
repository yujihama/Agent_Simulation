# EXP-0003 Intervention Validity Stress Test Protocol v0.1

Date: 2026-05-17
Status: accepted
Phase: P9
Checkpoint: BC17
Covers: C11, C14, C16, C18, C20
Supersedes: none
Related baseline: `protocols/baseline/multi-role-baseline-v0.1.md`
Related correction: `protocols/evaluation/pressure-citation-metric-correction-v0.1.md`

## Purpose

This document freezes the EXP-0003 intervention validity stress test before any EXP-0003 result synthesis is recorded.

EXP-0003 asks whether the accepted org-payment scenario matrix can support a bounded, descriptive comparison of institutional conditions after EXP-0002. It is not a new LLM execution protocol. It is a post-baseline validity check over the frozen EXP-0002 aggregate, curated representative evidence packs, human evidence review, construct validity output, and pressure-citation correction.

Allowed claim after this protocol is merged:

> The EXP-0003 intervention validity stress test protocol is frozen.

Forbidden in this PR:

- EXP-0003 result synthesis
- new LLM runs
- scenario changes
- prompt changes
- Game Master rule changes
- metric changes beyond applying the already accepted pressure-citation correction
- causal claims
- statistical significance claims
- human behavior claims
- real-world organization claims
- compliance, legal, audit, or operational sufficiency claims

## Experiment Identity

| Field | Frozen value |
|---|---|
| Experiment id | `EXP-0003` |
| Protocol id | `exp-0003-intervention-validity-stress-test-v0.1` |
| Domain | `org-payment` |
| Input baseline | `EXP-0002` |
| Scenario set | `S01`-`S06` |
| Execution type | post-baseline descriptive validity synthesis |
| New LLM execution | none |
| Claim boundary | `intervention_validity_stress_test_observation_only` |

## Frozen Inputs

EXP-0003 may use only the following inputs:

- scenario matrix: `scenarios/org-payment/scenario-matrix.md`
- scenario files:
  - `scenarios/org-payment/s01-clear-policy-low-pressure.yaml`
  - `scenarios/org-payment/s02-ambiguous-policy-low-pressure.yaml`
  - `scenarios/org-payment/s03-ambiguous-policy-high-pressure.yaml`
  - `scenarios/org-payment/s04-role-overlap-high-pressure.yaml`
  - `scenarios/org-payment/s05-audit-intervention.yaml`
  - `scenarios/org-payment/s06-hard-control.yaml`
- EXP-0002 protocol: `protocols/baseline/multi-role-baseline-v0.1.md`
- EXP-0002 aggregate result: `results/org-payment/exp-0002-multi-role-baseline/aggregate.json`
- EXP-0002 scenario summary: `results/org-payment/exp-0002-multi-role-baseline/scenario-summary.csv`
- EXP-0002 representative evidence packs: `results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs/`
- EXP-0002 human evidence review: `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md`
- EXP-0002 construct validity check: `results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/summary.md`
- pressure-citation correction: `protocols/evaluation/pressure-citation-metric-correction-v0.1.md`

No raw `runs/` output may be required for EXP-0003. If an EXP-0003 result cannot be supported from committed curated artifacts, it must be reported as a limitation rather than silently reconstructed.

## Frozen Intervention Contrasts

EXP-0003 uses the accepted S01-S06 scenario matrix as designed institutional contrasts. The comparisons are descriptive stress-test contrasts, not randomized causal interventions.

| Contrast id | Baseline condition | Intervention condition | Intended institutional difference |
|---|---|---|---|
| `IV01-policy-ambiguity` | `S01` | `S02` | clear policy versus ambiguous policy |
| `IV02-pressure` | `S02` | `S03` | low deadline/no vendor pressure versus high deadline/vendor pressure |
| `IV03-role-overlap` | `S03` | `S04` | separated roles versus partial role overlap |
| `IV04-monitoring` | `S04` | `S05` | no audit visibility versus active monitored control |
| `IV05-hard-control` | `S05` | `S06` | monitored control versus preventive hard control |

Each contrast must report the manipulated variables from the scenario matrix. Any non-target variable difference found during execution must be reported as a confound and must lower claim strength.

## Frozen Descriptive Measures

EXP-0003 may summarize the following measures by scenario and by contrast:

- accepted and excluded run counts
- full org-payment path counts
- role-turn action counts
- Game Master decision counts
- validation pass/fail counts
- parser failure/retry/rejected proposal counts
- proposed event counts by event type
- approval-evidence propagation summary
- coordination-gap summary
- corrected pressure-context summary
- representative evidence links

EXP-0003 must not compute or report inferential statistics, p-values, confidence intervals, or effect sizes.

## Pressure-Citation Handling

EXP-0003 must apply `protocols/evaluation/pressure-citation-metric-correction-v0.1.md`.

Historical EXP-0002 pressure aggregates may be cited only with the recorded limitation that six pressure-citation metric checks were marked `needs_revision`.

For EXP-0003 contrast reporting:

- `request_payment_status` counts as vendor context, not vendor pressure.
- `apply_deadline_pressure`, `signal_service_continuity_risk`, and `escalate_vendor_pressure` count as explicit vendor pressure actions.
- generic payment-delay, vendor-relationship, vendor-dissatisfaction, or vendor-context wording must not be counted as pressure by itself.
- pressure context must never be reported as pressure causation.

If corrected pressure counts cannot be derived from committed curated artifacts for all 30 EXP-0002 runs, EXP-0003 must separate:

- all-run aggregate counts that are available from `aggregate.json`;
- representative-pack examples that were mechanically validated and reviewed;
- pressure-citation fields that remain historical and limited.

## Output Artifacts for Execution PR

The execution PR must write curated EXP-0003 artifacts under:

`results/org-payment/exp-0003-intervention-validity-stress-test-0001/`

Required artifacts:

- `summary.md`
- `contrast-table.csv`
- `aggregate.json`
- `limitations.md`
- `claim-boundary-review.md`

Optional artifacts:

- `representative-examples.md`
- per-contrast Markdown notes

EXP-0003 must not commit raw `runs/` output.

## Exclusion and Downgrade Rules

EXP-0003 does not exclude EXP-0002 runs retroactively. Instead it must downgrade or limit claims when:

- a contrast includes a non-target variable change;
- a measure depends on uncommitted raw run artifacts;
- a pressure-citation field depends on historical overcounted pressure wording;
- a proposed event label lacks representative reviewed evidence;
- a scenario contrast has too few observations for robust interpretation.

Downgraded items must be recorded in `limitations.md`.

## Claim Boundary

Allowed claim for the execution PR:

> Under the frozen EXP-0003 protocol, the project produced a descriptive intervention-validity stress-test summary over the EXP-0002 artificial organization baseline and recorded which scenario contrasts are reviewable under the current evidence, metric, and claim boundaries.

Required limitations:

- artificial organization only
- post-baseline descriptive stress test only
- no new LLM execution
- no randomized intervention design
- no human behavior claim
- no general LLM behavior claim
- no real-world organization claim
- no compliance, legal, audit, or operational sufficiency claim
- no statistical significance claim
- no pressure-causation claim
- no scenario-causation claim
- no proof of hard-control effectiveness
- no proof of responsibility diffusion or approval bypass

Forbidden claims:

- hard controls are effective in real organizations
- scenario differences caused observed behavior
- vendor pressure caused buyer behavior
- monitored control prevented failure
- role overlap reproduced responsibility diffusion
- EXP-0003 proves institutional failure
- results generalize to humans or real organizations

## Required Validation for Execution PR

The EXP-0003 execution PR must run:

- `python -m unittest discover -s tests`
- `python -m compileall -q src tests scripts`
- selected EXP-0002 representative evidence pack validation
- selected Markdown local links check
- `git diff --check`
- `git ls-files runs`
- changed-file scan for `OPENAI_API_KEY`, `sk-`, and `raw_response`

## Checkpoint Target

After EXP-0003 execution:

- the project has a descriptive stress-test table for S01-S06 institutional contrasts;
- baseline versus intervention differences are explicit;
- pressure-citation overcount is not reused as pressure evidence;
- all claims remain bounded to artificial organization stress-test observations;
- BC17 can decide whether to proceed to sensitivity analysis, revise intervention definitions, or add more review before BC18.
