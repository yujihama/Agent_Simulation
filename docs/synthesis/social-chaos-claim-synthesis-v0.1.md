# Social Chaos Claim Synthesis v0.1

Date: 2026-05-17
Status: accepted
Phase: P10
Checkpoint: BC20
Protocol: `protocols/synthesis/social-chaos-claim-synthesis-v0.1.md`
Claim boundary: `bounded_artificial_system_synthesis_only`

## Scope

This synthesis integrates the project's committed governance, protocol, scenario, execution, review, construct-validity, sensitivity, and second-domain artifacts. It states what can be claimed about the project as an artificial-organization research pipeline and what remains outside the evidence.

This synthesis does not add new LLM runs, revise scenarios, revise prompts, revise event taxonomy, revise metrics, add human-review judgments, or run statistical analysis.

## Source Artifacts

| Area | Primary inputs |
|---|---|
| Research positioning | `docs/adr/ADR-0001-research-positioning.md`; `docs/adr/ADR-0002-game-master-architecture.md`; `docs/adr/ADR-0003-initial-domain-org-payment.md`; `docs/adr/ADR-0004-second-domain-expense-reimbursement.md` |
| Design and claim protocols | `protocols/odd-social/odd-social-v0.1.md`; `protocols/evaluation/event-taxonomy-v0.1.md`; `protocols/evaluation/metrics-v0.1.md`; `protocols/evaluation/evidence-pack-v0.1.md`; `protocols/evaluation/claim-boundaries-v0.1.md` |
| Org-payment baseline | `protocols/baseline/multi-role-baseline-v0.1.md`; `results/org-payment/exp-0002-multi-role-baseline/summary.md`; `results/org-payment/exp-0002-multi-role-baseline/review.md` |
| Human and construct review | `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md`; `results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/summary.md` |
| Intervention and sensitivity | `results/org-payment/exp-0003-intervention-validity-stress-test-0001/summary.md`; `results/org-payment/exp-0004-provider-randomness-sensitivity-0001/summary.md`; `results/org-payment/exp-0004-provider-randomness-sensitivity-0001/review.md` |
| Second domain | `protocols/domain-expansion/expense-reimbursement-pilot-v0.1.md`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/summary.md`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/review.md` |

## Synthesis Summary

The project built a staged artificial-organization research pipeline. It starts from explicit research positioning and a Game Master boundary, then adds ODD-Social scenario structure, action and evidence contracts, a validator, non-LLM dry runs, LLM pilots, a full org-payment multi-role baseline, human evidence review, construct-validity review, an intervention-style descriptive stress test, a provider-randomness sensitivity check, and one second-domain expense-reimbursement transfer pilot.

The strongest supported claim is not that the system reproduces real social chaos. The strongest supported claim is that the repository now contains a controlled artifact pipeline that can generate, validate, review, and synthesize traceable artificial-organization interactions while keeping claim boundaries explicit.

Under staged, frozen artificial-organization protocols, this project shows that LLM-controlled roles can generate mechanically valid, reviewable traces of institutional friction-like patterns such as evidence gaps, approval ambiguity, pressure context, and coordination holds in a constrained org-payment setting, with one limited second-domain transfer pilot. These are artificial-system observations and hypotheses for future validation, not direct evidence about human societies or real organizations.

## What The Project Can Claim

