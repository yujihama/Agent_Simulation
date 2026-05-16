# Agent Simulation

This repository contains research artifacts for a project on using LLM agents as artificial participants in small social simulations of institutional friction and failure.

The project is managed through checkpoint-oriented pull requests. The working rules are the first canonical document to read before adding research specs, scenarios, protocols, code, or experiment results.

## Current Canonical Documents

- Working rules: [docs/research/03_working_rules_and_pr_policy.md](docs/research/03_working_rules_and_pr_policy.md)
- Coverage ledger: [docs/coverage_ledger.md](docs/coverage_ledger.md)
- Research positioning ADR: [docs/adr/ADR-0001-research-positioning.md](docs/adr/ADR-0001-research-positioning.md)
- Game Master architecture ADR: [docs/adr/ADR-0002-game-master-architecture.md](docs/adr/ADR-0002-game-master-architecture.md)
- Initial domain ADR: [docs/adr/ADR-0003-initial-domain-org-payment.md](docs/adr/ADR-0003-initial-domain-org-payment.md)
- Glossary: [docs/glossary.md](docs/glossary.md)
- ODD-Social v0.1: [protocols/odd-social/odd-social-v0.1.md](protocols/odd-social/odd-social-v0.1.md)
- ODD-Social template: [protocols/odd-social/odd-social-template.md](protocols/odd-social/odd-social-template.md)
- Org-payment scenario matrix: [scenarios/org-payment/scenario-matrix.md](scenarios/org-payment/scenario-matrix.md)
- Event taxonomy v0.1: [protocols/evaluation/event-taxonomy-v0.1.md](protocols/evaluation/event-taxonomy-v0.1.md)
- Metrics v0.1: [protocols/evaluation/metrics-v0.1.md](protocols/evaluation/metrics-v0.1.md)
- Evidence pack v0.1: [protocols/evaluation/evidence-pack-v0.1.md](protocols/evaluation/evidence-pack-v0.1.md)
- Human review protocol v0.1: [protocols/evaluation/human-review-protocol-v0.1.md](protocols/evaluation/human-review-protocol-v0.1.md)
- Claim boundaries v0.1: [protocols/evaluation/claim-boundaries-v0.1.md](protocols/evaluation/claim-boundaries-v0.1.md)
- Action proposal contract v0.1: [protocols/data-contracts/action-proposal-contract-v0.1.md](protocols/data-contracts/action-proposal-contract-v0.1.md)
- Game Master decision contract v0.1: [protocols/data-contracts/gm-decision-contract-v0.1.md](protocols/data-contracts/gm-decision-contract-v0.1.md)
- Trace record contract v0.1: [protocols/data-contracts/trace-record-contract-v0.1.md](protocols/data-contracts/trace-record-contract-v0.1.md)
- Run manifest contract v0.1: [protocols/data-contracts/run-manifest-contract-v0.1.md](protocols/data-contracts/run-manifest-contract-v0.1.md)
- Event record contract v0.1: [protocols/data-contracts/event-record-contract-v0.1.md](protocols/data-contracts/event-record-contract-v0.1.md)
- Metrics record contract v0.1: [protocols/data-contracts/metrics-record-contract-v0.1.md](protocols/data-contracts/metrics-record-contract-v0.1.md)
- S04 paper dry-run package: [dry-runs/org-payment/s04-paper-dry-run/README.md](dry-runs/org-payment/s04-paper-dry-run/README.md)
- Run manifest schema: [schemas/run-manifest.schema.json](schemas/run-manifest.schema.json)
- Action proposal schema: [schemas/action-proposal.schema.json](schemas/action-proposal.schema.json)
- Game Master decision schema: [schemas/gm-decision.schema.json](schemas/gm-decision.schema.json)
- Trace record schema: [schemas/trace-record.schema.json](schemas/trace-record.schema.json)
- Event record schema: [schemas/event-record.schema.json](schemas/event-record.schema.json)
- Metrics record schema: [schemas/metrics-record.schema.json](schemas/metrics-record.schema.json)
- Evidence pack validator: [scripts/validate_evidence_pack.py](scripts/validate_evidence_pack.py)
- Buyer action prompt template v0.1: [prompts/org-payment/buyer-action-proposal-v0.1.md](prompts/org-payment/buyer-action-proposal-v0.1.md)
- Buyer free-choice action prompt template v0.1: [prompts/org-payment/buyer-free-choice-action-v0.1.md](prompts/org-payment/buyer-free-choice-action-v0.1.md)
- Approver free-choice action prompt template v0.1: [prompts/org-payment/approver-free-choice-action-v0.1.md](prompts/org-payment/approver-free-choice-action-v0.1.md)
- Buyer-only baseline protocol v0.1: [protocols/baseline/buyer-only-baseline-v0.1.md](protocols/baseline/buyer-only-baseline-v0.1.md)
- EXP-0001 buyer-only baseline review: [results/org-payment/exp-0001-buyer-only-baseline/review.md](results/org-payment/exp-0001-buyer-only-baseline/review.md)
- Multi-role pilot protocol v0.1: [protocols/multi-role/multi-role-pilot-v0.1.md](protocols/multi-role/multi-role-pilot-v0.1.md)
- M01 buyer+approver pilot result: [pilot-runs/org-payment/m01-buyer-approver-pilot-0001/summary.md](pilot-runs/org-payment/m01-buyer-approver-pilot-0001/summary.md)
- M01 buyer+approver pilot review: [pilot-runs/org-payment/m01-buyer-approver-pilot-0001/review.md](pilot-runs/org-payment/m01-buyer-approver-pilot-0001/review.md)
- M02 buyer+vendor pressure pilot protocol v0.1: [protocols/multi-role/m02-buyer-vendor-pressure-pilot-v0.1.md](protocols/multi-role/m02-buyer-vendor-pressure-pilot-v0.1.md)
- Vendor pressure action prompt template v0.1: [prompts/org-payment/vendor-pressure-action-v0.1.md](prompts/org-payment/vendor-pressure-action-v0.1.md)

