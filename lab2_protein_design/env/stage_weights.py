#!/usr/bin/env python
"""Instructor-only staging of public MIT-licensed ESM3 weights.

Run with the shared environment's Python after install_esm3.sh:
    python stage_weights.py /fs/ess/PNS0503/hf_cache

No Hugging Face login is required. Verify offline loading in a fresh process.
"""
import os
import sys
from pathlib import Path
import subprocess

cache = sys.argv[1] if len(sys.argv) > 1 else "/fs/ess/PNS0503/hf_cache"
os.umask(0o027)
os.environ["HF_HOME"] = cache
os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"
os.environ.pop("HF_HUB_OFFLINE", None)
os.environ.pop("HF_HUB_CACHE", None)

from huggingface_hub import snapshot_download  # noqa: E402

# Keep the original repository ID: esm 3.2.1 uses it for offline cache lookup.
print("Downloading public ESM3 weights into", cache, "...", flush=True)
snapshot_download(
    repo_id="EvolutionaryScale/esm3-sm-open-v1",
    cache_dir=str(Path(cache) / "hub"),
    token=False,
)
offline_env = os.environ.copy()
offline_env["HF_HUB_OFFLINE"] = "1"
subprocess.run(
    [sys.executable, "-c",
     "from esm.models.esm3 import ESM3; "
     "model = ESM3.from_pretrained('esm3-open'); "
     "print('OFFLINE LOAD VERIFIED - ESM3 READY')"],
    env=offline_env,
    check=True,
)

# Include cache metadata created during the first model load.
subprocess.run(
    ["setfacl", "-R", "-P", "-m", "g::r-X,g:PNS0503:r-X,o::---", cache],
    check=True,
)
for root, dirs, files in os.walk(cache):
    subprocess.run(
        ["setfacl", "-m",
         "d:u::rwx,d:g::r-x,d:g:PNS0503:r-x,d:m::r-x,d:o::---", root],
        check=True,
    )
