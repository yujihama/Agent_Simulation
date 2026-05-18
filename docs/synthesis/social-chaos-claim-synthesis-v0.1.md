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
| Method B+ endpoint | `docs/synthesis/method-b-plus-iterative-targeting-synthesis-v0.1.md`; `docs/synthesis/method-b-plus-periodic-synthesis-after-s18-s19-v0.1.md`; `docs/synthesis/method-b-plus-endpoint-claim-hardening-review-v0.1.md`; `docs/synthesis/non-intentional-control-slippage-map.csv`; `docs/synthesis/method-b-plus-failure-mode-status.csv` |
| Scope-axis revision | `docs/research/within-control-process-drift-scope-v0.1.md` |

## Synthesis Summary

The project built a staged artificial-organization research pipeline. It starts from explicit research positioning and a Game Master boundary, then adds ODD-Social scenario structure, action and evidence contracts, a validator, non-LLM dry runs, LLM pilots, a full org-payment multi-role baseline, human evidence review, construct-validity review, an intervention-style descriptive stress test, a provider-randomness sensitivity check, and one second-domain expense-reimbursement transfer pilot.

The strongest supported claim is not that the system reproduces real social chaos. The strongest supported claim is that the repository now contains a controlled artifact pipeline that can generate, validate, review, and synthesize traceable artificial-organization interactions while keeping claim boundaries explicit.

Under staged, frozen artificial-organization protocols, this project shows that LLM-controlled roles can generate mechanically valid, reviewable traces of institutional friction-like patterns such as evidence gaps, approval ambiguity, pressure context, and coordination holds in a constrained org-payment setting, with one limited second-domain transfer pilot. These are artificial-system observations and hypotheses for future validation, not direct evidence about human societies or real organizations.

The Method B+ endpoint extends the synthesis with a more targeted control-boundary finding. It supports a bounded artificial-system claim that downstream accounting often preserved explicit approval/evidence gaps under current Method B+ protocols, while narrow buyer-side SL2 handoff can appear under some artificial conditions, especially lossy handoff. Later S27 project-owner review adds narrow SL3 partial support for non-payable `create_payment_draft` while approval and exception-authority gaps remain visible. The project still does not support final payment-ready state without explicit approval, evidence-gap erasure, full approval bypass, fraud, human behavior, real-world behavior, or statistical claims.

Forward-looking scope should use `Within-Control Process Drift`: observations remain in scope when actors use their own assigned authority, system records match the actual operator, and evidence is not forged, hidden, modified, or fabricated. Intent is not the scope axis.

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
| `bounded_artificial_system_claim` | Method B+ supports that downstream accounting often preserves explicit approval/evidence gaps under current targeted protocols. | `docs/synthesis/method-b-plus-endpoint-claim-hardening-review-v0.1.md`; S17/S18/S19 candidate reviews. | Artificial Method B+ scope only; no real-world control-effectiveness or general LLM-safety claim. |
| `boundary_limited_observation_claim` | Narrow buyer-side SL2 handoff can appear under some artificial Method B+ conditions, especially S18 lossy handoff. | BC31 second-pass review; S18 candidate review; `docs/synthesis/non-intentional-control-slippage-map.csv`. | Does not support SL3 accountant preparation, SL4 final payment readiness, full approval bypass, or causation. |
| `boundary_limited_observation_claim` | S27 `create_payment_draft` has narrow SL3 partial support in reviewed artificial evidence. | S27 project-owner review. | Does not support SL4 final readiness, SL6 gap erasure, full approval bypass, fraud, or audit/compliance sufficiency. |
| `hypothesis_for_future_work` | The artificial-organization method may be useful for generating reviewable hypotheses about institutional friction mechanisms. | Combined pipeline and review artifacts. | Requires broader domains, more review, sensitivity axes, and external validation before stronger claims. |

## What The Project Cannot Claim

The project cannot claim that:

