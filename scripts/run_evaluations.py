#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


BENCHMARK_DIR = ""
DEFAULT_MANIFEST = ""
DEFAULT_RESULTS_DIR = ""


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run all dataset-specific eval sets from a shared manifest.")
    p.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    p.add_argument("--results-dir", default=str(DEFAULT_RESULTS_DIR))
    p.add_argument("--api-base", default="")
    p.add_argument("--api-key", default="")
    p.add_argument("--model", default="")
    p.add_argument("--concurrency", type=int, default=16)
    p.add_argument("--max-tokens", type=int, default=512)
    p.add_argument("--temperature", type=float, default=0.01)
    p.add_argument("--retries", type=int, default=3)
    p.add_argument("--timeout-sec", type=float, default=60.0)
    p.add_argument("--limit", type=int, default=0)
    return p.parse_args()


def load_manifest(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def model_to_slug(model: str) -> str:
    text = str(model).strip()
    if not text:
        return "unknown_model"
    text = text.replace("/", "_").replace(".", "-")
    text = re.sub(r"[^A-Za-z0-9_-]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "unknown_model"


def resolve_results_dir(base_results_dir: Path, model: str) -> Path:
    return base_results_dir / model_to_slug(model)


def env_with_overrides(args: argparse.Namespace) -> dict[str, str]:
    env = os.environ.copy()
    if args.api_base:
        env["OPENAI_API_BASE"] = args.api_base
    if args.api_key:
        env["OPENAI_API_KEY"] = args.api_key
    return env


def build_command(entry: dict, args: argparse.Namespace, results_dir: Path) -> list[str]:
    output_path = results_dir / f"{entry['slug']}_eval_results.jsonl"
    cmd = [
        sys.executable,
        str(Path(__file__).resolve().with_name("run_pilot_eval.py")),
        "--input",
        str(entry["eval_jsonl"]),
        "--output",
        str(output_path),
        "--model",
        str(args.model),
        "--concurrency",
        str(args.concurrency),
        "--max-tokens",
        str(args.max_tokens),
        "--temperature",
        str(args.temperature),
        "--retries",
        str(args.retries),
        "--timeout-sec",
        str(args.timeout_sec),
        "--frame-dir-default",
    ]
    if args.limit > 0:
        cmd.extend(["--limit", str(args.limit)])
    return cmd


async def run_one(cmd: list[str], env: dict[str, str]) -> int:
    proc = await asyncio.create_subprocess_exec(*cmd, env=env)
    return await proc.wait()


async def main_async(args: argparse.Namespace) -> None:
    manifest_path = Path(args.manifest)
    manifest = load_manifest(manifest_path)
    results_dir = resolve_results_dir(Path(args.results_dir), args.model)
    results_dir.mkdir(parents=True, exist_ok=True)
    env = env_with_overrides(args)

    run_rows: list[dict] = []
    for entry in manifest.get("datasets", []):
        cmd = build_command(entry, args, results_dir)
        print(f"[RUN] {entry['dataset']} -> {' '.join(cmd)}", flush=True)
        rc = await run_one(cmd, env)
        run_rows.append(
            {
                "dataset": entry["dataset"],
                "slug": entry["slug"],
                "returncode": int(rc),
                "result_jsonl": str(results_dir / f"{entry['slug']}_eval_results.jsonl"),
            }
        )
        if rc != 0:
            raise SystemExit(f"Eval failed for {entry['dataset']} with code {rc}")

    run_summary = {
        "manifest": str(manifest_path),
        "results_dir": str(results_dir),
        "model": args.model,
        "model_slug": model_to_slug(args.model),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "runs": run_rows,
    }
    (results_dir / "run_all_eval_sets_summary.json").write_text(
        json.dumps(run_summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(run_summary, ensure_ascii=False, indent=2))


def main() -> None:
    args = parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
