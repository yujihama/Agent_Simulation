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

## Initial PR Sequence

The project should be built up in small decision-oriented pull requests:

1. PR-A: introduce working rules and repository references.
2. PR-B: introduce `docs/coverage_ledger.md`.
3. PR-C: introduce ADRs for research positioning, Game Master architecture, initial org-payment domain, and summaries of prior research-positioning drafts.
4. P1/P2 design bundle: introduce ODD-Social v0.1 and the org-payment scenario matrix.
5. P3 evaluation protocol bundle: introduce event taxonomy, metrics, evidence pack, human review, and claim boundaries.
6. P4/P5 data contract and dry-run bundle: introduce data contracts and a non-LLM paper dry run.
7. P4/P5 schema and validator bundle: introduce JSON Schemas and executable validation for the S04 paper dry run.

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
