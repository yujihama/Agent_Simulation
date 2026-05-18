# Current Evidence Inventory v0.1

Date: 2026-05-17
Status: accepted
Phase: Phase 1
Checkpoint: BC1-2 current evidence inventory
Claim boundary: `current_evidence_inventory_only`

## Scope

This inventory organizes the project's current evidence base after BC1-1 research objective reframing and the Method B+ endpoint integration.

It adds no new runs, candidates, reviews, protocols, scenarios, prompts, metrics, or baseline artifacts. It classifies existing artifacts by claim level and review level so later synthesis does not overstate the evidence.

Post-scope-axis update: `docs/research/within-control-process-drift-scope-v0.1.md` changes forward-looking scope language from intent-based `non-intentional` framing to `within-control / outside-control`. This inventory keeps historical artifact names but future evidence entries should classify whether the observation remains within-control.

## Companion Tables

| Table | Purpose |
|---|---|
| `docs/synthesis/current-evidence-map.csv` | Maps major artifacts and result areas to claim level, review level, supported claims, unsupported claims, and next use. |
| `docs/synthesis/current-claim-level-table.csv` | Defines claim levels and distinguishes artifact, observation, reviewed evidence, construct-limited, boundary-limited, generated, not-observed, and forbidden claims. |

## Evidence Strength Summary

The strongest evidence in the project is not a single dramatic failure finding. It is a structured artifact and review pipeline:

- accepted research positioning and claim-boundary documents;
- versioned artificial-organization protocols and scenarios;
- schemas, data contracts, and validators;
- curated evidence packs;
- human review for selected EXP-0002 representative packs;
- construct-validity review for selected constructs;
- Method B and Method B+ candidate reviews that reject or narrow unsupported claims;
- synthesis documents that preserve conservative and not-observed results.

## Claim-Level Inventory

### Supported Artifact Claims

The repository supports artifact claims about:

- research positioning;
- Game Master architecture;
- ODD-Social and scenario structure;
- event, metric, evidence-pack, human-review, and claim-boundary protocols;
- data contracts and schemas;
- evidence-pack validation scripts;
- non-LLM and LLM runner infrastructure;
- documented synthesis and review processes.

These claims establish that the research apparatus exists. They do not prove that the constructs are valid or externally meaningful.

### Bounded Observation Claims

The repository supports bounded artificial observation claims about:

- EXP-0001 buyer-only baseline behavior;
- M01-M05 staged multi-role pilots;
- EXP-0002 multi-role baseline execution counts and path summaries;
- EXP-0003 descriptive scenario contrasts over committed artifacts;
- EXP-0004 one-axis provider-randomness sensitivity;
- EXP-0005 one-scenario expense-reimbursement transfer pilot;
- Method B+ S17/S18/S19 artificial diagnostic outcomes.

These are denominator-explicit artificial-system observations. They do not support statistical significance, human behavior, real-world behavior, causality, or compliance sufficiency.

### Reviewed Evidence Claims

The strongest human-reviewed evidence remains EXP-0002 human review:

- 14 representative packs reviewed for reconstruction and bounded event/metric interpretation;
- one primary reviewer;
- no second human reviewer;
- no adjudication;
- no inter-rater reliability claim.

Method B and Method B+ reviews are useful but have a different review level:

- Codex delegated/proxy reviews under project-owner authorization;
- candidate/support boundary control;
- not independent multi-reviewer human validation.

### Construct-Limited Claims

EXP-0002 construct validity supports only limited construct use:

- `evidence_gap`;
- `approval_evidence_propagation`;
- `coordination_gap`;
- partial pressure-context interpretation after metric correction.

It does not support:

- approval bypass in reviewed EXP-0002 representative packs;
- responsibility diffusion in reviewed EXP-0002 representative packs;
- policy ambiguity exploitation in reviewed EXP-0002 representative packs;
- communication breakdown in reviewed EXP-0002 representative packs.

### Boundary-Limited Method B+ Claims

Method B+ endpoint and later Phase 4 findings are boundary-limited:

- BC31 supports a narrow buyer handoff observation under second-pass proxy review.
- S18 supports SL2 buyer handoff in 3 of 5 reviewed artificial runs under lossy handoff.
- S17, S18, and S19 support downstream SL5 evidence-gap preservation.
- S27 project-owner review confirms `create_payment_draft` as narrow `SL3 partially_supported_needs_revision` while approval and exception-authority gaps remained visible.

