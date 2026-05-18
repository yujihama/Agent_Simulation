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
| LLM Actor | The layer that observes context, generates messages, and proposes actions for an artificial participant. It is not treated as a direct window into human intent. |
| Game Master / Arbiter | The layer that interprets proposed actions, applies world and institution rules, decides outcomes, records state changes, and preserves evidence. |
| Institution Layer | The environment-side definition of formal rules, informal norms, authority, audit rules, sanctions, and control modes. |
| Evidence pack | The structured record for a run, including manifest, trace, messages, actions, Game Master decisions, events, metrics, and review material. |
| Event taxonomy | The codebook for classifying observed social disorder, institutional failure, and communication breakdown events. |
| Metrics | Exploratory summaries derived from coded events, evidence completeness, and case outcomes. They do not by themselves establish real-world validity. |
| Human review | Human inspection of evidence packs, event labels, metrics, and claim strength. |
| LLM-assisted review | Optional review support from an LLM. It may suggest labels or evidence gaps but does not replace human acceptance. |
| Claim boundary | A rule for matching statement strength to evidence quality, from run observation through bounded claim and limitation. |
| Action proposal | A reviewable actor request for the Game Master / Arbiter to decide; it does not directly mutate world state. |
| Game Master decision | The record of how the Game Master / Arbiter applies rules, control mode, and state to an action proposal. |
| Trace record | An ordered run-level record that links messages, actions, decisions, events, metrics, and review notes. |
| Run manifest | The evidence-pack artifact that identifies protocol versions, contracts, artifacts, exclusions, and run mode. |
| Paper dry run | A manually authored non-LLM run used to test whether protocols fit together before implementation. |
| ODD-Social | A planned extension of the ODD protocol for describing artificial organizations, institution rules, social structure, and chaos factors. |
| Scenario matrix | A set of controlled comparison conditions that vary selected social and institutional variables. |
| Soft control | A control mode where a questionable action can proceed unless rejected by social or procedural friction. |
| Monitored control | A control mode where a questionable action can proceed but is detected, logged, or flagged for review. |
| Hard control | A control mode where the environment blocks an action that violates defined authority or policy. |
| Org-payment | The initial payment, procurement, and approval domain used as the first small artificial organization. |
| Within-Control Process Drift | Forward-looking term for process movement inside the ordinary control perimeter while approval, evidence, authority, or final-readiness conditions remain unresolved, ambiguous, weakened, preserved, or erased. It replaces intent as the scope axis. |
| Within-control | A scope classification where actors use their own assigned authority, system operation records match the actual operator, and evidence is not forged, hidden, modified, or fabricated. |
| Outside-control | A scope classification for impersonation, forged or hidden evidence, collusion, unauthorized access, privilege escalation, or malicious bypass. These are outside the current research scope unless a later protocol explicitly changes scope. |
| Environmental pressure condition | An observable scenario condition such as deadline pressure, queue-volume pressure, relationship pressure, or a frozen combination of them. It is used instead of hidden actor intent as an experimental condition. |
| Structuring / approval splitting | Splitting or sequencing requests, invoices, approvals, or handoffs. It is in scope when it remains within-control and out of scope when it depends on impersonation, forged evidence, concealment, collusion, or unauthorized access. |
