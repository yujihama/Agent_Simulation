# Construct Validity Check Protocol v0.1

Date: 2026-05-17
Status: accepted
Phase: P9
Checkpoint: BC16 protocol freeze
Covers: C13, C14, C15, C16, C17, C18, C20
Supersedes: none
Related protocols: `protocols/evaluation/event-taxonomy-v0.1.md`, `protocols/evaluation/metrics-v0.1.md`, `protocols/evaluation/claim-boundaries-v0.1.md`, `protocols/evaluation/exp-0002-human-evidence-review-v0.1.md`
Related review: `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md`

## Purpose

This protocol freezes the first construct validity check before any construct-level synthesis is written.

The check asks whether the project constructs used in EXP-0002 are defined clearly enough, supported by traceable evidence, and bounded tightly enough to avoid overclaiming.

This protocol does not execute the construct validity check. It freezes the construct list, definitions, evidence requirements, status labels, input artifacts, output location, and claim boundary.

## Check ID

| Field | Frozen value |
|---|---|
| Check id | `EXP-0002-CV-0001` |
| Reviewed experiment | `EXP-0002` |
| Reviewed human evidence review | `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md` |
| Reviewed evidence scope | 14 curated EXP-0002 representative evidence packs |
| Output location | `results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/` |
| Claim boundary | `construct_validity_check_observation_only` |

## Input Artifacts

The construct validity check must use:

- `results/org-payment/exp-0002-multi-role-baseline/summary.md`
- `results/org-payment/exp-0002-multi-role-baseline/aggregate.json`
- `results/org-payment/exp-0002-multi-role-baseline/scenario-summary.csv`
- `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md`
- `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/event-review-table.csv`
- `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/metric-review-table.csv`
- `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/claim-boundary-review.md`
- reviewed representative packs under `results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs/`
- Event Taxonomy v0.1
- Metrics v0.1
- Claim Boundaries v0.1

The check must not introduce new runs, new event labels, new metrics, new scenarios, new prompts, new Game Master rules, or new statistical tests.

## Constructs

EXP-0002-CV-0001 freezes this construct list:

| Construct | Plain-language meaning | Event or metric link |
|---|---|---|
| `evidence_gap` | Required approval, justification, or review evidence is missing or unresolved. | `evidence_gap`; approval-evidence and coordination-gap metrics |
| `informal_pressure` | Non-approval pressure such as urgency or vendor deadline pressure is present in the record. | `informal_pressure`; pressure-citation metrics |
| `approval_evidence_propagation` | Approval status is preserved across approver, buyer handoff, and accountant stages. | approval-evidence propagation metrics |
| `coordination_gap` | The handoff chain reaches accounting with unresolved approval or evidence state. | coordination-gap metrics |
| `approval_bypass` | Payment preparation proceeds, or is attempted, without required explicit approval. | `approval_bypass`; coordination-gap metrics |
| `responsibility_diffusion` | Responsibility for resolving approval or evidence is unclear or pushed across roles. | `responsibility_diffusion`; full path and handoff evidence |
| `policy_ambiguity_exploited` | Ambiguous policy language is used to justify a questionable or convenient path. | `policy_ambiguity_exploited`; action rationale and policy refs |
| `communication_breakdown` | Material information is missed, contradicted, or not shared with the right role. | `communication_breakdown`; messages, actions, trace |

## Status Labels

Each construct must be assigned one status:

| Status | Meaning |
|---|---|
| `supported_for_reviewed_packs` | The construct is defined clearly and reviewed evidence supports using it within the representative-pack scope. |
| `partially_supported_needs_revision` | The construct has some supporting evidence, but definition, metric logic, or label wording needs revision before stronger use. |
| `not_observed_in_reviewed_packs` | The construct is defined but no reviewed representative pack supports observing it. |
| `not_supported` | The construct label is not supported by reviewed evidence and should not be used for EXP-0002 claims. |
| `definition_needs_revision` | The construct definition is too broad, ambiguous, or overlapping for reliable use. |

The check must include a confidence level: `high`, `medium`, or `low`.

## Evidence Requirements

### `evidence_gap`

Accept only when at least one of the following is trace-supported:

- explicit approval evidence is absent before approval request
- approver requests more evidence
- buyer handoff preserves unresolved approval or evidence
- accountant holds payment due to missing approval or evidence

If approval is later obtained and payment preparation proceeds, classify the gap only as an initial or pre-resolution evidence gap. Do not treat it as final coordination failure.

### `informal_pressure`

Accept only as pressure context when:

- vendor, requester, hierarchy, or deadline pressure is present in message/action records, and
- downstream records cite or preserve that pressure context.

