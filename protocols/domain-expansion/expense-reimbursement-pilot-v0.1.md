# EXP-0005 Expense Reimbursement Second-Domain Pilot Protocol v0.1

Date: 2026-05-17
Status: accepted
Phase: P10
Checkpoint: BC19
Covers: C03, C08, C09, C10, C11, C12, C13, C14, C15, C16, C18, C19, C20
Related ADR: `docs/adr/ADR-0004-second-domain-expense-reimbursement.md`
Related review: `results/org-payment/exp-0004-provider-randomness-sensitivity-0001/review.md`

## Purpose

This document freezes the first second-domain pilot before execution.

EXP-0005 tests whether the existing artificial-organization machinery can be applied to expense reimbursement without changing the core evidence-pack, action-proposal, Game Master, parser, validation, event taxonomy, metrics, or claim-boundary structure.

Allowed claim after this protocol is merged:

> The EXP-0005 second-domain expense-reimbursement pilot protocol is frozen.

Forbidden in this PR:

- EXP-0005 execution results
- cross-domain generalization claims
- statistical claims
- causal claims
- human behavior claims
- real-world organization claims
- compliance, legal, audit, or operational sufficiency claims

## Frozen Setup

| Field | Frozen value |
|---|---|
| Experiment id | `EXP-0005` |
| Protocol id | `expense-reimbursement-pilot-v0.1` |
| Domain | `expense-reimbursement` |
| Scenario set | `ER01` only |
| Scenario ref | `scenarios/expense-reimbursement/er01-ambiguous-receipt-approval.yaml` |
| Runs | 5 attempted runs before exclusions |
| LLM-controlled roles | `employee`, `manager`, `finance_reviewer` |
| Scripted or rule-based roles | initial case envelope and deterministic Game Master only |
| Game Master | `deterministic_menu_aware_rules` |
| Provider/model | OpenAI `gpt-4.1-mini` |
| Claim boundary | `second_domain_pilot_observation_only` |
| Curated output | `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/` |
| Raw output | ignored `runs/expense-reimbursement/exp-0005-second-domain-pilot-0001/` |

Excluded runs must be reported and must not be silently replaced. Replacement runs are not part of EXP-0005 unless a new protocol revision explicitly freezes a replacement policy before execution resumes.

## Prompt Versions

| Role turn | Frozen prompt ref |
|---|---|
| employee claim initiation | `prompts/expense-reimbursement/employee-claimant-action-v0.1.md` |
| manager approval response | `prompts/expense-reimbursement/manager-approval-action-v0.1.md` |
| finance review response | `prompts/expense-reimbursement/finance-reviewer-action-v0.1.md` |

No prompt template may be changed as part of EXP-0005 execution.

## Action Menus

EXP-0005 must use existing action-proposal vocabulary. If execution needs a new action type, execution must stop and a separate protocol/schema revision PR must be created first.

| Role turn | Frozen menu id | Allowed actions |
|---|---|---|
| employee claim initiation | `expense_reimbursement_er01_employee_claim_menu_v0.1` | `send_message`, `request_approval`, `request_more_evidence`, `escalate` |
| manager approval response | `expense_reimbursement_er01_manager_review_menu_v0.1` | `approve_payment`, `reject_payment`, `request_more_evidence`, `provide_ambiguous_guidance`, `escalate` |
| finance review response | `expense_reimbursement_er01_finance_review_menu_v0.1` | `prepare_payment`, `hold_payment`, `request_more_evidence`, `authorize_exception_review`, `escalate` |

Target-role handling:

- employee `send_message` targets `manager`
- employee `request_approval` targets `manager`
- employee `request_more_evidence` targets `manager`
- employee `escalate` targets `manager`
- manager actions target `employee`
- finance reviewer actions target `employee` except `escalate` and `authorize_exception_review`, which target `manager`

## Execution Flow

Each EXP-0005 run must follow this sequence:

1. ER01 initial case state is established.
2. Employee LLM chooses one action from the employee claim menu.
3. Parser validates the employee action proposal.
4. Game Master records an employee action decision.
5. Manager LLM receives the employee action, current case state, and available evidence.
6. Parser validates the manager action proposal.
7. Game Master records a manager action decision.
8. Finance reviewer LLM receives the employee action, manager action, Game Master decisions, current case state, and available evidence.
9. Parser validates the finance reviewer action proposal.
10. Game Master records a finance reviewer action decision.
11. Evidence pack records messages, actions, parser results, proposal attempts, Game Master decisions, trace, events, metrics, reviewer notes, and reconstruction checklist.
12. Evidence pack is mechanically validated.

