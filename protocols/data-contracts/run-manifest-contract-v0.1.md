# Run Manifest Contract v0.1

Date: 2026-05-14
Status: accepted
Phase: P4
Step: P4/P5 data contracts and dry-run bundle
Covers: C12, C15, C16, C18, C20
Supersedes: none
Related ADR: ADR-0001, ADR-0002, ADR-0003

## Purpose

A run manifest identifies what was run, which protocols and contracts applied, which artifacts belong to the evidence pack, and which exclusions or limitations constrain interpretation.

For P4/P5, a manifest may describe a non-LLM paper dry run. That does not make it an automated experiment harness or baseline result.

This contract is a protocol-level artifact. It is not a JSON schema, production API, implementation code, or experiment execution framework.

## Required Fields

| Field | Meaning |
|---|---|
| `run_id` | Stable run or dry-run package identifier. |
| `run_type` | `paper_dry_run`, `non_llm_dry_run`, or later controlled run type. |
| `scenario_id` | Scenario condition used. |
| `scenario_ref` | File path or reference to the scenario spec. |
| `odd_social_ref` | ODD-Social protocol or model reference. |
| `protocol_versions` | ODD-Social, event taxonomy, metrics, evidence pack, human review, and claim boundary versions. |
| `contract_versions` | Data contract versions used by the run artifacts. |
| `artifact_inventory` | List of evidence-pack artifacts and whether each is present. |
| `actor_mode` | Whether actors were manual, scripted, LLM-driven, or mixed. |
| `llm_execution` | Boolean stating whether LLM execution occurred. |
| `automated_harness` | Boolean stating whether an automated harness produced the run. |
| `known_exclusions` | Explicit non-goals and missing capabilities. |

## Recommended Fields

| Field | Meaning |
|---|---|
| `authored_by` | Person or process that authored the dry run. |
| `review_status` | Not reviewed, primary reviewed, secondary reviewed, or adjudicated. |
| `randomness_policy` | Whether randomness was absent, scripted, seeded, or uncontrolled. |
| `model_provider` | Provider only when LLM execution occurs. |
| `claim_boundary` | Maximum statement class allowed from this run. |

## Contract Rules

- The manifest must make manual authorship visible.
- Protocol and contract versions must be stated before metrics or claims are reported.
- Missing artifacts should be recorded as missing, not silently omitted.
- A paper dry run must not be described as a baseline experiment.
- Claims from a manifest should not exceed the claim boundary stated in the manifest.

## Version Boundary

This contract is sufficient for paper dry runs and implementation planning. It does not define batch execution, seed management for automated runs, storage layout, or formal artifact validation.
