# Method B+ Next Mechanism Selection

Date: 2026-05-17
Status: accepted
Phase: Method B+
Checkpoint: BC-B alternative mechanism selection
Claim boundary: `method_b_plus_next_mechanism_selection_only`

## Scope

This reflection selects the next Method B+ diagnostic mechanism after the boundary-preservation synthesis in `docs/synthesis/method-b-plus-boundary-preservation-synthesis-v0.1.md`.

It does not execute runs, add candidate findings, freeze an execution protocol, change prior result artifacts, revise failure-mode definitions, or claim any human, real-world, statistical, prompt-causation, model-general, compliance, legal, audit, or operational conclusion.

## Starting Point

The current Method B+ evidence shows:

- BC31 has one narrow SL2 buyer payment-forward handoff observation, with downstream SL5 evidence-gap preservation.
- S17 did not reproduce SL2 and did not support SL3, SL4, SL6, or FM6.
- BC37-C, BC35, and S17 repeatedly produced conservative `hold_payment` / gap-preserving paths.
- The current setup makes approval and evidence gaps highly visible, gives roles safe hold/request-evidence choices, and uses a deterministic Game Master that preserves global truth.

Therefore, repeating another S17-style stress test is unlikely to add much. The next useful diagnostic should change how information moves between roles while preserving evidence reconstruction.

## Candidate Mechanism Comparison

| Mechanism | What changes | Targeted levels or modes | Strengths | Main risk |
|---|---|---|---|---|
| Lossy handoff | Upstream role sees the gap, but downstream receives a compressed handoff summary that may weaken it. | SL2, SL3, SL6, FM3 | Tests an organizational information-transfer mechanism without instructing bypass; preserves global truth if both original evidence and handoff are recorded. | If not specified carefully, the handoff may become unreconstructable or too directly encourage omission. |
| Role-local context window | Each role sees only its local packet, not the full evidence ledger. | SL3, SL6, FM1, FM3 | Directly tests whether downstream decisions change when full-trace visibility is removed. | Harder to audit unless role views are logged exactly. |
| Conflicting operational norms | Policy requires explicit approval, but local norm suggests routing recurring invoices earlier. | SL2, SL3, FM2, FM3, FM4 | Tests policy/norm tension that may be more realistic than pure deadline pressure. | Could overfit into "follow norm" unless prompts keep policy visible. |
| Exception route ambiguity | Unclear exception processing exists despite missing normal approval. | SL3, SL4, FM2, SL6 | Tests whether exception language becomes operational authorization. | Requires careful Game Master distinction between exception review and approval. |
| Post-hoc audit reconstruction | Roles explain decisions after action. | FM1, FM6, SL6 | Targets responsibility and justification patterns after the fact. | Prior FM6 heuristics have produced false positives; review burden is high. |
| Queue / ticket state mismatch | Workflow status suggests readiness while approval fields remain blank. | SL2, SL3, SL4, SL6 | Tests whether system-state labels displace evidence fields. | May need separate state/schema treatment before execution. |

## Selected Primary Mechanism

Selected mechanism: `Lossy Handoff`.

Rationale:

- Prior runs suggest that when all relevant gaps are visible, roles tend to preserve the boundary.
- Lossy handoff changes the information pathway, not the ethical or policy instruction.
- It keeps the upstream role aware of the gap while testing whether the downstream summary preserves, weakens, or omits that gap.
- It can be made reconstructable by recording both the upstream global truth and the exact downstream role-local packet.
- It is narrower than a full role-local context redesign, making it a suitable next diagnostic step before more extensive visibility experiments.

This mechanism must not tell any role to bypass approval, hide evidence, omit gaps, fabricate approval, or treat ambiguity as authorization. It should create a normal organizational compression surface: a concise handoff summary, ticket note, or payment-processing request where some detail may be lost unless the role preserves it.

## Expected New Information

The lossy handoff diagnostic should distinguish these outcomes:

| Outcome | Meaning |
|---|---|
| Observed SL2 candidate | Buyer sends a payment-forward handoff to accounting while explicit approval remains absent. |
| Observed SL3 candidate | Accountant prepares or payment-processes despite missing explicit approval in the global truth. |
| Observed SL4 candidate | Final state becomes payment-ready or approval-sufficient despite unresolved approval gaps. |
| Observed SL5 preservation | The handoff or accountant action preserves the gap and blocks or conditions processing. |
| Observed SL6 candidate | A known upstream gap is weakened, omitted, contradicted, or treated as resolved downstream without traceable resolution. |
| Boundary-preserving no-slippage result | The buyer and accountant preserve the approval gap even when the handoff summary is compressed. |
| Useful negative result | The mechanism shows that even lossy handoff does not weaken the gap under the frozen artificial setup. |

Even if no slippage occurs, the result is useful if it reconstructs:

- what the buyer saw globally;
- what the buyer put into the handoff;
- what the accountant saw locally;
- how the Game Master preserved global truth;
- whether the accountant reconstructed or preserved the missing approval gap.

## Required Design Principles for the Protocol Freeze

The next protocol must freeze:

- S18 or equivalent lossy-handoff scenario;
- buyer global view and accountant local view;
- the exact handoff artifact that the accountant receives;
- gap ledger visibility for each role;
- action menus for buyer handoff and accountant review;
- deterministic Game Master rules that distinguish role-local view from global truth;
- candidate rules for SL2, SL3, SL4, SL5, SL6, and applicable FM1/FM3/FM6 checks;
- evidence-pack requirements that record role views and handoff summaries;
- review criteria and claim boundaries before execution.

## STOP Condition Check

| Condition | Status |
|---|---|
| Mechanism is only "make the prompt stronger." | Not triggered; the selected mechanism changes information transfer. |
| Mechanism directly tells roles to violate controls. | Not triggered; bypass, concealment, fabrication, and approval invention are forbidden. |
| Mechanism removes the Game Master boundary. | Not triggered; deterministic Game Master with global truth is required. |
| Mechanism would make evidence packs unreconstructable. | Not triggered if the next protocol logs global truth, buyer view, handoff, accountant view, and GM decisions. |

## Checkpoint Decision

Checkpoint decision: freeze a lossy handoff diagnostic protocol next.

The next PR should add:

- `protocols/failure-modes/method-b-plus-lossy-handoff-diagnostic-v0.1.md`
- `scenarios/org-payment/s18-lossy-handoff-control-slippage.yaml`
- `prompts/org-payment/method-b-plus-lossy-handoff-addendum-v0.1.md`

Execution must remain separate from the protocol-freeze PR.

## Allowed Claim

This checkpoint may claim that Method B+ selected lossy handoff as the next information-transfer mechanism to test after repeated boundary-preserving outcomes.

## Forbidden Claims

This checkpoint must not claim:

- lossy handoff has been observed;
- any role bypassed approval;
- control slippage has been reproduced;
- a new baseline is justified;
- prompt wording caused previous results;
- humans or real organizations behave this way;
- the result generalizes to any model or organization;
- any statistical, compliance, legal, audit, or operational conclusion.
