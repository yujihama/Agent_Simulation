from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from social_sim.expense_reimbursement_runner import (  # noqa: E402
    CLAIM_BOUNDARY,
    EMPLOYEE_ACTION_MENU_ID,
    FINANCE_ACTION_MENU_ID,
    MANAGER_ACTION_MENU_ID,
    run_expense_reimbursement_pilot,
)
from social_sim.llm_actor import LLMRequest, LLMResponse  # noqa: E402


TARGET_ROLES_BY_ACTION_ID = {
    "A001": {
        "send_message": "manager",
        "request_approval": "manager",
        "request_more_evidence": "manager",
        "escalate": "manager",
    },
    "A002": {
        "approve_payment": "employee",
        "reject_payment": "employee",
        "request_more_evidence": "employee",
        "provide_ambiguous_guidance": "employee",
        "escalate": "employee",
    },
    "A003": {
        "prepare_payment": "employee",
        "hold_payment": "employee",
        "request_more_evidence": "employee",
        "authorize_exception_review": "manager",
        "escalate": "manager",
    },
}

SOURCE_REFS_BY_ACTION_ID = {
    "A001": ["initial_state/case.md", "T001"],
    "A002": ["M001", "A001", "D001", "T004"],
    "A003": ["M002", "A002", "D002", "A001", "D001", "T007"],
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def extract_fixed_field(prompt: str, field_name: str) -> str:
    match = re.search(rf"- `{field_name}`: `([^`]+)`", prompt)
    if match is None:
        raise AssertionError(f"missing fixed field {field_name}")
    return match.group(1)


class ExpenseRoleStubProvider:
    provider = "stub"
    model = "stub-expense-role-json"

    def __init__(self, role: str, selected_by_action_id: dict[str, list[str]]) -> None:
        self.role = role
        self.selected_by_action_id = selected_by_action_id
        self.calls_by_action_id = {action_id: 0 for action_id in selected_by_action_id}

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        action_id = extract_fixed_field(request.user_prompt, "action_id")
        run_id = extract_fixed_field(request.user_prompt, "run_id")
        turn = int(extract_fixed_field(request.user_prompt, "turn"))
        case_id = extract_fixed_field(request.user_prompt, "case_id")
        index = self.calls_by_action_id[action_id]
        self.calls_by_action_id[action_id] += 1
        action_type = self.selected_by_action_id[action_id][index]
        risk_flags = []
        if action_type in {"request_more_evidence", "hold_payment", "provide_ambiguous_guidance", "authorize_exception_review", "escalate"}:
            risk_flags.append("expense_evidence_or_approval_gap")
        action = {
            "action_id": action_id,
            "run_id": run_id,
            "turn": turn,
            "proposed_by": self.role,
            "target_role": TARGET_ROLES_BY_ACTION_ID[action_id][action_type],
            "action_type": action_type,
            "case_id": case_id,
            "intent": f"{self.role} selects {action_type} while preserving reimbursement approval and evidence state.",
            "payload_summary": f"{self.role} selected {action_type} for the ER01 reimbursement case.",
            "preconditions_claimed": ["ER01 case state is available"],
            "source_refs": SOURCE_REFS_BY_ACTION_ID[action_id],
            "expected_effect": "The selected action remains subject to deterministic Game Master review.",
            "risk_flags": risk_flags,
            "human_authored": False,
        }
        return LLMResponse(
            text=json.dumps(action),
            raw_response={"stub": True, "model": self.model, "action_id": action_id},
            provider=self.provider,
            model=self.model,
        )


class ExpenseReimbursementPilotTest(unittest.TestCase):
    def test_expense_reimbursement_batch_writes_valid_second_domain_result(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw_output = tmp_path / "runs" / "expense"
            results_output = tmp_path / "results" / "expense"
            run_expense_reimbursement_pilot(
                output_root=raw_output,
                results_output=results_output,
                employee_provider=ExpenseRoleStubProvider(
                    "employee",
                    {"A001": ["send_message", "request_approval", "request_more_evidence", "escalate", "request_approval"]},
                ),
                manager_provider=ExpenseRoleStubProvider(
                    "manager",
                    {"A002": ["approve_payment", "request_more_evidence", "provide_ambiguous_guidance", "reject_payment", "escalate"]},
                ),
                finance_provider=ExpenseRoleStubProvider(
                    "finance_reviewer",
                    {"A003": ["prepare_payment", "hold_payment", "request_more_evidence", "authorize_exception_review", "escalate"]},
                ),
            )

            aggregate = load_json(results_output / "aggregate.json")
            manifest = load_json(results_output / "execution-manifest.json")
            self.assertEqual(aggregate["experiment_id"], "EXP-0005")
            self.assertEqual(aggregate["protocol_ref"], "protocols/domain-expansion/expense-reimbursement-pilot-v0.1.md")
            self.assertEqual(aggregate["domain"], "expense-reimbursement")
            self.assertEqual(aggregate["scenario_id"], "ER01")
            self.assertEqual(aggregate["attempted_runs"], 5)
            self.assertEqual(aggregate["accepted_runs"], 5)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(aggregate["action_menu_ids"]["employee"], EMPLOYEE_ACTION_MENU_ID)
            self.assertEqual(aggregate["action_menu_ids"]["manager"], MANAGER_ACTION_MENU_ID)
            self.assertEqual(aggregate["action_menu_ids"]["finance_reviewer"], FINANCE_ACTION_MENU_ID)
            self.assertEqual(manifest["replacement_policy"], "excluded runs are not replaced in EXP-0005")
            self.assertEqual(aggregate["validation_summary"], {"pass": 5, "fail": 0, "pass_rate_included": 1.0})
            self.assertEqual(aggregate["parser_summaries_by_role"]["employee"]["total_attempts"], 5)
            self.assertEqual(aggregate["parser_summaries_by_role"]["finance_reviewer"]["total_retries"], 0)
            self.assertGreaterEqual(aggregate["approval_evidence_propagation_summary"]["finance_cited_manager_action_or_decision"], 5)
            self.assertGreaterEqual(aggregate["evidence_gap_summary"]["evidence_gap_event_proposed"], 4)
            self.assertGreaterEqual(len(aggregate["representative_evidence_packs"]), 1)

            representative = aggregate["representative_evidence_packs"][0]
            representative_pack = results_output / representative["evidence_pack"]
            actions = load_jsonl(representative_pack / "actions.jsonl")
            decisions = load_jsonl(representative_pack / "gm_decisions.jsonl")
            self.assertEqual([action["action_id"] for action in actions], ["A001", "A002", "A003"])
            self.assertEqual({decision["action_id"] for decision in decisions}, {"A001", "A002", "A003"})
            for role in ["employee", "manager", "finance_reviewer"]:
                self.assertTrue((representative_pack / "action_menus" / f"{role}.json").exists())
                self.assertTrue((representative_pack / "parser_results" / f"{role}.json").exists())
                self.assertTrue((representative_pack / "proposal_attempts" / f"{role}.jsonl").exists())
            self.assertTrue((representative_pack / "llm_prompts" / "employee_A001_claim.md").exists())
            self.assertTrue((representative_pack / "llm_outputs" / "finance_reviewer_A003_review.json").exists())
            self.assertNotIn("raw_response", (representative_pack / "llm_outputs" / "finance_reviewer_A003_review.json").read_text(encoding="utf-8"))

            validation_output = (results_output / representative["validation_output"]).read_text(encoding="utf-8")
            self.assertIn("PASS: selected employee action has a Game Master decision", validation_output)
            self.assertIn("PASS: selected finance_reviewer action matches action menu", validation_output)

            summary = (results_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("second-domain pilot", summary)
            self.assertIn("cross-domain generalization", summary)

    def test_existing_exp0002_representative_pack_remains_valid(self) -> None:
        pack_dir = ROOT / "results" / "org-payment" / "exp-0002-multi-role-baseline" / "representative-evidence-packs" / "s04" / "s04-path-001"
        if not pack_dir.exists():
            self.skipTest(f"committed representative pack not generated yet: {pack_dir}")
        subprocess.run(
            [sys.executable, "scripts/validate_evidence_pack.py", str(pack_dir)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
