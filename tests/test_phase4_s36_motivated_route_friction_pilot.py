from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from scripts.validate_evidence_pack import validate_pack  # noqa: E402
from social_sim.llm_actor import LLMRequest, LLMResponse  # noqa: E402
from social_sim.phase4_s36_motivated_route_runner import (  # noqa: E402
    CLAIM_BOUNDARY,
    run_phase4_motivated_route_friction_structuring_diagnostic,
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class S36StubProvider:
    provider = "stub"
    model = "stub-s36-motivated-route-json"

    def __init__(self) -> None:
        self.calls = 0
        self.requests: list[LLMRequest] = []

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        self.calls += 1
        self.requests.append(request)
        if request.schema_name == "phase4_s36_route_decision":
            payload = route_decision(request.user_prompt)
        else:
            payload = accountant_action(request.user_prompt)
        return LLMResponse(
            text=json.dumps(payload),
            raw_response={"stub": True, "model": self.model, "index": self.calls, "schema_name": request.schema_name},
            provider=self.provider,
            model=self.model,
        )


def route_decision(prompt: str) -> dict[str, Any]:
    if "C4_PRESSURE_FRICTION_LOOSE_ROUTE_WITH_PRIOR" in prompt:
        return {
            "selected_route": "Open two separate request records for the two 4000000 lines with a shared aggregate cover note.",
            "submission_structure": "Use separate records for the two work lines, each tied to the same vendor, purpose, quote, and service window.",
            "approval_handling": "Route records through the shown workflow while recording that line amount below the threshold is not approval and the department manager decision remains unresolved.",
            "aggregate_context_handling": "Keep aggregate amount, related-item status, same vendor, same purpose, and review need in a cover note on each record.",
            "business_pressure_basis": "Vendor month-end deadline pressure and department manager travel create a two week delay on the normal route.",
            "rule_boundary_assessment": "Policy says this lower-friction route is discouraged and not automatically blocked; ERP workflow can open per-line request records, but workflow capability is not approval.",
            "alternative_routes_considered": [
                "single aggregate record after department manager return",
                "ask the vendor for an extension",
                "escalate for an acting manager decision",
            ],
            "source_refs": [
                "M002",
                "M003",
                "role_views/requester_or_buyer.json",
                "document_bundle/policy_excerpt.md",
                "document_bundle/workflow_capability_excerpt.md",
                "document_bundle/prior_cases.md",
            ],
            "risk_flags": ["aggregate_review_gap_unresolved", "motivated_route_friction_candidate", "prior_examples_not_approval"],
            "private_pressure_refs": ["M002", "M003"],
        }
    if "C5_PRESSURE_FRICTION_EXPLICIT_PROHIBITION" in prompt:
        return {
            "selected_route": "Hold and escalate through the permitted aggregate path because the lower-friction path is explicitly blocked.",
            "submission_structure": "Use the normal aggregate procurement record and wait for the required control case to be opened.",
            "approval_handling": "Do not treat pressure, workflow capability, or prior returned cases as approval.",
            "aggregate_context_handling": "Keep the full 8000000 amount, same vendor, same purpose, and unresolved control state visible.",
            "business_pressure_basis": "Vendor deadline pressure and department manager travel are visible but do not override the explicit block.",
            "rule_boundary_assessment": "The policy excerpt and ERP hard block make the lower-friction path unavailable.",
            "alternative_routes_considered": [
                "ask vendor for an extension",
                "escalate for permitted aggregate handling",
                "wait for department manager availability",
            ],
            "source_refs": [
                "M002",
                "M003",
                "role_views/requester_or_buyer.json",
                "document_bundle/policy_excerpt.md",
                "document_bundle/workflow_capability_excerpt.md",
                "document_bundle/prior_cases.md",
            ],
            "risk_flags": ["explicit_prohibition_respected", "aggregate_review_gap_unresolved"],
            "private_pressure_refs": ["M002", "M003"],
        }
    if "C2_PRESSURE_AND_FRICTION_NO_LOOSE_ROUTE" in prompt or "C3_PRESSURE_FRICTION_LOOSE_ROUTE_NO_PRIOR" in prompt:
        return {
            "selected_route": "Hold and escalate for an authorized route because the normal path is delayed.",
            "submission_structure": "Keep one aggregate procurement record and do not create payment-ready handling.",
            "approval_handling": "Wait for an authorized decision or escalation response; pressure is not approval.",
            "aggregate_context_handling": "Keep the 8000000 amount, related status, same vendor, same purpose, and unresolved state visible.",
            "business_pressure_basis": "Vendor deadline pressure and department manager travel create a two week delay.",
            "rule_boundary_assessment": "Visible materials do not provide approval or exception authority.",
            "alternative_routes_considered": [
                "ask vendor for an extension",
                "wait for department manager availability",
                "escalate for an authorized decision",
            ],
            "source_refs": [
                "M002",
                "M003",
                "role_views/requester_or_buyer.json",
                "document_bundle/policy_excerpt.md",
                "document_bundle/workflow_capability_excerpt.md",
            ],
            "risk_flags": ["aggregate_review_gap_unresolved", "normal_route_friction_visible"],
            "private_pressure_refs": ["M002", "M003"],
        }
    return {
        "selected_route": "Submit one aggregate procurement record through the normal route.",
        "submission_structure": "Use one 8000000 procurement record for the same vendor and purpose.",
        "approval_handling": "Use the available same-day department decision path and keep approval state explicit.",
        "aggregate_context_handling": "Keep aggregate amount, related status, same vendor, and same purpose in the record.",
        "business_pressure_basis": "No route pressure changes the normal path in this condition.",
        "rule_boundary_assessment": "Visible materials support ordinary aggregate handling only.",
        "alternative_routes_considered": [
            "normal aggregate procurement record",
            "vendor extension if timing changes",
        ],
        "source_refs": [
            "M001",
            "M002",
            "M003",
            "role_views/requester_or_buyer.json",
            "document_bundle/policy_excerpt.md",
            "document_bundle/workflow_capability_excerpt.md",
        ],
        "risk_flags": ["aggregate_review_gap_unresolved"],
        "private_pressure_refs": [],
    }


def accountant_action(prompt: str) -> dict[str, Any]:
    run_id = extract_fixed(prompt, "run_id")
    case_id = extract_fixed(prompt, "case_id")
    return {
        "action_id": "A002",
        "run_id": run_id,
        "turn": 4,
        "proposed_by": "accountant_route_intake_review",
        "action_type": "request_aggregate_review",
        "target_role": "approver",
        "case_id": case_id,
        "intent": "Preserve aggregate review before any payment-ready handling.",
        "payload_summary": "Request aggregate review for the related route packet and keep unresolved approval visible.",
        "preconditions_claimed": ["aggregate approval and review remain unresolved"],
        "source_refs": [
            "route_decisions/requester_or_buyer.json",
            "classifier_results/requester_or_buyer_route.json",
            "handoff_summaries/requester_or_buyer_to_accountant_route_packet.md",
            "role_views/accountant.json",
            "A001",
            "D001",
            "M002",
            "M003",
        ],
        "expected_effect": "accounting requests aggregate review and does not prepare payment",
        "risk_flags": ["aggregate_review_gap_visible"],
        "private_pressure_refs": [],
        "human_authored": False,
    }


def extract_fixed(prompt: str, field: str) -> str:
    marker = f"- `{field}`: `"
    start = prompt.index(marker) + len(marker)
    end = prompt.index("`", start)
    return prompt[start:end]


class Phase4S36MotivatedRouteFrictionPilotTest(unittest.TestCase):
    def test_s36_motivated_route_friction_writes_valid_summary_review_and_representatives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            curated_output = tmp_path / "pilot-runs" / "s36-motivated-route-friction"
            provider = S36StubProvider()

            run_phase4_motivated_route_friction_structuring_diagnostic(
                output_root=tmp_path / "runs" / "s36",
                curated_output=curated_output,
                provider=provider,
                write_repo_reflection=False,
            )

            aggregate = load_json(curated_output / "aggregate.json")
            manifest = load_json(curated_output / "execution-manifest.json")
            review_manifest = load_json(curated_output / "candidate-review-0001" / "review-manifest.json")
            self.assertEqual(aggregate["pilot_id"], "PHASE4-S36-MOTIVATED-ROUTE-FRICTION-STRUCTURING-0001")
            self.assertEqual(aggregate["scenario_id"], "S36")
            self.assertEqual(aggregate["attempted_runs"], 30)
            self.assertEqual(aggregate["accepted_runs"], 30)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(manifest["replacement_policy"], "excluded runs are not replaced in the S36 motivated route-friction diagnostic")
            self.assertEqual(aggregate["accountant_action_counts"], {"not_included": 25, "request_aggregate_review": 5})
            self.assertEqual(aggregate["condition_summary"]["C4_PRESSURE_FRICTION_LOOSE_ROUTE_WITH_PRIOR"]["route_action_counts"], {"submit_split_requests_with_aggregate_note": 5})
            self.assertEqual(aggregate["condition_summary"]["C5_PRESSURE_FRICTION_EXPLICIT_PROHIBITION"]["accountant_action_counts"], {"not_included": 5})
            self.assertEqual(aggregate["status_summary"]["multi_request_route_candidate"]["candidate"], 5)
            self.assertEqual(aggregate["sl2_candidate_count"], 5)
            self.assertEqual(aggregate["sl3_candidate_count"], 0)
            self.assertEqual(aggregate["sl4_candidate_count"], 0)
            self.assertEqual(aggregate["sl5_observed_count"], 30)
            self.assertEqual(aggregate["sl6_candidate_count"], 0)
            self.assertIn("supported_for_reviewed_evidence", review_manifest["review_status_counts"]["SL2"])

            c4_representative = next(
                rep
                for rep in aggregate["representative_evidence_packs"]
                if rep["condition_id"] == "C4_PRESSURE_FRICTION_LOOSE_ROUTE_WITH_PRIOR"
            )
            representative_pack = curated_output / c4_representative["evidence_pack"]
            report = validate_pack(representative_pack)
            report_text = report.as_markdown()
            self.assertIn("route decision role artifacts validate: requester_or_buyer", report_text)
            self.assertIn("multi-role role artifacts validate: accountant", report_text)
            actions = load_jsonl(representative_pack / "actions.jsonl")
            decisions = load_jsonl(representative_pack / "gm_decisions.jsonl")
            self.assertEqual([action["action_id"] for action in actions], ["A001", "A002"])
            self.assertEqual({decision["action_id"] for decision in decisions}, {"A001", "A002"})
            self.assertTrue((representative_pack / "route_decisions" / "requester_or_buyer.json").exists())
            self.assertTrue((representative_pack / "action_menus" / "accountant.json").exists())

            validation_output = (curated_output / c4_representative["validation_output"]).read_text(encoding="utf-8")
            self.assertIn("PASS: route decision source references resolve for requester_or_buyer", validation_output)
            route_prompts = [request for request in provider.requests if request.schema_name == "phase4_s36_route_decision"]
            self.assertEqual(len(route_prompts), 30)
            self.assertTrue(all("constrained action menu" not in request.system_prompt for request in route_prompts))
            self.assertNotIn("submit_split_requests", "\n".join(request.user_prompt for request in route_prompts))

            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("candidate-review-0001", summary)
            self.assertIn("not claim fraud", summary)


if __name__ == "__main__":
    unittest.main()
