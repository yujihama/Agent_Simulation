# Non-Intentional Control Slippage Taxonomy v0.1

Date: 2026-05-17
Status: accepted
Phase: Method B+
Checkpoint: control slippage reframing after BC31 FM2 independent review
Covers: C13, C16, C17, C18, C20
Supersedes: none
Related taxonomy: `protocols/failure-modes/failure-mode-taxonomy-v0.1.md`
Related reflection: `docs/reflections/method-b-plus-bc36-after-bc31-fm2-independent-review.md`
Related mapping: `docs/synthesis/non-intentional-control-slippage-map.csv`

## Purpose

This taxonomy adds a higher-level category for partial, non-intentional process movement through unresolved control requirements. It does not replace the existing Method B failure-mode taxonomy. It adds a finer-grained vocabulary for distinguishing buyer handoff, accounting preparation, final readiness, evidence-gap preservation, and evidence-gap erasure.

The immediate trigger is the BC31 FM2 independent review. That review confirmed only a narrow buyer payment-forward handoff without explicit approval. It did not support accountant payment preparation, final payment-ready status, or full approval bypass.

## Higher-Level Category

Category id: `non_intentional_control_slippage`

Definition:

A process moves forward despite unresolved control requirements, not because a role intentionally commits fraud or knowingly violates policy, but because ambiguity, handoff, urgency, prior practice, or evidence gaps allow the process to advance one or more stages.

This category is about traceable process movement and evidence handling. It does not infer hidden intent.

## Explicit Exclusions

This taxonomy excludes:

- intentional fraud;
- forged approval;
- hidden manipulation;
- deliberate concealment;
- collusion;
- malicious bypass;
- fabricated evidence.

Those may be future fraud-indicator work, but they are not the target of this taxonomy and must not be inferred from ordinary artificial-run traces.

## Review Status Labels

Use the existing Method B review labels where possible:

| Status | Meaning in this taxonomy |
|---|---|
| `candidate` | Generated artifacts propose a slippage subtype, but no review has accepted it. |
| `supported_for_reviewed_evidence` | Review accepts the subtype for the reviewed artificial evidence scope. |
| `partially_supported_needs_revision` | Evidence supports part of the subtype, but the boundary or evidence requirements need refinement. |
| `rejected` | Review rejects the subtype for the trace. |
| `not_observed` | The artifact set contains no plausible subtype observation. |

Generated labels remain candidates until review accepts, rejects, or revises them.

## Cross-Cutting Evidence Rules

Every slippage observation must include:

- the unresolved control requirement;
- the role that acted;
- the action, message, Game Master decision, trace, or final-state source references;
- the process stage before and after the action;
- whether the evidence gap was preserved, erased, contradicted, or resolved;
- why the case is not merely normal cautious handling;
- a claim boundary.

Do not infer intent, fraud, or real-world control failure from a slippage label.

## SL1: Ambiguous Approval Interpretation

Definition:

A role receives ambiguous approval-related guidance and treats it as more operationally usable than explicit evidence supports.

Positive example:

- Approver says "looks okay if same as last time"; buyer treats it as sufficient to move forward.

Not enough for SL1:

- Role records ambiguity and holds payment.
- Role asks for clarification.
- Role accurately says explicit approval is absent.

Evidence requirement:

- ambiguous approval-related source text;
- downstream representation stronger than the source supports;
- approval state showing explicit approval was absent;
- source references linking the downstream representation to the ambiguous guidance.

## SL2: Payment-Forward Handoff Without Explicit Approval

Definition:

A buyer or process owner sends a payment-related request to accounting or the next processing role while explicit approval is absent.

This is the subtype confirmed narrowly by PR #73 for BC31 candidate `BC31-CAND-002`.

Evidence requirement:

- explicit approval absent;
- handoff action exists;
- handoff moves the case toward accounting or payment processing;
- evidence gap is still visible.

Important:

SL2 is weaker than full approval bypass. It does not require payment preparation or final payment readiness.

## SL3: Payment Preparation Without Explicit Approval

Definition:

Accounting or finance prepares payment, schedules payment, or performs equivalent payment-preparation work while explicit approval is absent.

Evidence requirement:

- explicit approval absent;
- accountant or finance action is payment-preparation-like;
- Game Master or final state records preparation or preparation-equivalent status.

Important:

SL3 is stronger than SL2 because the processing role has begun payment preparation rather than merely receiving a handoff.

## SL4: Final Payment-Ready State Without Explicit Approval

Definition:

The final state treats the case as payment-ready, payment-approved, or payment-prepared while explicit approval remains absent.

Evidence requirement:

- explicit approval absent;
- `final_state` shows payment-ready or equivalent;
- evidence gap is not blocking the final processing state.

Important:

SL4 is the strongest non-intentional approval-control slippage level in this taxonomy.

## SL5: Evidence Gap Preservation

Definition:

The process moves forward in some way, but the evidence gap is preserved and blocks later processing.

This is not necessarily a failure. It may be a boundary-preserving result.

Positive example:

- Buyer sends the case to accountant, but accountant requests more evidence and final state remains not payment-ready.

Relationship to PR #73:

PR #73 falls between SL2 and SL5:

- SL2 because buyer handed off a payment request without explicit approval;
- SL5 because downstream controls preserved the gap.

Evidence requirement:

- earlier unresolved gap exists;
- process moves at least one stage;
- downstream action, Game Master decision, or final state preserves the gap;
- later processing is held, blocked, or made conditional on resolving the gap.

## SL6: Evidence Gap Erasure

Definition:

A known evidence gap exists earlier but disappears or is no longer represented in downstream action, Game Master decision, final state, or metrics.

Evidence requirement:

- gap explicitly recorded earlier;
- downstream record omits or contradicts the gap;
- omission changes the process interpretation.

Important:

SL6 is a stronger concern than SL5. SL5 preserves the gap; SL6 loses or contradicts it.

## Relationship To FM2 Approval Bypass

The existing FM2 label remains valid, but it is too broad for the PR #73 observation if used without levels.

Use this taxonomy to distinguish:

- SL2: handoff without explicit approval;
- SL3: payment preparation without explicit approval;
- SL4: final payment-ready state without explicit approval;
- SL5: gap preservation after movement;
- SL6: gap erasure after movement.

A future full FM2 support claim would need to specify which slippage level is supported and what evidence shows the process stage.

## Claim Boundary

Allowed claims:

- A trace can be classified by slippage level for artificial evidence review.
- BC31 has a reviewed narrow SL2 observation plus SL5 gap preservation.
- Existing evidence does not support SL3 or SL4 for BC31.

Forbidden claims:

- any slippage label proves fraud or intentional misconduct;
- any slippage label proves real-world control failure;
- SL2 alone proves full approval bypass;
- generated slippage candidates are support before review;
- these labels support human behavior, real-world organization, model-general, statistical, compliance, legal, audit, or operational sufficiency claims.
