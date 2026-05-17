# Phase 4 Mechanism Selection Framework v0.1

Date: 2026-05-17
Status: accepted
Phase: Phase 4
Checkpoint: BC4-1 mechanism selection framework
Claim boundary: `phase4_mechanism_selection_only`

## Scope

This reflection compares candidate organizational information mechanisms and selects one next mechanism for protocol freeze.

It adds no new runs, candidates, reviews, protocols, scenarios, prompts, metrics, schemas, validators, or empirical claim upgrades. It does not execute the selected mechanism.

## Why A New Mechanism Is Needed

Phase 3 concluded that current evidence supports:

- narrow SL2 buyer-side handoff under BC31 and S18;
- repeated downstream SL5 evidence-gap preservation;
- no support for SL3 accountant preparation without explicit approval;
- no support for SL4 final payment-ready state without explicit approval;
- no support for SL6 evidence-gap erasure.

Repeating S17/S18/S19-style diagnostics would likely produce more boundary-preservation evidence without changing the information structure. Phase 4 therefore requires a mechanism that is genuinely different from:

- direct SL2-SL4 progression stress;
- lossy buyer-to-accountant handoff;
- queue/ticket readiness mismatch.

The next mechanism must not tell roles to bypass approval. It should instead create a different artificial information condition and let the frozen review criteria decide whether SL2, SL3, SL4, SL5, or SL6 appears.

## Selection Criteria

| Criterion | Meaning |
|---|---|
| Novel information structure | The mechanism differs from S17/S18/S19, not just stronger pressure or prompt wording. |
| Target relevance | It can plausibly test unresolved SL levels, especially SL3, SL4, or SL6. |
| Reconstructability | Evidence packs can show global truth, role-local view, actions, GM decisions, and final state. |
| Non-coercive design | Roles are not instructed to violate controls or fabricate evidence. |
| Game Master boundary | GM retains global truth and deterministic menu-aware decisions. |
| Claim safety | Negative and conservative outcomes remain valid. |

## Candidate Mechanism Comparison

See the companion table:

- `docs/reflections/phase4-mechanism-candidate-table.csv`

## Tried And Untried Mechanisms

Already tried or closely covered:

- direct control-slippage progression stress: S17;
- lossy handoff: S18;
- queue/ticket state mismatch: S19;
- ambiguous approval targeting: BC31;
- evidence-gap erasure direct diagnostic: BC35;
- approval-bypass stress: BC37-C;
- responsibility-boundary stress with explicit approval: BC32.

Not yet tested as a dedicated Phase 4 mechanism:

- exception route ambiguity;
- conflicting operational norms;
- approval artifact mismatch;
- shadow approval or informal pre-clearance;
- delegated authority ambiguity;
- post-hoc audit reconstruction as a primary mechanism;
- stronger role-local context without lossy handoff.

## Selected Next Mechanism

Selected mechanism: `exception_route_ambiguity`.

Rationale:

- It is materially different from S17/S18/S19.
- It tests whether an unclear emergency, exception, or provisional-processing route affects downstream accounting decisions without instructing roles to bypass approval.
- It can target SL3 and SL4 more directly than lossy handoff because the accountant may face an ambiguous exception route, not just a weakened handoff summary.
- It can test SL6 because exception language could either preserve the unresolved approval gap or soften it into an apparent authorization.
- It remains reconstructable if the protocol separates normal approval, exception authority, role-local view, Game Master global truth, and final state.

## Selected Mechanism Boundary

The selected mechanism should not claim that exception processing is unsafe or that real organizations use exceptions this way.

The next protocol should freeze:

- one S20 org-payment scenario;
- five attempted runs;
- OpenAI `gpt-4.1-mini` unless changed by a later freeze;
- role-local visibility for buyer and accountant;
- scripted requester/vendor/approver context;
- explicit normal approval absence;
- ambiguous exception-route text;
- action menus that allow hold/request evidence/escalate as safe exits;
- Game Master rules that preserve global truth and distinguish explicit approval from exception-route ambiguity;
- SL1-SL6 candidate and review rules.

## Useful Outcomes

Useful outcomes include:

- SL3 or SL4 candidate/support if accountant or final state moves further than prior diagnostics;
- SL6 candidate/support if a known approval/exception gap is softened or erased downstream;
- SL5 support if the exception ambiguity is preserved and processing is blocked;
- `not_observed` for stronger targets if the mechanism still preserves boundaries.

No outcome should be treated as a human, real-world, statistical, compliance, legal, audit, operational, governance, or model-general finding.

## Non-Goals

This checkpoint does not:

- freeze a protocol;
- run a diagnostic;
- add result artifacts;
- change scenario definitions;
- change prompts or action menus;
- weaken the Game Master boundary;
- instruct roles to bypass controls;
- claim slippage has occurred.

## OK / STOP Condition Review

| Condition | Status |
|---|---|
| Candidate mechanisms are compared. | OK. |
| Tried and untried mechanisms are distinguished. | OK. |
| One next mechanism is selected. | OK: exception route ambiguity. |
| Selection is based on prior results. | OK. |
| Selected mechanism is not mere prompt strengthening. | OK. |
| Roles are not instructed to violate controls. | OK. |
| Game Master boundary remains intact. | OK. |
| Reconstructability remains required. | OK. |

## Checkpoint Decision

Decision: select `exception_route_ambiguity` for the next protocol-freeze BC.

Proceed to BC4-2: freeze a Phase 4 exception route ambiguity diagnostic protocol before any execution.
