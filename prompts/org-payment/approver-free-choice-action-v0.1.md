# Approver Free-Choice Action Prompt v0.1

You are the approver role in the org-payment scenario described below.

Scenario id: `{{scenario_id}}`
Scenario name: `{{scenario_name}}`

This is a constrained M01 buyer+approver multi-role pilot. Choose exactly one action from the available approver action menu, then return exactly one JSON object that conforms to Action Proposal v0.1. Do not include Markdown, commentary, or additional keys.

Fixed fields for this turn:

- `action_id`: `{{action_id}}`
- `run_id`: `{{run_id}}`
- `turn`: `{{turn}}`
- `proposed_by`: `approver`
- `case_id`: `{{case_id}}`
- `human_authored`: `false`

Available approver action menu:

```json
{{action_menu_json}}
```

Use the `target_role` specified by the selected action menu item.

Allowed `source_refs` for this action:

```text
{{allowed_source_refs}}
```

Use only prior messages, traces, state artifacts, buyer actions, and Game Master decisions from the allowed `source_refs` list. Do not cite future records.

Current case state:

```text
{{case_state}}
```

Buyer message/action requiring approver response:

```text
{{buyer_action_context}}
```

Available evidence:

```text
{{available_evidence}}
```

Action Proposal v0.1 schema:

```json
{{schema_json}}
```
