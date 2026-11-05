"""Compare equal-length lab candidates using their shared residue numbering."""
from html import escape

import pandas as pd
from IPython.display import HTML, display


def compare_sequences(candidates, reference, *, fixed_constraints):
    if not candidates or not reference:
        raise ValueError("Run Parts 1-3 before comparing sequences.")
    sequences = [candidate["sequence"] for candidate in candidates]
    if any(not isinstance(seq, str) or len(seq) != len(reference) for seq in sequences):
        raise ValueError("Candidates must share the reference length for positional alignment.")
    if any("_" in seq or "|" in seq or "-" in seq for seq in sequences):
        raise ValueError("Comparison requires complete, single-chain sequences without gaps.")
    labels = [f"Candidate {candidate['i']}" for candidate in candidates]
    records = []
    for index, original in enumerate(reference):
        residues = [seq[index] for seq in sequences]
        different = len(set(residues)) > 1
        changed = any(residue != original for residue in residues)
        violation = fixed_constraints and original != "_" and changed
        if different or (changed and (not fixed_constraints or original != "_")):
            record = {"Position (1-based)": index + 1}
            if fixed_constraints:
                record["Prompt"] = original
                record["Constraint"] = "Designed" if original == "_" else "Fixed"
                record["Fixed residue retained"] = "NO" if violation else (
                    "Yes" if original != "_" else "Not applicable"
                )
            else:
                record["Original"] = original
            record.update(zip(labels, residues))
            records.append(record)

    rows = [("Prompt" if fixed_constraints else "Original", reference), *zip(labels, sequences)]
    blocks = []
    for start in range(0, len(reference), 50):
        end = min(start + 50, len(reference))
        lines = [f"Residues {start + 1}-{end}"]
        for label, seq in rows:
            residues_html = []
            for index in range(start, end):
                residues = [sequence[index] for sequence in sequences]
                violation = fixed_constraints and reference[index] != "_" and any(
                    residue != reference[index] for residue in residues
                )
                highlighted = len(set(residues)) > 1 or (
                    not fixed_constraints and any(residue != reference[index] for residue in residues)
                )
                color = "#ffcccc" if violation else "#fff0a6" if highlighted else None
                residue = escape(seq[index])
                if color:
                    residue = f'<span style="background:{color};color:#111">{residue}</span>'
                residues_html.append(residue)
            lines.append(f"{escape(label):<14} {''.join(residues_html)}")
        blocks.append("<pre style='overflow-x:auto'>" + "\n".join(lines) + "</pre>")
    display(HTML("<p>Yellow: sequence differences. Red: a fixed constraint was changed. "
                 "Numbering is 1-based within this lab sequence; no gaps are introduced.</p>"
                 + "".join(blocks)))

    if fixed_constraints:
        violations = [
            index + 1 for index, residue in enumerate(reference)
            if residue != "_" and any(seq[index] != residue for seq in sequences)
        ]
        print("Fixed-residue check:", "PASS" if not violations else f"FAILED at positions {violations}")
        print("Variable positions:", sum(len({seq[i] for seq in sequences}) > 1
                                         for i in range(len(reference))))
    else:
        summaries = []
        for candidate, seq in zip(candidates, sequences):
            substitutions = [f"{old}{index + 1}{new}" for index, (old, new)
                             in enumerate(zip(reference, seq)) if old != new]
            summaries.append({
                "Candidate": candidate["i"],
                "Substitutions": len(substitutions),
                "Sequence identity (%)": round(100 * (1 - len(substitutions) / len(reference)), 1),
                "Examples (first 10)": ", ".join(substitutions[:10]) or "None",
            })
        display(pd.DataFrame(summaries))
        print("Substitution notation: A12G means alanine at fragment position 12 changed to glycine.")
        print("These positions refer to the provided fragment, not full-length p53 numbering.")
    if records:
        table = pd.DataFrame(records)
        with pd.option_context("display.max_rows", None):
            display(table)
    else:
        table = pd.DataFrame()
        print("No sequence differences detected.")
    return table
