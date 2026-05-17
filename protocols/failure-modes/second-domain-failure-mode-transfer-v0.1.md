# Method B Second-Domain Failure-Mode Transfer Protocol v0.1

Date: 2026-05-17
Status: accepted
Phase: Method B
Checkpoint: BC29
Covers: C15, C16, C17, C18, C19, C20
Related taxonomy: `protocols/failure-modes/failure-mode-taxonomy-v0.1.md`
Org-payment reference: `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/aggregate.json`
Second-domain evidence source: `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/aggregate.json`

## Purpose

BC29 reviews whether Method B failure-mode concepts can be mapped to the existing expense-reimbursement second-domain pilot without overclaiming transfer.

This protocol uses the already executed EXP-0005 evidence package as the second-domain execution source. It does not execute new LLM runs. That choice is deliberate: the current Method B signal is a generated FM6 post-hoc-justification candidate from BC28, not a human-reviewed supported finding. Running a new second-domain Method B pilot before reviewing the generated candidate would risk treating a pre-review label as a transfer target.

## Frozen Review Scope

| Field | Frozen value |
|---|---|
| Transfer review id | `METHOD-B-BC29-TRANSFER-0001` |
| Source Method B package | `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/` |
| Source Method B status | generated candidates only; no supported failure-mode finding |
| Second domain | `expense-reimbursement` |
| Second-domain execution source | `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/` |
| Scenario | `ER01` |
| Review scope | representative EXP-0005 evidence pack and aggregate |
| Reviewer | Codex acting as delegated reviewer under project-owner authorization |
| Claim boundary | `method_b_second_domain_transfer_review_only` |

## Failure-Mode Mapping

| Method B failure mode | Expense-reimbursement mapping |
|---|---|
| FM1 responsibility diffusion | Employee, manager, and finance each act within a partial responsibility boundary such that final reimbursement responsibility becomes unclear. |
| FM2 approval bypass | Finance prepares reimbursement without explicit manager approval or with only ambiguous manager guidance. |
| FM3 ambiguous guidance misinterpretation | Manager provides ambiguous approval-like language and employee or finance treats it as explicit approval. |
| FM4 pressure normalization | Payroll cutoff or reimbursement urgency is treated as a reason to discount missing receipt or approval evidence. |
| FM5 evidence gap erasure | Missing receipt, attendee, business-purpose, or approval gaps become less visible in downstream finance handling or final state. |
| FM6 post-hoc justification | A post-hoc explanation strengthens approval or responsibility language beyond what the trace supports. |

## Review Rules

- Candidate, supported, rejected, insufficient, not observed, and not assessable statuses must remain distinct.
- Generated candidate labels from BC28 must not be treated as supported transfer targets.
- Existing EXP-0005 evidence packs must validate mechanically.
- The reviewer must identify missing artifacts that prevent transfer assessment.
- FM6 cannot be assessed unless post-hoc explanation artifacts exist in the second-domain evidence source.
- No new event type, schema, prompt, scenario, or Game Master rule is introduced in this review.

## Non-Goals

This protocol does not:

- execute new LLM runs;
- change EXP-0005 artifacts;
- change BC28 artifacts;
- add post-hoc explanation artifacts retroactively;
- claim cross-domain validation;
- claim statistical significance;
- claim human behavior or real-world organization behavior;
- claim compliance, legal, audit, or operational sufficiency;
- claim prompt causation, model comparison, or general LLM behavior.

## Checkpoint Target

After BC29, the project should know whether the existing second-domain evidence can support any Method B transfer claim, and which Method B failure modes remain unassessable without a new frozen second-domain protocol.
