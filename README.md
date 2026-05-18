# Agent Simulation

This repository contains research artifacts for a project on using LLM agents as artificial participants in small social simulations of institutional friction and failure.

The project is managed through checkpoint-oriented pull requests. The working rules are the first canonical document to read before adding research specs, scenarios, protocols, code, or experiment results.

## Current Canonical Documents

- Working rules: [docs/research/03_working_rules_and_pr_policy.md](docs/research/03_working_rules_and_pr_policy.md)
- Research objective reframing v0.1: [docs/research/research-objective-reframing-v0.1.md](docs/research/research-objective-reframing-v0.1.md)
- Research questions v0.2: [docs/research/research-questions-v0.2.md](docs/research/research-questions-v0.2.md)
- Within-Control Process Drift scope v0.1: [docs/research/within-control-process-drift-scope-v0.1.md](docs/research/within-control-process-drift-scope-v0.1.md)
- Claim positioning v0.2: [docs/research/claim-positioning-v0.2.md](docs/research/claim-positioning-v0.2.md)
- Coverage ledger: [docs/coverage_ledger.md](docs/coverage_ledger.md)
- Research positioning ADR: [docs/adr/ADR-0001-research-positioning.md](docs/adr/ADR-0001-research-positioning.md)
- Game Master architecture ADR: [docs/adr/ADR-0002-game-master-architecture.md](docs/adr/ADR-0002-game-master-architecture.md)
- Initial domain ADR: [docs/adr/ADR-0003-initial-domain-org-payment.md](docs/adr/ADR-0003-initial-domain-org-payment.md)
- Glossary: [docs/glossary.md](docs/glossary.md)
- ODD-Social v0.1: [protocols/odd-social/odd-social-v0.1.md](protocols/odd-social/odd-social-v0.1.md)
- ODD-Social template: [protocols/odd-social/odd-social-template.md](protocols/odd-social/odd-social-template.md)
- Org-payment scenario matrix: [scenarios/org-payment/scenario-matrix.md](scenarios/org-payment/scenario-matrix.md)
- Org-payment high-friction scenario matrix: [scenarios/org-payment/high-friction-scenario-matrix.md](scenarios/org-payment/high-friction-scenario-matrix.md)
- Event taxonomy v0.1: [protocols/evaluation/event-taxonomy-v0.1.md](protocols/evaluation/event-taxonomy-v0.1.md)
- Metrics v0.1: [protocols/evaluation/metrics-v0.1.md](protocols/evaluation/metrics-v0.1.md)
- Pressure-citation metric correction v0.1: [protocols/evaluation/pressure-citation-metric-correction-v0.1.md](protocols/evaluation/pressure-citation-metric-correction-v0.1.md)
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
- Approver multi-role action prompt template v0.1: [prompts/org-payment/approver-multirole-action-v0.1.md](prompts/org-payment/approver-multirole-action-v0.1.md)
- Buyer-only baseline protocol v0.1: [protocols/baseline/buyer-only-baseline-v0.1.md](protocols/baseline/buyer-only-baseline-v0.1.md)
- EXP-0001 buyer-only baseline review: [results/org-payment/exp-0001-buyer-only-baseline/review.md](results/org-payment/exp-0001-buyer-only-baseline/review.md)
- Multi-role pilot protocol v0.1: [protocols/multi-role/multi-role-pilot-v0.1.md](protocols/multi-role/multi-role-pilot-v0.1.md)
- M01 buyer+approver pilot result: [pilot-runs/org-payment/m01-buyer-approver-pilot-0001/summary.md](pilot-runs/org-payment/m01-buyer-approver-pilot-0001/summary.md)
- M01 buyer+approver pilot review: [pilot-runs/org-payment/m01-buyer-approver-pilot-0001/review.md](pilot-runs/org-payment/m01-buyer-approver-pilot-0001/review.md)
- M02 buyer+vendor pressure pilot protocol v0.1: [protocols/multi-role/m02-buyer-vendor-pressure-pilot-v0.1.md](protocols/multi-role/m02-buyer-vendor-pressure-pilot-v0.1.md)
- Vendor pressure action prompt template v0.1: [prompts/org-payment/vendor-pressure-action-v0.1.md](prompts/org-payment/vendor-pressure-action-v0.1.md)
- M02 buyer+vendor pressure pilot result: [pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/summary.md](pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/summary.md)
- M02 buyer+vendor pressure pilot review: [pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/review.md](pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/review.md)
- M03 buyer+approver+accountant coordination pilot protocol v0.1: [protocols/multi-role/m03-buyer-approver-accountant-coordination-pilot-v0.1.md](protocols/multi-role/m03-buyer-approver-accountant-coordination-pilot-v0.1.md)
- Accountant free-choice action prompt template v0.1: [prompts/org-payment/accountant-free-choice-action-v0.1.md](prompts/org-payment/accountant-free-choice-action-v0.1.md)
- M03 buyer+approver+accountant coordination pilot result: [pilot-runs/org-payment/m03-buyer-approver-accountant-coordination-pilot-0001/summary.md](pilot-runs/org-payment/m03-buyer-approver-accountant-coordination-pilot-0001/summary.md)
- M03 buyer+approver+accountant coordination pilot review: [pilot-runs/org-payment/m03-buyer-approver-accountant-coordination-pilot-0001/review.md](pilot-runs/org-payment/m03-buyer-approver-accountant-coordination-pilot-0001/review.md)
- M04 buyer+approver+accountant+vendor full-path pilot protocol v0.1: [protocols/multi-role/m04-buyer-approver-accountant-vendor-pilot-v0.1.md](protocols/multi-role/m04-buyer-approver-accountant-vendor-pilot-v0.1.md)
- M04 buyer+approver+accountant+vendor full-path pilot result: [pilot-runs/org-payment/m04-buyer-approver-accountant-vendor-pilot-0001/summary.md](pilot-runs/org-payment/m04-buyer-approver-accountant-vendor-pilot-0001/summary.md)
- M04 buyer+approver+accountant+vendor full-path pilot review: [pilot-runs/org-payment/m04-buyer-approver-accountant-vendor-pilot-0001/review.md](pilot-runs/org-payment/m04-buyer-approver-accountant-vendor-pilot-0001/review.md)
- Requester free-choice action prompt template v0.1: [prompts/org-payment/requester-free-choice-action-v0.1.md](prompts/org-payment/requester-free-choice-action-v0.1.md)
- M05 full org-payment multi-role pilot protocol v0.1: [protocols/multi-role/m05-full-org-payment-pilot-v0.1.md](protocols/multi-role/m05-full-org-payment-pilot-v0.1.md)
- M05 full org-payment multi-role pilot result: [pilot-runs/org-payment/m05-full-org-payment-pilot-0001/summary.md](pilot-runs/org-payment/m05-full-org-payment-pilot-0001/summary.md)
- M05 full org-payment multi-role pilot review: [pilot-runs/org-payment/m05-full-org-payment-pilot-0001/review.md](pilot-runs/org-payment/m05-full-org-payment-pilot-0001/review.md)
- Multi-role scenario sweep pilot protocol v0.1: [protocols/multi-role/multi-role-scenario-sweep-pilot-v0.1.md](protocols/multi-role/multi-role-scenario-sweep-pilot-v0.1.md)
- Multi-role scenario sweep pilot result: [pilot-runs/org-payment/multi-role-scenario-sweep-pilot-0001/summary.md](pilot-runs/org-payment/multi-role-scenario-sweep-pilot-0001/summary.md)
- Multi-role scenario sweep pilot review: [pilot-runs/org-payment/multi-role-scenario-sweep-pilot-0001/review.md](pilot-runs/org-payment/multi-role-scenario-sweep-pilot-0001/review.md)
- Multi-role baseline protocol v0.1: [protocols/baseline/multi-role-baseline-v0.1.md](protocols/baseline/multi-role-baseline-v0.1.md)
- EXP-0002 multi-role baseline result: [results/org-payment/exp-0002-multi-role-baseline/summary.md](results/org-payment/exp-0002-multi-role-baseline/summary.md)
- EXP-0002 multi-role baseline review: [results/org-payment/exp-0002-multi-role-baseline/review.md](results/org-payment/exp-0002-multi-role-baseline/review.md)
- EXP-0002 human evidence review protocol v0.1: [protocols/evaluation/exp-0002-human-evidence-review-v0.1.md](protocols/evaluation/exp-0002-human-evidence-review-v0.1.md)
- EXP-0002 LLM-assisted evidence pre-review: [results/org-payment/exp-0002-multi-role-baseline/llm-assisted-pre-review-0001/summary.md](results/org-payment/exp-0002-multi-role-baseline/llm-assisted-pre-review-0001/summary.md)
- EXP-0002 human evidence review: [results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md](results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md)
- Construct validity check protocol v0.1: [protocols/evaluation/construct-validity-check-v0.1.md](protocols/evaluation/construct-validity-check-v0.1.md)
- EXP-0002 construct validity check: [results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/summary.md](results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/summary.md)
- EXP-0003 intervention validity stress test protocol v0.1: [protocols/evaluation/exp-0003-intervention-validity-stress-test-v0.1.md](protocols/evaluation/exp-0003-intervention-validity-stress-test-v0.1.md)
- EXP-0003 intervention validity stress test: [results/org-payment/exp-0003-intervention-validity-stress-test-0001/summary.md](results/org-payment/exp-0003-intervention-validity-stress-test-0001/summary.md)
- EXP-0004 provider-randomness sensitivity protocol v0.1: [protocols/evaluation/exp-0004-provider-randomness-sensitivity-v0.1.md](protocols/evaluation/exp-0004-provider-randomness-sensitivity-v0.1.md)
- EXP-0004 provider-randomness sensitivity result: [results/org-payment/exp-0004-provider-randomness-sensitivity-0001/summary.md](results/org-payment/exp-0004-provider-randomness-sensitivity-0001/summary.md)
- EXP-0004 provider-randomness sensitivity review: [results/org-payment/exp-0004-provider-randomness-sensitivity-0001/review.md](results/org-payment/exp-0004-provider-randomness-sensitivity-0001/review.md)
- Second-domain ADR: [docs/adr/ADR-0004-second-domain-expense-reimbursement.md](docs/adr/ADR-0004-second-domain-expense-reimbursement.md)
- Expense reimbursement scenario ER01: [scenarios/expense-reimbursement/er01-ambiguous-receipt-approval.yaml](scenarios/expense-reimbursement/er01-ambiguous-receipt-approval.yaml)
- EXP-0005 expense reimbursement second-domain pilot protocol v0.1: [protocols/domain-expansion/expense-reimbursement-pilot-v0.1.md](protocols/domain-expansion/expense-reimbursement-pilot-v0.1.md)
- EXP-0005 expense reimbursement second-domain pilot result: [results/expense-reimbursement/exp-0005-second-domain-pilot-0001/summary.md](results/expense-reimbursement/exp-0005-second-domain-pilot-0001/summary.md)
- EXP-0005 expense reimbursement second-domain pilot review: [results/expense-reimbursement/exp-0005-second-domain-pilot-0001/review.md](results/expense-reimbursement/exp-0005-second-domain-pilot-0001/review.md)
- Social chaos claim synthesis protocol v0.1: [protocols/synthesis/social-chaos-claim-synthesis-v0.1.md](protocols/synthesis/social-chaos-claim-synthesis-v0.1.md)
- Social chaos claim synthesis v0.1: [docs/synthesis/social-chaos-claim-synthesis-v0.1.md](docs/synthesis/social-chaos-claim-synthesis-v0.1.md)
- Social chaos evidence map: [docs/synthesis/evidence-map.csv](docs/synthesis/evidence-map.csv)
- Social chaos claim-boundary review: [docs/synthesis/claim-boundary-review.md](docs/synthesis/claim-boundary-review.md)
- Social chaos synthesis limitations: [docs/synthesis/limitations.md](docs/synthesis/limitations.md)
- Method B+ integrated endpoint findings are included in the social chaos claim synthesis, evidence map, claim-boundary review, and limitations.
- Current evidence inventory v0.1: [docs/synthesis/current-evidence-inventory-v0.1.md](docs/synthesis/current-evidence-inventory-v0.1.md)
- Current evidence map: [docs/synthesis/current-evidence-map.csv](docs/synthesis/current-evidence-map.csv)
- Current claim-level table: [docs/synthesis/current-claim-level-table.csv](docs/synthesis/current-claim-level-table.csv)
- Phase 1 research position synthesis v0.1: [docs/synthesis/phase1-research-position-synthesis-v0.1.md](docs/synthesis/phase1-research-position-synthesis-v0.1.md)
- Methodological contribution v0.1: [docs/methodology/methodological-contribution-v0.1.md](docs/methodology/methodological-contribution-v0.1.md)
- Pipeline overview: [docs/methodology/pipeline-overview.md](docs/methodology/pipeline-overview.md)
- Evidence pack methodology v0.1: [docs/methodology/evidence-pack-methodology-v0.1.md](docs/methodology/evidence-pack-methodology-v0.1.md)
- Review protocol hardening v0.1: [docs/methodology/review-protocol-hardening-v0.1.md](docs/methodology/review-protocol-hardening-v0.1.md)
- Review status labels v0.2: [protocols/evaluation/review-status-labels-v0.2.md](protocols/evaluation/review-status-labels-v0.2.md)
- Negative and conservative results methodology v0.1: [docs/methodology/negative-and-conservative-results-v0.1.md](docs/methodology/negative-and-conservative-results-v0.1.md)
- Boundary preservation patterns v0.1: [docs/synthesis/boundary-preservation-patterns-v0.1.md](docs/synthesis/boundary-preservation-patterns-v0.1.md)
- Phase 2 methodology synthesis v0.1: [docs/synthesis/phase2-methodology-synthesis-v0.1.md](docs/synthesis/phase2-methodology-synthesis-v0.1.md)
- Within-Control Process Drift scope v0.1: [docs/research/within-control-process-drift-scope-v0.1.md](docs/research/within-control-process-drift-scope-v0.1.md)
- Non-intentional control slippage model v0.1: [docs/models/non-intentional-control-slippage-model-v0.1.md](docs/models/non-intentional-control-slippage-model-v0.1.md)
- Control slippage vs fraud: [docs/models/control-slippage-vs-fraud.md](docs/models/control-slippage-vs-fraud.md)
- Control slippage evidence requirements v0.1: [protocols/evaluation/control-slippage-evidence-requirements-v0.1.md](protocols/evaluation/control-slippage-evidence-requirements-v0.1.md)
- Control slippage positive and negative examples: [docs/models/control-slippage-positive-negative-examples.md](docs/models/control-slippage-positive-negative-examples.md)
- Control slippage existing evidence map v0.1: [docs/synthesis/control-slippage-existing-evidence-map-v0.1.md](docs/synthesis/control-slippage-existing-evidence-map-v0.1.md)
- Control slippage existing evidence map CSV: [docs/synthesis/control-slippage-existing-evidence-map.csv](docs/synthesis/control-slippage-existing-evidence-map.csv)
- Phase 3 control slippage model synthesis v0.1: [docs/synthesis/phase3-control-slippage-model-synthesis-v0.1.md](docs/synthesis/phase3-control-slippage-model-synthesis-v0.1.md)
- Phase 4 mechanism selection framework v0.1: [docs/reflections/phase4-mechanism-selection-framework-v0.1.md](docs/reflections/phase4-mechanism-selection-framework-v0.1.md)
- Phase 4 mechanism candidate table: [docs/reflections/phase4-mechanism-candidate-table.csv](docs/reflections/phase4-mechanism-candidate-table.csv)
- Phase 4 exception route ambiguity diagnostic protocol v0.1: [protocols/failure-modes/phase4-exception-route-ambiguity-diagnostic-v0.1.md](protocols/failure-modes/phase4-exception-route-ambiguity-diagnostic-v0.1.md)
- Phase 4 S20 exception route ambiguity scenario: [scenarios/org-payment/s20-exception-route-ambiguity.yaml](scenarios/org-payment/s20-exception-route-ambiguity.yaml)
- Phase 4 exception route ambiguity prompt addendum v0.1: [prompts/org-payment/phase4-exception-route-ambiguity-addendum-v0.1.md](prompts/org-payment/phase4-exception-route-ambiguity-addendum-v0.1.md)
- Phase 4 S20 exception route ambiguity diagnostic result: [pilot-runs/org-payment/phase4-exception-route-ambiguity-diagnostic-pilot-0001/summary.md](pilot-runs/org-payment/phase4-exception-route-ambiguity-diagnostic-pilot-0001/summary.md)
- Phase 4 S20 exception route ambiguity candidate review: [pilot-runs/org-payment/phase4-exception-route-ambiguity-diagnostic-pilot-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-exception-route-ambiguity-diagnostic-pilot-0001/candidate-review-0001/summary.md)
- Phase 4 BC36 reflection after exception route review: [docs/reflections/phase4-bc36-after-exception-route-review.md](docs/reflections/phase4-bc36-after-exception-route-review.md)
- Phase 4 mechanism exploration synthesis v0.1: [docs/synthesis/phase4-mechanism-exploration-synthesis-v0.1.md](docs/synthesis/phase4-mechanism-exploration-synthesis-v0.1.md)
- Phase 4 research objective reopen: [docs/reflections/phase4-reopen-research-objective.md](docs/reflections/phase4-reopen-research-objective.md)
- Phase 4 information-structure/model exploration protocol v0.1: [protocols/failure-modes/phase4-information-structure-model-exploration-v0.1.md](protocols/failure-modes/phase4-information-structure-model-exploration-v0.1.md)
- Phase 4 information-structure/model exploration result: [pilot-runs/org-payment/phase4-information-structure-model-exploration-0001/summary.md](pilot-runs/org-payment/phase4-information-structure-model-exploration-0001/summary.md)
- Phase 4 information-structure/model exploration reflection: [docs/reflections/phase4-information-structure-model-exploration-reflection.md](docs/reflections/phase4-information-structure-model-exploration-reflection.md)
- Phase 4 auxiliary candidate independent review protocol v0.1: [protocols/failure-modes/phase4-auxiliary-candidate-independent-review-v0.1.md](protocols/failure-modes/phase4-auxiliary-candidate-independent-review-v0.1.md)
- Phase 4 auxiliary candidate independent review: [pilot-runs/org-payment/phase4-information-structure-model-exploration-0001/auxiliary-candidate-independent-review-0001/summary.md](pilot-runs/org-payment/phase4-information-structure-model-exploration-0001/auxiliary-candidate-independent-review-0001/summary.md)
- Phase 4 reflection after auxiliary review: [docs/reflections/phase4-after-auxiliary-candidate-review.md](docs/reflections/phase4-after-auxiliary-candidate-review.md)
- Phase 4 prompt/persona variant diagnostic protocol v0.1: [protocols/failure-modes/phase4-prompt-persona-variant-diagnostic-v0.1.md](protocols/failure-modes/phase4-prompt-persona-variant-diagnostic-v0.1.md)
- Phase 4 prompt/persona variant addendum v0.1: [prompts/org-payment/phase4-prompt-persona-variant-addendum-v0.1.md](prompts/org-payment/phase4-prompt-persona-variant-addendum-v0.1.md)
- Phase 4 prompt/persona variant diagnostic result: [pilot-runs/org-payment/phase4-prompt-persona-variant-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-prompt-persona-variant-diagnostic-0001/summary.md)
- Phase 4 reflection after prompt/persona variant diagnostic: [docs/reflections/phase4-after-prompt-persona-variant-diagnostic.md](docs/reflections/phase4-after-prompt-persona-variant-diagnostic.md)
- Phase 4 prompt/persona candidate independent review: [pilot-runs/org-payment/phase4-prompt-persona-variant-diagnostic-0001/prompt-persona-candidate-independent-review-0001/summary.md](pilot-runs/org-payment/phase4-prompt-persona-variant-diagnostic-0001/prompt-persona-candidate-independent-review-0001/summary.md)
- Phase 4 reflection after prompt/persona candidate review: [docs/reflections/phase4-after-prompt-persona-candidate-review.md](docs/reflections/phase4-after-prompt-persona-candidate-review.md)
- Phase 4 S20 downstream-accounting threshold protocol v0.1: [protocols/failure-modes/phase4-s20-downstream-accounting-threshold-diagnostic-v0.1.md](protocols/failure-modes/phase4-s20-downstream-accounting-threshold-diagnostic-v0.1.md)
- Phase 4 downstream-accounting threshold prompt addendum v0.1: [prompts/org-payment/phase4-downstream-accounting-threshold-addendum-v0.1.md](prompts/org-payment/phase4-downstream-accounting-threshold-addendum-v0.1.md)
- Phase 4 S20 downstream-accounting threshold diagnostic result: [pilot-runs/org-payment/phase4-s20-downstream-accounting-threshold-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s20-downstream-accounting-threshold-diagnostic-0001/summary.md)
- Phase 4 S20 downstream-threshold auxiliary FM3 review: [pilot-runs/org-payment/phase4-s20-downstream-accounting-threshold-diagnostic-0001/auxiliary-fm3-operationalization-review-0001/summary.md](pilot-runs/org-payment/phase4-s20-downstream-accounting-threshold-diagnostic-0001/auxiliary-fm3-operationalization-review-0001/summary.md)
- Phase 4 reflection after S20 downstream-accounting threshold diagnostic: [docs/reflections/phase4-after-s20-downstream-accounting-threshold-diagnostic.md](docs/reflections/phase4-after-s20-downstream-accounting-threshold-diagnostic.md)
- Phase 4 reflection after S20 downstream-threshold auxiliary review: [docs/reflections/phase4-after-s20-downstream-threshold-auxiliary-review.md](docs/reflections/phase4-after-s20-downstream-threshold-auxiliary-review.md)
- Phase 4 exception-review authority-resolution protocol v0.1: [protocols/failure-modes/phase4-exception-review-authority-resolution-diagnostic-v0.1.md](protocols/failure-modes/phase4-exception-review-authority-resolution-diagnostic-v0.1.md)
- Phase 4 S21 exception-review authority-resolution scenario: [scenarios/org-payment/s21-exception-review-authority-resolution.yaml](scenarios/org-payment/s21-exception-review-authority-resolution.yaml)
- Phase 4 exception-review authority-resolution addendum v0.1: [prompts/org-payment/phase4-exception-review-authority-resolution-addendum-v0.1.md](prompts/org-payment/phase4-exception-review-authority-resolution-addendum-v0.1.md)
- Phase 4 S21 exception-review authority-resolution diagnostic result: [pilot-runs/org-payment/phase4-s21-exception-review-authority-resolution-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s21-exception-review-authority-resolution-diagnostic-0001/summary.md)
- Phase 4 S21 exception-review authority-resolution candidate review: [pilot-runs/org-payment/phase4-s21-exception-review-authority-resolution-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s21-exception-review-authority-resolution-diagnostic-0001/candidate-review-0001/summary.md)
- Phase 4 reflection after S21 authority-resolution diagnostic: [docs/reflections/phase4-after-s21-authority-resolution-diagnostic.md](docs/reflections/phase4-after-s21-authority-resolution-diagnostic.md)
- Phase 4 reflection after S21 boundary preservation and next mechanism: [docs/reflections/phase4-after-s21-boundary-preservation-and-next-mechanism.md](docs/reflections/phase4-after-s21-boundary-preservation-and-next-mechanism.md)
- Phase 4 prior approval carryover diagnostic protocol v0.1: [protocols/failure-modes/phase4-prior-approval-carryover-diagnostic-v0.1.md](protocols/failure-modes/phase4-prior-approval-carryover-diagnostic-v0.1.md)
- Phase 4 S22 prior approval carryover scenario: [scenarios/org-payment/s22-prior-approval-carryover-control-slippage.yaml](scenarios/org-payment/s22-prior-approval-carryover-control-slippage.yaml)
- Phase 4 prior approval carryover addendum v0.1: [prompts/org-payment/phase4-prior-approval-carryover-addendum-v0.1.md](prompts/org-payment/phase4-prior-approval-carryover-addendum-v0.1.md)
- Phase 4 S22 prior approval carryover diagnostic result: [pilot-runs/org-payment/phase4-s22-prior-approval-carryover-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s22-prior-approval-carryover-diagnostic-0001/summary.md)
- Phase 4 S22 prior approval carryover candidate review: [pilot-runs/org-payment/phase4-s22-prior-approval-carryover-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s22-prior-approval-carryover-diagnostic-0001/candidate-review-0001/summary.md)
- Phase 4 reflection after S22 prior approval carryover diagnostic: [docs/reflections/phase4-after-s22-prior-approval-carryover-diagnostic.md](docs/reflections/phase4-after-s22-prior-approval-carryover-diagnostic.md)
- Phase 4 reflection after S22 and next mechanism selection: [docs/reflections/phase4-after-s22-next-mechanism-selection.md](docs/reflections/phase4-after-s22-next-mechanism-selection.md)
- Phase 4 delegated authority provenance protocol v0.1: [protocols/failure-modes/phase4-delegated-authority-provenance-diagnostic-v0.1.md](protocols/failure-modes/phase4-delegated-authority-provenance-diagnostic-v0.1.md)
- Phase 4 S23 delegated authority provenance scenario: [scenarios/org-payment/s23-delegated-authority-provenance-control-slippage.yaml](scenarios/org-payment/s23-delegated-authority-provenance-control-slippage.yaml)
- Phase 4 delegated authority provenance addendum v0.1: [prompts/org-payment/phase4-delegated-authority-provenance-addendum-v0.1.md](prompts/org-payment/phase4-delegated-authority-provenance-addendum-v0.1.md)
- Phase 4 S23 delegated authority provenance diagnostic result: [pilot-runs/org-payment/phase4-s23-delegated-authority-provenance-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s23-delegated-authority-provenance-diagnostic-0001/summary.md)
- Phase 4 S23 delegated authority provenance candidate review: [pilot-runs/org-payment/phase4-s23-delegated-authority-provenance-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s23-delegated-authority-provenance-diagnostic-0001/candidate-review-0001/summary.md)
- Phase 4 reflection after S23 delegated authority provenance diagnostic: [docs/reflections/phase4-after-s23-delegated-authority-provenance-diagnostic.md](docs/reflections/phase4-after-s23-delegated-authority-provenance-diagnostic.md)
- Phase 4 reflection after S23 and next mechanism selection: [docs/reflections/phase4-after-s23-next-mechanism-selection.md](docs/reflections/phase4-after-s23-next-mechanism-selection.md)
- Phase 4 approval artifact mismatch protocol v0.1: [protocols/failure-modes/phase4-approval-artifact-mismatch-diagnostic-v0.1.md](protocols/failure-modes/phase4-approval-artifact-mismatch-diagnostic-v0.1.md)
- Phase 4 S24 approval artifact mismatch scenario: [scenarios/org-payment/s24-approval-artifact-mismatch-control-slippage.yaml](scenarios/org-payment/s24-approval-artifact-mismatch-control-slippage.yaml)
- Phase 4 approval artifact mismatch addendum v0.1: [prompts/org-payment/phase4-approval-artifact-mismatch-addendum-v0.1.md](prompts/org-payment/phase4-approval-artifact-mismatch-addendum-v0.1.md)
- Phase 4 S24 approval artifact mismatch diagnostic result: [pilot-runs/org-payment/phase4-s24-approval-artifact-mismatch-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s24-approval-artifact-mismatch-diagnostic-0001/summary.md)
- Phase 4 S24 approval artifact mismatch candidate review: [pilot-runs/org-payment/phase4-s24-approval-artifact-mismatch-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s24-approval-artifact-mismatch-diagnostic-0001/candidate-review-0001/summary.md)
- Phase 4 reflection after S24 approval artifact mismatch diagnostic: [docs/reflections/phase4-after-s24-approval-artifact-mismatch-diagnostic.md](docs/reflections/phase4-after-s24-approval-artifact-mismatch-diagnostic.md)
- Phase 4 reflection after S24 and next mechanism selection: [docs/reflections/phase4-after-s24-next-mechanism-selection.md](docs/reflections/phase4-after-s24-next-mechanism-selection.md)
- Phase 4 conflicting operational norms protocol v0.1: [protocols/failure-modes/phase4-conflicting-operational-norms-diagnostic-v0.1.md](protocols/failure-modes/phase4-conflicting-operational-norms-diagnostic-v0.1.md)
- Phase 4 S25 conflicting operational norms scenario: [scenarios/org-payment/s25-conflicting-operational-norms-control-slippage.yaml](scenarios/org-payment/s25-conflicting-operational-norms-control-slippage.yaml)
- Phase 4 conflicting operational norms addendum v0.1: [prompts/org-payment/phase4-conflicting-operational-norms-addendum-v0.1.md](prompts/org-payment/phase4-conflicting-operational-norms-addendum-v0.1.md)
- Phase 4 S25 conflicting operational norms diagnostic result: [pilot-runs/org-payment/phase4-s25-conflicting-operational-norms-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s25-conflicting-operational-norms-diagnostic-0001/summary.md)
- Phase 4 S25 conflicting operational norms candidate review: [pilot-runs/org-payment/phase4-s25-conflicting-operational-norms-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s25-conflicting-operational-norms-diagnostic-0001/candidate-review-0001/summary.md)
- Phase 4 reflection after S25 conflicting operational norms diagnostic: [docs/reflections/phase4-after-s25-conflicting-operational-norms-diagnostic.md](docs/reflections/phase4-after-s25-conflicting-operational-norms-diagnostic.md)
- Phase 4 reflection after S25 and next mechanism selection: [docs/reflections/phase4-after-s25-next-mechanism-selection.md](docs/reflections/phase4-after-s25-next-mechanism-selection.md)
- Phase 4 shadow approval / informal preclearance protocol v0.1: [protocols/failure-modes/phase4-shadow-approval-preclearance-diagnostic-v0.1.md](protocols/failure-modes/phase4-shadow-approval-preclearance-diagnostic-v0.1.md)
- Phase 4 S26 shadow approval / informal preclearance scenario: [scenarios/org-payment/s26-shadow-approval-preclearance-control-slippage.yaml](scenarios/org-payment/s26-shadow-approval-preclearance-control-slippage.yaml)
- Phase 4 shadow approval / informal preclearance addendum v0.1: [prompts/org-payment/phase4-shadow-approval-preclearance-addendum-v0.1.md](prompts/org-payment/phase4-shadow-approval-preclearance-addendum-v0.1.md)
- Phase 4 S26 shadow approval / informal preclearance diagnostic result: [pilot-runs/org-payment/phase4-s26-shadow-approval-preclearance-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s26-shadow-approval-preclearance-diagnostic-0001/summary.md)
- Phase 4 S26 shadow approval / informal preclearance candidate review: [pilot-runs/org-payment/phase4-s26-shadow-approval-preclearance-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s26-shadow-approval-preclearance-diagnostic-0001/candidate-review-0001/summary.md)
- Phase 4 reflection after S26 shadow approval / informal preclearance diagnostic: [docs/reflections/phase4-after-s26-shadow-approval-preclearance-diagnostic.md](docs/reflections/phase4-after-s26-shadow-approval-preclearance-diagnostic.md)
- Phase 4 reflection after S26 and next mechanism selection: [docs/reflections/phase4-after-s26-next-mechanism-selection.md](docs/reflections/phase4-after-s26-next-mechanism-selection.md)
- Phase 4 payment-draft staging protocol v0.1: [protocols/failure-modes/phase4-payment-draft-staging-diagnostic-v0.1.md](protocols/failure-modes/phase4-payment-draft-staging-diagnostic-v0.1.md)
- Phase 4 S27 payment-draft staging scenario: [scenarios/org-payment/s27-payment-draft-staging-control-slippage.yaml](scenarios/org-payment/s27-payment-draft-staging-control-slippage.yaml)
- Phase 4 payment-draft staging addendum v0.1: [prompts/org-payment/phase4-payment-draft-staging-addendum-v0.1.md](prompts/org-payment/phase4-payment-draft-staging-addendum-v0.1.md)
- Phase 4 S27 payment-draft staging diagnostic result: [pilot-runs/org-payment/phase4-s27-payment-draft-staging-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s27-payment-draft-staging-diagnostic-0001/summary.md)
- Phase 4 S27 payment-draft staging candidate review: [pilot-runs/org-payment/phase4-s27-payment-draft-staging-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s27-payment-draft-staging-diagnostic-0001/candidate-review-0001/summary.md)
- Phase 4 S27 payment-draft staging project-owner review: [pilot-runs/org-payment/phase4-s27-payment-draft-staging-diagnostic-0001/project-owner-review-0001/summary.md](pilot-runs/org-payment/phase4-s27-payment-draft-staging-diagnostic-0001/project-owner-review-0001/summary.md)
- Phase 4 reflection after S27 payment-draft staging diagnostic: [docs/reflections/phase4-after-s27-payment-draft-staging-diagnostic.md](docs/reflections/phase4-after-s27-payment-draft-staging-diagnostic.md)
- Phase 4 reflection after S27 project-owner review: [docs/reflections/phase4-after-s27-project-owner-review.md](docs/reflections/phase4-after-s27-project-owner-review.md)
- Phase 4 reflection after S27 and next mechanism selection: [docs/reflections/phase4-after-s27-next-mechanism-selection.md](docs/reflections/phase4-after-s27-next-mechanism-selection.md)
- Phase 4 structuring / approval-splitting protocol v0.1: [protocols/failure-modes/phase4-structuring-approval-splitting-diagnostic-v0.1.md](protocols/failure-modes/phase4-structuring-approval-splitting-diagnostic-v0.1.md)
- Phase 4 S28 structuring / approval-splitting scenario: [scenarios/org-payment/s28-structuring-approval-splitting.yaml](scenarios/org-payment/s28-structuring-approval-splitting.yaml)
- Phase 4 structuring / approval-splitting addendum v0.1: [prompts/org-payment/phase4-structuring-approval-splitting-addendum-v0.1.md](prompts/org-payment/phase4-structuring-approval-splitting-addendum-v0.1.md)
- Phase 4 S28 structuring / approval-splitting diagnostic result: [pilot-runs/org-payment/phase4-s28-structuring-approval-splitting-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s28-structuring-approval-splitting-diagnostic-0001/summary.md)
- Phase 4 S28 structuring / approval-splitting candidate review: [pilot-runs/org-payment/phase4-s28-structuring-approval-splitting-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s28-structuring-approval-splitting-diagnostic-0001/candidate-review-0001/summary.md)
- Phase 4 S28 structuring / approval-splitting synthesis v0.1: [docs/synthesis/phase4-structuring-approval-splitting-synthesis-v0.1.md](docs/synthesis/phase4-structuring-approval-splitting-synthesis-v0.1.md)
- Phase 4 reflection after S28 structuring / approval-splitting diagnostic: [docs/reflections/phase4-after-s28-structuring-approval-splitting-review.md](docs/reflections/phase4-after-s28-structuring-approval-splitting-review.md)
- Phase 4 reflection after S28 research correction: [docs/reflections/phase4-after-s28-research-correction.md](docs/reflections/phase4-after-s28-research-correction.md)
- Phase 4 applicant-side structuring protocol v0.1: [protocols/failure-modes/phase4-applicant-side-structuring-diagnostic-v0.1.md](protocols/failure-modes/phase4-applicant-side-structuring-diagnostic-v0.1.md)
- Phase 4 S29 applicant-side structuring scenario: [scenarios/org-payment/s29-applicant-side-structuring.yaml](scenarios/org-payment/s29-applicant-side-structuring.yaml)
- Phase 4 applicant-side structuring addendum v0.1: [prompts/org-payment/phase4-applicant-side-structuring-addendum-v0.1.md](prompts/org-payment/phase4-applicant-side-structuring-addendum-v0.1.md)
- Phase 4 S29 applicant-side structuring diagnostic result: [pilot-runs/org-payment/phase4-s29-applicant-side-structuring-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s29-applicant-side-structuring-diagnostic-0001/summary.md)
- Phase 4 S29 applicant-side structuring candidate review: [pilot-runs/org-payment/phase4-s29-applicant-side-structuring-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s29-applicant-side-structuring-diagnostic-0001/candidate-review-0001/summary.md)
- Phase 4 S29 applicant-side structuring project-owner review: [pilot-runs/org-payment/phase4-s29-applicant-side-structuring-diagnostic-0001/project-owner-review-0001/summary.md](pilot-runs/org-payment/phase4-s29-applicant-side-structuring-diagnostic-0001/project-owner-review-0001/summary.md)
- Phase 4 reflection after S29 applicant-side structuring diagnostic: [docs/reflections/phase4-after-s29-applicant-side-structuring-review.md](docs/reflections/phase4-after-s29-applicant-side-structuring-review.md)
- Phase 4 S29 applicant-side structuring synthesis v0.1: [docs/synthesis/phase4-applicant-side-structuring-synthesis-v0.1.md](docs/synthesis/phase4-applicant-side-structuring-synthesis-v0.1.md)
- Phase 4 S30 freeform applicant structuring protocol v0.1: [protocols/failure-modes/phase4-freeform-applicant-structuring-diagnostic-v0.1.md](protocols/failure-modes/phase4-freeform-applicant-structuring-diagnostic-v0.1.md)
- Phase 4 S30 freeform applicant structuring scenario: [scenarios/org-payment/s30-freeform-applicant-structuring.yaml](scenarios/org-payment/s30-freeform-applicant-structuring.yaml)
- Phase 4 S30 freeform applicant structuring addendum v0.1: [prompts/org-payment/phase4-freeform-applicant-structuring-addendum-v0.1.md](prompts/org-payment/phase4-freeform-applicant-structuring-addendum-v0.1.md)
- Phase 4 S30 freeform applicant structuring diagnostic result: [pilot-runs/org-payment/phase4-s30-freeform-applicant-structuring-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s30-freeform-applicant-structuring-diagnostic-0001/summary.md)
- Phase 4 S30 freeform applicant structuring candidate review: [pilot-runs/org-payment/phase4-s30-freeform-applicant-structuring-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s30-freeform-applicant-structuring-diagnostic-0001/candidate-review-0001/summary.md)
- Phase 4 reflection after S30 freeform applicant structuring: [docs/reflections/phase4-after-s30-freeform-applicant-structuring-review.md](docs/reflections/phase4-after-s30-freeform-applicant-structuring-review.md)
- Phase 4 freeform vs menu-conditioned structuring synthesis v0.1: [docs/synthesis/phase4-freeform-vs-menu-conditioned-structuring-synthesis-v0.1.md](docs/synthesis/phase4-freeform-vs-menu-conditioned-structuring-synthesis-v0.1.md)
- Phase 4 advisor-seeded structuring protocol v0.1: [protocols/failure-modes/phase4-advisor-seeded-structuring-diagnostic-v0.1.md](protocols/failure-modes/phase4-advisor-seeded-structuring-diagnostic-v0.1.md)
- Phase 4 S31 advisor-seeded structuring scenario: [scenarios/org-payment/s31-advisor-seeded-structuring.yaml](scenarios/org-payment/s31-advisor-seeded-structuring.yaml)
- Phase 4 advisor-seeded structuring addendum v0.1: [prompts/org-payment/phase4-advisor-seeded-structuring-addendum-v0.1.md](prompts/org-payment/phase4-advisor-seeded-structuring-addendum-v0.1.md)
- Phase 4 S31 advisor-seeded structuring diagnostic result: [pilot-runs/org-payment/phase4-s31-advisor-seeded-structuring-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s31-advisor-seeded-structuring-diagnostic-0001/summary.md)
- Phase 4 S31 advisor-seeded structuring candidate review: [pilot-runs/org-payment/phase4-s31-advisor-seeded-structuring-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s31-advisor-seeded-structuring-diagnostic-0001/candidate-review-0001/summary.md)
- Phase 4 reflection after S31 advisor-seeded structuring: [docs/reflections/phase4-after-s31-advisor-seeded-structuring-review.md](docs/reflections/phase4-after-s31-advisor-seeded-structuring-review.md)
- Phase 4 S31 advisor-seeded structuring synthesis v0.1: [docs/synthesis/phase4-advisor-seeded-structuring-synthesis-v0.1.md](docs/synthesis/phase4-advisor-seeded-structuring-synthesis-v0.1.md)
- Phase 4 reflection after S31 next mechanism selection: [docs/reflections/phase4-after-s31-next-mechanism-selection.md](docs/reflections/phase4-after-s31-next-mechanism-selection.md)
- Phase 4 S32 recommendation-weighted advisor structuring protocol v0.1: [protocols/failure-modes/phase4-recommendation-weighted-advisor-structuring-diagnostic-v0.1.md](protocols/failure-modes/phase4-recommendation-weighted-advisor-structuring-diagnostic-v0.1.md)
- Phase 4 S32 recommendation-weighted advisor structuring scenario: [scenarios/org-payment/s32-recommendation-weighted-advisor-structuring.yaml](scenarios/org-payment/s32-recommendation-weighted-advisor-structuring.yaml)
- Phase 4 S32 recommendation-weighted advisor structuring addendum v0.1: [prompts/org-payment/phase4-recommendation-weighted-advisor-structuring-addendum-v0.1.md](prompts/org-payment/phase4-recommendation-weighted-advisor-structuring-addendum-v0.1.md)
- Phase 4 reflection after S32 design correction: [docs/reflections/phase4-after-s32-design-correction-gray-option-selection.md](docs/reflections/phase4-after-s32-design-correction-gray-option-selection.md)
- Phase 4 S33 gray-option seeded structuring protocol v0.1: [protocols/failure-modes/phase4-gray-option-seeded-structuring-diagnostic-v0.1.md](protocols/failure-modes/phase4-gray-option-seeded-structuring-diagnostic-v0.1.md)
- Phase 4 S33 gray-option seeded structuring scenario: [scenarios/org-payment/s33-gray-option-seeded-structuring.yaml](scenarios/org-payment/s33-gray-option-seeded-structuring.yaml)
- Phase 4 S33 gray-option seeded structuring addendum v0.1: [prompts/org-payment/phase4-gray-option-seeded-structuring-addendum-v0.1.md](prompts/org-payment/phase4-gray-option-seeded-structuring-addendum-v0.1.md)
- Phase 4 S33 gray-option seeded structuring result: [pilot-runs/org-payment/phase4-s33-gray-option-seeded-structuring-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s33-gray-option-seeded-structuring-diagnostic-0001/summary.md)
- Phase 4 S33 gray-option seeded structuring synthesis: [docs/synthesis/phase4-gray-option-seeded-structuring-synthesis-v0.1.md](docs/synthesis/phase4-gray-option-seeded-structuring-synthesis-v0.1.md)
- Phase 1-4 project synthesis v0.1: [docs/synthesis/phase1-4-project-synthesis-v0.1.md](docs/synthesis/phase1-4-project-synthesis-v0.1.md)
- Phase 1-4 report outline: [docs/reports/phase1-4-report-outline.md](docs/reports/phase1-4-report-outline.md)
- Method B synthesis protocol v0.1: [protocols/synthesis/method-b-synthesis-v0.1.md](protocols/synthesis/method-b-synthesis-v0.1.md)
- Method B synthesis v0.1: [docs/synthesis/method-b-synthesis-v0.1.md](docs/synthesis/method-b-synthesis-v0.1.md)
- Method B failure-mode status table: [docs/synthesis/method-b-failure-mode-status.csv](docs/synthesis/method-b-failure-mode-status.csv)
- Method B claim-boundary review: [docs/synthesis/method-b-claim-boundary-review.md](docs/synthesis/method-b-claim-boundary-review.md)
- Method B BC28 FM6 candidate review: [pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/fm6-candidate-review-0001/summary.md](pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/fm6-candidate-review-0001/summary.md)
- Method B+ BC36 reflection after FM6 review: [docs/reflections/method-b-plus-bc36-after-fm6-review.md](docs/reflections/method-b-plus-bc36-after-fm6-review.md)
- Method B+ BC31 ambiguity interpretation protocol v0.1: [protocols/failure-modes/method-b-plus-ambiguity-interpretation-v0.1.md](protocols/failure-modes/method-b-plus-ambiguity-interpretation-v0.1.md)
- Method B+ S13 ambiguous approval interpretation scenario: [scenarios/org-payment/s13-ambiguous-approval-interpretation.yaml](scenarios/org-payment/s13-ambiguous-approval-interpretation.yaml)
- Method B+ ambiguity interpretation prompt addendum v0.1: [prompts/org-payment/method-b-plus-ambiguity-interpretation-addendum-v0.1.md](prompts/org-payment/method-b-plus-ambiguity-interpretation-addendum-v0.1.md)
- Method B+ BC31 ambiguity interpretation pilot result: [pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/summary.md](pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/summary.md)
- Method B+ BC31 ambiguity candidate review: [pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/ambiguity-candidate-review-0001/summary.md](pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/ambiguity-candidate-review-0001/summary.md)
- Method B+ BC31 FM2 independent review: [pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/bc31-fm2-independent-review-0001/summary.md](pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/bc31-fm2-independent-review-0001/summary.md)
- Method B+ BC36 reflection after BC31 FM2 independent review: [docs/reflections/method-b-plus-bc36-after-bc31-fm2-independent-review.md](docs/reflections/method-b-plus-bc36-after-bc31-fm2-independent-review.md)
- Method B+ non-intentional control slippage taxonomy v0.1: [protocols/failure-modes/non-intentional-control-slippage-taxonomy-v0.1.md](protocols/failure-modes/non-intentional-control-slippage-taxonomy-v0.1.md)
- Method B+ non-intentional control slippage map: [docs/synthesis/non-intentional-control-slippage-map.csv](docs/synthesis/non-intentional-control-slippage-map.csv)
- Method B+ SL2-SL4 control slippage progression diagnostic protocol v0.1: [protocols/failure-modes/method-b-plus-control-slippage-progression-diagnostic-v0.1.md](protocols/failure-modes/method-b-plus-control-slippage-progression-diagnostic-v0.1.md)
- Method B+ S17 control slippage progression scenario: [scenarios/org-payment/s17-control-slippage-progression-diagnostic.yaml](scenarios/org-payment/s17-control-slippage-progression-diagnostic.yaml)
- Method B+ control slippage progression prompt addendum v0.1: [prompts/org-payment/method-b-plus-control-slippage-progression-addendum-v0.1.md](prompts/org-payment/method-b-plus-control-slippage-progression-addendum-v0.1.md)
- Method B+ S17 control slippage progression diagnostic result: [pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/summary.md](pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/summary.md)
- Method B+ S17 control slippage progression candidate review: [pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/candidate-review-0001/summary.md)
- Method B+ BC36 reflection after S17 control slippage review: [docs/reflections/method-b-plus-bc36-after-slippage-progression-review.md](docs/reflections/method-b-plus-bc36-after-slippage-progression-review.md)
- Method B+ mechanism iteration synthesis v0.1: [docs/synthesis/method-b-plus-mechanism-iteration-synthesis-v0.1.md](docs/synthesis/method-b-plus-mechanism-iteration-synthesis-v0.1.md)
- Method B+ queue/ticket state mismatch diagnostic protocol v0.1: [protocols/failure-modes/method-b-plus-queue-ticket-state-mismatch-diagnostic-v0.1.md](protocols/failure-modes/method-b-plus-queue-ticket-state-mismatch-diagnostic-v0.1.md)
- Method B+ S19 queue/ticket state mismatch scenario: [scenarios/org-payment/s19-queue-ticket-state-mismatch-control-slippage.yaml](scenarios/org-payment/s19-queue-ticket-state-mismatch-control-slippage.yaml)
- Method B+ queue/ticket state mismatch prompt addendum v0.1: [prompts/org-payment/method-b-plus-queue-ticket-state-mismatch-addendum-v0.1.md](prompts/org-payment/method-b-plus-queue-ticket-state-mismatch-addendum-v0.1.md)
- Method B+ S19 queue/ticket state mismatch diagnostic result: [pilot-runs/org-payment/method-b-plus-queue-ticket-state-mismatch-diagnostic-pilot-0001/summary.md](pilot-runs/org-payment/method-b-plus-queue-ticket-state-mismatch-diagnostic-pilot-0001/summary.md)
- Method B+ S19 queue/ticket state mismatch candidate review: [pilot-runs/org-payment/method-b-plus-queue-ticket-state-mismatch-diagnostic-pilot-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/method-b-plus-queue-ticket-state-mismatch-diagnostic-pilot-0001/candidate-review-0001/summary.md)
- Method B+ BC36 reflection after S19 queue/ticket review: [docs/reflections/method-b-plus-bc36-after-queue-ticket-state-mismatch-review.md](docs/reflections/method-b-plus-bc36-after-queue-ticket-state-mismatch-review.md)
- Method B+ periodic synthesis after S18/S19: [docs/synthesis/method-b-plus-periodic-synthesis-after-s18-s19-v0.1.md](docs/synthesis/method-b-plus-periodic-synthesis-after-s18-s19-v0.1.md)
- Method B+ endpoint claim-hardening review: [docs/synthesis/method-b-plus-endpoint-claim-hardening-review-v0.1.md](docs/synthesis/method-b-plus-endpoint-claim-hardening-review-v0.1.md)
- Method B+ BC36 reflection after BC31 review: [docs/reflections/method-b-plus-bc36-after-bc31-review.md](docs/reflections/method-b-plus-bc36-after-bc31-review.md)
- Method B+ BC37-C approval bypass stress protocol v0.1: [protocols/failure-modes/method-b-plus-approval-bypass-stress-v0.1.md](protocols/failure-modes/method-b-plus-approval-bypass-stress-v0.1.md)
- Method B+ S14 approval bypass stress scenario: [scenarios/org-payment/s14-approval-bypass-stress.yaml](scenarios/org-payment/s14-approval-bypass-stress.yaml)
- Method B+ approval bypass stress prompt addendum v0.1: [prompts/org-payment/method-b-plus-approval-bypass-stress-addendum-v0.1.md](prompts/org-payment/method-b-plus-approval-bypass-stress-addendum-v0.1.md)
- Method B+ BC37-C approval bypass stress pilot result: [pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/summary.md](pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/summary.md)
- Method B+ BC37-C approval bypass stress candidate review: [pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/candidate-review-0001/summary.md)
- Method B+ BC36 reflection after BC37-C review: [docs/reflections/method-b-plus-bc36-after-bc37c-review.md](docs/reflections/method-b-plus-bc36-after-bc37c-review.md)
- Method B+ BC32 responsibility boundary protocol v0.1: [protocols/failure-modes/method-b-plus-responsibility-boundary-v0.1.md](protocols/failure-modes/method-b-plus-responsibility-boundary-v0.1.md)
- Method B+ S15 responsibility boundary stress scenario: [scenarios/org-payment/s15-responsibility-boundary-stress.yaml](scenarios/org-payment/s15-responsibility-boundary-stress.yaml)
- Method B+ responsibility boundary prompt addendum v0.1: [prompts/org-payment/method-b-plus-responsibility-boundary-addendum-v0.1.md](prompts/org-payment/method-b-plus-responsibility-boundary-addendum-v0.1.md)
- Method B+ BC32 responsibility boundary pilot result: [pilot-runs/org-payment/method-b-plus-responsibility-boundary-pilot-0001/summary.md](pilot-runs/org-payment/method-b-plus-responsibility-boundary-pilot-0001/summary.md)
- Method B+ BC36 reflection after BC32 execution: [docs/reflections/method-b-plus-bc36-after-bc32-execution.md](docs/reflections/method-b-plus-bc36-after-bc32-execution.md)
- Method B+ BC35 evidence-gap erasure diagnostic protocol v0.1: [protocols/failure-modes/method-b-plus-evidence-gap-erasure-diagnostic-v0.1.md](protocols/failure-modes/method-b-plus-evidence-gap-erasure-diagnostic-v0.1.md)
- Method B+ S16 evidence-gap erasure diagnostic scenario: [scenarios/org-payment/s16-evidence-gap-erasure-diagnostic.yaml](scenarios/org-payment/s16-evidence-gap-erasure-diagnostic.yaml)
- Method B+ evidence-gap erasure prompt addendum v0.1: [prompts/org-payment/method-b-plus-evidence-gap-erasure-addendum-v0.1.md](prompts/org-payment/method-b-plus-evidence-gap-erasure-addendum-v0.1.md)
- Method B+ BC35 evidence-gap erasure diagnostic pilot result: [pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/summary.md](pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/summary.md)
- Method B+ BC35 FM6 candidate review: [pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/candidate-review-0001/summary.md)
- Method B+ BC36 reflection after BC35 review: [docs/reflections/method-b-plus-bc36-after-bc35-review.md](docs/reflections/method-b-plus-bc36-after-bc35-review.md)
- Method B+ iterative targeting synthesis v0.1: [docs/synthesis/method-b-plus-iterative-targeting-synthesis-v0.1.md](docs/synthesis/method-b-plus-iterative-targeting-synthesis-v0.1.md)
- Method B+ failure-mode status table: [docs/synthesis/method-b-plus-failure-mode-status.csv](docs/synthesis/method-b-plus-failure-mode-status.csv)
- Method B failure-mode taxonomy v0.1: [protocols/failure-modes/failure-mode-taxonomy-v0.1.md](protocols/failure-modes/failure-mode-taxonomy-v0.1.md)
- Method B multi-turn memory and justification pilot v0.1: [protocols/failure-modes/multi-turn-memory-justification-pilot-v0.1.md](protocols/failure-modes/multi-turn-memory-justification-pilot-v0.1.md)
- Method B targeted failure-mode pilot v0.1: [protocols/failure-modes/targeted-failure-mode-pilot-v0.1.md](protocols/failure-modes/targeted-failure-mode-pilot-v0.1.md)
- Method B failure-mode evidence review v0.1: [protocols/failure-modes/method-b-failure-mode-review-v0.1.md](protocols/failure-modes/method-b-failure-mode-review-v0.1.md)
- Method B failure-mode baseline decision v0.1: [protocols/failure-modes/failure-mode-baseline-decision-v0.1.md](protocols/failure-modes/failure-mode-baseline-decision-v0.1.md)
- Method B diagnostic sensitivity protocol v0.1: [protocols/failure-modes/failure-mode-diagnostic-sensitivity-v0.1.md](protocols/failure-modes/failure-mode-diagnostic-sensitivity-v0.1.md)
- Method B second-domain failure-mode transfer protocol v0.1: [protocols/failure-modes/second-domain-failure-mode-transfer-v0.1.md](protocols/failure-modes/second-domain-failure-mode-transfer-v0.1.md)

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
18. P8 M02 execution bundle: execute the frozen S04 buyer+vendor pressure pilot without changing protocol conditions.
19. P8 M02 review and M03 protocol bundle: review M02 and freeze the buyer+approver+accountant coordination pilot protocol without executing M03.
20. P8 M03 execution bundle: execute the frozen S04 buyer+approver+accountant coordination pilot without changing protocol conditions.
21. P8 M03 review and M04 protocol bundle: review M03 and freeze the buyer+approver+accountant+vendor full-path pilot protocol without executing M04.
22. P8 M04 execution bundle: execute the frozen S04 buyer+approver+accountant+vendor full-path pilot without changing protocol conditions.
23. P8 M04 review and M05 protocol bundle: review M04 and freeze the requester+vendor+buyer+approver+accountant pilot protocol without executing M05.
24. P8 M05 execution bundle: execute the frozen S04 requester+vendor+buyer+approver+accountant pilot without changing protocol conditions.
25. P8 M05 review and multi-role scenario sweep protocol bundle: review M05 and freeze the S01-S06 full org-payment scenario sweep pilot protocol without executing the sweep.
26. P8 multi-role scenario sweep execution bundle: execute the frozen S01-S06 requester+vendor+buyer+approver+accountant scenario sweep pilot without changing protocol conditions.
27. P8 multi-role scenario sweep review and baseline protocol bundle: review the S01-S06 full org-payment scenario sweep and freeze EXP-0002 multi-role baseline conditions before baseline execution.
28. P8 multi-role baseline execution bundle: execute EXP-0002 under frozen conditions and add curated aggregate baseline result.
29. P9 EXP-0002 review and human evidence review protocol bundle: review the multi-role baseline and freeze EXP-0002-HR-0001 before any human-reviewed judgments are recorded.
30. P9 LLM-assisted evidence pre-review bundle: add candidate judgments and escalation items for EXP-0002 representative evidence packs without marking any event as human-reviewed.
31. P9 human evidence review bundle: record primary human confirmation for EXP-0002-HR-0001 representative evidence review and preserve metric revision items.
32. P9 construct validity protocol bundle: freeze EXP-0002-CV-0001 construct definitions, evidence requirements, examples, and claim boundaries before construct-level synthesis.
33. P9 construct validity execution bundle: execute EXP-0002-CV-0001 and record construct support, limitations, examples, and pressure metric revision needs.
34. P9 pressure-citation metric correction bundle: tighten future pressure-citation metrics so routine `request_payment_status` paths preserve vendor context without being counted as vendor pressure.
35. P9 intervention validity protocol bundle: freeze EXP-0003 as a descriptive S01-S06 institutional stress test over the committed EXP-0002 baseline artifacts.
36. P9 intervention validity execution bundle: execute EXP-0003 as a post-baseline descriptive stress test without new LLM runs or causal/statistical claims.
37. P9 provider-randomness sensitivity protocol bundle: freeze EXP-0004 as a small repeat-run sensitivity check with model, prompts, menus, scenarios, parser, and Game Master held fixed.
38. P9 provider-randomness sensitivity execution bundle: execute EXP-0004 and compare fresh repeat-run paths descriptively with EXP-0002.
39. P10 second-domain protocol bundle: review EXP-0004, select expense reimbursement as the second domain, and freeze EXP-0005 without executing second-domain runs.
40. P10 second-domain execution bundle: execute EXP-0005 on ER01 and add curated aggregate result without cross-domain generalization claims.
41. P10 synthesis protocol bundle: review EXP-0005 and freeze BC20 social-chaos claim synthesis inputs, claim levels, and forbidden claims before writing synthesis.
42. P10 synthesis execution bundle: write the BC20 social-chaos claim synthesis, evidence map, limitations, and claim-boundary review without adding new runs or upgrading evidence strength.
43. Method B BC21 failure-mode taxonomy bundle: define responsibility diffusion, approval bypass, ambiguous guidance misinterpretation, pressure-normalization, evidence-gap erasure, and post-hoc justification candidates before adding high-friction scenarios.
44. Method B BC22 high-friction scenario design bundle: introduce S07-S12 org-payment scenarios targeting failure-mode candidates without execution, prompt, action menu, Game Master, event taxonomy, or result changes.
45. Method B BC23 multi-turn memory and justification pilot bundle: define bounded short-term memory, post-hoc explanation artifacts, and a reviewable S09 paper trace before targeted failure-mode execution.
46. Method B BC24 targeted failure-mode pilot bundle: execute S09/S12 targeted full-role pilots, record candidate/not-observed failure-mode statuses, and prepare human pre-review material without supported failure-mode claims.
47. Method B BC25 failure-mode evidence review bundle: review BC24 candidate/not-observed material, keep candidate/support boundaries intact, and record that no Method B failure mode is supported in the curated representative evidence.
48. Method B BC26 baseline decision bundle: record that no failure-mode baseline protocol can be frozen because BC25 produced no supported or partially supported Method B failure-mode target.
49. Method B BC27 baseline execution status bundle: record that controlled failure-mode baseline execution is not executable because no baseline protocol was frozen.
50. Method B BC28 diagnostic sensitivity protocol bundle: freeze a prompt-framing diagnostic sensitivity pilot that changes only role-local prompt framing before execution.
51. Method B BC28 diagnostic sensitivity execution bundle: execute `METHOD-B-DSP-0001`, record candidate/not-observed failure-mode statuses, and compare descriptively against BC24 without prompt-causation or supported failure-mode claims.
52. Method B BC29 second-domain transfer review bundle: review existing EXP-0005 expense-reimbursement evidence against Method B failure-mode mapping without new runs or cross-domain validation claims.
53. Method B BC30 synthesis bundle: synthesize BC21-BC29 failure-mode status, evidence levels, human-review scope, diagnostic sensitivity, and second-domain limits without supported failure-mode or human-society claims.
54. Method B BC28 FM6 candidate review bundle: review the three generated FM6 post-hoc-justification candidate rows and decide whether any are supported, partially supported, rejected, or need revision.
55. Method B+ BC36 reflection bundle: reflect on the rejected FM6 review result and select BC31 ambiguity interpretation targeting as the next checkpoint without adding execution.
56. Method B+ BC31 ambiguity interpretation protocol bundle: introduce S13 and freeze the ambiguity targeting protocol, prompt addendum, action menus, Game Master rules, candidate rules, evidence requirements, and claim boundary before execution.
57. Method B+ BC31 ambiguity interpretation execution bundle: execute the frozen S13 buyer/accountant ambiguity pilot, record candidate/not-observed rows, and preserve candidate/support boundaries.
58. Method B+ BC31 ambiguity candidate review bundle: review the four generated BC31 candidate rows and classify them without adding new runs or changing failure-mode definitions.
59. Method B+ BC36 reflection after BC31 review bundle: reflect on the partial FM2 handoff observation and select an approval-bypass stress variant as the next checkpoint without adding execution.
60. Method B+ BC37-C approval-bypass stress protocol bundle: introduce S14 and freeze handoff/preparation/payment-ready candidate distinctions before execution.
61. Method B+ BC37-C approval-bypass stress execution bundle: execute the frozen S14 buyer/accountant stress pilot, record candidate/not-observed rows, and preserve candidate/support boundaries.
62. Method B+ BC32 responsibility-boundary protocol/execution/reflection bundles: freeze S15 responsibility-boundary targeting, execute the pilot, and record that no generated candidate rows were produced.
63. Method B+ BC35 evidence-gap erasure protocol bundle: introduce S16 and freeze the G001/G002 evidence-gap diagnostic before execution.
64. Method B+ BC35 evidence-gap erasure execution bundle: execute the frozen S16 buyer/accountant diagnostic, record candidate/not-observed rows, and preserve candidate/support boundaries.
65. Method B+ BC35 FM6 candidate review bundle: review the three generated FM6 candidate rows without adding runs or changing failure-mode definitions.
66. Method B+ BC36 reflection after BC35 review bundle: synthesize the BC35 review outcome and select a Method B+ iterative targeting synthesis as the next checkpoint.
67. Method B+ iterative targeting synthesis bundle: summarize BC34/BC28, BC31, BC37-C, BC32, and BC35 status without adding runs or upgrading claims.
68. Method B+ control-slippage reframing bundle: reflect after the BC31 FM2 independent review and add a non-intentional control slippage taxonomy plus mapping without adding runs or upgrading BC31 to full approval-bypass support.
69. Method B+ SL2-SL4 control-slippage progression protocol bundle: freeze S17, a prompt addendum, action menus, Game Master rules, and candidate/reporting requirements before execution.
70. Method B+ SL2-SL4 control-slippage progression execution/review bundle: execute frozen S17, review generated rows, update synthesis, and pause targeted execution after conservative gap preservation.

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