| Claim level | Claim | Evidence | Boundary |
|---|---|---|---|
| `supported_artifact_claim` | The repository contains a versioned artificial-organization research pipeline from governance through synthesis. | ADRs, protocols, schemas, runners, validators, EXP-0002 through EXP-0005 results, and this synthesis. | This is a repository/artifact claim, not a claim about external society. |
| `bounded_observation_claim` | EXP-0002 generated 30 accepted, mechanically valid org-payment baseline runs across S01-S06 under frozen conditions. | `results/org-payment/exp-0002-multi-role-baseline/summary.md`; `review.md`. | Descriptive counts only; no statistical, causal, human, or real-world claim. |
| `reviewed_evidence_claim` | The 14 curated EXP-0002 representative packs were accepted for path reconstruction, Game Master boundary reconstruction, proposed event review, and claim-boundary compliance. | `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md`. | Applies only to curated representative packs, with one primary reviewer and no secondary adjudication. |
| `construct_validity_limited_claim` | `evidence_gap`, `approval_evidence_propagation`, and `coordination_gap` are supported for reviewed representative-pack descriptions when their interpretation limits are preserved. | `results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/summary.md`. | Construct support is limited to reviewed representative packs. |
| `construct_validity_limited_claim` | `informal_pressure` is partially supported as pressure-context evidence, while pressure-citation metric rules required correction. | Human review, construct-validity check, and `protocols/evaluation/pressure-citation-metric-correction-v0.1.md`. | This does not show pressure causation or pressure-propagation proof. |
| `bounded_observation_claim` | EXP-0003 records descriptive S01-S06 institutional contrasts over committed EXP-0002 artifacts. | `results/org-payment/exp-0003-intervention-validity-stress-test-0001/summary.md`. | It is not a new causal intervention experiment. |
| `bounded_observation_claim` | EXP-0004 records one provider-randomness sensitivity axis with fixed model, prompts, menus, scenarios, parser, metrics, and Game Master conditions. | `results/org-payment/exp-0004-provider-randomness-sensitivity-0001/summary.md`; `review.md`. | It does not support robustness, model-comparison, or statistical claims. |
| `bounded_observation_claim` | EXP-0005 shows that the action-proposal, Game Master, evidence-pack, validator, and aggregate-reporting structure can produce one mechanically valid expense-reimbursement pilot artifact. | `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/summary.md`; `review.md`. | It is one second-domain pilot, not cross-domain validation. |
| `hypothesis_for_future_work` | The artificial-organization method may be useful for generating reviewable hypotheses about institutional friction mechanisms. | Combined pipeline and review artifacts. | Requires broader domains, more review, sensitivity axes, and external validation before stronger claims. |

## What The Project Cannot Claim

The project cannot claim that:

- LLM agents reproduce human society.
- Human organizations would behave like these artificial runs.
- Real organizations can be predicted from these artifacts.
- Institutional failure has been proven.
- Responsibility diffusion, approval bypass, or policy exploitation has been proven as a real-world or human phenomenon.
- Vendor pressure, requester framing, scenario settings, monitoring, or hard control caused any observed path.
- Any contrast is statistically significant.
- Org-payment findings generalize to expense reimbursement or other domains.
- The system provides compliance, legal, audit, operational, or governance sufficiency.
- The results describe general LLM behavior.

## Evidence By Checkpoint

### EXP-0002 Org-Payment Baseline

EXP-0002 executed the frozen requester + vendor + buyer + approver + accountant baseline across S01-S06. It attempted 30 runs, accepted 30 runs, and excluded 0. Representative evidence packs validate mechanically.

The descriptive pattern is useful but bounded. S01 produced the completed approval/payment-preparation path in all accepted runs. S02, S03, and S04 produced request-more-evidence or hold-payment paths at the accountant stage. S05 and S06 produced mixed approval/preparation and hold paths. These differences are descriptive observations under frozen artificial conditions, not causal scenario effects.

### EXP-0002 Human Evidence Review

The human evidence review covered 14 curated representative EXP-0002 packs, not all raw runs. It accepted 14 packs for reconstruction, accepted 21 proposed event labels with interpretation limits, accepted 120 metric checks, and marked 6 pressure-citation metric checks as `needs_revision`.

The review confirmed that generated event labels can support reconstruction and review, but it did not upgrade all generated labels or all raw runs into human-reviewed evidence.

### EXP-0002 Construct Validity

The construct-validity check supports `evidence_gap`, `approval_evidence_propagation`, and `coordination_gap` for reviewed representative-pack descriptions. It treats `informal_pressure` as partially supported pressure-context evidence. It records `approval_bypass`, `responsibility_diffusion`, `policy_ambiguity_exploited`, and `communication_breakdown` as not observed in the reviewed representative packs.

This is a narrowing result. It protects the synthesis from turning labels that were not observed into project findings.

### EXP-0003 Intervention Validity Stress Test

EXP-0003 summarized institutional contrasts over committed EXP-0002 artifacts without new LLM execution. It records descriptive contrasts for policy ambiguity, pressure, role overlap, monitoring, and hard control. It also applies the pressure-citation correction so routine status requests remain vendor context rather than vendor pressure.

EXP-0003 is useful as a structured descriptive reading of EXP-0002. It is not an intervention experiment that can establish cause or effectiveness.

### EXP-0004 Provider-Randomness Sensitivity

EXP-0004 attempted and accepted 12 fresh repeat runs, 2 per S01-S06 scenario, while keeping model, prompts, menus, scenario wording, parser rules, metrics, and deterministic Game Master behavior fixed. It observed the same path set in S01 and S03, subsets in S02 and S05, and overlap with one new sensitivity path in S04 and S06.

