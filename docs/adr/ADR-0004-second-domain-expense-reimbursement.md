# ADR-0004: Select Expense Reimbursement as the Second Domain

Date: 2026-05-17
Status: accepted
Phase: P10
Checkpoint: BC19
Touches: C03, C08, C10, C11, C12, C16, C18, C19, C20

## Context

The initial domain is org-payment. It has enough protocol, scenario, runner, evidence-pack, review, construct-validity, intervention, and sensitivity artifacts to test the next question: whether the research infrastructure can move beyond a single payment workflow without overclaiming generality.

The second domain should be close enough to reuse the action-proposal, Game Master, trace, evidence-pack, metrics, and validator concepts, but different enough to expose org-payment-specific assumptions.

Candidate domains considered:

- expense reimbursement
- procurement
- contract review
- incident response
- access management
- disaster supply allocation
- school rule enforcement

## Decision

Use `expense-reimbursement` as the second domain for the first domain-expansion pilot.

The first pilot is intentionally narrow:

- one scenario: `ER01`
- three LLM-controlled roles: `employee`, `manager`, `finance_reviewer`
- one reimbursement case involving an ambiguous receipt/policy situation
- deterministic menu-aware Game Master
- existing action-proposal, trace, event, metric, evidence-pack, and validation contracts

## Rationale

Expense reimbursement is adjacent to org-payment but not identical:

- It still involves approval, evidence, policy ambiguity, and finance processing.
- It shifts the initiating actor from a business requester/vendor payment flow to an employee claim flow.
- It tests whether evidence gaps and ambiguous approval can be represented without vendor pressure as the primary driver.
- It can reuse existing action vocabulary such as `send_message`, `request_approval`, `approve_payment`, `request_more_evidence`, `hold_payment`, `prepare_payment`, and `escalate`.
- It avoids adding a new event taxonomy before the transfer test.

This is not a claim that expense reimbursement is representative of all institutions or organizations. It is a controlled transfer test for the existing research machinery.

## Consequences

The project will add a frozen EXP-0005 second-domain pilot protocol before any execution.

The execution PR must not change:

- ER01 scenario definition
- prompt templates
- action menus
- parser retry rules
- deterministic Game Master handling
- event taxonomy
- metrics protocol
- evidence-pack requirements
- claim boundary

If EXP-0005 requires new action types or event labels, execution should stop and a separate protocol/schema revision PR should be created before continuing.

## Non-Claims

This ADR does not claim:

- the project generalizes beyond org-payment
- expense reimbursement is representative of human organizations
- the existing event taxonomy is complete for all domains
- a second-domain pilot is a real-world validation
- any statistical, causal, compliance, legal, audit, or operational conclusion
