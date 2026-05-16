# EXP-0002 Human Evidence Review Protocol v0.1

Date: 2026-05-17
Status: accepted
Phase: P9
Checkpoint: BC15 protocol freeze
Covers: C13, C14, C15, C16, C17, C18, C20
Supersedes: none
Related protocols: `protocols/evaluation/human-review-protocol-v0.1.md`, `protocols/evaluation/event-taxonomy-v0.1.md`, `protocols/evaluation/metrics-v0.1.md`, `protocols/evaluation/evidence-pack-v0.1.md`, `protocols/evaluation/claim-boundaries-v0.1.md`, `protocols/baseline/multi-role-baseline-v0.1.md`

## Purpose

This protocol freezes the first human evidence review package for EXP-0002 before any human-reviewed judgments are recorded.

The review checks whether proposed event labels, approval-evidence propagation summaries, coordination-gap summaries, source references, Game Master decisions, and claim boundaries are supported by the curated EXP-0002 representative evidence packs.

This protocol does not execute the review. It freezes the review target, inputs, labels, output format, exclusion rules, and claim boundary so that review criteria are not changed after reviewing the evidence.

## Review ID

| Field | Frozen value |
|---|---|
| Review id | `EXP-0002-HR-0001` |
| Reviewed experiment | `EXP-0002` |
| Reviewed result | `results/org-payment/exp-0002-multi-role-baseline/summary.md` |
| Baseline protocol | `protocols/baseline/multi-role-baseline-v0.1.md` |
| Generic human review protocol | `protocols/evaluation/human-review-protocol-v0.1.md` |
| Claim boundary | `human_evidence_review_observation_only` |
| Execution output location | `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/` |

## Review Target

EXP-0002-HR-0001 reviews all curated representative EXP-0002 evidence packs:

| Scenario | Representative pack |
|---|---|
| `S01` | `results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs/s01/s01-path-001` |
| `S02` | `results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs/s02/s02-path-001` |
| `S02` | `results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs/s02/s02-path-002` |
| `S02` | `results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs/s02/s02-path-003` |
| `S03` | `results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs/s03/s03-path-001` |
| `S03` | `results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs/s03/s03-path-002` |
| `S04` | `results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs/s04/s04-path-001` |
| `S04` | `results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs/s04/s04-path-002` |
| `S05` | `results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs/s05/s05-path-001` |
| `S05` | `results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs/s05/s05-path-002` |
| `S05` | `results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs/s05/s05-path-003` |
| `S06` | `results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs/s06/s06-path-001` |
| `S06` | `results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs/s06/s06-path-002` |
| `S06` | `results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs/s06/s06-path-003` |

No additional raw runs may be introduced into this review unless a later protocol revision freezes an expanded review set before review execution resumes.

## Reviewers

EXP-0002-HR-0001 requires at least one primary human reviewer.

| Role | Required | Responsibility |
|---|---|---|
| Primary human reviewer | Required | Performs trace-based review and records final review judgments. |
| Secondary human reviewer | Optional for v0.1 | Checks a subset or all judgments for disagreement. |
| Adjudicator | Conditional | Resolves material disagreements if a secondary reviewer is used and disagreement remains. |
| LLM-assisted reviewer | Optional | May prepare summaries or candidate issues, but cannot finalize judgments. |

The execution artifact must record reviewer role, date, and whether any secondary review or adjudication was performed.

An LLM or automation must not mark an event, gap, or claim as human-reviewed. If no human reviewer completes the review, the execution PR must not claim BC15 human review completion.

## Review Inputs

Each representative pack must be reviewed with:

- `manifest.json`
- `scenario.yaml`
- `initial_state/case.md`
- `final_state/case.md`
- `messages.jsonl`
- `actions.jsonl`
- `gm_decisions.jsonl`
- `parser_results/`
- `proposal_attempts/`
- `trace.jsonl`
- `events.jsonl`
- `metrics.json`
- `llm_prompts/`
- `llm_outputs/`
- `reviewer_notes.md`
- `reconstruction-checklist.md`
- matching representative validation output
- EXP-0002 aggregate: `results/org-payment/exp-0002-multi-role-baseline/aggregate.json`
- EXP-0002 scenario summary: `results/org-payment/exp-0002-multi-role-baseline/scenario-summary.csv`

Review must not be performed from `summary.md` or `aggregate.json` alone.

## Frozen Review Questions

For each evidence pack, the primary reviewer must answer:

1. Can the full role path be reconstructed from messages, actions, Game Master decisions, and trace records?
2. Does every reviewed action have a corresponding Game Master decision?
3. Do source references support the action proposal they are attached to?
4. Do proposed event labels in `events.jsonl` match Event Taxonomy v0.1?
5. Are proposed `evidence_gap` labels trace-supported?
6. Are proposed `informal_pressure` labels trace-supported?
7. Does the buyer accounting handoff cite and represent the approver response correctly?
8. Does the accountant action cite the buyer handoff and relevant approval evidence?
9. If explicit approval is absent, is that gap preserved at the accountant stage?
10. If explicit approval is present, is payment preparation trace-supported?
11. Do metrics in `metrics.json` match reviewed evidence and proposed event records?
12. Does the evidence pack contain any claim or note that exceeds the frozen EXP-0002 claim boundary?

