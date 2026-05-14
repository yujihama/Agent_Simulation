# Org-Payment Control Modes

Date: 2026-05-14
Status: accepted
Phase: P1
Step: P1/P2 design bundle
Covers: C06, C09, C11
Supersedes: none
Related ADR: ADR-0002, ADR-0003

Control modes describe how the Game Master / Arbiter should handle proposed actions under institution rules. This file defines expected behavior only; it does not implement enforcement.

## Soft Control

Soft control allows the organization to rely on roles, communication, and policy interpretation. Questionable actions may proceed unless another participant objects or the Game Master determines that a hard domain boundary is violated.

Expected effects:

- More room for ambiguity.
- More reliance on informal clarification.
- Fewer automatic blocks.

## Monitored Control

Monitored control allows some questionable actions to proceed but records, flags, or exposes them for review.

Expected effects:

- Actions may still occur under pressure.
- Audit visibility changes participant behavior.
- Review material is easier to reconstruct.

## Hard Control

Hard control blocks proposed actions that violate defined authority, approval, or segregation-of-duties rules.

Expected effects:

- Unauthorized payment handling is prevented.
- Participants may seek alternate justifications or escalation paths.
- Some failures may shift from action failure to communication or process deadlock.

## Game Master Boundary

The Game Master / Arbiter decides whether a proposed action:

- proceeds
- proceeds and is flagged
- requires clarification
- is rejected
- is blocked by hard control

This decision must be recorded in later evidence-pack work, but this PR does not define that evidence format.
