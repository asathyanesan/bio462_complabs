"""Export single-chain ESM3 predictions with pLDDT in the PDB B-factor column."""
from pathlib import Path

import numpy as np
from esm.sdk.api import ESMProtein, ESMProteinError


def save_pdb_with_plddt(protein: ESMProtein, filename: str) -> None:
    if isinstance(protein, ESMProteinError):
        raise RuntimeError(f"ESM3 generation failed: {protein}")
    if protein.sequence is None or protein.coordinates is None:
        raise ValueError("A sequence and structure are required for PDB export.")
    if "|" in protein.sequence:
        raise ValueError("This lab exporter supports single-chain proteins only.")
    if protein.plddt is None:
        raise ValueError("ESM3 returned no pLDDT scores; regenerate the structure.")
    scores = protein.plddt.detach().cpu().numpy()
    if scores.shape != (len(protein.sequence),):
        raise ValueError("There must be one pLDDT score per sequence residue.")
    if not np.isfinite(scores).all() or np.any((scores < 0) | (scores > 1)):
        raise ValueError("Expected finite ESM3 pLDDT scores on the 0-1 scale.")

    # ESMProtein.to_pdb() in esm 3.2.1 discards confidence; the chain exporter retains it.
    chain = protein.to_protein_chain().infer_oxygen()
    chain.confidence = scores * 100
    chain.to_pdb(filename)
    ca_scores = np.array([
        float(line[60:66])
        for line in Path(filename).read_text().splitlines()
        if line.startswith("ATOM") and line[12:16].strip() == "CA"
    ])
    if ca_scores.shape != scores.shape or not np.allclose(
        ca_scores, scores * 100, atol=0.011, rtol=0
    ):
        raise RuntimeError(f"PDB confidence values do not match ESM3 scores: {filename}")
