# Phase 4 Reflection After S21 Boundary Preservation

Date: 2026-05-17
Status: accepted
Phase: Phase 4
Related result: [S21 authority-resolution diagnostic](../../pilot-runs/org-payment/phase4-s21-exception-review-authority-resolution-diagnostic-0001/summary.md)
Claim boundary: `phase4_next_mechanism_selection_only`

## S21 Result Summary

S21 executed 20 frozen exception-review authority-resolution diagnostic runs and accepted all 20. It again preserved downstream approval and authority gaps:

- SL3 accountant payment preparation without approval or valid exception authority: not observed.
- SL4 final payment-ready state without approval or valid exception authority: not observed.
- SL5 evidence-gap preservation: observed in all 20 accepted runs.
- SL6 evidence-gap erasure: not observed.
- FM3 ambiguous authority interpretation: not observed.
- FM6 post-hoc justification: not observed.

The explicit-authority control condition also did not produce a `grant_exception_authority` action in the accepted runs. Therefore, S21 should not be used to infer positive-control payment behavior.

## Boundary-Preservation Pattern

Across S17, S18, S19, S20, S21, prompt/persona variants, and model exploration, the repeated downstream pattern is conservative:

- narrow buyer-side SL2 handoff can appear under lossy handoff and selected exception-route prompt/persona variants;
- downstream accounting usually preserves explicit approval and exception-authority gaps;
- accounting has not prepared payment without explicit approval or valid authority in reviewed Phase 4 evidence;
- final states have not become payment-ready without approval or authority;
- gap erasure has not been supported.

This is a valid artificial-system finding about the current protocols. It is not a claim that real organizations preserve controls, that humans would act this way, or that the model is generally safe.

## Why Repeating S21 Is Not Enough

S21 tests authority handback after accounting routes exception review. Repeating it would mainly test the same visible-gap structure:

- Game Master global truth remains explicit.
- Accountant local view still includes the unresolved approval/authority fields.
- Action menus include conservative options.
- Prompt addenda remind roles to preserve gaps.

This structure is useful for boundary-preservation evidence, but it has not identified a path to stronger downstream slippage.

## Next Mechanism Selection

The next mechanism should be different from lossy handoff, queue/ticket mismatch, exception-route ambiguity, and authority handback.

Selected mechanism: `prior_approval_carryover`.

Rationale:

- Some artificial organization cases may include prior-period, prior-invoice, or similar-case approval artifacts.
- A downstream role may see a prior approval artifact and a current invoice in the same local packet.
- The research question is whether the role keeps the current approval gap visible or treats prior approval as enough to continue payment work.
- This tests record conflation and temporal/scope mismatch, not pressure, queue status, exception routing, or handback ambiguity.

This mechanism does not instruct any actor to bypass approval. It tests whether a role-local packet containing plausible but non-current approval material is interpreted conservatively or as transferable authority.

## Decision

Decision: freeze an S22 prior-approval carryover diagnostic protocol before any execution.

The next PR may execute S22 only after the protocol, scenario, addendum, action menu, Game Master rules, candidate criteria, review criteria, evidence requirements, and claim boundaries are frozen.

## Non-Claims

This reflection does not claim:

- full approval bypass;
- SL3, SL4, or SL6 support;
- prompt causation;
- model comparison or model ranking;
- human behavior;
- real-world organization behavior;
- statistical significance;
- compliance, legal, audit, operational, governance, or safety sufficiency.