## M02 Buyer+Vendor Pressure Pilot

Run the frozen M02 pilot locally with raw and generated curated output under ignored `runs/` paths:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-m02-buyer-vendor-pressure-pilot `
  --output runs/org-payment/m02-buyer-vendor-pressure-pilot-local/raw `
  --curated-output runs/org-payment/m02-buyer-vendor-pressure-pilot-local/curated `
  --dotenv .env
```

Reference M02 pilot output:

- [pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/summary.md](pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/summary.md)
- [pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/aggregate.json](pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/aggregate.json)
- [pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/execution-manifest.json](pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/execution-manifest.json)
- [pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/scenario-summary.csv](pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/scenario-summary.csv)
- [pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/representative-evidence-packs](pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/representative-evidence-packs)
- [pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/representative-validation-outputs](pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/representative-validation-outputs)

Under the frozen M02 artificial organization protocol, vendor+buyer LLM pilot runs produced recorded vendor pressure actions, buyer response actions, paired paths, parser outcomes, GM decisions, validation outcomes, and pressure-citation observations. M02 remains a pressure pilot, not a multi-role baseline. It does not support pressure-causation, statistical, human behavior, real-world organization, compliance, legal, audit, or operational claims.

## M02 Review and M03 Coordination Protocol

The M02 review is recorded in [pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/review.md](pilot-runs/org-payment/m02-buyer-vendor-pressure-pilot-0001/review.md).

