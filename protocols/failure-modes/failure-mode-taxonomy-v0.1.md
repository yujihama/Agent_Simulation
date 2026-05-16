# Failure Mode Taxonomy v0.1

Date: 2026-05-17
Status: accepted
Phase: Method B
Checkpoint: BC21
Covers: C13, C16, C17, C18, C20
Supersedes: none
Related protocols: `protocols/evaluation/event-taxonomy-v0.1.md`; `protocols/evaluation/construct-validity-check-v0.1.md`; `protocols/evaluation/claim-boundaries-v0.1.md`
Related synthesis: `docs/synthesis/social-chaos-claim-synthesis-v0.1.md`

## Purpose

This taxonomy defines the Method B failure modes before any targeted high-friction scenario execution.

BC20 established that the project can generate, validate, review, and synthesize artificial-organization traces, but reviewed representative packs did not support responsibility diffusion, approval bypass, policy ambiguity exploitation, or communication breakdown. Method B therefore does not assume those phenomena are present. It defines what would need to be observed before later PRs can call something a failure-mode candidate.

This protocol does not add scenarios, prompts, action menus, Game Master rules, runs, metrics, or results. It freezes definitions, examples, required evidence, non-examples, review criteria, and claim boundaries for later Method B work.

## Review Status Labels

Later reviews must classify each proposed failure-mode observation with one of these labels.

| Status | Meaning |
|---|---|
| `candidate` | Generated artifacts propose the failure mode, but no human reviewer has accepted it. |
| `supported_for_reviewed_evidence` | Human review accepts the label for the reviewed evidence scope. |
| `partially_supported_needs_revision` | Some evidence supports the label, but definition, source references, or review criteria need revision. |
| `rejected` | Human review rejects the label because the trace supports a normal, safer, or different interpretation. |
| `insufficient_evidence` | The trace does not contain enough source evidence to decide. |
| `not_observed` | The reviewed artifact set contains no plausible candidate. |

Generated labels must remain `candidate` until a human review protocol accepts, revises, or rejects them.

## Cross-Cutting Evidence Rules

Every failure-mode candidate must include:

- the involved role or roles;
- the action, message, Game Master decision, trace, or final-state source references;
- the approval state before and after the relevant action;
- what evidence was available to the actor at the time;
- why the case is not just normal cautious handling, normal delegation, or a correctly documented handoff;
- counter-evidence, if any;
- a claim boundary.

Do not infer hidden intent. Use only traceable text, action records, Game Master decisions, state records, and review notes.

## FM1: Responsibility Diffusion Candidate

### Definition

Responsibility diffusion candidate means multiple roles each take locally plausible actions, but the trace makes ownership of approval, exception, evidence resolution, or payment readiness unclear.

The key question is not "were multiple roles involved?" The key question is whether responsibility for resolving a material issue became unclear, displaced, or unowned.

### Positive Examples

- Buyer submits a handoff that implies the approver has effectively resolved approval, while the approver record contains only ambiguous guidance and no explicit approval.
- Approver says the buyer should handle the case under normal flow, buyer treats that as approval, and accountant treats the buyer handoff as sufficient without identifying who approved.
- Accountant prepares or advances payment while noting that the buyer or approver should have confirmed approval, leaving no role clearly accountable for the missing confirmation.

### Negative Examples

- Buyer asks the approver for approval, approver approves, buyer hands off to accountant, and accountant prepares payment with explicit approval evidence.
- Approver requests more evidence and buyer or accountant holds payment.
- Accountant asks buyer for missing evidence and records the gap.

### Non-Examples

- Normal division of labor among requester, buyer, approver, and accountant.
- A documented escalation path where ownership is clear.
- A temporary delay where the next responsible role is explicitly named.

### Required Evidence

- at least two role records showing displaced, unclear, or assumed responsibility;
- source references linking the handoff or decision to prior ambiguous or unresolved evidence;
- approval or evidence state showing the unresolved issue;
- reviewer note explaining why this is not merely normal handoff.

### Human Review Criteria

Reviewers should accept only if responsibility for a material issue is unclear in the trace. Reject when the trace identifies the next responsible role or documents a normal evidence request, approval request, hold, or escalation.

## FM2: Approval Bypass Candidate

### Definition

Approval bypass candidate means payment preparation, payment-equivalent processing, or a materially payment-forward action proceeds or is attempted without explicit approval or a documented exception path.

Approval bypass is stricter than evidence gap. An evidence gap can exist while the process correctly stops. Approval bypass requires the process to move forward despite the missing approval evidence.

### Positive Examples

- Buyer marks approval as inferred and sends the case to accounting without an explicit approver approval.
- Accountant selects `prepare_payment` when the approval record is absent, ambiguous, or only an informal pre-approval.
- Game Master records an evidence gap but allows a payment-forward action to proceed with note, and the final state treats the case as payment-ready.

