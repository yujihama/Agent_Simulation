# ADR-0003: Initial Domain Org Payment

Date: 2026-05-14
Status: accepted
Phase: P0
Step: PR-C
Covers: C03; domain context for C05, C06, C11, C13, C20
Supersedes: none
Related ADR: ADR-0001, ADR-0002

## Context

The project needs an initial domain small enough for controlled scenarios but rich enough to contain institutional friction, authority boundaries, evidence, and auditability.

Prior drafts identify payment, procurement, and approval work as a useful initial artificial society because it naturally includes monetary amounts, approvals, segregation of duties, external vendor pressure, deadlines, exception handling, and audit logs.

## Decision

The initial domain is `org-payment`: a small artificial organization handling payment, procurement, and approval work.

The domain may include:

- payment requests
- invoices
- purchase or procurement context
- approval status
- authority and segregation-of-duties rules
- accounting or payment handling
- vendor communication
- deadlines and pressure
- audit logs and review evidence

The initial domain should support events such as:

- duplicate payment
- approval bypass
- self-approval
- wrong-handler action
- evidence gap
- audit-log gap
- amount inconsistency
- responsibility diffusion
- after-the-fact justification

The initial domain excludes:

- real company data
- real vendor data
- bank API integration
- tax processing
- production payment execution
- legal advice or compliance certification
- claims that simulated behavior directly predicts real organizations

## Alternatives considered

1. Start from a general-purpose social simulation.
   - Rejected because it would be too broad for early event taxonomy and evidence design.

2. Start from a purely technical AI-agent task benchmark.
   - Rejected because it would not naturally test institutional failure mechanisms.

3. Start from a high-stakes real domain such as healthcare triage or disaster allocation.
   - Deferred because those domains raise heavier ethical and domain-validity requirements before the evidence protocol is ready.

4. Start from a different organizational domain such as expense reimbursement or contract review.
   - Deferred as later domain expansion candidates after `org-payment` validates the basic framework.

## Consequences

- PR-D should define ODD-Social v0.1 in a way that can describe `org-payment` without embedding implementation details.
- PR-E should define the initial scenario matrix around clear policy, ambiguous policy, pressure, role overlap, monitored control, and hard control.
- Domain-specific events should be separated from general institutional failure concepts where possible.
- Ethics boundaries remain important because the domain includes rule-bending, pressure, and simulated control failures.

## Follow-up

- Define ODD-Social v0.1 for the `org-payment` artificial society.
- Define the S01-S06 scenario matrix for initial comparisons.
- Later evaluate whether event taxonomy is overly tied to payment work before expanding to a second domain.
