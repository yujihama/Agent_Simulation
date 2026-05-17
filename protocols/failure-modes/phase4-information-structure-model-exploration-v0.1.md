# Phase 4 Information-Structure And Model Exploration v0.1

Date: 2026-05-17
Status: accepted
Phase: Phase 4
Checkpoint: research-reopen exploration protocol freeze
Protocol id: `phase4-information-structure-model-exploration-v0.1`
Related reopen: `docs/reflections/phase4-reopen-research-objective.md`
Claim boundary: `phase4_information_structure_model_exploration_protocol_only`

## Purpose

This protocol freezes the next Phase 4 run-producing exploration after Phase 4 was reopened as an active research objective.

The objective is to test whether the current evidence pattern is specific to one information structure and one model setting, or whether additional model variation and repeated trials change which structures produce reviewable control-slippage candidates.

This is an exploration protocol, not a baseline protocol. It does not execute runs, add result artifacts, change prior candidate reviews, or upgrade any claim.

## Research Question

Which tested artificial information structures produce reviewable non-intentional control-slippage candidates under fixed artificial org-payment conditions?

The first reopened exploration asks this narrower question:

> Does increasing trials and varying OpenAI model choice across already-tested information structures change the observed candidate pattern?

## Frozen Information Structures

This protocol reuses three already-defined information structures without changing their scenarios, prompts, action menus, Game Master rules, candidate criteria, or claim boundaries.

| Structure id | Structure | Existing protocol | Existing scenario | Current known result |
|---|---|---|---|---|
| `S18_LOSSY_HANDOFF` | Lossy handoff | `protocols/failure-modes/method-b-plus-lossy-handoff-diagnostic-v0.1.md` | `scenarios/org-payment/s18-lossy-handoff-control-slippage.yaml` | Produced reviewed SL2 buyer-side handoff support and SL5 preservation. |
| `S19_QUEUE_TICKET` | Queue/ticket state mismatch | `protocols/failure-modes/method-b-plus-queue-ticket-state-mismatch-diagnostic-v0.1.md` | `scenarios/org-payment/s19-queue-ticket-state-mismatch-control-slippage.yaml` | Produced SL5 preservation only. |
| `S20_EXCEPTION_ROUTE` | Exception route ambiguity | `protocols/failure-modes/phase4-exception-route-ambiguity-diagnostic-v0.1.md` | `scenarios/org-payment/s20-exception-route-ambiguity.yaml` | Produced SL5 preservation only in accepted runs. |

The execution PR must not alter those frozen protocols after seeing outputs.

## Frozen Model Conditions

The exploration attempts these OpenAI model identifiers:

| Model condition id | Requested model |
|---|---|
| `M_GPT_4_1_MINI` | `gpt-4.1-mini` |
| `M_GPT_5_2` | `gpt-5.2` |
| `M_GPT_5_4` | `gpt-5.4` |

If a requested model is unavailable to the configured API key or unsupported by the Responses API, the execution PR must record the cell as `model_unavailable` or `provider_failure`. It must not silently substitute another model.

Model variation is exploratory. It does not support model-comparison, model-ranking, model-general safety, or model-general reliability claims.

## Frozen Run Count

Each available structure/model cell should attempt 5 runs before exclusions.

The total planned matrix is:

- 3 information structures;
- 3 requested model conditions;
- 5 attempted runs per available cell;
- 45 attempted runs if all model conditions are available.

Excluded runs must be reported and must not be silently replaced.

## Execution Requirements

The execution PR may add an orchestration runner or CLI command, for example:

- `src/social_sim/phase4_info_structure_model_explorer.py`
- `execute-phase4-information-structure-model-exploration`

The orchestration may call the existing frozen diagnostic runners for S18, S19, and S20, but it must preserve their frozen artifacts and claim boundaries.

Raw outputs:

- write raw per-cell outputs under ignored `runs/`;
- do not commit raw `runs/`.

Curated output:

- commit only curated aggregate material under `pilot-runs/org-payment/phase4-information-structure-model-exploration-0001/`.

## Required Curated Artifacts

The execution PR should add:

- `summary.md`
- `aggregate.json`
- `execution-manifest.json`
- `matrix-summary.csv`
- `candidate-summary.csv`
- representative evidence packs for at least:
  - one accepted run per available structure/model cell where practical;
  - each structure/model cell that generates SL2, SL3, SL4, or SL6 candidates;
- representative validation outputs;
- candidate review package;
- reflection document.

The candidate review package should be under:

- `pilot-runs/org-payment/phase4-information-structure-model-exploration-0001/candidate-review-0001/`

