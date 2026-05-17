# Org-Payment Scenarios

Date: 2026-05-14
Status: accepted
Phase: P2
Step: P1/P2 design bundle
Covers: C03, C05, C06, C07, C08, C11
Supersedes: none
Related ADR: ADR-0003

This folder defines the initial `org-payment` scenario family for payment, procurement, and approval work.

The scenario family is designed to compare a small set of institutional and social conditions without introducing evaluation protocols, schemas, implementation code, experiment plans, or results.

## Files

- `scenario-matrix.md`: comparison matrix for S01-S06
- `high-friction-scenario-matrix.md`: Method B high-friction scenario matrix for S07-S12
- `s01-clear-policy-low-pressure.yaml`: clear policy, low pressure baseline
- `s02-ambiguous-policy-low-pressure.yaml`: policy ambiguity comparison
- `s03-ambiguous-policy-high-pressure.yaml`: deadline and vendor pressure comparison
- `s04-role-overlap-high-pressure.yaml`: role overlap comparison
- `s05-audit-intervention.yaml`: monitored control comparison
- `s06-hard-control.yaml`: hard control comparison
- `s07-ambiguous-delegated-authority.yaml`: ambiguous delegated authority scenario
- `s08-split-responsibility-deadline.yaml`: split responsibility under deadline scenario
- `s09-informal-pre-approval.yaml`: informal pre-approval scenario
- `s10-conflicting-policy-and-norm.yaml`: conflicting policy and norm scenario
- `s11-audit-visibility-workaround.yaml`: audit visibility with workaround scenario
- `s12-post-hoc-justification-setting.yaml`: post-hoc justification setting scenario

## Shared Model Inputs

- Organization model: `../../society/org-payment/organization.yaml`
- Role model: `../../society/org-payment/roles.yaml`
- Norm model: `../../society/org-payment/norms.yaml`
- Payment policy: `../../institutions/org-payment/policies.md`
- Control modes: `../../institutions/org-payment/control-modes.md`

## Non-Goals

- No event taxonomy is defined here.
- No metrics are defined here.
- No evidence pack protocol is defined here.
- No schema or implementation code is introduced here.
- No experiment is executed here.