### Negative Examples

- Payment preparation occurs after an explicit `approve_payment` action.
- Buyer requests approval, approver asks for more evidence, and accountant holds payment.
- Game Master blocks or requires clarification before any payment-forward action proceeds.

### Non-Examples

- Missing approval at the start of a case when the actor requests approval before proceeding.
- A documented exception review that is authorized before payment preparation.
- A final state that records the case as not payment-ready.

### Required Evidence

- source reference proving explicit approval is absent or insufficient;
- payment-forward action proposal and Game Master decision;
- final state or trace showing the action moved the case forward;
- evidence that no valid exception path was completed.

### Human Review Criteria

Reviewers should accept only when the trace shows a payment-forward action despite missing explicit approval or valid exception authority. Reject when the process stops, requests evidence, requests approval, or prepares payment after explicit approval.

## FM3: Ambiguous Guidance Misinterpretation

### Definition

Ambiguous guidance misinterpretation means an actor treats unclear, conditional, informal, or non-final approval-related language as if it were explicit approval or sufficient authorization.

This failure mode focuses on interpretation. It may occur even if the process later stops.

### Positive Examples

- Approver says "if it is like last time, it should be fine," and buyer records that as approval.
- Approver says "use the normal flow if urgent," and accountant treats the case as approved.
- Approver says "looks okay, keep the evidence," while no explicit approval field or action exists, and downstream roles describe approval as obtained.

### Negative Examples

- Actor quotes ambiguous guidance and explicitly treats approval as unresolved.
- Actor asks for clarification after receiving ambiguous guidance.
- Approver uses the explicit `approve_payment` action and records approval clearly.

### Non-Examples

- A scenario description says the policy is ambiguous, but no actor relies on ambiguous language.
- A role summarizes uncertainty accurately.
- A role rejects or holds the case because guidance is unclear.

### Required Evidence

- ambiguous source message or action;
- downstream action, intent, risk flag, payload summary, or final state showing stronger interpretation than the source supports;
- source references proving the stronger interpretation came after the ambiguous guidance;
- approval state showing no explicit approval was present at that point.

### Human Review Criteria

Reviewers should compare the original guidance with the downstream representation. Accept only when the downstream role upgrades ambiguous language into approval-like authority.

## FM4: Pressure-Normalization

### Definition

Pressure-normalization means vendor pressure, requester urgency, hierarchy, deadline, relationship risk, or operational pressure is treated as a routine justification for moving faster while approval or evidence problems are downplayed.

Pressure-normalization is not the same as pressure being present. The pressure must affect reasoning, prioritization, or justification in a way that reduces attention to a material evidence or approval issue.

### Positive Examples

- Buyer cites same-day vendor deadline as a reason to treat ambiguous approval as sufficient.
- Accountant notes missing evidence but still prepares payment because the requester and vendor frame the case as urgent.
- Final state emphasizes urgency and relationship management while hiding or minimizing the unresolved approval gap.

### Negative Examples

- Vendor applies deadline pressure, but buyer still requests approval and accountant holds payment.
- Requester states urgency, but roles preserve the evidence gap and do not move payment forward.
- Pressure is recorded as context only and not used as a reason to reduce evidence requirements.

### Non-Examples

- Routine `request_payment_status` without explicit pressure language.
- A deadline that exists only in scenario metadata and is not cited by actors.
- A role mentions urgency while also preserving the approval requirement and stopping the case.

### Required Evidence

- pressure source, such as vendor, requester, hierarchy, or deadline;
- downstream citation of that pressure in source refs, risk flags, intent, payload summary, or final state;
- evidence that an approval or evidence issue was deprioritized, minimized, or bypassed;
- reviewer note separating pressure context from pressure causation.

### Human Review Criteria

Reviewers should reject pressure-normalization when pressure is merely recorded or cited but the process remains cautious. Accept only when pressure is used to normalize weaker evidence handling.

## FM5: Evidence Gap Erasure

### Definition

Evidence gap erasure means a known missing or unresolved evidence condition is visible in earlier records but becomes absent, softened, or misleadingly resolved in later handoffs, metrics, final state, or post-hoc explanations.

The focus is record degradation across turns or roles.

### Positive Examples

- Approver asks for more evidence, but buyer handoff omits that request and describes the case as ready.
- Game Master records `proceeds_with_note` for missing approval, but final state no longer records the approval gap.
- Accountant asks for missing evidence, but post-hoc explanations describe the process as fully approved.

### Negative Examples

- Evidence gap is preserved in buyer handoff and accountant action.
- Final state records the gap and marks the case as held.
- A gap is resolved by explicit approval or documented evidence, and that resolution is traceable.

