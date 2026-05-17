# Phase 4 Reflection After S24 And Next Mechanism Selection

Date: 2026-05-17
Status: accepted
Phase: Phase 4
Checkpoint: after S24 mechanism selection
Claim boundary: `phase4_mechanism_selection_only`

## Context

S24 approval-artifact mismatch preserved approval gaps in all non-control accepted runs. The positive-control condition prepared payment only when current approval and authoritative approval evidence were recorded.

Current Phase 4 state:

- Lossy handoff remains the only tested information structure that produced reviewed narrow SL2 buyer-side handoff support.
- S19 queue/ticket mismatch, S20 exception-route ambiguity, S21 authority-resolution, S22 prior-approval carryover, S23 delegated-authority provenance, and S24 approval-artifact mismatch reinforced downstream SL5 evidence-gap preservation.
- No tested mechanism has produced reviewed SL3 accountant payment preparation without explicit approval, SL4 final payment-ready state without explicit approval, or SL6 evidence-gap erasure.

Phase 4 remains research-open. Repeating S24 or strengthening the same approval-artifact packet would not address the research objective.

## Candidate Mechanism Comparison

| Candidate mechanism | Relation to prior work | Decision |
|---|---|---|
| Repeat approval-artifact mismatch | Same information structure as S24 | Do not select. |
| Increase artifact ambiguity only | Changes intensity, not information structure | Do not select. |
| Model-only substitution | Already explored in Phase 4 matrix; not an organizational mechanism by itself | Defer unless paired with a new frozen mechanism. |
| Shadow approval / informal preclearance | Adjacent to prior ambiguity work and buyer-side SL2 findings | Hold. |
| Conflicting operational norms | Written policy requires explicit approval, while local practice may encourage parallel payment preparation before formal approval arrives | Select. |

## Selected Mechanism

Decision: freeze an S25 conflicting operational norms diagnostic.

The selected mechanism tests a different information structure from S19, S20, S22, S23, and S24:

- S19 tested workflow queue state against approval gaps.
- S20/S21 tested exception-route authority and authority handback.
- S22 tested prior approval carryover.
- S23 tested delegated-authority provenance.
- S24 tested approval-like artifact mismatch.
- S25 tests whether an accountant distinguishes written approval policy from local operating practice when those records conflict.

This mechanism is useful because organizational control slippage may arise from routine practice rather than from a single misleading artifact. The diagnostic must not instruct actors to violate controls. It should instead present policy and norm records separately, allow the accountant to choose from the frozen menu, and preserve whether any payment-preparation action relied on local practice while explicit approval remained absent.

## Research Completion Criteria

S25 can move Phase 4 forward if one of the following happens:

- ON02 or ON03 produces reviewed SL3, SL4, SL6, or FM3 support or partial support, in which case run-producing work must stop for project-owner or external review before any baseline discussion.
- ON01-ON03 produce only SL5 gap preservation, in which case conflicting operational norms should be recorded as another boundary-preserving mechanism rather than repeated without a new mechanism.
- ON04 produces payment preparation only when explicit approval is recorded, which supports positive-control distinction but not slippage.
- Parser, validator, or evidence reconstruction fails, in which case execution must stop for infrastructure correction.

## Boundaries

This reflection adds no runs, candidates, results, protocol execution, baseline, statistical claim, prompt-causation claim, model-comparison claim, human behavior claim, real-world organization claim, or compliance/legal/audit/operational/governance/safety sufficiency claim.

Proceed to freeze the S25 conflicting operational norms diagnostic before any execution.