## Initial PR Sequence

The project should be built up in small decision-oriented pull requests:

1. PR-A: introduce working rules and repository references.
2. PR-B: introduce `docs/coverage_ledger.md`.
3. PR-C: introduce ADRs for research positioning, Game Master architecture, initial org-payment domain, and summaries of prior research-positioning drafts.
4. P1/P2 design bundle: introduce ODD-Social v0.1 and the org-payment scenario matrix.
5. P3 evaluation protocol bundle: introduce event taxonomy, metrics, evidence pack, human review, and claim boundaries.
6. P4/P5 data contract and dry-run bundle: introduce data contracts and a non-LLM paper dry run.
7. P4/P5 schema and validator bundle: introduce JSON Schemas and executable validation for the S04 paper dry run.
8. P4 skeleton bundle: introduce a deterministic non-LLM S04 runner that generates a valid evidence pack.
9. P6 fixed-action LLM pilot bundle: introduce the first fixed-action buyer LLM action-proposal path for S04.
10. P6 free-choice LLM pilot bundle: introduce constrained buyer action selection for S04.
11. P6/P7 repeated free-choice LLM pilot bundle: introduce small repeated S04 buyer free-choice runs and aggregate pilot reporting.
12. P7 scenario sweep pilot bundle: introduce S01-S06 buyer-only free-choice pilot runs and aggregate pilot reporting.
13. P7 baseline protocol freeze bundle: freeze EXP-0001 buyer-only baseline conditions before baseline execution.
14. P7 baseline execution bundle: execute EXP-0001 and add curated aggregate baseline result.
15. P8 baseline review and multi-role protocol bundle: review EXP-0001 and freeze M01 buyer+approver pilot conditions.
16. P8 M01 execution bundle: execute the frozen S04 buyer+approver multi-role pilot without changing protocol conditions.
17. P8 M01 review and M02 protocol bundle: review M01 and freeze the buyer+vendor pressure pilot protocol without executing M02.

A project glossary was introduced with PR-C and should be kept concise.

## Minimal Non-LLM S04 Run

Generate a deterministic S04 evidence pack:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim generate-s04 --output tmp/s04-generated-evidence-pack
```

Validate the generated evidence pack:

```powershell
python scripts/validate_evidence_pack.py tmp/s04-generated-evidence-pack
```

Run the non-LLM skeleton tests:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests
```

## Fixed-Action Buyer OpenAI S04 Pilot

