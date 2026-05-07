# Quickstart

## 1. Install

```bash
conda env create -f environment.yml
conda activate processbench
```

## 2. Download Hugging Face artifacts

```bash
python scripts/download_hf_artifacts.py \
  --repo ProcessBench-2026/RoboProcessBench \
  --out data/
```

## 3. Score provided predictions

```bash
python scripts/score_vlm.py \
  data/ProcessData-SFT-Qwen_results/ProcessData-SFT-Qwen_predictions.json 
```