These do not support:

- SL4 final payment-ready state without explicit approval;
- SL6 evidence-gap erasure;
- full approval bypass;
- responsibility diffusion;
- ambiguous-guidance misinterpretation;
- post-hoc justification.

They also do not support fraud, intentional misconduct, impersonation, collusion, forged evidence, concealment, unauthorized access, or any outside-control finding.

## Review-Level Inventory

| Review level | Meaning | Current examples | Boundary |
|---|---|---|---|
| `accepted_document` | A project document is accepted as canonical or supporting. | ADRs, research reframing, claim positioning. | Not empirical evidence. |
| `accepted_protocol` | A protocol exists and is versioned. | ODD-Social, evaluation protocols, baseline protocols. | Does not validate outcomes alone. |
| `mechanically_validated_result` | Evidence packs or result artifacts pass mechanical checks. | EXP-0001, EXP-0002, Method B+ representative packs. | Structural validity only. |
| `primary_human_review` | A human reviewer accepted or limited curated artifacts. | EXP-0002 human review. | Curated representative packs only. |
| `construct_validity_review` | A review limited construct interpretation. | EXP-0002 construct validity. | Construct-specific and scope-specific. |
| `codex_proxy_review` | Codex reviewed candidates under project-owner authorization. | S17/S18/S19 Method B+ reviews. | Not independent human validation. |
| `codex_second_pass_proxy_review` | Codex independently re-reviewed a candidate as a second pass. | BC31 FM2 independent review. | Still not multi-reviewer human validation. |
| `generated_only` | A generated candidate exists but has not been reviewed. | Pre-review candidate rows. | Not support. |

## Method B+ SL-Level Inventory

| Level | Current status | Evidence | Boundary |
|---|---|---|---|
| SL2 buyer handoff without explicit approval | Supported with boundary limits. | BC31 narrow review; S18 3/5 reviewed artificial runs. | Buyer-side only; no downstream completion. |
| SL3 accountant payment preparation without explicit approval | Partially supported with boundary limits. | S27 project-owner review confirms `create_payment_draft` as narrow partial support. | Non-payable draft creation only; no final payment readiness, full approval bypass, or gap erasure. |
| SL4 final payment-ready without explicit approval | Not supported. | S17/S18/S19 not observed. | Do not infer from SL2 or SL5. |
| SL5 evidence-gap preservation | Supported for reviewed artificial evidence. | S17/S18/S19 downstream preservation; S27 preserves approval and exception gaps. | Boundary preservation, not failure completion. |
| SL6 evidence-gap erasure | Not supported. | BC35/S17/S18/S19 not observed. | Not proof of absence generally. |

## What Is Strongest

The strongest current claims are:

1. The artifact pipeline exists and is reviewable.
2. EXP-0002 representative packs have limited human-review support.
3. Construct-validity review supports some constructs but rejects or limits others.
4. Method B+ supports downstream gap preservation and narrow SL2 buyer handoff in earlier reviewed diagnostics.
5. Phase 4 S27 adds project-owner-confirmed narrow SL3 partial support for `create_payment_draft` with gaps preserved.
6. The project has strong claim-boundary discipline around negative and conservative results.

## What Is Weakest Or Unsupported

The weakest or unsupported areas are:

- no direct human-social reproduction evidence;
- no real-world organization claim;
- no causal intervention claim;
- no statistical significance claim;
- no full approval-bypass support;
- no SL4/SL6 support;
- only narrow SL3 partial support from S27 `create_payment_draft`, without final payment readiness or gap erasure;
- no responsibility-diffusion, ambiguous-guidance misinterpretation, or post-hoc-justification support;
- no cross-domain validation from one expense-reimbursement pilot;
- no general model safety or reliability claim.

## STOP Condition Review

| STOP condition | Status |
|---|---|
| Generated candidate is treated as reviewed evidence. | Not present. |
| SL2 is upgraded to full approval bypass. | Not present. |
| Proxy review is treated as independent human review. | Not present. |
| Artifact links are missing. | Not present in selected inventory tables. |
| Evidence strength is mixed or unclear. | Not present; claim and review levels are separated. |

## Next Step

BC1-3 should synthesize the reframed objective from BC1-1 and the evidence inventory from BC1-2 into a Phase 1 research position synthesis.
