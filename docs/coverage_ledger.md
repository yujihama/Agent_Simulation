# Coverage Ledger

Date: 2026-05-14
Status: accepted
Phase: P0
Step: PR-B
Covers: coverage tracking for C01-C20
Supersedes: none
Related ADR: none

This ledger is the source of truth for design coverage. It records which design components have been introduced, what evidence supports that status, which gaps remain, and which later PR should address them.

Status values follow the working rules: `Not started`, `Draft`, `Specified`, `Tried`, `Revised`, `Validated`, `Extended`, `Superseded`.

`Draft` in this initial ledger does not mean a substantive design specification is accepted. For PR-A, it means governance language exists and should guide future specifications.

| ID | Design area | Status | First covered by | Latest PR | Evidence | Remaining gaps | Next step |
|---|---|---|---|---|---|---|---|
| C01 | Research Concept | Specified | PR-A | PR-P10-synthesis-execution | `docs/adr/ADR-0001-research-positioning.md`; `docs/research/03_working_rules_and_pr_policy.md`; `protocols/evaluation/claim-boundaries-v0.1.md`; `protocols/synthesis/social-chaos-claim-synthesis-v0.1.md`; `docs/synthesis/social-chaos-claim-synthesis-v0.1.md` | Research concept is synthesized only as an artificial-system research position; no direct human society or real-organization claim is supported | Use synthesis as the bounded project-level research position |
| C02 | Research Questions | Specified | PR-C | PR-P10-synthesis-execution | `docs/adr/ADR-0001-research-positioning.md`; `protocols/synthesis/social-chaos-claim-synthesis-v0.1.md`; `docs/synthesis/social-chaos-claim-synthesis-v0.1.md`; `docs/synthesis/evidence-map.csv` | RQ-level findings remain bounded to artifact generation, reconstruction, reviewed representative evidence, and hypotheses for future validation | Add stronger RQ claims only after separately frozen validation work |
| C03 | Scope / Domain | Extended | PR-A | PR-P10-synthesis-execution | `docs/adr/ADR-0003-initial-domain-org-payment.md`; `docs/adr/ADR-0004-second-domain-expense-reimbursement.md`; `protocols/odd-social/odd-social-v0.1.md`; `scenarios/org-payment/scenario-matrix.md`; `scenarios/expense-reimbursement/er01-ambiguous-receipt-approval.yaml`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/summary.md`; `docs/synthesis/limitations.md`; `README.md` | Org-payment has the strongest artifact chain; expense reimbursement has one transfer pilot only; no cross-domain validation exists | Freeze additional second-domain protocols before any broader domain claim |
| C04 | ODD-Social | Tried | PR-P1P2 | PR-P4P5 | `protocols/odd-social/odd-social-v0.1.md`; `protocols/odd-social/odd-social-template.md`; `dry-runs/org-payment/s04-paper-dry-run/README.md` | Only one manually authored S04 paper dry run has tested the protocol fit | Implementation planning; later repeated dry runs |
| C05 | World / Environment | Tried | PR-P1P2 | PR-MethodBPlus-BC32-protocol | `protocols/odd-social/odd-social-v0.1.md`; `society/org-payment/organization.yaml`; `protocols/data-contracts/trace-record-contract-v0.1.md`; `schemas/trace-record.schema.json`; `src/social_sim/runner.py`; generated S04 evidence pack validation tests; `scenarios/org-payment/high-friction-scenario-matrix.md`; `scenarios/org-payment/s07-ambiguous-delegated-authority.yaml`; `scenarios/org-payment/s08-split-responsibility-deadline.yaml`; `scenarios/org-payment/s09-informal-pre-approval.yaml`; `scenarios/org-payment/s10-conflicting-policy-and-norm.yaml`; `scenarios/org-payment/s11-audit-visibility-workaround.yaml`; `scenarios/org-payment/s12-post-hoc-justification-setting.yaml`; `scenarios/org-payment/s13-ambiguous-approval-interpretation.yaml`; `scenarios/org-payment/s14-approval-bypass-stress.yaml`; `scenarios/org-payment/s15-responsibility-boundary-stress.yaml` | S15 specifies a responsibility-boundary stress environment for Method B+ targeting; no execution result or supported failure-mode finding is added | Execute BC32 only under the frozen responsibility-boundary protocol |
| C06 | Institution Layer | Tried | PR-P1P2 | PR-P4-skeleton | `institutions/org-payment/policies.md`; `institutions/org-payment/control-modes.md`; `protocols/data-contracts/gm-decision-contract-v0.1.md`; `schemas/gm-decision.schema.json`; `src/social_sim/game_master.py`; generated S04 validation tests | Rule application is deterministic and minimal for one S04 path; no general rule engine exists | Add GM rules only when additional scenarios require them |
| C07 | Population Layer | Specified | PR-P1P2 | PR-P1P2 | `society/org-payment/roles.yaml`; `society/org-payment/norms.yaml` | Role prompts and actor I/O are not yet defined | P4 LLM actor boundary PR |
| C08 | Interaction Layer | Tried | PR-P1P2 | PR-MethodBPlus-BC32-protocol | `society/org-payment/roles.yaml`; scenario specs; action proposal contracts and schemas; `protocols/baseline/multi-role-baseline-v0.1.md`; `results/org-payment/exp-0002-multi-role-baseline/summary.md`; `protocols/domain-expansion/expense-reimbursement-pilot-v0.1.md`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/aggregate.json`; `docs/synthesis/social-chaos-claim-synthesis-v0.1.md`; `scenarios/org-payment/high-friction-scenario-matrix.md`; `protocols/failure-modes/method-b-plus-ambiguity-interpretation-v0.1.md`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/aggregate.json`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/ambiguity-candidate-review-0001/summary.md`; `docs/reflections/method-b-plus-bc36-after-bc31-review.md`; `protocols/failure-modes/method-b-plus-approval-bypass-stress-v0.1.md`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/summary.md`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/candidate-review-0001/summary.md`; `docs/reflections/method-b-plus-bc36-after-bc37c-review.md`; `protocols/failure-modes/method-b-plus-responsibility-boundary-v0.1.md` | BC32 freezes buyer/approver/accountant responsibility-boundary interaction design before execution; no responsibility diffusion observation is added | Execute BC32 only after protocol freeze |
| C09 | Game Master / Arbiter | Tried | PR-C | PR-P8-baseline-execution | `docs/adr/ADR-0002-game-master-architecture.md`; Game Master contracts and schemas; `src/social_sim/game_master.py`; `protocols/baseline/multi-role-baseline-v0.1.md`; `results/org-payment/exp-0002-multi-role-baseline/aggregate.json` | Deterministic menu-aware GM decisions were recorded for all accepted EXP-0002 actions; no external adjudication or human review yet | Review whether any GM rule needs revision before stronger validity claims |
| C10 | LLM Actor Layer | Tried | PR-C | PR-MethodBPlus-BC32-protocol | `docs/adr/ADR-0002-game-master-architecture.md`; `schemas/action-proposal.schema.json`; role prompt templates; `src/social_sim/multi_role_baseline_runner.py`; EXP-0002 representative LLM prompt/output artifacts; `protocols/evaluation/exp-0004-provider-randomness-sensitivity-v0.1.md`; `results/org-payment/exp-0004-provider-randomness-sensitivity-0001/summary.md`; `prompts/expense-reimbursement/employee-claimant-action-v0.1.md`; `prompts/expense-reimbursement/manager-approval-action-v0.1.md`; `prompts/expense-reimbursement/finance-reviewer-action-v0.1.md`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/representative-evidence-packs/path-001/llm_outputs`; `docs/synthesis/limitations.md`; `prompts/org-payment/post-hoc-explanation-v0.1.md`; `protocols/failure-modes/multi-turn-memory-justification-pilot-v0.1.md`; `prompts/org-payment/method-b-diagnostic-role-local-framing-addendum-v0.1.md`; `src/social_sim/method_b_diagnostic_runner.py`; `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/representative-evidence-packs`; `prompts/org-payment/method-b-plus-ambiguity-interpretation-addendum-v0.1.md`; `src/social_sim/method_b_plus_ambiguity_runner.py`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/representative-evidence-packs`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/ambiguity-candidate-review-0001/summary.md`; `prompts/org-payment/method-b-plus-approval-bypass-stress-addendum-v0.1.md`; `src/social_sim/method_b_plus_approval_bypass_runner.py`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/representative-evidence-packs`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/candidate-review-0001/summary.md`; `prompts/org-payment/method-b-plus-responsibility-boundary-addendum-v0.1.md` | BC32 freezes a responsibility-boundary prompt addendum that asks roles to preserve decision ownership without instructing blame shifting; no prompt-causation or model-general behavior claim is supported | Execute BC32 and review generated candidates separately |
| C11 | Scenario Matrix | Tried | PR-P1P2 | PR-MethodBPlus-BC32-protocol | `scenarios/org-payment/scenario-matrix.md`; S01-S06 scenario specs; `protocols/baseline/multi-role-baseline-v0.1.md`; `results/org-payment/exp-0002-multi-role-baseline/scenario-summary.csv`; `protocols/evaluation/exp-0003-intervention-validity-stress-test-v0.1.md`; `results/org-payment/exp-0003-intervention-validity-stress-test-0001/contrast-table.csv`; `protocols/evaluation/exp-0004-provider-randomness-sensitivity-v0.1.md`; `results/org-payment/exp-0004-provider-randomness-sensitivity-0001/comparison-table.csv`; `scenarios/expense-reimbursement/er01-ambiguous-receipt-approval.yaml`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/scenario-summary.csv`; `docs/synthesis/evidence-map.csv`; `scenarios/org-payment/high-friction-scenario-matrix.md`; S07-S12 high-friction scenario specs; `scenarios/org-payment/s13-ambiguous-approval-interpretation.yaml`; `scenarios/org-payment/s14-approval-bypass-stress.yaml`; `scenarios/org-payment/s15-responsibility-boundary-stress.yaml` | S15 is a Method B+ targeted scenario, not a causal scenario-matrix result; it freezes responsibility-boundary conditions before execution | Execute targeted pilots before any scenario-effect reporting |
| C12 | Experiment Harness | Tried | PR-P4P5 | PR-MethodBPlus-BC37C-execution | run/trace contracts and schemas; `scripts/validate_evidence_pack.py`; `src/social_sim/m05_full_org_runner.py`; `src/social_sim/multi_role_baseline_runner.py`; `src/social_sim/sensitivity_runner.py`; `src/social_sim/expense_reimbursement_runner.py`; `tests/test_expense_reimbursement_pilot.py`; `results/org-payment/exp-0002-multi-role-baseline/aggregate.json`; `results/org-payment/exp-0004-provider-randomness-sensitivity-0001/aggregate.json`; `protocols/domain-expansion/expense-reimbursement-pilot-v0.1.md`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/aggregate.json`; `docs/synthesis/social-chaos-claim-synthesis-v0.1.md`; `src/social_sim/method_b_targeted_runner.py`; `src/social_sim/method_b_diagnostic_runner.py`; `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/aggregate.json`; `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/failure-mode-review-0001/baseline-execution-status.md`; `protocols/failure-modes/failure-mode-diagnostic-sensitivity-v0.1.md`; `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/aggregate.json`; `protocols/failure-modes/method-b-plus-ambiguity-interpretation-v0.1.md`; `src/social_sim/method_b_plus_ambiguity_runner.py`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/aggregate.json`; `src/social_sim/method_b_plus_approval_bypass_runner.py`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/aggregate.json` | BC37-C harness executed 5 attempted / 5 accepted / 0 excluded runs and wrote curated aggregate plus representative validated packs; raw output remains under ignored `runs/` | Review generated FM6 candidates before any supported status |
| C13 | Event Taxonomy | Revised | PR-P3 | PR-MethodBPlus-BC31-review | `protocols/evaluation/event-taxonomy-v0.1.md`; event record contract and schema; EXP-0002 representative `events.jsonl` files; `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/event-review-table.csv`; `results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/summary.md`; `results/org-payment/exp-0003-intervention-validity-stress-test-0001/aggregate.json`; `protocols/failure-modes/failure-mode-taxonomy-v0.1.md`; `scenarios/org-payment/high-friction-scenario-matrix.md`; `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/event-candidate-table.csv`; `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/failure-mode-review-0001/failure-mode-review-table.csv`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/event-candidate-table.csv`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/ambiguity-candidate-review-0001/candidate-review-table.csv` | BC31 review does not revise event taxonomy; the partial FM2 handoff observation remains a reviewed candidate-status result, not a new event type | Reflect before any taxonomy or status change |
| C14 | Metrics | Revised | PR-P3 | PR-MethodBPlus-BC31-review | `protocols/evaluation/metrics-v0.1.md`; `protocols/evaluation/pressure-citation-metric-correction-v0.1.md`; `protocols/evaluation/exp-0003-intervention-validity-stress-test-v0.1.md`; `protocols/evaluation/exp-0004-provider-randomness-sensitivity-v0.1.md`; corrected pressure-citation generation in `src/social_sim/m02_pressure_runner.py`, `src/social_sim/m04_full_role_runner.py`, and `src/social_sim/m05_full_org_runner.py`; `results/org-payment/exp-0004-provider-randomness-sensitivity-0001/aggregate.json`; `results/org-payment/exp-0004-provider-randomness-sensitivity-0001/comparison-table.csv`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/aggregate.json`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/scenario-summary.csv`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/ambiguity-candidate-review-0001/review-manifest.json` | BC31 review adds descriptive reviewed-status counts only; no inferential statistics, baseline metric, or full supported failure-mode metric is added | Use reviewed statuses only through BC36 reflection |
| C15 | Evidence Pack | Tried | PR-P3 | PR-MethodBPlus-BC37C-review | `protocols/evaluation/evidence-pack-v0.1.md`; data contracts; schemas; `scripts/validate_evidence_pack.py`; `results/org-payment/exp-0002-multi-role-baseline/representative-evidence-packs`; `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/pack-review-table.csv`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/representative-evidence-packs/path-001`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/representative-validation-outputs/path-001.md`; `docs/synthesis/social-chaos-claim-synthesis-v0.1.md`; `pilot-runs/org-payment/method-b-bc23-memory-justification-pilot-0001/representative-trace.jsonl`; `pilot-runs/org-payment/method-b-bc23-memory-justification-pilot-0001/post-hoc-explanations.jsonl`; `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/representative-evidence-packs`; `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/failure-mode-review-0001/pack-review-table.csv`; `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/representative-evidence-packs`; `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/representative-validation-outputs`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/method-b-transfer-review-0001/summary.md`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/representative-evidence-packs`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/representative-validation-outputs`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/ambiguity-candidate-review-0001/candidate-detail-notes.md`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/representative-evidence-packs`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/representative-validation-outputs`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/candidate-review-0001/candidate-detail-notes.md` | BC37-C representative evidence packs validate mechanically, and candidate review rejects both generated FM6 rows for the reviewed artificial evidence scope | Preserve reviewed rejection status until a new frozen pilot adds new evidence |
| C16 | Validity Protocol | Revised | PR-A | PR-MethodBPlus-BC32-protocol | evaluation protocols; `scripts/validate_evidence_pack.py`; `results/org-payment/exp-0002-multi-role-baseline/review.md`; `protocols/evaluation/exp-0002-human-evidence-review-v0.1.md`; `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md`; `protocols/evaluation/construct-validity-check-v0.1.md`; `results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/summary.md`; `protocols/evaluation/pressure-citation-metric-correction-v0.1.md`; `protocols/evaluation/exp-0003-intervention-validity-stress-test-v0.1.md`; `results/org-payment/exp-0003-intervention-validity-stress-test-0001/summary.md`; `protocols/evaluation/exp-0004-provider-randomness-sensitivity-v0.1.md`; `results/org-payment/exp-0004-provider-randomness-sensitivity-0001/review.md`; `protocols/domain-expansion/expense-reimbursement-pilot-v0.1.md`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/review.md`; `protocols/synthesis/social-chaos-claim-synthesis-v0.1.md`; `docs/synthesis/claim-boundary-review.md`; `protocols/failure-modes/failure-mode-taxonomy-v0.1.md`; `scenarios/org-payment/high-friction-scenario-matrix.md`; `protocols/failure-modes/multi-turn-memory-justification-pilot-v0.1.md`; `protocols/failure-modes/targeted-failure-mode-pilot-v0.1.md`; `protocols/failure-modes/method-b-failure-mode-review-v0.1.md`; `protocols/failure-modes/failure-mode-baseline-decision-v0.1.md`; `protocols/failure-modes/failure-mode-diagnostic-sensitivity-v0.1.md`; `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/reference-comparison.json`; `protocols/failure-modes/second-domain-failure-mode-transfer-v0.1.md`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/method-b-transfer-review-0001/construct-validity-notes.md`; `protocols/synthesis/method-b-synthesis-v0.1.md`; `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/fm6-candidate-review-0001/summary.md`; `docs/reflections/method-b-plus-bc36-after-fm6-review.md`; `protocols/failure-modes/method-b-plus-ambiguity-interpretation-v0.1.md`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/summary.md`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/event-candidate-table.csv`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/ambiguity-candidate-review-0001/summary.md`; `docs/reflections/method-b-plus-bc36-after-bc31-review.md`; `protocols/failure-modes/method-b-plus-approval-bypass-stress-v0.1.md`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/event-candidate-table.csv`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/candidate-review-0001/candidate-review-table.csv`; `docs/reflections/method-b-plus-bc36-after-bc37c-review.md`; `protocols/failure-modes/method-b-plus-responsibility-boundary-v0.1.md` | BC32 freezes reviewable criteria distinguishing ordinary role specialization from responsibility diffusion before execution | Execute and review BC32 without treating generated candidates as support |
| C17 | Human / LLM Review | Tried | PR-P3 | PR-MethodBPlus-BC37C-review | `protocols/evaluation/human-review-protocol-v0.1.md`; `protocols/evaluation/exp-0002-human-evidence-review-v0.1.md`; `results/org-payment/exp-0002-multi-role-baseline/llm-assisted-pre-review-0001/summary.md`; `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md`; `docs/synthesis/social-chaos-claim-synthesis-v0.1.md`; `docs/synthesis/limitations.md`; `protocols/failure-modes/failure-mode-taxonomy-v0.1.md`; `pilot-runs/org-payment/method-b-bc23-memory-justification-pilot-0001/review-checklist.md`; `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/human-pre-review-notes.md`; `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/failure-mode-review-0001/summary.md`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/method-b-transfer-review-0001/summary.md`; `docs/synthesis/method-b-synthesis-v0.1.md`; `docs/synthesis/method-b-failure-mode-status.csv`; `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/fm6-candidate-review-0001/fm6-candidate-review-table.csv`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/ambiguity-candidate-review-0001/candidate-review-table.csv`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/candidate-review-0001/candidate-review-table.csv` | Delegated BC37-C candidate review rejects both generated FM6 rows; this remains a single artificial evidence review, not an independent human review | Add independent review only through a separately frozen review protocol |
| C18 | Reporting / Claims | Revised | PR-A | PR-MethodBPlus-BC32-protocol | `protocols/evaluation/claim-boundaries-v0.1.md`; `protocols/baseline/multi-role-baseline-v0.1.md`; `results/org-payment/exp-0002-multi-role-baseline/review.md`; `results/org-payment/exp-0002-multi-role-baseline/human-review-0001/claim-boundary-review.md`; `results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/summary.md`; `protocols/evaluation/pressure-citation-metric-correction-v0.1.md`; `protocols/evaluation/exp-0003-intervention-validity-stress-test-v0.1.md`; `results/org-payment/exp-0003-intervention-validity-stress-test-0001/claim-boundary-review.md`; `protocols/evaluation/exp-0004-provider-randomness-sensitivity-v0.1.md`; `results/org-payment/exp-0004-provider-randomness-sensitivity-0001/claim-boundary-review.md`; `protocols/domain-expansion/expense-reimbursement-pilot-v0.1.md`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/claim-boundary-review.md`; `protocols/synthesis/social-chaos-claim-synthesis-v0.1.md`; `docs/synthesis/claim-boundary-review.md`; `docs/synthesis/evidence-map.csv`; `protocols/failure-modes/failure-mode-taxonomy-v0.1.md`; `scenarios/org-payment/high-friction-scenario-matrix.md`; `protocols/failure-modes/multi-turn-memory-justification-pilot-v0.1.md`; `pilot-runs/org-payment/method-b-bc23-memory-justification-pilot-0001/summary.md`; `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/claim-boundary-review.md`; `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/failure-mode-review-0001/claim-boundary-review.md`; `protocols/failure-modes/failure-mode-baseline-decision-v0.1.md`; `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/failure-mode-review-0001/baseline-execution-status.md`; `protocols/failure-modes/failure-mode-diagnostic-sensitivity-v0.1.md`; `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/summary.md`; `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/claim-boundary-review.md`; `protocols/failure-modes/second-domain-failure-mode-transfer-v0.1.md`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/method-b-transfer-review-0001/claim-boundary-review.md`; `docs/synthesis/method-b-synthesis-v0.1.md`; `docs/synthesis/method-b-claim-boundary-review.md`; `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/fm6-candidate-review-0001/claim-boundary-review.md`; `docs/reflections/method-b-plus-bc36-after-fm6-review.md`; `protocols/failure-modes/method-b-plus-ambiguity-interpretation-v0.1.md`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/summary.md`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/claim-boundary-review.md`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/ambiguity-candidate-review-0001/claim-boundary-review.md`; `docs/reflections/method-b-plus-bc36-after-bc31-review.md`; `protocols/failure-modes/method-b-plus-approval-bypass-stress-v0.1.md`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/summary.md`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/claim-boundary-review.md`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/candidate-review-0001/claim-boundary-review.md`; `docs/reflections/method-b-plus-bc36-after-bc37c-review.md`; `protocols/failure-modes/method-b-plus-responsibility-boundary-v0.1.md` | BC32 freezes artificial-system-only reporting boundaries and forbids treating normal role specialization as responsibility diffusion | Keep BC32 execution and review claims bounded to artificial evidence |
| C19 | Domain Expansion | Tried | PR-P10-second-domain-protocol | PR-MethodB-BC30 | `docs/adr/ADR-0004-second-domain-expense-reimbursement.md`; `scenarios/expense-reimbursement/README.md`; `scenarios/expense-reimbursement/er01-ambiguous-receipt-approval.yaml`; `protocols/domain-expansion/expense-reimbursement-pilot-v0.1.md`; `prompts/expense-reimbursement/employee-claimant-action-v0.1.md`; `prompts/expense-reimbursement/manager-approval-action-v0.1.md`; `prompts/expense-reimbursement/finance-reviewer-action-v0.1.md`; `src/social_sim/expense_reimbursement_runner.py`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/summary.md`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/review.md`; `docs/synthesis/limitations.md`; `protocols/failure-modes/second-domain-failure-mode-transfer-v0.1.md`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/method-b-transfer-review-0001/comparison-with-org-payment.md`; `docs/synthesis/method-b-synthesis-v0.1.md` | BC30 incorporates BC29: second-domain evidence does not support Method B transfer and cannot assess FM6 without post-hoc artifacts | Add a frozen second-domain post-hoc diagnostic before testing FM6 transfer |
| C20 | Ethics / Misuse Boundaries | Revised | PR-A | PR-MethodBPlus-BC32-protocol | `protocols/evaluation/claim-boundaries-v0.1.md`; `protocols/evaluation/human-review-protocol-v0.1.md`; `protocols/evaluation/exp-0002-human-evidence-review-v0.1.md`; `protocols/evaluation/construct-validity-check-v0.1.md`; `results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/limitations.md`; `protocols/evaluation/pressure-citation-metric-correction-v0.1.md`; `protocols/evaluation/exp-0003-intervention-validity-stress-test-v0.1.md`; `results/org-payment/exp-0003-intervention-validity-stress-test-0001/limitations.md`; `protocols/evaluation/exp-0004-provider-randomness-sensitivity-v0.1.md`; `results/org-payment/exp-0004-provider-randomness-sensitivity-0001/limitations.md`; `protocols/domain-expansion/expense-reimbursement-pilot-v0.1.md`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/limitations.md`; `protocols/synthesis/social-chaos-claim-synthesis-v0.1.md`; `docs/synthesis/limitations.md`; `docs/synthesis/claim-boundary-review.md`; `protocols/failure-modes/failure-mode-taxonomy-v0.1.md`; `scenarios/org-payment/high-friction-scenario-matrix.md`; `protocols/failure-modes/multi-turn-memory-justification-pilot-v0.1.md`; `prompts/org-payment/post-hoc-explanation-v0.1.md`; `protocols/failure-modes/targeted-failure-mode-pilot-v0.1.md`; `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/claim-boundary-review.md`; `pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/failure-mode-review-0001/claim-boundary-review.md`; `protocols/failure-modes/failure-mode-baseline-decision-v0.1.md`; `protocols/failure-modes/failure-mode-diagnostic-sensitivity-v0.1.md`; `prompts/org-payment/method-b-diagnostic-role-local-framing-addendum-v0.1.md`; `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/claim-boundary-review.md`; `protocols/failure-modes/second-domain-failure-mode-transfer-v0.1.md`; `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/method-b-transfer-review-0001/claim-boundary-review.md`; `docs/synthesis/method-b-claim-boundary-review.md`; `pilot-runs/org-payment/method-b-diagnostic-sensitivity-pilot-0001/fm6-candidate-review-0001/claim-boundary-review.md`; `docs/reflections/method-b-plus-bc36-after-fm6-review.md`; `protocols/failure-modes/method-b-plus-ambiguity-interpretation-v0.1.md`; `prompts/org-payment/method-b-plus-ambiguity-interpretation-addendum-v0.1.md`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/claim-boundary-review.md`; `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/ambiguity-candidate-review-0001/claim-boundary-review.md`; `docs/reflections/method-b-plus-bc36-after-bc31-review.md`; `protocols/failure-modes/method-b-plus-approval-bypass-stress-v0.1.md`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/claim-boundary-review.md`; `pilot-runs/org-payment/method-b-plus-approval-bypass-stress-pilot-0001/candidate-review-0001/claim-boundary-review.md`; `docs/reflections/method-b-plus-bc36-after-bc37c-review.md`; `protocols/failure-modes/method-b-plus-responsibility-boundary-v0.1.md` | BC32 protocol forbids prompting blame shifting, hidden responsibility, human behavior claims, real-world claims, or statistical claims | Preserve artificial-system-only boundaries through BC32 execution and review |

## Method B+ BC32 Execution Update

Latest PR label: `PR-MethodBPlus-BC32-execution`

This update applies to C08, C09, C10, C12, C13, C14, C15, C16, C17, C18, and C20.

Evidence added:

- `src/social_sim/method_b_plus_responsibility_runner.py`
- `tests/test_method_b_plus_responsibility_boundary_pilot.py`
- `pilot-runs/org-payment/method-b-plus-responsibility-boundary-pilot-0001/summary.md`
- `pilot-runs/org-payment/method-b-plus-responsibility-boundary-pilot-0001/aggregate.json`
- `pilot-runs/org-payment/method-b-plus-responsibility-boundary-pilot-0001/event-candidate-table.csv`
- `pilot-runs/org-payment/method-b-plus-responsibility-boundary-pilot-0001/claim-boundary-review.md`
- `pilot-runs/org-payment/method-b-plus-responsibility-boundary-pilot-0001/representative-evidence-packs/`
- `pilot-runs/org-payment/method-b-plus-responsibility-boundary-pilot-0001/representative-validation-outputs/`

Coverage impact:

- C08 Interaction Layer: BC32 buyer -> approver -> buyer -> accountant responsibility-boundary interaction was executed for 5 accepted S15 pilot runs.
- C09 Game Master / Arbiter: deterministic menu-aware decisions were recorded for all BC32 actions.
- C10 LLM Actor Layer: buyer, approver, accountant action turns and post-hoc explanation turns were generated through frozen prompts and addendum.
- C12 Experiment Harness: the BC32 runner generated 5 attempted / 5 accepted / 0 excluded evidence packs and curated aggregate artifacts; raw outputs remain under ignored `runs/`.
- C13 Event Taxonomy: no new event type was added; generated/proposed events remain bounded to existing taxonomy.
- C14 Metrics: BC32 descriptive metrics include action counts, responsibility-boundary flags, generated candidate/not-observed statuses, parser outcomes, and validation outcomes.
- C15 Evidence Pack: representative BC32 evidence packs validate mechanically.
- C16 Validity Protocol: generated candidate rows remain review inputs only; 0 candidate rows were generated in this execution.
- C17 Human / LLM Review: no independent human review is added; post-hoc explanation artifacts are LLM-generated and not human-reviewed coded evidence.
- C18 Reporting / Claims: BC32 reports only artificial-system pilot observations and not supported failure-mode findings.
- C20 Ethics / Misuse Boundaries: the result preserves no human behavior, real-world organization, prompt-causation, compliance, legal, audit, operational sufficiency, or statistical claim.

Remaining gaps:

- BC32 has no supported FM1/FM2/FM5/FM6 finding. The run produced `not_observed` statuses for all four reviewed modes by generated heuristic.
- Because there are 0 generated candidate rows, the next checkpoint should record a BC36-style reflection rather than a candidate review.

## Method B+ BC36 Reflection After BC32 Update

Latest PR label: `PR-MethodBPlus-BC36-after-BC32`

Evidence added:

- `docs/reflections/method-b-plus-bc36-after-bc32-execution.md`

Coverage impact:

- C16 Validity Protocol: BC32 is classified as `no candidate / not observed`, and the reflection chooses a new target rather than repeating the same responsibility-boundary setup.
- C18 Reporting / Claims: the reflection keeps BC32 bounded to artificial-system pilot accounting and does not upgrade any generated status to support.
- C20 Ethics / Misuse Boundaries: the reflection explicitly forbids human, real-world, prompt-causation, compliance, legal, audit, operational, and statistical claims.

Next step:

- Freeze BC35 evidence-gap erasure diagnostic before any BC35 execution.

## Method B+ BC35 Protocol Freeze Update

Latest PR label: `PR-MethodBPlus-BC35-protocol`

Evidence added:

- `protocols/failure-modes/method-b-plus-evidence-gap-erasure-diagnostic-v0.1.md`
- `scenarios/org-payment/s16-evidence-gap-erasure-diagnostic.yaml`
- `prompts/org-payment/method-b-plus-evidence-gap-erasure-addendum-v0.1.md`

Coverage impact:

- C05 World / Environment: S16 freezes an evidence-gap diagnostic environment with `G001` explicit approval missing and `G002` service acceptance evidence missing.
- C08 Interaction Layer: BC35 freezes the buyer handoff and accountant evidence-review surface before execution.
- C10 LLM Actor Layer: BC35 freezes an evidence-gap addendum that asks actors to preserve known gaps without instructing unsafe behavior.
- C12 Experiment Harness: no execution is added; the later execution PR must generate raw outputs under ignored `runs/` and commit only curated artifacts.
- C14 Metrics: BC35 freezes descriptive reporting for gap preservation, FM5/FM2/FM6 generated statuses, parser outcomes, GM outcomes, and validation outcomes.
- C16 Validity Protocol: generated candidates remain review inputs only; supported status is reserved for a later review PR.
- C18 Reporting / Claims: BC35 allows only artificial-system diagnostic observations after execution.
- C20 Ethics / Misuse Boundaries: the protocol forbids instructing evidence erasure, approval bypass, or claims about humans, real organizations, prompt causation, compliance, legal, audit, operational sufficiency, or statistics.

Remaining gaps:

- BC35 has not been executed.
- No FM5 evidence-gap-erasure candidate or support is added by this protocol-freeze update.

## Method B+ BC35 Execution Update

Latest PR label: `PR-MethodBPlus-BC35-execution`

This update applies to C08, C09, C10, C12, C13, C14, C15, C16, C17, C18, and C20.

Evidence added:

- `src/social_sim/method_b_plus_evidence_gap_runner.py`
- `tests/test_method_b_plus_evidence_gap_diagnostic_pilot.py`
- `pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/summary.md`
- `pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/aggregate.json`
- `pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/event-candidate-table.csv`
- `pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/claim-boundary-review.md`
- `pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/representative-evidence-packs/`
- `pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/representative-validation-outputs/`

Coverage impact:

- C08 Interaction Layer: BC35 buyer accounting-handoff and accountant evidence-review interaction was executed for 5 accepted S16 diagnostic runs.
- C09 Game Master / Arbiter: deterministic menu-aware decisions were recorded for all BC35 actions and preserved the distinction between unresolved G001/G002 gaps and explicit approval.
- C10 LLM Actor Layer: buyer/accountant action turns and post-hoc explanation turns were generated through frozen prompts and the BC35 evidence-gap addendum.
- C12 Experiment Harness: the BC35 runner generated 5 attempted / 5 accepted / 0 excluded evidence packs and curated aggregate artifacts; raw outputs remain under ignored `runs/`.
- C13 Event Taxonomy: no new event type was added; generated/proposed events remain bounded to existing taxonomy.
- C14 Metrics: BC35 descriptive metrics include G001/G002 preservation flags, approval-bypass level counts, generated candidate/not-observed statuses, parser outcomes, GM outcomes, and validation outcomes.
- C15 Evidence Pack: representative BC35 evidence packs validate mechanically.
- C16 Validity Protocol: generated candidate rows remain review inputs only; BC35 produced 3 FM6 candidate rows and 0 FM5 candidate rows by the generated heuristic.
- C17 Human / LLM Review: no independent human review is added; post-hoc explanation artifacts are LLM-generated and not human-reviewed coded evidence.
- C18 Reporting / Claims: BC35 reports only artificial-system diagnostic observations and not supported failure-mode findings.
- C20 Ethics / Misuse Boundaries: the result preserves no human behavior, real-world organization, prompt-causation, compliance, legal, audit, operational sufficiency, or statistical claim.

Remaining gaps:

- BC35 has no supported FM5 evidence-gap-erasure finding. The generated heuristic marked FM5 `not_observed` in all 5 runs.
- The 3 generated FM6 rows are candidates only and require a separate review before any supported, partially supported, rejected, or needs-revision status can be recorded.

## Method B+ BC35 Candidate Review Update

Latest PR label: `PR-MethodBPlus-BC35-FM6-review`

This update applies to C16, C17, C18, and C20.

Evidence added:

- `pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/candidate-review-0001/summary.md`
- `pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/candidate-review-0001/candidate-review-table.csv`
- `pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/candidate-review-0001/candidate-detail-notes.md`
- `pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/candidate-review-0001/claim-boundary-review.md`
- `pilot-runs/org-payment/method-b-plus-evidence-gap-erasure-diagnostic-pilot-0001/candidate-review-0001/review-manifest.json`

Coverage impact:

- C16 Validity Protocol: the three generated BC35 FM6 candidate rows were reviewed against the frozen FM6 definition without adding runs or changing definitions.
- C17 Human / LLM Review: delegated review rejects all three generated FM6 rows for the reviewed artificial evidence scope; this remains a delegated review, not independent human review.
- C18 Reporting / Claims: BC35 candidate review records `reviewed_rejected: 3` and no supported or partially supported FM6 finding.
- C20 Ethics / Misuse Boundaries: the review preserves no human behavior, real-world organization, prompt-causation, compliance, legal, audit, operational sufficiency, or statistical claim.

Remaining gaps:

- BC35 has no supported FM2, FM5, or FM6 finding after review.
- A BC36-style reflection should decide whether to revise the evidence-gap diagnostic surface, shift to another Method B+ target, or add independent human review before further targeted execution.

## Method B+ BC36 Reflection After BC35 Review Update

Latest PR label: `PR-MethodBPlus-BC36-after-BC35`

This update applies to C16, C18, and C20.

Evidence added:

- `docs/reflections/method-b-plus-bc36-after-bc35-review.md`

Coverage impact:

- C16 Validity Protocol: BC35 is classified as `candidateあり、reviewでrejected` plus `no candidate / not observed` for the primary FM5 target, and the reflection selects synthesis rather than immediate repeated execution.
- C18 Reporting / Claims: the reflection keeps BC35 bounded to artificial-system pilot accounting and does not upgrade any generated or rejected candidate to support.
- C20 Ethics / Misuse Boundaries: the reflection explicitly forbids human, real-world, prompt-causation, model-general, compliance, legal, audit, operational, and statistical claims.

Next step:

- Add a Method B+ iterative targeting synthesis before any new targeted protocol freeze.

## Method B+ Iterative Targeting Synthesis Update

Latest PR label: `PR-MethodBPlus-iterative-synthesis`

This update applies to C01, C02, C16, C17, C18, and C20.

Evidence added:

- `docs/synthesis/method-b-plus-iterative-targeting-synthesis-v0.1.md`
- `docs/synthesis/method-b-plus-failure-mode-status.csv`
- `docs/synthesis/method-b-plus-claim-boundary-review.md`

Coverage impact:

- C01 Research Concept: Method B+ is synthesized as bounded artificial-system failure-mode targeting, not human society reproduction.
- C02 Research Questions: Method B+ status is summarized as workflow progress plus one narrow partial FM2 boundary observation, not full failure-mode support.
- C16 Validity Protocol: generated, reviewed rejected, partially supported, and not-observed statuses are separated in a compact table.
- C17 Human / LLM Review: delegated review scope is documented; no independent multi-reviewer human validation or inter-rater reliability claim is added.
- C18 Reporting / Claims: the synthesis explicitly forbids baseline, statistical, real-world, prompt-causation, and human behavior claims from Method B+ evidence.
- C20 Ethics / Misuse Boundaries: the synthesis preserves artificial-system-only, non-operational, non-compliance, non-legal, and non-audit boundaries.

Remaining gaps:

- Method B+ should not proceed to a controlled baseline from current evidence.
- Stronger claims require either independent review of the BC31 partial FM2 boundary observation or a separately frozen protocol targeting a clearly different mechanism.

## Method B+ BC31 FM2 Independent Review Update

Latest PR label: `PR-MethodBPlus-BC31-FM2-independent-review`

This update applies to C16, C17, C18, and C20.

Evidence added:

- `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/bc31-fm2-independent-review-0001/summary.md`
- `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/bc31-fm2-independent-review-0001/review-table.csv`
- `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/bc31-fm2-independent-review-0001/evidence-notes.md`
- `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/bc31-fm2-independent-review-0001/claim-boundary-review.md`
- `pilot-runs/org-payment/method-b-plus-ambiguity-targeting-pilot-0001/bc31-fm2-independent-review-0001/review-manifest.json`

Coverage impact:

- C16 Validity Protocol: BC31 candidate `BC31-CAND-002` was independently re-reviewed against the existing FM2 taxonomy without adding runs or changing definitions.
- C17 Human / LLM Review: the second-pass proxy review confirms the prior partial-support classification for the narrow buyer handoff boundary only; it is still not independent multi-reviewer human validation.
- C18 Reporting / Claims: Method B+ may report `partially_supported_needs_revision_confirmed` for the BC31 buyer handoff boundary, but not full approval bypass, accountant payment preparation, or final payment readiness.
- C20 Ethics / Misuse Boundaries: the review preserves no human behavior, real-world organization, prompt-causation, model-general, compliance, legal, audit, operational sufficiency, or statistical claim.

Remaining gaps:

- BC31 FM2 remains a narrow partial support item, not a baseline-ready failure-mode finding.
- Stronger reviewed-evidence status would require an external or project-owner human-review protocol, or a new frozen protocol that separately tests buyer handoff, accountant preparation, and final-state payment readiness.

## Method B+ Control Slippage Reframing Update

Latest PR label: `PR-MethodBPlus-control-slippage-taxonomy`

This update applies to C13, C16, C17, C18, and C20.

Evidence added:

- `docs/reflections/method-b-plus-bc36-after-bc31-fm2-independent-review.md`
- `protocols/failure-modes/non-intentional-control-slippage-taxonomy-v0.1.md`
- `docs/synthesis/non-intentional-control-slippage-map.csv`

Coverage impact:

- C13 Event Taxonomy / Failure-Mode Vocabulary: the project adds non-intentional control slippage as a higher-level review vocabulary that separates SL2 handoff, SL3 preparation, SL4 final readiness, SL5 gap preservation, and SL6 gap erasure.
- C16 Validity Protocol: BC31 FM2 is reframed without upgrading it; the confirmed support remains narrow SL2 plus SL5, with SL3 and SL4 not supported.
- C17 Human / LLM Review: the mapping preserves reviewed, generated, partial, not-observed, and not-applicable scopes; no independent multi-reviewer human validation is added.
- C18 Reporting / Claims: the synthesis now describes the strongest Method B+ signal as non-intentional control slippage rather than full approval bypass.
- C20 Ethics / Misuse Boundaries: the taxonomy explicitly excludes fraud, forged approval, concealment, collusion, malicious bypass, fabricated evidence, human behavior, real-world organization, model-general, compliance, legal, audit, operational, and statistical claims.

Remaining gaps:

- No SL3 or SL4 evidence exists.
- At the control-slippage reframing checkpoint, the next executable path was to freeze an `SL2 -> SL3 -> SL4` progression diagnostic; the following update records that protocol freeze.

## Method B+ SL2-SL4 Control Slippage Progression Protocol Update

Latest PR label: `PR-MethodBPlus-control-slippage-progression-protocol`

This update applies to C05, C08, C10, C12, C13, C16, C17, C18, and C20.

Evidence added:

- `protocols/failure-modes/method-b-plus-control-slippage-progression-diagnostic-v0.1.md`
- `scenarios/org-payment/s17-control-slippage-progression-diagnostic.yaml`
- `prompts/org-payment/method-b-plus-control-slippage-progression-addendum-v0.1.md`

Coverage impact:

- C05 World / Environment: S17 freezes unresolved approval, exception-authority, and final-readiness gaps for a future control-slippage progression diagnostic.
- C08 Interaction Layer: the protocol freezes buyer accounting-handoff and accountant control-review surfaces before execution.
- C10 LLM Actor Layer: the control-slippage addendum asks roles to preserve and cite control gaps without instructing bypass, gap erasure, or risky action.
- C12 Experiment Harness: no execution is added; the later execution PR must generate raw outputs under ignored `runs/` and commit only curated artifacts.
- C13 Event Taxonomy / Failure-Mode Vocabulary: SL2, SL3, SL4, SL5, and SL6 candidate/not-observed accounting is frozen without adding new event types.
- C16 Validity Protocol: generated slippage candidates remain review inputs only, and SL2 handoff must not be collapsed into SL3 preparation or SL4 final readiness.
- C17 Human / LLM Review: no human review or supported finding is added.
- C18 Reporting / Claims: the protocol allows only future artificial-system diagnostic observations after execution.
- C20 Ethics / Misuse Boundaries: the protocol forbids fraud, intentional misconduct, human, real-world, model-general, prompt-causation, compliance, legal, audit, operational, and statistical claims.

Remaining gaps:

- At this protocol-freeze checkpoint, S17 had not yet been executed; the following update records the later execution and review.
- No SL3, SL4, SL6, or full approval-bypass evidence is added by this protocol-freeze update.

## Method B+ SL2-SL4 Control Slippage Progression Execution And Review Update

Latest PR label: `PR-MethodBPlus-control-slippage-progression-execution-review`

This update applies to C08, C10, C12, C13, C14, C15, C16, C17, C18, and C20.

Evidence added:

- `src/social_sim/method_b_plus_control_slippage_runner.py`
- `tests/test_method_b_plus_control_slippage_progression_pilot.py`
- `pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/summary.md`
- `pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/aggregate.json`
- `pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/execution-manifest.json`
- `pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/event-candidate-table.csv`
- `pilot-runs/org-payment/method-b-plus-control-slippage-progression-diagnostic-pilot-0001/candidate-review-0001/summary.md`
- `docs/reflections/method-b-plus-bc36-after-slippage-progression-review.md`
- `docs/synthesis/method-b-plus-iterative-targeting-synthesis-v0.1.md`
- `docs/synthesis/method-b-plus-failure-mode-status.csv`
- `docs/synthesis/non-intentional-control-slippage-map.csv`
- `docs/synthesis/method-b-plus-claim-boundary-review.md`

Coverage impact:

- C08 Interaction Layer: S17 executed the frozen buyer accounting-handoff and accountant control-review interaction path without changing the frozen protocol.
- C10 LLM Actor Layer: buyer and accountant were the only LLM-controlled action turns; post-hoc explanations were generated as explanation artifacts only.
- C12 Experiment Harness: the new command executed 5 attempted / 5 accepted / 0 excluded runs, with raw outputs under ignored `runs/` and curated artifacts under `pilot-runs/`.
- C13 Event Taxonomy / Failure-Mode Vocabulary: SL2, SL3, SL4, SL5, SL6, and FM6 are reported separately without adding new event types.
- C14 Metrics: aggregate reporting separates action counts, path counts, parser outcomes, GM decisions, validation status, unresolved gap status, and SL/FM candidate or observed status.
- C15 Evidence Pack: representative S17 evidence packs validate mechanically and include action menus, parser results, proposal attempts, post-hoc explanations, trace, events, metrics, reviewer notes, and reconstruction checklists.
- C16 Validity Protocol: generated rows are reviewed in `candidate-review-0001`; SL2 handoff is not collapsed into SL3 preparation or SL4 final readiness.
- C17 Human / LLM Review: Codex proxy review under project-owner authorization records SL5 as supported for reviewed artificial evidence and records SL2/SL3/SL4/SL6/FM6 as not observed; this is not independent multi-reviewer human validation.
- C18 Reporting / Claims: the reflection selects pause-and-synthesize rather than baseline execution, preserving the artificial-evidence-only claim boundary.
- C20 Ethics / Misuse Boundaries: no human behavior, real-world organization, prompt-causation, model-general, fraud, compliance, legal, audit, operational, or statistical claim is added.

Observed S17 result:

- Buyer selected `hold_payment` in all 5 accepted runs.
- Accountant selected `hold_payment` in all 5 accepted runs.
- SL2, SL3, SL4, SL6, and FM6 were not observed.
- SL5 evidence-gap preservation was supported for the reviewed artificial evidence.

Remaining gaps:

- S17 does not extend the BC31 narrow SL2 observation.
- No SL3 payment-preparation or SL4 final payment-ready evidence exists.
- The project should not freeze a Method B+ controlled baseline from the current evidence.

## Method B+ Boundary Preservation Synthesis Update

Latest PR label: `PR-MethodBPlus-boundary-preservation-synthesis`

This update applies to C01, C02, C16, C18, and C20.

Evidence added:

- `docs/synthesis/method-b-plus-boundary-preservation-synthesis-v0.1.md`

Coverage impact:

- C01 Research Concept: Method B+ conservative outcomes are synthesized as an artificial-system boundary-preservation result, not as a failed search hidden from the record.
- C02 Research Questions: the synthesis clarifies that the current question has shifted from "why no failure mode appeared" to "which artificial setup features preserve approval and evidence boundaries."
- C16 Validity Protocol: BC31 narrow SL2 partial support, repeated SL5 preservation, and unsupported SL3/SL4/SL6/FM6 statuses are separated before any new mechanism is selected.
- C18 Reporting / Claims: the synthesis permits only bounded artificial-environment claims about explicit gaps and hold/request-evidence options; it does not claim real-world control effectiveness.
- C20 Ethics / Misuse Boundaries: the document explicitly forbids human behavior, real-world organization, prompt-causation, model-general, compliance, legal, audit, operational, and statistical claims.

Remaining gaps:

- The synthesis does not select or freeze a new mechanism.
- Future work should choose a genuinely different information mechanism, such as lossy handoff or role-local context, before any additional execution.

## Method B+ Next Mechanism Selection Update

Latest PR label: `PR-MethodBPlus-next-mechanism-selection`

This update applies to C01, C02, C08, C16, C18, and C20.

Evidence added:

- `docs/reflections/method-b-plus-next-mechanism-selection.md`

Coverage impact:

- C01 Research Concept: Method B+ advances from repeated stress targeting toward mechanism-level information-transfer diagnostics.
- C02 Research Questions: the next question is narrowed to whether a known approval gap remains visible after a compressed buyer-to-accountant handoff.
- C08 Interaction Layer: lossy handoff is selected as the next interaction mechanism, but no scenario, prompt, or run is added yet.
- C16 Validity Protocol: the reflection requires the future protocol to distinguish global truth, role-local view, handoff artifact, candidate status, and reviewed support.
- C18 Reporting / Claims: the reflection allows only a planning claim that lossy handoff was selected; it does not claim slippage or approval bypass.
- C20 Ethics / Misuse Boundaries: the selected mechanism forbids instructing bypass, concealment, fabrication, human behavior claims, real-world claims, prompt-causation claims, model-general claims, compliance/legal/audit/operational claims, or statistical claims.

Remaining gaps:

- Lossy handoff is selected but not frozen as a protocol.
- No S18 scenario, prompt addendum, action menus, Game Master rules, candidate rules, evidence requirements, or review criteria have been frozen yet.

## Method B+ Lossy Handoff Protocol Freeze Update

Latest PR label: `PR-MethodBPlus-lossy-handoff-protocol`

This update applies to C05, C08, C10, C12, C13, C16, C17, C18, and C20.

Evidence added:

- `protocols/failure-modes/method-b-plus-lossy-handoff-diagnostic-v0.1.md`
- `scenarios/org-payment/s18-lossy-handoff-control-slippage.yaml`
- `prompts/org-payment/method-b-plus-lossy-handoff-addendum-v0.1.md`

Coverage impact:

- C05 World / Environment: S18 freezes a lossy-handoff diagnostic environment with unresolved G001/G002/G003 gaps, buyer global visibility, and accountant local-packet visibility.
- C08 Interaction Layer: the protocol freezes buyer lossy handoff and accountant local review before execution.
- C10 LLM Actor Layer: the addendum instructs roles to use only visible records, preserve source refs, and avoid fabricating or hiding approval evidence; it does not instruct risky behavior.
- C12 Experiment Harness: no execution is added; the later execution PR must write raw outputs under ignored `runs/` and commit only curated artifacts.
- C13 Event Taxonomy / Failure-Mode Vocabulary: the protocol separates SL2, SL3, SL4, SL5, SL6, FM1, FM3, and FM6 candidate criteria without adding new event types.
- C16 Validity Protocol: future candidate classification must record global truth, buyer full view, handoff packet, accountant local view, and Game Master decisions separately.
- C17 Human / LLM Review: no review result is added; future generated candidates remain review inputs only.
- C18 Reporting / Claims: the protocol permits only future artificial diagnostic observations after execution and forbids claiming slippage before review.
- C20 Ethics / Misuse Boundaries: the protocol forbids fraud, intentional misconduct, concealment, fabricated evidence, human behavior, real-world organization, model-general, prompt-causation, compliance, legal, audit, operational, and statistical claims.

Remaining gaps:

- S18 has not been executed.
- No lossy handoff candidate, reviewed support, or boundary-preserving result is added by this protocol-freeze update.

## Method B+ Lossy Handoff Execution And Review Update

Latest PR label: `PR-MethodBPlus-lossy-handoff-execution-review`

This update applies to C08, C10, C12, C13, C14, C15, C16, C17, C18, and C20.

Evidence added:

- `src/social_sim/method_b_plus_lossy_handoff_runner.py`
- `tests/test_method_b_plus_lossy_handoff_pilot.py`
- `pilot-runs/org-payment/method-b-plus-lossy-handoff-diagnostic-pilot-0001/summary.md`
- `pilot-runs/org-payment/method-b-plus-lossy-handoff-diagnostic-pilot-0001/aggregate.json`
- `pilot-runs/org-payment/method-b-plus-lossy-handoff-diagnostic-pilot-0001/execution-manifest.json`
- `pilot-runs/org-payment/method-b-plus-lossy-handoff-diagnostic-pilot-0001/event-candidate-table.csv`
- `pilot-runs/org-payment/method-b-plus-lossy-handoff-diagnostic-pilot-0001/candidate-review-0001/summary.md`
- `docs/reflections/method-b-plus-bc36-after-lossy-handoff-review.md`
- `docs/synthesis/method-b-plus-iterative-targeting-synthesis-v0.1.md`
- `docs/synthesis/method-b-plus-failure-mode-status.csv`
- `docs/synthesis/non-intentional-control-slippage-map.csv`
- `docs/synthesis/method-b-plus-claim-boundary-review.md`

Coverage impact:

- C08 Interaction Layer: S18 executed the frozen buyer lossy-handoff and accountant local-review interaction path without changing the frozen protocol.
- C10 LLM Actor Layer: buyer and accountant were the only LLM-controlled action turns; post-hoc explanations were generated as explanation artifacts only.
- C12 Experiment Harness: the new command executed 5 attempted / 5 accepted / 0 excluded runs, with raw outputs under ignored `runs/` and curated artifacts under `pilot-runs/`.
- C13 Event Taxonomy / Failure-Mode Vocabulary: SL2, SL3, SL4, SL5, SL6, FM1, FM3, and FM6 are reported separately without adding new event types.
- C14 Metrics: aggregate reporting separates handoff condition counts, action counts, path counts, parser outcomes, GM decisions, validation status, role-local preservation, and candidate or observed status.
- C15 Evidence Pack: representative S18 evidence packs validate mechanically and include role views, handoff summaries, action menus, parser results, proposal attempts, post-hoc explanations, trace, events, metrics, reviewer notes, and reconstruction checklists.
- C16 Validity Protocol: generated rows are reviewed in `candidate-review-0001`; SL2 handoff is not collapsed into SL3 preparation or SL4 final readiness.
- C17 Human / LLM Review: Codex proxy review under project-owner authorization records SL2 and SL5 as supported for reviewed artificial evidence and records SL3/SL4/SL6/FM1/FM3/FM6 as not observed; this is not independent multi-reviewer human validation.
- C18 Reporting / Claims: the reflection selects mechanism synthesis rather than baseline execution, preserving artificial-evidence-only claim boundaries.
- C20 Ethics / Misuse Boundaries: no human behavior, real-world organization, prompt-causation, model-general, causation, fraud, compliance, legal, audit, operational, or statistical claim is added.

Observed S18 result:

- Buyer selected `submit_payment_request` in 3 accepted runs and `hold_payment` in 2 accepted runs.
- Accountant selected `hold_payment` in all 5 accepted runs.
- SL2 buyer payment-forward handoff and SL5 evidence-gap preservation were supported for reviewed artificial evidence.
- SL3, SL4, SL6, FM1, FM3, and FM6 were not observed.

Remaining gaps:

- S18 does not support accountant payment preparation, final payment readiness, evidence-gap erasure, responsibility diffusion, ambiguous-guidance misinterpretation, or post-hoc justification.
- The result does not justify a controlled failure-mode baseline from SL2 alone.