This shows that the pipeline can run an isolated sensitivity check and expose small-run path variation. It does not prove robustness, instability, or general model behavior.

### EXP-0005 Second-Domain Pilot

EXP-0005 executed one expense-reimbursement scenario, ER01, with employee, manager, and finance reviewer roles. It attempted 5 runs, accepted 5 runs, excluded 0, and observed `request_approval -> request_more_evidence -> hold_payment` in all accepted runs.

This shows mechanical transfer of the artifact structure to one adjacent domain. It does not validate the approach across domains and does not establish that expense reimbursement behaves like org-payment.

## Observed Strengths

- Versioned protocols prevent later results from silently changing scenarios, prompts, action menus, evidence requirements, and claim boundaries.
- The Game Master boundary keeps actor proposals separate from institutional decisions and recorded outcomes.
- Evidence packs make runs reconstructable through messages, actions, Game Master decisions, traces, proposed events, metrics, prompts, outputs, and reviewer notes.
- The validator and tests repeatedly caught structural requirements before artifacts were treated as reviewable.
- Human review and construct-validity checkpoints narrowed claims instead of expanding them.
- Stable or conservative paths were preserved as findings rather than hidden.
- The second-domain pilot showed that the artifact machinery is not hard-coded only to the org-payment file layout.

## Observed Weak Points

- Early buyer-only and pressure pilots often produced conservative action choices, especially `request_approval`.
- EXP-0002 pressure-citation metrics overcounted generic vendor delay or dissatisfaction language on routine payment-status paths; this required a forward-looking metric correction.
- `approval_bypass`, `responsibility_diffusion`, `policy_ambiguity_exploited`, and `communication_breakdown` were not observed in reviewed EXP-0002 representative packs.
- EXP-0003 contrasts are descriptive over existing artifacts and do not isolate causal interventions.
- EXP-0004 tests only provider randomness; it does not test prompt, model, menu, Game Master, scenario wording, or metric sensitivity.
- EXP-0005 uses one adjacent second-domain scenario and has no human review or domain baseline.

## Human Review Limits

The human review is a primary review of curated EXP-0002 representative packs. It is not a review of every raw run. It has no secondary reviewer, no disagreement adjudication, and no inter-rater reliability claim.

The review is still valuable because it confirms that selected evidence packs are reconstructable and that reviewed proposed labels can be interpreted within strict boundaries. It does not make EXP-0003, EXP-0004, or EXP-0005 event labels human-reviewed.

## Construct Validity Limits

Construct validity is limited to the reviewed representative-pack scope. The strongest construct support is for reconstructable evidence gaps, preservation of approval evidence, and coordination holds when approval evidence remains unresolved.

Pressure remains a pressure-context construct, not a causal construct. Missing constructs are also findings: the reviewed packs did not show approval bypass, responsibility diffusion, policy ambiguity exploitation, or communication breakdown.

## Sensitivity Limits

EXP-0004 covers one narrow sensitivity axis: provider randomness under otherwise fixed conditions. It does not establish repeatability, robustness, or model-level stability. Any future sensitivity claim needs separately frozen protocols for model, prompt, menu, scenario wording, parser, metric, or Game Master variants.

## Second-Domain Limits

EXP-0005 is a second-domain transfer pilot, not domain validation. It uses one expense-reimbursement scenario, one model, one prompt set, one deterministic Game Master structure, and one 5-run pilot. It supports only the claim that the evidence machinery can produce a mechanically valid adjacent-domain pilot artifact.

## Final Bounded Claim

The project supports a bounded artificial-system synthesis:

> Under staged, frozen artificial-organization protocols, this project shows that LLM-controlled roles can generate mechanically valid, reviewable traces of institutional friction-like patterns such as evidence gaps, approval ambiguity, pressure context, and coordination holds in a constrained org-payment setting, with one limited second-domain transfer pilot. These are artificial-system observations and hypotheses for future validation, not direct evidence about human societies or real organizations.

## Future Work

The next research work should strengthen validity before broadening claims:

- add secondary human review or adjudication for representative packs;
- run additional construct-validity checks after any new baseline;
- freeze separate sensitivity protocols for prompts, menus, models, scenario wording, and Game Master strictness;
- add additional second-domain scenarios before any cross-domain claim;
- define any real-world comparison protocol separately before referencing human or organizational behavior.
