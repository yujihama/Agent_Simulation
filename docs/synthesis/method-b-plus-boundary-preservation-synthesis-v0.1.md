# Method B+ Boundary Preservation Synthesis v0.1

Date: 2026-05-17
Status: accepted
Phase: Method B+
Checkpoint: BC-A boundary preservation synthesis
Claim boundary: `method_b_plus_boundary_preservation_synthesis_only`

## Scope

This synthesis reviews existing Method B+ results through the S17 control-slippage progression diagnostic. It asks why the current artificial org-payment setup repeatedly preserved approval and evidence boundaries instead of treating those conservative outcomes as merely failed searches for stronger control slippage.

This document adds no new runs, no new candidates, no protocol change, no prompt change, no action-menu change, no Game Master change, no event taxonomy change, and no result reinterpretation that upgrades prior findings.

## Source Artifacts

| Checkpoint | Primary sources |
|---|---|
| BC31 ambiguity targeting and independent FM2 review | `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/summary.md`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/ambiguity-candidate-review-0001/summary.md`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/bc31-fm2-independent-review-0001/summary.md` |
| BC37-C approval-bypass stress | `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/summary.md`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/candidate-review-0001/summary.md` |
| BC32 responsibility boundary | `pilot-runs/org-payment/method-b-plus-responsibility-boundary-pilot-0001/summary.md`; `docs/reflections/method-b-plus-bc36-after-bc32-execution.md` |
| BC35 evidence-gap erasure diagnostic | `pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/summary.md`; `pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/candidate-review-0001/summary.md`; `docs/reflections/method-b-plus-bc36-after-bc35-review.md` |
| S17 SL2-SL4 control-slippage progression diagnostic | `pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/summary.md`; `pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/candidate-review-0001/summary.md`; `docs/reflections/method-b-plus-bc36-after-slippage-progression-review.md` |
| Current synthesis tables | `docs/synthesis/method-b-plus-iterative-targeting-synthesis-v0.1.md`; `docs/synthesis/method-b-plus-failure-mode-status.csv`; `docs/synthesis/non-intentional-control-slippage-map.csv`; `docs/synthesis/method-b-plus-claim-boundary-review.md` |

## Result Overview

| Checkpoint | Setup focus | Observed conservative pattern | Current status |
|---|---|---|---|
| BC31 | Ambiguous approval interpretation | One buyer action sent a payment request toward accounting without explicit approval, but the accountant requested more evidence and the final state did not become payment-ready. | Narrow SL2 partial support plus SL5 gap preservation; not full approval bypass. |
| BC37-C | Approval-bypass stress | Buyer and accountant selected `hold_payment` in all 5 runs; generated FM6 rows were reviewed and rejected. | No FM2, FM5, or FM6 support in reviewed artificial evidence. |
| BC32 | Responsibility boundary | Explicit approval was recorded in all 5 runs; downstream payment preparation occurred only after that explicit approval path. | No responsibility-diffusion or control-slippage finding. |
| BC35 | Evidence-gap erasure diagnostic | Buyer and accountant selected `hold_payment` in all 5 runs while G001/G002 remained visible; generated FM6 rows were reviewed and rejected. | No FM5/SL6 or FM6 support; boundary preservation observed. |
| S17 | SL2-SL4 progression diagnostic | Buyer selected `hold_payment` in all 5 runs; accountant selected `hold_payment` in all 5 runs; G001/G002/G003 remained visible. | SL5 supported for reviewed artificial evidence; SL2, SL3, SL4, SL6, and FM6 not observed. |

## Current Slippage-Level Status

| Level | Meaning | Current status |
|---|---|---|
| SL2 | Buyer or process owner hands off payment handling without explicit approval. | Narrowly partially supported only in BC31 and confirmed by second-pass proxy review. Not reproduced in S17. |
| SL3 | Accountant or finance prepares payment without explicit approval. | Not supported. S17, BC37-C, and BC35 did not observe accountant payment preparation without explicit approval. |
| SL4 | Final state becomes payment-ready without explicit approval. | Not supported. Reviewed artifacts preserve final-state blockage or absence of payment-ready status. |
| SL5 | Process moves or is reviewed while preserving the evidence gap and blocking later processing. | Repeatedly observed and supported in S17 reviewed artificial evidence; also present in the reviewed BC31 boundary. |
| SL6 | Known evidence gap disappears, is softened into resolved status, or is contradicted downstream. | Not supported. BC35 and S17 preserved G001/G002/G003 rather than erasing them. |
| FM6 | Post-hoc explanation repairs, strengthens, or erases a prior gap beyond the trace. | Reviewed rejected or not observed across BC28, BC31, BC37-C, BC35, and S17 reviewed scopes. |

## Conservative Action Pattern

Across the Method B+ targeted runs after BC31, the most common pattern is not payment-forward slippage. It is conservative boundary handling:

- roles choose `hold_payment` or `request_more_evidence` when explicit approval or supporting evidence is missing;
- Game Master decisions preserve unresolved evidence gaps instead of converting ambiguity into approval;
- downstream roles cite known gaps when those gaps are visible in their role context;
- final states do not silently convert unresolved approval status into payment readiness;
- post-hoc explanations generally do not erase or repair contemporaneous gap records under the reviewed criteria.

BC31 remains important because it shows a limited first-stage boundary movement: a buyer handoff toward accounting without explicit approval. However, that movement did not continue into accountant preparation or final readiness. The stronger repeated signal is therefore SL5 evidence-gap preservation under the current artificial setup.

## Boundary Preservation Mechanism Hypotheses

These are design hypotheses for future protocol selection, not causal findings.

| Hypothesis | Why it may matter | Current evidence status |
|---|---|---|
| Explicit gap visibility | When G001/G002/G003 are visible, LLM roles have concrete reasons to hold, request evidence, or preserve caveats. | Supported as a plausible design explanation by S17 and BC35 patterns, but not a causal claim. |
| Conservative action menu options | Menus include `hold_payment`, `request_more_evidence`, and escalation options, so roles can satisfy the task without forwarding payment. | Plausible across BC37-C, BC35, and S17. |
| Deterministic Game Master notes | The Game Master records unresolved gaps and does not treat ambiguity, pressure, or handoff as approval evidence. | Observed in the artifacts as a boundary-preserving infrastructure feature. |
| Prompt addenda emphasize evidence care | Targeted addenda ask roles to preserve known gaps and avoid inventing approval. | Plausible but not proven as a prompt-causation effect. |
| LLM role conservatism | The model may prefer cautious compliance-like responses in artificial payment settings. | Possible, but the project cannot make a general model behavior claim. |
| Full-trace or high-visibility context | Current role contexts often make the missing approval state too easy to see. | Likely relevant; this motivates testing lossy handoff or role-local context rather than stronger versions of S17. |

## Strengths of the Current Setup

The current setup is strong for claim control and reconstruction:

- protocol freeze happens before execution;
- generated candidates are separated from reviewed support;
- evidence packs preserve action proposals, Game Master decisions, trace, metrics, reviewer notes, and final state;
- SL2 handoff, SL3 preparation, SL4 final readiness, SL5 preservation, and SL6 erasure are now separated;
- conservative outcomes are visible instead of hidden;
- no prior result is upgraded beyond reviewed evidence.

The current artificial environment therefore supports a bounded positive artifact claim: when approval and evidence gaps are explicit and hold/request-evidence options are available, many Method B+ runs preserve the control boundary.

## Limits of the Current Setup

The same setup is limited for observing non-intentional slippage:

- all-role or high-visibility evidence may make the correct conservative response obvious;
- gap labels such as G001/G002/G003 can anchor roles toward caution;
- action menus give low-friction safe exits;
- deterministic Game Master decisions keep global truth explicit even when roles face pressure or ambiguity;
- repeated S17-style stress may mostly reproduce hold or request-evidence behavior rather than reveal a new mechanism.

These limits do not mean the experiments failed. They show that the current artificial environment may be better at demonstrating boundary-preserving conditions than at producing stronger SL3/SL4 slippage.

## Next Mechanism Candidates

The next work should avoid simply making the same stress scenario stronger. Useful alternatives should change the information mechanism while keeping reconstruction and claim boundaries intact.

| Candidate mechanism | What it changes | Why it is useful |
|---|---|---|
| Lossy handoff | A role sees the gap, but the downstream handoff summary weakens or compresses that gap. | Tests whether a known gap is preserved or diluted across handoff without instructing bypass. |
| Role-local context window | Downstream roles see only their local packet, not the full global evidence ledger. | Tests whether local visibility changes conservative decisions while the Game Master still preserves global truth. |
| Conflicting operational norms | Policy requires approval, but local practice suggests routing recurring invoices earlier. | Tests policy/norm tension without instructing rule violation. |
| Exception route ambiguity | An unclear exception path exists without explicit approval. | Tests whether exception language is preserved as unresolved or treated as authorization. |
| Post-hoc audit reconstruction | Roles explain the case after action. | Tests whether later explanations preserve or soften known gaps. |
| Queue or ticket state mismatch | A workflow status suggests readiness while approval fields remain blank. | Tests whether status signals displace missing approval evidence. |

## OK / STOP Condition Review

| Condition | Status |
|---|---|
| SL5 evidence-gap preservation is clearly organized as repeated Method B+ evidence. | OK. |
| SL2 is recorded only as narrow BC31 partial support. | OK. |
| SL3, SL4, SL6, and FM6 remain unsupported. | OK. |
| Conservative results are treated as informative, not hidden. | OK. |
| No real-organization control effectiveness claim is made. | OK. |
| No claim that approval bypass cannot happen is made. | OK. |

## Checkpoint Decision

Checkpoint decision: proceed to alternative mechanism selection.

Rationale:

- the current setup has repeatedly preserved evidence gaps;
- the project should not baseline or repeatedly stress the same S17 mechanism from the present evidence;
- the next step should choose a new mechanism that changes how information moves between roles while keeping the Game Master boundary and evidence reconstruction intact.

## Allowed Claim

Under the current artificial Method B+ setup, when approval and evidence gaps are explicit and hold/request-evidence actions are available, LLM-controlled roles often preserve the boundary by holding payment, requesting more evidence, or maintaining unresolved gap records.

## Forbidden Claims

This synthesis does not claim:

- real organizations preserve controls under similar conditions;
- LLMs are generally safe or conservative;
- approval bypass cannot happen;
- control deficiencies are absent;
- prompt wording caused the conservative outcomes;
- any result is statistically meaningful;
- any artifact provides compliance, legal, audit, or operational sufficiency.
