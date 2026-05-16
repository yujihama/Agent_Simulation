# Evidence Pack Validation Output

Evidence pack: `pilot-runs/org-payment/m01-buyer-approver-pilot-0001/representative-evidence-packs/buyer-request_approval_approver-request_more_evidence-run-002`

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
- PASS: multi-role buyer action menu is present and non-empty
- PASS: selected buyer action matches action menu
- PASS: parser result matches selected buyer action
- PASS: proposal attempts record accepted buyer selection
- PASS: selected buyer action has a Game Master decision
- PASS: multi-role approver action menu is present and non-empty
- PASS: selected approver action matches action menu
- PASS: parser result matches selected approver action
- PASS: proposal attempts record accepted approver selection
- PASS: selected approver action has a Game Master decision
- PASS: multi-role buyer and approver artifacts validate
- PASS: cross-references among actions, decisions, trace, events, and metrics resolve

## Boundary

This validation is mechanical. It does not execute LLMs, run a multi-run experiment harness, produce baseline results, or support statistical claims.
