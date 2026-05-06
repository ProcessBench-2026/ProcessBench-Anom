#!/usr/bin/env python3
"""
从已评分的 JSONL 文件中统计整体及各题型(task_type)的正确率。
输入格式示例每行:
{"index": 0, "dataset": "GM100", "task_type": "T1", "task_id": "task_00001", 
 "recording_id": "None", "gold_answer": "B", "pred_answer": "B", 
 "raw_prediction": "B. approach", "correct": true}
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="score results"
    )
    p.add_argument("jsonl_file", default="")
    p.add_argument(
        "--output-json", 
        default="", 
    )
    return p.parse_args()

def main() -> None:
    args = parse_args()
    jsonl_path = Path(args.jsonl_file)
    if not jsonl_path.exists():
        raise FileNotFoundError(f"could not find: {jsonl_path}")

    # 数据结构: {task_type: {"correct": int, "total": int}}
    task_stats: dict[str, dict[str, int]] = defaultdict(lambda: {"correct": 0, "total": 0})
    dataset_stats: dict[str, dict[str, int]] = defaultdict(lambda: {"correct": 0, "total": 0})
    
    overall_correct = 0
    overall_total = 0
    invalid_lines = 0

    with jsonl_path.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"⚠️ Line {line_no} JSON parsing failed, skipped: {e}")
                invalid_lines += 1
                continue

            task_type = str(row.get("task_type", "UNKNOWN")).strip()
            dataset = str(row.get("dataset", "UNKNOWN")).strip()
            is_correct = bool(row.get("correct", False))

            # 累加题型统计
            task_stats[task_type]["total"] += 1
            if is_correct:
                task_stats[task_type]["correct"] += 1

            # 累加数据集统计（可选扩展）
            dataset_stats[dataset]["total"] += 1
            if is_correct:
                dataset_stats[dataset]["correct"] += 1

            # 全局统计
            overall_total += 1
            if is_correct:
                overall_correct += 1

    if overall_total == 0:
        print("❌ File contains no valid data lines.")
        return

    print("\n" + "=" * 50)
    print(f"{'Task Type':<18} {'Accuracy':>8} {'Correct':>6} {'Total':>6} {'Incorrect':>6}")
    print("-" * 50)
    for task_type in sorted(task_stats.keys()):
        stats = task_stats[task_type]
        acc = stats["correct"] / stats["total"]
        print(f"{task_type:<18} {acc*100:>7.2f}% {stats['correct']:>6} {stats['total']:>6} {stats['total']-stats['correct']:>6}")
    print("=" * 50)

    overall_acc = overall_correct / overall_total
    print(f"{'Overall':<18} {overall_acc*100:>7.2f}% {overall_correct:>6} {overall_total:>6} {overall_total-overall_correct:>6}")
    print(f"⚠️ Skipped invalid lines: {invalid_lines}\n")

    if args.output_json:
        out_path = Path(args.output_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        
        summary = {
            "source_file": str(jsonl_path.resolve()),
            "overall_accuracy": round(overall_acc, 4),
            "overall_correct": overall_correct,
            "overall_total": overall_total,
            "skipped_lines": invalid_lines,
            "by_task_type": {
                k: {
                    "accuracy": round(v["correct"] / v["total"], 4) if v["total"] > 0 else 0.0,
                    "correct": v["correct"],
                    "total": v["total"],
                    "incorrect": v["total"] - v["correct"]
                } for k, v in task_stats.items()
            },
            "by_dataset": {
                k: {
                    "accuracy": round(v["correct"] / v["total"], 4) if v["total"] > 0 else 0.0,
                    "correct": v["correct"],
                    "total": v["total"]
                } for k, v in dataset_stats.items()
            }
        }
        out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"📁 Detailed statistics saved to: {out_path.resolve()}")


if __name__ == "__main__":
    main()