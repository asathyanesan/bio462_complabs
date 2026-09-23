"""Download the Lab 3 dataset (Su et al. 2020 COVID PBMC, CELLxGENE).

Run once before class. The dataset is saved next to this script (in data/),
regardless of the directory from which the script is launched.
217 MB download. The Immune_All_Low.pkl CellTypist model is already included.
"""
from pathlib import Path
import urllib.request

URL = "https://datasets.cellxgene.cziscience.com/8d7fad46-2f37-4aa0-ac9d-babbc36efb6f.h5ad"
DEST = Path(__file__).with_name("su2020_pbmc_covid.h5ad")

print(f"downloading {URL} -> {DEST} (217 MB)...")
urllib.request.urlretrieve(URL, DEST)
print("done")