The review records that M02 established mechanically valid buyer+vendor pressure-pilot evidence generation, with 5 attempted runs, 5 accepted runs, 0 exclusions, no parser failures, no validation failures, and no rejected or invalid proposals. Vendor selected `apply_deadline_pressure` in all 5 runs. Buyer selected `request_approval` in all 5 runs. Pressure-citation fields were present in all included buyer actions.

The review also records that M02 did not show buyer action-selection variation and does not prove that vendor pressure caused buyer behavior. The checkpoint decision is to advance to M03 buyer+approver+accountant coordination pilot protocol.

The M03 protocol is frozen in [protocols/multi-role/m03-buyer-approver-accountant-coordination-pilot-v0.1.md](protocols/multi-role/m03-buyer-approver-accountant-coordination-pilot-v0.1.md). M03 is S04 only, 5 attempted runs, buyer + approver + accountant LLM-controlled, requester/vendor scripted or rule-based, deterministic menu-aware Game Master, OpenAI `gpt-4.1-mini`, generated/proposed event labels only, and claim boundary `multi_role_coordination_pilot_observation_only`.

The M03 approver prompt template is [prompts/org-payment/approver-multirole-action-v0.1.md](prompts/org-payment/approver-multirole-action-v0.1.md). The M01 prompt [prompts/org-payment/approver-free-choice-action-v0.1.md](prompts/org-payment/approver-free-choice-action-v0.1.md) remains the frozen M01 prompt and is not revised retroactively.

The accountant prompt template is [prompts/org-payment/accountant-free-choice-action-v0.1.md](prompts/org-payment/accountant-free-choice-action-v0.1.md). It instructs the accountant not to simulate other roles, bypass the Game Master, treat pressure as approval evidence, or treat ambiguous guidance as explicit approval unless explicit approval is recorded in the provided evidence.

This protocol-freeze step does not execute M03 and does not add M03 results. It does not make responsibility-diffusion, approval-bypass, statistical, human behavior, real-world organization, compliance, legal, audit, model comparison, or multi-role baseline claims.

## M03 Buyer+Approver+Accountant Coordination Pilot

Run the frozen M03 pilot locally with raw and generated curated output under ignored `runs/` paths:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-m03-buyer-approver-accountant-coordination-pilot `
  --output runs/org-payment/m03-buyer-approver-accountant-coordination-pilot-local/raw `
  --curated-output runs/org-payment/m03-buyer-approver-accountant-coordination-pilot-local/curated `
  --dotenv .env
```

Reference M03 pilot output:

- [summary.md](pilot-runs/org-payment/m03-buyer-approver-accountant-coordination-pilot-0001/summary.md)
- [aggregate.json](pilot-runs/org-payment/m03-buyer-approver-accountant-coordination-pilot-0001/aggregate.json)
- [execution-manifest.json](pilot-runs/org-payment/m03-buyer-approver-accountant-coordination-pilot-0001/execution-manifest.json)
- [scenario-summary.csv](pilot-runs/org-payment/m03-buyer-approver-accountant-coordination-pilot-0001/scenario-summary.csv)
- Representative evidence pack: [path-001](pilot-runs/org-payment/m03-buyer-approver-accountant-coordination-pilot-0001/representative-evidence-packs/path-001)
- Representative validation output: [path-001.md](pilot-runs/org-payment/m03-buyer-approver-accountant-coordination-pilot-0001/representative-validation-outputs/path-001.md)

Under the frozen M03 artificial organization protocol, buyer+approver+accountant LLM pilot runs produced recorded coordination paths, parser outcomes, GM decisions, validation outcomes, approval-evidence propagation observations, and coordination-gap observations. M03 remains a coordination pilot, not a multi-role baseline. It does not support responsibility-diffusion, approval-bypass, statistical, human behavior, real-world organization, compliance, legal, audit, or operational claims.

## M03 Review and M04 Full-Path Protocol

The M03 review is recorded in [pilot-runs/org-payment/m03-buyer-approver-accountant-coordination-pilot-0001/review.md](pilot-runs/org-payment/m03-buyer-approver-accountant-coordination-pilot-0001/review.md).

The review records that M03 established mechanically valid buyer+approver+accountant coordination-pilot evidence generation, with 5 attempted runs, 5 accepted runs, 0 exclusions, no parser failures, no validation failures, and no rejected or invalid proposals. The observed full coordination path was `request_approval -> approve_payment -> submit_payment_request -> prepare_payment` in all 5 runs. No ambiguous approval, evidence-gap, approval-bypass, or responsibility-diffusion path was observed in the curated 5-run pilot.

The checkpoint decision is to advance to M04 buyer+approver+accountant+vendor full-path pilot protocol. The M04 protocol is frozen in [protocols/multi-role/m04-buyer-approver-accountant-vendor-pilot-v0.1.md](protocols/multi-role/m04-buyer-approver-accountant-vendor-pilot-v0.1.md). M04 is S04 only, 5 attempted runs, vendor + buyer + approver + accountant LLM-controlled, requester scripted or rule-based, deterministic menu-aware Game Master, OpenAI `gpt-4.1-mini`, generated/proposed event labels only, and claim boundary `multi_role_full_path_pilot_observation_only`.

This protocol-freeze step does not execute M04 and does not add M04 results. It does not make pressure-causation, pressure-propagation, responsibility-diffusion, approval-bypass, statistical, human behavior, real-world organization, compliance, legal, audit, model comparison, or multi-role baseline claims.

## M04 Buyer+Approver+Accountant+Vendor Full-Path Pilot

Run the frozen M04 pilot locally with raw and generated curated output under ignored `runs/` paths:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-m04-buyer-approver-accountant-vendor-pilot `
  --output runs/org-payment/m04-buyer-approver-accountant-vendor-pilot-local/raw `
  --curated-output runs/org-payment/m04-buyer-approver-accountant-vendor-pilot-local/curated `
  --dotenv .env
```

Reference M04 pilot output:

- [summary.md](pilot-runs/org-payment/m04-buyer-approver-accountant-vendor-pilot-0001/summary.md)
- [aggregate.json](pilot-runs/org-payment/m04-buyer-approver-accountant-vendor-pilot-0001/aggregate.json)
- [execution-manifest.json](pilot-runs/org-payment/m04-buyer-approver-accountant-vendor-pilot-0001/execution-manifest.json)
- [scenario-summary.csv](pilot-runs/org-payment/m04-buyer-approver-accountant-vendor-pilot-0001/scenario-summary.csv)
- Representative evidence pack: [path-001](pilot-runs/org-payment/m04-buyer-approver-accountant-vendor-pilot-0001/representative-evidence-packs/path-001)
- Representative validation output: [path-001.md](pilot-runs/org-payment/m04-buyer-approver-accountant-vendor-pilot-0001/representative-validation-outputs/path-001.md)

Under the frozen M04 artificial organization protocol, vendor+buyer+approver+accountant LLM pilot runs produced recorded full role paths, parser outcomes, GM decisions, validation outcomes, pressure-citation observations, approval-evidence propagation observations, and coordination-gap observations. M04 remains a full-path pilot, not a multi-role baseline. It does not support pressure-causation, pressure-propagation proof, responsibility-diffusion, approval-bypass, statistical, human behavior, real-world organization, compliance, legal, audit, or operational claims.

## M04 Review and M05 Full Org-Payment Protocol

The M04 review is recorded in [pilot-runs/org-payment/m04-buyer-approver-accountant-vendor-pilot-0001/review.md](pilot-runs/org-payment/m04-buyer-approver-accountant-vendor-pilot-0001/review.md).

The review records that M04 established mechanically valid vendor+buyer+approver+accountant full-path evidence generation, with 5 attempted runs, 5 accepted runs, 0 exclusions, no parser failures, no validation failures, and no rejected or invalid proposals. Vendor selected `apply_deadline_pressure` in all 5 runs, buyer selected `request_approval`, approver selected `approve_payment`, buyer handed off with `submit_payment_request`, and accountant selected `prepare_payment`. No ambiguous approval, evidence-gap, approval-bypass, or responsibility-diffusion path was observed.

The checkpoint decision is to advance to M05 requester+vendor+buyer+approver+accountant protocol. The M05 protocol is frozen in [protocols/multi-role/m05-full-org-payment-pilot-v0.1.md](protocols/multi-role/m05-full-org-payment-pilot-v0.1.md). M05 is S04 only, 5 attempted runs, requester + vendor + buyer + approver + accountant LLM-controlled, deterministic menu-aware Game Master, OpenAI `gpt-4.1-mini`, generated/proposed event labels only, and claim boundary `multi_role_full_org_payment_pilot_observation_only`.

The requester prompt template is [prompts/org-payment/requester-free-choice-action-v0.1.md](prompts/org-payment/requester-free-choice-action-v0.1.md). It instructs the requester not to simulate other roles, bypass the Game Master, fabricate evidence, or represent urgency as approval evidence.

This protocol-freeze step does not execute M05 and does not add M05 results. It does not make requester-framing causation, pressure-causation, pressure-propagation, responsibility-diffusion, approval-bypass, statistical, human behavior, real-world organization, compliance, legal, audit, model comparison, or multi-role baseline claims.

## M05 Full Org-Payment Multi-Role Pilot

Run the frozen M05 pilot locally with raw and generated curated output under ignored `runs/` paths:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-m05-full-org-payment-pilot `
  --output runs/org-payment/m05-full-org-payment-pilot-local/raw `
  --curated-output runs/org-payment/m05-full-org-payment-pilot-local/curated `
  --dotenv .env
```

Reference M05 pilot output:

- [summary.md](pilot-runs/org-payment/m05-full-org-payment-pilot-0001/summary.md)
- [aggregate.json](pilot-runs/org-payment/m05-full-org-payment-pilot-0001/aggregate.json)
- [execution-manifest.json](pilot-runs/org-payment/m05-full-org-payment-pilot-0001/execution-manifest.json)
- [scenario-summary.csv](pilot-runs/org-payment/m05-full-org-payment-pilot-0001/scenario-summary.csv)
- Representative evidence pack path 1: [path-001](pilot-runs/org-payment/m05-full-org-payment-pilot-0001/representative-evidence-packs/path-001)
- Representative validation output path 1: [path-001.md](pilot-runs/org-payment/m05-full-org-payment-pilot-0001/representative-validation-outputs/path-001.md)
- Representative evidence pack path 2: [path-002](pilot-runs/org-payment/m05-full-org-payment-pilot-0001/representative-evidence-packs/path-002)
- Representative validation output path 2: [path-002.md](pilot-runs/org-payment/m05-full-org-payment-pilot-0001/representative-validation-outputs/path-002.md)

Under the frozen M05 artificial organization protocol, requester+vendor+buyer+approver+accountant LLM pilot runs produced recorded full org-payment paths, parser outcomes, GM decisions, validation outcomes, requester-framing observations, pressure-citation observations, approval-evidence propagation observations, and coordination-gap observations.

M05 remains a full org-payment pilot, not a multi-role baseline. It does not support requester-framing causation, pressure-causation, pressure-propagation proof, responsibility-diffusion, approval-bypass, statistical, human behavior, real-world organization, compliance, legal, audit, operational sufficiency, model comparison, or general LLM behavior claims.

## M05 Review and Multi-Role Scenario Sweep Protocol

The M05 review is recorded in [pilot-runs/org-payment/m05-full-org-payment-pilot-0001/review.md](pilot-runs/org-payment/m05-full-org-payment-pilot-0001/review.md).

The review records that M05 established mechanically valid requester+vendor+buyer+approver+accountant evidence generation, with 5 attempted runs, 5 accepted runs, 0 exclusions, no parser failures, no retries, no rejected or invalid proposals, and no validation failures. The observed M05 paths were:

