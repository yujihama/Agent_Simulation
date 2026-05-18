# Phase 2 Methodology Synthesis v0.1

Date: 2026-05-17
Status: accepted
Phase: Phase 2
Checkpoint: BC2-4 phase 2 methodology synthesis
Claim boundary: `phase2_methodology_synthesis_only`

## Scope

This synthesis integrates Phase 2 methodology artifacts:

- BC2-1 methodological contribution definition;
- BC2-2 evidence-pack and review protocol hardening;
- BC2-3 negative and conservative result methodology.

It adds no new runs, candidates, reviews, protocols, scenarios, prompts, metrics, schemas, validators, or empirical claim upgrades.

## Source Artifacts

| Purpose | Artifact |
|---|---|
| Phase 1 research position | `docs/synthesis/phase1-research-position-synthesis-v0.1.md` |
| Methodological contribution | `docs/methodology/methodological-contribution-v0.1.md` |
| Pipeline overview | `docs/methodology/pipeline-overview.md` |
| Evidence-pack methodology | `docs/methodology/evidence-pack-methodology-v0.1.md` |
| Review hardening | `docs/methodology/review-protocol-hardening-v0.1.md` |
| Review status labels | `protocols/evaluation/review-status-labels-v0.2.md` |
| Negative/conservative results | `docs/methodology/negative-and-conservative-results-v0.1.md` |
| Boundary preservation patterns | `docs/synthesis/boundary-preservation-patterns-v0.1.md` |

## Phase 2 Conclusion

Phase 2 establishes the project as a methodology contribution:

> A protocol-governed artificial-organization research method that freezes conditions before execution, records role proposals and deterministic Game Master decisions, packages reconstructable evidence, validates artifacts mechanically, reviews candidates against source refs, preserves negative and conservative outcomes, and constrains claims to the evidence boundary.

This conclusion is intentionally methodological. It does not claim that the project has reproduced human social behavior, real organizational failure, full approval bypass, statistical effects, model-general behavior, or compliance/audit sufficiency.

## Methodological Contribution

The core contribution is the full pipeline, not any single run result.

The pipeline is:

1. Research positioning and claim boundary.
2. Protocol freeze.
3. Scenario, roles, prompts, and action menus.
4. LLM or scripted role action proposals.
5. Parser and schema checks.
6. Deterministic Game Master decisions.
7. Evidence pack generation.
8. Mechanical validation.
9. Candidate detection.
10. Candidate review.
11. Reflection and synthesis.
12. Claim-boundary update or next protocol.

The method matters because institutional-friction concepts can be overread from transcripts. The pipeline forces stronger interpretations through visible artifacts, source refs, review statuses, and claim boundaries.

## Evidence And Review Method

Phase 2 clarifies that evidence packs are the unit of reconstruction.

A pack should support review of:

- what each role saw;
- what each role proposed;
- what the parser accepted or rejected;
- what the Game Master decided;
- what changed in the trace and final state;
- which generated events and metrics were recorded;
- which source refs support or contradict a candidate;
- which claim boundary applies.

Mechanical validation is necessary but not sufficient. It means the artifact is structurally reviewable. It does not imply construct validity, human review, statistical inference, or external validity.

Review status labels v0.2 now provide a stable vocabulary:

- `candidate`;
- `requires_review`;
- `supported_for_reviewed_evidence`;
- `partially_supported_needs_revision`;
- `rejected`;
- `needs_revision`;
- `not_observed`;
- `not_applicable`;
- reconstruction-specific labels.

Review level must also be preserved so proxy review, project-owner human review, independent human review, construct-validity review, and accepted documents are not collapsed.

## Negative And Conservative Results

Phase 2 makes negative and conservative results reportable.

This is important because the project did not produce a full approval-bypass result. Instead, Method B+ and later Phase 4 reviews found:

- narrow SL2 buyer handoff support in limited artificial conditions;
- repeated downstream SL5 evidence-gap preservation;
- later S27 narrow SL3 partial support for non-payable draft creation;
- no support for SL4 final payment-ready state without explicit approval;
- no support for SL6 evidence-gap erasure;
- reviewed rejection or not-observed status for several failure-mode candidates.

The methodology treats those outcomes as evidence about the artificial setup, not as failed work to hide.

## Current Strengths

The project is strong at:

- documenting artificial conditions before execution;
- separating role proposals from Game Master institutional decisions;
- packaging evidence for reconstruction;
- validating references mechanically;
- preserving candidate/support/rejection distinctions;
- reviewing and narrowing overbroad candidates;
- recording conservative and not-observed outcomes;
- preventing unsupported external claims.

## Current Limits

The project remains limited because:

- many claims are artificial-system-only;
- proxy review is not independent multi-reviewer human validation;
- only selected representative packs have human review;
- construct validity is limited to reviewed constructs;
- observed counts are descriptive unless a frozen statistical protocol exists;
- Method B+ / Phase 4 does not support full approval bypass, SL4, SL6, or real-world control claims;
- no artifact supports human behavior, real-world organization, model-general, compliance, legal, audit, operational, governance, or safety sufficiency claims.

## Phase 3 Readiness

Phase 3 should model control-slippage levels more precisely. Forward-looking scope is now refined by `docs/research/within-control-process-drift-scope-v0.1.md`.

The next work should not restart run-producing diagnostics immediately. It should first define:

- what within-control process drift means;
- how it differs from intentional fraud, malicious bypass, forged approval, concealment, or collusion;
- how SL1 through SL6 relate conceptually;
- which evidence is required for each level;
- how negative examples and boundary preservation fit the model.

Phase 3 can build on Phase 2 because the method now has:

- a claim-safe pipeline;
- review status vocabulary;
- source-ref expectations;
- negative result handling;
- a boundary-preservation synthesis.

## OK / STOP Condition Review

| Condition | Status |
|---|---|
| Phase 2 artifacts are integrated. | OK. |
| Methodological contribution is framed as more than implementation. | OK. |
| Experimental strength and limits are explicit. | OK. |
| Phase 3 connection to non-intentional control slippage is explicit. | OK. |
| Methodology is not reduced to a code or runner description. | OK. |
| No human, real-world, statistical, or compliance claim is made. | OK. |

## Checkpoint Decision

Decision: Phase 2 is complete.

Proceed to Phase 3: establish the non-intentional control slippage conceptual model and evidence requirements before any further run-producing work.
