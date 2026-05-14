# S04 Paper Dry Run Package

Date: 2026-05-14
Status: accepted
Phase: P5
Step: P4/P5 data contracts and dry-run bundle
Covers: C04, C05, C06, C08, C09, C11, C13, C14, C15, C16, C17, C18
Supersedes: none
Related ADR: ADR-0001, ADR-0002, ADR-0003

## Purpose

This package is a manually authored, non-LLM paper dry run for S04 `role-overlap-high-pressure`.

It tests whether ODD-Social v0.1, the org-payment scenario matrix, Event Taxonomy v0.1, Metrics v0.1, Evidence Pack v0.1, Human Review Protocol v0.1, and the P4 data contracts can be used together before implementation begins.

It is not an experiment, baseline result, automated harness output, statistical claim, or LLM execution record.

## Scenario

- Scenario: `S04`
- Scenario file: [scenarios/org-payment/s04-role-overlap-high-pressure.yaml](../../../scenarios/org-payment/s04-role-overlap-high-pressure.yaml)
- Manipulated condition: partial role overlap under ambiguous policy and high pressure
- Control mode: soft

## Evidence Pack

The sample evidence pack is under [evidence-pack/](evidence-pack/).

Key review artifacts:

- [manifest.json](evidence-pack/manifest.json)
- [trace.jsonl](evidence-pack/trace.jsonl)
- [actions.jsonl](evidence-pack/actions.jsonl)
- [gm_decisions.jsonl](evidence-pack/gm_decisions.jsonl)
- [events.jsonl](evidence-pack/events.jsonl)
- [metrics.json](evidence-pack/metrics.json)
- [reviewer_notes.md](evidence-pack/reviewer_notes.md)
- [reconstruction-checklist.md](evidence-pack/reconstruction-checklist.md)
- [validation-output.md](validation-output.md)

## Dry-Run Result

The evidence pack was reconstructable from manifest, trace, messages, actions, Game Master decisions, coded events, metrics, and reviewer notes.

The dry run exposed two implementation-planning needs:

- action and decision records need stable cross-references before any automated harness is written
- evidence gaps can be represented cleanly, but they require explicit reviewer notes to prevent over-claiming

## Claim Boundary

This package supports only a protocol-readiness observation: the current protocol set can represent one manually authored S04 sequence well enough for reconstruction review.

It does not support claims about real organizations, model behavior, baseline rates, or scenario-level statistical effects.
