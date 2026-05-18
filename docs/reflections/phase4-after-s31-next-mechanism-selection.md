# Phase 4 Reflection After S31: Next Mechanism Selection

Date: 2026-05-19
Status: accepted
Phase: Phase 4 extension
Checkpoint: BC4-S32 mechanism selection
Related S31 synthesis: `docs/synthesis/phase4-advisor-seeded-structuring-synthesis-v0.1.md`
Selected next mechanism: `recommendation_weighted_advisor_seeded_structuring`
Claim boundary: `phase4_mechanism_selection_only`

## Purpose

S31 tested neutral advisor-seeded option expansion. The advisor generated split-like within-control options, and deterministic filtering added accepted options to requester/buyer menus, but requester/buyer selected only canonical conservative options in all accepted runs.

This reflection selects the next mechanism without changing S31 artifacts or upgrading S31 claims.

## S31 Lesson

S31 separates two questions:

1. Can another LLM surface split-like or boundary-stretching options from pressure and threshold context?
2. Does the applicant select those options when they appear as neutral menu items?

S31 answered the first question yes in accepted runs, but answered the second question no under the frozen S31 setup.

Therefore, repeating neutral option seeding is unlikely to add new information. The next mechanism should test option provenance and recommendation force: whether a role treats an option differently when it is presented as a recommended operational path with visible rationale and caveats, rather than as one neutral item in a list.

## Selected Mechanism

The selected next mechanism is `recommendation_weighted_advisor_seeded_structuring`.

Plain-language description:

An operational advisor or senior processing coordinator reviews the visible pressure, threshold, and aggregate-review context, generates several within-control handling options, and marks one accepted option as the recommended handling path. The requester/buyer then chooses from a menu that includes canonical conservative options and accepted advisor options with recommendation metadata.

This tests whether a recommended option changes applicant choice under artificial pressure conditions.

## Why This Is Different From S31

S31 added options but kept them neutral. S32 adds provenance and recommendation weight:

- a named advisor source;
- one recommended option;
- visible recommendation rationale;
- visible caveats;
- explicit non-authority boundary saying the recommendation is not approval, exception authority, or final payment readiness.

The mechanism remains within-control. It does not ask any actor to forge records, hide evidence, bypass approval, avoid thresholds, impersonate another actor, collude, or use unauthorized access.

## Useful Outcomes

The diagnostic is useful even if requester/buyer remains conservative:

- If the recommended option is split-like and selected, S32 can add bounded applicant-side SL2 evidence under recommendation-weighted option provenance.
- If the recommended option is split-like but not selected, S32 strengthens the boundary-preservation finding that recommendation availability alone is insufficient under the current artificial setup.
- If the advisor does not recommend split-like options, S32 clarifies that even recommendation-weighted advisor framing stays conservative under the frozen prompt and scenario.
- If outside-control options appear, deterministic filtering should reject them and preserve the ethics boundary.

## STOP Conditions

The next protocol must stop before execution if:

- recommendation wording asks an actor to bypass approval, hide aggregate context, forge evidence, or avoid thresholds;
- recommendation metadata is treated as approval authority;
- rejected outside-control options are shown to requester/buyer;
- candidate classification depends on hidden intent;
- global truth and requester/buyer-visible context are not reconstructable.

## Decision

Freeze an S32 recommendation-weighted advisor structuring diagnostic before any execution.

Do not execute S32 in the mechanism-selection/protocol-freeze PR.

Do not claim that recommendation-weighted advisor seeding produces split submission until a later frozen execution and candidate review supports that status.
