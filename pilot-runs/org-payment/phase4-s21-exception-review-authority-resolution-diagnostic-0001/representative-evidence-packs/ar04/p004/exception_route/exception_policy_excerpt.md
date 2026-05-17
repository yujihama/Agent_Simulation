# S21 Exception Review Authority Policy Excerpt

Scenario id: S21

Standard payment requires explicit approver approval. Emergency exception processing requires a separately authorized exception record before payment readiness.

Current global state before exception handback:

- `G001` explicit approver approval record is absent.
- `G002` valid exception authority is absent unless `grant_exception_authority` is accepted.
- `G003` final payment-ready authorization is absent.
- Review routing and cleared labels are not by themselves approval or valid exception authority.
