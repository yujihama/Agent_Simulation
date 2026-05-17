# Review Status Labels v0.2

Date: 2026-05-17
Status: accepted
Phase: Phase 2
Checkpoint: BC2-2 evidence pack and review protocol hardening
Claim boundary: `review_status_labels_only`
Supersedes: none
Related protocols: `protocols/evaluation/human-review-protocol-v0.1.md`, `protocols/evaluation/evidence-pack-v0.1.md`

## Scope

This document standardizes review status labels for candidate findings, event labels, metric checks, evidence-pack reconstruction, and claim-boundary reviews.

It does not change prior review artifacts. Existing labels remain valid in their original context. Future reviews should prefer these labels or explicitly map legacy labels to them.

## Label Families

Use two fields when possible:

- `review_status`: what the review concluded;
- `review_level`: who or what performed the review and with what authority.

This prevents a status such as `supported_for_reviewed_evidence` from hiding whether the review was proxy, project-owner human, independent human, or multi-reviewer adjudicated.

## Review Status Labels

| Label | Meaning | Required evidence | Claim boundary |
|---|---|---|---|
| `candidate` | A possible pattern has been generated or identified but not reviewed. | Candidate rule or reviewer note. | No support claim. |
| `requires_review` | The artifact must be reviewed before interpretation. | Generated candidate, unresolved review item, or flagged artifact. | No support claim. |
| `supported_for_reviewed_evidence` | Reviewed source artifacts satisfy the frozen criterion in the reviewed scope. | Source refs, reconstruction notes, claim-boundary check. | Reviewed artificial evidence only unless another protocol says otherwise. |
| `partially_supported_needs_revision` | Reviewed source artifacts support a narrower part of the claim, but the label, scope, or criterion needs revision. | Source refs plus explicit supported and unsupported portions. | Only the narrow supported part may be cited. |
| `rejected` | Review finds that the candidate is contradicted or does not satisfy the criterion. | Source refs or counter-evidence. | Do not use as support; may be cited as reviewed rejection. |
| `needs_revision` | Evidence, artifact structure, metric definition, or review criterion is too ambiguous or flawed for a stable decision. | Description of the ambiguity or defect. | Do not upgrade until revised and re-reviewed. |
| `not_observed` | No qualifying pattern was observed in the reviewed scope. | Denominator or reviewed scope plus absence check. | Not proof of absence outside the scope. |
| `not_applicable` | The label or criterion is outside the artifact scope. | Scope reason. | No positive or negative empirical claim. |
| `accepted_for_reconstruction` | The pack can be reconstructed sufficiently for the review task. | Reconstruction checklist or review notes. | Structural/reconstruction claim only. |
| `partially_reconstructed` | The pack can be partly reconstructed, but missing or ambiguous records limit interpretation. | Missing/ambiguous artifact notes. | Use only weak or narrowed claims. |
| `not_reconstructed` | The pack cannot be reconstructed for the review task. | Missing or inconsistent artifact notes. | No substantive claim from the pack. |

## Review Level Labels

| Label | Meaning | Boundary |
|---|---|---|
| `generated_only` | Produced by runner, heuristic, metric, or script. | Not support. |
| `mechanically_validated` | Structural validator passed. | Reviewable artifact, not substantive support. |
| `proxy_review` | Delegated assistant or project proxy reviewed artifacts. | Disclose as proxy; not independent human validation. |
| `project_owner_human_review` | Project owner reviewed artifacts. | Human-reviewed scope only; not independent multi-reviewer validation. |
| `independent_human_review` | A separate human reviewer reviewed artifacts. | Stronger review, still artificial scope unless protocol extends it. |
| `multi_reviewer_adjudicated` | Multiple reviewers and adjudication process completed. | Reliability claims require a separate frozen protocol. |
| `construct_validity_review` | Review assessed construct interpretation. | Construct-limited use only. |
| `accepted_document` | A document, protocol, or synthesis was accepted. | Artifact status, not empirical review. |

## Recommended Status Combinations

| Situation | `review_status` | `review_level` |
|---|---|---|
| Generated candidate row before review | `requires_review` | `generated_only` |
| Validator passed evidence pack | `accepted_for_reconstruction` or applicable pack status | `mechanically_validated` |
| Proxy-reviewed candidate accepted narrowly | `partially_supported_needs_revision` | `proxy_review` |
| Human-reviewed representative pack accepted | `accepted_for_reconstruction` | `project_owner_human_review` |
| Reviewed candidate contradicted by source refs | `rejected` | reviewer-specific level |
| Target absent in reviewed scope | `not_observed` | reviewer-specific level |
| Metric cannot be interpreted as designed | `needs_revision` | reviewer-specific level |

## Label Use Rules

1. Use the weakest accurate label.
2. Preserve denominator and reviewed scope for `not_observed`.
3. Preserve supported and unsupported portions for `partially_supported_needs_revision`.
4. Do not convert `candidate` or `requires_review` into support.
5. Do not convert `mechanically_validated` into construct validity.
6. Do not convert `proxy_review` into independent human review.
7. Do not convert reviewed artificial evidence into human or real-world claims.
8. Do not use hidden chain-of-thought as evidence for a label.

## Legacy Label Mapping

| Legacy or local label | Preferred v0.2 representation |
|---|---|
| `generated_candidate` | `review_status: candidate`, `review_level: generated_only` |
| `reviewed_not_observed` | `review_status: not_observed`, reviewer-specific `review_level` |
| `observed_boundary_preservation` | Use a concrete status such as `supported_for_reviewed_evidence` or `not_observed` with a clear construct label. |
| `partially_supported_needs_revision_confirmed` | `review_status: partially_supported_needs_revision`; add a note that second-pass review confirmed the narrow status. |
| `completed_for_curated_representative_packs` | Use review-manifest status plus item-level `review_status` and `review_level`. |

## Required Fields For Future Review Tables

Future review tables should include:

- `review_item_id`;
- `artifact_ref`;
- `candidate_or_claim`;
- `review_status`;
- `review_level`;
- `source_refs`;
- `supported_scope`;
- `unsupported_scope`;
- `claim_boundary`;
- `review_notes_ref`.

## Non-Goals

This label set does not:

- revise past results;
- make proxy review equivalent to human review;
- define reviewer recruitment or adjudication protocol;
- support statistical inference;
- support human, real-world, model-general, compliance, legal, audit, operational, governance, or safety sufficiency claims.

## Checkpoint Decision

Decision: review status labels v0.2 are accepted for future reviews.

Future PRs should use these labels when adding review packages or synthesis tables, and should map legacy labels only when needed for clarity.
