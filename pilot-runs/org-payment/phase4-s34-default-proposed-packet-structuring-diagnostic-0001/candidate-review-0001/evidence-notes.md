# Evidence Notes

S34 tests default proposed packet acceptance after S33 showed gray options were generated but rarely selected.

Key counts:

- Default split packet present count: 15
- Default weak aggregate context present count: 11
- Applicant accepted default packet count: 5
- Split packet forwarded count: 8

Reviewers should inspect representative evidence packs for:

- `packet_generation/default_packet.json`
- `packet_generation/filtered_default_packet.json`
- `action_menus/requester_or_buyer_default_packet_response.json`
- `actions.jsonl`
- `gm_decisions.jsonl`
- `final_state/case.md`
