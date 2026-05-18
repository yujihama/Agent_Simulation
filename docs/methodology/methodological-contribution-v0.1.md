# Methodological Contribution v0.1

Date: 2026-05-17
Status: accepted
Phase: Phase 2
Checkpoint: BC2-1 methodological contribution definition
Claim boundary: `methodological_contribution_definition_only`

## Scope

This document defines the project's methodological contribution after Phase 1 research-position synthesis.

It adds no new runs, candidates, reviews, protocols, scenarios, prompts, metrics, schemas, or baseline artifacts. It does not upgrade any empirical result. It explains how the existing project apparatus functions as a research method.

## Contribution Statement

The project contributes a reviewable artificial-organization research method for studying institutional friction, evidence gaps, and within-control process drift. Earlier documents use `non-intentional control slippage`; forward-looking scope is defined by `docs/research/within-control-process-drift-scope-v0.1.md`.

The method is not "multiple LLMs chatting in a simulated office." Its contribution is the disciplined separation of:

- frozen artificial conditions;
- role-local action proposals;
- deterministic Game Master decisions;
- reconstructable evidence packs;
- mechanical validation;
- generated candidate detection;
- candidate review;
- negative and conservative result preservation;
- explicit claim boundaries.

This structure allows the project to ask what happened inside an artificial organization, what evidence supports that interpretation, what remains unsupported, and which claims must remain forbidden.

## Why Ordinary Multi-Agent Simulation Is Not Enough

Ordinary multi-agent simulation can produce interaction transcripts, but transcripts alone do not make a research claim reviewable.

This project requires additional structure because institutional-friction claims are easy to overstate. A transcript may show a role saying something suggestive, but the research question depends on whether:

- the role had authority to act;
- a control requirement was explicit or unresolved;
- another role actually received the relevant evidence;
- the Game Master allowed, conditioned, or blocked the action;
- the final state preserved or erased the gap;
- a candidate label was later reviewed;
- the reported claim stays within the evidence boundary.

The method therefore treats LLM output as one artifact inside a governed evidence system, not as the result itself.

## Method Elements

| Element | Methodological role | Anti-overclaim function |
|---|---|---|
| Research positioning | Defines the project as artificial-organization methodology, not human-social reproduction. | Prevents human, real-world, model-general, and compliance claims. |
| Protocol freeze | Fixes scenario, roles, prompts, action menus, GM rules, candidate criteria, review criteria, and claim boundary before execution. | Prevents changing evaluation rules after seeing outputs. |
| Scenario and ODD-Social artifacts | Describe the artificial organization, roles, norms, controls, and scenario conditions. | Makes the artificial setting inspectable and bounded. |
| Role prompts and action menus | Constrain each LLM-controlled role to a versioned action proposal surface. | Separates allowed artificial actions from unrestricted behavior claims. |
| Game Master boundary | Converts role proposals into deterministic institutional decisions. | Prevents role text from becoming institutional state without arbitration. |
| Evidence pack | Records prompts, outputs, actions, GM decisions, messages, trace, events, metrics, final state, and reviewer notes. | Makes later reconstruction possible without relying on memory or hidden reasoning. |
| Validator and schemas | Check required files, JSON/JSONL structure, references, decisions, and role artifacts. | Distinguish mechanically valid evidence packs from unsupported artifacts. |
| Event and metric protocols | Define generated/proposed labels and descriptive metrics. | Prevent event labels or counts from becoming reviewed, causal, or statistical claims. |
| Candidate detection | Marks possible failure-mode or slippage observations as candidates only. | Keeps generated labels separate from support. |
| Candidate review | Reviews candidates against source references and frozen criteria. | Allows supported, partially supported, rejected, needs-revision, and not-observed statuses. |
| Reflection and synthesis | Records checkpoint decisions, STOP conditions, and next-scope choices. | Prevents repeated execution from drifting into result chasing. |
| Negative/conservative result preservation | Records not-observed results and boundary-preserving outcomes as findings. | Prevents hiding conservative outcomes or treating not-observed as proof of absence. |

## Game Master Boundary

The Game Master is the methodological boundary between an actor's proposal and the artificial institution's recorded decision.

An LLM role may propose an action such as a handoff, approval request, hold, escalation, preparation, or exception review. That proposal is not automatically the institutional outcome. The Game Master records whether the action:

- proceeds;
- proceeds with a note;
- requires clarification;
- preserves an evidence gap;
- records explicit approval, rejection, ambiguity, or unresolved status.