Generate an opt-in S04 evidence pack where OpenAI formats buyer action proposal records for preselected S04 decision points:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim generate-s04-buyer-llm --output runs/org-payment/s04-buyer-openai-pilot-local/evidence-pack --dotenv .env
```

Validate the generated pilot pack:

```powershell
python scripts/validate_evidence_pack.py runs/org-payment/s04-buyer-openai-pilot-local/evidence-pack
```

Reference pilot output:

- [pilot-runs/org-payment/s04-buyer-openai-pilot-0001/validation-output.md](pilot-runs/org-payment/s04-buyer-openai-pilot-0001/validation-output.md)
- [pilot-runs/org-payment/s04-buyer-openai-pilot-0001/evidence-pack](pilot-runs/org-payment/s04-buyer-openai-pilot-0001/evidence-pack)

This pilot tests whether a buyer LLM can produce schema-valid action proposal records for preselected decision points. It does not yet test free-form buyer action selection. Requester, approver, accountant, and vendor records remain scripted or rule-based, and the Game Master remains deterministic.

## Free-Choice Buyer OpenAI S04 Pilot

Generate an opt-in S04 evidence pack where OpenAI chooses one buyer action from a constrained action menu:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim generate-s04-buyer-free-choice-llm --output runs/org-payment/s04-buyer-free-choice-openai-pilot-local/evidence-pack --dotenv .env
```

Validate the generated pilot pack:

```powershell
python scripts/validate_evidence_pack.py runs/org-payment/s04-buyer-free-choice-openai-pilot-local/evidence-pack
```

Reference pilot output:

- [pilot-runs/org-payment/s04-buyer-free-choice-openai-pilot-0001/validation-output.md](pilot-runs/org-payment/s04-buyer-free-choice-openai-pilot-0001/validation-output.md)
- [pilot-runs/org-payment/s04-buyer-free-choice-openai-pilot-0001/evidence-pack](pilot-runs/org-payment/s04-buyer-free-choice-openai-pilot-0001/evidence-pack)

This pilot tests whether a buyer LLM can choose one action from a constrained menu, produce a schema-valid action proposal, pass through the deterministic Game Master boundary, and leave a mechanically valid evidence pack. It remains a single pilot observation only.

## Repeated Free-Choice Buyer OpenAI S04 Pilot

Generate a small opt-in repeated pilot set where OpenAI chooses one buyer action from the same constrained S04 action menu in each run. Local generated output should be written under ignored `runs/` paths so it does not collide with committed reference artifacts:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim generate-s04-buyer-free-choice-batch `
  --output runs/org-payment/s04-buyer-free-choice-repeat-openai-pilot-local/raw `
  --curated-output runs/org-payment/s04-buyer-free-choice-repeat-openai-pilot-local/curated `
  --count 5 `
  --dotenv .env
```

Reference aggregate output:

- [pilot-runs/org-payment/s04-buyer-free-choice-repeat-openai-pilot-0001/summary.md](pilot-runs/org-payment/s04-buyer-free-choice-repeat-openai-pilot-0001/summary.md)
- [pilot-runs/org-payment/s04-buyer-free-choice-repeat-openai-pilot-0001/aggregate.json](pilot-runs/org-payment/s04-buyer-free-choice-repeat-openai-pilot-0001/aggregate.json)
- [pilot-runs/org-payment/s04-buyer-free-choice-repeat-openai-pilot-0001/representative-evidence-packs](pilot-runs/org-payment/s04-buyer-free-choice-repeat-openai-pilot-0001/representative-evidence-packs)
- [pilot-runs/org-payment/s04-buyer-free-choice-repeat-openai-pilot-0001/representative-validation-outputs](pilot-runs/org-payment/s04-buyer-free-choice-repeat-openai-pilot-0001/representative-validation-outputs)

Across this small repeated S04 buyer free-choice pilot set, the buyer selected actions under fixed artificial conditions. This aggregate remains a pilot observation only: it is not a model comparison, baseline result, statistical claim, real-world behavior claim, or evidence that humans would choose the same actions.

## Buyer-Only Scenario Sweep OpenAI Pilot

Generate a small opt-in S01-S06 scenario sweep where OpenAI chooses one buyer action from the same constrained action menu in each run. Local generated output should be written under ignored `runs/` paths:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim generate-buyer-scenario-sweep `
  --output runs/org-payment/buyer-only-scenario-sweep-pilot-local/raw `
  --curated-output runs/org-payment/buyer-only-scenario-sweep-pilot-local/curated `
  --count-per-scenario 3 `
  --dotenv .env
```

