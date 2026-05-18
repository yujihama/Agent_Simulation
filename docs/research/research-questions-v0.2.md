# Research Questions v0.2

Date: 2026-05-17
Status: accepted
Phase: Phase 1
Checkpoint: BC1-1 research objective reframing
Supersedes: positioning-level questions in `docs/adr/ADR-0001-research-positioning.md`
Claim boundary: `research_questions_reframing_only`

## Scope

This document updates the project research questions after the current evidence base and the Method B+ endpoint. It adds no new run, protocol, scenario, candidate, review, metric, or result.

## Research Aim

The project asks how to build a reviewable artificial-organization method for observing institutional friction and within-control process drift without overclaiming human or real-world behavior.

Scope-axis update: forward-looking research should use `Within-Control Process Drift` as the scope term. The research target remains process movement inside the ordinary control perimeter, not hidden actor intent.

## Primary Research Questions

### RQ1: Artifact Method

How can an artificial organization be structured so that role actions, Game Master decisions, messages, traces, events, metrics, and final states are reconstructable from evidence packs?

Current evidence:

- Supported as a project-artifact claim by schemas, contracts, validators, runner outputs, representative evidence packs, and review artifacts.

Open limits:

- Mechanical validity is not construct validity.
- Reviewability of selected packs is not reviewability of every possible run.

### RQ2: Claim Control

How can generated candidates, reviewed support, partial support, rejected candidates, not-observed outcomes, and unsupported claims be kept separate?

Current evidence:

- Supported as a workflow claim by Method B and Method B+ candidate review, reflection, and claim-hardening artifacts.

Open limits:

- Most Method B+ reviews are Codex delegated/proxy reviews under project-owner authorization, not independent multi-reviewer human validation.

### RQ3: Institutional Friction Representation

Which institutional-friction-like patterns can be represented and reviewed in artificial org-payment settings?

Current evidence:

- Bounded support exists for evidence gaps, approval-evidence propagation, coordination holds, pressure context, and narrow Method B+ buyer-side handoff observations.

Open limits:

- These are artificial-system observations, not direct evidence about humans or real organizations.

### RQ4: Within-Control Process Drift Stages

At which stage does a payment process move forward, and at which stage is the approval or evidence gap preserved?

Current evidence:

- SL2 buyer-side handoff has narrow support in BC31 and reviewed support in S18 lossy handoff.
- SL5 downstream evidence-gap preservation is repeatedly supported in S17, S18, and S19 reviewed artificial evidence.
- S27 project-owner review confirms narrow SL3 partial support for `create_payment_draft` while approval and exception-authority gaps remained visible.

Open limits:

- SL4 final payment-ready state without explicit approval is not supported.
- SL6 evidence-gap erasure is not supported.

### RQ4a: Scope Boundary

Which cases are within the control perimeter and therefore in scope?

Current answer:

- In scope: actors use their own assigned authority, system records match the actual operator, and evidence is not forged, hidden, or modified.
- Out of scope: impersonation, evidence fabrication or concealment, collusion, unauthorized access, privilege escalation, or malicious bypass.
- Structuring / approval splitting is in scope when it remains within-control.

Open limits:

- Future protocols must freeze boundary examples such as delegated authority, proxy approvals, exception approvals, or approval splitting before execution.

### RQ4b: Environmental Pressure Conditions

How do observable pressure conditions shape within-control process drift?

Current answer:

- Pressure should be represented as scenario state, system status, role-local packet, tool return, or prompt addendum.
- Pressure is not an inferred mental state.

Open limits:

- No current result supports pressure causation or statistical pressure effects.

### RQ5: Boundary-Preserving Conditions

Under current artificial protocols, what conditions appear to preserve control boundaries rather than produce stronger slippage?

Current evidence:

- Explicit gaps, available `hold_payment` or request-evidence actions, and deterministic Game Master gap recording are plausible boundary-preserving design features.

Open limits:

- The project does not claim these features cause the results.
- The project does not claim real organizations would preserve controls under similar conditions.

### RQ6: Future Mechanism Selection

What would count as a genuinely different mechanism if future work continues after the Method B+ endpoint?

Current answer:

- A new mechanism must change the organizational information mechanism, not simply increase stress in S17/S18/S19-like setups.
- Possible future mechanisms include role-local information rules, exception-route ambiguity, audit reconstruction, approval artifact mismatch, shadow approval, or delegated authority ambiguity.

Open limits:

- Any such mechanism must be selected and frozen in a separate PR before execution.
- No additional Method B+ diagnostic should run from the current endpoint without that mechanism-selection step.

## Deprecated Or Weakened Questions

The following early questions should be weakened:

| Earlier framing | Updated framing |
|---|---|
| Can an artificial organization produce institutional failure? | Can artificial-organization artifacts represent bounded institutional-friction and control-boundary observations? |
| Which conditions make failures more likely? | Which frozen artificial conditions are associated with observed paths, candidate rows, or boundary preservation, without causal claims? |
| Which controls reduce failures? | Which artificial design features appear to preserve evidence gaps or route decisions conservatively, without real-world control-effectiveness claims? |
| Can this reproduce social chaos? | Can this method generate reviewable hypotheses about institutional friction mechanisms? |

## Claim Boundary

The research questions do not ask whether:

- humans would behave this way;
- real organizations would experience the same failures;
- the model is generally safe, unsafe, reliable, or unreliable;
- any count is statistically meaningful;
- the artifacts establish compliance, legal, audit, operational, or governance sufficiency.

## Next Step

BC1-2 should map current artifacts to claim levels and review levels so these questions are grounded in the committed evidence base.
