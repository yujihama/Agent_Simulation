# Method B Failure-Mode Baseline Decision v0.1

Date: 2026-05-17
Status: accepted
Phase: Method B
Checkpoint: BC26
Covers: C16, C17, C18, C20
Supersedes: none
Related protocols: `protocols/failure-modes/failure-mode-taxonomy-v0.1.md`; `protocols/failure-modes/method-b-failure-mode-review-v0.1.md`
Related review: `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/failure-mode-review-0001/summary.md`

## Purpose

BC26 was originally intended to freeze a controlled Method B failure-mode baseline protocol after BC25 human/delegated review identified at least one supported or partially supported failure-mode target.

BC25 did not identify any supported or partially supported Method B failure-mode target. Therefore the precondition for a controlled failure-mode baseline is not met.

This decision records that BC26 does not freeze a baseline protocol. It also records why BC27 baseline execution is not executable from the current evidence state.

## Precondition Check

| Field | Required for baseline freeze | BC25 state |
|---|---|---|
| Generated candidate rows | At least one plausible candidate is useful, but not sufficient | 0 |
| Supported reviewed rows | At least one required | 0 |
| Partially supported rows needing revision | May support a revised protocol if explicitly scoped | 0 |
| Rejected candidate rows | May guide revisions | 0 |
| Representative evidence packs reviewed | Required | 6 |
| Candidate/support boundary preserved | Required | yes |

## Decision

Checkpoint decision: do not freeze a controlled Method B failure-mode baseline protocol in BC26.

BC27 controlled baseline execution is not executable because there is no frozen baseline protocol and no supported failure-mode target set.

This is not a project failure. It is a negative checkpoint result: the current high-friction scenario, prompt, action menu, Game Master, memory, and post-hoc explanation setup did not produce reviewed support for the targeted Method B failure modes.

## Rationale

- Freezing a baseline without a supported target would turn a no-observation pilot into an unsupported experiment.
- Changing prompts, menus, Game Master strictness, memory policy, or post-hoc explanation structure inside BC26 would violate the result-before-protocol boundary.
- Treating `not_observed` as proof of absence would overclaim.
- The next useful step is diagnostic protocol work that changes one design axis at a time before any future baseline.

## Next Direction

The next feasible Method B step should be a diagnostic sensitivity or revised targeting protocol, not a failure-mode baseline execution.

Candidate diagnostic axes:

- prompt framing;
- action menu breadth;
- Game Master strictness;
- memory richness;
- post-hoc explanation presence;
- scenario targeting.

Any such diagnostic protocol must be frozen before execution and must preserve the same claim boundaries.

## Claim Boundary

Allowed claim:

- BC26 checked the baseline-freeze preconditions and found that no controlled failure-mode baseline can be frozen from the current reviewed evidence.

Forbidden claims:

- Method B failure modes are absent in general;
- S09/S12 failed as scenarios;
- the current prompts, menus, or Game Master prove safe behavior;
- any human behavior, real-world organization, statistical, causal, compliance, legal, audit, operational, model-comparison, or general LLM behavior conclusion.

## Non-Goals

BC26 does not:

- execute new runs;
- revise BC24 or BC25 results;
- change scenarios, prompts, action menus, Game Master rules, event taxonomy, metrics, schemas, or evidence-pack requirements;
- freeze a baseline run count;
- add baseline results;
- claim failure-mode absence.
