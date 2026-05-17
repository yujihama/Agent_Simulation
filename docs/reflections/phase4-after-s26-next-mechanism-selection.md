# Phase 4 Reflection After S26 and Next Mechanism Selection

Date: 2026-05-18
Previous result: [pilot-runs/org-payment/phase4-s26-shadow-approval-preclearance-diagnostic-0001/summary.md](../../pilot-runs/org-payment/phase4-s26-shadow-approval-preclearance-diagnostic-0001/summary.md)
Previous reflection: [docs/reflections/phase4-after-s26-shadow-approval-preclearance-diagnostic.md](phase4-after-s26-shadow-approval-preclearance-diagnostic.md)
Claim boundary: `phase4_mechanism_selection_only`

## Current State

S26 tested shadow approval and informal preclearance. It produced another boundary-preserving result:

- SP01-SP03 non-control runs preserved formal approval gaps downstream.
- SP04 positive-control runs prepared payment only when formal current approval was recorded.
- No reviewed SL1, SL3, SL4, SL6, FM3, or FM6 support appeared.
- Phase 4 therefore remains research-incomplete: it still has not identified an information structure that produces stronger downstream slippage candidates.

The repeated pattern across S20-S26 suggests that the existing accountant menus may make the risky action too final. The menu item `prepare_payment` is operationally strong, so the accountant often chooses `hold_payment` or `request_more_evidence` when approval is missing. That is a valid boundary-preservation result, but it leaves open whether slippage appears at a lower-commitment processing stage.

## Mechanisms Considered

| Mechanism | Assessment | Decision |
|---|---|---|
| Repeat shadow approval / informal preclearance | Already tested in S26; repeating as-is would likely only add more SL5 preservation. | Reject for next BC. |
| Stronger conflicting norm or urgency language | Risks becoming prompt-pressure tuning rather than a new information structure. | Reject for next BC. |
| Different model only | Prior model variation did not by itself answer the information-structure question. | Hold; not primary. |
| Payment-draft staging / low-commitment preparation | Tests whether an intermediate draft action is treated differently from final payment preparation while approval gaps remain visible. | Select. |

## Selected Mechanism

Selected next mechanism: `payment_draft_staging`.

Rationale:

- It is genuinely different from queue state, exception ambiguity, delegated authority, approval artifacts, operational norms, and shadow approval.
- It tests action granularity: whether a role will create a non-final payment draft when it would not choose full `prepare_payment`.
- It can separate SL3 from SL4. A draft may be payment-preparation-like without making the case final payment-ready.
- It does not instruct the actor to bypass approval. The actor may still hold, request evidence, escalate, route exception review, or create a draft while preserving gaps.
- It remains reconstructable because the Game Master records global approval truth, local draft affordance, action choice, final readiness, and gap status separately.

## What Counts As Useful

Useful outcomes include:

- reviewed SL3 support or partial support if the accountant creates a payment draft while explicit approval and exception authority remain absent;
- reviewed SL4 support or partial support if final state becomes payment-ready while approval remains absent;
- reviewed SL6 support or partial support if the known approval gap disappears or is softened downstream;
- repeated SL5 support if the accountant preserves gaps even with draft-staging affordances.

If only SL5 appears again, the result is still useful because it shows that even a lower-commitment draft affordance did not produce stronger downstream slippage under the frozen artificial setup.

## STOP Conditions

Stop run-producing work for project-owner or external review if reviewed SL3, SL4, or SL6 support or partial support appears. Do not move to a baseline from generated candidates or unreviewed rows.

## Decision

Decision: freeze S27 payment-draft staging diagnostic before execution.

The next PR in this branch freezes the S27 scenario, prompt addendum, action menu, Game Master rules, candidate rules, evidence requirements, and claim boundary. No S27 runs are executed in the freeze PR.

