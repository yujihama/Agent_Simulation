# Phase 4 Reflection After S22 and Next Mechanism Selection

Date: 2026-05-17
Checkpoint: Phase 4 next-mechanism selection after S22
Related result: [S22 prior approval carryover diagnostic](../../pilot-runs/org-payment/phase4-s22-prior-approval-carryover-diagnostic-0001/summary.md)
Claim boundary: `phase4_next_mechanism_selection_only`

## Current State

S22 executed 20 frozen prior-approval carryover runs with 20 accepted and 0 excluded. In the 15 non-control runs, current approval and valid carryover authority were absent and the accountant selected `request_more_evidence` every time. In the 5 positive-control runs, current approval was present and the accountant selected `prepare_payment` every time.

Reviewed status after S22:

- SL2 remains a scripted setup context in S22, not a new buyer-choice result.
- SL3 accountant payment preparation without current approval or valid carryover authority: not observed.
- SL4 final payment-ready state without authority: not observed.
- SL5 approval/carryover gap preservation: supported for reviewed artificial evidence in the 15 non-control S22 runs.
- SL6 evidence-gap erasure: not observed.
- FM3 prior-approval misattribution: not observed.
- FM6 post-hoc justification: not observed.

S22 therefore strengthens the boundary-preservation pattern. It does not identify an information structure that produces stronger downstream slippage.

## Why Not Repeat S22

Repeating the same prior-approval packet structure would mostly test sampling variation around an already conservative pattern. The non-control packets made the current approval gap and carryover-authority gap visible enough that the accountant preserved the boundary. Phase 4 needs a genuinely different information mechanism before more run-producing work.

## Mechanism Options Considered

| Mechanism | Difference from S22 | Reason to choose or reject now |
|---|---|---|
| More prior-approval repetitions | Same mechanism | Rejected; would not address the unachieved Phase 4 objective. |
| Stronger pressure wording | Pressure intensity only | Rejected; pressure has already been captured without changing buyer/accountant selection. |
| Model-only change | Same information structure | Deferred; model substitution alone is not a new organizational information mechanism. |
| Delegated authority provenance ambiguity | Current-period approval-like record from a substitute or delegate, but authority provenance is missing or conflicting | Selected; it tests whether a role treats an approval-like current record as valid authority when the delegation record is unresolved. |

## Selected Mechanism

Decision: freeze an S23 delegated-authority provenance diagnostic.

The next mechanism is not prior approval carryover. It tests a different boundary: a current-period substitute or delegate produces approval-like language, but the authority source is unresolved unless the protocol condition explicitly records valid delegation.

This is expected to reveal something new because the local packet is closer to current approval than S22 prior approval was, while the Game Master still preserves global truth:

- a delegate or substitute may appear operationally authoritative;
- the current invoice may have approval-like wording;
- the delegation register may be blank, expired, scope-limited, or valid;
- the accountant must decide whether the approval-like note is enough to prepare payment, request evidence, hold, or escalate.

## Useful Outcomes

Useful outcomes include:

- SL3/SL4/SL6 candidate support appears and triggers project-owner or external review before any baseline discussion;
- only SL5 appears again, confirming another boundary-preserving mechanism under the current artificial setup;
- the positive-control condition prepares payment only when valid delegated authority is recorded;
- parser, validator, or reconstruction issues are found and corrected before further Phase 4 execution.

## Non-Claims

This reflection does not claim delegated-authority slippage occurred. It does not claim human behavior, real-world organization behavior, statistical significance, prompt causation, model comparison, or compliance/legal/audit/operational/governance/safety sufficiency.
