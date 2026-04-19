#!/bin/bash
set -e
export MINIMAX_API_KEY="your_minimax_api_key_here"

AGENTS=(self_stream_icl)
BENCHES=(cosql)

for bench in "${BENCHES[@]}"; do
  for agent in "${AGENTS[@]}"; do
    echo "=== $agent on $bench ==="
    python -m stream_bench.pipelines.run_bench \
      --agent_cfg "configs/agent/minimax/${agent}.yml" \
      --bench_cfg "configs/bench/${bench}.yml" \
      --use_wandb
  done
done
