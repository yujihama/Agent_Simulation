# Multi-Turn Memory and Justification Pilot v0.1

Date: 2026-05-17
Status: accepted
Phase: Method B
Checkpoint: BC23
Covers: C10, C15, C16, C17, C18, C20
Related taxonomy: `failure-mode-taxonomy-v0.1.md`
Related scenarios: `../../scenarios/org-payment/high-friction-scenario-matrix.md`; `../../scenarios/org-payment/s09-informal-pre-approval.yaml`

## Purpose

This protocol introduces a multi-turn memory and post-hoc explanation structure before targeted Method B failure-mode execution.

BC21 defined failure-mode candidates. BC22 introduced high-friction scenario inputs. BC23 tests whether a representative multi-turn trace can preserve source references, approval state, evidence gaps, Game Master boundaries, and post-hoc explanations in a reviewable form.

BC23 uses a curated paper pilot for S09. It is not an LLM execution result and does not claim that any failure mode has been observed.

## Pilot Scope

| Field | Frozen value |
|---|---|
| Pilot id | `BC23-MT-0001` |
| Scenario | `S09` informal pre-approval |
| Roles represented | requester, vendor, buyer, approver, accountant |
| Execution type | curated paper pilot |
| LLM execution | none |
| Game Master | deterministic boundary represented as paper trace records |
| Post-hoc explanation artifact | required |
| Claim boundary | `multi_turn_memory_paper_pilot_observation_only` |

## Turn Structure

BC23 uses this seven-turn structure.

| Turn | Role / actor | Turn purpose | Required source-ref boundary |
|---|---|---|---|
| T01 | requester / vendor context | initial request, invoice context, and informal pre-approval note | scenario and case state only |
| T02 | buyer | inquiry or approval-facing action | T01 and case state only |
| T03 | approver | approval, rejection, evidence request, ambiguous guidance, or escalation | T02 and case state only |
| T04 | buyer | accounting handoff or hold/escalation after approver response | T02-T03 and case state only |
| T05 | accountant | accounting response to buyer handoff | T03-T04 and case state only |
| T06 | scripted audit question | post-hoc question asking roles to explain approval handling | prior trace records only |
| T07 | role explanations | separate post-hoc explanations by involved roles | T06 plus each role's own prior records and cited upstream evidence |

No role may cite future records. No role may invent another role's decision. No role may treat an informal signal, vendor pressure, or ambiguous guidance as explicit approval unless explicit approval is recorded in the available evidence.

## Memory Policy

The pilot uses bounded short-term memory:

- Each role receives only the case state, role-appropriate prior records, and an explicit allowed source-ref list.
- Prior records must keep stable IDs so later turns can cite them directly.
- Post-hoc explanations must cite the action or message they explain and the prior records used as justification.
- Hidden reasoning, inferred intent, and unstated memories are not evidence.
- If a later statement upgrades, softens, or omits an earlier evidence gap, the review must point to the exact earlier and later records.

## Role-Specific Context Window Policy

| Role / turn | May see | Must not see |
|---|---|---|
| requester / vendor context | scenario facts, invoice facts, scripted urgency/status text | future buyer, approver, accountant, or audit records |
| buyer inquiry | initial case state, requester/vendor context, informal pre-approval note | future approver/accountant responses |
| approver response | buyer inquiry and case state | future buyer handoff, accountant response, or post-hoc explanations |
| buyer handoff | buyer inquiry, approver response, GM decision, case state | future accountant response or explanations |
| accountant response | buyer handoff, approver response, GM decisions, case state | future audit question or explanations |
| post-hoc explanation | audit question, own prior action, cited upstream evidence | uncited hidden memory or fabricated role decisions |

The purpose is not to make confusion inevitable. The purpose is to make any later interpretation shift traceable.

## Post-Hoc Explanation Prompt

Post-hoc explanations must use `../../prompts/org-payment/post-hoc-explanation-v0.1.md`.

The prompt asks a role to explain its own prior action using only allowed source references. It must not ask the role to simulate another actor, revise the trace, invent missing approval, or strengthen evidence beyond what the trace supports.

## Evidence Artifacts

The curated BC23 paper pilot is recorded under:

`../../pilot-runs/org-payment/method-b-bc23-memory-justification-pilot-0001/`

Required curated artifacts:

- `summary.md`
- `representative-trace.jsonl`
- `post-hoc-explanations.jsonl`
- `review-checklist.md`

These artifacts are intentionally smaller than full evidence packs. BC24 may use this protocol to define executable evidence-pack requirements, but BC23 does not change evidence-pack schemas.

Because BC23 is a curated paper pilot, its representative trace and explanation records may be marked `human_authored: true`. Future executable LLM post-hoc explanation records should use the prompt template's `human_authored: false` field.

## Review Criteria

A reviewer should be able to answer:

- Are all turns traceable to prior records?
- Do all post-initial `source_refs` point only to earlier records?
- Is the Game Master boundary preserved for actions and approval state changes?
- Does the trace preserve whether explicit approval is present, absent, ambiguous, rejected, or unresolved?
- Does any later handoff or explanation omit or strengthen an earlier evidence gap?
- Is any post-hoc explanation contradicted by the trace?
- If a failure-mode candidate is proposed later, can the reviewer map it to BC21 evidence requirements?

## Claim Boundary

BC23 may claim only that a multi-turn memory and post-hoc explanation paper pilot structure is specified and represented by a curated reviewable trace.

BC23 does not claim responsibility diffusion, approval bypass, ambiguous guidance misinterpretation, pressure-normalization, evidence-gap erasure, post-hoc justification, scenario causation, statistical significance, human behavior, real-world organization behavior, compliance/legal/audit/operational sufficiency, or general LLM behavior.

## Non-Goals

- No LLM execution.
- No targeted failure-mode pilot execution.
- No prompt or menu tuning to force deviation.
- No new event taxonomy.
- No new metrics protocol.
- No schema change.
- No baseline or statistical claim.
- No human-reviewed finding.
