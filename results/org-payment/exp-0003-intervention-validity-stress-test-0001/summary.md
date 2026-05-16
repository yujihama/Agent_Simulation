# EXP-0003 Intervention Validity Stress Test

Status: accepted
Claim boundary: `intervention_validity_stress_test_observation_only`

## Scope

- Protocol: [protocols/evaluation/exp-0003-intervention-validity-stress-test-v0.1.md](../../../protocols/evaluation/exp-0003-intervention-validity-stress-test-v0.1.md)
- Input baseline: [results/org-payment/exp-0002-multi-role-baseline/aggregate.json](../../../results/org-payment/exp-0002-multi-role-baseline/aggregate.json)
- Human evidence review: [results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md](../../../results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md)
- Construct validity check: [results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/summary.md](../../../results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/summary.md)
- Pressure-citation correction: [protocols/evaluation/pressure-citation-metric-correction-v0.1.md](../../../protocols/evaluation/pressure-citation-metric-correction-v0.1.md)
- New LLM execution: none
- EXP-0002 accepted runs summarized: 30

## Contrast Summary

| Contrast | Baseline | Intervention | Descriptive observation |
|---|---|---|---|
| `IV01-policy-ambiguity` | `S01` | `S02` | S01 records a completed approval/payment-preparation path in all accepted runs, while S02 records approver requests for more evidence and accountant holds in all accepted runs. |
| `IV02-pressure` | `S02` | `S03` | S03 records explicit vendor deadline-pressure actions and informal-pressure events, but both S02 and S03 retain accountant-stage holds due to missing approval evidence in all accepted runs. |
| `IV03-role-overlap` | `S03` | `S04` | S03 and S04 record the same aggregate action path and coordination-gap counts in accepted runs; no responsibility-diffusion event is observed in the committed aggregate. |
| `IV04-monitoring` | `S04` | `S05` | S05 records one explicit approval/payment-preparation path and four hold paths, while S04 records hold paths in all accepted runs. |
| `IV05-hard-control` | `S05` | `S06` | S06 records four explicit approval/payment-preparation paths and one hold path, while S05 records one explicit approval/payment-preparation path and four hold paths. |

## Pressure-Citation Handling

EXP-0003 applies the pressure-citation correction. `request_payment_status` is treated as vendor context, not vendor pressure. Explicit vendor pressure actions are limited to `apply_deadline_pressure`, `signal_service_continuity_risk`, and `escalate_vendor_pressure`.

Historical EXP-0002 pressure-language fields are not reused as pressure evidence where human review marked them `needs_revision`.

## Claim Boundary

EXP-0003 is descriptive only. It does not support scenario-causation, pressure-causation, pressure-propagation proof, hard-control effectiveness, responsibility-diffusion proof, approval-bypass proof, statistical significance, human behavior, real-world organization, compliance, legal, audit, operational sufficiency, model-comparison, or general LLM behavior claims.
