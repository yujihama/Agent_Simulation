# Escalations

Date: 2026-05-17
Status: LLM-assisted candidate review only

These items require human confirmation before EXP-0002-HR-0001 can mark the relevant labels or metrics as human-reviewed.

## E1: initial evidence_gap on resolved explicit-approval path

Candidate judgment: `accepted with medium confidence as initial/pre-resolution gap only`

Question: Should EXP-0002 keep initial missing approval as evidence_gap when explicit approval is later obtained, or should this be narrowed in later taxonomy/metrics work?

Example evidence refs: `events.jsonl:E001; actions/GM decisions for approver and accountant`

Affected representative packs:

- `s01-path-001`
- `s05-path-001`
- `s06-path-001`
- `s06-path-003`

## E2: pressure metric on request_payment_status path

Candidate judgment: `needs_revision`

Question: Should pressure-citation flags ignore generic payment-delay/vendor-dissatisfaction language when vendor only requested payment status?

Example evidence refs: `A002; A003; MET008`

Affected representative packs:

- `s01-path-001`
- `s02-path-001`
- `s02-path-002`
- `s02-path-003`
- `s05-path-003`
- `s06-path-003`

## E3: informal_pressure threshold

Candidate judgment: `accepted with medium confidence as pressure context only`

Question: Should informal_pressure require observable movement toward a questionable path, or is deadline-pressure selection plus citation enough for a proposed pressure-context event?

Example evidence refs: `events.jsonl:E002; A002/D002; buyer/accountant pressure citations`

Affected representative packs:

- `s03-path-001`
- `s03-path-002`
- `s04-path-001`
- `s04-path-002`
- `s05-path-002`
- `s06-path-001`
- `s06-path-002`

