from __future__ import annotations

import argparse
from pathlib import Path

from .llm_actor import OpenAIResponsesProvider
from .runner import run_s04, run_s04_buyer_llm


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

    parser.error(f"unknown command: {args.command}")
    return 2