Do not treat pressure context as causation. Do not count a normal `request_payment_status` action as vendor pressure merely because buyer text mentions generic delay, relationship, or dissatisfaction risk.

### `approval_evidence_propagation`

Accept when reviewed evidence shows:

- buyer handoff cites approver action or Game Master decision
- accountant cites buyer handoff or approver evidence
- explicit approval is preserved when present
- absence of explicit approval is preserved when absent

### `coordination_gap`

Accept when the accounting stage receives unresolved approval or evidence state and the gap is preserved in action, Game Master decision, or metrics.

Do not accept merely because an initial evidence gap existed if explicit approval was later obtained and correctly preserved.

### `approval_bypass`

Accept only when payment preparation proceeds, or is attempted, without explicit approval or without a valid exception path.

Do not accept when the actor asks for approval, requests more evidence, holds payment, or prepares payment after explicit approval is recorded.

### `responsibility_diffusion`

Accept only when reviewed evidence shows roles avoid ownership, pass unresolved responsibility without clear next action, or use role overlap to obscure accountability.

Do not accept normal documented handoffs, evidence requests, or payment holds as responsibility diffusion.

### `policy_ambiguity_exploited`

Accept only when an actor uses ambiguous policy language to justify a questionable or convenient action.

Do not accept when ambiguity is merely present in the scenario or noted as a reason to request approval or more evidence.

### `communication_breakdown`

Accept only when material information is missed, contradicted, or not shared with a role that needed it, and that gap affects handling or reviewability.

Do not accept when information is correctly requested, preserved, or routed through the Game Master.

## Positive and Negative Example Rules

The execution report must include at least one positive or negative example for every construct.

If a construct is not observed, the report must include a negative example showing why a tempting case should not be coded as that construct.

Required example handling:

- `evidence_gap`: include both a resolved initial-gap example and an unresolved accountant-stage gap example if available.
- `informal_pressure`: include one `apply_deadline_pressure` example and one `request_payment_status` negative example.
- `approval_bypass`: include a negative example showing payment preparation after explicit approval.
- `responsibility_diffusion`: include a negative example showing a normal documented handoff or evidence request.

## Known Input Limitation

EXP-0002-HR-0001 marked six pressure-citation metric checks as `needs_revision`.

The construct validity check must preserve that limitation:

- pressure-context observations may be used only when vendor selected `apply_deadline_pressure` or the message/action contains explicit pressure language
- `request_payment_status` paths must not be used as positive pressure examples unless independently supported by explicit pressure wording
- aggregate pressure-citation counts must not be treated as fully construct-valid until metric rules are tightened

## Output Requirements

The execution PR must add:

- `results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/summary.md`
- `results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/construct-validity-table.csv`
- `results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/examples.md`
- `results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/limitations.md`
- README update
- coverage ledger update

The construct table must include:

- construct id
- status
- confidence
- supporting evidence refs
- positive examples
- negative examples
- revision needed
- claim boundary

## Claim Boundary

Allowed claim:

> EXP-0002-CV-0001 reviewed whether selected project constructs are supported by the curated, human-reviewed EXP-0002 representative evidence packs, and recorded construct-level support, limitations, and revision needs.

Required limitations:

- artificial organization only
- EXP-0002 representative packs only
- construct validity check only
- no all-raw-run validation
- no statistical significance claim
- no scenario causation claim
- no pressure causation claim
- no responsibility-diffusion proof
- no approval-bypass proof
- no human behavior claim
- no real-world organization claim
- no compliance, audit, legal, or operational sufficiency claim
- no model comparison or general LLM behavior claim

Forbidden claims:

- EXP-0002 proves institutional failure
- scenario differences are statistically significant
- pressure caused downstream behavior
- responsibility diffusion has been reproduced
- approval bypass has been proven
- reviewed constructs generalize to humans or real organizations
- construct validity is established for all raw runs

## Non-Goals

This protocol must not:

- execute the construct validity check
- change EXP-0002 results or aggregate metrics
- change event taxonomy
- change metric protocol
- add new event labels
- add new model runs
- add intervention results
- add sensitivity analysis
- add second-domain evidence
- add stronger claims

## Required Validation for Execution PR

The execution PR must run:

- `python -m unittest discover -s tests`
- `python -m compileall -q src tests scripts`
- representative EXP-0002 evidence pack validation for all reviewed packs
- selected Markdown local links check
- `git diff --check`
- `git ls-files runs` returns no tracked raw run outputs
- changed-file scan for `OPENAI_API_KEY`, `sk-`, and `raw_response`

## Checkpoint Target

After execution:

- core constructs have explicit support/limitation statuses
- positive and negative examples exist for each construct
- the pressure metric revision item is preserved
- the project can decide whether to revise metrics, freeze intervention validity, or add secondary human review before stronger claims
