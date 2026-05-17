# Comparison With Org-Payment Method B Evidence

Claim boundary: `method_b_second_domain_transfer_review_only`

## Org-Payment Reference

The BC28 diagnostic sensitivity package is the current Method B org-payment reference:

- `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/aggregate.json`
- attempted runs: 10
- accepted runs: 10
- generated FM6 candidate rows: 3
- generated FM1-FM5 candidate rows: 0

The BC28 FM6 rows are generated candidates only. They are not human-reviewed supported findings.

## Expense-Reimbursement Reference

The EXP-0005 second-domain package is the current expense-reimbursement reference:

- `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/aggregate.json`
- attempted runs: 5
- accepted runs: 5
- reviewed representative path: `request_approval -> request_more_evidence -> hold_payment`

## Comparison

| Area | Org-payment BC28 | Expense reimbursement EXP-0005 review |
|---|---|---|
| FM1-FM5 generated/reviewed support | No generated candidates in BC28 | Reviewed as not observed in representative EXP-0005 evidence |
| FM6 post-hoc justification | 3 generated candidates, not supported | Not assessable because EXP-0005 lacks post-hoc explanations |
| Evidence-pack validity | Representative packs validate | Representative pack validates |
| Transfer claim | Not supported | Not supported |

## Conclusion

BC29 does not establish Method B transfer across domains. It shows that the failure-mode mapping can be written and applied to existing expense-reimbursement evidence, but the only current org-payment candidate type, FM6, requires post-hoc explanation artifacts that EXP-0005 does not contain.

A future second-domain Method B pilot would need a frozen protocol that adds post-hoc explanations before FM6 transfer can be tested.