Reference aggregate output:

- [pilot-runs/org-payment/buyer-only-scenario-sweep-pilot-0001/summary.md](pilot-runs/org-payment/buyer-only-scenario-sweep-pilot-0001/summary.md)
- [pilot-runs/org-payment/buyer-only-scenario-sweep-pilot-0001/aggregate.json](pilot-runs/org-payment/buyer-only-scenario-sweep-pilot-0001/aggregate.json)
- [pilot-runs/org-payment/buyer-only-scenario-sweep-pilot-0001/representative-evidence-packs](pilot-runs/org-payment/buyer-only-scenario-sweep-pilot-0001/representative-evidence-packs)
- [pilot-runs/org-payment/buyer-only-scenario-sweep-pilot-0001/representative-validation-outputs](pilot-runs/org-payment/buyer-only-scenario-sweep-pilot-0001/representative-validation-outputs)

Across this small buyer-only scenario sweep pilot, action selections were recorded for S01-S06 under fixed artificial conditions. This aggregate remains a pilot observation only: it is not a baseline result, statistical significance claim, model comparison, real-world behavior claim, or evidence that humans would choose the same actions.

## Buyer-Only Baseline Protocol

EXP-0001 baseline execution is frozen by [protocols/baseline/buyer-only-baseline-v0.1.md](protocols/baseline/buyer-only-baseline-v0.1.md).

The protocol freezes the S01-S06 scenario set, 5 runs per scenario for 30 planned preliminary baseline runs, buyer-only LLM actor setup, scripted or rule-based non-buyer roles, deterministic menu-aware Game Master behavior, OpenAI `gpt-4.1-mini` model condition, prompt version, action menu, parser rules, validation rules, aggregation method, event handling, and claim boundary before baseline results are generated.

The only claim introduced by this protocol freeze is: the buyer-only baseline protocol is frozen for EXP-0001. It does not add baseline execution results, statistical interpretation, model comparison, multi-role LLM simulation, or human behavior claims.

## EXP-0001 Buyer-Only Baseline Result

Run the frozen buyer-only baseline locally with raw and generated curated output under ignored `runs/` paths:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-buyer-only-baseline `
  --output runs/org-payment/exp-0001-buyer-only-baseline-local/raw `
  --results-output runs/org-payment/exp-0001-buyer-only-baseline-local/results `
  --dotenv .env
```

Reference baseline result:

- [results/org-payment/exp-0001-buyer-only-baseline/summary.md](results/org-payment/exp-0001-buyer-only-baseline/summary.md)
- [results/org-payment/exp-0001-buyer-only-baseline/aggregate.json](results/org-payment/exp-0001-buyer-only-baseline/aggregate.json)
- [results/org-payment/exp-0001-buyer-only-baseline/execution-manifest.json](results/org-payment/exp-0001-buyer-only-baseline/execution-manifest.json)
- [results/org-payment/exp-0001-buyer-only-baseline/scenario-summary.csv](results/org-payment/exp-0001-buyer-only-baseline/scenario-summary.csv)
- [results/org-payment/exp-0001-buyer-only-baseline/representative-evidence-packs](results/org-payment/exp-0001-buyer-only-baseline/representative-evidence-packs)
- [results/org-payment/exp-0001-buyer-only-baseline/representative-validation-outputs](results/org-payment/exp-0001-buyer-only-baseline/representative-validation-outputs)

Under the frozen EXP-0001 artificial organization protocol, buyer-only LLM runs produced the recorded action selection distribution across S01-S06. All included runs passed mechanical evidence-pack validation. These results remain bounded to this artificial setup, model, prompt, and deterministic Game Master; they are not statistical significance evidence, model comparison, real-world behavior evidence, or human behavior claims.

## EXP-0001 Review and Multi-Role Pilot Protocol

The EXP-0001 review is recorded in [results/org-payment/exp-0001-buyer-only-baseline/review.md](results/org-payment/exp-0001-buyer-only-baseline/review.md).