- LLM agents reproduce human society.
- Human organizations would behave like these artificial runs.
- Real organizations can be predicted from these artifacts.
- Institutional failure has been proven.
- Responsibility diffusion, approval bypass, or policy exploitation has been proven as a real-world or human phenomenon.
- Full approval bypass has been reproduced in Method B+.
- S27 narrow SL3 partial support implies final payment-ready state without explicit approval, evidence-gap erasure, full approval bypass, fraud, or audit/compliance sufficiency.
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

### Method B+ Endpoint

Method B+ explored targeted artificial failure-mode and control-boundary diagnostics after the broader baseline and second-domain work. Its endpoint is recorded in the endpoint claim-hardening review.

The current Method B+ finding is two-sided:

- narrow buyer-side SL2 handoff can appear under some artificial conditions: BC31 gave a narrow partially supported buyer handoff observation, and S18 lossy handoff supported SL2 in 3 of 5 reviewed artificial runs;
- downstream accounting repeatedly preserved explicit approval/evidence gaps: S17, S18, and S19 all preserved SL5 evidence gaps downstream, with accountant-side `hold_payment` or evidence-preserving outcomes rather than payment preparation.

The endpoint also records what did not appear or did not survive review:

- S27 adds narrow SL3 partial support for `create_payment_draft`, not final payment readiness or full approval bypass;
- SL4 final payment-ready state without explicit approval is not supported;
- SL6 evidence-gap erasure is not supported;
- FM1 responsibility diffusion is not supported;
- FM3 ambiguous-guidance misinterpretation is reviewed rejected or not observed;
- FM6 post-hoc justification is reviewed rejected or not observed.

This matters because it refines the project-level institutional-friction claim. The project can now discuss a bounded artificial-system pattern of downstream control-boundary preservation and narrow buyer-side handoff slippage. It cannot claim full approval bypass, control failure, or real-world control effectiveness.

Method B+ does not justify a controlled failure-mode baseline. Additional autonomous run-producing Method B+ diagnostics should stop at this endpoint unless a separate mechanism-selection PR identifies a substantially different organizational mechanism before any new protocol freeze or execution.

## Observed Strengths

- Versioned protocols prevent later results from silently changing scenarios, prompts, action menus, evidence requirements, and claim boundaries.
- The Game Master boundary keeps actor proposals separate from institutional decisions and recorded outcomes.
- Evidence packs make runs reconstructable through messages, actions, Game Master decisions, traces, proposed events, metrics, prompts, outputs, and reviewer notes.
- The validator and tests repeatedly caught structural requirements before artifacts were treated as reviewable.
- Human review and construct-validity checkpoints narrowed claims instead of expanding them.
- Stable or conservative paths were preserved as findings rather than hidden.
- The second-domain pilot showed that the artifact machinery is not hard-coded only to the org-payment file layout.
- Method B+ separated buyer handoff, accountant preparation, final payment readiness, gap preservation, and gap erasure instead of collapsing them into one broad approval-bypass label.
- Method B+ preserved conservative downstream accounting outcomes as boundary-preservation evidence rather than treating them as failed runs.

## Observed Weak Points

- Early buyer-only and pressure pilots often produced conservative action choices, especially `request_approval`.
- EXP-0002 pressure-citation metrics overcounted generic vendor delay or dissatisfaction language on routine payment-status paths; this required a forward-looking metric correction.
- `approval_bypass`, `responsibility_diffusion`, `policy_ambiguity_exploited`, and `communication_breakdown` were not observed in reviewed EXP-0002 representative packs.
- EXP-0003 contrasts are descriptive over existing artifacts and do not isolate causal interventions.
- EXP-0004 tests only provider randomness; it does not test prompt, model, menu, Game Master, scenario wording, or metric sensitivity.
- EXP-0005 uses one adjacent second-domain scenario and has no human review or domain baseline.
- Method B+ endpoint did not produce reviewed support for SL3, SL4, SL6, responsibility diffusion, ambiguous-guidance misinterpretation, or post-hoc justification. Later S27 adds narrow SL3 partial support for non-payable draft creation only.
- The control-drift evidence remains narrow: Method B+ endpoint evidence is buyer-side SL2, and S27 adds only narrow SL3 partial support for non-payable draft creation. It does not justify a controlled failure-mode baseline.

