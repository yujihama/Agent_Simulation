# Evidence Pack Validation Output

Evidence pack: `results/expense-reimbursement/exp-0005-second-domain-pilot-0001/representative-evidence-packs/path-001`

Result: PASS

## Checks

- PASS: manifest.json validates against run-manifest.schema.json
- PASS: manifest declares explicit LLM execution status and no automated harness
- PASS: manifest artifact inventory matches files on disk
- PASS: scenario YAML files parse and scenario id matches manifest
- PASS: JSON and JSONL records validate against contract schemas
- PASS: run_id and metrics envelope inheritance are consistent
- PASS: action proposal source references resolve
- PASS: every current action proposal has a corresponding Game Master decision
- PASS: multi-role employee action menu is present and non-empty
- PASS: selected employee action matches action menu
- PASS: parser result matches selected employee action
- PASS: proposal attempts record accepted employee selection
- PASS: selected employee action has a Game Master decision
- PASS: multi-role finance_reviewer action menu is present and non-empty
- PASS: selected finance_reviewer action matches action menu
- PASS: parser result matches selected finance_reviewer action
- PASS: proposal attempts record accepted finance_reviewer selection
- PASS: selected finance_reviewer action has a Game Master decision
- PASS: multi-role manager action menu is present and non-empty
- PASS: selected manager action matches action menu
- PASS: parser result matches selected manager action
- PASS: proposal attempts record accepted manager selection
- PASS: selected manager action has a Game Master decision
- PASS: multi-role role artifacts validate: employee, finance_reviewer, manager
- PASS: cross-references among actions, decisions, trace, events, and metrics resolve

## Boundary

This validation is mechanical. It does not execute LLMs, run a multi-run experiment harness, produce baseline results, or support statistical claims.