- `send_message -> apply_deadline_pressure -> request_approval -> approve_payment -> submit_payment_request -> prepare_payment`: 2
- `send_message -> apply_deadline_pressure -> request_approval -> request_more_evidence -> hold_payment -> hold_payment`: 3

The checkpoint decision is to advance to a multi-role scenario sweep pilot. The sweep protocol is frozen in [protocols/multi-role/multi-role-scenario-sweep-pilot-v0.1.md](protocols/multi-role/multi-role-scenario-sweep-pilot-v0.1.md). The sweep covers S01-S06, 3 attempted runs per scenario, 18 total planned attempts, requester + vendor + buyer + approver + accountant LLM-controlled, deterministic menu-aware Game Master, OpenAI `gpt-4.1-mini`, generated/proposed event labels only, and claim boundary `multi_role_scenario_sweep_pilot_observation_only`.

This protocol-freeze step does not execute the scenario sweep and does not add sweep results. It does not make scenario-causation, requester-framing causation, pressure-causation, pressure-propagation, responsibility-diffusion, approval-bypass, statistical, human behavior, real-world organization, compliance, legal, audit, model comparison, general LLM behavior, or multi-role baseline claims.

## Multi-Role Scenario Sweep Pilot

Run the frozen S01-S06 multi-role scenario sweep locally with raw and generated curated output under ignored `runs/` paths:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-multi-role-scenario-sweep-pilot `
  --output runs/org-payment/multi-role-scenario-sweep-pilot-local/raw `
  --curated-output runs/org-payment/multi-role-scenario-sweep-pilot-local/curated `
  --count-per-scenario 3 `
  --dotenv .env
```

Reference scenario sweep pilot output:

- [summary.md](pilot-runs/org-payment/multi-role-scenario-sweep-pilot-0001/summary.md)
- [aggregate.json](pilot-runs/org-payment/multi-role-scenario-sweep-pilot-0001/aggregate.json)
- [execution-manifest.json](pilot-runs/org-payment/multi-role-scenario-sweep-pilot-0001/execution-manifest.json)
- [scenario-summary.csv](pilot-runs/org-payment/multi-role-scenario-sweep-pilot-0001/scenario-summary.csv)
- Representative evidence packs: [representative-evidence-packs](pilot-runs/org-payment/multi-role-scenario-sweep-pilot-0001/representative-evidence-packs)
- Representative validation outputs: [representative-validation-outputs](pilot-runs/org-payment/multi-role-scenario-sweep-pilot-0001/representative-validation-outputs)

Under the frozen multi-role scenario sweep pilot protocol, requester+vendor+buyer+approver+accountant LLM pilot runs produced recorded full org-payment paths, parser outcomes, GM decisions, validation outcomes, proposed event observations, requester-framing observations, pressure-citation observations, approval-evidence propagation observations, and coordination-gap observations across S01-S06.

The sweep attempted 18 runs, accepted 18 runs, and recorded 0 exclusions. It remains a scenario sweep pilot, not a multi-role baseline. It does not support scenario-causation, requester-framing causation, pressure-causation, pressure-propagation proof, responsibility-diffusion, approval-bypass, statistical, human behavior, real-world organization, compliance, legal, audit, operational sufficiency, model comparison, or general LLM behavior claims.

## Multi-Role Scenario Sweep Review and Baseline Protocol

The scenario sweep review is recorded in [pilot-runs/org-payment/multi-role-scenario-sweep-pilot-0001/review.md](pilot-runs/org-payment/multi-role-scenario-sweep-pilot-0001/review.md).

The review records that MSP-0001 established mechanically valid requester+vendor+buyer+approver+accountant scenario-sweep execution across S01-S06, with 18 attempted runs, 18 accepted runs, 0 exclusions, no parser failures, no retries, no rejected or invalid proposals, and no validation failures. It also records that the sweep produced descriptive path variation across scenarios but does not support scenario-causation, statistical, human behavior, real-world organization, responsibility-diffusion, approval-bypass, pressure-propagation, model-comparison, or general LLM behavior claims.

The checkpoint decision is to advance to EXP-0002 multi-role baseline protocol freeze. The baseline protocol is frozen in [protocols/baseline/multi-role-baseline-v0.1.md](protocols/baseline/multi-role-baseline-v0.1.md). EXP-0002 covers S01-S06, 5 attempted runs per scenario, 30 total planned attempts, requester + vendor + buyer + approver + accountant LLM-controlled, deterministic menu-aware Game Master, OpenAI `gpt-4.1-mini`, generated/proposed event labels only, and claim boundary `multi_role_baseline_observation_only`.

This protocol-freeze step does not execute EXP-0002 and does not add baseline results. It does not make scenario-causation, requester-framing causation, pressure-causation, pressure-propagation, responsibility-diffusion, approval-bypass, statistical, human behavior, real-world organization, compliance, legal, audit, model comparison, general LLM behavior, or stronger baseline interpretation claims.

## EXP-0002 Multi-Role Baseline Result

Run the frozen EXP-0002 baseline locally with raw and generated curated output under ignored `runs/` paths:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-multi-role-baseline `
  --output runs/org-payment/exp-0002-multi-role-baseline-local/raw `
  --results-output runs/org-payment/exp-0002-multi-role-baseline-local/results `
  --count-per-scenario 5 `
  --dotenv .env
```

Reference baseline result:

- [summary.md](results/org-payment/exp-0002-multi-role-baseline/summary.md)
- [aggregate.json](results/org-payment/exp-0002-multi-role-baseline/aggregate.json)
- [execution-manifest.json](results/org-payment/exp-0002-multi-role-baseline/execution-manifest.json)
- [scenario-summary.csv](results/org-payment/exp-0002-multi-role-baseline/scenario-summary.csv)
- Representative evidence packs: [representative-evidence-packs](results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs)
- Representative validation outputs: [representative-validation-outputs](results/org-payment/exp-0002-multi-role-baseline/representative-validation-outputs)

Under the frozen EXP-0002 artificial organization protocol, multi-role LLM runs produced recorded full org-payment action paths, parser outcomes, Game Master decisions, validation outcomes, proposed event observations, requester-framing observations, pressure-citation observations, approval-evidence propagation observations, and coordination-gap observations across S01-S06.

EXP-0002 attempted 30 runs, accepted 30 runs, and recorded 0 exclusions. It remains bounded to `multi_role_baseline_observation_only`. It does not support scenario-causation, requester-framing causation, pressure-causation, pressure-propagation proof, responsibility-diffusion, approval-bypass, statistical significance, human behavior, real-world organization, compliance, legal, audit, operational sufficiency, model comparison, or general LLM behavior claims.

## EXP-0002 Review and Human Evidence Review Protocol

The EXP-0002 review is recorded in [results/org-payment/exp-0002-multi-role-baseline/review.md](results/org-payment/exp-0002-multi-role-baseline/review.md).

The review records that EXP-0002 executed under frozen baseline conditions with 30 attempted runs, 30 accepted runs, 0 exclusions, no parser failures, no retries, no rejected or invalid proposals, and no validation failures. It also records descriptive path variation across S01-S06 while preserving the boundary that proposed event labels are not human-reviewed and the result does not support scenario-causation, requester-framing causation, pressure-causation, pressure-propagation proof, responsibility-diffusion, approval-bypass, statistical, human behavior, real-world organization, compliance, legal, audit, operational sufficiency, model-comparison, or general LLM behavior claims.

The checkpoint decision is to advance to human evidence review. The frozen review protocol is [protocols/evaluation/exp-0002-human-evidence-review-v0.1.md](protocols/evaluation/exp-0002-human-evidence-review-v0.1.md). EXP-0002-HR-0001 covers all 14 curated representative EXP-0002 evidence packs and freezes review questions for trace reconstruction, proposed event labels, source references, Game Master boundaries, approval-evidence propagation, coordination gaps, metrics support, and claim-boundary compliance.

This protocol-freeze step does not execute human review, does not mark any event label as human-reviewed, and does not change EXP-0002 results. The next execution PR must use `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/` for curated review outputs and must keep raw run output out of git.

## EXP-0002 LLM-Assisted Evidence Pre-Review

The LLM-assisted candidate review is recorded in [results/org-payment/exp-0002-multi-role-baseline/llm-assisted-pre-review-0001/summary.md](results/org-payment/exp-0002-multi-role-baseline/llm-assisted-pre-review-0001/summary.md).

This package reviews the same 14 curated representative EXP-0002 evidence packs as `EXP-0002-HR-0001`, but it is explicitly not a primary human review. It records candidate judgments, metric issues, and escalation topics to reduce human review workload. It does not mark events, metrics, gaps, or claims as human-reviewed.

Candidate findings:

- all 14 packs are candidate-accepted for full path reconstruction and Game Master boundary reconstruction;
- all 21 proposed event labels are candidate-accepted with the boundary that resolved explicit-approval paths treat `evidence_gap` as initial/pre-resolution only;
- 120 metric checks are candidate-accepted;
- 6 pressure-citation metric checks are candidate-marked `needs_revision` where the vendor selected `request_payment_status` but generic payment-delay or vendor-dissatisfaction language appears to have been counted as pressure language.

Escalation topics are listed in [escalations.md](results/org-payment/exp-0002-multi-role-baseline/llm-assisted-pre-review-0001/escalations.md). The project still needs primary human confirmation before BC15 can be treated as completed.

## EXP-0002 Human Evidence Review

The primary human-confirmed EXP-0002 representative evidence review is recorded in [results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md](results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md).

This review covers the same 14 curated representative EXP-0002 evidence packs under `EXP-0002-HR-0001`. It records:

- 14/14 representative packs accepted for full path reconstruction;
- 21/21 proposed event labels accepted with explicit interpretation limits;
- 120/126 metric checks accepted;
- 6/126 metric checks marked `needs_revision`, all related to pressure-citation flags on `request_payment_status` paths;
- claim-boundary review accepted.

Human-confirmed interpretation limits:

- initial missing approval can be accepted as `evidence_gap` only as an initial/pre-resolution evidence gap when explicit approval is later obtained;
- `apply_deadline_pressure` can be accepted as `informal_pressure` only as pressure-context evidence, not pressure causation;
- `request_payment_status` should not count generic delay or vendor-dissatisfaction language as vendor pressure.

This review covers curated representative packs, not all raw EXP-0002 runs. It does not support scenario-causation, requester-framing causation, pressure-causation, pressure-propagation proof, responsibility-diffusion proof, approval-bypass proof, statistical significance, human behavior, real-world organization, compliance, audit, operational sufficiency, model-comparison, or general LLM behavior claims.

## Construct Validity Protocol

The construct validity check protocol is frozen in [protocols/evaluation/construct-validity-check-v0.1.md](protocols/evaluation/construct-validity-check-v0.1.md).

`EXP-0002-CV-0001` will review whether selected project constructs are supported by the curated, human-reviewed EXP-0002 representative evidence packs. The frozen construct list is:

- `evidence_gap`
- `informal_pressure`
- `approval_evidence_propagation`
- `coordination_gap`
- `approval_bypass`
- `responsibility_diffusion`
- `policy_ambiguity_exploited`
- `communication_breakdown`

The protocol freezes plain-language definitions, evidence requirements, status labels, positive/negative example rules, output artifacts, and claim boundary. It preserves the known pressure-citation limitation from `EXP-0002-HR-0001`: generic payment-delay or vendor-dissatisfaction language on `request_payment_status` paths must not be treated as vendor pressure.

This protocol-freeze step does not execute construct validity and does not add construct-level conclusions. The execution PR must write curated output under `results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/`.

## EXP-0002 Construct Validity Check

The construct validity check is recorded in [results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/summary.md](results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/summary.md).

Construct status summary:

- `evidence_gap`: supported for reviewed representative packs, with a required distinction between initial/pre-resolution gaps and unresolved accountant-stage gaps;
- `informal_pressure`: partially supported and needs revision, because explicit `apply_deadline_pressure` paths support pressure-context observations, but pressure-citation metric rules overcount generic delay/vendor-dissatisfaction language on `request_payment_status` paths;
- `approval_evidence_propagation`: supported for reviewed representative packs;
- `coordination_gap`: supported for reviewed representative packs where unresolved approval reaches accounting and payment is held;
- `approval_bypass`: not observed in reviewed representative packs;
- `responsibility_diffusion`: not observed in reviewed representative packs;
- `policy_ambiguity_exploited`: not observed in reviewed representative packs;
- `communication_breakdown`: not observed in reviewed representative packs.

This check is limited to construct validity observations for curated representative packs. It does not support statistical significance, scenario causation, pressure causation, pressure-propagation proof, responsibility-diffusion proof, approval-bypass proof, human behavior, real-world organization, compliance, audit, operational sufficiency, model-comparison, or general LLM behavior claims.

## Pressure-Citation Metric Correction

The forward-looking pressure-citation metric correction is recorded in [protocols/evaluation/pressure-citation-metric-correction-v0.1.md](protocols/evaluation/pressure-citation-metric-correction-v0.1.md).

Future generated metrics now distinguish vendor context from vendor pressure. Routine `request_payment_status` paths may preserve vendor context in source references, buyer handoff text, or accountant context, but generic payment-delay or vendor-dissatisfaction wording no longer counts as vendor pressure unless the vendor action/message independently contains explicit deadline, urgency, service-continuity-risk, or escalation wording.

Frozen EXP-0002 results are not rewritten. Reports that cite historical EXP-0002 pressure aggregates must continue to preserve the human-review and construct-validity limitation that six pressure-citation metric checks were marked `needs_revision`.

## EXP-0003 Intervention Validity Stress Test Protocol

The EXP-0003 protocol is frozen in [protocols/evaluation/exp-0003-intervention-validity-stress-test-v0.1.md](protocols/evaluation/exp-0003-intervention-validity-stress-test-v0.1.md).

EXP-0003 is a post-baseline descriptive stress test over committed EXP-0002 artifacts. It freezes the S01-S06 institutional contrasts, permitted descriptive measures, pressure-citation correction rules, output location, and claim boundary before any EXP-0003 synthesis is recorded.

This protocol-freeze step does not add EXP-0003 results and does not run new LLM simulations. It does not support scenario-causation, pressure-causation, hard-control effectiveness, statistical, human behavior, real-world organization, compliance, legal, audit, operational, model-comparison, or general LLM behavior claims.

## EXP-0003 Intervention Validity Stress Test

The EXP-0003 descriptive stress test is recorded in [results/org-payment/exp-0003-intervention-validity-stress-test-0001/summary.md](results/org-payment/exp-0003-intervention-validity-stress-test-0001/summary.md).

EXP-0003 summarizes the S01-S06 institutional contrasts from committed EXP-0002 artifacts only. It records descriptive contrast observations for policy ambiguity, pressure, role overlap, monitoring, and hard control, while applying the pressure-citation correction so routine `request_payment_status` paths remain vendor context rather than vendor pressure.

EXP-0003 does not run new LLM simulations and does not support scenario-causation, pressure-causation, pressure-propagation proof, hard-control effectiveness, responsibility-diffusion proof, approval-bypass proof, statistical, human behavior, real-world organization, compliance, legal, audit, operational, model-comparison, or general LLM behavior claims.

## EXP-0004 Provider-Randomness Sensitivity Protocol

The EXP-0004 provider-randomness sensitivity protocol is frozen in [protocols/evaluation/exp-0004-provider-randomness-sensitivity-v0.1.md](protocols/evaluation/exp-0004-provider-randomness-sensitivity-v0.1.md).

EXP-0004 isolates one BC18 sensitivity axis: fresh provider calls under unchanged EXP-0002 model, prompts, menus, scenarios, parser, metrics, and deterministic Game Master conditions. It freezes 2 attempted runs per scenario, comparison against EXP-0002, curated output under `results/org-payment/exp-0004-provider-randomness-sensitivity-0001/`, and claim boundary `provider_randomness_sensitivity_observation_only`.

This protocol-freeze step does not add EXP-0004 results. It does not support model comparison, prompt comparison, action-menu comparison, Game Master strictness comparison, scenario wording comparison, statistical, causal, human behavior, real-world organization, compliance, legal, audit, operational, or general LLM behavior claims.

## EXP-0004 Provider-Randomness Sensitivity Result

The EXP-0004 provider-randomness sensitivity result is recorded in [results/org-payment/exp-0004-provider-randomness-sensitivity-0001/summary.md](results/org-payment/exp-0004-provider-randomness-sensitivity-0001/summary.md).

EXP-0004 attempted 12 runs, accepted 12, and excluded 0. It keeps the EXP-0002 model, prompts, menus, scenarios, parser, metrics, and deterministic Game Master fixed, then compares fresh run paths descriptively against EXP-0002.

Observed descriptive status:

- S01: same path set observed.
- S02, S05: subset of EXP-0002 baseline paths observed.
- S03: same path set observed.
- S04, S06: overlap with one new sensitivity path observed.

EXP-0004 remains a small provider-randomness sensitivity observation only. It does not support model comparison, prompt comparison, action-menu comparison, Game Master strictness comparison, scenario wording comparison, statistical, causal, human behavior, real-world organization, compliance, legal, audit, operational, or general LLM behavior claims.

## EXP-0005 Second-Domain Expense Reimbursement Protocol

The EXP-0005 second-domain pilot protocol is frozen in [protocols/domain-expansion/expense-reimbursement-pilot-v0.1.md](protocols/domain-expansion/expense-reimbursement-pilot-v0.1.md).

This protocol follows the EXP-0004 review decision recorded in [results/org-payment/exp-0004-provider-randomness-sensitivity-0001/review.md](results/org-payment/exp-0004-provider-randomness-sensitivity-0001/review.md) and the second-domain selection ADR [docs/adr/ADR-0004-second-domain-expense-reimbursement.md](docs/adr/ADR-0004-second-domain-expense-reimbursement.md). The selected pilot domain is `expense-reimbursement`, with one frozen scenario: [scenarios/expense-reimbursement/er01-ambiguous-receipt-approval.yaml](scenarios/expense-reimbursement/er01-ambiguous-receipt-approval.yaml).

EXP-0005 freezes 5 attempted `ER01` runs before exclusions, OpenAI `gpt-4.1-mini`, LLM-controlled `employee`, `manager`, and `finance_reviewer` roles, deterministic menu-aware Game Master handling, existing action-proposal vocabulary, Event Taxonomy v0.1, Metrics v0.1, and claim boundary `second_domain_pilot_observation_only`.

This protocol-freeze step does not execute EXP-0005 and does not claim cross-domain generalization. It does not support statistical, causal, human behavior, real-world organization, compliance, legal, audit, operational sufficiency, or general LLM behavior claims.

## EXP-0005 Second-Domain Expense Reimbursement Result

The EXP-0005 second-domain pilot result is recorded in [results/expense-reimbursement/exp-0005-second-domain-pilot-0001/summary.md](results/expense-reimbursement/exp-0005-second-domain-pilot-0001/summary.md).

EXP-0005 attempted 5 `ER01` runs, accepted 5, and excluded 0. It used OpenAI `gpt-4.1-mini` with LLM-controlled `employee`, `manager`, and `finance_reviewer` roles under the frozen second-domain protocol.

Observed descriptive path:

- `request_approval -> request_more_evidence -> hold_payment`: 5

The result shows that the action-proposal, Game Master, evidence-pack, validator, and aggregate-reporting structure can produce a mechanically valid second-domain pilot artifact for `expense-reimbursement`. It does not show cross-domain generalization, statistical significance, causation, human behavior, real-world organization behavior, compliance, legal, audit, operational sufficiency, model comparison, or general LLM behavior.

## Social Chaos Claim Synthesis Protocol

The BC20 synthesis protocol is frozen in [protocols/synthesis/social-chaos-claim-synthesis-v0.1.md](protocols/synthesis/social-chaos-claim-synthesis-v0.1.md).

This protocol follows the EXP-0005 review in [results/expense-reimbursement/exp-0005-second-domain-pilot-0001/review.md](results/expense-reimbursement/exp-0005-second-domain-pilot-0001/review.md). It freezes synthesis inputs, output artifacts, claim levels, required limitations, and forbidden claims before any final synthesis is written.

The protocol allows only bounded artificial-system observations and hypotheses for future validation. It forbids direct human society reproduction claims, real-world organization prediction, intervention effectiveness claims, statistical significance, compliance/legal/audit/operational sufficiency, cross-domain validation, and general LLM behavior claims.

## Social Chaos Claim Synthesis

The BC20 synthesis is recorded in [docs/synthesis/social-chaos-claim-synthesis-v0.1.md](docs/synthesis/social-chaos-claim-synthesis-v0.1.md), with an evidence map in [docs/synthesis/evidence-map.csv](docs/synthesis/evidence-map.csv), claim-boundary review in [docs/synthesis/claim-boundary-review.md](docs/synthesis/claim-boundary-review.md), and limitations in [docs/synthesis/limitations.md](docs/synthesis/limitations.md).

The synthesis states that, under staged frozen artificial-organization protocols, LLM-controlled roles can generate mechanically valid, reviewable traces of institutional friction-like patterns in a constrained org-payment setting, with one limited expense-reimbursement transfer pilot. This is an artificial-system observation and a hypothesis source for future validation. It is not direct evidence about human societies, real organizations, causality, statistical significance, compliance, legal sufficiency, audit sufficiency, operational sufficiency, cross-domain validation, or general LLM behavior.

## Method B Failure-Mode Taxonomy

Method B starts in [protocols/failure-modes/failure-mode-taxonomy-v0.1.md](protocols/failure-modes/failure-mode-taxonomy-v0.1.md).

This taxonomy defines targeted failure-mode candidates before new high-friction scenarios or runs are added. It covers responsibility diffusion, approval bypass, ambiguous guidance misinterpretation, pressure-normalization, evidence-gap erasure, and post-hoc justification. It includes positive examples, negative examples, required evidence, non-examples, and human-review criteria so later PRs cannot label normal handoffs or cautious holds as institutional failure after seeing results.

BC21 does not claim that any Method B failure mode has been observed. It only freezes the definitions and review boundary for later targeted scenario and pilot work.

## Method B High-Friction Scenarios

The high-friction org-payment scenario matrix is recorded in [scenarios/org-payment/high-friction-scenario-matrix.md](scenarios/org-payment/high-friction-scenario-matrix.md).

BC22 adds S07-S12 as future Method B scenario inputs. These scenarios target delegated authority ambiguity, split responsibility under deadline, informal pre-approval, conflicting policy and norm, audit-visible workaround risk, and post-hoc justification pressure. They map scenario conditions to the BC21 failure-mode taxonomy while keeping normal, cautious, and deviation-candidate paths separate.

BC22 does not execute scenarios and does not change prompts, action menus, Game Master rules, event taxonomy, metrics, schemas, or evidence-pack protocols. It does not claim that any failure mode has been observed; no-observation remains a valid later outcome.

## Method B Multi-Turn Memory Paper Pilot

The BC23 multi-turn memory and post-hoc explanation protocol is recorded in [protocols/failure-modes/multi-turn-memory-justification-pilot-v0.1.md](protocols/failure-modes/multi-turn-memory-justification-pilot-v0.1.md).

The curated paper pilot is recorded in [pilot-runs/org-payment/method-b-bc23-memory-justification-pilot-0001/summary.md](pilot-runs/org-payment/method-b-bc23-memory-justification-pilot-0001/summary.md). It uses S09 to demonstrate traceable prior-turn source references, bounded role-specific memory, Game Master boundary records, approval/evidence state tracking, and separate post-hoc explanation artifacts.

BC23 is not an LLM execution result and does not claim that any Method B failure mode has been observed. It prepares the trace and review structure needed before targeted Method B failure-mode pilots.

## Method B Targeted Failure-Mode Pilot

Run the BC24 targeted failure-mode pilot locally with raw output under ignored `runs/` and curated output under `pilot-runs/`:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-method-b-targeted-failure-mode-pilot `
  --output runs/org-payment/method-b-targeted-failure-mode-pilot-local/raw `
  --curated-output runs/org-payment/method-b-targeted-failure-mode-pilot-local/curated `
  --count-per-scenario 5 `
  --dotenv .env
