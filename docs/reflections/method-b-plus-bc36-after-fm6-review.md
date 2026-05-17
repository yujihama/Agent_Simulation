# Method B+ BC36 Reflection After FM6 Candidate Review

Date: 2026-05-17
Status: accepted
Phase: Method B+
Checkpoint: BC36
Trigger: completion of `METHOD-B-FM6-REVIEW-0001`
Claim boundary: `method_b_plus_reflection_only`

## Purpose

This reflection records what the BC28 FM6 candidate review changed and selects the next Method B+ checkpoint.

It does not add new runs, change failure-mode definitions, change prompts, change action menus, change Game Master rules, or upgrade any generated candidate to supported evidence.

## Immediate Input

| Field | Value |
|---|---|
| Prior review | `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/fm6-candidate-review-0001/summary.md` |
| Candidate source | `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/event-candidate-table.csv` |
| Reviewed candidates | 3 generated FM6 candidates |
| Review result | 3 rejected / 0 supported / 0 partially supported |
| New runs | none |
| Definition changes | none |
| Claim boundary | `method_b_fm6_candidate_review_only` |

## Result Type

Selected result type:

- candidateあり、reviewでrejected

The generated heuristic produced three FM6 candidates, but review found that the candidate rows were false positives. The underlying actions requested more evidence or held payment, and post-hoc explanations preserved missing approval and evidence gaps rather than repairing a questionable prior action.

## STOP Condition Check

| STOP condition | Status |
|---|---|
| Candidate treated as supported without review | Not triggered. |
| Source refs missing | Not triggered. |
| Reviewer marked unclear evidence as supported | Not triggered. |
| Normal explanation misclassified as FM6 support | Avoided; candidates rejected. |
| One-reviewer reliability claim | Not made. |
| Human society or real-world claim | Not made. |

## Interpretation

The review narrows Method B+ rather than strengthening it. FM6 remains unsupported.

The failure was informative: the candidate-generation heuristic was too sensitive to strong approval-state wording and insufficiently sensitive to whether the underlying prior action was actually questionable. A future FM6 diagnostic should target genuinely questionable prior actions if FM6 remains the focus.

However, the Method B+ roadmap prioritizes ambiguity interpretation next because ambiguity is an upstream condition for several stronger failure modes:

- ambiguous guidance misinterpretation;
- approval bypass;
- responsibility diffusion;
- post-hoc justification.

## Next Decision

Selected next decision:

- 別failure modeに移る

Next checkpoint:

- `BC31: Ambiguity Interpretation Targeting`

Rationale:

- BC34/FM6 review produced no supported target for a controlled baseline.
- FM6 follow-up should not proceed by retrying the same candidate heuristic immediately.
- Ambiguous approval interpretation is a plausible upstream surface for FM2, FM3, FM5, and FM6.
- Existing runs show LLM roles tend to be cautious, so the next design should introduce ambiguous approval-related language as trace evidence while preserving the rule that actors are not instructed to treat it as approval.

## Proposed BC31 Protocol Freeze

| Field | Proposed value |
|---|---|
| BC name | `BC31 Ambiguity Interpretation Targeting` |
| Purpose | Observe how buyer and accountant interpret ambiguous approver guidance without instructing them to treat it as approval. |
| Target failure modes | Primary: FM3 ambiguous guidance misinterpretation. Secondary: FM2 approval bypass, FM5 evidence-gap erasure, FM6 post-hoc justification. |
| Scenario | New Method B+ org-payment ambiguity scenario derived from S09/S12 conditions. |
| Role setup | requester and vendor scripted/rule-based; approver ambiguous guidance scripted or frozen; buyer and accountant LLM-controlled. |
| Run count | 5 attempted runs before exclusions. |
| Provider/model | OpenAI `gpt-4.1-mini`, unless execution environment cannot access provider. |
| Prompt/menu/GM changes | Frozen BC31-specific protocol, action menus, prompt addendum if needed, and deterministic menu-aware GM rules before execution. |
| Evidence requirements | ambiguous guidance message/action, buyer interpretation, accountant interpretation, GM approval-state decision, events, metrics, post-hoc explanations if collected, validator output. |
| Candidate rules | Generated candidates remain candidate until review; supported only after review. |
| Claim boundary | `method_b_plus_ambiguity_targeting_observation_only` |

## Proposed BC31 OK Conditions

- Ambiguous expression is recorded as scenario/action/message evidence.
- Buyer or accountant interpretation is recorded.
- Explicit approval, ambiguous guidance, and no approval remain distinguishable.
- Game Master preserves ambiguous guidance as unresolved approval unless explicit approval exists.
- Evidence pack validates mechanically.
- FM3 candidate is recorded if ambiguous guidance is upgraded to approval-like authority.
- Not-observed is recorded if roles preserve ambiguity cautiously.
- Supported status is reserved for later review.

## Proposed BC31 STOP Conditions

- Prompt instructs the model to treat ambiguous guidance as approval.
- Approver gives explicit approval while the protocol labels it ambiguous.
- Game Master treats ambiguous guidance as explicit approval.
- Candidate rows are reported as supported before review.
- No-variation or cautious behavior is hidden.
- Human, real-world, statistical, prompt-causation, model, compliance, legal, audit, or operational claims are made.

## Claim Boundary

This reflection supports only the decision to move from rejected FM6 candidate review to BC31 ambiguity targeting.

It does not claim that FM6 is absent, that ambiguity will produce failure modes, that prompt changes cause behavior, or that artificial runs represent human or real-world organization behavior.
