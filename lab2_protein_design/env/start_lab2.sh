#!/usr/bin/env bash
set -euo pipefail
umask 0077

LAB_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${1:-$HOME/bio462_lab2_protein_design}"
PYTHON=/fs/ess/PNS0503/envs/esm3/bin/python
KERNEL=/fs/ess/PNS0503/BIOLOGICAL_DISCOVERY_DAYTON/jupyter/share/jupyter/kernels/esm3

if [[ ! -x "$PYTHON" || ! -r "$KERNEL/kernel.json" ]]; then
    echo "The shared ESM3 environment is unavailable; contact your instructor." >&2
    exit 1
fi
if [[ -e "$DEST" ]]; then
    echo "Keeping existing work at $DEST (no files copied)."
else
    mkdir -p -- "$DEST"
    cp -- "$LAB_DIR/Lab2_Student.ipynb" "$DEST/"
    cp -- "$LAB_DIR/pdb_confidence.py" "$DEST/"
    cp -- "$LAB_DIR/sequence_comparison.py" "$DEST/"
    cp -R -- "$LAB_DIR/data" "$DEST/"
    chmod -R u+rwX,go-rwx -- "$DEST"
fi

# Also works in Jupyter sessions that do not use the classroom server prefix.
PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 "$PYTHON" -m jupyter kernelspec install --user --replace "$KERNEL"
echo "Open $DEST/Lab2_Student.ipynb"
echo "Select: Python (BIO 462/594 Lab 2 - ESM3)"
