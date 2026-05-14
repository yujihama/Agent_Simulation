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
| C01 | Research Concept | Specified | PR-A | PR-C | `docs/adr/ADR-0001-research-positioning.md`; `docs/research/03_working_rules_and_pr_policy.md` | Full framework draft is not yet imported; claim boundary still needs P7/P8 validation | PR-D: ODD-Social v0.1; later P7/P8 claim boundary |
| C02 | Research Questions | Draft | PR-C | PR-C | `docs/adr/ADR-0001-research-positioning.md` | RQ1-RQ5 are only recorded at positioning level | Follow-up research framework PR |
| C03 | Scope / Domain | Specified | PR-A | PR-C | `docs/adr/ADR-0003-initial-domain-org-payment.md`; `README.md` | Detailed domain boundary and scenario design are not yet introduced | PR-D / PR-E |
| C04 | ODD-Social | Specified | PR-P1P2 | PR-P1P2 | `protocols/odd-social/odd-social-v0.1.md`; `protocols/odd-social/odd-social-template.md` | Not dry-run tested; may need revision after evaluation protocols | P3 evaluation protocols, then P5 dry run |
| C05 | World / Environment | Specified | PR-P1P2 | PR-P1P2 | `protocols/odd-social/odd-social-v0.1.md`; `society/org-payment/organization.yaml`; scenario specs | State schema and trace contract are not yet defined | P3 evidence protocol; later P4 data contract |
| C06 | Institution Layer | Specified | PR-P1P2 | PR-P1P2 | `institutions/org-payment/policies.md`; `institutions/org-payment/control-modes.md` | Rule application examples and evidence recording are not yet defined | P3 evidence protocol; later P5 GM dry run |
| C07 | Population Layer | Specified | PR-P1P2 | PR-P1P2 | `society/org-payment/roles.yaml`; `society/org-payment/norms.yaml` | Role prompts and actor I/O are not yet defined | P4 LLM actor boundary PR |
| C08 | Interaction Layer | Specified | PR-P1P2 | PR-P1P2 | `society/org-payment/roles.yaml`; `society/org-payment/norms.yaml`; scenario specs | Interaction event coding is not yet defined | P3 event taxonomy PR |
| C09 | Game Master / Arbiter | Specified | PR-C | PR-C | `docs/adr/ADR-0002-game-master-architecture.md` | Concrete action proposal and decision data contracts are not yet specified | P4 Game Master boundary / data contract PR |
| C10 | LLM Actor Layer | Draft | PR-C | PR-C | `docs/adr/ADR-0002-game-master-architecture.md` | Actor I/O and provider-neutral adapter details are not yet specified | P4 LLM actor boundary PR |
| C11 | Scenario Matrix | Specified | PR-P1P2 | PR-P1P2 | `scenarios/org-payment/scenario-matrix.md`; S01-S06 scenario specs | Not dry-run tested; comparison strength may need revision | P3 evaluation protocols, then P5 dry run |
| C12 | Experiment Harness | Not started | none | PR-B | none | Manifest, seed policy, run isolation, and batch execution are not yet specified | P4 data contract / harness PR |
| C13 | Event Taxonomy | Not started | none | PR-B | none | Core event codebook is not yet introduced | P3 event taxonomy PR |
| C14 | Metrics | Not started | none | PR-B | none | Metrics are not yet specified | P3 metrics spec PR |
| C15 | Evidence Pack | Not started | none | PR-B | none | Evidence pack format is not yet specified | P3 evidence pack spec PR |
| C16 | Validity Protocol | Draft | PR-A | PR-C | `docs/adr/ADR-0001-research-positioning.md`; `docs/research/03_working_rules_and_pr_policy.md` | Face, pattern, intervention, construct, and sensitivity protocols are not yet specified | P3/P8 validity protocol PR |
| C17 | Human / LLM Review | Not started | none | PR-B | none | Human review and LLM-assisted review protocol are not yet specified | P3 human review protocol PR |
| C18 | Reporting / Claims | Draft | PR-A | PR-C | `docs/adr/ADR-0001-research-positioning.md`; `docs/research/03_working_rules_and_pr_policy.md` | Reporting format and claim boundary specs are not yet introduced | P7 claim boundary / reporting PR |
| C19 | Domain Expansion | Not started | none | PR-B | none | Second-domain selection criteria are not yet specified | P9 second-domain selection PR |
| C20 | Ethics / Misuse Boundaries | Draft | PR-A | PR-C | `docs/adr/ADR-0001-research-positioning.md`; `docs/adr/ADR-0003-initial-domain-org-payment.md`; `docs/glossary.md` | Ethics and misuse boundaries need a dedicated protocol before experiments | Dedicated ethics boundary or P3 review protocol PR |
