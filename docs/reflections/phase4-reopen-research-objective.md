# Phase 4 Research Objective Reopen

Date: 2026-05-17
Status: accepted
Phase: Phase 4
Checkpoint: corrective reopen
Claim boundary: `phase4_reopen_only`

## Purpose

This corrective note reopens Phase 4 as an active research objective.

Earlier synthesis correctly separated delivery completion from research completion, but it still leaned too far toward pausing run-producing work. That was not aligned with the user's current instruction: Phase 4 should continue until the project has enough evidence to identify which information structures can produce slippage candidates, or until a concrete blocker prevents further progress.

## Correction

Phase 4 should now be treated as:

- Delivery status: prior Phase 4 artifacts were delivered.
- Research status: open / incomplete.

The completed work shows:

- lossy handoff is currently the only tested mechanism that produced reviewed SL2 buyer-side handoff support;
- queue/ticket mismatch did not produce stronger slippage and reinforced SL5 evidence-gap preservation;
- exception-route ambiguity did not produce stronger slippage and reinforced SL5 evidence-gap preservation;
- no tested mechanism has produced reviewed SL3, SL4, or SL6 support.

Therefore, Phase 4 has not yet achieved its research objective.

## Active Research Objective

The active Phase 4 objective is:

> Identify which artificial organization information structures can produce reviewable non-intentional control-slippage candidates, especially whether any structure can move beyond narrow buyer-side SL2 handoff toward SL3 accountant preparation, SL4 final payment-ready state, or SL6 evidence-gap erasure.

This objective can be pursued through:

- more trials under a frozen protocol;
- model variation, including newer OpenAI models where available;
- prompt/persona variants, if frozen before execution;
- alternative information structures;
- analysis of why lossy handoff produced SL2 while S19/S20 did not.

## Guardrails

Future Phase 4 work must still preserve:

- protocol freeze before execution;
- raw output under ignored `runs/`;
- curated artifacts only under `pilot-runs/` or `results/`;
- candidate versus reviewed support separation;
- SL2, SL3, SL4, SL5, and SL6 separation;
- no baseline unless a later synthesis justifies it;
- no human behavior claim;
- no real-world organization claim;
- no statistical significance claim unless separately frozen and justified;
- no compliance, legal, audit, operational, governance, or safety sufficiency claim;
- no prompt-causation or model-general claim from exploratory diagnostics.

## Next BC Direction

The next BC should not merely repeat S20.

It should first freeze a research-completion-aware exploration protocol that can test:

- information-structure variation;
- run count variation;
- model variation;
- prompt/persona variation;
- candidate criteria for SL2, SL3, SL4, SL5, and SL6;
- review criteria after candidate generation.

The protocol must define, before execution, what would count as:

- delivery completion;
- research progress;
- research completion;
- stop or retarget conditions.

## Checkpoint Decision

Decision: reopen Phase 4 research work.

Proceed to a new Phase 4 exploration protocol freeze before any additional execution.

## Post-S27 Update

S27 payment-draft staging later produced project-owner-confirmed `SL3 partially_supported_needs_revision` for `create_payment_draft`. This supersedes the earlier "no tested mechanism has produced reviewed SL3 support" status for current Phase 4 tracking.

The update is narrow:

- no SL3a / SL3b split is introduced;
- SL5 evidence-gap preservation remains supported because approval and exception gaps remained visible;
- SL4 final payment-ready state remains unsupported;
- SL6 evidence-gap erasure remains unsupported;
- full approval bypass remains unsupported.
