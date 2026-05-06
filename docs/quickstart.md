# Quickstart

## 1. Install

```bash
conda env create -f environment.yml
conda activate processbench
```

## 2. Download Hugging Face artifacts

```bash
python scripts/download_hf_artifacts.py \
  --repo ProcessBench-2026/ProcessBench-Anom \
  --out data/
```

## 3. Validate public dataset artifacts

```bash
python scripts/validate_dataset.py \
  --eval data/processbench_eval.jsonl \
  --sft data/processdata_sft.jsonl \
  --task-distribution data/metadata/task_distribution.csv
```

## 4. Score provided predictions

```bash
python scripts/score_predictions.py \
  --predictions data/results/processeval_7b_predictions.jsonl \
  --split data/processbench_eval.jsonl \
  --output outputs/processeval_7b_scores.json
```

