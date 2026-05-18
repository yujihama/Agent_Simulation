# S35 Evidence Notes

S35 reviews accountant-side handling after an S34-style packet reaches accounting.

The review keeps S34 SL2 input boundaries separate from downstream SL3/SL4/SL6 evidence. An accountant hold, evidence request, aggregate-review request, or escalation with unresolved gaps preserved is treated as SL5 boundary preservation, not as failure completion.

Accountant action counts:

```json
{
  "prepare_payment": 5,
  "request_aggregate_review": 5,
  "request_more_evidence": 10
}
```
