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
| C01 | Research Concept | Specified | PR-A | PR-P3 | `docs/adr/ADR-0001-research-positioning.md`; `docs/research/03_working_rules_and_pr_policy.md`; `protocols/evaluation/claim-boundaries-v0.1.md` | Full framework draft is not yet imported; claim boundary is specified but not validated | P5 dry run; later P7/P8 claim boundary validation |
| C02 | Research Questions | Draft | PR-C | PR-C | `docs/adr/ADR-0001-research-positioning.md` | RQ1-RQ5 are only recorded at positioning level | Follow-up research framework PR |
| C03 | Scope / Domain | Specified | PR-A | PR-P1P2 | `docs/adr/ADR-0003-initial-domain-org-payment.md`; `protocols/odd-social/odd-social-v0.1.md`; `scenarios/org-payment/scenario-matrix.md`; `README.md` | Scope is specified for the initial org-payment domain only; no second domain has been selected | P5 dry run; later P9 domain expansion |
| C04 | ODD-Social | Specified | PR-P1P2 | PR-P1P2 | `protocols/odd-social/odd-social-v0.1.md`; `protocols/odd-social/odd-social-template.md` | Not dry-run tested | P5 dry run |
| C05 | World / Environment | Specified | PR-P1P2 | PR-P1P2 | `protocols/odd-social/odd-social-v0.1.md`; `society/org-payment/organization.yaml`; scenario specs | State schema and trace contract are not yet defined | P4 data contract; P5 dry run |
| C06 | Institution Layer | Specified | PR-P1P2 | PR-P1P2 | `institutions/org-payment/policies.md`; `institutions/org-payment/control-modes.md` | Rule application examples are not yet dry-run tested | P5 GM dry run |
| C07 | Population Layer | Specified | PR-P1P2 | PR-P1P2 | `society/org-payment/roles.yaml`; `society/org-payment/norms.yaml` | Role prompts and actor I/O are not yet defined | P4 LLM actor boundary PR |
| C08 | Interaction Layer | Specified | PR-P1P2 | PR-P1P2 | `society/org-payment/roles.yaml`; `society/org-payment/norms.yaml`; scenario specs | Interaction event coding is specified but not dry-run tested | P5 dry run |
| C09 | Game Master / Arbiter | Specified | PR-C | PR-C | `docs/adr/ADR-0002-game-master-architecture.md` | Concrete action proposal and decision data contracts are not yet specified | P4 Game Master boundary / data contract PR |
| C10 | LLM Actor Layer | Draft | PR-C | PR-C | `docs/adr/ADR-0002-game-master-architecture.md` | Actor I/O and provider-neutral adapter details are not yet specified | P4 LLM actor boundary PR |
| C11 | Scenario Matrix | Specified | PR-P1P2 | PR-P1P2 | `scenarios/org-payment/scenario-matrix.md`; S01-S06 scenario specs | Not dry-run tested; comparison strength may need revision | P5 dry run |
| C12 | Experiment Harness | Not started | none | PR-B | none | Manifest, seed policy, run isolation, and batch execution are not yet specified | P4 data contract / harness PR |
| C13 | Event Taxonomy | Specified | PR-P3 | PR-P3 | `protocols/evaluation/event-taxonomy-v0.1.md` | Not dry-run coded; inter-reviewer reliability unknown | P5 dry coding and reconstruction check |
| C14 | Metrics | Specified | PR-P3 | PR-P3 | `protocols/evaluation/metrics-v0.1.md` | Metrics are not applied to runs; denominator choices need dry-run validation | P5 dry run; later P7 baseline reporting |
| C15 | Evidence Pack | Specified | PR-P3 | PR-P3 | `protocols/evaluation/evidence-pack-v0.1.md` | Layout is not schema-validated; reconstruction has not been tested | P4 data contract; P5 reconstruction check |
| C16 | Validity Protocol | Specified | PR-A | PR-P3 | `protocols/evaluation/evidence-pack-v0.1.md`; `protocols/evaluation/human-review-protocol-v0.1.md`; `protocols/evaluation/claim-boundaries-v0.1.md`; `docs/adr/ADR-0001-research-positioning.md` | Face, pattern, intervention, construct, and sensitivity checks are specified only at protocol boundary level and not executed | P5 dry run; later P8 validity review |
| C17 | Human / LLM Review | Specified | PR-P3 | PR-P3 | `protocols/evaluation/human-review-protocol-v0.1.md`; `protocols/evaluation/event-taxonomy-v0.1.md` | No reviewer agreement data; LLM-assisted review not piloted | P5 dry review |
| C18 | Reporting / Claims | Specified | PR-A | PR-P3 | `protocols/evaluation/claim-boundaries-v0.1.md`; `protocols/evaluation/metrics-v0.1.md`; `docs/research/03_working_rules_and_pr_policy.md` | Reporting template and baseline result examples are not yet introduced | P5 dry reporting; later P7 baseline reporting |
| C19 | Domain Expansion | Not started | none | PR-B | none | Second-domain selection criteria are not yet specified | P9 second-domain selection PR |
| C20 | Ethics / Misuse Boundaries | Specified | PR-A | PR-P3 | `protocols/evaluation/claim-boundaries-v0.1.md`; `protocols/evaluation/human-review-protocol-v0.1.md`; `docs/adr/ADR-0001-research-positioning.md`; `docs/glossary.md` | Misuse boundaries are specified for early reporting but not stress-tested during experiments | P5 dry run; revisit before experiment results |