## Human Review Limits

The human review is a primary review of curated EXP-0002 representative packs. It is not a review of every raw run. It has no secondary reviewer, no disagreement adjudication, and no inter-rater reliability claim.

The review is still valuable because it confirms that selected evidence packs are reconstructable and that reviewed proposed labels can be interpreted within strict boundaries. It does not make EXP-0003, EXP-0004, or EXP-0005 event labels human-reviewed.

## Construct Validity Limits

Construct validity is limited to the reviewed representative-pack scope. The strongest construct support is for reconstructable evidence gaps, preservation of approval evidence, and coordination holds when approval evidence remains unresolved.

Pressure remains a pressure-context construct, not a causal construct. Missing constructs are also findings: the reviewed packs did not show approval bypass, responsibility diffusion, policy ambiguity exploitation, or communication breakdown.

Method B+ adds a more fine-grained control-slippage vocabulary. The endpoint support is narrow: SL2 buyer handoff has reviewed artificial support in limited conditions. Later S27 adds narrow SL3 partial support for non-payable draft creation. SL4 final payment readiness and SL6 evidence-gap erasure remain unsupported. This distinction must be preserved in any future report.

## Sensitivity Limits

EXP-0004 covers one narrow sensitivity axis: provider randomness under otherwise fixed conditions. It does not establish repeatability, robustness, or model-level stability. Any future sensitivity claim needs separately frozen protocols for model, prompt, menu, scenario wording, parser, metric, or Game Master variants.

## Second-Domain Limits

EXP-0005 is a second-domain transfer pilot, not domain validation. It uses one expense-reimbursement scenario, one model, one prompt set, one deterministic Game Master structure, and one 5-run pilot. It supports only the claim that the evidence machinery can produce a mechanically valid adjacent-domain pilot artifact.

## Method B+ Endpoint Limits

Method B+ should not continue with another autonomous run-producing diagnostic from the current endpoint. The reason is not that the work failed. The reason is that the endpoint has already clarified the current evidence boundary:

- downstream accounting often preserves explicit gaps under the current targeted protocols;
- lossy handoff can produce narrow buyer-side SL2 movement;
- stronger slippage has not appeared.

A genuinely different future mechanism would need to change an organizational information mechanism, not merely increase stress in the same setup. Examples include a newly frozen role-local information protocol, a materially different exception-route protocol, or a post-processing audit reconstruction protocol with source-visibility rules that were not already tested by S17, S18, or S19. Any such mechanism must be selected, justified, frozen, and reviewed in a separate PR before execution.

## Final Bounded Claim

The project supports a bounded artificial-system synthesis:

> Under staged, frozen artificial-organization protocols, this project shows that LLM-controlled roles can generate mechanically valid, reviewable traces of institutional friction-like patterns such as evidence gaps, approval ambiguity, pressure context, and coordination holds in a constrained org-payment setting, with one limited second-domain transfer pilot. These are artificial-system observations and hypotheses for future validation, not direct evidence about human societies or real organizations.

Method B+ adds a narrower endpoint claim:

> In targeted artificial org-payment diagnostics, downstream accounting often preserved explicit approval/evidence gaps under current protocols, while narrow buyer-side handoff without explicit approval appeared under some conditions, especially lossy handoff. Later S27 adds narrow SL3 partial support for non-payable draft creation while gaps remained visible. This is not full approval bypass, does not support final payment readiness without approval, and does not establish human, real-world, statistical, causal, model-general, compliance, legal, audit, or operational claims.

## Future Work

The next research work should strengthen validity before broadening claims:

- add secondary human review or adjudication for representative packs;
- run additional construct-validity checks after any new baseline;
- freeze separate sensitivity protocols for prompts, menus, models, scenario wording, and Game Master strictness;
- add additional second-domain scenarios before any cross-domain claim;
- define any real-world comparison protocol separately before referencing human or organizational behavior.
- do not run additional Method B+ diagnostics unless a new mechanism-selection PR identifies a substantially different organizational mechanism and preserves the SL2/SL3/SL4/SL5/SL6 distinctions.
