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
- `s01-clear-policy-low-pressure.yaml`: clear policy, low pressure baseline
- `s02-ambiguous-policy-low-pressure.yaml`: policy ambiguity comparison
- `s03-ambiguous-policy-high-pressure.yaml`: deadline and vendor pressure comparison
- `s04-role-overlap-high-pressure.yaml`: role overlap comparison
- `s05-audit-intervention.yaml`: monitored control comparison
- `s06-hard-control.yaml`: hard control comparison

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
