# ADR-0001: Research Positioning

Date: 2026-05-14
Status: accepted
Phase: P0
Step: PR-C
Covers: C01; positioning context for C02, C16, C18, C20
Supersedes: none
Related ADR: none

## Context

The project began from observations in an LLM-agent payment and approval sandbox: duplicate payments, approval bypasses, self-approval, missing audit logs, handler confusion, inconsistent amounts, and corrupted state files.

Those observations are useful, but they are not sufficient as a research foundation. Without clearer boundaries, failures can be caused by prompt design, missing authority checks, model behavior, implementation bugs, or ambiguous institutional rules. The project therefore needs an explicit research position before adding protocols, scenarios, or code.

Source drafts not yet imported into this repository:

- `research_history_and_rationale.md`
- `research_framework_design.md`
- `phase_step_checkpoint_coverage_plan.md`

## Decision

This project studies artificial social simulations of institutional friction and failure. LLM agents are used as artificial participants that can generate social friction, misunderstanding, justification, pressure response, responsibility diffusion, and norm drift.

The project does not treat LLM agents as complete human substitutes and does not claim direct prediction of real human society.

The research should be framed as:

> Using LLM agents as artificial participants, explore how ambiguity, pressure, incentives, informal norms, information asymmetry, and responsibility diffusion can produce institutional failure in small artificial organizations.

The main research outputs should be auditable research artifacts rather than task-completion demos:

- scenarios
- runs
- event taxonomy
- metrics
- evidence packs
- human or LLM-assisted review records
- claim boundaries and limitations

Early research questions are accepted only at a positioning level:

- Can an artificial organization produce observable social friction and institutional failure events?
- Which institutional and social conditions make those events more likely?
- Which controls reduce failures, and which merely change how failures are justified or hidden?
- Can a reviewer reconstruct failures from evidence packs?
- Which observed patterns can reasonably become hypotheses for real-world study?

## Alternatives considered

1. Treat the project as an AI-agent performance benchmark.
   - Rejected because the research target would drift toward task success and agent capability instead of institutional failure mechanisms.

2. Treat the project as a production workflow automation sandbox.
   - Rejected because production automation would favor reliability and completion, while the research needs controlled observation of failure conditions.

3. Treat LLM behavior as direct evidence of human behavior.
   - Rejected because LLM outputs are evidence for hypothesis generation, not proof that humans will behave the same way.

4. Keep the project as an informal demo of interesting accidents.
   - Rejected because the project needs scenario, event, metric, and evidence structures to support reviewable research claims.

## Consequences

- Claims must be controlled. The project can claim observed artificial-organization behavior and hypotheses, not direct human-social conclusions.
- Evaluation must be based on structured evidence, not only raw conversations or anecdotal logs.
- Protocols and scenarios should be versioned so later changes do not rewrite the basis of earlier observations.
- Ethics and misuse boundaries must remain explicit because the project simulates pressure, rule-bending, and institutional failure.
- Later implementation work must reference this research positioning and avoid turning the core into a task-agent benchmark.

## Follow-up

- PR-D should introduce ODD-Social v0.1 without changing this research position.
- Later P3 work should define event taxonomy, metrics, evidence pack, and review protocols.
- P7/P8 work should define claim boundaries before presenting baseline results as research findings.
