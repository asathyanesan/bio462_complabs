#!/usr/bin/env bash
# Instructor provisioning; students must not modify the shared environment.
set -euo pipefail
umask 0027
export PYTHONNOUSERSITE=1
export PYTHONDONTWRITEBYTECODE=1

ENV_DIR="${1:-/fs/ess/PNS0503/envs/esm3}"
CLASS_JUPYTER=/fs/ess/PNS0503/BIOLOGICAL_DISCOVERY_DAYTON/jupyter
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

if [[ -e "$ENV_DIR" && "${2:-}" != "--resume" ]]; then
    echo "Environment already exists: $ENV_DIR; use --resume only for a failed build." >&2
    exit 1
fi

module load miniconda3/24.1.2-py310
if [[ ! -e "$ENV_DIR" ]]; then
    conda create --yes --prefix "$ENV_DIR" python=3.10 pip
fi
PYTHON="$ENV_DIR/bin/python"

# Matched PyTorch/torchtext releases with CUDA 12.1 support for the class A100 GPUs.
"$PYTHON" -m pip install --no-cache-dir --no-compile \
    torch==2.3.0 torchvision==0.18.0 \
    --index-url https://download.pytorch.org/whl/cu121
"$PYTHON" -m pip install --no-cache-dir --no-compile \
    -r "$SCRIPT_DIR/requirements.txt"
"$PYTHON" -m pip check
"$PYTHON" - <<'PY'
import torch
from esm.models.esm3 import ESM3
from esm.sdk.api import ESMProtein, GenerationConfig
from esm.utils.structure.protein_chain import ProteinChain
print("ESM3 imports OK; torch:", torch.__version__)
PY

"$PYTHON" -m ipykernel install --prefix "$CLASS_JUPYTER" \
    --name esm3 --display-name "Python (BIO 462/594 Lab 2 - ESM3)"
"$PYTHON" - "$CLASS_JUPYTER/share/jupyter/kernels/esm3/kernel.json" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
spec = json.loads(path.read_text())
spec["env"] = {
    "PYTHONNOUSERSITE": "1",
    "PYTHONDONTWRITEBYTECODE": "1",
    "HF_HOME": "/fs/ess/PNS0503/hf_cache",
    "HF_HUB_CACHE": "/fs/ess/PNS0503/hf_cache/hub",
    "HF_HUB_OFFLINE": "1",
    "HF_HUB_DISABLE_IMPLICIT_TOKEN": "1",
    "ESM3_HF_CACHE": "/fs/ess/PNS0503/hf_cache",
    "OMP_NUM_THREADS": "4",
}
path.write_text(json.dumps(spec, indent=2) + "\n")
PY
setfacl -R -P -m g::r-X,g:PNS0503:r-X,o::--- \
    "$ENV_DIR" "$CLASS_JUPYTER/share/jupyter/kernels/esm3"
find "$ENV_DIR" "$CLASS_JUPYTER/share/jupyter/kernels/esm3" -type d \
    -exec setfacl -m d:u::rwx,d:g::r-x,d:g:PNS0503:r-x,d:m::r-x,d:o::--- {} +
echo "Shared ESM3 kernel installed. Next run: $PYTHON $SCRIPT_DIR/stage_weights.py"