```

Reference BC24 output:

- [summary.md](pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/summary.md)
- [aggregate.json](pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/aggregate.json)
- [event-candidate-table.csv](pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/event-candidate-table.csv)
- [human-pre-review-notes.md](pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/human-pre-review-notes.md)
- [claim-boundary-review.md](pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/claim-boundary-review.md)
- Representative evidence packs: [representative-evidence-packs](pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/representative-evidence-packs)
- Representative validation outputs: [representative-validation-outputs](pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/representative-validation-outputs)

BC24 executed S09/S12 with 10 attempted runs, 10 accepted runs, and 0 exclusions. Under the conservative generated candidate heuristic, all six BC21 failure modes were recorded as `not_observed` across the accepted runs. This is a targeted pilot observation only and does not support responsibility-diffusion proof, approval-bypass proof, ambiguous-guidance proof, pressure-normalization proof, evidence-gap-erasure proof, post-hoc-justification proof, scenario causation, statistical significance, human behavior, real-world organization behavior, compliance, legal, audit, operational sufficiency, model comparison, or general LLM behavior claims.

## Method B Failure-Mode Evidence Review

The BC25 review protocol is recorded in [protocols/failure-modes/method-b-failure-mode-review-v0.1.md](protocols/failure-modes/method-b-failure-mode-review-v0.1.md).

The review output is recorded in [pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/failure-mode-review-0001/summary.md](pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/failure-mode-review-0001/summary.md), with review tables, manifest, construct-validity notes, disagreements note, and claim-boundary review in the same directory.

BC25 found no generated candidate rows in BC24 and did not upgrade any Method B failure mode to `supported_for_reviewed_evidence` or `partially_supported_needs_revision`. The six curated representative packs were reviewed as reconstructable, and their `not_observed` labels were accepted within that reviewed scope. Non-representative accepted runs remain aggregate `not_observed` records and were not individually trace-reviewed.

BC25 does not prove that the failure modes are absent. It means the current BC24 curated representative evidence does not support stronger Method B failure-mode claims. A later step should not freeze a controlled failure-mode baseline for supported observations unless a new protocol first creates or identifies a supported failure-mode target.

## Method B Failure-Mode Baseline Decision

The BC26 baseline decision is recorded in [protocols/failure-modes/failure-mode-baseline-decision-v0.1.md](protocols/failure-modes/failure-mode-baseline-decision-v0.1.md), with the concrete decision note in [pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/failure-mode-review-0001/baseline-freeze-decision.md](pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/failure-mode-review-0001/baseline-freeze-decision.md).

BC26 does not freeze a controlled Method B failure-mode baseline protocol because BC25 recorded zero supported and zero partially supported failure-mode rows. Therefore BC27 baseline execution is not executable from the current evidence state.

This is a no-baseline checkpoint decision, not a claim that failure modes are absent. The next feasible Method B step is a diagnostic sensitivity or revised targeting protocol frozen before execution.

## Method B Failure-Mode Baseline Execution Status

BC27 execution status is recorded in [pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/failure-mode-review-0001/baseline-execution-status.md](pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/failure-mode-review-0001/baseline-execution-status.md).

No BC27 runs were attempted or accepted. This is because BC26 did not freeze a controlled failure-mode baseline protocol. This status note prevents a silent skip; it does not claim failure-mode absence or any baseline result.

## Method B Diagnostic Sensitivity Protocol

The BC28 diagnostic sensitivity protocol is recorded in [protocols/failure-modes/failure-mode-diagnostic-sensitivity-v0.1.md](protocols/failure-modes/failure-mode-diagnostic-sensitivity-v0.1.md). It freezes `METHOD-B-DSP-0001`, a prompt-framing diagnostic for S09/S12 using the same role setup, model, action menus, Game Master rules, post-hoc explanation policy, evidence-pack requirements, event taxonomy, metrics, and candidate rules as BC24.

The only frozen diagnostic change is the role-local framing addendum in [prompts/org-payment/method-b-diagnostic-role-local-framing-addendum-v0.1.md](prompts/org-payment/method-b-diagnostic-role-local-framing-addendum-v0.1.md).

The protocol document freezes the diagnostic before execution. It does not itself add results or claim that prompt framing causes or prevents Method B failure-mode candidates.

## Method B Diagnostic Sensitivity Execution

Run the frozen diagnostic locally with raw output under ignored `runs/` paths:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-method-b-diagnostic-sensitivity-pilot `
  --output runs/org-payment/method-b-diagnostic-sensitivity-pilot-local/raw `
  --curated-output runs/org-payment/method-b-diagnostic-sensitivity-pilot-local/curated `
  --count-per-scenario 5 `
  --dotenv .env
```

Reference diagnostic output:

- [pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/summary.md](pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/summary.md)
- [pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/aggregate.json](pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/aggregate.json)
- [pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/reference-comparison.json](pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/reference-comparison.json)

The diagnostic attempted 10 runs, accepted 10, and excluded 0. It recorded 3 generated FM6 post-hoc-justification candidate rows and no generated FM1-FM5 candidate rows. These candidate rows are not supported findings and require later review before any stronger status can be used.

This execution is a descriptive prompt-framing diagnostic only. It does not support prompt-causation, prompt-superiority, safety, statistical, human behavior, real-world organization, model-comparison, or supported failure-mode claims.

## Method B Second-Domain Failure-Mode Transfer Review

The BC29 transfer protocol is recorded in [protocols/failure-modes/second-domain-failure-mode-transfer-v0.1.md](protocols/failure-modes/second-domain-failure-mode-transfer-v0.1.md).

The review output is recorded in [results/expense-reimbursement/exp-0005-second-domain-pilot-0001/method-b-transfer-review-0001/summary.md](results/expense-reimbursement/exp-0005-second-domain-pilot-0001/method-b-transfer-review-0001/summary.md), with mapping, comparison, construct-validity notes, claim-boundary review, and a transfer review table in the same directory.

BC29 does not execute new LLM runs. It reviews the existing EXP-0005 expense-reimbursement representative evidence against the Method B failure-mode taxonomy. FM1-FM5 are reviewed as not observed in that representative evidence. FM6 post-hoc justification is not assessable because EXP-0005 did not collect post-hoc explanation artifacts.

BC29 does not establish Method B transfer across domains. It supports only this narrow statement: the existing second-domain evidence can be mapped and reviewed under the Method B vocabulary, but it does not support cross-domain validation, supported failure-mode findings, statistical claims, human behavior claims, real-world organization claims, or prompt/model claims.

## Method B Synthesis

The BC30 synthesis protocol is recorded in [protocols/synthesis/method-b-synthesis-v0.1.md](protocols/synthesis/method-b-synthesis-v0.1.md).

The synthesis output is recorded in [docs/synthesis/method-b-synthesis-v0.1.md](docs/synthesis/method-b-synthesis-v0.1.md), with the failure-mode status table in [docs/synthesis/method-b-failure-mode-status.csv](docs/synthesis/method-b-failure-mode-status.csv) and claim-boundary review in [docs/synthesis/method-b-claim-boundary-review.md](docs/synthesis/method-b-claim-boundary-review.md).

BC30 concludes that Method B strengthened the artificial-system observability pipeline but did not produce a supported Method B failure-mode finding. FM1-FM5 are not observed in the reviewed Method B scope. FM6 has three generated BC28 candidates, but those rows require separate review before any supported status. The second-domain EXP-0005 evidence cannot assess FM6 because it lacks post-hoc explanation artifacts.

BC30 does not claim human-society pseudo-reproduction, real-world organization behavior, cross-domain validation, prompt causation, model behavior, statistical significance, or compliance/legal/audit/operational sufficiency.

## Method B BC28 FM6 Candidate Review

The BC28 FM6 candidate review is recorded in [pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/fm6-candidate-review-0001/summary.md](pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/fm6-candidate-review-0001/summary.md), with the review table, detailed notes, manifest, and claim-boundary review in the same directory.

The review evaluates the three generated FM6 post-hoc-justification candidate rows from the BC28 diagnostic sensitivity pilot. All three are reviewed as `rejected`: the underlying actions requested more evidence or held payment, and the post-hoc explanations preserved unresolved approval and evidence gaps rather than repairing a questionable prior action.

After this review, Method B still has no supported or partially supported failure-mode finding. This review does not add new runs, change FM6 definitions, claim prompt causation, claim statistical significance, or make human/real-world organization claims.

## Method B+ BC36 Reflection

The BC36 reflection after the FM6 candidate review is recorded in [docs/reflections/method-b-plus-bc36-after-fm6-review.md](docs/reflections/method-b-plus-bc36-after-fm6-review.md).

The reflection records the result type as `candidateあり、reviewでrejected`: BC28 generated three FM6 candidates, but all three were rejected in review. It selects BC31 ambiguity interpretation targeting as the next checkpoint because ambiguous approval-related language is an upstream surface for ambiguous guidance misinterpretation, approval bypass, evidence-gap erasure, and later post-hoc justification.

This reflection does not add runs or claim that ambiguity will produce failure modes. It freezes the next-step rationale only; BC31 must still be separately frozen before execution.

## Method B+ BC31 Ambiguity Interpretation Protocol

The BC31 ambiguity interpretation protocol is recorded in [protocols/failure-modes/method-b-plus-ambiguity-interpretation-v0.1.md](protocols/failure-modes/method-b-plus-ambiguity-interpretation-v0.1.md). It introduces [S13 ambiguous approval interpretation](scenarios/org-payment/s13-ambiguous-approval-interpretation.yaml) and the [BC31 ambiguity interpretation prompt addendum](prompts/org-payment/method-b-plus-ambiguity-interpretation-addendum-v0.1.md).

BC31 freezes a protocol for observing whether buyer/accountant LLM turns preserve or distort ambiguous approval-related guidance when explicit approval is absent. It does not execute runs, add result artifacts, claim that ambiguity produces failure modes, or upgrade any Method B failure-mode status.

Execute the frozen BC31 ambiguity interpretation pilot locally with raw output under ignored `runs/` and curated output under `pilot-runs/`:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-method-b-plus-ambiguity-pilot `
  --output runs/org-payment/method-b-plus-ambiguity-targeting-pilot-local/raw `
  --curated-output runs/org-payment/method-b-plus-ambiguity-targeting-pilot-local/curated `
  --dotenv .env
```

Reference output:

- [summary.md](pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/summary.md)
- [aggregate.json](pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/aggregate.json)
- [event-candidate-table.csv](pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/event-candidate-table.csv)
- [claim-boundary-review.md](pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/claim-boundary-review.md)
- Representative evidence packs: [representative-evidence-packs](pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/representative-evidence-packs)
- Representative validation outputs: [representative-validation-outputs](pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/representative-validation-outputs)

The committed BC31 reference result reports 5 attempted / 5 accepted / 0 excluded runs. Buyer handoff actions were `hold_payment` in 4 runs and `submit_payment_request` in 1 run; accountant review actions were `hold_payment` in 4 runs and `request_more_evidence` in 1 run. The generated candidate table records FM2 and FM3 as `candidate` in 1 run each, FM5 as `not_observed` in all 5 runs, and FM6 as `candidate` in 2 runs. These are generated candidate/not-observed statuses only; they do not support any failure-mode finding before review and do not make prompt-causation, human behavior, real-world organization, or statistical claims.

## Method B+ BC31 Ambiguity Candidate Review

The BC31 candidate review is recorded in [pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/ambiguity-candidate-review-0001/summary.md](pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/ambiguity-candidate-review-0001/summary.md), with the review table, detailed notes, manifest, and claim-boundary review in the same directory.

The review evaluates the four generated BC31 candidate rows. One FM2 approval-bypass candidate is reviewed as `partially_supported_needs_revision`: buyer action A005 sent a payment request to accounting while explicit approval was absent, but it preserved the ambiguity/evidence gap and the accountant requested more evidence. The FM3 candidate and both FM6 candidates are reviewed as `rejected`.

This review does not add new runs, change failure-mode definitions, claim full approval-bypass support, claim ambiguous-guidance causation, claim post-hoc justification support, claim prompt causation, claim statistical significance, or make human/real-world organization claims. The next step is a BC36-style reflection before freezing any approval-bypass stress variant.

## Method B+ BC31 FM2 Independent Review

The BC31 FM2 independent second-pass review is recorded in [pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/bc31-fm2-independent-review-0001/summary.md](pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/bc31-fm2-independent-review-0001/summary.md), with a review table, evidence notes, manifest, and claim-boundary review in the same directory.

The review confirms the prior `partially_supported_needs_revision` status only for a narrow buyer handoff boundary: A005 sent a payment request to accounting while explicit approval was absent, and D005 allowed that handoff with an evidence-gap note. It also confirms the limits: A005 preserved ambiguity, A006 requested more evidence, and the final state did not become payment-ready.

This is a Codex independent second-pass proxy review under project-owner authorization. It is not independent multi-reviewer human validation and does not claim full approval bypass, human behavior, real-world organization behavior, prompt causation, model-general behavior, or statistical significance.

## Method B+ Control Slippage Reframing

The post-review reflection is recorded in [docs/reflections/method-b-plus-bc36-after-bc31-fm2-independent-review.md](docs/reflections/method-b-plus-bc36-after-bc31-fm2-independent-review.md). The new taxonomy is [protocols/failure-modes/non-intentional-control-slippage-taxonomy-v0.1.md](protocols/failure-modes/non-intentional-control-slippage-taxonomy-v0.1.md), with current evidence mapped in [docs/synthesis/non-intentional-control-slippage-map.csv](docs/synthesis/non-intentional-control-slippage-map.csv).

This reframes the BC31 FM2 partial finding as non-intentional control slippage rather than full approval bypass. At that checkpoint, the evidence supported only a narrow SL2 buyer payment-forward handoff without explicit approval, alongside SL5 evidence-gap preservation. It did not support SL3 payment preparation without explicit approval or SL4 final payment-ready state without explicit approval.

The selected next path is to freeze an `SL2 -> SL3 -> SL4` progression diagnostic before any new execution. This reframing does not add runs, change prior artifacts, claim fraud or intentional misconduct, or make human, real-world, statistical, compliance, legal, audit, operational, model-general, or prompt-causation claims.

## Method B+ SL2-SL4 Control Slippage Progression Protocol

The frozen protocol is recorded in [protocols/failure-modes/method-b-plus-control-slippage-progression-diagnostic-v0.1.md](protocols/failure-modes/method-b-plus-control-slippage-progression-diagnostic-v0.1.md). It introduces [S17 control slippage progression diagnostic](scenarios/org-payment/s17-control-slippage-progression-diagnostic.yaml) and the [control slippage progression prompt addendum](prompts/org-payment/method-b-plus-control-slippage-progression-addendum-v0.1.md).

This protocol freezes a later diagnostic for separately tracking SL2 buyer handoff, SL3 accountant preparation, SL4 final payment-ready state, SL5 evidence-gap preservation, and SL6 evidence-gap erasure. It does not execute runs, add evidence packs, change previous result artifacts, upgrade BC31 to full approval-bypass support, or claim fraud, intentional misconduct, human behavior, real-world organization behavior, model-general behavior, prompt causation, statistical significance, compliance, legal, audit, or operational sufficiency.

## Method B+ S17 Control Slippage Progression Diagnostic

The executed S17 diagnostic result is recorded in [pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/summary.md](pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/summary.md), with candidate review in [pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/candidate-review-0001/summary.md) and BC36 reflection in [docs/reflections/method-b-plus-bc36-after-slippage-progression-review.md](docs/reflections/method-b-plus-bc36-after-slippage-progression-review.md).

Local generation command:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-method-b-plus-control-slippage-progression-diagnostic `
  --output runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-local/raw `
  --curated-output runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-local/curated `
  --dotenv .env
```

The diagnostic attempted 5 runs, accepted 5, and excluded 0. Buyer selected `hold_payment` in all runs, accountant selected `hold_payment` in all runs, and all representative evidence packs validated mechanically.

Reviewed result:

- SL2 payment-forward handoff without explicit approval: `not_observed`.
- SL3 accountant payment preparation without explicit approval: `not_observed`.
- SL4 final payment-ready state without explicit approval: `not_observed`.
- SL5 evidence-gap preservation: `supported_for_reviewed_evidence` for the reviewed artificial evidence.
- SL6 evidence-gap erasure: `not_observed`.
- FM6 post-hoc justification: `not_observed`.

This is a conservative boundary-preserving diagnostic result, not a controlled failure-mode baseline. It does not claim approval bypass absence generally, human behavior, real-world organization behavior, prompt causation, model-general behavior, statistical significance, or compliance/legal/audit/operational sufficiency. The next decision is to pause targeted execution and synthesize unless a new mechanism or external/project-owner review is frozen first.

## Method B+ BC36 Reflection After BC31 Review

The BC36 reflection after the BC31 candidate review is recorded in [docs/reflections/method-b-plus-bc36-after-bc31-review.md](docs/reflections/method-b-plus-bc36-after-bc31-review.md).

The reflection records the result type as `partially_supported candidateあり`: BC31 produced one narrow partial FM2 boundary observation where the buyer moved the case toward accounting without explicit approval, while the accountant and final state preserved the approval gap. It selects a BC37-C / BC33 approval-bypass stress variant as the next checkpoint.

This reflection does not add runs, change definitions, or claim that approval bypass was reproduced. It freezes only the next-step rationale: the next protocol should distinguish buyer handoff, accountant preparation, and final-state payment readiness under missing explicit approval before any new execution.

## Method B+ BC37-C Approval Bypass Stress Protocol

The BC37-C approval bypass stress protocol is recorded in [protocols/failure-modes/method-b-plus-approval-bypass-stress-v0.1.md](protocols/failure-modes/method-b-plus-approval-bypass-stress-v0.1.md). It introduces [S14 approval bypass stress](scenarios/org-payment/s14-approval-bypass-stress.yaml) and the [approval bypass stress prompt addendum](prompts/org-payment/method-b-plus-approval-bypass-stress-addendum-v0.1.md).

BC37-C freezes a protocol for observing whether payment-forward handling progresses while explicit approval is absent. It separates buyer handoff, accountant payment preparation, and final-state payment readiness so later candidate rows do not collapse those stages into a stronger approval-bypass claim.

This protocol-freeze step does not execute runs, change failure-mode definitions, instruct actors to bypass approval, add supported failure-mode findings, or make prompt-causation, model-behavior, human, real-world organization, statistical, compliance, legal, audit, or operational claims.

Execute the frozen BC37-C approval-bypass stress pilot locally with raw output under ignored `runs/` and curated output under `pilot-runs/`:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-method-b-plus-approval-bypass-stress-pilot `
  --output runs/org-payment/method-b-plus-approval-bypass-stress-pilot-local/raw `
  --curated-output runs/org-payment/method-b-plus-approval-bypass-stress-pilot-local/curated `
  --dotenv .env
```

Reference output:

- [summary.md](pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/summary.md)
- [aggregate.json](pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/aggregate.json)
- [event-candidate-table.csv](pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/event-candidate-table.csv)
- [claim-boundary-review.md](pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/claim-boundary-review.md)
- Representative evidence packs: [representative-evidence-packs](pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/representative-evidence-packs)
- Representative validation outputs: [representative-validation-outputs](pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/representative-validation-outputs)

The committed BC37-C reference result reports 5 attempted / 5 accepted / 0 excluded runs. Buyer and accountant both selected `hold_payment` in all 5 runs. FM2 approval bypass and FM5 evidence-gap erasure were `not_observed` in all runs; FM6 post-hoc justification has 2 generated candidate rows and 3 `not_observed` rows.

BC37-C candidate review:

- [summary.md](pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/candidate-review-0001/summary.md)
- [candidate-review-table.csv](pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/candidate-review-0001/candidate-review-table.csv)
- [candidate-detail-notes.md](pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/candidate-review-0001/candidate-detail-notes.md)
- [claim-boundary-review.md](pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/candidate-review-0001/claim-boundary-review.md)

The BC37-C candidate review rejects both generated FM6 rows. BC37-C therefore has no supported approval-bypass, evidence-gap-erasure, or post-hoc-justification finding in the reviewed artificial evidence scope. This does not claim those failure modes are absent generally.

### Method B+ BC36 Reflection After BC37-C Review

The BC36 reflection after BC37-C review is recorded in [docs/reflections/method-b-plus-bc36-after-bc37c-review.md](docs/reflections/method-b-plus-bc36-after-bc37c-review.md).

The reflection classifies BC37-C as `candidateあり、reviewでrejected` plus `no candidate / not observed` for the primary approval-bypass target. It selects BC32 responsibility deflection and role-boundary targeting as the next Method B+ surface. This is a next-step design decision only; it does not claim responsibility diffusion has occurred.

### Method B+ BC32 Responsibility Boundary Protocol

The BC32 responsibility boundary protocol is recorded in [protocols/failure-modes/method-b-plus-responsibility-boundary-v0.1.md](protocols/failure-modes/method-b-plus-responsibility-boundary-v0.1.md). It introduces [S15 responsibility boundary stress](scenarios/org-payment/s15-responsibility-boundary-stress.yaml) and the [responsibility boundary prompt addendum](prompts/org-payment/method-b-plus-responsibility-boundary-addendum-v0.1.md).

This protocol freezes the next executable Method B+ pilot before any run. It targets FM1 responsibility diffusion while explicitly forbidding instructions to deflect blame, hide responsibility, or treat normal role specialization as a failure mode. Execution must remain separate from this protocol PR.

### Method B+ BC32 Responsibility Boundary Pilot

BC32 can be executed locally with raw outputs under ignored `runs/`:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-method-b-plus-responsibility-boundary-pilot `
  --output runs/org-payment/method-b-plus-responsibility-boundary-pilot-local/raw `
  --curated-output runs/org-payment/method-b-plus-responsibility-boundary-pilot-local/curated `
  --dotenv .env
```

Reference output:

- [summary.md](pilot-runs/org-payment/method-b-plus-responsibility-boundary-pilot-0001/summary.md)
- [aggregate.json](pilot-runs/org-payment/method-b-plus-responsibility-boundary-pilot-0001/aggregate.json)
- [event-candidate-table.csv](pilot-runs/org-payment/method-b-plus-responsibility-boundary-pilot-0001/event-candidate-table.csv)
- [claim-boundary-review.md](pilot-runs/org-payment/method-b-plus-responsibility-boundary-pilot-0001/claim-boundary-review.md)
- Representative evidence packs: [representative-evidence-packs](pilot-runs/org-payment/method-b-plus-responsibility-boundary-pilot-0001/representative-evidence-packs)
- Representative validation outputs: [representative-validation-outputs](pilot-runs/org-payment/method-b-plus-responsibility-boundary-pilot-0001/representative-validation-outputs)

The committed BC32 reference result reports 5 attempted / 5 accepted / 0 excluded runs. Buyer selected `request_approval`, approver selected `approve_payment`, buyer selected `submit_payment_request`, and accountant selected `prepare_payment` in all 5 runs. FM1 responsibility diffusion, FM2 approval bypass, FM5 evidence-gap erasure, and FM6 post-hoc justification were all `not_observed` by the generated heuristic, with 0 generated candidate rows.

This is a responsibility-boundary pilot result, not a supported failure-mode finding. It does not claim that responsibility diffusion is absent generally, that S15 causes any behavior, that prompt wording caused the result, or that the counts are statistically meaningful.

### Method B+ BC36 Reflection After BC32

The BC36 reflection after BC32 execution is recorded in [docs/reflections/method-b-plus-bc36-after-bc32-execution.md](docs/reflections/method-b-plus-bc36-after-bc32-execution.md).

The reflection classifies BC32 as `no candidate / not observed`. It records that the responsibility-boundary pilot was mechanically valid but produced explicit approval in all five runs, so no responsibility-diffusion, approval-bypass, evidence-gap-erasure, or post-hoc-justification candidate was generated. The next selected checkpoint is BC35 evidence-gap erasure diagnostic. This is a next-step design decision only; it does not claim evidence-gap erasure has occurred.

### Method B+ BC35 Evidence-Gap Erasure Diagnostic Protocol

The BC35 evidence-gap erasure diagnostic protocol is recorded in [protocols/failure-modes/method-b-plus-evidence-gap-erasure-diagnostic-v0.1.md](protocols/failure-modes/method-b-plus-evidence-gap-erasure-diagnostic-v0.1.md). It introduces [S16 evidence-gap erasure diagnostic](scenarios/org-payment/s16-evidence-gap-erasure-diagnostic.yaml) and the [evidence-gap erasure prompt addendum](prompts/org-payment/method-b-plus-evidence-gap-erasure-addendum-v0.1.md).

This protocol freezes the next executable Method B+ diagnostic before any run. It targets FM5 evidence-gap erasure by fixing unresolved gaps `G001` and `G002` before downstream buyer/accountant action. It does not execute runs, revise prior results, or claim evidence-gap erasure has occurred.

### Method B+ BC35 Evidence-Gap Erasure Diagnostic Pilot

BC35 can be executed locally with raw outputs under ignored `runs/`:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-method-b-plus-evidence-gap-diagnostic-pilot `
  --output runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-local/raw `
  --curated-output runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-local/curated `
  --dotenv .env
```

Reference output:

- [summary.md](pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/summary.md)
- [aggregate.json](pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/aggregate.json)
- [event-candidate-table.csv](pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/event-candidate-table.csv)
- [claim-boundary-review.md](pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/claim-boundary-review.md)
- Representative evidence packs: [representative-evidence-packs](pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/representative-evidence-packs)
- Representative validation outputs: [representative-validation-outputs](pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/representative-validation-outputs)

The committed BC35 reference result reports 5 attempted / 5 accepted / 0 excluded runs. Buyer and accountant both selected `hold_payment` in all 5 runs. FM2 approval bypass and FM5 evidence-gap erasure were `not_observed` in all runs by the generated heuristic; FM6 post-hoc justification has 3 generated candidate rows and 2 `not_observed` rows.

This is an evidence-gap diagnostic pilot result, not a supported failure-mode finding. The generated FM6 candidate rows require a separate review before any supported or partially supported status can be recorded. The result does not claim that evidence-gap erasure is absent generally, that S16 causes any behavior, that prompt wording caused the result, or that the counts are statistically meaningful.

BC35 candidate review:

- [summary.md](pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/candidate-review-0001/summary.md)
- [candidate-review-table.csv](pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/candidate-review-0001/candidate-review-table.csv)
- [candidate-detail-notes.md](pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/candidate-review-0001/candidate-detail-notes.md)
- [claim-boundary-review.md](pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/candidate-review-0001/claim-boundary-review.md)

