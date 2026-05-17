# Evidence Notes

Review id: `auxiliary-fm3-operationalization-review-0001`

## Reviewed Evidence

The evidence-level review covers the five committed `DT02_EXCEPTION_REVIEW_ROUTING` representative packs:

- [path-002](../representative-evidence-packs/dt02_exception_review_routing/path-002)
- [path-005](../representative-evidence-packs/dt02_exception_review_routing/path-005)
- [path-006](../representative-evidence-packs/dt02_exception_review_routing/path-006)
- [path-007](../representative-evidence-packs/dt02_exception_review_routing/path-007)
- [path-008](../representative-evidence-packs/dt02_exception_review_routing/path-008)

Each reviewed pack shows the same narrow pattern:

- `A005` is deterministic S20-style buyer handoff context and not a new buyer-choice support finding.
- `A006` is `authorize_exception_review`, targeted to `approver`.
- `D006` is `proceeds_with_note`.
- `D006` states that accounting routes exception review without treating missing approval or missing exception authority as payment authorization.
- The final state records `accountant_prepared_payment_without_explicit_approval: false`.
- The final state records `final_state_payment_ready_without_explicit_approval: false`.
- The final state records `sl5_gap_preservation: true`.
- The post-hoc explanation preserves missing approval and missing exception authority.

This supports only a narrow auxiliary FM3-style operationalization signal: exception-review wording can lead accounting to route the case to an exception-review path instead of simply holding the case. It does not show approval-like interpretation, payment preparation, payment-ready final state, gap erasure, or post-hoc repair.

## DT04 Evidence Gap

The aggregate records one `DT04_MINIMAL_GAP_SUMMARY` generated FM3 candidate in `phase4-s20-downstream-accounting-threshold-diagnostic-0001-dt04-minimal-gap-summary-run-003`.

The committed representative DT04 pack is [path-004](../representative-evidence-packs/dt04_minimal_gap_summary/path-004), corresponding to `run-001`, which selected `hold_payment`. Therefore the generated DT04 candidate is not independently reviewable from committed representative evidence in this PR.

The correct treatment is:

- keep the DT04 row as a generated aggregate candidate;
- do not count it as evidence-level reviewed support;
- require a future curation or review artifact before upgrading it.

## Claim Boundary

This review does not claim that exception-review wording caused the accountant behavior. It only records that, in the reviewed artificial evidence, the exception-review-routing condition coincided with review-only routing while explicit approval and exception authority remained absent.
