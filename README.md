# BIO 462/594 Molecular Biology: Computational Labs

Fall 2026, University of Dayton. Labs run on the Ohio Supercomputer Center (OSC) Pitzer cluster
via OnDemand Jupyter.

| Lab | Date | Topic | Report due |
|---|---|---|---|
| 1 | Tue Sep 29 | Variant interpretation (AlphaMissense + ClinVar + ACMG) | Oct 13 |
| 2 | Thu Nov 5 | Protein structure prediction (ESMFold, pLDDT/PAE) | Nov 12 |
| 3 | Thu Dec 3 | Single-cell annotation of COVID PBMCs (Scanpy + CellTypist) | Dec 11 |

## In class: first step

Log in to [OSC Classroom](https://class.osc.edu) and click **Classroom Jupyter**. Before starting
the session, use these settings for the lab:

| Parameter | Lab 1 (Sep 29) | Lab 2 (Nov 5) | Lab 3 (Dec 3) |
|---|---|---|---|
| Classroom | BIOLOGICAL DISCOVERY DAYTON | BIOLOGICAL DISCOVERY DAYTON | BIOLOGICAL DISCOVERY DAYTON |
| Size | **medium** (2 core / 8 GB) | **extra-large** (8 core / 32 GB) | **extra-large** (8 core / 32 GB) |
| Hours | 2 hours | 2 hours | 2 hours |
| GPUs | 0 | 1 | 0 |
| JupyterLab | Leave unchecked | Leave unchecked | Leave unchecked |

Students should work from their own copy, not a shared folder. Clone the repository into the
materials directory:

```bash
cd ~
cd /users/PNS0489/aaronsathya1/osc_classes/BIOLOGICAL_DISCOVERY_DAYTON/materials
git clone https://github.com/asathyanesan/bio462_complabs.git
```

In the Classroom Jupyter launch form, set **Project Directory** to
`/users/PNS0489/aaronsathya1/osc_classes/BIOLOGICAL_DISCOVERY_DAYTON/materials/bio462_complabs` instead of the default `$HOME`.

Then change into that day's lab directory before opening the notebook. This keeps the notebook's
relative `data/` paths working in Jupyter:

```bash
cd /users/PNS0489/aaronsathya1/osc_classes/BIOLOGICAL_DISCOVERY_DAYTON/materials/bio462_complabs/lab1_variant_interpretation   # or lab2_structure / lab3_singlecell
```

Open `Lab1_Student.ipynb` (or the notebook for the day), select the kernel your instructor
announces, and run from the top.

## Lab 3: one extra step (217 MB dataset)

The single-cell dataset is too large for GitHub. After cloning, run once:

```bash
cd /users/PNS0489/aaronsathya1/osc_classes/BIOLOGICAL_DISCOVERY_DAYTON/materials/bio462_complabs/lab3_singlecell
python data/download_dataset.py
```

The dataset is saved in `lab3_singlecell/data/`, where the notebook expects it. You can run the
command from any directory by using the script's full path. Do this during the pre-class buffer:
the download takes about a minute on OSC.

## Lab 2: environment

Lab 2 uses a pre-built `esmfold` environment on OSC. Select the kernel your instructor announces;
you do not need to install anything. Do not run `env/install_esmfold.sh`; it is for instructor
provisioning only.

## Notebooks

Each notebook runs top-to-bottom as-is. Short **"Your turn"** exercises ask for short answers or
small code edits; no coding background assumed. Figures you generate are saved next to the
notebook in your own clone.
