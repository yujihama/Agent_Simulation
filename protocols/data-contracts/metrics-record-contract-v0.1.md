# Metrics Record Contract v0.1

Date: 2026-05-14
Status: accepted
Phase: P4
Step: P4/P5 data contracts and dry-run bundle
Covers: C14, C15, C16, C18, C20
Supersedes: none
Related ADR: ADR-0001, ADR-0002, ADR-0003

## Purpose

A metrics record captures an exploratory metric derived from reviewable evidence, coded events, or state reconstruction.

Metrics records must preserve denominator choices, source evidence, and limitations so that counts do not become stronger claims than the evidence supports.

This contract is a protocol-level artifact. It is not a JSON schema, production API, implementation code, automated analysis, baseline result, or statistical claim.

## Required Fields

| Field | Meaning |
|---|---|
| `metric_id` | Stable identifier unique within the run or report. |
| `run_id` | Run, dry-run package, or run set identifier. |
| `metrics_version` | Metrics protocol version used. |
| `metric_group` | Metric group from Metrics v0.1. |
| `metric_name` | Human-readable metric name. |
| `value` | Metric value, which may be numeric, categorical, or structured. |
| `denominator` | Denominator used, or explicit `not_applicable`. |
| `source_event_ids` | Event records used by the metric, if any. |
| `source_record_refs` | Trace, state, action, decision, or review records used. |
| `interpretation_limit` | Maximum statement class allowed from this metric. |
| `known_limitations` | Missing evidence, ambiguity, or denominator concerns. |

## Recommended Fields

| Field | Meaning |
|---|---|
| `scenario_id` | Scenario condition used. |
| `calculation_note` | Human-readable explanation of how the value was derived. |
| `review_status` | Proposed, checked, revised, disputed, or accepted. |
| `human_authored` | Whether the metric was manually authored for a dry run. |

## Contract Rules

- Metrics must cite their input evidence.
- Event-count metrics must cite event ids.
- Auditability metrics must cite artifact inventory or reconstruction notes.
- Scenario contrast metrics must cite the scenario pair being compared and must not imply statistical evidence from a single dry run.
- Metrics from a paper dry run may support protocol-readiness observations, not baseline claims.

## Version Boundary

This contract is sufficient for paper dry runs and implementation planning. It does not define automated calculation, aggregation rules, statistical tests, or publication-ready reporting.
