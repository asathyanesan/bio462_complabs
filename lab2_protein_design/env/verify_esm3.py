#!/usr/bin/env python
"""Run on an A100 GPU with 32 GB RAM to verify the shared offline Lab 2 setup."""
import os
from pathlib import Path
import tempfile
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ["HF_HOME"] = "/fs/ess/PNS0503/hf_cache"
os.environ["HF_HUB_CACHE"] = "/fs/ess/PNS0503/hf_cache/hub"
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"
os.environ["OMP_NUM_THREADS"] = "4"

import torch
from esm.models.esm3 import ESM3
from esm.sdk.api import ESMProtein, ESMProteinError, GenerationConfig
from pdb_confidence import save_pdb_with_plddt

if not torch.cuda.is_available():
    raise RuntimeError("GPU validation requires an OSC allocation with --gres=gpu:1.")

print("GPU:", torch.cuda.get_device_name(0), flush=True)
model = ESM3.from_pretrained("esm3-open").to("cuda")
print("Offline model load OK", flush=True)
sequence = model.generate(
    ESMProtein(sequence="_" * 32),
    GenerationConfig(track="sequence", num_steps=2),
)
if isinstance(sequence, ESMProteinError):
    raise RuntimeError(f"Sequence generation failed: {sequence}")
assert sequence.sequence is not None and len(sequence.sequence) == 32
assert "_" not in sequence.sequence
structure = model.generate(
    sequence, GenerationConfig(track="structure", num_steps=2),
)
if isinstance(structure, ESMProteinError):
    raise RuntimeError(f"Structure generation failed: {structure}")
assert structure.coordinates is not None
assert structure.coordinates.shape == (32, 37, 3)
with tempfile.TemporaryDirectory(prefix="bio462-esm3-verify-") as directory:
    pdb = Path(directory) / "test.pdb"
    save_pdb_with_plddt(structure, str(pdb))
    atoms = [line for line in pdb.read_text().splitlines()
             if line.startswith("ATOM") and line[12:16].strip() == "CA"]
    assert len(atoms) == 32
    assert all(0 <= float(line[60:66]) <= 100 for line in atoms)
    assert any(float(line[60:66]) > 0 for line in atoms)
print("PASS: offline sequence + structure generation, 32 CA atoms, valid pLDDT", flush=True)
