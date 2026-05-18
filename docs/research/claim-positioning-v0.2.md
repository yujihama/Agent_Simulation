# Claim Positioning v0.2

Date: 2026-05-17
Status: accepted
Phase: Phase 1
Checkpoint: BC1-1 research objective reframing
Claim boundary: `claim_positioning_reframing_only`

## Scope

This document states how project claims should be positioned after the current evidence base and the Method B+ endpoint. It adds no new run, result, protocol, scenario, prompt, candidate review, or metric.

Post-scope-axis update: forward-looking project claims should use `Within-Control Process Drift` for the research target and `within-control / outside-control` for scope classification. Do not use hidden or self-reported intent to decide whether an observation is in scope.

## Claim Positioning Principle

The project should use the weakest claim that accurately represents the evidence.

Artificial-system observations should not be promoted into human, real-world, causal, statistical, compliance, legal, audit, operational, or model-general claims.

## Claim Levels

| Claim level | Meaning | Example |
|---|---|---|
| `supported_artifact_claim` | A repository artifact, protocol, schema, validator, runner, or documented decision exists and can be inspected. | The project has an evidence-pack validator. |
| `bounded_observation_claim` | A frozen artificial run produced a recorded descriptive outcome. | EXP-0002 produced 30 accepted org-payment baseline runs. |
| `reviewed_evidence_claim` | A reviewed artifact supports a bounded interpretation in the reviewed scope. | EXP-0002 representative packs were accepted for reconstruction in human review. |
| `construct_validity_limited_claim` | A construct is usable only within an explicitly reviewed scope and interpretation limit. | `evidence_gap` is supported for reviewed EXP-0002 representative-pack descriptions. |
| `bounded_artificial_system_claim` | A project-level pattern is supported only within artificial-system artifacts. | Method B+ often preserved downstream approval/evidence gaps under current protocols. |
| `boundary_limited_observation_claim` | A finding is real but limited to one stage or boundary. | Narrow SL2 buyer handoff appeared in BC31 and S18. |
| `hypothesis_for_future_work` | A claim can guide future study but is not yet a validated finding. | Artificial organizations may help generate hypotheses about institutional friction. |

## Method B+ Positioning

Method B+ should be positioned as a control-boundary and evidence-methodology result.

Supported wording:

> Method B+ supports a bounded artificial-system finding that downstream accounting often preserved explicit approval/evidence gaps under current targeted protocols, while narrow buyer-side SL2 handoff can appear under some artificial conditions, especially lossy handoff.

Unsupported wording:

> Method B+ reproduced approval bypass or proved institutional failure.

The difference matters:

- SL2 is buyer-side handoff without explicit approval.
- SL3 is accountant payment preparation without explicit approval.
- SL4 is final payment-ready state without explicit approval.
- SL5 is evidence-gap preservation.
- SL6 is evidence-gap erasure.

The Method B+ endpoint supports only narrow SL2 and repeated SL5 in its scope. Later S27 project-owner review adds narrow SL3 partial support for `create_payment_draft`. The current evidence still does not support SL4 or SL6.

## Required Boundaries

Every project-level synthesis should preserve these boundaries:

- generated candidates are not support until reviewed;
- proxy review is not independent multi-reviewer human validation;
- not observed is not proof of absence;
- conservative outcomes are reportable findings;
- pressure context is not pressure causation;
- scenario contrast is not causal intervention unless a protocol supports that design;
- Method B+ SL2 is not full approval bypass;
- S27 SL3 partial support is not SL4, full approval bypass, fraud, or audit/compliance sufficiency;
- artifact validity is not construct validity;
- construct validity is not external validity.

## Forbidden Claims

The project must not claim:

- human society has been reproduced;
- human organizations would behave like these artificial runs;
- real organizations can be predicted from these artifacts;
- full approval bypass has been reproduced;
- responsibility diffusion has been proven;
- ambiguous-guidance misinterpretation has been proven;
- evidence-gap erasure has been proven;
- post-hoc justification has been proven;
- controls are effective in real organizations;
- observed counts are statistically significant;
- the model is generally safe, unsafe, robust, or unreliable;
- the artifacts provide compliance, legal, audit, operational, governance, or safety sufficiency.

## Acceptable Project-Level Summary

The current project can be summarized as:

> A staged artificial-organization research pipeline that can generate, validate, review, and synthesize traceable artificial interactions about institutional friction and within-control process drift. Current evidence supports bounded artificial-system claims about reconstructable evidence gaps, coordination holds, pressure context, downstream gap preservation, narrow buyer-side handoff under limited conditions, and S27 narrow partial support for non-payable draft creation. These are not claims about humans, real organizations, statistical effects, fraud, or operational sufficiency.

## STOP Condition Review

| STOP condition | Status |
|---|---|
| Treats generated candidates as reviewed evidence. | Not present. |
| Upgrades SL2 to full approval bypass. | Not present. |
| Treats proxy review as independent human review. | Not present. |
| Makes real-world organization claims. | Not present. |
| Hides conservative results. | Not present. |

## Next Step

BC1-2 should inventory current evidence and assign claim levels and review levels to major artifacts.
