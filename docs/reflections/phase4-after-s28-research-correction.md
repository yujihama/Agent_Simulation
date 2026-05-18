# Phase 4 Reflection After S28 Research Correction

Date: 2026-05-18
Status: accepted
Phase: Phase 4 extension
Previous synthesis: `docs/synthesis/phase4-structuring-approval-splitting-synthesis-v0.1.md`
Selected mechanism: `applicant_side_structuring`
Claim boundary: `phase4_next_mechanism_selection_only`

## Purpose

This reflection records a correction after the S28 synthesis.

S28 remains valid as a downstream accountant-side diagnostic. It tested how accounting handled already-split items when aggregate approval or aggregate review remained unresolved. It did not test whether a requester, applicant, or buyer would choose to split a case before it reaches accounting.

This reflection adds no runs, result artifacts, candidate findings, baseline, or claim upgrade.

## Corrected Reading Of S28

S28 should be read as:

- downstream accountant-side structuring review;
- bounded SL2 split-item handoff support in AS02/AS03;
- SL5 aggregate-gap preservation in all non-control accepted runs;
- no SL1, SL3, SL4, SL6, FM3, or FM6 support;
- no test of applicant-side or buyer-side split-submission choice.

S28 should not be read as:

- evidence that a requester or buyer chooses to split cases under pressure;
- evidence of fraud, malicious bypass, or hidden intent;
- evidence of full approval bypass;
- evidence that real organizations or humans behave similarly.

## Missing Upstream Question

The Phase 4 research purpose includes identifying which within-control information structures can produce process-drift candidates.

S28 answered a downstream question:

> If split items reach accounting, does the accountant preserve aggregate approval/review gaps?

The unanswered upstream question is:

> Given a case that would require higher approval if submitted as one aggregate request, does the applicant, requester, or buyer choose to submit it as split requests under observable pressure?

This upstream question is materially different from S28. It targets the actor's visible action choice, pressure condition, threshold awareness, and whether aggregate context is preserved in the submitted packet.

## Selected Mechanism

Decision: freeze S29 `applicant_side_structuring`.

Rationale:

- it directly tests the upstream choice that S28 did not test;
- it remains inside the within-control scope because records are genuine and actors use their own roles;
- environmental pressure is treated as an observable condition rather than hidden intent;
- candidate classification can use visible artifacts: action choice, source refs, risk flags, payload summary, Game Master decision, and final state;
- it can separate split-with-note boundary preservation from split-without-aggregate-note candidates.

## Boundary

S29 must not:

- instruct an actor to commit fraud, hide evidence, forge records, use another identity, collude, or bypass access controls;
- infer hidden intent from the model's wording;
- treat split submission as fraud by definition;
- treat split submission as full approval bypass without SL4 final-state evidence;
- collapse SL2, SL3, SL4, SL5, and SL6;
- claim human behavior, real-world organization behavior, statistical significance, prompt causation, model-general behavior, or audit/compliance sufficiency.

## Checkpoint Decision

Proceed to BC4-S29-A: freeze an applicant-side structuring / approval-splitting protocol before any execution.

Execution must wait until S29 scenario, role visibility, action menu, Game Master rules, candidate criteria, evidence-pack requirements, review questions, and claim boundary are frozen.
