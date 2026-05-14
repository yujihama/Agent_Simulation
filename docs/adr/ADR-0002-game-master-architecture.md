# ADR-0002: Game Master Architecture

Date: 2026-05-14
Status: accepted
Phase: P0
Step: PR-C
Covers: C09; architecture direction for C10, C12, C15, C16
Supersedes: none
Related ADR: ADR-0001

## Context

The project needs to observe social action under institutional constraints. If LLM agents directly edit state, files, approvals, or logs, the simulation cannot separate agent intent from institutional outcome.

The technical selection draft also rejects using task-solving agent frameworks as the research core. Those frameworks are useful for work execution, but they can obscure whether an observed result came from social conditions, tool behavior, framework orchestration, or model capability.

Source drafts not yet imported into this repository:

- `technical_selection_for_social_simulation.md`
- `research_framework_design.md`

## Decision

The simulation architecture will use a Game Master / Arbiter boundary.

LLM actors may observe state, form intent, send messages, and propose actions. They do not directly mutate the world state. A Game Master / Arbiter interprets proposed actions, applies the Institution Layer and World / Environment rules, records the outcome, and writes evidence.

The intended architecture direction is:

```text
Social Simulation Core
|-- Scenario / ODD-Social Spec
|-- World / Environment
|-- Institution Layer
|-- Population Layer
|-- Interaction Layer
|-- Game Master / Arbiter
|-- LLM Actor Adapter
|-- Experiment Harness
`-- Evaluation Layer
```

Early implementation should prefer a minimal custom Python core with a provider-neutral LLM actor adapter. Concordia is the primary conceptual reference because its Game Master pattern separates agent intent from world consequences. LangChain DeepAgents is not the research core; it may only be used as a limited actor implementation or comparison condition if later work needs it.

## Alternatives considered

1. Let agents directly update world state and files.
   - Rejected because it collapses agent intent, authority, institutional permission, and state mutation into one layer.

2. Use LangChain DeepAgents as the core architecture.
   - Rejected for the research core because it is optimized for task execution, sub-agents, tools, and file work rather than auditable institutional simulation.

3. Use LangGraph as the primary simulation model.
   - Rejected for Phase 1 as a core model because it can make the system feel like a workflow rather than a social simulation. It remains a later option for execution management or human-in-the-loop review.

4. Directly adopt Concordia as the complete implementation base.
   - Not accepted yet. Concordia is a strong architectural reference, but direct adoption requires later dependency, maintenance, and extension checks.

## Consequences

- Every consequential state transition should be traceable to an agent proposal and a Game Master decision.
- Institution rules must live outside agent prompts as environment-side constraints.
- Evidence packs should include traces, messages, proposed actions, Game Master decisions, events, and metrics.
- Provider-specific SDKs can be implementation details, but the research architecture should remain provider-neutral.
- Later code PRs must preserve the actor-to-GM boundary.

## Follow-up

- P4 should define concrete action proposal, trace, event, and Game Master decision data contracts.
- P5 should test Game Master decisions with non-LLM dry runs.
- P6 should verify that LLM actors can generate usable action proposals without direct state mutation.
