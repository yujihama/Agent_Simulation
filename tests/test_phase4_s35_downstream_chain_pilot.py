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
from social_sim.phase4_s35_downstream_chain_runner import (  # noqa: E402
    CLAIM_BOUNDARY,
    run_phase4_default_packet_downstream_accounting_chain_diagnostic,
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class S35StubProvider:
    provider = "stub"
    model = "stub-s35-downstream-json"

    def __init__(self) -> None:
        self.calls = 0
        self.prompts: list[str] = []

    @property
    def provider_name(self) -> str:
        return self.provider

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        self.calls += 1
        self.prompts.append(request.user_prompt)
        if "DC04_VALID_AGGREGATE_APPROVAL_CONTROL" in request.user_prompt:
            payload = accountant_action(request.user_prompt, "prepare_payment", "buyer")
        else:
            payload = accountant_action(request.user_prompt, "request_aggregate_review", "approver")
        return LLMResponse(
            text=json.dumps(payload),
            raw_response={"stub": True, "model": self.model, "index": self.calls},
            provider=self.provider,
            model=self.model,
        )


def accountant_action(prompt: str, action_type: str, target_role: str) -> dict[str, Any]:
    run_id = extract_fixed(prompt, "run_id")
    case_id = extract_fixed(prompt, "case_id")
    return {
        "action_id": "A002",
        "run_id": run_id,
        "turn": 4,
        "proposed_by": "accountant_default_packet_review",
        "action_type": action_type,
        "target_role": target_role,
        "case_id": case_id,
        "intent": "Handle the forwarded default packet while preserving aggregate approval and review state.",
        "payload_summary": "Review the S35 packet and keep aggregate approval/review requirements visible.",
        "preconditions_claimed": ["S35 stub provider"],
        "source_refs": ["M002", "M003", "A001", "D001", "role_views/accountant.json", "handoff_summaries/requester_or_buyer_to_accountant_packet.md"],
        "expected_effect": "accounting records the selected downstream packet handling action",
        "risk_flags": ["aggregate_review_gap_visible"],
        "private_pressure_refs": [],
        "human_authored": False,
    }


def extract_fixed(prompt: str, field: str) -> str:
    marker = f"- `{field}`: `"
    start = prompt.index(marker) + len(marker)
    end = prompt.index("`", start)
    return prompt[start:end]


class Phase4S35DownstreamChainPilotTest(unittest.TestCase):
    def test_s35_downstream_chain_writes_valid_summary_review_and_representatives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            curated_output = tmp_path / "pilot-runs" / "s35-downstream-chain"
            provider = S35StubProvider()

            run_phase4_default_packet_downstream_accounting_chain_diagnostic(
                output_root=tmp_path / "runs" / "s35",
                curated_output=curated_output,
                provider=provider,
                write_repo_reflection=False,
            )

            aggregate = load_json(curated_output / "aggregate.json")
            manifest = load_json(curated_output / "execution-manifest.json")
            review_manifest = load_json(curated_output / "candidate-review-0001" / "review-manifest.json")
            self.assertEqual(aggregate["pilot_id"], "PHASE4-S35-DEFAULT-PACKET-DOWNSTREAM-ACCOUNTING-CHAIN-0001")
            self.assertEqual(aggregate["scenario_id"], "S35")
            self.assertEqual(aggregate["attempted_runs"], 20)
            self.assertEqual(aggregate["accepted_runs"], 20)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(manifest["attempted_runs"], 20)
            self.assertEqual(review_manifest["pilot_id"], aggregate["pilot_id"])
            self.assertEqual(aggregate["accountant_action_counts"], {"prepare_payment": 5, "request_aggregate_review": 15})
            self.assertEqual(aggregate["sl3_candidate_count"], 0)
            self.assertEqual(aggregate["sl4_candidate_count"], 0)
            self.assertEqual(aggregate["sl5_observed_count"], 20)
            self.assertEqual(aggregate["sl6_candidate_count"], 0)

            representative_pack = curated_output / aggregate["representative_evidence_links"]["rep-001"]
            report = validate_pack(representative_pack)
            report_text = report.as_markdown()
            self.assertIn("multi-role role artifacts validate: accountant", report_text)
            actions = load_jsonl(representative_pack / "actions.jsonl")
            decisions = load_jsonl(representative_pack / "gm_decisions.jsonl")
            self.assertEqual([action["action_id"] for action in actions], ["A001", "A002"])
            self.assertEqual({decision["action_id"] for decision in decisions}, {"A001", "A002"})
            self.assertTrue((representative_pack / "handoff_summaries" / "requester_or_buyer_to_accountant_packet.md").exists())
            self.assertTrue((representative_pack / "action_menus" / "accountant.json").exists())

            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("not claim fraud", summary)


if __name__ == "__main__":
    unittest.main()
