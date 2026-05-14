# ODD-Social v0.1

Date: 2026-05-14
Status: accepted
Phase: P1
Step: P1/P2 design bundle
Covers: C04, C05, C06, C07, C08, C11
Supersedes: none
Related ADR: ADR-0001, ADR-0002, ADR-0003

## Purpose

ODD-Social v0.1 extends the ODD model-description style for small artificial organizations where social friction and institutional failure can be studied without implementing code first.

The protocol describes:

- what entities exist in the artificial organization
- what state they can observe or affect
- which institutional rules constrain action
- how social structure and pressure shape interaction
- which scenario variables are intentionally manipulated

ODD-Social does not define event taxonomy, metrics, evidence pack structure, schema validation, implementation code, or experiment results. Those belong to later evaluation and implementation PRs.

## Required Sections

Each ODD-Social scenario or domain model should include the following sections.

### 1. Overview

- Purpose
- Research positioning
- Domain boundary
- Entities
- State variables
- Process overview
- Scheduling assumptions
- Termination condition

### 2. Design Concepts

- Emergence
- Adaptation
- Objectives
- Learning or memory
- Sensing
- Interaction
- Stochasticity
- Collectives
- Observation

### 3. Details

- Initialization
- Input artifacts
- Submodels
- Randomness policy
- Run boundary
- Non-goals

### 4. Institution Extension

- Formal rules
- Informal norms
- Authority model
- Segregation of duties
- Exception handling
- Auditability
- Sanctions
- Control mode

### 5. Social Structure Extension

- Role assignment
- Hierarchy
- Dependency relation
- Trust network
- Information asymmetry
- Communication channels
- Private goals
- Public obligations

### 6. Chaos Factors Extension

- Policy ambiguity
- Deadline pressure
- External pressure
- Workload
- Role overlap
- Blame avoidance
- Informal norm strength
- Memory persistence

## Org-Payment v0.1 Model Summary

The initial ODD-Social domain is `org-payment`, a small artificial organization handling payment, procurement, and approval work.

### Entities

- payment case
- requester
- buyer
- approver
- accountant
- manager
- vendor contact
- auditor
- policy document
- invoice
- approval record
- message thread
- audit log

### State Variables

| State variable | Description |
|---|---|
| case_id | Stable identifier for the payment case. |
| amount | Requested payment amount. |
| vendor | External vendor associated with the invoice. |
| policy_clarity | Whether payment policy is clear, ambiguous, or contradictory. |
| deadline_pressure | Low, medium, or high pressure to complete the case. |
| control_mode | Soft, monitored, or hard institutional control. |
| approval_status | Not requested, requested, approved, rejected, or bypassed. |
| current_handler | Role currently expected to act. |
| audit_presence | None, passive, or active. |
| role_overlap | Whether requester, buyer, approver, and accountant responsibilities are separated or overlapping. |
| communication_state | Open questions, warnings, informal side-channel messages, and unresolved disagreements. |
| record_completeness | Whether key decision and approval records are complete enough for later review. |

### Process Overview

1. A requester asks for payment or purchase handling.
2. A buyer or handler reviews the case and invoice.
3. An approver decides whether the request can proceed.
4. An accountant prepares or records the payment action.
5. A vendor may apply time or relationship pressure.
6. A manager or auditor may intervene depending on scenario conditions.
7. The Game Master / Arbiter applies institution rules and records outcomes.

### Institutional Assumptions

- The organization has formal payment and approval rules.
- Informal norms may encourage speed, deference to managers, or avoidance of escalation.
- Soft control permits questionable action unless blocked socially or procedurally.
- Monitored control allows action but records or flags questionable behavior.
- Hard control blocks actions that violate authority or policy.

### Social Assumptions

- Agents have role obligations and private incentives.
- Agents may face deadline pressure, vendor pressure, hierarchy pressure, or ambiguity.
- Agents may use official or informal communication channels.
- Agents may justify decisions after the fact.
- Agents do not directly mutate world state; the Game Master / Arbiter decides outcomes.

## Version Boundary

ODD-Social v0.1 is sufficient for defining the first artificial organization and scenario matrix. It is not sufficient for evaluation, scoring, or experiment execution.

Expected next protocol work:

- event taxonomy v0.1
- metrics v0.1
- evidence pack v0.1
- human review protocol v0.1
