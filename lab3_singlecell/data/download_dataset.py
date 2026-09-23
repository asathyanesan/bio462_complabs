"""Download the Lab 3 dataset (Su et al. 2020 COVID PBMC, CELLxGENE).

Run once before class; place su2020_pbmc_covid.h5ad next to this script (in data/).
217 MB download. The Immune_All_Low.pkl CellTypist model is already included.
"""
import urllib.request

URL = "https://datasets.cellxgene.cziscience.com/8d7fad46-2f37-4aa0-ac9d-babbc36efb6f.h5ad"
DEST = "su2020_pbmc_covid.h5ad"

print(f"downloading {URL} -> {DEST} (217 MB)...")
urllib.request.urlretrieve(URL, DEST)
print("done")
