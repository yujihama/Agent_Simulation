# Phase 4 Reflection: Correct S32 Direction And Select Gray-Option Seeding

Date: 2026-05-19
Status: accepted
Phase: Phase 4 extension
Checkpoint: BC4-S33 mechanism selection
Related S31 synthesis: `docs/synthesis/phase4-advisor-seeded-structuring-synthesis-v0.1.md`
Related S32 protocol: `protocols/failure-modes/phase4-recommendation-weighted-advisor-structuring-diagnostic-v0.1.md`
Selected next mechanism: `gray_option_seeded_structuring`
Claim boundary: `phase4_mechanism_selection_only`

## Purpose

This reflection corrects the next Phase 4 direction before any S32 execution result is committed.

S31 showed that a neutral advisor can generate split-like within-control options, but requester/buyer did not select those options. S32 froze a recommendation-weighted advisor protocol, but the protocol still frames the advisor as an ordinary operational advisor. That role is likely to recommend conservative, control-preserving processing because the visible control gap is explicit.

The project-owner direction is to test a different social information mechanism: not a general advisor recommending the safest processing path, but a role that surfaces "gray" processing ideas under pressure. This is closer to the organizational pattern where applicants do not invent shortcuts from scratch; another person or tool suggests process-simplifying ideas that remain inside normal system records.

## Design Correction

Do not execute S32 as the next run-producing diagnostic.

S32 remains a frozen protocol artifact, but it is deferred before execution because it does not sufficiently implement the intended "bad-idea / gray-idea seeding" mechanism.

The next mechanism should explicitly separate:

1. gray-option ideation;
2. deterministic outside-control filtering;
3. requester/buyer selection from accepted gray and conservative options;
4. later candidate review.

## Selected Mechanism

The selected next mechanism is `gray_option_seeded_structuring`.

Plain-language description:

A gray-option ideation advisor is asked to generate handling ideas that an operator might raise under deadline, queue, or prior-practice pressure. The advisor should include conservative options and operationally gray but within-control options, such as separate packet handling or split submission with weakened aggregate-note prominence. A deterministic filter rejects outside-control options before requester/buyer sees them.

This mechanism tests whether gray-option availability, not just neutral option availability, changes applicant-side selection.

## Scope Boundary

The mechanism remains within-control only.

Allowed within-control gray ideas may include:

- separate invoice packets with aggregate context preserved;
- separate invoice packets with weaker aggregate-note prominence while source records remain genuine and traceable;
- routing individual packets for queue handling while preserving global aggregate truth;
- requesting aggregate review in parallel with packet preparation;
- holding payment readiness while moving a non-payment processing packet forward.

Out of scope:

- forged approval;
- fake invoices;
- hidden, deleted, or modified evidence;
- impersonation;
- collusion;
- unauthorized access;
- privilege escalation;
- instructions to bypass approval;
- instructions to avoid thresholds through deception.

## Why This Is Different From S31 And S32

S31: neutral advisor-generated options were added to the menu.

S32: an ordinary advisor would recommend one option, but the role is still expected to behave like a careful processing advisor.

S33: a gray-option ideation role is explicitly asked to surface boundary-stretching but still within-control ideas. This tests the upstream idea-seeding mechanism more directly without instructing fraud or concealment.

## Useful Outcomes

S33 is useful even if requester/buyer remains conservative:

- If gray split options are generated and selected, S33 may add bounded SL2 applicant-side evidence after review.
- If gray split options are generated but not selected, S33 strengthens the finding that applicant-side selection remains conservative even when gray ideas are surfaced.
- If the ideation advisor generates outside-control options, deterministic filtering should reject them and demonstrate the safety boundary.
- If no gray options are generated, the prompt may still be too conservative and future work should pause or redesign the mechanism before more runs.

## Decision

Freeze an S33 gray-option seeded structuring diagnostic.

Do not execute S33 until the protocol is frozen.

Do not claim gray-option seeding produces process drift until a later frozen execution and candidate review supports that status.
