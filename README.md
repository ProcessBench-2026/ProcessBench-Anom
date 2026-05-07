# RoboProcessBench

RoboProcessBench is a comprehensive benchmark for evaluating robotic process learning and understanding. This repository contains the evaluation suite, dataset utilities, and scoring tools for the RoboProcessBench paper.

## Repository Contents

- **`scripts/`** — Evaluation and data processing scripts
  - `download_hf_artifacts.py` — Download benchmark datasets from Hugging Face
  - `score_evaluations.py` — Score model predictions against benchmarks
  - `score_vlm.py` — Score vision language model predictions
  - `run_evaluations.py` — Execute full evaluation pipelines
  - `extract_frames_*.py` — Video frame extraction for various datasets (AIST++, GM-100, RH20T)
  - `split_sft_eval.py` — Split SFT and evaluation datasets
  - `eval_vlm.sh`, `post-train_vlm.sh` — VLM evaluation and post-training scripts

- **`configs/`** — Configuration files
  - YAML configs for evaluation, post-training, HF datasets, and SFT data processing

- **`docs/`** — Documentation
  - `quickstart.md` — Get started in 3 steps
  - `evaluation_protocol.md` — Detailed evaluation methodology

- **`data/`** — Data directory (populated after downloading artifacts)

- **`outputs/`** — Results and evaluation outputs

- **`environment.yml`** — Conda environment specification

- **`requirements.txt`** — Python package dependencies

## Repository Structure

```
ProcessBench-GitHub/
├── configs/                       # Configuration files
│   ├── evaluation.yaml
│   ├── post-train_lora.yaml
│   ├── hf_dataset.yaml
│   ├── processdata-sft-intern.yaml
│   └── processdata-sft-qwen.yaml
├── scripts/                       # Evaluation and processing scripts
│   ├── download_hf_artifacts.py
│   ├── score_vlm.py
│   ├── score_evaluations.py
│   ├── run_evaluations.py
│   ├── extract_frames_*.py
│   ├── split_sft_eval.py
│   ├── eval_vlm.sh
│   └── post-train_vlm.sh
├── docs/                          # Documentation
│   ├── quickstart.md
│   └── evaluation_protocol.md
├── data/                          # Benchmark datasets (download via scripts)
├── outputs/                       # Evaluation results
├── environment.yml                # Conda environment
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Quick Start

### 1. Install Environment

```bash
conda env create -f environment.yml
conda activate processbench
```

### 2. Download Benchmark Artifacts

```bash
python scripts/download_hf_artifacts.py \
  --repo ProcessBench-2026/RoboProcessBench \
  --out data/
```

### 3. Run Evaluations

```bash
python scripts/score_evaluations.py \
  --input data/predictions.jsonl \
  --output outputs/scores.json
```

### 4. View Results

Results are saved to `outputs/` in JSON format.

## Dependencies

- Python 3.11+
- PyYAML, Hugging Face Hub, Pillow, NumPy, Pandas, PyArrow
- Transformers, Datasets, PEFT, TRL, DeepSpeed, Accelerate
- LLamaFactory 0.9.3

See `requirements.txt` for full list.

## Documentation

- **[Quickstart Guide](docs/quickstart.md)** — Get up and running quickly
- **[Evaluation Protocol](docs/evaluation_protocol.md)** — Detailed benchmark methodology

## License

See [LICENSE](LICENSE) file for details.

See `docs/reconstruction.md` for how public release references map to upstream source episodes and recordings. Full visual reconstruction requires access to the upstream datasets under their original terms.

## Files To Read First

- `docs/quickstart.md`
- `docs/data_schema.md`
- `docs/evaluation_protocol.md`
- `docs/reconstruction.md`
- `docs/anonymization.md`

## Intended Use

- reproducing ProcessBench scoring logic
- validating public benchmark artifacts
- recomputing task-distribution tables and bootstrap CIs
- reproducing appendix-style evaluation summaries from hosted artifacts

## Out Of Scope

- redistributing upstream raw videos or full frame caches
- claiming deployment safety from benchmark score alone
- using this repo as a substitute for upstream dataset access
