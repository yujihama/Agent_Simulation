# Review Protocol Hardening v0.1

Date: 2026-05-17
Status: accepted
Phase: Phase 2
Checkpoint: BC2-2 evidence pack and review protocol hardening
Claim boundary: `review_protocol_hardening_only`

## Scope

This document hardens the review procedure for artificial-organization evidence packs and candidate findings.

It adds no new run, candidate, review result, scenario, prompt, metric, schema, validator, or empirical claim. It standardizes how later reviews should convert evidence into bounded statuses.

## Review Principle

Review should answer a narrow question:

> Does the cited artifact evidence support this specific interpretation inside the frozen artificial scope?

Review should not answer:

> What probably happened in a real organization?

or:

> What does the model generally do?

## Review Levels

| Review level | Meaning | Claim limit |
|---|---|---|
| `generated_only` | A runner, heuristic, or script produced a candidate or not-observed label. | No support claim. |
| `proxy_review` | A delegated or assistant review checked artifacts and source refs. | Useful bounded review, not independent human validation. |
| `project_owner_human_review` | The project owner reviewed artifacts under a documented protocol. | Human-reviewed scope only; not multi-reviewer validation. |
| `independent_human_review` | A reviewer independent of the run production and proxy review checked artifacts. | Stronger review claim, still artificial scope only. |
| `multi_reviewer_adjudicated` | Multiple reviewers reviewed and disagreements were adjudicated. | May support stronger reliability claims if protocol defines them. |
| `construct_validity_review` | Review checks whether an event/metric construct is interpretable. | Construct-limited claim only. |
| `accepted_document` | A protocol, synthesis, or governance artifact is accepted. | Artifact claim, not empirical support. |

## Review Inputs

A review should use:

- frozen protocol reference;
- scenario reference;
- action menus and prompt refs;
- evidence pack or curated review pack;
- validator output when structural validity matters;
- event taxonomy and metric protocol refs;
- candidate table, if any;
- claim-boundary document;
- prior review notes, if applicable.

Do not review trace-level candidates from summary text alone when source traces are available.

## Review Procedure

1. Confirm the review target and claim boundary.
2. Confirm protocol and scenario refs.
3. Confirm the evidence pack validates or record why validation is not applicable.
4. Reconstruct the relevant trace segment from messages, actions, decisions, trace records, and final state.
5. Check the candidate definition or review criterion.
6. Check supporting evidence and counter-evidence.
7. Assign a review status from `protocols/evaluation/review-status-labels-v0.2.md`.
8. Record source refs, limitations, and alternative interpretations.
9. Record whether the result affects synthesis, future protocol design, or neither.

## Status Assignment Rules

Use the weakest accurate status.

| If evidence shows... | Use... |
|---|---|
| Full criterion is satisfied in reviewed evidence. | `supported_for_reviewed_evidence` |
| Only a bounded part is satisfied and gaps remain. | `partially_supported_needs_revision` |
| The candidate is contradicted or criterion is not met. | `rejected` |
| Evidence is too ambiguous or the criterion is underspecified. | `needs_revision` |
| No candidate or qualifying pattern appears in the reviewed scope. | `not_observed` |
| The label is outside the scope of the artifact. | `not_applicable` |
| The artifact is generated and not yet reviewed. | `requires_review` |

## Source Reference Requirements

Every supported, partially supported, rejected, or needs-revision decision should cite:

- the source records used;
- any decisive counter-evidence;
- final state when downstream outcome matters;
- the reason the status is weaker or stronger than adjacent labels.

For example, SL2 buyer handoff without explicit approval, SL3 accountant preparation without explicit approval, and SL4 final payment-ready state without explicit approval require separate source checks. A supported SL2 handoff does not imply SL3 or SL4.

## Proxy Review Boundary

Proxy review is useful for fast iteration, but it must remain labeled.

Proxy review may:

- check source refs;
- reject overbroad generated candidates;
- narrow a candidate to a smaller supported scope;
- recommend human review;
- support artificial-evidence findings within a disclosed proxy-review boundary.

Proxy review must not:

- be described as independent human validation;
- create inter-rater reliability claims;
- upgrade artificial evidence to real-world claims;
- replace project-owner or external human review where the protocol requires it.

## Human Review Boundary

Project-owner human review can strengthen a reviewed-evidence claim, but only for the reviewed artifacts and criteria.

It does not automatically create:

- full run-set review;
- independent replication;
- cross-domain validation;
- external validity;
- statistical significance;
- compliance, legal, audit, operational, governance, or safety sufficiency.

If stronger review claims are desired, a future protocol must define reviewer independence, selection, adjudication, and reliability criteria before review begins.

## Hidden Reasoning Boundary

Review must not depend on hidden chain-of-thought or unstated internal reasoning by an LLM or reviewer.

Allowed evidence includes visible artifacts:

- prompts;
- LLM outputs;
- parsed actions;
- messages;
- Game Master decisions;
- trace records;
- events;
- metrics;
- final state;
- reviewer notes.

If a claim depends on what an actor "must have thought" but no visible artifact supports it, the claim should be rejected or marked needs revision.

## Claim Boundary Check

Every review should include a claim-boundary check:

- What can be said?
- What cannot be said?
- What review level supports the statement?
- Which adjacent stronger claims remain unsupported?

The review should explicitly prevent:

- candidate/support collapse;
- not-observed/proof-of-absence collapse;
- SL2/SL3/SL4 collapse;
- artificial/human claim collapse;
- validation/construct-validity collapse;
- observation/statistical-inference collapse.

## BC2-2 OK Condition Review

| Condition | Status |
|---|---|
| Review statuses are defined. | OK, with canonical labels in `review-status-labels-v0.2.md`. |
| Proxy review and independent human review are separated. | OK. |
| Candidate, partially supported, supported, rejected, and not observed are distinct. | OK. |
| Reviewer evidence requirements are explicit. | OK. |
| Source refs are required for review decisions. | OK. |
| Hidden chain-of-thought is excluded. | OK. |

## Next Step

Future reviews should use the v0.2 status labels and preserve the review level in tables, manifests, summaries, and synthesis documents.
