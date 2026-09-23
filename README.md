# BIO 462/594 Molecular Biology — Computational Labs

Fall 2026, University of Dayton. Labs run on the Ohio Supercomputer Center (OSC) Pitzer cluster
via OnDemand Jupyter.

| Lab | Date | Topic | Report due |
|---|---|---|---|
| 1 | Tue Sep 29 | Variant interpretation (AlphaMissense + ClinVar + ACMG) | Oct 13 |
| 2 | Thu Nov 5 | Protein structure prediction (ESMFold, pLDDT/PAE) | Nov 12 |
| 3 | Thu Dec 3 | Single-cell annotation of COVID PBMCs (Scanpy + CellTypist) | Dec 11 |

## In class — first step

Log in to [OSC OnDemand](https://ondemand.osc.edu), open Jupyter, open a Terminal, and clone
**your own copy** (never edit a shared folder):

```bash
cd ~
git clone https://github.com/aaronsathya/bio462_594_complabs.git
```

Then change into that day's lab directory before opening the notebook. This keeps the notebook's
relative `data/` paths working in Jupyter:

```bash
cd ~/bio462_594_complabs/lab1_variant_interpretation   # or lab2_structure / lab3_singlecell
```

Open `Lab1_Student.ipynb` (or the notebook for the day), select the kernel your instructor
announces, and run from the top. Keep the clone in your home directory so each student has a
private working copy.

## Lab 3 — one extra step (217 MB dataset)

The single-cell dataset is too large for GitHub. After cloning, run once:

```bash
cd ~/bio462_594_complabs/lab3_singlecell
python data/download_dataset.py
```

The dataset is saved in `lab3_singlecell/data/`, where the notebook expects it. You can run the
command from any directory by using the script's full path. Do this during the pre-class buffer —
the download takes about a minute on OSC.

## Lab 2 — environment

Lab 2 uses a pre-built `esmfold` environment on OSC. Select the kernel your instructor announces;
you do not need to install anything. Do not run `env/install_esmfold.sh`; it is for instructor
provisioning only.

## Notebooks

Each notebook runs top-to-bottom as-is. Short **"Your turn"** exercises ask for short answers or
small code edits — no coding background assumed. Figures you generate are saved next to the
notebook in your own clone.
