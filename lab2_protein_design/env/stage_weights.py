#!/usr/bin/env python
"""stage_weights.py — one-time instructor step: download esm3-open weights into a shared cache.

Usage (on a GPU node, after install_esm3.sh):
    export HF_TOKEN=<your token>          # from huggingface.co, after accepting the
                                          # EvolutionaryScale Community License at
                                          # https://huggingface.co/EvolutionaryScale/esm3
    python stage_weights.py /fs/ess/PNS0503/hf_cache

After this succeeds, students never need a token: the notebook sets HF_HOME to the shared
cache and HF_HUB_OFFLINE=1.
"""
import os
import sys

cache = sys.argv[1] if len(sys.argv) > 1 else "/fs/ess/PNS0503/hf_cache"
os.environ["HF_HOME"] = cache
os.environ.pop("HF_HUB_OFFLINE", None)  # we ARE online here

from huggingface_hub import login  # noqa: E402
login()  # prompts for the token (or reads HF_TOKEN)

from esm.models.esm3 import ESM3  # noqa: E402
print("downloading esm3-open weights (~6 GB) into", cache, "...")
model = ESM3.from_pretrained("esm3-open")
print("weights cached OK")

# offline-load verification (what students will do)
os.environ["HF_HUB_OFFLINE"] = "1"
model2 = ESM3.from_pretrained("esm3-open")
print("OFFLINE LOAD VERIFIED — ESM3 READY")
