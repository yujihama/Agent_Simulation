# Human Review Protocol v0.1

Date: 2026-05-14
Status: accepted
Phase: P3
Step: P3 evaluation protocol bundle
Covers: C16, C17, C18, C20
Supersedes: none
Related ADR: ADR-0001, ADR-0002, ADR-0003

## Purpose

This protocol defines how humans review evidence packs, coded events, metrics, and claim boundaries for artificial organization runs.

Human review is used to control over-claiming, detect ambiguous evidence, and separate run observations from claims about real-world organizations.

## Review Roles

| Role | Responsibility |
|---|---|
| Primary reviewer | Reviews the evidence pack, codes or verifies events, and records limitations. |
| Secondary reviewer | Checks event coding, ambiguity, and claim strength for selected runs. |
| Adjudicator | Resolves material disagreements when reviewers cannot converge. |
| LLM-assisted reviewer | Optional tool role that suggests candidate labels or missing evidence, never the final authority. |

One person may perform multiple roles during early dry runs, but the review notes must record that limitation.

## Review Inputs

A review should use:

- ODD-Social version
- scenario specification
- evidence pack
- event taxonomy version
- metrics version
- claim boundary protocol
- prior review notes, if any

Do not review from summary output alone when source traces are available.

## Review Procedure

1. Confirm scope and protocol versions.
2. Run the evidence reconstruction check.
3. Code or verify events using Event Taxonomy v0.1.
4. Mark severity and reviewer confidence.
5. Identify missing, inconsistent, or ambiguous evidence.
6. Verify metrics against coded events and cited evidence.
7. Classify proposed statements using Claim Boundaries v0.1.
8. Record disagreements, limitations, and recommended revisions.

## Confidence Levels

| Level | Meaning |
|---|---|
| High | Evidence directly supports the event label or claim classification. |
| Medium | Evidence supports the label, but context is incomplete or alternative readings exist. |
| Low | Evidence is weak, indirect, or substantially ambiguous. |

Low-confidence events may be retained as review notes, but they should not carry strong claims.

## Disagreement Handling

Reviewers should distinguish between:

- label disagreement: which event type applies
- severity disagreement: how consequential the event is inside the artificial run
- evidence disagreement: whether the source trace supports the label
- claim disagreement: whether the proposed wording is stronger than the evidence permits

Material disagreements should be recorded in `reviewer_notes.md`. If a disagreement affects a reported pattern or claim, it should be resolved by adjudication or explicitly carried as a limitation.

## LLM-Assisted Review Boundary

LLM-assisted review may be used to:

- suggest candidate event labels
- identify possible evidence gaps
- summarize trace segments for human inspection
- check whether claim wording appears stronger than the cited evidence

LLM-assisted review must not:

- finalize event labels without human acceptance
- resolve reviewer disagreement by itself
- create missing evidence
- convert artificial-run observations into real-world claims
- be treated as an independent validation source

## Review Output

Review notes should include:

```text
Review id:
Run id or run set:
Scenario id:
Protocol versions:
Reviewer role:
Reconstruction outcome:
Coded event summary:
Metric verification:
Claim boundary review:
Disagreements:
Limitations:
Checkpoint recommendation:
```

## Version Boundary

Human Review Protocol v0.1 is sufficient for non-LLM dry runs and early implementation planning. It does not define reviewer recruitment, formal inter-rater reliability thresholds, or final experiment acceptance criteria.