## Candidate Accounting

The execution PR must aggregate these statuses separately by information structure and model condition:

- SL2 candidate / reviewed support / reviewed rejection / not observed;
- SL3 candidate / reviewed support / reviewed rejection / not observed;
- SL4 candidate / reviewed support / reviewed rejection / not observed;
- SL5 observed / reviewed support / reviewed rejection / not observed;
- SL6 candidate / reviewed support / reviewed rejection / not observed;
- FM1, FM3, and FM6 if generated by the underlying runner.

Generated candidates are not support until reviewed.

Do not collapse:

- SL2 into SL3 or SL4;
- SL5 preservation into failure completion;
- model variation into model comparison;
- run counts into statistical significance.

## Research-Completion Criteria

Delivery completion for this protocol means:

- all available structure/model cells were attempted according to the matrix;
- unavailable model cells were recorded transparently;
- accepted/excluded runs were counted;
- representative evidence packs validate mechanically;
- candidate rows were reviewed;
- a reflection selected the next Phase 4 step.

Research progress means at least one of:

- a non-lossy structure generates reviewed SL2 support;
- any structure generates reviewed SL3, SL4, or SL6 support;
- additional trials or model variation explain why lossy handoff remains uniquely productive at SL2;
- the matrix produces enough negative/conservative evidence to select a different next mechanism with a concrete rationale.

Research completion for Phase 4 is not automatically achieved by this protocol.

Phase 4 research completion can be claimed only if the execution and review establish one of:

- a tested information structure reliably produces reviewed slippage candidates under bounded artificial conditions, with level-specific support and limitations;
- a tested information structure produces reviewed stronger downstream support for SL3, SL4, or SL6;
- the project explicitly decides, with evidence, that the current explored family only supports narrow SL2 plus SL5 preservation and that a substantially different mechanism class is required.

## Reflection Decision Rules

After candidate review, the execution PR must choose one next decision:

1. If S18 remains the only SL2-producing structure and S19/S20 remain SL5-only, freeze an analysis-focused BC explaining why lossy handoff differs before trying prompt/persona variants.
2. If any non-lossy structure produces reviewed SL2 support, freeze a focused follow-up on that structure.
3. If any structure produces reviewed SL3, SL4, or SL6 support, pause additional execution and request project-owner or external human review before baseline discussion.
4. If model identifiers are unavailable, record that limitation and decide whether to test available models only or update model conditions in a new protocol.
5. If no cell yields useful new evidence, freeze a genuinely new information mechanism or stop run-producing work with an explicit evidence-based rationale.

The execution PR must not execute the next selected protocol.

## Non-goals

This protocol must not:

- add new run results;
- alter existing S18/S19/S20 protocols;
- change prompts, personas, scenarios, menus, Game Master rules, event taxonomy, metrics, schemas, validators, or claim boundaries;
- run a baseline;
- make model-comparison or model-ranking claims;
- make prompt-causation claims;
- make human behavior claims;
- make real-world organization claims;
- make statistical significance claims;
- make compliance, legal, audit, operational, governance, or safety sufficiency claims.

## Allowed Claims After Execution

The execution PR may claim only:

- the frozen Phase 4 information-structure/model matrix was attempted;
- available model cells produced recorded candidate/not-observed/reviewed statuses;
- reviewed results are bounded to artificial evidence;
- the matrix did or did not change the current understanding of which information structures produce slippage candidates.

## Forbidden Claims

The execution PR must not claim:

- humans or real organizations behave this way;
- a model is safer, riskier, better, or worse;
- prompt or model choice caused an outcome;
- the result is statistically meaningful;
- full approval bypass was reproduced unless SL3/SL4 support is separately reviewed and still bounded;
- compliance, legal, audit, operational, governance, or safety sufficiency.

## Validation Required After Execution

The execution PR must run:

- `python -m unittest discover -s tests`
- `python -m compileall -q src tests scripts`
- representative evidence pack validation for all available cells
- existing representative evidence pack validation for S18, S19, and S20
- JSON syntax checks for aggregate and manifests
- CSV parse checks for matrix and candidate tables
- selected Markdown local links check
- `git diff --check`
- `git ls-files runs`
- scan changed and curated artifacts for API-key strings, provider secret prefixes, and full provider raw payloads

## Checkpoint Target

After this protocol is executed in a later PR, the project should know whether repeated trials and requested model variation change the current Phase 4 pattern:

- lossy handoff producing narrow SL2;
- queue/ticket mismatch and exception-route ambiguity preserving gaps;
- no tested mechanism producing SL3, SL4, or SL6.
