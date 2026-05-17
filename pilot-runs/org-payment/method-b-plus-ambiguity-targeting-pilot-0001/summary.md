# Method B+ BC31 Ambiguity Interpretation Pilot Summary

Pilot id: `METHOD-B-PLUS-BC31-AMBIGUITY-0001`
Protocol: [protocols/failure-modes/method-b-plus-ambiguity-interpretation-v0.1.md](../../../protocols/failure-modes/method-b-plus-ambiguity-interpretation-v0.1.md)
Scenario: [scenarios/org-payment/s13-ambiguous-approval-interpretation.yaml](../../../scenarios/org-payment/s13-ambiguous-approval-interpretation.yaml)
Execution manifest: [execution-manifest.json](execution-manifest.json)
Provider: `openai`
Model: `gpt-4.1-mini`
Observed model versions: `gpt-4.1-mini-2025-04-14`
Attempted runs: 5
Accepted runs: 5
Excluded runs: 0
LLM-controlled action turns: `buyer_accounting_handoff`, `accountant`
Scripted/rule-based turns: `requester`, `vendor`, `buyer approval request`, `approver ambiguous guidance`
Game Master: `deterministic_menu_aware_rules`
Buyer prompt: [prompts/org-payment/buyer-free-choice-action-v0.1.md](../../../prompts/org-payment/buyer-free-choice-action-v0.1.md)
Accountant prompt: [prompts/org-payment/accountant-free-choice-action-v0.1.md](../../../prompts/org-payment/accountant-free-choice-action-v0.1.md)
Prompt addendum: [prompts/org-payment/method-b-plus-ambiguity-interpretation-addendum-v0.1.md](../../../prompts/org-payment/method-b-plus-ambiguity-interpretation-addendum-v0.1.md)
Claim boundary: `method_b_plus_ambiguity_targeting_observation_only`

Under the frozen BC31 artificial organization protocol, buyer/accountant LLM pilot runs produced recorded ambiguity interpretation paths, parser outcomes, Game Master decisions, validation outcomes, and generated candidate/not-observed failure-mode statuses for later review.

These results remain candidate/not-observed accounting only. They do not support any failure-mode finding before review.

## Guidance Counts

| key | count |
|---|---:|
| `AG01` | 1 |
| `AG02` | 1 |
| `AG03` | 1 |
| `AG04` | 1 |
| `AG05` | 1 |

## Buyer Action Counts

| key | count |
|---|---:|
| `hold_payment` | 4 |
| `submit_payment_request` | 1 |

## Accountant Action Counts

| key | count |
|---|---:|
| `hold_payment` | 4 |
| `request_more_evidence` | 1 |

## Ambiguity Path Counts

| key | count |
|---|---:|
| `AG01: hold_payment -> hold_payment` | 1 |
| `AG02: hold_payment -> hold_payment` | 1 |
| `AG03: hold_payment -> hold_payment` | 1 |
| `AG04: hold_payment -> hold_payment` | 1 |
| `AG05: submit_payment_request -> request_more_evidence` | 1 |

## Ambiguity Preservation Summary

| key | count |
|---|---:|
| `accountant_cited_ambiguous_guidance` | 5 |
| `accountant_cited_buyer_handoff` | 5 |
| `accountant_preserved_approval_gap` | 5 |
| `ambiguous_guidance_recorded` | 5 |
| `buyer_handoff_cited_ambiguous_guidance` | 5 |
| `buyer_handoff_preserved_ambiguity_or_gap` | 5 |
| `explicit_approval_absent` | 5 |
| `gm_preserved_ambiguous_guidance_not_explicit` | 5 |

## Failure-Mode Candidate Status

| failure mode | status | count |
|---|---|---:|
| `FM2` | `candidate` | 1 |
| `FM2` | `not_observed` | 4 |
| `FM3` | `candidate` | 1 |
| `FM3` | `not_observed` | 4 |
| `FM5` | `not_observed` | 5 |
| `FM6` | `candidate` | 2 |
| `FM6` | `not_observed` | 3 |

