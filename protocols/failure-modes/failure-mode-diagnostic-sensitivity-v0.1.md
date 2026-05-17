# Method B Failure-Mode Diagnostic Sensitivity Protocol v0.1

Date: 2026-05-17
Status: accepted
Phase: Method B
Checkpoint: BC28
Covers: C10, C12, C16, C18, C20
Supersedes: none
Related protocols: `protocols/failure-modes/failure-mode-taxonomy-v0.1.md`; `protocols/failure-modes/targeted-failure-mode-pilot-v0.1.md`; `protocols/failure-modes/method-b-failure-mode-review-v0.1.md`; `protocols/failure-modes/failure-mode-baseline-decision-v0.1.md`
Related prompt: `prompts/org-payment/method-b-diagnostic-role-local-framing-addendum-v0.1.md`

## Purpose

BC24 produced no generated Method B failure-mode candidates. BC25 found no supported or partially supported failure-mode rows in curated representative evidence. BC26 therefore did not freeze a controlled failure-mode baseline, and BC27 was not executable.

This protocol freezes the next feasible Method B step: a diagnostic prompt-framing sensitivity pilot. The goal is to test whether the current no-candidate result is sensitive to prompt framing while holding scenario set, role set, model, action menus, Game Master rules, memory policy, post-hoc explanation policy, evidence-pack requirements, and claim boundary structure fixed.

This protocol does not execute runs.

## Diagnostic ID

| Field | Frozen value |
|---|---|
| Diagnostic id | `METHOD-B-DSP-0001` |
| Diagnostic axis | prompt framing |
| Executable next | yes |
| Scenario set | `S09`, `S12` |
| Runs per scenario | 5 |
| Total planned attempted runs | 10 |
| Provider/model | OpenAI `gpt-4.1-mini` |
| Role setup | requester, vendor, buyer, approver, accountant LLM-controlled |
| Game Master | existing deterministic menu-aware rules |
| Action menus | existing BC24/M05 menus |
| Post-hoc explanations | enabled, same as BC24 |
| Claim boundary | `method_b_diagnostic_sensitivity_observation_only` |

## Single-Axis Rule

Only one axis changes in `METHOD-B-DSP-0001`: each role action prompt receives the diagnostic role-local framing addendum.

The following must remain unchanged from BC24 unless a later protocol revision freezes a new diagnostic:

- S09/S12 scenario definitions;
- role set;
- provider/model;
- action menus;
- Game Master rules;
- parser and retry behavior;
- evidence-pack requirements;
- event taxonomy;
- metrics and failure-mode classification rules;
- post-hoc explanation prompt;
- validation requirements;
- raw output and curated output policy.

## Prompt Framing Addendum

`METHOD-B-DSP-0001` appends this addendum to each action-producing role prompt:

- `prompts/org-payment/method-b-diagnostic-role-local-framing-addendum-v0.1.md`

The addendum is intentionally bounded. It must not instruct actors to create failure modes, bypass approval, ignore evidence, or behave unsafely. It asks actors to make role-local decisions and to record uncertainty, urgency, informal practice, ambiguity, and missing evidence when they matter.

## Execution Requirements for the Later PR

The later execution PR must:

- write raw outputs under ignored `runs/`;
- commit only curated artifacts under `pilot-runs/`;
- attempt 5 runs per scenario before exclusions;
- report attempted, accepted, excluded, parser failures, provider failures, validation failures, retries, and rejected proposals;
- validate representative evidence packs mechanically;
- generate an aggregate failure-mode table using the unchanged BC21/BC24 candidate rules;
- keep candidate, supported, rejected, insufficient, and not_observed statuses distinct;
- include post-hoc explanations;
- include representative evidence packs and validation outputs;
- include a claim-boundary review.

## Reporting Requirements

The aggregate report must compare `METHOD-B-DSP-0001` descriptively against the BC24 reference package:

- candidate counts by failure mode;
- not_observed counts by failure mode;
- full path counts by scenario;
- approval-forward paths with explicit approval;
- approval-forward paths without explicit approval;
- hold/request-more-evidence paths;
- post-hoc explanation gap-preservation observations.

This is descriptive comparison only. It must not claim statistical significance, causation, prompt superiority, safety, or real-world behavior.

## Non-Goals

This protocol does not:

- execute the diagnostic;
- revise BC24, BC25, BC26, or BC27 artifacts;
- revise failure-mode definitions after seeing diagnostic results;
- revise scenarios;
- revise action menus;
- revise Game Master rules;
- add event taxonomy entries;
- run a controlled baseline;
- make statistical, causal, human behavior, real-world organization, compliance, legal, audit, operational, model-comparison, or general LLM behavior claims.

## Stop Conditions for Execution

The later execution PR must stop and open a separate protocol revision if:

- the addendum is found to force or directly instruct a failure mode;
- implementation requires changing more than the prompt-framing axis;
- the existing evidence-pack validator cannot reconstruct diagnostic runs without schema or contract changes;
- a new event type appears necessary;
- candidate rows are converted to supported rows without review;
- results are interpreted as human behavior, real-world organization behavior, statistical significance, or causation.

## Checkpoint Target

After the later execution PR, the project should know whether the no-candidate Method B result remains stable under a role-local prompt-framing diagnostic, without claiming that any result generalizes beyond the artificial setup.
