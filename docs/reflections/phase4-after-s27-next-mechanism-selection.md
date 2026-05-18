# Phase 4 Reflection After S27 And Next Mechanism Selection

Date: 2026-05-18
Status: accepted
Phase: Phase 4
Previous review: `docs/reflections/phase4-after-s27-project-owner-review.md`
Selected mechanism: `structuring_approval_splitting`
Claim boundary: `phase4_next_mechanism_selection_only`

## Purpose

This reflection records the mechanism-selection decision after the S27 project-owner review and the research scope-axis revision in `docs/research/within-control-process-drift-scope-v0.1.md`.

It adds no runs, scenarios, candidates, result artifacts, baseline, or claim upgrade.

## Current Evidence Position

Current Phase 4 evidence is bounded:

- lossy handoff produced narrow SL2 buyer-side handoff support;
- S27 payment-draft staging produced narrow SL3 partial support for `create_payment_draft`;
- many other tested mechanisms reinforced SL5 evidence-gap preservation;
- SL4 final payment-ready state remains unsupported;
- SL6 evidence-gap erasure remains unsupported;
- full approval bypass remains unsupported;
- fraud, intentional misconduct, human behavior, real-world organization behavior, statistical significance, and audit/compliance sufficiency remain unsupported.

S27 resolved one classification blocker but did not justify baseline discussion by itself. The result remains a narrow artificial-system finding with visible approval and exception-authority gaps preserved.

## Scope-Axis Implication

PR #131 changed the forward-looking scope axis from intent to control perimeter:

- in scope: actors use their own assigned authority, system operation records match the actual operator, and evidence is not forged, hidden, modified, or fabricated;
- out of scope: impersonation, forged or hidden evidence, collusion, unauthorized access, privilege escalation, or malicious bypass.

This makes structuring / approval splitting a valid Phase 4 information-structure mechanism when it remains within-control.

## Mechanism Comparison

| Mechanism | Current status | Reason not to repeat as-is |
|---|---|---|
| Lossy handoff | Produced narrow SL2 and downstream SL5. | Already tested; did not produce SL3/SL4/SL6. |
| Queue/ticket mismatch | Produced SL5 preservation. | Status label did not overcome visible approval gaps. |
| Exception route ambiguity | Produced SL5 preservation in accepted runs. | Exception language did not create stronger downstream drift. |
| Approval artifact mismatch | Produced SL5 preservation. | Approval-like artifact did not displace authoritative approval fields. |
| Conflicting operational norms | Produced SL5 preservation. | Local practice did not overcome written approval gap. |
| Shadow approval / informal preclearance | Produced SL5 preservation. | Informal signal did not become formal approval or preparation. |
| Payment-draft staging | Produced narrow SL3 partial support. | Needs a different mechanism before further run-producing work. |
| Structuring / approval splitting | In scope, untried. | Tests individual-unit vs aggregate-control mismatch. |

## Selected Mechanism

Decision: freeze S28 `structuring_approval_splitting`.

Rationale:

- it is newly in scope under the within-control process drift axis;
- it changes the information structure from approval ambiguity to processing-unit granularity;
- it tests whether individual below-threshold units and aggregate approval/review requirements remain separated;
- it can target SL2, SL3, SL4, SL5, SL6, FM3, and FM6 without instructing actors to bypass controls;
- it is materially different from S27 because the key question is aggregate relationship and threshold review, not draft/payment-preparation affordance.

## Boundary

The S28 protocol must not:

- depend on forged records, hidden evidence, impersonation, collusion, unauthorized access, privilege escalation, or malicious bypass;
- infer hidden actor intent;
- instruct an actor to evade approval;
- treat individual approval, below-threshold amount, ticket readiness, local approval, or urgency as aggregate approval;
- claim real-world organization behavior, fraud, human behavior, statistical significance, prompt causation, or audit/compliance sufficiency.

## Checkpoint Decision

Proceed to BC4-S28-A: freeze a structuring / approval-splitting diagnostic protocol before any execution.

Execution must wait until the S28 protocol, scenario, prompt addendum, action menu, Game Master rules, visibility rules, candidate criteria, evidence-pack requirements, and claim boundary are frozen.