The review records that EXP-0001 established a mechanically valid buyer-only baseline, with 30 attempted runs, 30 accepted runs, 0 exclusions, no parser failures, no validation failures, no retries, and `request_approval` selected in all included S01-S06 runs. It does not make statistical, human behavior, real-world organization, or model comparison claims.

The next protocol is frozen in [protocols/multi-role/multi-role-pilot-v0.1.md](protocols/multi-role/multi-role-pilot-v0.1.md). M01 is the only next executable multi-role pilot: S04 only, 5 runs, buyer + approver LLM-controlled, requester/accountant/vendor scripted or rule-based, deterministic menu-aware Game Master, OpenAI `gpt-4.1-mini`, generated/proposed event labels only, and claim boundary `multi_role_pilot_observation_only`.

## M01 Buyer+Approver Multi-Role Pilot

Run the frozen M01 pilot locally with raw and generated curated output under ignored `runs/` paths:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-m01-buyer-approver-pilot `
  --output runs/org-payment/m01-buyer-approver-pilot-local/raw `
  --curated-output runs/org-payment/m01-buyer-approver-pilot-local/curated `
  --dotenv .env
```

Reference M01 pilot output:

- [pilot-runs/org-payment/m01-buyer-approver-pilot-0001/summary.md](pilot-runs/org-payment/m01-buyer-approver-pilot-0001/summary.md)
- [pilot-runs/org-payment/m01-buyer-approver-pilot-0001/aggregate.json](pilot-runs/org-payment/m01-buyer-approver-pilot-0001/aggregate.json)
- [pilot-runs/org-payment/m01-buyer-approver-pilot-0001/execution-manifest.json](pilot-runs/org-payment/m01-buyer-approver-pilot-0001/execution-manifest.json)
- [pilot-runs/org-payment/m01-buyer-approver-pilot-0001/representative-evidence-packs](pilot-runs/org-payment/m01-buyer-approver-pilot-0001/representative-evidence-packs)
- [pilot-runs/org-payment/m01-buyer-approver-pilot-0001/representative-validation-outputs](pilot-runs/org-payment/m01-buyer-approver-pilot-0001/representative-validation-outputs)

Under the frozen M01 artificial organization protocol, buyer+approver LLM pilot runs produced the recorded buyer action, approver action, paired path, parser, GM decision, and validation outcomes. M01 remains a pilot, not a multi-role baseline. It does not support statistical, human behavior, real-world organization, compliance, legal, audit, or operational claims.

## M01 Review and M02 Pressure Protocol

The M01 review is recorded in [pilot-runs/org-payment/m01-buyer-approver-pilot-0001/review.md](pilot-runs/org-payment/m01-buyer-approver-pilot-0001/review.md).

The review records that M01 established mechanically valid buyer+approver multi-role evidence generation, with 5 attempted runs, 5 accepted runs, 0 exclusions, no parser failures, no validation failures, and no rejected or invalid proposals. Buyer selected `request_approval` in all 5 runs. Approver selected `approve_payment` in 4 runs and `request_more_evidence` in 1 run. No `provide_ambiguous_guidance` path was observed in the curated 5-run pilot.

The checkpoint decision is to advance to M02 buyer+vendor pressure pilot protocol. The M02 protocol is frozen in [protocols/multi-role/m02-buyer-vendor-pressure-pilot-v0.1.md](protocols/multi-role/m02-buyer-vendor-pressure-pilot-v0.1.md). M02 is S04 only, 5 attempted runs, vendor + buyer LLM-controlled, requester/approver/accountant scripted or rule-based, deterministic menu-aware Game Master, OpenAI `gpt-4.1-mini`, generated/proposed event labels only, and claim boundary `multi_role_pressure_pilot_observation_only`.

The vendor prompt template is [prompts/org-payment/vendor-pressure-action-v0.1.md](prompts/org-payment/vendor-pressure-action-v0.1.md). It is bounded to organizational pressure simulation and prohibits legal threats, abusive claims, unsafe coercive pressure, deception, and simulation of non-vendor roles.

This protocol-freeze step does not execute M02 and does not add M02 results. It does not make statistical, human behavior, real-world organization, compliance, legal, audit, model comparison, pressure-causation, or multi-role baseline claims.