This boundary matters because many target claims depend on institutional state, not just actor language. For example, a buyer handoff without explicit approval is not the same as accounting preparation without explicit approval, and neither is the same as final payment-ready state without explicit approval. The Game Master decision and final state preserve those distinctions.

## Evidence Pack And Validator Role

The evidence pack is the unit of reconstruction. It should allow a reviewer to answer:

- what each role saw;
- what each role proposed;
- whether the parser accepted the proposal;
- how the Game Master decided;
- which messages and traces support the interpretation;
- which events and metrics were generated;
- whether the final state preserves or erases gaps;
- which review status is justified.

The validator does not prove that a construct is valid. It proves that the pack is mechanically inspectable enough to review. This distinction is central:

- validator pass: the artifact is structurally reviewable;
- candidate generated: the artifact may contain a pattern worth reviewing;
- candidate reviewed: the evidence supports, partially supports, rejects, or leaves unresolved a bounded interpretation;
- project claim: the reviewed interpretation remains inside the claim boundary.

## Review And Claim Boundary

Review is the conversion point between generated material and supported findings.

The project distinguishes:

- generated candidates;
- proxy or delegated review;
- project-owner human review;
- construct-validity review;
- accepted documents and protocols.

These are not equivalent. A generated candidate is not support. A proxy review is not independent multi-reviewer human validation. A human-reviewed representative pack is not automatically a statistical or real-world claim.

Claim boundaries are therefore part of the method, not a reporting afterthought. The method uses them to preserve weak-but-accurate statements and to forbid stronger statements that the evidence cannot support.

## Negative And Conservative Results

The project treats conservative results as research information.

Method B+ and later Phase 4 reviews showed that:

- narrow SL2 buyer handoff can appear under limited artificial conditions;
- S27 produced narrow SL3 partial support for non-payable draft creation while gaps stayed visible;
- downstream SL5 evidence-gap preservation appears repeatedly;
- stronger slippage levels such as SL4 and SL6 remain unsupported.

This is not a failed experiment. It is evidence that the current artificial setup, prompts, action menus, Game Master decisions, and review rules often preserve control boundaries. The method keeps that result visible instead of discarding it because it is not a dramatic failure.

The distinction remains:

- not observed does not prove absence;
- boundary preservation does not prove real-world control effectiveness;
- conservative artificial outcomes can still guide later mechanism selection.

## What The Method Enables

The method enables bounded claims that:

- versioned artificial-organization protocols exist;
- evidence packs can be mechanically validated;
- selected artifacts can be reconstructed and reviewed;
- generated candidates can be separated from supported findings;
- conservative and not-observed results can be preserved;
- future mechanisms can be selected from reviewed evidence rather than from desired outcomes.

## What The Method Does Not Enable

The method does not enable claims that:

- human society has been reproduced;
- real organizations behave like these artificial runs;
- controls are effective or ineffective in real organizations;
- a model is generally safe, unsafe, reliable, or unreliable;
- observed counts are statistically meaningful without a frozen statistical design;
- artifacts provide compliance, legal, audit, operational, governance, or safety sufficiency.

## Relation To Current Evidence

Phase 1 established the current evidence position:

- artifact and pipeline claims are relatively strong;
- selected EXP-0002 representative packs have bounded human-review support;
- Method B+ has narrow SL2 and repeated SL5 support in artificial scope;
- S27 adds narrow SL3 partial support for `create_payment_draft`;
- stronger failure modes such as SL4 final readiness, SL6 gap erasure, full approval bypass, fraud, human behavior, or real-world organization behavior remain unsupported, rejected, or not observed.

This methodological contribution therefore rests less on reproducing a severe failure mode and more on building a disciplined way to inspect, reject, narrow, and preserve artificial evidence.

## BC2-1 OK Condition Review

| Condition | Status |
|---|---|
| Methodological elements are decomposed. | OK. |
| Game Master boundary is explained. | OK. |
| Evidence pack and validator roles are explained. | OK. |
| Review and claim boundary importance is explained. | OK. |
| Negative result preservation is explained. | OK. |
| Description goes beyond "multiple LLMs." | OK. |
| Methodology and empirical results remain separated. | OK. |

## Checkpoint Decision

Decision: BC2-1 is complete.

Proceed to BC2-2: harden the evidence-pack methodology, review protocol, and review status labels.
