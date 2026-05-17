# Phase 4 Reflection After S25 And Next Mechanism Selection

Date: 2026-05-17
Status: accepted
Phase: Phase 4
Checkpoint: after S25 mechanism selection
Claim boundary: `phase4_mechanism_selection_only`

## Context

S25 conflicting operational norms preserved approval gaps in all non-control accepted runs. The positive-control condition prepared payment only when explicit current approval was recorded.

Current Phase 4 state:

- Lossy handoff remains the only tested information structure that produced reviewed narrow SL2 buyer-side handoff support.
- S19 queue/ticket mismatch, S20 exception-route ambiguity, S21 authority-resolution, S22 prior-approval carryover, S23 delegated-authority provenance, S24 approval-artifact mismatch, and S25 conflicting operational norms reinforced downstream SL5 evidence-gap preservation.
- No tested mechanism has produced reviewed SL3 accountant payment preparation without explicit approval, SL4 final payment-ready state without explicit approval, or SL6 evidence-gap erasure.

Phase 4 remains research-open. Repeating S25 or strengthening the same policy-versus-practice packet would not address the research objective.

## Candidate Mechanism Comparison

| Candidate mechanism | Relation to prior work | Decision |
|---|---|---|
| Repeat conflicting operational norms | Same information structure as S25 | Do not select. |
| Increase local-practice pressure only | Changes intensity, not information structure | Do not select. |
| Model-only substitution | Already explored in Phase 4 matrix; not an organizational mechanism by itself | Defer unless paired with a new frozen mechanism. |
| Post-hoc audit reconstruction only | More likely to test explanation drift than downstream payment preparation | Defer. |
| Shadow approval / informal preclearance | Tests whether informal approver-side signals are treated differently from written policy, system state, delegated authority, prior approval, artifacts, or local practice | Select. |

## Selected Mechanism

Decision: freeze an S26 shadow approval / informal preclearance diagnostic.

The selected mechanism tests a different information structure from recent Phase 4 mechanisms:

- S22 tested prior formal approval carryover from an earlier period.
- S23 tested delegated authority provenance.
- S24 tested approval-like artifact mismatch.
- S25 tested written policy versus local operating practice.
- S26 will test whether an informal approver-side preclearance signal, or a buyer summary of such a signal, is preserved as informal context or softened into approval-like evidence by the accountant.

This mechanism is useful because non-intentional control slippage may arise when a downstream processor receives language that sounds socially authoritative but is not a formal approval record. The diagnostic must not instruct actors to bypass controls. It should record formal approval state, informal preclearance state, buyer summary state, and accountant-local visibility separately.

## Research Completion Criteria

S26 can move Phase 4 forward if one of the following happens:

- Informal-preclearance conditions produce reviewed SL3, SL4, SL6, SL1, FM3, or FM6 support or partial support, in which case run-producing work must stop for project-owner or external review before any baseline discussion.
- Informal-preclearance conditions produce only SL5 gap preservation, in which case this mechanism should be recorded as another boundary-preserving result rather than repeated without a new mechanism.
- The formal-approval positive control produces payment preparation only when explicit current approval is recorded, which supports positive-control distinction but not slippage.
- Parser, validator, or evidence reconstruction fails, in which case execution must stop for infrastructure correction.

## Boundaries

This reflection adds no runs, candidates, results, protocol execution, baseline, statistical claim, prompt-causation claim, model-comparison claim, human behavior claim, real-world organization claim, or compliance/legal/audit/operational/governance/safety sufficiency claim.

Proceed to freeze the S26 shadow approval / informal preclearance diagnostic before any execution.
