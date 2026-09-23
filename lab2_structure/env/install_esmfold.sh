#!/bin/bash
# ============================================================================
# install_esmfold.sh — ESMFold environment for BIO 462/594 Comp Lab 2
# Ohio Supercomputer Center | Pitzer | project PNS0503
#
# Run this ONCE, on a GPU compute node (the CUDA kernel needs nvcc):
#   srun --cluster=pitzer --gres=gpu:A100:1 --mem=32G --time=01:00:00 --pty bash
#   module load cuda/12.x          (check `module avail cuda` for the version)
#   bash install_esmfold.sh /fs/ess/PNS0503/envs/esmfold
#
# Validated recipe (tested end-to-end on a CPU mirror of this environment):
#   python 3.10, torch 2.x, fair-esm 2.0.0, openfold @ 4d513bb (2022-08-31),
#   deepspeed 0.9.5, pytorch-lightning 1.9.5, numpy<2, setuptools<81,
#   plus three small source patches applied below.
# ============================================================================
set -e

ENV_PATH=${1:-/fs/ess/PNS0503/envs/esmfold}
PY=${2:-3.10}

echo "== creating conda env at $ENV_PATH (python $PY)"
module load miniconda3 2>/dev/null || true
conda create -y -p "$ENV_PATH" python="$PY"
source activate "$ENV_PATH" 2>/dev/null || conda activate "$ENV_PATH"

echo "== installing torch (CUDA-aware wheel)"
pip install torch --index-url https://download.pytorch.org/whl/cu121

echo "== installing fair-esm[esmfold] and pinned dependencies"
pip install "fair-esm[esmfold]"
pip install "deepspeed==0.9.5" "numpy<2" "pytorch-lightning==1.9.5" "setuptools<81"
pip install modelcif
pip install "git+https://github.com/NVIDIA/dllogger.git"

echo "== installing openfold @ 4d513bb (2022-08-31, checkpoint-compatible)"
# NOTE: --no-build-isolation so setup.py sees the installed torch.
pip install --no-build-isolation "git+https://github.com/aqlaboratory/openfold.git@4d513bb1d9c58b1ab412c455b2c9b576905c428a"

SITE=$(python -c "import openfold, os; print(os.path.dirname(openfold.__file__))")
echo "== applying three small patches in $SITE"

python - "$SITE" << 'EOF'
import sys, pathlib
site = pathlib.Path(sys.argv[1])

# Patch 1: StructureModule must return "states" (fair-esm 2.0.0 reads it)
p = site / 'model' / 'structure_module.py'
s = p.read_text()
old = '''            preds = {
                "frames": scaled_rigids.to_tensor_7(),
                "sidechain_frames": all_frames_to_global.to_tensor_4x4(),
                "unnormalized_angles": unnormalized_angles,
                "angles": angles,
                "positions": pred_xyz,
            }'''
new = old.replace('"positions": pred_xyz,', '"positions": pred_xyz,\n                "states": s,')
assert old in s, 'patch 1 anchor not found'
p.write_text(s.replace(old, new))

# Patch 2: tolerate a missing CUDA kernel (CPU-only installs)
for rel in ['model/structure_module.py', 'utils/kernel/attention_core.py']:
    p = site / rel
    s = p.read_text()
    old = 'attn_core_inplace_cuda = importlib.import_module("attn_core_inplace_cuda")'
    new = '''try:
    attn_core_inplace_cuda = importlib.import_module("attn_core_inplace_cuda")
except ModuleNotFoundError:
    attn_core_inplace_cuda = None  # CPU-only install'''
    if old in s:
        p.write_text(s.replace(old, new))

# Patch 3: deepspeed 0.9.5 lacks utils.is_initialized
p = site / 'model' / 'primitives.py'
s = p.read_text()
s = s.replace('deepspeed.utils.is_initialized()',
              "getattr(deepspeed.utils, 'is_initialized', lambda: False)()")
p.write_text(s)
print('patches applied')
EOF

echo "== smoke test: loading ESMFold weights (~3 GB download on first run)"
python - << 'EOF'
import esm, torch
m = esm.pretrained.esmfold_v1().eval()
print('ESMFOLD READY on', 'cuda' if torch.cuda.is_available() else 'cpu')
EOF

echo "== DONE. Next: register the kernel for OnDemand Jupyter (see walkthrough)."
