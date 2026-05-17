# Method B Synthesis v0.1

Date: 2026-05-17
Status: accepted
Phase: Method B
Checkpoint: BC30
Protocol: `protocols/synthesis/method-b-synthesis-v0.1.md`
Claim boundary: `method_b_synthesis_only`

## Scope

This synthesis integrates Method B checkpoints BC21 through BC29. It asks what the project can currently say about targeted failure-mode observability in artificial organization runs.

This synthesis does not add new LLM execution, new scenarios, prompt changes, action-menu changes, Game Master changes, event taxonomy changes, metric changes, human-review judgments, or statistical analysis.

## Source Artifacts

| Area | Primary inputs |
|---|---|
| Failure-mode definitions | `protocols/failure-modes/failure-mode-taxonomy-v0.1.md` |
| High-friction scenarios | `scenarios/org-payment/high-friction-scenario-matrix.md`; S07-S12 scenario files |
| Multi-turn and post-hoc design | `protocols/failure-modes/multi-turn-memory-justification-pilot-v0.1.md`; `pilot-runs/org-payment/method-b-bc23-memory-justification-pilot-0001/` |
| Targeted execution | `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/summary.md`; `aggregate.json` |
| Targeted evidence review | `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/failure-mode-review-0001/summary.md` |
| Baseline decision | `protocols/failure-modes/failure-mode-baseline-decision-v0.1.md`; `baseline-execution-status.md` |
| Diagnostic sensitivity | `protocols/failure-modes/failure-mode-diagnostic-sensitivity-v0.1.md`; `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/summary.md`; `aggregate.json` |
| Second-domain transfer review | `protocols/failure-modes/second-domain-failure-mode-transfer-v0.1.md`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/method-b-transfer-review-0001/summary.md` |

## Synthesis Summary

Method B successfully strengthened the project's ability to define, execute, record, validate, and review targeted artificial-organization failure-mode candidates. It did not yet produce a supported failure-mode finding.

The targeted Method B pilot did not generate candidate rows for FM1-FM6 after the conservative classifier correction. The delegated evidence review accepted the not-observed status for curated representative evidence and did not support or partially support any Method B failure mode.

The diagnostic sensitivity pilot changed one axis: role-local framing. It produced three generated FM6 post-hoc-justification candidate rows and no generated FM1-FM5 candidate rows. Those FM6 rows are useful because they show where review should focus next, but they remain generated candidate material. They are not supported findings and do not show that prompt framing caused the candidates.

The second-domain transfer review mapped Method B concepts to the existing expense-reimbursement EXP-0005 evidence. FM1-FM5 were reviewed as not observed in that representative evidence. FM6 was not assessable because EXP-0005 did not collect post-hoc explanation artifacts. Therefore Method B has no supported cross-domain transfer finding.

## Failure-Mode Status

The authoritative status table is [method-b-failure-mode-status.csv](method-b-failure-mode-status.csv).

Post-BC30 update: `METHOD-B-FM6-REVIEW-0001` reviewed the three BC28 generated FM6 candidate rows and rejected all three. The BC30 synthesis text below preserves the original BC30 interpretation, while the status table records the latest current Method B status.

| Failure mode | BC30 status | Plain-language meaning |
|---|---|---|
| FM1 responsibility diffusion | `not_observed_in_reviewed_method_b_scope` | The reviewed evidence does not show roles passing responsibility around so that accountability becomes unclear. |
| FM2 approval bypass | `not_observed_in_reviewed_method_b_scope` | The reviewed evidence does not show payment or reimbursement moving forward without explicit approval in a way that satisfies the failure-mode definition. |
| FM3 ambiguous guidance misinterpretation | `not_observed_in_reviewed_method_b_scope` | The reviewed evidence does not show ambiguous approval-like language being treated as clear approval. |
| FM4 pressure-normalization | `not_observed_in_reviewed_method_b_scope` | The reviewed evidence does not show urgency or pressure being normalized as a reason to ignore missing evidence. |
| FM5 evidence-gap erasure | `not_observed_in_reviewed_method_b_scope` | The reviewed evidence does not show known evidence gaps disappearing from downstream handling. |
| FM6 post-hoc justification | `needs_review_before_supported_status` | Three generated candidates exist in BC28, but they need separate review before any stronger status. EXP-0005 cannot assess FM6 because it lacks post-hoc explanations. |

After `METHOD-B-FM6-REVIEW-0001`, the current FM6 status for the BC28 candidates is `reviewed_rejected_for_bc28_candidates`.

## What Method B Can Claim

| Claim level | Claim | Evidence | Boundary |
|---|---|---|---|
| `supported_artifact_claim` | The repository now has Method B failure-mode definitions, high-friction scenarios, multi-turn/post-hoc artifacts, targeted execution, diagnostic sensitivity execution, and second-domain transfer review. | BC21-BC29 committed artifacts. | Artifact and workflow claim only. |
| `reviewed_not_observed_claim` | FM1-FM5 are not observed in the reviewed Method B scope. | BC25 delegated review; BC29 delegated transfer review. | This is not proof that the failure modes are absent generally. |
| `generated_candidate_claim` | BC28 generated three FM6 candidate rows under the role-local diagnostic addendum. | `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/aggregate.json`. | Candidate only; not supported; no prompt-causation claim. |
| `not_assessable_claim` | FM6 transfer to expense reimbursement cannot be assessed from EXP-0005. | BC29 transfer review. | Missing post-hoc artifacts, not evidence of absence. |
| `hypothesis_for_future_work` | Future review should focus on BC28 FM6 candidate rows or a frozen second-domain post-hoc diagnostic. | BC28 and BC29 results. | Future work only. |

## What Method B Cannot Claim

Method B cannot claim that:

- human society has been reproduced;
- real organizations would behave similarly;
- responsibility diffusion, approval bypass, ambiguous guidance misinterpretation, pressure-normalization, evidence-gap erasure, or post-hoc justification has been proven;
- any generated candidate is human-reviewed support;
- role-local prompt framing caused the FM6 candidates;
- org-payment findings transfer to expense reimbursement;
- one second-domain scenario validates cross-domain generality;
- results are statistically meaningful;
- the model is generally safe, unsafe, robust, or unstable;
- the artifacts provide compliance, legal, audit, or operational sufficiency.

## Human-Reviewed Scope

Method B does not currently have independent multi-reviewer human support for any failure mode.

BC25 is a delegated review of curated BC24 representative packs under project-owner authorization. It has no secondary reviewer, no disagreement adjudication, and no inter-rater reliability claim.

BC29 is also a delegated transfer review of one EXP-0005 representative pack. It is useful for claim control and construct mapping, but it does not provide cross-domain human validation.

## Sensitivity Result

The BC28 diagnostic sensitivity result is the only Method B step that produced new candidate material after BC25. It attempted 10 runs, accepted 10, excluded 0, and recorded three generated FM6 candidate rows.

The correct interpretation is narrow: when role-local framing was added under otherwise fixed Method B diagnostic conditions, the generated classifier found three post-hoc-justification candidate rows. This does not show that the addendum caused the candidates, that the prompt is better or worse, or that the candidate labels are supported.

## Second-Domain Result

BC29 reviewed the existing EXP-0005 expense-reimbursement evidence against the Method B taxonomy. The mapping is conceptually usable, but the evidence does not support transfer:

- FM1-FM5 were reviewed as not observed in the representative EXP-0005 path.
- FM6 was not assessable because EXP-0005 lacks post-hoc explanations.
- No cross-domain validation claim is supported.

## Pseudo-Reproduction Assessment

Method B does not yet support saying that human social chaos was pseudo-reproduced.

The stronger and safer conclusion is:

> Method B built a reviewable artificial-system pipeline for targeting failure-mode candidates. It produced no supported Method B failure-mode finding. It did produce three generated FM6 post-hoc-justification candidates under a diagnostic prompt-framing condition, but those candidates need review before they can become evidence.

If the term "pseudo-reproduction" is used later, it must mean only a bounded artificial analogue observed and reviewed inside the repository's artificial organization protocols. It must not mean human society, real organizations, or statistical generality.

## Recommended Next Step

Do not proceed to a controlled Method B baseline or cross-domain transfer claim yet.

The next useful checkpoint should be one of:

- review the three BC28 FM6 generated candidate rows in detail;
- freeze and execute a second-domain post-hoc diagnostic that collects the artifacts EXP-0005 lacked;
- revise Method B targeting if FM1-FM5 remain important but unobserved.

Any of these should be a new frozen protocol before execution or stronger interpretation.
