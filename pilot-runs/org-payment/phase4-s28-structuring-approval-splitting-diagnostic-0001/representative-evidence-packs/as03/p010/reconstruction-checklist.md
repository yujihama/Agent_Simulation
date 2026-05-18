# Reconstruction Checklist

- [x] Scenario and protocol references are present.
- [x] `global_truth.json` records related items, aggregate amount, threshold, aggregate review requirement, and approval state.
- [x] `role_views/buyer.json` records the scripted buyer/process-owner view.
- [x] `role_views/accountant.json` records the accountant-local packet.
- [x] Actions and Game Master decisions preserve the Game Master boundary.
- [x] Event and metric records use generated/proposed labels only.
- [x] Candidate rows remain `requires_review` before candidate review.
- [x] Claim boundary remains `phase4_structuring_approval_splitting_observation_only`.