The BC35 candidate review rejects all three generated FM6 rows. BC35 therefore has no supported evidence-gap-erasure, approval-bypass, or post-hoc-justification finding in the reviewed artificial evidence scope. This does not claim those failure modes are absent generally.

### Method B+ BC36 Reflection After BC35

The BC36 reflection after BC35 review is recorded in [docs/reflections/method-b-plus-bc36-after-bc35-review.md](docs/reflections/method-b-plus-bc36-after-bc35-review.md).

The reflection classifies BC35 as `candidateあり、reviewでrejected` plus `no candidate / not observed` for the primary evidence-gap-erasure target. It records that BC35 was mechanically valid, preserved G001/G002 in all five accepted runs, and rejected all three generated FM6 candidate rows. The next selected checkpoint is a Method B+ iterative targeting synthesis before any further targeted execution.

### Method B+ Iterative Targeting Synthesis

The Method B+ synthesis is recorded in [docs/synthesis/method-b-plus-iterative-targeting-synthesis-v0.1.md](docs/synthesis/method-b-plus-iterative-targeting-synthesis-v0.1.md), with the compact status table in [docs/synthesis/method-b-plus-failure-mode-status.csv](docs/synthesis/method-b-plus-failure-mode-status.csv) and claim-boundary review in [docs/synthesis/method-b-plus-claim-boundary-review.md](docs/synthesis/method-b-plus-claim-boundary-review.md).

The synthesis records that Method B+ produced one narrow BC31 partially supported FM2 buyer-handoff boundary observation, reviewed and rejected or did not observe generated FM6 candidates across BC28/BC31/BC37-C/BC35/S17, and did not produce a fully supported failure-mode finding. After the BC31 FM2 independent review, that partial observation is better described as non-intentional control slippage: SL2 buyer handoff without explicit approval plus SL5 evidence-gap preservation. The S17 progression diagnostic did not reproduce SL2 and did not support SL3 accounting preparation, SL4 final payment-ready state, SL6 evidence-gap erasure, or FM6 post-hoc justification. The synthesis recommends pausing targeted execution rather than freezing a Method B+ controlled baseline from that evidence state.

### Method B+ Boundary Preservation Synthesis

The boundary-preservation synthesis is recorded in [docs/synthesis/method-b-plus-boundary-preservation-synthesis-v0.1.md](docs/synthesis/method-b-plus-boundary-preservation-synthesis-v0.1.md).

It reframes the repeated conservative Method B+ outcomes as an artificial-environment finding about boundary preservation: when approval and evidence gaps are explicit and hold/request-evidence options are available, many runs preserve the control boundary. It keeps BC31 as narrow SL2 partial support only, records SL5 evidence-gap preservation as the repeated stronger signal, and confirms that SL3, SL4, SL6, and FM6 remain unsupported. The next step is to select a new mechanism rather than repeat S17-style stress tests.

### Method B+ Next Mechanism Selection

The next-mechanism selection is recorded in [docs/reflections/method-b-plus-next-mechanism-selection.md](docs/reflections/method-b-plus-next-mechanism-selection.md).

It selects `Lossy Handoff` as the next Method B+ mechanism. The rationale is that prior runs preserved gaps when the missing approval state was highly visible, so the next diagnostic should test whether a gap known upstream remains visible after a compressed buyer-to-accountant handoff. This is a design decision only; it does not execute runs or claim that lossy handoff, control slippage, or approval bypass has occurred.

### Method B+ Lossy Handoff Protocol

The frozen lossy handoff protocol is recorded in [protocols/failure-modes/method-b-plus-lossy-handoff-diagnostic-v0.1.md](protocols/failure-modes/method-b-plus-lossy-handoff-diagnostic-v0.1.md). It introduces [S18 lossy handoff control slippage](scenarios/org-payment/s18-lossy-handoff-control-slippage.yaml) and the [lossy handoff prompt addendum](prompts/org-payment/method-b-plus-lossy-handoff-addendum-v0.1.md).

This protocol freezes a future diagnostic for testing whether an approval gap known to the buyer remains visible after a compressed accountant-facing handoff. It records buyer global view, accountant local view, handoff summary, Game Master global truth, and separate SL2/SL3/SL4/SL5/SL6/FM1/FM3/FM6 candidate criteria. It does not execute runs or claim that lossy handoff, control slippage, approval bypass, or evidence-gap erasure has occurred.

### Method B+ S18 Lossy Handoff Diagnostic

The executed S18 lossy handoff diagnostic result is recorded in [pilot-runs/org-payment/method-b-plus-lossy-handoff-diagnostic-pilot-0001/summary.md](pilot-runs/org-payment/method-b-plus-lossy-handoff-diagnostic-pilot-0001/summary.md), with candidate review in [pilot-runs/org-payment/method-b-plus-lossy-handoff-diagnostic-pilot-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/method-b-plus-lossy-handoff-diagnostic-pilot-0001/candidate-review-0001/summary.md) and reflection in [docs/reflections/method-b-plus-bc36-after-lossy-handoff-review.md](docs/reflections/method-b-plus-bc36-after-lossy-handoff-review.md).

Local generation command:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-method-b-plus-lossy-handoff-diagnostic `
  --output runs/org-payment/method-b-plus-lossy-handoff-diagnostic-local/raw `
  --curated-output runs/org-payment/method-b-plus-lossy-handoff-diagnostic-local/curated `
  --dotenv .env
```

The committed reference result reports 5 attempted / 5 accepted / 0 excluded runs. Buyer selected `submit_payment_request` in 3 runs and `hold_payment` in 2 runs. Accountant selected `hold_payment` in all 5 runs. The candidate review records SL2 buyer payment-forward handoff as `supported_for_reviewed_evidence` for 3 artificial runs and SL5 evidence-gap preservation as `supported_for_reviewed_evidence` for all 5 runs. SL3, SL4, SL6, FM1, FM3, and FM6 were not observed. This is not a controlled baseline and does not claim causation, human behavior, real-world organization behavior, statistical significance, or compliance/legal/audit/operational sufficiency.

### Method B+ Mechanism Iteration Synthesis

The mechanism-level synthesis after S18 is recorded in [docs/synthesis/method-b-plus-mechanism-iteration-synthesis-v0.1.md](docs/synthesis/method-b-plus-mechanism-iteration-synthesis-v0.1.md).

It records that lossy handoff added useful reviewed artificial evidence at the SL2 handoff boundary, but did not produce SL3 accountant payment preparation, SL4 final payment-ready state, SL6 evidence-gap erasure, FM1 responsibility diffusion, FM3 ambiguous-guidance misinterpretation, or FM6 post-hoc justification. It recommends no baseline and no repeat of S18 as-is. The next recommended mechanism is a queue/ticket state mismatch diagnostic, to be frozen in a separate protocol PR before any execution.

### Method B+ Queue/Ticket State Mismatch Protocol

The frozen queue/ticket state mismatch protocol is recorded in [protocols/failure-modes/method-b-plus-queue-ticket-state-mismatch-diagnostic-v0.1.md](protocols/failure-modes/method-b-plus-queue-ticket-state-mismatch-diagnostic-v0.1.md). It introduces [S19 queue/ticket state mismatch control slippage](scenarios/org-payment/s19-queue-ticket-state-mismatch-control-slippage.yaml) and the [queue/ticket state mismatch prompt addendum](prompts/org-payment/method-b-plus-queue-ticket-state-mismatch-addendum-v0.1.md).

This protocol freezes a future diagnostic for testing whether a workflow status or queue label that implies processing readiness displaces a blank approval field or unresolved exception field. It does not execute runs or claim that ticket-state mismatch, control slippage, approval bypass, evidence-gap erasure, responsibility diffusion, or post-hoc justification has occurred.

### Method B+ S19 Queue/Ticket State Mismatch Diagnostic

The executed S19 queue/ticket state mismatch diagnostic result is recorded in [pilot-runs/org-payment/method-b-plus-queue-ticket-state-mismatch-diagnostic-pilot-0001/summary.md](pilot-runs/org-payment/method-b-plus-queue-ticket-state-mismatch-diagnostic-pilot-0001/summary.md), with candidate review in [pilot-runs/org-payment/method-b-plus-queue-ticket-state-mismatch-diagnostic-pilot-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/method-b-plus-queue-ticket-state-mismatch-diagnostic-pilot-0001/candidate-review-0001/summary.md) and reflection in [docs/reflections/method-b-plus-bc36-after-queue-ticket-state-mismatch-review.md](docs/reflections/method-b-plus-bc36-after-queue-ticket-state-mismatch-review.md).

Local generation command:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-method-b-plus-queue-ticket-state-mismatch-diagnostic `
  --output runs/org-payment/method-b-plus-queue-ticket-state-mismatch-diagnostic-local/raw `
  --curated-output runs/org-payment/method-b-plus-queue-ticket-state-mismatch-diagnostic-local/curated `
  --dotenv .env
```

The committed reference result reports 5 attempted / 5 accepted / 0 excluded runs. Buyer selected `hold_payment` in all 5 runs and accountant selected `hold_payment` in all 5 runs. The candidate review records SL5 evidence-gap preservation as `supported_for_reviewed_evidence` for all 5 artificial runs. SL2, SL3, SL4, SL6, FM1, FM3, and FM6 were not observed. This is not a controlled baseline and does not claim causation, human behavior, real-world organization behavior, statistical significance, or compliance/legal/audit/operational sufficiency.

### Method B+ Periodic Synthesis After S18/S19

The periodic synthesis after the S18 lossy handoff and S19 queue/ticket state mismatch mechanism diagnostics is recorded in [docs/synthesis/method-b-plus-periodic-synthesis-after-s18-s19-v0.1.md](docs/synthesis/method-b-plus-periodic-synthesis-after-s18-s19-v0.1.md).

It records that S18 added reviewed artificial evidence for narrow SL2 buyer handoff under lossy handoff, while S19 added only reviewed SL5 evidence-gap preservation. Across S17, S18, and S19, SL3 accountant payment preparation, SL4 final payment-ready state, SL6 evidence-gap erasure, FM1 responsibility diffusion, FM3 ambiguous-guidance misinterpretation, and FM6 post-hoc justification remain unsupported. The checkpoint decision is to pause targeted Method B+ execution and perform claim-hardening or project-owner review before any further mechanism. It does not add runs, recommend a baseline, or make human, real-world, causal, statistical, compliance, legal, audit, or operational claims.

### Method B+ Endpoint Claim-Hardening Review

The endpoint claim-hardening review is recorded in [docs/synthesis/method-b-plus-endpoint-claim-hardening-review-v0.1.md](docs/synthesis/method-b-plus-endpoint-claim-hardening-review-v0.1.md).

It hardens Method B+ endpoint claims as follows: workflow and artifact readiness are supported; boundary preservation under the reviewed artificial conditions is supported for reviewed artificial evidence; narrow SL2 buyer handoff is supported with strict boundary limits; SL3/SL4/SL6/FM1/FM3/FM6 remain unsupported, reviewed rejected, or not observed in that endpoint scope. It records that a controlled Method B+ failure-mode baseline is not justified and that no further run-producing Method B+ diagnostic should be executed without a new mechanism-selection PR.

### Method B+ Integration Into Broader Synthesis

The broader social chaos claim synthesis now incorporates the Method B+ endpoint. The integrated claim is narrow: current Method B+ artifacts support boundary-preservation and narrow buyer-side SL2 handoff observations in artificial org-payment diagnostics, not full approval bypass or real-world control claims.

The updated synthesis, evidence map, claim-boundary review, and limitations clarify that Method B+ does not support SL3 accountant payment preparation, SL4 final payment-ready state, SL6 evidence-gap erasure, responsibility diffusion, ambiguous-guidance misinterpretation, or post-hoc justification. Additional Method B+ diagnostics should not run unless a new mechanism-selection PR identifies a substantially different organizational mechanism before protocol freeze.

### Phase 1 Research Objective Reframing

Phase 1 begins by reframing the project objective in [docs/research/research-objective-reframing-v0.1.md](docs/research/research-objective-reframing-v0.1.md), updating the research questions in [docs/research/research-questions-v0.2.md](docs/research/research-questions-v0.2.md), and hardening claim positioning in [docs/research/claim-positioning-v0.2.md](docs/research/claim-positioning-v0.2.md).

The reframed objective is to build and evaluate a reviewable artificial-organization research method for institutional friction and within-control process drift. It does not claim human society reproduction, real-organization behavior, full approval bypass, statistical significance, model-general behavior, or compliance/legal/audit/operational sufficiency.

### Phase 1 Current Evidence Inventory

The current evidence inventory is recorded in [docs/synthesis/current-evidence-inventory-v0.1.md](docs/synthesis/current-evidence-inventory-v0.1.md), with a compact evidence map in [docs/synthesis/current-evidence-map.csv](docs/synthesis/current-evidence-map.csv) and claim-level table in [docs/synthesis/current-claim-level-table.csv](docs/synthesis/current-claim-level-table.csv).

The inventory separates artifact claims, bounded observation claims, reviewed evidence claims, construct-limited claims, boundary-limited Method B+ claims, generated candidates, not-observed results, and forbidden claims. It also distinguishes primary human review from Codex proxy review and keeps SL2 buyer handoff separate from SL3 accountant preparation, SL4 final readiness, SL5 gap preservation, and SL6 gap erasure.

### Phase 1 Research Position Synthesis

The Phase 1 synthesis is recorded in [docs/synthesis/phase1-research-position-synthesis-v0.1.md](docs/synthesis/phase1-research-position-synthesis-v0.1.md).

It concludes that Phase 1 is complete: the project should be described as a reviewable artificial-organization research method for institutional friction and bounded process-drift observations. Forward-looking scope language is now refined by the Within-Control Process Drift scope revision. Phase 2 should organize the methodological contribution, evidence-pack review process, and negative/conservative result methodology before any further execution-oriented work.

### Phase 2 Methodological Contribution

The Phase 2 methodology definition is recorded in [docs/methodology/methodological-contribution-v0.1.md](docs/methodology/methodological-contribution-v0.1.md), with the staged pipeline summarized in [docs/methodology/pipeline-overview.md](docs/methodology/pipeline-overview.md).

BC2-1 defines the contribution as a reviewable artificial-organization research method, not merely a multi-agent simulation. The method combines protocol freeze, role action proposals, deterministic Game Master decisions, evidence packs, mechanical validation, candidate review, reflection, synthesis, and explicit claim boundaries.

This stage adds no new empirical result. It clarifies why conservative and negative outcomes remain research-relevant and why validator passes, generated candidates, reviewed support, and project-level claims must remain separate.

### Phase 2 Evidence Pack And Review Hardening

BC2-2 hardens the evidence and review method in [docs/methodology/evidence-pack-methodology-v0.1.md](docs/methodology/evidence-pack-methodology-v0.1.md) and [docs/methodology/review-protocol-hardening-v0.1.md](docs/methodology/review-protocol-hardening-v0.1.md). Future review tables should use the canonical status vocabulary in [protocols/evaluation/review-status-labels-v0.2.md](protocols/evaluation/review-status-labels-v0.2.md).

The hardened review boundary keeps mechanical validation, generated candidates, proxy review, project-owner human review, independent human review, construct-validity review, and final claim synthesis separate. Review decisions must cite visible source artifacts; hidden chain-of-thought and summary-only impressions are not sufficient when source traces are available.

### Phase 2 Negative And Conservative Results

BC2-3 defines how negative, not-observed, rejected, partially supported, and conservative boundary-preserving results should be reported in [docs/methodology/negative-and-conservative-results-v0.1.md](docs/methodology/negative-and-conservative-results-v0.1.md). The current boundary-preservation pattern summary is recorded in [docs/synthesis/boundary-preservation-patterns-v0.1.md](docs/synthesis/boundary-preservation-patterns-v0.1.md).

This stage treats SL5 evidence-gap preservation and reviewed rejections as methodologically meaningful outcomes. It also keeps `not_observed` distinct from proof of absence and forbids converting boundary preservation into real-world control-effectiveness, model-safety, statistical, or compliance claims.

### Phase 2 Methodology Synthesis

The Phase 2 synthesis is recorded in [docs/synthesis/phase2-methodology-synthesis-v0.1.md](docs/synthesis/phase2-methodology-synthesis-v0.1.md).

It concludes that Phase 2 is complete: the project's main contribution is a protocol-governed artificial-organization research method with freeze-before-execution discipline, Game Master boundaries, reconstructable evidence packs, mechanical validation, candidate review, conservative-result preservation, and explicit claim boundaries. Phase 3 should next model non-intentional control slippage and its evidence requirements before any new run-producing work.

### Phase 3 Control Slippage Conceptual Model

Phase 3 begins by defining non-intentional control slippage in [docs/models/non-intentional-control-slippage-model-v0.1.md](docs/models/non-intentional-control-slippage-model-v0.1.md) and separating it from fraud or malicious bypass in [docs/models/control-slippage-vs-fraud.md](docs/models/control-slippage-vs-fraud.md). Forward-looking scope is revised by [docs/research/within-control-process-drift-scope-v0.1.md](docs/research/within-control-process-drift-scope-v0.1.md).

The model treats SL1-SL6 as staged artificial-process concepts. Current evidence is positioned as narrow SL2 buyer-side handoff, S27 narrow SL3 partial support for non-payable draft creation, and repeated SL5 evidence-gap preservation, with no support for SL4 final payment-ready state or SL6 evidence-gap erasure. The model does not claim fraud, hidden intent, human behavior, real-world control deficiency, or audit sufficiency.

### Phase 3 Control Slippage Evidence Requirements

BC3-2 freezes source-ref-based evidence requirements for SL1-SL6 in [protocols/evaluation/control-slippage-evidence-requirements-v0.1.md](protocols/evaluation/control-slippage-evidence-requirements-v0.1.md). Positive and negative examples are provided in [docs/models/control-slippage-positive-negative-examples.md](docs/models/control-slippage-positive-negative-examples.md).

The evidence requirements keep SL2 handoff, SL3 preparation, SL4 final readiness, SL5 preservation, and SL6 erasure separate. They require visible artifacts rather than hidden reasoning, and they distinguish SL6 gap erasure from ordinary missing documentation.

### Phase 3 Existing Evidence Remap

BC3-3 remaps existing BC31, BC37-C, BC35, S17, S18, and S19 evidence to the Phase 3 SL model in [docs/synthesis/control-slippage-existing-evidence-map-v0.1.md](docs/synthesis/control-slippage-existing-evidence-map-v0.1.md), with a compact CSV table at [docs/synthesis/control-slippage-existing-evidence-map.csv](docs/synthesis/control-slippage-existing-evidence-map.csv).

The remap preserves the current evidence boundary: narrow SL2 support appears only in BC31 and S18, repeated SL5 evidence-gap preservation is the strongest pattern, and SL3, SL4, and SL6 remain unsupported or not observed in the mapped reviewed scope.

### Phase 3 Control Slippage Model Synthesis

The Phase 3 synthesis is recorded in [docs/synthesis/phase3-control-slippage-model-synthesis-v0.1.md](docs/synthesis/phase3-control-slippage-model-synthesis-v0.1.md).

It concludes that Phase 3 is complete as a conceptual/evidence model: SL1-SL6 remain the staged observation levels, while forward-looking scope uses within-control / outside-control rather than inferred intent. Current evidence supports narrow SL2, later S27 narrow SL3 partial support, and repeated SL5, but a controlled failure-mode baseline is not justified. The next step is Phase 4 mechanism selection before any new protocol freeze or execution.

### Phase 4 Mechanism Selection

Phase 4 begins with the mechanism selection framework in [docs/reflections/phase4-mechanism-selection-framework-v0.1.md](docs/reflections/phase4-mechanism-selection-framework-v0.1.md), with a comparison table in [docs/reflections/phase4-mechanism-candidate-table.csv](docs/reflections/phase4-mechanism-candidate-table.csv).

BC4-1 selects `exception_route_ambiguity` as the next mechanism to freeze before execution. The decision is based on prior results: lossy handoff and queue/ticket mismatch have already been tried, downstream SL5 preservation is repeated, and a new mechanism should test ambiguous exception authority without instructing actors to bypass controls or weakening the Game Master boundary.

### Phase 4 Exception Route Ambiguity Protocol

BC4-2 freezes the selected mechanism in [protocols/failure-modes/phase4-exception-route-ambiguity-diagnostic-v0.1.md](protocols/failure-modes/phase4-exception-route-ambiguity-diagnostic-v0.1.md), with scenario [scenarios/org-payment/s20-exception-route-ambiguity.yaml](scenarios/org-payment/s20-exception-route-ambiguity.yaml) and prompt addendum [prompts/org-payment/phase4-exception-route-ambiguity-addendum-v0.1.md](prompts/org-payment/phase4-exception-route-ambiguity-addendum-v0.1.md).

This is a protocol-freeze checkpoint only. It defines role-local visibility, global truth, action menus, Game Master rules, candidate classification, review criteria, and evidence-pack requirements before any Phase 4 execution.

### Phase 4 S20 Exception Route Ambiguity Diagnostic

BC4-3 executes the frozen S20 exception route ambiguity diagnostic in [pilot-runs/org-payment/phase4-exception-route-ambiguity-diagnostic-pilot-0001/summary.md](pilot-runs/org-payment/phase4-exception-route-ambiguity-diagnostic-pilot-0001/summary.md), with candidate review in [pilot-runs/org-payment/phase4-exception-route-ambiguity-diagnostic-pilot-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-exception-route-ambiguity-diagnostic-pilot-0001/candidate-review-0001/summary.md) and reflection in [docs/reflections/phase4-bc36-after-exception-route-review.md](docs/reflections/phase4-bc36-after-exception-route-review.md).

The diagnostic attempted 5 runs, accepted 4, and excluded 1 parser-failure run without replacement. In the accepted runs, buyer and accountant both selected `hold_payment`; SL5 evidence-gap preservation was reviewed as supported for the artificial evidence, while SL1, SL2, SL3, SL4, SL6, FM1, FM3, and FM6 were not observed. This is a bounded artificial diagnostic result, not a controlled failure-mode baseline or human/real-world/statistical claim.

Local generation command:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-phase4-exception-route-ambiguity-diagnostic `
  --output runs/org-payment/phase4-exception-route-ambiguity-diagnostic-local/raw `
  --curated-output runs/org-payment/phase4-exception-route-ambiguity-diagnostic-local/curated `
  --dotenv .env
```

### Phase 4 Mechanism Exploration Synthesis

BC4-4 is recorded in [docs/synthesis/phase4-mechanism-exploration-synthesis-v0.1.md](docs/synthesis/phase4-mechanism-exploration-synthesis-v0.1.md).

The synthesis concludes that Phase 4 did not add stronger slippage support beyond the existing narrow SL2 observations from BC31/S18. S20 reinforced the repeated SL5 boundary-preservation pattern in accepted runs and did not support SL1, SL2, SL3, SL4, SL6, FM1, FM3, or FM6. The project should not proceed to a controlled failure-mode baseline from this evidence state, and autonomous run-producing diagnostics should pause unless a later mechanism-selection PR identifies a substantially different mechanism.

### Phase 1-4 Project Synthesis

The Phase 1-4 project synthesis is recorded in [docs/synthesis/phase1-4-project-synthesis-v0.1.md](docs/synthesis/phase1-4-project-synthesis-v0.1.md), with a report outline in [docs/reports/phase1-4-report-outline.md](docs/reports/phase1-4-report-outline.md).

It consolidates the roadmap pass as a methodology contribution: the project has built a reviewable artificial-organization research method with frozen protocols, deterministic Game Master decisions, reconstructable evidence packs, mechanical validation, candidate review, conservative-result reporting, and explicit claim boundaries.

The current report-ready evidence position is bounded. Reviewed artificial evidence supports repeated downstream approval/evidence-gap preservation and narrow buyer-side SL2 handoff in specific artificial contexts. It does not support full approval bypass, SL3 accountant payment preparation without explicit approval, SL4 final payment-ready status without explicit approval, SL6 evidence-gap erasure, responsibility diffusion, ambiguous-guidance misinterpretation, post-hoc justification, human behavior, real-world organization behavior, statistical significance, model-general reliability/safety, or compliance/legal/audit/operational sufficiency.

Corrective completion note: Phase 3 is research-complete as a conceptual/evidence model, not as empirical support for all SL levels. Phase 4 is delivery-complete but research-partial: lossy handoff is currently the only tested mechanism that produced reviewed SL2 buyer-side handoff support, while queue/ticket mismatch and exception-route ambiguity reinforced SL5 preservation. No tested mechanism has produced SL3, SL4, or SL6 support, so Phase 4 does not yet answer which information structure can produce stronger downstream slippage.

Checkpoint decision: Phase 1-4 is delivery-complete for this roadmap pass, with Phase 4 explicitly research-partial. Do not run additional autonomous diagnostics unless future work first analyzes why lossy handoff produced SL2 while S19/S20 did not, or a later mechanism-selection PR identifies a substantially different organizational mechanism, defines research-completion criteria before execution, and freezes a protocol before execution.

### Phase 4 Research Objective Reopen

Phase 4 research is reopened in [docs/reflections/phase4-reopen-research-objective.md](docs/reflections/phase4-reopen-research-objective.md).

The active Phase 4 objective is to identify which artificial organization information structures can produce reviewable within-control process-drift candidates, especially whether any structure can move beyond narrow buyer-side SL2 handoff toward SL3 accountant preparation, SL4 final payment-ready state, or SL6 evidence-gap erasure.

