# Evidence Pack v0.1

Date: 2026-05-14
Status: accepted
Phase: P3
Step: P3 evaluation protocol bundle
Covers: C15, C16, C17, C18, C20
Supersedes: none
Related ADR: ADR-0001, ADR-0002, ADR-0003

## Purpose

The evidence pack defines the minimum record required to review, reconstruct, and compare an artificial organization run.

This document defines artifact expectations and traceability rules. It does not define JSON schemas, implementation code, experiment execution, or baseline results.

## Evidence Pack Boundary

An evidence pack belongs to one run unless explicitly documented as an aggregate review pack. It should contain enough information for a reviewer to answer:

- which scenario and protocol versions were used
- which roles participated
- which messages, actions, and Game Master / Arbiter decisions occurred
- which events were coded
- which metrics were derived
- what evidence is missing or ambiguous

## Expected Layout

The following layout is a protocol-level target, not a schema contract.

```text
run_<run_id>/
  manifest.json
  odd_social.md
  scenario.yaml
  initial_state/
  final_state/
  trace.jsonl
  messages.jsonl
  actions.jsonl
  gm_decisions.jsonl
  events.jsonl
  metrics.json
  reviewer_notes.md
  llm_review.json
```

## Artifact Expectations

| Artifact | Purpose | Required for v0.1 review |
|---|---|---|
| `manifest.json` | Identifies run id, scenario id, protocol versions, model or actor configuration, and known exclusions. | Yes |
| `odd_social.md` | Captures the ODD-Social description used for the run. | Yes |
| `scenario.yaml` | Captures the scenario condition and manipulated variables. | Yes |
| `initial_state/` | Stores starting organization and case state. | Yes |
| `final_state/` | Stores ending organization and case state. | Yes |
| `trace.jsonl` | Provides ordered run-level trace entries. | Yes |
| `messages.jsonl` | Records participant communication. | Yes |
| `actions.jsonl` | Records proposed and accepted actions. | Yes |
| `gm_decisions.jsonl` | Records Game Master / Arbiter decisions and reasons. | Yes |
| `events.jsonl` | Records coded events from the event taxonomy. | Yes after review |
| `metrics.json` | Records derived metrics and version references. | Yes after metrics pass |
| `reviewer_notes.md` | Records human review notes, disagreements, and limitations. | Yes after review |
| `llm_review.json` | Records optional LLM-assisted review suggestions. | Optional |

## Traceability Rules

Every coded event should cite at least one source record from a message, action, trace entry, or Game Master / Arbiter decision.

Every metric should be traceable to:

- the event taxonomy version
- the metrics version
- the set of event records or state records used
- known missing evidence

Every claim based on a run should cite the evidence pack and should state whether human review is complete.

## Reconstruction Check

Before a run can support more than a weak observation, a reviewer should attempt a reconstruction check:

1. Identify the initial payment case.
2. Reconstruct the sequence of messages, proposed actions, and Game Master / Arbiter decisions.
3. Confirm the final case state.
4. Confirm which required approval, exception, audit, and evidence records exist.
5. Mark missing or inconsistent evidence as a visible gap.

The reconstruction outcome should be one of:

- reconstructed
- partially reconstructed
- not reconstructed

## Exclusions

The evidence pack must not be treated as:

- a privacy-safe public data release by default
- a real-world compliance record
- proof that human organizations behave the same way
- a substitute for review of the underlying protocol versions

## Version Boundary

Evidence Pack v0.1 is sufficient for non-LLM dry-run planning and implementation scoping. It will need schema work and reconstruction testing before full experiment execution.