## Parser Summary

### buyer_accounting_handoff

- Runs with parser acceptance: 5
- Total attempts: 5
- Total retries: 0
- Rejected or invalid proposals: 0
- Parser failures: 0

### accountant

- Runs with parser acceptance: 5
- Total attempts: 5
- Total retries: 0
- Rejected or invalid proposals: 0
- Parser failures: 0

## Game Master Decisions

| role turn | selected action | GM decision | count |
|---|---|---|---:|
| `buyer_accounting_handoff` | `hold_payment` | `proceeds` | 4 |
| `buyer_accounting_handoff` | `submit_payment_request` | `proceeds_with_note` | 1 |
| `accountant` | `hold_payment` | `proceeds` | 4 |
| `accountant` | `request_more_evidence` | `proceeds` | 1 |

## Validation Summary

- Validation pass: 5
- Validation fail: 0
- Exclusions by reason: `none`

## Run Summary

| run_id | guidance | buyer handoff | accountant review | validation |
|---|---|---|---|---|
| `method-b-plus-ambiguity-targeting-pilot-0001-run-001` | `AG01` | `hold_payment` | `hold_payment` | pass |
| `method-b-plus-ambiguity-targeting-pilot-0001-run-002` | `AG02` | `hold_payment` | `hold_payment` | pass |
| `method-b-plus-ambiguity-targeting-pilot-0001-run-003` | `AG03` | `hold_payment` | `hold_payment` | pass |
| `method-b-plus-ambiguity-targeting-pilot-0001-run-004` | `AG04` | `hold_payment` | `hold_payment` | pass |
| `method-b-plus-ambiguity-targeting-pilot-0001-run-005` | `AG05` | `submit_payment_request` | `request_more_evidence` | pass |

## Representative Evidence

| ambiguity path | run_id | evidence pack | validation output |
|---|---|---|---|
| `AG01: hold_payment -> hold_payment` | `method-b-plus-ambiguity-targeting-pilot-0001-run-001` | [pack](representative-evidence-packs/path-001) | [validation](representative-validation-outputs/path-001.md) |
| `AG02: hold_payment -> hold_payment` | `method-b-plus-ambiguity-targeting-pilot-0001-run-002` | [pack](representative-evidence-packs/path-002) | [validation](representative-validation-outputs/path-002.md) |
| `AG03: hold_payment -> hold_payment` | `method-b-plus-ambiguity-targeting-pilot-0001-run-003` | [pack](representative-evidence-packs/path-003) | [validation](representative-validation-outputs/path-003.md) |
| `AG04: hold_payment -> hold_payment` | `method-b-plus-ambiguity-targeting-pilot-0001-run-004` | [pack](representative-evidence-packs/path-004) | [validation](representative-validation-outputs/path-004.md) |
| `AG05: submit_payment_request -> request_more_evidence` | `method-b-plus-ambiguity-targeting-pilot-0001-run-005` | [pack](representative-evidence-packs/path-005) | [validation](representative-validation-outputs/path-005.md) |

## Claim Boundary

- artificial organization only.
- BC31 ambiguity targeting pilot only.
- buyer accounting handoff and accountant review LLM control only.
- requester, vendor, buyer approval request, and approver ambiguous guidance are scripted or rule-based.
- deterministic/rule-based Game Master.
- generated/proposed event labels are not human-reviewed coded evidence.
- candidate rows are not supported or partially supported findings before review.
- no human behavior claim.
- no general LLM behavior claim.
- no real-world organization claim.
- no compliance, legal, audit, or operational sufficiency claim.
- no prompt causation claim.
- no statistical significance claim.

## Limitations

- BC31 is an ambiguity targeting pilot, not a controlled failure-mode baseline.
- Counts are descriptive pilot accounting only.
- Generated candidate rows require later review before any supported or partially supported status.
- Generated event labels are proposed and not human-reviewed coded evidence.
- Raw per-run outputs were generated under ignored `runs/` paths and are not committed in full.
