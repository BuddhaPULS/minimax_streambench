# Evaluating MiniMax-M2.7 on Text-to-SQL with StreamBench

Streaming vs. non-streaming prompting methods on the CoSQL benchmark.

This project evaluates **MiniMax-M2.7** on the **CoSQL** text-to-SQL benchmark using the [StreamBench](https://github.com/stream-bench/stream-bench) framework. It compares three non-streaming baselines against three streaming in-context learning methods to provide an objective view of MiniMax-M2.7's capabilities for developers choosing an LLM API for text-to-SQL tasks.

## Dataset

[CoSQL](https://yale-lily.github.io/cosql) is a cross-domain conversational text-to-SQL dataset of medium difficulty. The task is to convert a user's natural language query into a SQL statement that retrieves the correct data from a given database.

## Methods

### Non-Streaming Baselines
- **Zero-shot**: Prompts the model with the schema and query only — tests raw instruction-following ability.
- **Few-shot**: Provides several ground-truth (query, SQL) pairs in the prompt as demonstrations.
- **Self-Refine**: The model iteratively improves its output based on its own feedback.

### Streaming Methods
- **GrowPrompt**: Maintains a sliding window of recent (input, output, feedback) triples, incorporated into the prompt at inference time.
- **MemPrompt**: Stores all past (input, output, feedback) triples; a retriever selects the most relevant ones at inference time.
- **Self-StreamICL**: Stores only past correct outputs and incorporates them as demonstrations during inference.

## Results

| Method | Execution Accuracy (%) |
| :--- | :---: |
| Zero-shot | 54.75 |
| Few-shot | 54.83 |
| Self-Refine | 52.31 |
| GrowPrompt | 54.86 |
| MemPrompt | 53.02 |
| Self-StreamICL | 54.94 |

Streaming and non-streaming methods achieve similar execution accuracy (~54%). MemPrompt and Self-StreamICL marginally outperform the zero-shot baseline, suggesting that retrieving relevant past examples provides a small but consistent benefit on this benchmark.

## Project Structure

```
stream-bench/
├── configs/
│   ├── agent/minimax/        # Agent configs for each method (zeroshot, fewshot, etc.)
│   └── bench/                # Benchmark configs (cosql.yml, spider.yml, etc.)
├── stream_bench/
│   ├── agents/               # Agent implementations (ZeroShot, FewShot, GrowPrompt, etc.)
│   ├── benchmarks/           # Benchmark dataset loaders
│   ├── llms/
│   │   └── minimax.py        # MiniMax LLM integration
│   └── pipelines/            # Main entry point (run_bench.py)
├── scripts/
│   └── run_minimax_text2sql.sh  # Script to reproduce all experiments
├── data/                     # Dataset files (downloaded separately, not in repo)
├── download_text2sql_data.py # Script to download CoSQL/Spider/Bird datasets
└── requirements.txt
```

## Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/<your-username>/stream-bench.git
cd stream-bench
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Download the CoSQL dataset**
```bash
python download_text2sql_data.py
```

**4. Set your MiniMax API key**
```bash
export MINIMAX_API_KEY="your_api_key_here"
```

Get a MiniMax API key at [minimax.io](https://minimax.io).

## How to Run

**Run a single experiment:**
```bash
python -m stream_bench.pipelines.run_bench \
  --agent_cfg configs/agent/minimax/zeroshot.yml \
  --bench_cfg configs/bench/cosql.yml
```

**Reproduce all results** — edit `scripts/run_minimax_text2sql.sh` to set the desired agents, then:
```bash
bash scripts/run_minimax_text2sql.sh
```

Add `--use_wandb` to log metrics to [Weights & Biases](https://wandb.ai).

## Acknowledgment

This project is built on top of the [StreamBench](https://github.com/stream-bench/stream-bench) framework. We extend it with MiniMax LLM support and evaluate MiniMax-M2.7 on text-to-SQL tasks.