## Review Judgments

Each reviewed item must use one of these statuses:

| Status | Meaning |
|---|---|
| `accepted` | The evidence directly supports the reviewed label or statement. |
| `rejected` | The evidence does not support the reviewed label or statement. |
| `needs_revision` | The reviewed label or statement is partly supported but should be narrowed, renamed, or clarified. |
| `insufficient_evidence` | The evidence is too incomplete or ambiguous to decide. |
| `not_applicable` | The item does not apply to this pack. |

Confidence must use the levels from Human Review Protocol v0.1: `high`, `medium`, or `low`.

## Event Review Scope

EXP-0002-HR-0001 reviews the proposed event labels already present in representative packs. It does not add a new event taxonomy and does not introduce new event types.

Likely reviewed proposed labels include:

- `evidence_gap`
- `informal_pressure`

If a reviewer believes another event type is needed, the review output must record that as a recommended taxonomy revision. It must not silently add the new type to EXP-0002 or treat it as accepted coded evidence.

## Metrics Verification Scope

The review must verify, for each representative pack:

- full role path
- selected action per role turn
- parser result status per role turn
- Game Master decision per action
- proposed event labels
- approval-evidence propagation flags
- coordination-gap flags
- pressure-citation flags where applicable

The review may report disagreement between reviewed evidence and generated metrics. It must not rewrite EXP-0002 aggregate metrics. Any correction must be proposed as a later correction or protocol revision.

## Output Requirements

The later execution PR must add, at minimum:

- `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md`
- `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/review-manifest.json`
- `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/pack-review-table.csv`
- `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/event-review-table.csv`
- `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/metric-review-table.csv`
- `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/claim-boundary-review.md`
- `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/disagreements.md`
- README update
- coverage ledger update

If no secondary reviewer is used, `disagreements.md` must explicitly say that no secondary review was performed rather than implying agreement.

## Review Manifest Fields

`review-manifest.json` must include:

- `review_id`
- `review_protocol_ref`
- `reviewed_experiment_id`
- `reviewed_result_ref`
- `reviewed_pack_count`
- `reviewed_pack_refs`
- `primary_reviewer_role`
- `primary_review_date`
- `secondary_reviewer_role`
- `secondary_review_date`
- `adjudication_performed`
- `llm_assistance_used`
- `claim_boundary`
- `review_status`
- `limitations`

Do not record private personal data beyond reviewer role labels unless the project later adopts a privacy policy for reviewer identity handling.

## Exclusion Criteria

A representative pack may be excluded from the human review only if:

- the pack is missing from the committed curated result
- the pack no longer validates mechanically
- required trace files are missing
- required action or Game Master decision files are missing
- file corruption prevents reconstruction

Excluded packs must be listed with reason. Excluded packs must not be silently replaced unless a protocol revision freezes a replacement policy before review execution resumes.

## Claim Boundary

EXP-0002-HR-0001 may claim only:

> The curated EXP-0002 representative evidence packs were reviewed under the frozen human evidence review protocol, and review judgments were recorded for trace reconstruction, proposed event labels, metrics support, and claim-boundary compliance.

Required limitations:

- artificial organization only
- EXP-0002 representative evidence only
- review of curated representative packs, not all raw runs
- generated/proposed event labels remain non-human-reviewed until a primary human reviewer records review judgments
- human review judgments do not establish human behavior, real-world organization behavior, compliance sufficiency, audit sufficiency, operational sufficiency, statistical significance, scenario causation, pressure causation, pressure-propagation proof, responsibility-diffusion proof, approval-bypass proof, model comparison, or general LLM behavior claims

Forbidden claims:

- EXP-0002 reproduces human organizational behavior
- scenario differences are statistically significant
- a scenario caused coordination gaps
- pressure caused downstream behavior
- responsibility diffusion has been reproduced
- approval bypass has been proven
- generated event labels are accepted unless reviewed and marked `accepted`
- reviewing representative packs validates all raw runs
- human review proves real-world compliance, audit, legal, or operational sufficiency

## Non-Goals

This protocol must not:

- execute human review
- add human-reviewed event labels
- change EXP-0002 results
- change EXP-0002 aggregate metrics
- change scenario definitions
- change prompts
- change action menus
- change Game Master rules
- change event taxonomy
- change metrics protocol
- add new LLM runs
- add model comparison
- add statistical analysis
- add human behavior or real-world organization claims

## Required Validation for Execution PR

The later execution PR must run:

- `python -m unittest discover -s tests`
- `python -m compileall -q src tests scripts`
- representative EXP-0002 evidence pack validation for every reviewed pack
- `git diff --check`
- `git ls-files runs` returns no tracked raw run outputs
- scan changed files and curated review artifacts for `OPENAI_API_KEY`, `sk-`, and `raw_response`

## Checkpoint Target

After this protocol is merged:

- EXP-0002 has a documented review.
- The project has decided to advance to human evidence review.
- The human evidence review target and criteria are frozen.
- The next PR can execute EXP-0002-HR-0001 without changing the review target, review questions, status labels, exclusion criteria, output schema, or claim boundary.
