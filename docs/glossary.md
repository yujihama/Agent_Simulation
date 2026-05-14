# Glossary

Date: 2026-05-14
Status: accepted
Phase: P0
Step: PR-C
Covers: terminology for C01-C20
Supersedes: none
Related ADR: ADR-0001, ADR-0002, ADR-0003

This glossary keeps early project terms stable. It should stay concise; detailed protocol definitions belong in later protocol documents.

| Term | Meaning |
|---|---|
| Social chaos | A shorthand for social friction, confusion, responsibility diffusion, informal pressure, and institutional failure patterns in an artificial organization. It is not a claim that real society is fully reproduced. |
| Social friction | Misunderstanding, pressure, incentive conflict, informal norms, information asymmetry, and relationship effects that make institutional behavior unstable. |
| Institutional failure | A failure of rules, authority, approval, evidence, auditability, segregation of duties, or control mechanisms inside the artificial organization. |
| Artificial participant | An LLM-driven actor used to generate social behavior in the simulation. It is not treated as a complete substitute for a human. |
| LLM Actor | The layer that observes context, forms intent, generates messages, and proposes actions for an artificial participant. |
| Game Master / Arbiter | The layer that interprets proposed actions, applies world and institution rules, decides outcomes, records state changes, and preserves evidence. |
| Institution Layer | The environment-side definition of formal rules, informal norms, authority, audit rules, sanctions, and control modes. |
| Evidence pack | The structured record for a run, including manifest, trace, messages, actions, Game Master decisions, events, metrics, and review material. |
| Event taxonomy | The codebook for classifying observed social disorder, institutional failure, and communication breakdown events. |
| Metrics | Exploratory summaries derived from coded events, evidence completeness, and case outcomes. They do not by themselves establish real-world validity. |
| Human review | Human inspection of evidence packs, event labels, metrics, and claim strength. |
| LLM-assisted review | Optional review support from an LLM. It may suggest labels or evidence gaps but does not replace human acceptance. |
| Claim boundary | A rule for matching statement strength to evidence quality, from run observation through bounded claim and limitation. |
| ODD-Social | A planned extension of the ODD protocol for describing artificial organizations, institution rules, social structure, and chaos factors. |
| Scenario matrix | A set of controlled comparison conditions that vary selected social and institutional variables. |
| Soft control | A control mode where a questionable action can proceed unless rejected by social or procedural friction. |
| Monitored control | A control mode where a questionable action can proceed but is detected, logged, or flagged for review. |
| Hard control | A control mode where the environment blocks an action that violates defined authority or policy. |
| Org-payment | The initial payment, procurement, and approval domain used as the first small artificial organization. |
