from __future__ import annotations

import argparse
from pathlib import Path

from .baseline_runner import run_buyer_only_baseline
from .free_choice_runner import run_s04_buyer_free_choice_llm
from .llm_actor import OpenAIResponsesProvider
from .m02_pressure_runner import run_m02_buyer_vendor_pressure_pilot
from .m03_coordination_runner import run_m03_coordination_pilot
from .m04_full_role_runner import run_m04_full_role_pilot
from .m05_full_org_runner import run_m05_full_org_payment_pilot
from .multi_role_baseline_runner import DEFAULT_BASELINE_BATCH_ID as DEFAULT_MULTI_ROLE_BASELINE_BATCH_ID
from .multi_role_baseline_runner import run_multi_role_baseline
from .multi_role_sweep_runner import DEFAULT_SWEEP_BATCH_ID as DEFAULT_MULTI_ROLE_SWEEP_BATCH_ID
from .multi_role_sweep_runner import run_multi_role_scenario_sweep_pilot
from .multirole_runner import run_m01_buyer_approver_pilot
from .repeated_runner import DEFAULT_REPEATED_BATCH_ID, run_s04_buyer_free_choice_batch
from .runner import run_s04, run_s04_buyer_llm
from .scenario_sweep_runner import DEFAULT_SWEEP_BATCH_ID, run_buyer_scenario_sweep
from .sensitivity_runner import DEFAULT_BATCH_ID as DEFAULT_PROVIDER_RANDOMNESS_SENSITIVITY_BATCH_ID
from .sensitivity_runner import DEFAULT_COUNT_PER_SCENARIO as DEFAULT_PROVIDER_RANDOMNESS_SENSITIVITY_COUNT
from .sensitivity_runner import run_provider_randomness_sensitivity


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run minimal non-LLM social simulations.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_s04 = subparsers.add_parser(
        "generate-s04",
        help="Generate a deterministic S04 non-LLM evidence pack.",
    )
    generate_s04.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Output evidence-pack directory. Must be new or empty.",
    )
    generate_s04.add_argument(
        "--run-id",
        default="generated-s04-scripted-0001",
        help="Run id to write into the generated evidence pack.",
    )
    buyer_llm = subparsers.add_parser(
        "generate-s04-buyer-llm",
        help="Generate an S04 pack where OpenAI formats fixed-action buyer proposals.",
    )
    buyer_llm.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Output evidence-pack directory. Must be new or empty.",
    )
    buyer_llm.add_argument(
        "--run-id",
        default="pilot-s04-buyer-openai-0001",
        help="Run id to write into the generated evidence pack.",
    )
    buyer_llm.add_argument(
        "--dotenv",
        default=Path(".env"),
        type=Path,
        help="Optional dotenv file containing OPENAI_API_KEY.",
    )
    buyer_llm.add_argument(
        "--model",
        help="OpenAI model name. Defaults to OPENAI_MODEL or gpt-4.1-mini.",
    )
    buyer_free_choice = subparsers.add_parser(
        "generate-s04-buyer-free-choice-llm",
        help="Generate an S04 pack where OpenAI chooses one buyer action from a constrained menu.",
    )
    buyer_free_choice.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Output evidence-pack directory. Must be new or empty.",
    )
    buyer_free_choice.add_argument(
        "--run-id",
        default="pilot-s04-buyer-free-choice-openai-0001",
        help="Run id to write into the generated evidence pack.",
    )
    buyer_free_choice.add_argument(
        "--dotenv",
        default=Path(".env"),
        type=Path,
        help="Optional dotenv file containing OPENAI_API_KEY.",
    )
    buyer_free_choice.add_argument(
        "--model",
        help="OpenAI model name. Defaults to OPENAI_MODEL or gpt-4.1-mini.",
    )
    buyer_free_choice_batch = subparsers.add_parser(
        "generate-s04-buyer-free-choice-batch",
        help="Generate repeated S04 buyer free-choice OpenAI pilot packs and a curated aggregate summary.",
    )
    buyer_free_choice_batch.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Raw batch output directory under ignored runs/. Must be new or empty.",
    )
    buyer_free_choice_batch.add_argument(
        "--curated-output",
        required=True,
        type=Path,
        help="Curated aggregate output directory. Must be new or empty.",
    )
    buyer_free_choice_batch.add_argument(
        "--count",
        default=5,
        type=int,
        help="Number of repeated pilot runs to generate. Defaults to 5.",
    )
    buyer_free_choice_batch.add_argument(
        "--batch-id",
        default=DEFAULT_REPEATED_BATCH_ID,
        help="Stable batch id prefix used for per-run ids.",
    )
    buyer_free_choice_batch.add_argument(
        "--dotenv",
        default=Path(".env"),
        type=Path,
        help="Optional dotenv file containing OPENAI_API_KEY.",
    )
    buyer_free_choice_batch.add_argument(
        "--model",
        help="OpenAI model name. Defaults to OPENAI_MODEL or gpt-4.1-mini.",
    )
    buyer_sweep = subparsers.add_parser(
        "generate-buyer-scenario-sweep",
        help="Generate S01-S06 buyer-only free-choice OpenAI pilot packs and a curated aggregate summary.",
    )
    buyer_sweep.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Raw sweep output directory under ignored runs/. Must be new or empty.",
    )
    buyer_sweep.add_argument(
        "--curated-output",
        required=True,
        type=Path,
        help="Curated sweep output directory. Must be new or empty.",
    )
    buyer_sweep.add_argument(
        "--count-per-scenario",
        default=3,
        type=int,
        help="Number of pilot runs per scenario. Defaults to 3.",
    )
    buyer_sweep.add_argument(
        "--batch-id",
        default=DEFAULT_SWEEP_BATCH_ID,
        help="Stable batch id prefix used for per-run ids.",
    )
    buyer_sweep.add_argument(
        "--dotenv",
        default=Path(".env"),
        type=Path,
        help="Optional dotenv file containing OPENAI_API_KEY.",
    )
    buyer_sweep.add_argument(
        "--model",
        help="OpenAI model name. Defaults to OPENAI_MODEL or gpt-4.1-mini.",
    )
    buyer_baseline = subparsers.add_parser(
        "execute-buyer-only-baseline",
        help="Execute frozen EXP-0001 buyer-only baseline and write curated results.",
    )
    buyer_baseline.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Raw baseline output directory under ignored runs/. Must be new or empty.",
    )
    buyer_baseline.add_argument(
        "--results-output",
        required=True,
        type=Path,
        help="Curated baseline result directory. Must be new or empty.",
    )
    buyer_baseline.add_argument(
        "--dotenv",
        default=Path(".env"),
        type=Path,
        help="Optional dotenv file containing OPENAI_API_KEY.",
    )
    m01_pilot = subparsers.add_parser(
        "execute-m01-buyer-approver-pilot",
        help="Execute frozen M01 buyer+approver multi-role pilot and write curated results.",
    )
    m01_pilot.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Raw M01 output directory under ignored runs/. Must be new or empty.",
    )
    m01_pilot.add_argument(
        "--curated-output",
        required=True,
        type=Path,
        help="Curated M01 pilot output directory. Must be new or empty.",
    )
    m01_pilot.add_argument(
        "--dotenv",
        default=Path(".env"),
        type=Path,
        help="Optional dotenv file containing OPENAI_API_KEY.",
    )
    m02_pilot = subparsers.add_parser(
        "execute-m02-buyer-vendor-pressure-pilot",
        help="Execute frozen M02 buyer+vendor pressure pilot and write curated results.",
    )
    m02_pilot.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Raw M02 output directory under ignored runs/. Must be new or empty.",
    )
    m02_pilot.add_argument(
        "--curated-output",
        required=True,
        type=Path,
        help="Curated M02 pilot output directory. Must be new or empty.",
    )
    m02_pilot.add_argument(
        "--dotenv",
        default=Path(".env"),
        type=Path,
        help="Optional dotenv file containing OPENAI_API_KEY.",
    )
    m03_pilot = subparsers.add_parser(
        "execute-m03-buyer-approver-accountant-coordination-pilot",
        help="Execute frozen M03 buyer+approver+accountant coordination pilot and write curated results.",
    )
    m03_pilot.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Raw M03 output directory under ignored runs/. Must be new or empty.",
    )
    m03_pilot.add_argument(
        "--curated-output",
        required=True,
        type=Path,
        help="Curated M03 pilot output directory. Must be new or empty.",
    )
    m03_pilot.add_argument(
        "--dotenv",
        default=Path(".env"),
        type=Path,
        help="Optional dotenv file containing OPENAI_API_KEY.",
    )
    m04_pilot = subparsers.add_parser(
        "execute-m04-buyer-approver-accountant-vendor-pilot",
        help="Execute frozen M04 buyer+approver+accountant+vendor full-path pilot and write curated results.",
    )
    m04_pilot.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Raw M04 output directory under ignored runs/. Must be new or empty.",
    )
    m04_pilot.add_argument(
        "--curated-output",
        required=True,
        type=Path,
        help="Curated M04 pilot output directory. Must be new or empty.",
    )
    m04_pilot.add_argument(
        "--dotenv",
        default=Path(".env"),
        type=Path,
        help="Optional dotenv file containing OPENAI_API_KEY.",
    )
    m05_pilot = subparsers.add_parser(
        "execute-m05-full-org-payment-pilot",
        help="Execute frozen M05 requester+vendor+buyer+approver+accountant pilot and write curated results.",
    )
    m05_pilot.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Raw M05 output directory under ignored runs/. Must be new or empty.",
    )
    m05_pilot.add_argument(
        "--curated-output",
        required=True,
        type=Path,
        help="Curated M05 pilot output directory. Must be new or empty.",
    )
    m05_pilot.add_argument(
        "--dotenv",
        default=Path(".env"),
        type=Path,
        help="Optional dotenv file containing OPENAI_API_KEY.",
    )
    multi_role_sweep = subparsers.add_parser(
        "execute-multi-role-scenario-sweep-pilot",
        help="Execute frozen requester+vendor+buyer+approver+accountant S01-S06 scenario sweep pilot and write curated results.",
    )
    multi_role_sweep.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Raw sweep output directory under ignored runs/. Must be new or empty.",
    )
    multi_role_sweep.add_argument(
        "--curated-output",
        required=True,
        type=Path,
        help="Curated scenario sweep pilot output directory. Must be new or empty.",
    )
    multi_role_sweep.add_argument(
        "--count-per-scenario",
        default=3,
        type=int,
        help="Number of attempted runs per scenario before exclusions. Defaults to 3.",
    )
    multi_role_sweep.add_argument(
        "--batch-id",
        default=DEFAULT_MULTI_ROLE_SWEEP_BATCH_ID,
        help="Stable batch id prefix used for per-run ids.",
    )
    multi_role_sweep.add_argument(
        "--dotenv",
        default=Path(".env"),
        type=Path,
        help="Optional dotenv file containing OPENAI_API_KEY.",
    )
    multi_role_baseline = subparsers.add_parser(
        "execute-multi-role-baseline",
        help="Execute frozen EXP-0002 requester+vendor+buyer+approver+accountant baseline and write curated results.",
    )
    multi_role_baseline.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Raw baseline output directory under ignored runs/. Must be new or empty.",
    )
    multi_role_baseline.add_argument(
        "--results-output",
        required=True,
        type=Path,
        help="Curated baseline result directory. Must be new or empty.",
    )
    multi_role_baseline.add_argument(
        "--count-per-scenario",
        default=5,
        type=int,
        help="Number of attempted runs per scenario before exclusions. Defaults to 5.",
    )
    multi_role_baseline.add_argument(
        "--batch-id",
        default=DEFAULT_MULTI_ROLE_BASELINE_BATCH_ID,
        help="Stable batch id prefix used for per-run ids.",
    )
    multi_role_baseline.add_argument(
        "--dotenv",
        default=Path(".env"),
        type=Path,
        help="Optional dotenv file containing OPENAI_API_KEY.",
    )
    provider_randomness_sensitivity = subparsers.add_parser(
        "execute-provider-randomness-sensitivity",
        help="Execute frozen EXP-0004 provider-randomness sensitivity run and write curated results.",
    )
    provider_randomness_sensitivity.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Raw sensitivity output directory under ignored runs/. Must be new or empty.",
    )
    provider_randomness_sensitivity.add_argument(
        "--results-output",
        required=True,
        type=Path,
        help="Curated EXP-0004 result directory. Must be new or empty.",
    )
    provider_randomness_sensitivity.add_argument(
        "--count-per-scenario",
        default=DEFAULT_PROVIDER_RANDOMNESS_SENSITIVITY_COUNT,
        type=int,
        help="Number of attempted runs per scenario before exclusions. Defaults to 2.",
    )
    provider_randomness_sensitivity.add_argument(
        "--batch-id",
        default=DEFAULT_PROVIDER_RANDOMNESS_SENSITIVITY_BATCH_ID,
        help="Stable batch id prefix used for per-run ids.",
    )
    provider_randomness_sensitivity.add_argument(
        "--dotenv",
        default=Path(".env"),
        type=Path,
        help="Optional dotenv file containing OPENAI_API_KEY.",
    )

    args = parser.parse_args(argv)
    if args.command == "generate-s04":
        output = args.output
        if output.exists() and any(output.iterdir()):
            parser.error(f"output directory is not empty: {output}")
        run_s04(output_dir=output, run_id=args.run_id)
        print(output)
        return 0
    if args.command == "generate-s04-buyer-llm":
        output = args.output
        if output.exists() and any(output.iterdir()):
            parser.error(f"output directory is not empty: {output}")
        provider = OpenAIResponsesProvider.from_env(dotenv_path=args.dotenv, model=args.model)
        run_s04_buyer_llm(output_dir=output, provider=provider, run_id=args.run_id)
        print(output)
        return 0
    if args.command == "generate-s04-buyer-free-choice-llm":
        output = args.output
        if output.exists() and any(output.iterdir()):
            parser.error(f"output directory is not empty: {output}")
        provider = OpenAIResponsesProvider.from_env(dotenv_path=args.dotenv, model=args.model)
        run_s04_buyer_free_choice_llm(output_dir=output, provider=provider, run_id=args.run_id)
        print(output)
        return 0
    if args.command == "generate-s04-buyer-free-choice-batch":
        output = args.output
        curated_output = args.curated_output
        if output.exists() and any(output.iterdir()):
            parser.error(f"output directory is not empty: {output}")
        if curated_output.exists() and any(curated_output.iterdir()):
            parser.error(f"curated output directory is not empty: {curated_output}")
        provider = OpenAIResponsesProvider.from_env(dotenv_path=args.dotenv, model=args.model)
        run_s04_buyer_free_choice_batch(
            output_root=output,
            curated_output=curated_output,
            provider=provider,
            count=args.count,
            batch_id=args.batch_id,
        )
        print(curated_output)
        return 0
    if args.command == "generate-buyer-scenario-sweep":
        output = args.output
        curated_output = args.curated_output
        if output.exists() and any(output.iterdir()):
            parser.error(f"output directory is not empty: {output}")
        if curated_output.exists() and any(curated_output.iterdir()):
            parser.error(f"curated output directory is not empty: {curated_output}")
        provider = OpenAIResponsesProvider.from_env(dotenv_path=args.dotenv, model=args.model)
        run_buyer_scenario_sweep(
            output_root=output,
            curated_output=curated_output,
            provider=provider,
            count_per_scenario=args.count_per_scenario,
            batch_id=args.batch_id,
        )
        print(curated_output)
        return 0
    if args.command == "execute-buyer-only-baseline":
        output = args.output
        results_output = args.results_output
        if output.exists() and any(output.iterdir()):
            parser.error(f"output directory is not empty: {output}")
        if results_output.exists() and any(results_output.iterdir()):
            parser.error(f"results output directory is not empty: {results_output}")
        provider = OpenAIResponsesProvider.from_env(dotenv_path=args.dotenv, model="gpt-4.1-mini")
        run_buyer_only_baseline(
            output_root=output,
            results_output=results_output,
            provider=provider,
        )
        print(results_output)
        return 0
    if args.command == "execute-m01-buyer-approver-pilot":
        output = args.output
        curated_output = args.curated_output
        if output.exists() and any(output.iterdir()):
            parser.error(f"output directory is not empty: {output}")
        if curated_output.exists() and any(curated_output.iterdir()):
            parser.error(f"curated output directory is not empty: {curated_output}")
        provider = OpenAIResponsesProvider.from_env(dotenv_path=args.dotenv, model="gpt-4.1-mini")
        run_m01_buyer_approver_pilot(
            output_root=output,
            curated_output=curated_output,
            provider=provider,
        )
        print(curated_output)
        return 0
    if args.command == "execute-m02-buyer-vendor-pressure-pilot":
        output = args.output
        curated_output = args.curated_output
        if output.exists() and any(output.iterdir()):
            parser.error(f"output directory is not empty: {output}")
        if curated_output.exists() and any(curated_output.iterdir()):
            parser.error(f"curated output directory is not empty: {curated_output}")
        provider = OpenAIResponsesProvider.from_env(dotenv_path=args.dotenv, model="gpt-4.1-mini")
        run_m02_buyer_vendor_pressure_pilot(
            output_root=output,
            curated_output=curated_output,
            provider=provider,
        )
        print(curated_output)
        return 0
    if args.command == "execute-m03-buyer-approver-accountant-coordination-pilot":
        output = args.output
        curated_output = args.curated_output
        if output.exists() and any(output.iterdir()):
            parser.error(f"output directory is not empty: {output}")
        if curated_output.exists() and any(curated_output.iterdir()):
            parser.error(f"curated output directory is not empty: {curated_output}")
        provider = OpenAIResponsesProvider.from_env(dotenv_path=args.dotenv, model="gpt-4.1-mini")
        run_m03_coordination_pilot(
            output_root=output,
            curated_output=curated_output,
            provider=provider,
        )
        print(curated_output)
        return 0
    if args.command == "execute-m04-buyer-approver-accountant-vendor-pilot":
        output = args.output
        curated_output = args.curated_output
        if output.exists() and any(output.iterdir()):
            parser.error(f"output directory is not empty: {output}")
        if curated_output.exists() and any(curated_output.iterdir()):
            parser.error(f"curated output directory is not empty: {curated_output}")
        provider = OpenAIResponsesProvider.from_env(dotenv_path=args.dotenv, model="gpt-4.1-mini")
        run_m04_full_role_pilot(
            output_root=output,
            curated_output=curated_output,
            provider=provider,
        )
        print(curated_output)
        return 0
    if args.command == "execute-m05-full-org-payment-pilot":
        output = args.output
        curated_output = args.curated_output
        if output.exists() and any(output.iterdir()):
            parser.error(f"output directory is not empty: {output}")
        if curated_output.exists() and any(curated_output.iterdir()):
            parser.error(f"curated output directory is not empty: {curated_output}")
        provider = OpenAIResponsesProvider.from_env(dotenv_path=args.dotenv, model="gpt-4.1-mini")
        run_m05_full_org_payment_pilot(
            output_root=output,
            curated_output=curated_output,
            provider=provider,
        )
        print(curated_output)
        return 0
    if args.command == "execute-multi-role-scenario-sweep-pilot":
        output = args.output
        curated_output = args.curated_output
        if output.exists() and any(output.iterdir()):
            parser.error(f"output directory is not empty: {output}")
        if curated_output.exists() and any(curated_output.iterdir()):
            parser.error(f"curated output directory is not empty: {curated_output}")
        provider = OpenAIResponsesProvider.from_env(dotenv_path=args.dotenv, model="gpt-4.1-mini")
        run_multi_role_scenario_sweep_pilot(
            output_root=output,
            curated_output=curated_output,
            provider=provider,
            count_per_scenario=args.count_per_scenario,
            batch_id=args.batch_id,
        )
        print(curated_output)
        return 0
    if args.command == "execute-multi-role-baseline":
        output = args.output
        results_output = args.results_output
        if output.exists() and any(output.iterdir()):
            parser.error(f"output directory is not empty: {output}")
        if results_output.exists() and any(results_output.iterdir()):
            parser.error(f"results output directory is not empty: {results_output}")
        provider = OpenAIResponsesProvider.from_env(dotenv_path=args.dotenv, model="gpt-4.1-mini")
        run_multi_role_baseline(
            output_root=output,
            results_output=results_output,
            provider=provider,
            count_per_scenario=args.count_per_scenario,
            batch_id=args.batch_id,
        )
        print(results_output)
        return 0
    if args.command == "execute-provider-randomness-sensitivity":
        output = args.output
        results_output = args.results_output
        if output.exists() and any(output.iterdir()):
            parser.error(f"output directory is not empty: {output}")
        if results_output.exists() and any(results_output.iterdir()):
            parser.error(f"results output directory is not empty: {results_output}")
        provider = OpenAIResponsesProvider.from_env(dotenv_path=args.dotenv, model="gpt-4.1-mini")
        run_provider_randomness_sensitivity(
            output_root=output,
            results_output=results_output,
            provider=provider,
            count_per_scenario=args.count_per_scenario,
            batch_id=args.batch_id,
        )
        print(results_output)
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2