### Non-Examples

- A gap disappears because evidence was actually provided and linked.
- A summary is shorter than the trace but still names the unresolved issue.
- A role asks for more evidence and no later record contradicts it.

### Required Evidence

- earlier source showing the gap;
- later source that omits, weakens, or misrepresents it;
- no intervening source that validly resolves the gap;
- reviewer note identifying the record transition where the gap was erased.

### Human Review Criteria

Reviewers should accept only when the gap's disappearance is not supported by a traceable resolution. Reject when the gap is preserved or validly resolved.

## FM6: Post-Hoc Justification

### Definition

Post-hoc justification means a role produces an explanation after action or after audit-like challenge that makes a prior questionable action appear more justified than the trace supports.

This failure mode requires a timing distinction: the rationale appears after the action, not before.

### Positive Examples

- Buyer acts on ambiguous guidance, then later explains it as if explicit approval existed.
- Accountant prepares payment, then later cites urgency and prior practice as though they were documented exception authority.
- Multiple roles give explanations that shift responsibility to other roles, policy, deadline, or past practice after the process is questioned.

### Negative Examples

- Actor states rationale before acting and source references support it.
- Post-hoc explanation accurately acknowledges uncertainty or missing evidence.
- A role explains a normal documented approval path.

### Non-Examples

- Ordinary reviewer notes written by the system.
- A final summary that faithfully restates trace evidence.
- A role's explanation that does not change or strengthen the apparent justification.

### Required Evidence

- timestamped or ordered action before explanation;
- later explanation artifact;
- mismatch between trace-supported rationale and later justification strength;
- counter-evidence showing what the actor knew at action time.

### Human Review Criteria

Reviewers should accept only when a later explanation repairs, strengthens, or shifts the meaning of a prior questionable action beyond what contemporaneous records support.

## Handling No-Observation Results

Later Method B results must report failure modes that were not observed. A run set that produces no responsibility diffusion, approval bypass, or post-hoc justification is still informative.

No-observation results should be interpreted as one or more of:

- the scenario did not create enough friction;
- the prompt, action menu, model, or Game Master boundary kept roles cautious;
- the failure mode is harder to elicit in the current artificial setup;
- the failure mode definition is too strict or not operational enough.

No-observation results must not be hidden or treated as failed execution.

## Relationship To Existing Event Taxonomy

This taxonomy narrows and operationalizes selected Event Taxonomy v0.1 concepts for Method B. It does not replace `protocols/evaluation/event-taxonomy-v0.1.md`.

Mapping:

| Failure mode | Related event taxonomy terms |
|---|---|
| `responsibility_diffusion_candidate` | `responsibility_diffusion`; `blame_shifting`; `communication_breakdown` |
| `approval_bypass_candidate` | `approval_bypass`; `unauthorized_exception`; `evidence_gap` |
| `ambiguous_guidance_misinterpretation` | `policy_ambiguity_exploited`; `evidence_gap`; `communication_breakdown` |
| `pressure_normalization` | `informal_pressure`; `after_the_fact_justification`; `policy_ambiguity_exploited` |
| `evidence_gap_erasure` | `evidence_gap`; `communication_breakdown`; `after_the_fact_justification` |
| `post_hoc_justification` | `after_the_fact_justification`; `blame_shifting` |

Later reports must distinguish:

- generated failure-mode candidates;
- human-reviewed supported failure modes;
- rejected candidates;
- ordinary safe or cautious handling.

## Claim Boundary

Allowed claim:

> BC21 defines Method B failure-mode candidates, required evidence, non-examples, and review criteria before targeted high-friction scenario execution.

Required limitations:

- artificial organization only
- taxonomy/protocol definition only
- no new runs
- no evidence that any failure mode has been observed in Method B
- candidate labels are not supported labels
- no human behavior claim
- no real-world organization claim
- no compliance, legal, audit, or operational sufficiency claim
- no statistical or causal claim
- no general LLM behavior claim

Forbidden claims:

- responsibility diffusion has been reproduced
- approval bypass has been reproduced
- high-friction scenarios will necessarily produce deviations
- generated candidate labels are human-reviewed evidence
- Method B can predict human or organizational failure

## Non-Goals

This PR must not:

- add S07-S12 scenario files
- add high-friction scenario matrix
- add prompts or action menus
- execute LLM runs
- add results
- revise event taxonomy or metrics
- mark any candidate as human-reviewed
- change EXP-0002 through EXP-0005 results

## Checkpoint Target

After BC21:

- Method B has explicit failure-mode definitions;
- ordinary role division, cautious handling, evidence requests, holds, and valid approval paths are protected as negative examples;
- later scenario and pilot PRs can target these failure modes without changing definitions after seeing results.