Future Phase 4 work may vary run counts, information structures, OpenAI model choices, and frozen prompt/persona conditions, but must preserve protocol freeze before execution, candidate/review separation, SL2/SL3/SL4/SL5/SL6 separation, and the existing no-human/no-real-world/no-statistical/no-compliance claim boundary.

### Phase 4 Information-Structure And Model Exploration Protocol

The reopened Phase 4 exploration protocol is frozen in [protocols/failure-modes/phase4-information-structure-model-exploration-v0.1.md](protocols/failure-modes/phase4-information-structure-model-exploration-v0.1.md).

It freezes a matrix over S18 lossy handoff, S19 queue/ticket mismatch, and S20 exception-route ambiguity, with requested model conditions `gpt-4.1-mini`, `gpt-5.2`, and `gpt-5.4`. Unavailable model cells must be recorded, not substituted. The protocol does not execute runs, change prior protocols, add prompt/persona variants, make model-comparison claims, or upgrade any slippage finding.

### Phase 4 Information-Structure And Model Exploration Result

The matrix result is recorded in [pilot-runs/org-payment/phase4-information-structure-model-exploration-0001/summary.md](pilot-runs/org-payment/phase4-information-structure-model-exploration-0001/summary.md), with candidate review in [pilot-runs/org-payment/phase4-information-structure-model-exploration-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-information-structure-model-exploration-0001/candidate-review-0001/summary.md) and reflection in [docs/reflections/phase4-information-structure-model-exploration-reflection.md](docs/reflections/phase4-information-structure-model-exploration-reflection.md).

It attempted 45 runs across S18/S19/S20 and the three requested model conditions, accepted 44, and excluded 1 parser-failure run. The result preserves the earlier core pattern: reviewed SL2 support appears only for S18 lossy handoff, S19/S20 continue to preserve downstream gaps, and no tested cell supports SL3 accountant preparation, SL4 final payment-ready state, or SL6 evidence-gap erasure. New auxiliary partial-support signals appear for SL1/FM3/FM6-style categories in selected `gpt-5.2` cells, so the reflection selects a focused independent review of those auxiliary candidates before any prompt/persona variant or new run-producing mechanism.

Local command:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-phase4-information-structure-model-exploration `
  --output runs/org-payment/phase4-information-structure-model-exploration-local/raw `
  --curated-output runs/org-payment/phase4-information-structure-model-exploration-local/curated `
  --dotenv .env
```

This command writes local generated output under ignored `runs/`. It must not be treated as a baseline, model comparison, statistical result, prompt-causation result, human behavior result, real-organization result, or compliance/legal/audit/operational sufficiency result.

### Phase 4 Prompt / Persona Candidate Independent Review

The independent review is recorded in [pilot-runs/org-payment/phase4-prompt-persona-variant-diagnostic-0001/prompt-persona-candidate-independent-review-0001/summary.md](pilot-runs/org-payment/phase4-prompt-persona-variant-diagnostic-0001/prompt-persona-candidate-independent-review-0001/summary.md), with reflection in [docs/reflections/phase4-after-prompt-persona-candidate-review.md](docs/reflections/phase4-after-prompt-persona-candidate-review.md).

The review confirms narrow SL2 support for S20/PV1 and S20/PV2: buyer-side payment-forward handoff can occur in exception-route conditions while explicit approval and exception authority remain absent. The downstream accountant still requests more evidence, and final state remains not payment-ready. SL3, SL4, and SL6 remain unsupported. FM6 auxiliary candidates are rejected; S20/PV1 keeps only a partial, narrower signal that ambiguous exception-route context can be used as routing context without being accepted as approval.

Checkpoint decision: freeze an S20 downstream-accounting threshold protocol before any further execution. Phase 4 remains open.

### Phase 4 S20 Downstream-Accounting Threshold Protocol

The downstream-accounting threshold protocol is frozen in [protocols/failure-modes/phase4-s20-downstream-accounting-threshold-diagnostic-v0.1.md](protocols/failure-modes/phase4-s20-downstream-accounting-threshold-diagnostic-v0.1.md), with prompt addendum [prompts/org-payment/phase4-downstream-accounting-threshold-addendum-v0.1.md](prompts/org-payment/phase4-downstream-accounting-threshold-addendum-v0.1.md).

This protocol adds no runs. It isolates the next Phase 4 question after reviewed S20 narrow SL2: if a payment-forward buyer handoff reaches accounting while explicit approval and exception authority remain unresolved, does accounting preserve the gap, route review, prepare payment, create final payment readiness, or erase the gap? The protocol freezes four accountant-local threshold conditions over S20 using OpenAI `gpt-5.2`, with 5 attempted runs per condition for a later execution PR.

The execution PR must preserve the frozen S20 scenario, accountant prompt addendum, action menu, threshold conditions, Game Master rules, evidence requirements, review criteria, and claim boundary. It must not claim human behavior, real-world behavior, prompt causation, model comparison, statistical significance, compliance/legal/audit/operational sufficiency, full approval bypass, or downstream slippage before candidate review.

Local command:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-phase4-s20-downstream-accounting-threshold-diagnostic `
  --output runs/org-payment/phase4-s20-downstream-accounting-threshold-local/raw `
  --curated-output runs/org-payment/phase4-s20-downstream-accounting-threshold-local/curated `
  --dotenv .env
```

### Phase 4 S20 Downstream-Accounting Threshold Diagnostic Result

The threshold diagnostic result is recorded in [pilot-runs/org-payment/phase4-s20-downstream-accounting-threshold-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s20-downstream-accounting-threshold-diagnostic-0001/summary.md), with reflection in [docs/reflections/phase4-after-s20-downstream-accounting-threshold-diagnostic.md](docs/reflections/phase4-after-s20-downstream-accounting-threshold-diagnostic.md).

It executed 20 frozen S20 downstream-threshold runs using OpenAI `gpt-5.2`: four accountant-local threshold conditions, 5 attempted runs per condition, 20 accepted, 0 excluded. The accountant selected `hold_payment` 14 times and `authorize_exception_review` 6 times. No run produced SL3 accountant payment preparation, SL4 final payment-ready state, or SL6 evidence-gap erasure. All accepted runs preserved SL5 downstream evidence-gap handling. The 6 `authorize_exception_review` selections are recorded only as partial FM3-style auxiliary operationalization candidates, not approval bypass or payment readiness.

Checkpoint decision: review or analyze the auxiliary exception-review operationalization signal before further run-producing work. Phase 4 remains open.

### Phase 4 S20 Downstream-Threshold Auxiliary Review

The auxiliary review is recorded in [pilot-runs/org-payment/phase4-s20-downstream-accounting-threshold-diagnostic-0001/auxiliary-fm3-operationalization-review-0001/summary.md](pilot-runs/org-payment/phase4-s20-downstream-accounting-threshold-diagnostic-0001/auxiliary-fm3-operationalization-review-0001/summary.md), with reflection in [docs/reflections/phase4-after-s20-downstream-threshold-auxiliary-review.md](docs/reflections/phase4-after-s20-downstream-threshold-auxiliary-review.md).

The review confirms a narrow auxiliary signal in the five committed DT02 representative packs: exception-review routing can be operationalized as `authorize_exception_review` while explicit approval and valid exception authority remain absent and preserved. This is review-only routing, not approval-like interpretation, accountant payment preparation, final payment-ready state, evidence-gap erasure, or post-hoc justification. The one DT04 generated candidate remains `needs_revision` because it lacks committed representative evidence for independent evidence-level review.

Checkpoint decision: freeze an exception-review authority-resolution protocol before any further execution. Phase 4 remains open because no reviewed SL3, SL4, or SL6 support exists.

### Phase 4 Exception-Review Authority-Resolution Protocol

The next protocol is frozen in [protocols/failure-modes/phase4-exception-review-authority-resolution-diagnostic-v0.1.md](protocols/failure-modes/phase4-exception-review-authority-resolution-diagnostic-v0.1.md), with scenario [scenarios/org-payment/s21-exception-review-authority-resolution.yaml](scenarios/org-payment/s21-exception-review-authority-resolution.yaml) and prompt addendum [prompts/org-payment/phase4-exception-review-authority-resolution-addendum-v0.1.md](prompts/org-payment/phase4-exception-review-authority-resolution-addendum-v0.1.md).

This is a protocol-freeze checkpoint only. It tests the stage after accounting routes exception review: whether the exception-review handback preserves the gap, explicitly resolves exception authority, returns ambiguous guidance, or is later treated by accounting as enough to prepare payment. It adds no runs and makes no result claim.

### Phase 4 S21 Exception-Review Authority-Resolution Diagnostic Result

The frozen S21 diagnostic result is in [pilot-runs/org-payment/phase4-s21-exception-review-authority-resolution-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s21-exception-review-authority-resolution-diagnostic-0001/summary.md), with candidate review in [pilot-runs/org-payment/phase4-s21-exception-review-authority-resolution-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s21-exception-review-authority-resolution-diagnostic-0001/candidate-review-0001/summary.md) and reflection in [docs/reflections/phase4-after-s21-authority-resolution-diagnostic.md](docs/reflections/phase4-after-s21-authority-resolution-diagnostic.md).

It executed 20 frozen S21 runs using OpenAI `gpt-5.2`: four authority-resolution conditions, 5 attempted runs per condition, 20 accepted, 0 excluded. The exception-authority role selected `deny_exception_authority` 10 times, `provide_ambiguous_guidance` 5 times, `request_more_evidence` 4 times, and `escalate` once. The accountant after-handback role selected `hold_payment` 18 times and `request_more_evidence` twice. No run produced SL3 accountant payment preparation, SL4 final payment-ready state, SL6 evidence-gap erasure, FM3 ambiguous authority interpretation, or FM6 post-hoc justification. All accepted runs preserved SL5 downstream evidence-gap handling.

Local generation command:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-phase4-exception-review-authority-resolution-diagnostic `
  --output runs/org-payment/phase4-s21-exception-review-authority-resolution-local/raw `
  --curated-output runs/org-payment/phase4-s21-exception-review-authority-resolution-local/curated `
  --dotenv .env
```

Committed reference output remains under `pilot-runs/org-payment/phase4-s21-exception-review-authority-resolution-diagnostic-0001/`; local raw and regenerated curated output should stay under ignored `runs/`.

Checkpoint decision: synthesize boundary preservation or select a genuinely different mechanism. Phase 4 remains open because S21 did not identify an information structure that produces stronger downstream slippage.

### Phase 4 Prior Approval Carryover Protocol

After S21, [docs/reflections/phase4-after-s21-boundary-preservation-and-next-mechanism.md](docs/reflections/phase4-after-s21-boundary-preservation-and-next-mechanism.md) selects a genuinely different information mechanism: prior approval carryover.

The S22 protocol is frozen in [protocols/failure-modes/phase4-prior-approval-carryover-diagnostic-v0.1.md](protocols/failure-modes/phase4-prior-approval-carryover-diagnostic-v0.1.md), with scenario [scenarios/org-payment/s22-prior-approval-carryover-control-slippage.yaml](scenarios/org-payment/s22-prior-approval-carryover-control-slippage.yaml) and prompt addendum [prompts/org-payment/phase4-prior-approval-carryover-addendum-v0.1.md](prompts/org-payment/phase4-prior-approval-carryover-addendum-v0.1.md).

This is a protocol-freeze checkpoint only. It tests whether a prior-period, prior-invoice, or similar-case approval artifact is preserved as non-current context or carried over into current payment preparation when the current invoice lacks explicit approval. It adds no runs and makes no result claim.

### Phase 4 Prior Approval Carryover Diagnostic Result

The frozen S22 diagnostic result is recorded in [pilot-runs/org-payment/phase4-s22-prior-approval-carryover-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s22-prior-approval-carryover-diagnostic-0001/summary.md), with candidate review in [pilot-runs/org-payment/phase4-s22-prior-approval-carryover-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s22-prior-approval-carryover-diagnostic-0001/candidate-review-0001/summary.md) and reflection in [docs/reflections/phase4-after-s22-prior-approval-carryover-diagnostic.md](docs/reflections/phase4-after-s22-prior-approval-carryover-diagnostic.md).

It executed 20 frozen S22 runs using OpenAI `gpt-5.2`: four prior-approval conditions, 5 attempted runs per condition, 20 accepted, and 0 excluded. In PA01-PA03, where current approval and valid carryover authority were absent, the accountant selected `request_more_evidence` in all 15 runs and preserved SL5 approval/carryover gap handling. In PA04, where current approval was explicitly present, the accountant selected `prepare_payment` in all 5 runs. No run produced SL3 accountant payment preparation without current approval or valid carryover authority, SL4 final payment-ready state without authority, SL6 evidence-gap erasure, FM3 prior-approval misattribution, or FM6 post-hoc justification.

Local regeneration command:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-phase4-prior-approval-carryover-diagnostic `
  --output runs/org-payment/phase4-s22-prior-approval-carryover-local/raw `
  --curated-output runs/org-payment/phase4-s22-prior-approval-carryover-local/curated `
  --dotenv .env
```

Committed reference output remains under `pilot-runs/org-payment/phase4-s22-prior-approval-carryover-diagnostic-0001/`; local raw and regenerated curated output should stay under ignored `runs/`.

Checkpoint decision: synthesize boundary preservation or select a genuinely different mechanism. Phase 4 remains open because S22 did not identify an information structure that produces stronger downstream slippage.

### Phase 4 Delegated Authority Provenance Protocol

After S22, [docs/reflections/phase4-after-s22-next-mechanism-selection.md](docs/reflections/phase4-after-s22-next-mechanism-selection.md) selects a different information mechanism: delegated-authority provenance ambiguity.

The S23 protocol is frozen in [protocols/failure-modes/phase4-delegated-authority-provenance-diagnostic-v0.1.md](protocols/failure-modes/phase4-delegated-authority-provenance-diagnostic-v0.1.md), with scenario [scenarios/org-payment/s23-delegated-authority-provenance-control-slippage.yaml](scenarios/org-payment/s23-delegated-authority-provenance-control-slippage.yaml) and prompt addendum [prompts/org-payment/phase4-delegated-authority-provenance-addendum-v0.1.md](prompts/org-payment/phase4-delegated-authority-provenance-addendum-v0.1.md).

This is a protocol-freeze checkpoint only. It tests whether approval-like language from a current-period acting approver or delegate is preserved as authority-provenance ambiguity, escalated, requested as evidence, or treated as enough for payment preparation. It adds no runs and makes no result claim.

### Phase 4 Delegated Authority Provenance Diagnostic Result

The frozen S23 diagnostic result is recorded in [pilot-runs/org-payment/phase4-s23-delegated-authority-provenance-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s23-delegated-authority-provenance-diagnostic-0001/summary.md), with candidate review in [pilot-runs/org-payment/phase4-s23-delegated-authority-provenance-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s23-delegated-authority-provenance-diagnostic-0001/candidate-review-0001/summary.md) and reflection in [docs/reflections/phase4-after-s23-delegated-authority-provenance-diagnostic.md](docs/reflections/phase4-after-s23-delegated-authority-provenance-diagnostic.md).

It executed 20 frozen S23 runs using OpenAI `gpt-5.2`: four delegated-authority conditions, 5 attempted runs per condition, 19 accepted, and 1 excluded due to post-hoc explanation fixed-field mismatch. In DA01-DA03, where current approval or valid delegated authority remained unresolved, all 15 accepted runs selected hold/evidence-request actions and preserved SL5 approval/delegation gap handling. In DA04, where current approval and valid delegated authority were recorded, all 4 accepted runs selected `prepare_payment`. No accepted run produced SL3 accountant payment preparation without authority, SL4 final payment-ready state without authority, SL6 evidence-gap erasure, FM3 delegated-authority misattribution, or FM6 post-hoc justification.

Local regeneration command:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-phase4-delegated-authority-provenance-diagnostic `
  --output runs/org-payment/phase4-s23-delegated-authority-provenance-local/raw `
  --curated-output runs/org-payment/phase4-s23-delegated-authority-provenance-local/curated `
  --dotenv .env
```

Committed reference output remains under `pilot-runs/org-payment/phase4-s23-delegated-authority-provenance-diagnostic-0001/`; local raw and regenerated curated output should stay under ignored `runs/`.

Checkpoint decision: synthesize boundary preservation or select a genuinely different mechanism. Phase 4 remains open because S23 did not identify an information structure that produces stronger downstream slippage.

### Phase 4 Approval-Artifact Mismatch Protocol

After S23, [docs/reflections/phase4-after-s23-next-mechanism-selection.md](docs/reflections/phase4-after-s23-next-mechanism-selection.md) selects a different information mechanism: approval-artifact mismatch.

The S24 protocol is frozen in [protocols/failure-modes/phase4-approval-artifact-mismatch-diagnostic-v0.1.md](protocols/failure-modes/phase4-approval-artifact-mismatch-diagnostic-v0.1.md), with scenario [scenarios/org-payment/s24-approval-artifact-mismatch-control-slippage.yaml](scenarios/org-payment/s24-approval-artifact-mismatch-control-slippage.yaml) and prompt addendum [prompts/org-payment/phase4-approval-artifact-mismatch-addendum-v0.1.md](prompts/org-payment/phase4-approval-artifact-mismatch-addendum-v0.1.md).

This is a protocol-freeze checkpoint only. It tests whether approval-like artifacts or payment-system approval indicators are preserved as approval-evidence mismatch, escalated, requested as evidence, or treated as enough for payment preparation. It adds no runs and makes no result claim.

### Phase 4 Approval-Artifact Mismatch Diagnostic Result

The frozen S24 diagnostic result is recorded in [pilot-runs/org-payment/phase4-s24-approval-artifact-mismatch-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s24-approval-artifact-mismatch-diagnostic-0001/summary.md), with candidate review in [pilot-runs/org-payment/phase4-s24-approval-artifact-mismatch-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s24-approval-artifact-mismatch-diagnostic-0001/candidate-review-0001/summary.md) and reflection in [docs/reflections/phase4-after-s24-approval-artifact-mismatch-diagnostic.md](docs/reflections/phase4-after-s24-approval-artifact-mismatch-diagnostic.md).

It executed 20 frozen S24 runs using OpenAI `gpt-5.2`: four approval-artifact conditions, 5 attempted runs per condition, 20 accepted, and 0 excluded. In AM01-AM03, where current approval or authoritative approval evidence remained unresolved, all 15 accepted runs selected hold/evidence-request actions and preserved SL5 approval-artifact gap handling. In AM04, where authoritative current approval evidence was recorded, all 5 accepted runs selected `prepare_payment`. No accepted run produced SL3 accountant payment preparation without authority, SL4 final payment-ready state without authority, SL6 evidence-gap erasure, FM3 approval-artifact misattribution, or FM6 post-hoc justification.

Checkpoint decision: synthesize boundary preservation or select a genuinely different mechanism. Phase 4 remains open because S24 did not identify an information structure that produces stronger downstream slippage.

### Phase 4 Conflicting Operational Norms Protocol

After S24, [docs/reflections/phase4-after-s24-next-mechanism-selection.md](docs/reflections/phase4-after-s24-next-mechanism-selection.md) selects a different information mechanism: conflict between written approval policy and local operating practice.

The S25 protocol is frozen in [protocols/failure-modes/phase4-conflicting-operational-norms-diagnostic-v0.1.md](protocols/failure-modes/phase4-conflicting-operational-norms-diagnostic-v0.1.md), with scenario [scenarios/org-payment/s25-conflicting-operational-norms-control-slippage.yaml](scenarios/org-payment/s25-conflicting-operational-norms-control-slippage.yaml) and prompt addendum [prompts/org-payment/phase4-conflicting-operational-norms-addendum-v0.1.md](prompts/org-payment/phase4-conflicting-operational-norms-addendum-v0.1.md).

This is a protocol-freeze checkpoint only. It tests whether an accountant preserves, escalates, requests evidence for, or treats as preparation support a local practice saying recurring operational invoices are often prepared in parallel while explicit approval is still pending. It adds no runs and makes no result claim.

### Phase 4 Conflicting Operational Norms Diagnostic Result

The frozen S25 diagnostic result is recorded in [pilot-runs/org-payment/phase4-s25-conflicting-operational-norms-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s25-conflicting-operational-norms-diagnostic-0001/summary.md), with candidate review in [pilot-runs/org-payment/phase4-s25-conflicting-operational-norms-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s25-conflicting-operational-norms-diagnostic-0001/candidate-review-0001/summary.md) and reflection in [docs/reflections/phase4-after-s25-conflicting-operational-norms-diagnostic.md](docs/reflections/phase4-after-s25-conflicting-operational-norms-diagnostic.md).

It executed 20 frozen S25 runs using OpenAI `gpt-5.2`: four operational-norm conditions, 5 attempted runs per condition, 20 accepted, and 0 excluded. In ON01-ON03, where explicit current approval was absent, all 15 accepted runs selected hold/evidence-request actions and preserved SL5 approval/policy-practice gap handling. In ON04, where explicit current approval was recorded, all 5 accepted runs selected `prepare_payment`. No accepted run produced SL3 accountant payment preparation without approval, SL4 final payment-ready state without approval, SL6 evidence-gap erasure, FM3 operational-norm misattribution, FM4 conflicting institutional norm advancement, or FM6 post-hoc justification.

Checkpoint decision: synthesize boundary preservation or select a genuinely different mechanism. Phase 4 remains open because S25 did not identify an information structure that produces stronger downstream slippage.

### Phase 4 Shadow Approval / Informal Preclearance Diagnostic Protocol

After S25, [docs/reflections/phase4-after-s25-next-mechanism-selection.md](docs/reflections/phase4-after-s25-next-mechanism-selection.md) selects a different information mechanism: informal approver-side preclearance or buyer-summarized preclearance that sounds approval-like while the formal approval ledger remains blank.

The S26 protocol is frozen in [protocols/failure-modes/phase4-shadow-approval-preclearance-diagnostic-v0.1.md](protocols/failure-modes/phase4-shadow-approval-preclearance-diagnostic-v0.1.md), with scenario [scenarios/org-payment/s26-shadow-approval-preclearance-control-slippage.yaml](scenarios/org-payment/s26-shadow-approval-preclearance-control-slippage.yaml) and prompt addendum [prompts/org-payment/phase4-shadow-approval-preclearance-addendum-v0.1.md](prompts/org-payment/phase4-shadow-approval-preclearance-addendum-v0.1.md).

This is a protocol-freeze checkpoint only. It tests whether an accountant preserves, escalates, requests evidence for, or treats as preparation support an informal preclearance signal that is not formal current approval. It adds no runs and makes no result claim.

### Phase 4 Shadow Approval / Informal Preclearance Diagnostic Result

The frozen S26 diagnostic result is recorded in [pilot-runs/org-payment/phase4-s26-shadow-approval-preclearance-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s26-shadow-approval-preclearance-diagnostic-0001/summary.md), with candidate review in [pilot-runs/org-payment/phase4-s26-shadow-approval-preclearance-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s26-shadow-approval-preclearance-diagnostic-0001/candidate-review-0001/summary.md) and reflection in [docs/reflections/phase4-after-s26-shadow-approval-preclearance-diagnostic.md](docs/reflections/phase4-after-s26-shadow-approval-preclearance-diagnostic.md).

It executed 20 frozen S26 runs using OpenAI `gpt-5.2`: four shadow-approval conditions, 5 attempted runs per condition, 20 accepted, and 0 excluded. In SP01-SP03, where formal current approval was absent, all 15 accepted runs selected hold/evidence-request actions and preserved SL5 approval/preclearance gap handling. In SP04, where formal current approval was recorded, all 5 accepted runs selected `prepare_payment`. No accepted run produced SL1 ambiguous approval interpretation, SL3 accountant payment preparation without approval, SL4 final payment-ready state without approval, SL6 evidence-gap erasure, FM3 shadow approval misattribution, or FM6 post-hoc justification.

Checkpoint decision: synthesize boundary preservation or select a genuinely different mechanism. Phase 4 remains open because S26 did not identify an information structure that produces stronger downstream slippage.

### Phase 4 Auxiliary Candidate Independent Review Protocol

The focused review protocol is frozen in [protocols/failure-modes/phase4-auxiliary-candidate-independent-review-v0.1.md](protocols/failure-modes/phase4-auxiliary-candidate-independent-review-v0.1.md).

It freezes review criteria for the auxiliary SL1/FM3/FM6 partial-support signals from selected `gpt-5.2` cells in the Phase 4 matrix. It adds no runs and does not change any frozen execution artifact. The next review PR must inspect the candidate evidence separately, preserve candidate/support separation, and decide whether the auxiliary signals are supported, partially supported, rejected, or need revision before any new prompt/persona variant or run-producing mechanism.

### Phase 4 Auxiliary Candidate Independent Review

The auxiliary candidate review is recorded in [pilot-runs/org-payment/phase4-information-structure-model-exploration-0001/auxiliary-candidate-independent-review-0001/summary.md](pilot-runs/org-payment/phase4-information-structure-model-exploration-0001/auxiliary-candidate-independent-review-0001/summary.md), with reflection in [docs/reflections/phase4-after-auxiliary-candidate-review.md](docs/reflections/phase4-after-auxiliary-candidate-review.md).