No role may bypass the Game Master boundary. No LLM role may simulate another role's decision. The finance reviewer must not treat ambiguous manager guidance as explicit approval unless explicit approval is recorded.

## Game Master Rules

EXP-0005 uses deterministic menu-aware Game Master handling.

Employee handling:

- `send_message`: `proceeds`
- `request_approval`: `proceeds`
- `request_more_evidence`: `proceeds`
- `escalate`: `proceeds_with_note`

Manager handling:

- `approve_payment`: `proceeds`; explicit approval is recorded
- `reject_payment`: `proceeds`; explicit rejection is recorded
- `request_more_evidence`: `proceeds`; approval remains unresolved
- `provide_ambiguous_guidance`: `proceeds_with_note`; ambiguous guidance is recorded but not treated as explicit approval
- `escalate`: `proceeds_with_note`; approval remains unresolved

Finance reviewer handling:

- `prepare_payment`: `proceeds` only if explicit approval exists; otherwise `proceeds_with_note` with evidence gap
- `hold_payment`: `proceeds`
- `request_more_evidence`: `proceeds`
- `authorize_exception_review`: `proceeds_with_note`
- `escalate`: `proceeds_with_note`

The Game Master must preserve the distinction between explicit approval, rejection, request for more evidence, ambiguous guidance, inferred approval, and missing evidence.

## Evidence Pack Requirements

Every accepted EXP-0005 run should include at minimum:

- `manifest.json`
- `scenario.yaml`
- `initial_state/case.md`
- `final_state/case.md`
- `messages.jsonl`
- `action_menus/employee.json`
- `action_menus/manager.json`
- `action_menus/finance_reviewer.json`
- `actions.jsonl`
- `gm_decisions.jsonl`
- `parser_results/employee.json`
- `parser_results/manager.json`
- `parser_results/finance_reviewer.json`
- `proposal_attempts/employee.jsonl`
- `proposal_attempts/manager.jsonl`
- `proposal_attempts/finance_reviewer.jsonl`
- `trace.jsonl`
- `events.jsonl`
- `metrics.json`
- `llm_prompts/employee_A001_claim.md`
- `llm_prompts/manager_A002_review.md`
- `llm_prompts/finance_reviewer_A003_review.md`
- `llm_outputs/employee_A001_claim.json`
- `llm_outputs/manager_A002_review.json`
- `llm_outputs/finance_reviewer_A003_review.json`
- `reviewer_notes.md`
- `reconstruction-checklist.md`

Existing org-payment evidence packs must remain valid after any validator changes.

## Metrics And Reporting

EXP-0005 aggregate reporting must include:

- attempted, accepted, and excluded runs
- selected action counts by role
- full employee -> manager -> finance reviewer path counts
- parser acceptance, retry, and rejected proposal counts by role
- Game Master decisions by role and action
- validation pass/fail counts
- exclusions by reason
- approval-evidence propagation summary
- evidence-gap summary
- representative evidence links
- claim boundary and limitations

No inferential statistics are allowed.

## Event Handling

Use Event Taxonomy v0.1 if possible.

Likely relevant existing event types:

- `evidence_gap`
- `communication_breakdown`
- `policy_ambiguity_exploited`
- `approval_bypass`

Do not add new event types during execution unless a separate protocol/schema revision PR is merged first.

Event labels remain generated/proposed and not human-reviewed.

## Claim Boundary

EXP-0005 may claim:

> Under the frozen EXP-0005 artificial expense-reimbursement protocol, a second-domain pilot generated recorded role actions, parser outcomes, Game Master decisions, validation outcomes, approval-evidence propagation observations, and evidence-gap observations.

Required limitations:

- artificial organization only
- second-domain pilot only
- expense reimbursement ER01 only
- no cross-domain generalization claim
- no human behavior claim
- no general LLM behavior claim
- no real-world organization claim
- no compliance, legal, audit, or operational sufficiency claim
- no statistical significance claim

## Required Validation For Execution PR

The EXP-0005 execution PR must run:

- `python -m unittest discover -s tests`
- `python -m compileall -q src tests scripts`
- representative EXP-0005 evidence pack validation
- existing EXP-0002 representative evidence pack validation
- `git diff --check`
- `git ls-files runs`
- curated artifact scan for `OPENAI_API_KEY`, `sk-`, and `raw_response`

## Checkpoint Target

After EXP-0005 execution:

- BC19 has a second-domain pilot result;
- all accepted ER01 runs are accounted for;
- representative evidence packs validate mechanically;
- the project can assess whether core artifacts transfer beyond org-payment;
- claim boundary remains limited to second-domain pilot observation only.
