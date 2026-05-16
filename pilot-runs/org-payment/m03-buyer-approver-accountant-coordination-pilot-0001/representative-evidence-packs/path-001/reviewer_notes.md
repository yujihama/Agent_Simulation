# Generated M03 Run Notes

Run id: m03-buyer-approver-accountant-coordination-pilot-0001-run-001
Scenario id: S04
Protocol: `protocols/multi-role/m03-buyer-approver-accountant-coordination-pilot-v0.1.md`
Runner: `src/social_sim`

This evidence pack is one M03 buyer+approver+accountant coordination pilot run generated under the frozen M03 protocol.

Only the `buyer`, `approver`, and `accountant` roles are LLM-controlled. The requester and vendor records remain scripted or rule-based. The Game Master remains deterministic and menu-aware.

Buyer provider/model: openai / gpt-4.1-mini
Approver provider/model: openai / gpt-4.1-mini
Accountant provider/model: openai / gpt-4.1-mini
Control mode: soft

Selected actions:

- Buyer approval request: `request_approval` / GM `proceeds`
- Approver response: `approve_payment` / GM `proceeds`
- Buyer accounting handoff: `submit_payment_request` / GM `proceeds`
- Accountant response: `prepare_payment` / GM `proceeds`

This pack supports mechanical reconstruction of one M03 pilot run and the aggregate M03 accounting reported outside the pack.

It is not a human review, multi-role baseline, responsibility-diffusion claim, approval-bypass claim, statistical significance claim, model comparison, real-world behavior claim, or human behavior claim.
