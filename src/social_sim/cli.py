from __future__ import annotations

import argparse
from pathlib import Path

from .baseline_runner import run_buyer_only_baseline
from .free_choice_runner import run_s04_buyer_free_choice_llm
from .llm_actor import OpenAIResponsesProvider
from .repeated_runner import DEFAULT_REPEATED_BATCH_ID, run_s04_buyer_free_choice_batch
from .runner import run_s04, run_s04_buyer_llm
from .scenario_sweep_runner import DEFAULT_SWEEP_BATCH_ID, run_buyer_scenario_sweep


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

    parser.error(f"unknown command: {args.command}")
    return 2
