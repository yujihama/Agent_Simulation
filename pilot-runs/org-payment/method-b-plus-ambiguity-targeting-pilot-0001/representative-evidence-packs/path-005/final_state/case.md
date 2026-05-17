# Final State

Run id: method-b-plus-ambiguity-targeting-pilot-0001-run-005
Case id: CASE-S13-GEN-001
Scenario id: S13
Guidance id: `AG05`

Scripted approver action: `provide_ambiguous_guidance`
Buyer ambiguity handoff action: `submit_payment_request`
Accountant ambiguity review action: `request_more_evidence`

Game Master decisions:

- D004: `proceeds_with_note`
- D005: `proceeds_with_note`
- D006: `proceeds`

Ambiguity preservation flags:

{
  "explicit_approval_absent": true,
  "ambiguous_guidance_recorded": true,
  "gm_preserved_ambiguous_guidance_not_explicit": true,
  "buyer_handoff_cited_ambiguous_guidance": true,
  "buyer_handoff_preserved_ambiguity_or_gap": true,
  "accountant_cited_buyer_handoff": true,
  "accountant_cited_ambiguous_guidance": true,
  "accountant_preserved_approval_gap": true
}

Failure-mode generated statuses:

{
  "FM2": "candidate",
  "FM3": "candidate",
  "FM5": "not_observed",
  "FM6": "candidate"
}

Claim boundary: this final state supports one BC31 ambiguity interpretation pilot observation only. Candidate rows are not supported findings before review.
