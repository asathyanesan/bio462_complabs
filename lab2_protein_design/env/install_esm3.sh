#!/usr/bin/env bash
# =============================================================================
# install_esm3.sh — one-time ESM3 environment build for BIO 462/594 Comp Lab 2
# Run ON THE OSC PITZER GPU NODE (srun --gres=gpu:1) with the cuda module loaded:
#     module load cuda
#     bash install_esm3.sh /fs/ess/PNS0503/envs/esm3
# ~10-15 min including the CUDA kernel install. Weights are staged separately
# (see STAGE_WEIGHTS below) — this script only builds the environment.
# =============================================================================
set -euo pipefail

ENV_DIR="${1:-/fs/ess/PNS0503/envs/esm3}"

echo "== 1/4 creating venv at ${ENV_DIR} =="
python3.11 -m venv "${ENV_DIR}" || { echo "python3.11 not found; try: module load python/3.11"; exit 1; }
source "${ENV_DIR}/bin/activate"

echo "== 2/4 installing torch (cu121) =="
pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cu121

echo "== 3/4 installing esm + deps =="
# 'esm[gpu]' adds xformers + cuequivariance CUDA kernels (Linux x86-64)
pip install --no-cache-dir "esm[gpu]" || pip install --no-cache-dir esm
pip install --no-cache-dir py3Dmol matplotlib pandas ipykernel nbconvert nbformat

echo "== 4/4 registering Jupyter kernel + smoke test =="
python -m ipykernel install --user --name esm3 --display-name "Python 3 (esm3)"

python - << 'EOF'
import torch
print("torch:", torch.__version__, "| cuda available:", torch.cuda.is_available())
from esm.models.esm3 import ESM3          # noqa: F401  (import check only; weights staged separately)
from esm.sdk.api import ESMProtein, GenerationConfig
from esm.utils.structure.protein_chain import ProteinChain
print("ESM3 READY  (run STAGE_WEIGHTS block to download weights once)")
EOF

# =============================================================================
# STAGE_WEIGHTS — one-time, run by the INSTRUCTOR (needs your HuggingFace token):
#   1. Create a HF account, open https://huggingface.co/EvolutionaryScale/esm3
#   2. Accept the EvolutionaryScale Community License, create a token (Read permission)
#   3. On a GPU node:  export HF_TOKEN=<your token>  then:
#      source /fs/ess/PNS0503/envs/esm3/bin/activate
#      python stage_weights.py /fs/ess/PNS0503/hf_cache
#   Students then load offline from that cache — no token, no internet needed in class.
# =============================================================================
