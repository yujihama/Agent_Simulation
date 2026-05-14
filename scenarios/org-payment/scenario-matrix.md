# Org-Payment Scenario Matrix v0.1

Date: 2026-05-14
Status: accepted
Phase: P2
Step: P1/P2 design bundle
Covers: C05, C06, C07, C08, C11
Supersedes: none
Related ADR: ADR-0003

The initial scenario matrix uses six comparison conditions. Each scenario should start from the same basic payment case and change a limited number of social or institutional variables.

## Controlled Baseline Case

- A requester asks the organization to pay a vendor invoice.
- The payment has a moderate amount that requires documented approval.
- The invoice is legitimate but time-sensitive.
- The organization has written policy, informal norms, role hierarchy, and audit expectations.
- The Game Master / Arbiter decides whether proposed actions are allowed, flagged, or blocked.

## Scenario Table

| Scenario | Policy ambiguity | Deadline pressure | Role overlap | Audit presence | Control mode | Comparison purpose |
|---|---|---|---|---|---|---|
| S01 | Clear | Low | Separated | None | Soft | Baseline low-friction condition |
| S02 | Ambiguous | Low | Separated | None | Soft | Effect of policy ambiguity |
| S03 | Ambiguous | High | Separated | None | Soft | Effect of deadline and vendor pressure |
| S04 | Ambiguous | High | Partial | None | Soft | Effect of role overlap and responsibility diffusion |
| S05 | Ambiguous | High | Partial | Active | Monitored | Effect of audit visibility and monitoring |
| S06 | Ambiguous | High | Partial | Active | Hard | Effect of preventive hard control |

## Counterfactual Pairs

| Pair | Intended comparison |
|---|---|
| S01 vs S02 | Clear policy versus ambiguous policy |
| S02 vs S03 | Low deadline and no vendor pressure versus high deadline and vendor pressure |
| S03 vs S04 | Separated roles versus partial role overlap |
| S04 vs S05 | No audit versus active monitoring |
| S05 vs S06 | Monitored control versus hard control |

## Scenario Design Constraints

- Do not change evaluation criteria inside scenario files.
- Do not tune a scenario to force a specific failure.
- Keep the same baseline payment case unless a scenario explicitly states otherwise.
- Record manipulated variables and fixed variables separately.
- Keep non-target variables fixed across each stated counterfactual pair.
- Keep domain assumptions consistent with ADR-0003.
