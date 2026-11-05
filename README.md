# BIO 462/594 Molecular Biology — Computational Labs

Fall 2026, University of Dayton. Labs run on the Ohio Supercomputer Center (OSC) Pitzer cluster
via OnDemand Jupyter.

| Lab | Date | Topic | Report due |
|---|---|---|---|
| 1 | Tue Sep 29 | Variant interpretation (AlphaMissense + ClinVar + ACMG) | Oct 13 |
| 2 | Thu Nov 5 | Protein design with ESM3 (generative, novel proteins) | Nov 12 |
| 3 | Thu Dec 3 | Single-cell annotation of COVID PBMCs (Scanpy + CellTypist) | Dec 11 |

## Get Lab 2 on OSC

Students who already cloned the full repository should update only the Lab 2 files in their
existing personal copy. First log into your <a href="https://class.osc.edu" target="_blank" rel="noopener noreferrer">OSC Classroom account</a>. Then, come back to this page and open an <a href="https://class.osc.edu/pun/sys/shell/ssh/pitzer.osc.edu" target="_blank" rel="noopener noreferrer">OSC terminal</a>,
fetch the latest version, then replace the old Lab 2 folder with the new one:

```bash
cd osc_classes/BIOLOGICAL_DISCOVERY_DAYTON/materials/bio462_complabs
git fetch origin main
git restore --source=FETCH_HEAD --worktree -- lab2_structure lab2_protein_design
cd lab2_protein_design
```

The restore removes the replaced `lab2_structure/` files and downloads the current
`lab2_protein_design/` files; it leaves the other lab folders unchanged. Save any personal changes
you want to keep from either Lab 2 folder elsewhere first. Instructions to start the Jupyter notebook for this lab are in the <a href="https://github.com/asathyanesan/bio462_complabs/raw/refs/heads/main/lab2_protein_design/Lab2_PreLab_Handout.docx" target="_blank" rel="noopener noreferrer">Pre-lab handout doc</a>. Once the jupyter app has been initiated, open `Lab2_Student.ipynb` in the updated folder in Jupyter and select the ESM3 kernel your instructor announces.

## Lab 3 — one extra step (217 MB dataset)

The single-cell dataset is too large for GitHub. After cloning, run once:

```bash
cd ~/bio462_complabs/lab3_singlecell
python data/download_dataset.py
```

or run the first notebook cell, which does the same thing. Do this during the pre-class buffer —
the download takes about a minute on OSC.

## Lab 2 — environment

Lab 2 uses ESM3-open for generative protein design. The shared environment and weights are already installed for PNS0503. Students do not run the instructor installation scripts. If the ESM3 kernel is missing, run this in the Classroom Jupyter terminal:
```bash
bash env/start_lab2.sh
```
This registers the kernel and creates an additional notebook/data copy in your home directory without overwriting existing work. You may continue using the updated notebook in your repository.

Choose one of the 10 design problems in `lab2_protein_design/data/design_menu.csv`. The scripts in `lab2_protein_design/env/` are for instructor setup.

## Notebooks

Each notebook runs top-to-bottom as-is. Short **"Your turn"** exercises ask for short answers or
small code edits — no coding background assumed. Figures you generate are saved next to the
notebook in your own clone.

## Validated notebook checksums

- Lab 2 `Lab2_Student.ipynb` — MD5 `7fa41adf4fa3091ce49997c801b9dc6f`
- Lab 3 `Lab3_Student.ipynb` — MD5 `17f55c0bfda392a20c9aac8a1475cc8c`
