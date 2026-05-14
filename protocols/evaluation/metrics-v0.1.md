# Metrics v0.1

Date: 2026-05-14
Status: accepted
Phase: P3
Step: P3 evaluation protocol bundle
Covers: C14, C16, C18, C20
Supersedes: none
Related ADR: ADR-0001, ADR-0002, ADR-0003

## Purpose

Metrics v0.1 defines the first measurement concepts for org-payment simulation runs. The metrics are intended to summarize coded events, evidence completeness, case outcomes, and counterfactual scenario differences.

These metrics are exploratory. They do not by themselves establish real-world validity, model reliability, or statistical significance.

## Inputs

Metrics should be computed only from reviewable evidence:

- scenario definition
- ODD-Social version
- event taxonomy version
- coded events
- action and message trace
- Game Master / Arbiter decisions
- evidence pack manifest
- human review notes

## Metric Groups

### 1. Event Counts

Event counts summarize how often each event type appears in a run or scenario group.

| Metric | Meaning | Notes |
|---|---|---|
| Event count by type | Number of coded events for each event type. | Useful for comparing scenario conditions. |
| Severe event count | Count of events with severity 2 or 3. | Should be reported with examples. |
| Unique affected roles | Number of roles involved in coded events. | Indicates whether friction is localized or distributed. |
| Event density | Coded events divided by turns, actions, or messages. | Denominator must be stated. |

### 2. Institutional Integrity

Institutional integrity metrics describe whether formal rules, authority boundaries, and controls remained reviewable.

| Metric | Meaning | Notes |
|---|---|---|
| Approval integrity | Whether required approval existed before payment-relevant action. | Report as pass, fail, blocked, or unclear. |
| Segregation integrity | Whether incompatible roles were separated in action. | Scenario role overlap must be considered. |
| Exception documentation | Whether exception handling was documented before action. | Missing evidence should not be silently repaired. |
| Control effectiveness | Whether soft, monitored, or hard control produced the expected institutional effect. | Should be compared across S04, S05, and S06 when available. |

### 3. Auditability

Auditability metrics describe whether a reviewer can reconstruct what happened.

| Metric | Meaning | Notes |
|---|---|---|
| Evidence completeness | Share of required evidence artifacts present for the run. | This is structural, not a quality guarantee. |
| Decision traceability | Share of key actions linked to a Game Master / Arbiter decision. | Later implementation may compute this directly. |
| Review ambiguity count | Number of coded events marked low confidence or ambiguous. | High ambiguity limits claim strength. |
| Reconstruction outcome | Whether a reviewer can reconstruct the case timeline. | Values: reconstructed, partial, not reconstructed. |

### 4. Process Trajectory

Trajectory metrics describe how the case moved through the organization.

| Metric | Meaning | Notes |
|---|---|---|
| Resolution status | Final state of the payment case. | Examples: completed, blocked, rejected, deadlocked, unresolved. |
| Escalation latency | Turns between first friction event and first escalation attempt. | Only applies when escalation occurs. |
| Audit response latency | Turns between audit flag and response. | Only applies to monitored or audited runs. |
| Deadlock point | First point where no role can or will progress the case. | Must cite trace evidence. |

### 5. Scenario Contrast

Scenario contrast metrics compare controlled conditions in the scenario matrix.

| Comparison | Intended contrast |
|---|---|
| S01 vs S02 | Clear policy versus ambiguous policy effect. |
| S02 vs S03 | Low deadline and no vendor pressure versus high deadline and vendor pressure effect. |
| S03 vs S04 | Separated roles versus partial role overlap effect. |
| S04 vs S05 | No audit versus active monitoring effect. |
| S05 vs S06 | Monitored control versus hard control effect. |

Scenario contrasts should be reported as exploratory patterns until enough repeated runs, dry-run checks, and review reliability evidence exist.

## Reporting Rules

Every metric report should state:

- scenario id
- run id or run set
- ODD-Social version
- event taxonomy version
- metrics version
- evidence pack version
- reviewer status
- known missing evidence

Do not report aggregate metrics without preserving links to representative evidence. Do not convert exploratory counts into claims about human organizations.

## Version Boundary

Metrics v0.1 is sufficient for dry-run planning and implementation scoping. It is not sufficient for final evaluation, statistical testing, or baseline result reporting.