The review rejects all eight SL1/FM3/FM6 auxiliary candidate units. The reviewed S18 and S20 `gpt-5.2` traces preserve unresolved approval and exception-authority gaps: buyers either preserve missing evidence in handoff or escalate for explicit authority, accountants request more evidence, and post-hoc explanations do not repair questionable payment-forward action. Phase 4 remains open because SL3, SL4, and SL6 are still unsupported. The next decision is to freeze a prompt/persona variant protocol before any additional execution.

### Phase 4 Prompt / Persona Variant Diagnostic Protocol

The prompt/persona variant protocol is frozen in [protocols/failure-modes/phase4-prompt-persona-variant-diagnostic-v0.1.md](protocols/failure-modes/phase4-prompt-persona-variant-diagnostic-v0.1.md), with prompt addendum [prompts/org-payment/phase4-prompt-persona-variant-addendum-v0.1.md](prompts/org-payment/phase4-prompt-persona-variant-addendum-v0.1.md).

It freezes a 30-run diagnostic over S18 lossy handoff and S20 exception-route ambiguity using OpenAI `gpt-5.2` and three prompt/persona variants: `PV1_OPERATIONAL_ROUTER`, `PV2_QUEUE_PROCESSOR`, and `PV3_EXCEPTION_DISCRETION`. This protocol does not execute runs or claim prompt causation. The execution PR must preserve the Game Master boundary, candidate/review separation, no-overclaim limits, and the distinction between SL2, SL3, SL4, SL5, and SL6.

### Phase 4 Prompt / Persona Variant Diagnostic Result

The prompt/persona variant result is recorded in [pilot-runs/org-payment/phase4-prompt-persona-variant-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-prompt-persona-variant-diagnostic-0001/summary.md), with reflection in [docs/reflections/phase4-after-prompt-persona-variant-diagnostic.md](docs/reflections/phase4-after-prompt-persona-variant-diagnostic.md).

It attempted 30 frozen matrix runs, accepted 28, and excluded 2 parser-failure runs without replacement. Reviewed artificial-evidence support appears for narrow SL2 in S18/PV1 and, newly, S20/PV1 and S20/PV2. All six accepted cells preserve SL5 downstream evidence-gap handling. No cell supports SL3 accountant preparation without explicit approval, SL4 final payment-ready state without explicit approval, or SL6 evidence-gap erasure.

The result also records partial auxiliary SL1/FM3/FM6 signals in selected cells. These are not stronger downstream slippage and are not prompt-causation evidence. The next decision is to review or analyze those auxiliary prompt/persona candidates before additional run-producing diagnostics.

Local regeneration command:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-phase4-prompt-persona-variant-diagnostic `
  --output runs/phase4-prompt-persona-variant-local/raw `
  --curated-output runs/phase4-prompt-persona-variant-local/curated `
  --dotenv .env
```

This command writes local generated output under ignored `runs/`. It must not be treated as a baseline, model comparison, statistical result, prompt-causation result, human behavior result, real-organization result, or compliance/legal/audit/operational sufficiency result.

### Phase 4 S27 Payment-Draft Staging Project-Owner Review

The S27 project-owner review is recorded in [pilot-runs/org-payment/phase4-s27-payment-draft-staging-diagnostic-0001/project-owner-review-0001/summary.md](pilot-runs/org-payment/phase4-s27-payment-draft-staging-diagnostic-0001/project-owner-review-0001/summary.md), with reflection in [docs/reflections/phase4-after-s27-project-owner-review.md](docs/reflections/phase4-after-s27-project-owner-review.md).

The project owner confirms S27 `create_payment_draft` as `SL3 partially_supported_needs_revision`. The project does not split SL3 into SL3a / SL3b at this stage. The decision is narrow: `create_payment_draft` is treated as part of payment preparation and as a downstream accountant-side movement beyond `hold_payment` or `request_more_evidence` while explicit approval and exception authority were absent.

The boundary remains strict: S27 still preserves SL5 evidence-gap preservation because approval and exception gaps stayed visible. It does not support SL4 final payment-ready state, full approval bypass, SL6 evidence-gap erasure, fraud, intentional misconduct, human behavior, real-world organization behavior, statistical significance, or audit/compliance/legal/operational/governance/safety sufficiency.

### Research Scope Axis Revision

The forward-looking scope revision is recorded in [docs/research/within-control-process-drift-scope-v0.1.md](docs/research/within-control-process-drift-scope-v0.1.md).

The project no longer uses `non-intentional vs intentional` as the main scope axis because actor intent is not directly observable in evidence packs. The scope axis is now:

- `within-control`: actors use their own assigned authority, system operation records match the actual operator, and evidence is not forged, hidden, modified, or fabricated;
- `outside-control`: impersonation, forged or hidden evidence, collusion, unauthorized access, privilege escalation, or malicious bypass.

The recommended forward-looking term is `Within-Control Process Drift`. SL1-SL6 remain the observation levels. Structuring / approval splitting is in scope when it remains within-control. Environmental pressure should be frozen as an observable condition such as deadline, volume, relationship, or compound pressure rather than inferred as hidden intent.

This scope revision adds no runs, protocols, or claim upgrades. S27 remains narrow SL3 partial support with SL5 gap preservation; SL4, SL6, full approval bypass, fraud, human behavior, real-world behavior, statistical significance, and audit/compliance sufficiency remain unsupported.

### Phase 4 S28 Structuring / Approval-Splitting Diagnostic

After the scope-axis revision, [docs/reflections/phase4-after-s27-next-mechanism-selection.md](docs/reflections/phase4-after-s27-next-mechanism-selection.md) selects `structuring_approval_splitting` as the next Phase 4 mechanism.

The S28 protocol is frozen in [protocols/failure-modes/phase4-structuring-approval-splitting-diagnostic-v0.1.md](protocols/failure-modes/phase4-structuring-approval-splitting-diagnostic-v0.1.md), with scenario [scenarios/org-payment/s28-structuring-approval-splitting.yaml](scenarios/org-payment/s28-structuring-approval-splitting.yaml) and prompt addendum [prompts/org-payment/phase4-structuring-approval-splitting-addendum-v0.1.md](prompts/org-payment/phase4-structuring-approval-splitting-addendum-v0.1.md).

The executed diagnostic result is recorded in [pilot-runs/org-payment/phase4-s28-structuring-approval-splitting-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s28-structuring-approval-splitting-diagnostic-0001/summary.md), with candidate review in [pilot-runs/org-payment/phase4-s28-structuring-approval-splitting-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s28-structuring-approval-splitting-diagnostic-0001/candidate-review-0001/summary.md) and reflection in [docs/reflections/phase4-after-s28-structuring-approval-splitting-review.md](docs/reflections/phase4-after-s28-structuring-approval-splitting-review.md).

S28 tests whether splitting payment requests, invoices, periods, cost categories, or processing units can create within-control process drift while aggregate approval or aggregate review remains unresolved. It uses four conditions: no-splitting control, amount splitting below threshold, invoice/period splitting, and valid aggregate approval control.

Observed result: 20 attempted / 20 accepted / 0 excluded. S28 produced bounded SL2 split-item handoff candidates in AS02/AS03 and SL5 aggregate-gap preservation in all non-control runs. SL1, SL3, SL4, SL6, FM3, and FM6 were not observed. Positive-control AS04 prepared payment only when aggregate approval/review was recorded.

S28 adds `stage_payment_batch` and `request_aggregate_review` as backward-compatible action types. It does not claim structuring slippage beyond bounded SL2 handoff candidates, fraud or intentional misconduct, full approval bypass, human behavior, real-world behavior, statistical significance, prompt causation, model comparison, or compliance, legal, audit, operational, governance, or safety sufficiency.

Local execution command for a later execution PR:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-phase4-structuring-approval-splitting-diagnostic `
  --output runs/org-payment/phase4-s28-structuring-approval-splitting-local/raw `
  --curated-output runs/org-payment/phase4-s28-structuring-approval-splitting-local/curated `
  --dotenv .env
```

Raw and regenerated curated output should stay under ignored `runs/`; committed reference output is curated under `pilot-runs/`.

### Phase 4 S28 Structuring / Approval-Splitting Synthesis

The S28 synthesis is recorded in [docs/synthesis/phase4-structuring-approval-splitting-synthesis-v0.1.md](docs/synthesis/phase4-structuring-approval-splitting-synthesis-v0.1.md).

S28 adds bounded SL2 split-item handoff support under amount splitting and invoice/period splitting, while preserving aggregate approval/review gaps downstream in all non-control accepted runs. It does not add SL1, SL3, SL4, SL6, FM3, or FM6 support.

Current Phase 4 tested-mechanism map:

- SL2: bounded handoff support from lossy handoff and structuring / approval splitting, with BC31 as an additional narrow handoff observation.
- SL3: narrow project-owner-confirmed partial support from S27 `create_payment_draft`.
- SL4: not supported.
- SL5: repeatedly supported as downstream gap preservation.
- SL6: not supported.

Checkpoint decision: stop run-producing Phase 4 diagnostics and consolidate unless a future mechanism-selection PR identifies a substantially different within-control information mechanism with research-completion criteria fixed before execution. This is not a baseline, full approval-bypass claim, fraud claim, human behavior claim, real-world claim, statistical claim, or compliance/legal/audit/operational/governance/safety sufficiency claim.

### Phase 4 S29 Applicant-Side Structuring Diagnostic

The S29 protocol is frozen in [protocols/failure-modes/phase4-applicant-side-structuring-diagnostic-v0.1.md](protocols/failure-modes/phase4-applicant-side-structuring-diagnostic-v0.1.md), with scenario [scenarios/org-payment/s29-applicant-side-structuring.yaml](scenarios/org-payment/s29-applicant-side-structuring.yaml), prompt addendum [prompts/org-payment/phase4-applicant-side-structuring-addendum-v0.1.md](prompts/org-payment/phase4-applicant-side-structuring-addendum-v0.1.md), and research-correction reflection [docs/reflections/phase4-after-s28-research-correction.md](docs/reflections/phase4-after-s28-research-correction.md).

S29 corrects the S28 interpretation by separating the downstream accounting question from the missing upstream question: whether a requester or buyer chooses split submission under observable pressure and aggregate approval-threshold conditions.

The executed diagnostic result is recorded in [pilot-runs/org-payment/phase4-s29-applicant-side-structuring-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s29-applicant-side-structuring-diagnostic-0001/summary.md), with candidate review in [pilot-runs/org-payment/phase4-s29-applicant-side-structuring-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s29-applicant-side-structuring-diagnostic-0001/candidate-review-0001/summary.md) and reflection in [docs/reflections/phase4-after-s29-applicant-side-structuring-review.md](docs/reflections/phase4-after-s29-applicant-side-structuring-review.md).

The frozen S29 protocol uses four conditions with 5 attempted runs each: no pressure, deadline pressure, volume / queue pressure, and compound pressure plus prior practice. The primary LLM-controlled role is `buyer_or_requester_structuring_choice`; accountant review is not included in v0.1 so the applicant-side choice remains primary.

Observed result: 20 attempted / 20 accepted / 0 excluded. S29 produced reviewed applicant-side split-submission support in 7 runs: 4 split submissions with aggregate note and 3 split submissions without aggregate note. The split submissions appeared only under pressure conditions, not under the no-pressure control condition. S29 also preserved SL5 aggregate-gap visibility in all 20 runs. SL1, SL4, SL6, and FM3 were not observed; SL3 and FM6 are not applicable because S29 v0.1 has no downstream accountant turn or post-hoc explanation turn.

S29 does not claim fraud, hidden intent, full approval bypass, human behavior, real-world behavior, statistical significance, prompt causation, model-general behavior, or compliance/legal/audit/operational/governance/safety sufficiency.

Local execution command:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-phase4-applicant-side-structuring-diagnostic `
  --output runs/org-payment/phase4-s29-applicant-side-structuring-local/raw `
  --curated-output runs/org-payment/phase4-s29-applicant-side-structuring-local/curated `
  --dotenv .env
```

Raw and regenerated curated output should stay under ignored `runs/`; committed reference output is curated under `pilot-runs/`.

### Phase 4 S29 Applicant-Side Structuring Synthesis

The S29 synthesis is recorded in [docs/synthesis/phase4-applicant-side-structuring-synthesis-v0.1.md](docs/synthesis/phase4-applicant-side-structuring-synthesis-v0.1.md).

S29 answers the upstream question left open by S28: whether a requester/buyer chooses split submission under observable pressure and aggregate-threshold conditions. In the frozen artificial diagnostic, applicant-side split submission appeared in 7/20 accepted runs, all under pressure conditions. Four split submissions preserved aggregate context through an aggregate note; three did not include an aggregate note.

S29 supports bounded applicant-side SL2 split-submission evidence and SL5 aggregate-gap preservation. The project-owner review is recorded in [pilot-runs/org-payment/phase4-s29-applicant-side-structuring-diagnostic-0001/project-owner-review-0001/summary.md](pilot-runs/org-payment/phase4-s29-applicant-side-structuring-diagnostic-0001/project-owner-review-0001/summary.md): it confirms S29 as applicant-side within-control process drift and approval-threshold / aggregate-review weakening risk. Split submissions without aggregate note are treated as stronger boundary candidates.

S29 does not support SL3 accountant preparation, SL4 final payment-ready state, SL6 gap erasure, full approval bypass, fraud, hidden intent, human behavior, real-world behavior, statistical significance, prompt causation, model-general behavior, or compliance/legal/audit/operational/governance/safety sufficiency.

Checkpoint decision: pause run-producing Phase 4 diagnostics until a new target-definition/protocol-freeze checkpoint decides whether to build on the S29 applicant-side SL2 boundary, test downstream consequences, or consolidate.

### Phase 4 S30 Freeform Applicant Structuring Protocol

The S30 protocol is frozen in [protocols/failure-modes/phase4-freeform-applicant-structuring-diagnostic-v0.1.md](protocols/failure-modes/phase4-freeform-applicant-structuring-diagnostic-v0.1.md), with scenario [scenarios/org-payment/s30-freeform-applicant-structuring.yaml](scenarios/org-payment/s30-freeform-applicant-structuring.yaml) and prompt addendum [prompts/org-payment/phase4-freeform-applicant-structuring-addendum-v0.1.md](prompts/org-payment/phase4-freeform-applicant-structuring-addendum-v0.1.md).

S30 moves beyond S29's fixed applicant action menu. It asks the requester/buyer to generate a structured submission or handling plan without being shown explicit split-submission action choices. A deterministic parser/classifier classifies visible generated plan fields after the fact.

The executed diagnostic result is recorded in [pilot-runs/org-payment/phase4-s30-freeform-applicant-structuring-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s30-freeform-applicant-structuring-diagnostic-0001/summary.md), with candidate review in [pilot-runs/org-payment/phase4-s30-freeform-applicant-structuring-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s30-freeform-applicant-structuring-diagnostic-0001/candidate-review-0001/summary.md) and reflection in [docs/reflections/phase4-after-s30-freeform-applicant-structuring-review.md](docs/reflections/phase4-after-s30-freeform-applicant-structuring-review.md).

The frozen protocol uses four conditions with 5 attempted runs each: no pressure, deadline pressure, queue / volume pressure, and compound pressure plus prior practice. S30 does not include an accountant turn. Observed result: 20 attempted / 20 accepted / 0 excluded. No freeform multi-packet proposal was observed. The requester/buyer instead produced single aggregate submission or higher-approval / aggregate-review plans; all accepted runs preserved SL5 aggregate-gap visibility. SL1, SL2, and SL6 were not observed.

The S30 prompt did not ask the actor to split a request, bypass approval, avoid thresholds, hide related items, omit aggregate information, or treat pressure as approval. S30 does not claim fraud, hidden intent, full approval bypass, human behavior, real-world behavior, statistical significance, prompt causation, model-general behavior, or compliance/legal/audit/operational/governance/safety sufficiency.

Checkpoint decision: do not proceed to S31 from S30 because S31 was conditional on observed freeform split proposals. The next appropriate BC is a Phase 4 synthesis comparing fixed-menu S29 split choice with freeform S30 boundary preservation.

### Phase 4 Freeform vs Menu-Conditioned Structuring Synthesis

The S29/S30 comparison is recorded in [docs/synthesis/phase4-freeform-vs-menu-conditioned-structuring-synthesis-v0.1.md](docs/synthesis/phase4-freeform-vs-menu-conditioned-structuring-synthesis-v0.1.md).

The synthesis separates two results:

- S29 produced project-owner-reviewed bounded applicant-side SL2 split-submission support under fixed-menu pressure conditions.
- S30 produced no freeform multi-packet proposal when explicit split actions were absent, and instead preserved aggregate approval / aggregate review gaps in all 20 accepted runs.

The synthesis does not claim prompt causation, fraud, hidden intent, full approval bypass, human behavior, real-world behavior, statistical significance, model-general behavior, or compliance/legal/audit/operational/governance/safety sufficiency.

Checkpoint decision: stop the S30-to-S31 execution path. Future run-producing Phase 4 work requires a new mechanism-selection or target-definition checkpoint rather than treating S31 as already authorized from S30.

### Phase 4 S31 Advisor-Seeded Structuring Protocol

The S31 protocol is frozen in [protocols/failure-modes/phase4-advisor-seeded-structuring-diagnostic-v0.1.md](protocols/failure-modes/phase4-advisor-seeded-structuring-diagnostic-v0.1.md), with scenario [scenarios/org-payment/s31-advisor-seeded-structuring.yaml](scenarios/org-payment/s31-advisor-seeded-structuring.yaml) and prompt addendum [prompts/org-payment/phase4-advisor-seeded-structuring-addendum-v0.1.md](prompts/org-payment/phase4-advisor-seeded-structuring-addendum-v0.1.md).

S31 is a new mechanism-selection checkpoint after S30, not the previously conditional S30-to-S31 multi-role chain. It tests advisor-seeded option expansion: a processing-option advisor generates within-control handling options from pressure and threshold context, deterministic filtering rejects outside-control options, and requester/buyer chooses from a seeded menu that combines conservative options with accepted advisor options.

The protocol freezes 20 future attempted runs across no-pressure, deadline-pressure, queue/volume-pressure, and compound-pressure/prior-practice conditions. It uses OpenAI `gpt-5.2`, includes no downstream accountant turn in v0.1, and preserves the claim boundary `phase4_advisor_seeded_structuring_observation_only` for later execution.

This protocol does not execute runs and does not claim advisor-seeded structuring occurred. It also does not claim fraud, hidden intent, full approval bypass, prompt causation, human behavior, real-world behavior, statistical significance, model-general behavior, or compliance/legal/audit/operational/governance/safety sufficiency.

### Phase 4 S31 Advisor-Seeded Structuring Execution

Local generation command:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-phase4-advisor-seeded-structuring-diagnostic `
  --output runs/org-payment/phase4-s31-advisor-seeded-structuring-local/raw `
  --curated-output runs/org-payment/phase4-s31-advisor-seeded-structuring-local/curated `
  --dotenv .env
```

Reference output:

- [pilot-runs/org-payment/phase4-s31-advisor-seeded-structuring-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s31-advisor-seeded-structuring-diagnostic-0001/summary.md)
- [pilot-runs/org-payment/phase4-s31-advisor-seeded-structuring-diagnostic-0001/aggregate.json](pilot-runs/org-payment/phase4-s31-advisor-seeded-structuring-diagnostic-0001/aggregate.json)
- [pilot-runs/org-payment/phase4-s31-advisor-seeded-structuring-diagnostic-0001/candidate-review-0001/summary.md](pilot-runs/org-payment/phase4-s31-advisor-seeded-structuring-diagnostic-0001/candidate-review-0001/summary.md)
- [docs/reflections/phase4-after-s31-advisor-seeded-structuring-review.md](docs/reflections/phase4-after-s31-advisor-seeded-structuring-review.md)
- [docs/synthesis/phase4-advisor-seeded-structuring-synthesis-v0.1.md](docs/synthesis/phase4-advisor-seeded-structuring-synthesis-v0.1.md)

Observed S31 result: 20 attempted / 17 accepted / 3 excluded. Advisor-generated split-like options appeared and seeded split options were present in 15/17 accepted applicant menus, but requester/buyer selected only canonical conservative options. S31 supports SL5 aggregate-gap preservation in accepted runs and does not add SL1, SL2, SL4, or SL6 support.

Checkpoint decision: do not repeat neutral advisor-seeded option expansion as-is. Any further Phase 4 run-producing work should begin with a new mechanism-selection and protocol-freeze checkpoint focused on option provenance or recommendation force.

### Phase 4 S32 Recommendation-Weighted Advisor Structuring Protocol

The S32 mechanism-selection reflection is recorded in [docs/reflections/phase4-after-s31-next-mechanism-selection.md](docs/reflections/phase4-after-s31-next-mechanism-selection.md).

The S32 protocol is frozen in [protocols/failure-modes/phase4-recommendation-weighted-advisor-structuring-diagnostic-v0.1.md](protocols/failure-modes/phase4-recommendation-weighted-advisor-structuring-diagnostic-v0.1.md), with scenario [scenarios/org-payment/s32-recommendation-weighted-advisor-structuring.yaml](scenarios/org-payment/s32-recommendation-weighted-advisor-structuring.yaml) and prompt addendum [prompts/org-payment/phase4-recommendation-weighted-advisor-structuring-addendum-v0.1.md](prompts/org-payment/phase4-recommendation-weighted-advisor-structuring-addendum-v0.1.md).

S32 is a protocol-freeze checkpoint only. It tests a mechanism distinct from S31: an operational advisor generates within-control options and marks one option as recommended with rationale and caveats, then requester/buyer chooses from a menu that includes canonical conservative options plus accepted advisor options and recommendation metadata. The recommendation is explicitly not approval, exception authority, final payment readiness, compliance clearance, or audit clearance.

The protocol freezes 20 future attempted runs across no-pressure, deadline-pressure, queue/volume-pressure, and compound-pressure/prior-practice conditions. It uses OpenAI `gpt-5.2`, includes no downstream accountant turn in v0.1, and preserves the claim boundary `phase4_recommendation_weighted_advisor_structuring_observation_only` for later execution.

This protocol does not execute runs and does not claim recommendation-weighted structuring occurred. It also does not claim fraud, hidden intent, full approval bypass, prompt causation, human behavior, real-world behavior, statistical significance, model-general behavior, or compliance/legal/audit/operational/governance/safety sufficiency.

### Phase 4 S33 Gray-Option Seeded Structuring Protocol

The S33 design-correction reflection is recorded in [docs/reflections/phase4-after-s32-design-correction-gray-option-selection.md](docs/reflections/phase4-after-s32-design-correction-gray-option-selection.md).

The S33 protocol is frozen in [protocols/failure-modes/phase4-gray-option-seeded-structuring-diagnostic-v0.1.md](protocols/failure-modes/phase4-gray-option-seeded-structuring-diagnostic-v0.1.md), with scenario [scenarios/org-payment/s33-gray-option-seeded-structuring.yaml](scenarios/org-payment/s33-gray-option-seeded-structuring.yaml) and prompt addendum [prompts/org-payment/phase4-gray-option-seeded-structuring-addendum-v0.1.md](prompts/org-payment/phase4-gray-option-seeded-structuring-addendum-v0.1.md).

S33 supersedes S32 for the immediate next execution path. S32 remains a frozen protocol artifact, but it is deferred before execution because an ordinary operational advisor is likely to recommend control-preserving handling. S33 instead introduces a gray-option ideation advisor that explicitly surfaces conservative and boundary-stretching within-control ideas, then deterministic filtering rejects outside-control options before requester/buyer selection.

The protocol freezes 20 future attempted runs across no-pressure, deadline-pressure, queue/volume-pressure, and compound-pressure/prior-practice conditions. It uses OpenAI `gpt-5.2`, includes no downstream accountant turn in v0.1, and preserves the claim boundary `phase4_gray_option_seeded_structuring_observation_only` for later execution.

This protocol does not execute runs and does not claim gray-option seeded structuring occurred. It also does not claim fraud, hidden intent, full approval bypass, prompt causation, human behavior, real-world behavior, statistical significance, model-general behavior, or compliance/legal/audit/operational/governance/safety sufficiency.

S33 execution is recorded in [pilot-runs/org-payment/phase4-s33-gray-option-seeded-structuring-diagnostic-0001/summary.md](pilot-runs/org-payment/phase4-s33-gray-option-seeded-structuring-diagnostic-0001/summary.md) and synthesized in [docs/synthesis/phase4-gray-option-seeded-structuring-synthesis-v0.1.md](docs/synthesis/phase4-gray-option-seeded-structuring-synthesis-v0.1.md).

Local execution command:

```powershell
$env:PYTHONPATH = "src"
python -m social_sim execute-phase4-gray-option-seeded-structuring-diagnostic `
  --output runs/org-payment/phase4-s33-gray-option-seeded-structuring-diagnostic-local/raw `
  --curated-output runs/org-payment/phase4-s33-gray-option-seeded-structuring-diagnostic-local/curated `
  --dotenv .env
```

Observed S33 result: 20 attempted / 19 accepted / 1 excluded provider failure. Gray split options were present in all 19 accepted runs. Requester/buyer selected conservative canonical actions in 18 accepted runs (`request_higher_approval`: 11, `submit_single_aggregate_request`: 7) and selected one gray-seeded split action with aggregate note in the compound-pressure/prior-practice condition. S33 adds one bounded SL2 candidate with SL5 aggregate-gap preservation, and does not add SL4 or SL6 support.
