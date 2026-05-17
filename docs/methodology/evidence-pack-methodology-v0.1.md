# Evidence Pack Methodology v0.1

Date: 2026-05-17
Status: accepted
Phase: Phase 2
Checkpoint: BC2-2 evidence pack and review protocol hardening
Claim boundary: `evidence_pack_methodology_only`

## Scope

This document explains how evidence packs function as the core research artifact in this project.

It adds no new runs, candidates, reviews, scenarios, prompts, metrics, schemas, validators, or result claims. It does not change Evidence Pack v0.1. It hardens the methodology for using evidence packs in later review and synthesis.

## Methodological Purpose

An evidence pack is the smallest artifact set that should allow a reviewer to reconstruct an artificial organization run or curated run subset.

The evidence pack is not just storage. It is the bridge between:

- a frozen protocol;
- LLM or scripted role outputs;
- Game Master decisions;
- generated events and metrics;
- candidate detection;
- review status;
- bounded claim synthesis.

Without a reconstructable evidence pack, the project should not upgrade a run observation into a reviewed finding.

## Reconstruction Questions

A reviewable evidence pack should let a reviewer answer these questions from artifacts, not from memory or hidden reasoning:

| Question | Required evidence surface |
|---|---|
| What artificial protocol and scenario governed the run? | `manifest.json`, `scenario.yaml`, protocol refs. |
| What did each role see? | prompts, messages, role-local context, source visibility notes. |
| What did each role propose? | `actions.jsonl`, parser results, proposal attempts, LLM output artifacts. |
| Was the proposal accepted as valid? | parser result artifacts and proposal attempts. |
| What did the Game Master decide? | `gm_decisions.jsonl`, trace records, final state notes. |
| What changed in the artificial case state? | trace records, final state artifacts, GM notes. |
| Which events and metrics were generated? | `events.jsonl`, `metrics.json`, event and metric protocol refs. |
| Which source records support a label or candidate? | `source_refs`, trace ids, action ids, decision ids, message ids, artifact paths. |
| What evidence is missing, ambiguous, or contradicted? | reviewer notes, reconstruction checklist, gap records, final state. |
| What claim level is justified? | review table, claim-boundary review, synthesis document. |

## Required Methodological Distinctions

### Pack Validity Is Not Claim Support

Mechanical validation checks whether the pack is structurally inspectable. It does not prove that:

- an event label is substantively correct;
- a candidate is supported;
- a construct is valid;
- a count is statistically meaningful;
- a result generalizes outside the artificial setup.

### Candidate Generation Is Not Review

Candidate rows identify possible patterns. They remain review inputs until a reviewer checks the source records.

Generated candidate labels should use statuses such as:

- `candidate`;
- `requires_review`;
- `not_observed_generated`;
- `not_applicable_generated`.

They should not use `supported_for_reviewed_evidence`.

### Review Needs Source References

A review decision must cite source records. Acceptable sources include:

- message ids;
- action ids;
- Game Master decision ids;
- trace ids;
- event ids;
- metric ids;
- final-state paths;
- prompt or output artifacts where the review is about prompt/output content.

Unsupported review basis:

- hidden chain-of-thought;
- reviewer intuition alone;
- aggregate counts without source packs when the claim requires trace evidence;
- summary text when source traces are available and materially relevant.

## Minimum Evidence Pack Components By Use

| Use | Minimum components | Boundary |
|---|---|---|
| Weak artifact/run observation | manifest, scenario, actions, GM decisions, trace, final state. | Can say the run produced artifacts, not that a construct is supported. |
| Mechanical reviewability | above plus validator output and resolvable source refs. | Can say the pack is structurally reviewable. |
| Candidate review | above plus candidate table, source refs, reviewer notes, claim-boundary review. | Can support, narrow, reject, or leave candidate unresolved within reviewed scope. |
| Construct-validity use | above plus construct criteria and explicit review of alternative interpretations. | Can use construct only inside reviewed boundary. |
| Human-reviewed representative claim | above plus human review protocol, reviewer role, limitations, and representative-pack selection rule. | Does not imply full-run-set review or statistical inference. |

## Source Reference Standards

Every candidate-supporting review should check:

- source refs exist;
- source refs point to the same event/action/decision being interpreted;
- source refs include the relevant counter-evidence or missing-evidence record when applicable;
- final state is checked when the candidate concerns downstream outcome;
- the reviewer records whether the source refs are sufficient, incomplete, or misleading.

For role-local context experiments, the evidence pack should distinguish:

- global truth known to the Game Master;
- role-local information shown to the actor;
- handoff summaries;
- hidden or omitted evidence;
- final state and gap ledger.

This distinction prevents reviewers from judging an actor by evidence the actor did not see while still preserving the global truth needed for reconstruction.

## Reviewer Notes Requirements

Reviewer notes should record:

- review target and scope;
- reviewed artifacts;
- reviewer role and review level;
- reconstruction outcome;
- source refs used;
- evidence gaps;
- alternative interpretations;
- decision status;
- claim boundary;
- limitations;
- whether additional human or external review is needed.

If a candidate is partially supported, the notes must state exactly which portion is supported and which portion is not.

## Evidence Pack Anti-Patterns

The following should block claim upgrades:

- actions without corresponding Game Master decisions when decisions are required;
- unresolved `source_refs`;
- candidate rows without source refs;
- final-state claims not checked against final-state artifacts;
- aggregate-only evidence for a trace-level claim;
- review decisions that rely on hidden reasoning;
- treating generated/proposed event labels as human-reviewed coded evidence;
- replacing missing evidence with plausible narrative.

## Relationship To Existing Protocols

This methodology document complements:

- `protocols/evaluation/evidence-pack-v0.1.md`;
- `protocols/evaluation/human-review-protocol-v0.1.md`;
- `protocols/evaluation/review-status-labels-v0.2.md`;
- `docs/methodology/review-protocol-hardening-v0.1.md`.

It does not supersede existing result artifacts. Prior packs retain their original review level and claim boundary.

## BC2-2 OK Condition Review

| Condition | Status |
|---|---|
| Evidence pack required elements are organized. | OK. |
| Reconstructability is central. | OK. |
| Source refs are required for review decisions. | OK. |
| Validator pass is separated from claim support. | OK. |
| Hidden chain-of-thought is not accepted as evidence. | OK. |

## Next Step

Use this methodology with `docs/methodology/review-protocol-hardening-v0.1.md` and `protocols/evaluation/review-status-labels-v0.2.md` for future candidate reviews and synthesis work.
