# Social Chaos Claim Synthesis Protocol v0.1

Date: 2026-05-17
Status: accepted
Phase: P10
Checkpoint: BC20
Covers: C01, C02, C03, C08, C10, C11, C12, C15, C16, C17, C18, C19, C20

## Purpose

This document freezes the BC20 synthesis protocol before the final synthesis is written.

The synthesis should integrate the project's staged artifacts and state what can be claimed about LLM-agent artificial organizations as controlled social-simulation artifacts, while explicitly preserving what cannot be claimed about humans, real organizations, causality, prediction, compliance, or statistical significance.

Allowed claim after this protocol is merged:

> The BC20 social-chaos claim synthesis protocol is frozen.

Forbidden in this PR:

- final synthesis conclusions
- new experiment execution
- new scenario definitions
- prompt changes
- event taxonomy changes
- metric changes
- human behavior claims
- real-world organization claims
- statistical or causal claims

## Frozen Synthesis Inputs

The synthesis must use the following committed inputs:

| Input area | Frozen input refs |
|---|---|
| Research positioning | `docs/adr/ADR-0001-research-positioning.md`; `docs/adr/ADR-0002-game-master-architecture.md`; `docs/adr/ADR-0003-initial-domain-org-payment.md`; `docs/adr/ADR-0004-second-domain-expense-reimbursement.md` |
| Working rules and ledger | `docs/research/03_working_rules_and_pr_policy.md`; `docs/coverage_ledger.md` |
| Design protocols | `protocols/odd-social/odd-social-v0.1.md`; `protocols/evaluation/event-taxonomy-v0.1.md`; `protocols/evaluation/metrics-v0.1.md`; `protocols/evaluation/evidence-pack-v0.1.md`; `protocols/evaluation/claim-boundaries-v0.1.md` |
| Org-payment baseline | `protocols/baseline/multi-role-baseline-v0.1.md`; `results/org-payment/exp-0002-multi-role-baseline/summary.md`; `results/org-payment/exp-0002-multi-role-baseline/review.md` |
| Human/review artifacts | `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md`; `results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/summary.md` |
| Intervention and sensitivity | `results/org-payment/exp-0003-intervention-validity-stress-test-0001/summary.md`; `results/org-payment/exp-0004-provider-randomness-sensitivity-0001/summary.md`; `results/org-payment/exp-0004-provider-randomness-sensitivity-0001/review.md` |
| Second domain | `protocols/domain-expansion/expense-reimbursement-pilot-v0.1.md`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/summary.md`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/review.md` |

If a required input is missing or internally inconsistent, the synthesis execution PR must stop and either fix the input in a separate PR or record the input as excluded from synthesis with rationale.

## Output Artifacts

The synthesis execution PR should add:

- `docs/synthesis/social-chaos-claim-synthesis-v0.1.md`
- `docs/synthesis/evidence-map.csv`
- `docs/synthesis/claim-boundary-review.md`
- `docs/synthesis/limitations.md`
- README update
- coverage ledger update

The synthesis execution PR should not add:

- new LLM runs
- new baseline results
- revised event labels
- revised metrics
- new scenario matrix
- human-review judgments
- statistical analysis

## Claim Levels

The synthesis must classify claims into the following levels.

| Level | Meaning | Status in BC20 |
|---|---|---|
| `supported_artifact_claim` | The repository contains a protocol/result/review artifact supporting the statement. | Allowed when cited. |
| `bounded_observation_claim` | A statement about what occurred in artificial runs under frozen conditions. | Allowed with scenario/model/protocol limits. |
| `reviewed_evidence_claim` | A statement about evidence accepted by the recorded human-review protocol. | Allowed only for artifacts covered by EXP-0002-HR-0001. |
| `construct_validity_limited_claim` | A construct statement that must cite construct-validity limitations. | Allowed only with limitations. |
| `hypothesis_for_future_work` | A possible research interpretation requiring further validation. | Allowed if clearly marked as hypothesis. |
| `forbidden_external_claim` | Human, real-world, compliance, legal, audit, operational, causal, predictive, or statistical overclaim. | Forbidden. |

## Required Synthesis Sections

The synthesis must include:

- scope and source artifacts
- what the project can claim
- what the project cannot claim
- evidence map by checkpoint
- observed strengths
- observed failures or weak points
- construct-validity limitations
- human-review limitations
- second-domain limitations
- sensitivity limitations
- implications for future work
- explicit claim-boundary review

## Required Preserved Findings

The synthesis must preserve these points:

- The project built a staged artificial-organization research pipeline from governance through protocols, scenarios, contracts, validators, LLM pilots, baseline, review, construct validity, intervention stress test, sensitivity check, and second-domain pilot.
- EXP-0002 produced mechanically valid full org-payment baseline evidence across S01-S06.
- EXP-0002 human review covered curated representative evidence, not all raw runs.
- Construct-validity outputs include limitations and do not convert generated event labels into unrestricted proof.
- EXP-0003 was descriptive over existing EXP-0002 artifacts and did not run a causal intervention experiment.
- EXP-0004 tested one sensitivity axis only: provider randomness under otherwise fixed conditions.
- EXP-0005 showed mechanical transfer to one expense-reimbursement pilot scenario only.
- Stable or conservative action paths are part of the findings and must not be hidden.
- Generated/proposed event labels remain distinct from human-reviewed evidence.

## Allowed Bounded Synthesis Claim

The final synthesis may claim:

> Under staged, frozen artificial-organization protocols, this project shows that LLM-controlled roles can generate mechanically valid, reviewable traces of institutional friction-like patterns such as evidence gaps, approval ambiguity, pressure context, and coordination holds in a constrained org-payment setting, with one limited second-domain transfer pilot. These are artificial-system observations and hypotheses for future validation, not direct evidence about human societies or real organizations.

The synthesis may also state:

- the evidence-pack and validator machinery worked across org-payment and one expense-reimbursement pilot;
- the strongest evidence is about artifact generation, traceability, and claim-control discipline;
- construct and domain validity remain limited.

## Forbidden Claims

The synthesis must not claim:

- LLM agents reproduced human society
- human organizations would behave this way
- real organizations can be predicted from these runs
- institutional failure has been proven
- responsibility diffusion has been proven as a human phenomenon
- approval bypass has been proven as a real-world phenomenon
- intervention effectiveness has been established
- results are statistically significant
- the approach is validated across domains
- compliance, legal, audit, or operational sufficiency
- general LLM behavior

## Review Requirements

The synthesis execution PR must run:

- `python -m unittest discover -s tests`
- `python -m compileall -q src tests scripts`
- selected Markdown local links check
- input reference existence check
- `git diff --check`
- `git ls-files runs`
- changed/curated artifact scan for `OPENAI_API_KEY`, `sk-`, and provider raw payload markers

## Checkpoint Target

After synthesis execution:

- BC20 has a bounded final synthesis artifact;
- success, failure, and limitation findings are all visible;
- claims are mapped to evidence and claim levels;
- no human, real-world, causal, statistical, compliance, legal, audit, operational, or general LLM overclaim is introduced.
