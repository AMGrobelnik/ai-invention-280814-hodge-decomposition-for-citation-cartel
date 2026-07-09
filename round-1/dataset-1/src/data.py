#!/usr/bin/env python3
"""Load journal citation network into exp_sel_data_out.json schema.

Each example = one journal (node) with its citation network features and cartel label.
Dataset: journal_citation_network (OpenAlex API, journal-level directed weighted graph).
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/data.log", rotation="30 MB", level="DEBUG")

WS = Path("/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_1/gen_art/gen_art_dataset_1")
DATASETS_DIR = WS / "temp/datasets"
OUT_PATH = WS / "full_data_out.json"

# Known cartel ground truth — ISSN → label
CARTEL_ISSNS: dict[str, str] = {
    # Citation stacking (mutual cartel behavior)
    "1099-0739": "citation_stacking",  # Applied Organometallic Chemistry 2025
    "2307-3608": "citation_stacking",  # Asian Journal of Agriculture and Biology 2025
    "2645-0739": "citation_stacking",  # Chemical Methodologies 2025
    "1573-5109": "citation_stacking",  # Genetic Resources and Crop Evolution 2025
    "2073-8994": "citation_stacking",  # Symmetry 2024
    "2227-7390": "citation_stacking",  # Mathematics 2024
    "1678-2674": "citation_stacking",  # Acta Cirurgica Brasileira 2013
    "1980-5322": "citation_stacking",  # Clinics 2013
    "1980-220X": "citation_stacking",  # Revista da Escola de Enfermagem da USP 2013
    "1806-9282": "citation_stacking",  # Revista da Associacao Medica Brasileira 2013
    "1873-4286": "citation_stacking",  # Current Pharmaceutical Design 2018
    "1875-533X": "citation_stacking",  # Current Medicinal Chemistry 2018
    # Self-citation only
    "0974-1658": "self_citation",       # Advances and Applications in Discrete Mathematics 2025
    "2321-6786": "self_citation",       # Annals of Phytomedicine 2025
    "1875-8622": "self_citation",       # Clinical Hemorheology and Microcirculation 2025
    "1818-9962": "self_citation",       # Lobachevskii Journal of Mathematics 2025
    "1793-7116": "self_citation",       # Journal of Earthquake and Tsunami 2025
}


def get_label(issn_l: str, issn_list: list[str]) -> str:
    all_issns = ([issn_l] if issn_l else []) + (issn_list or [])
    for issn in all_issns:
        if issn and issn in CARTEL_ISSNS:
            return CARTEL_ISSNS[issn]
    return "normal"


def compute_features(net: dict) -> list[dict]:
    """Compute per-journal network features from citation graph."""
    in_degree: dict[str, int] = defaultdict(int)
    out_degree: dict[str, int] = defaultdict(int)
    in_weight: dict[str, int] = defaultdict(int)
    out_weight: dict[str, int] = defaultdict(int)
    out_neighbors: dict[str, set] = defaultdict(set)
    in_neighbors: dict[str, set] = defaultdict(set)

    edge_lookup: dict[tuple, int] = {}
    for e in net.get("edges", []):
        src, tgt, cnt = e["source_id"], e["target_id"], e["citation_count"]
        edge_lookup[(src, tgt)] = cnt
        out_degree[src] += 1
        in_degree[tgt] += 1
        out_weight[src] += cnt
        in_weight[tgt] += cnt
        out_neighbors[src].add(tgt)
        in_neighbors[tgt].add(src)

    # Mutual citation features
    mutual_weight: dict[str, int] = defaultdict(int)
    seen: set = set()
    for (src, tgt), cnt in edge_lookup.items():
        pair = (min(src, tgt), max(src, tgt))
        if pair not in seen:
            seen.add(pair)
            rev = edge_lookup.get((tgt, src), 0)
            if rev > 0:
                mutual_weight[src] += cnt + rev
                mutual_weight[tgt] += cnt + rev

    journal_meta = {j["id"]: j for j in net.get("journals", [])}
    all_ids = set(journal_meta) | set(in_degree) | set(out_degree)

    rows = []
    for jid in all_ids:
        meta = journal_meta.get(jid, {})
        inw = in_weight.get(jid, 0)
        outw = out_weight.get(jid, 0)
        mutw = mutual_weight.get(jid, 0)
        total_w = inw + outw
        asym = round((inw - outw) / (total_w + 1), 4)
        mut_ratio = round(mutw / (total_w + 1), 4)
        n_mutual = len(in_neighbors.get(jid, set()) & out_neighbors.get(jid, set()))

        issn_l = meta.get("issn_l", "")
        issn_list = meta.get("issn") or []
        label = get_label(issn_l, issn_list)

        rows.append({
            "jid": jid,
            "name": meta.get("name", ""),
            "issn_l": issn_l,
            "issn_list": issn_list,
            "works_count": meta.get("works_count", 0),
            "global_cited_by_count": meta.get("cited_by_count", 0),
            "in_degree": in_degree.get(jid, 0),
            "out_degree": out_degree.get(jid, 0),
            "in_citation_weight": inw,
            "out_citation_weight": outw,
            "mutual_citation_weight": mutw,
            "citation_asymmetry": asym,
            "mutual_citation_ratio": mut_ratio,
            "n_mutual_partners": n_mutual,
            "label": label,
        })
    return rows


@logger.catch(reraise=True)
def main():
    # Find network file: prefer full, then mini
    candidates = sorted(DATASETS_DIR.glob("*journal_citation_network*.json"))
    if not candidates:
        raise FileNotFoundError("No journal citation network found. Run build_datasets.py first.")
    net_path = next((p for p in candidates if p.name.startswith("full")), candidates[0])
    logger.info(f"Loading {net_path.name} ({net_path.stat().st_size//1024} KB)")

    net = json.loads(net_path.read_text())
    logger.info(f"Graph: {net['graph_stats']}")

    rows = compute_features(net)
    label_counts: dict[str, int] = defaultdict(int)
    for r in rows:
        label_counts[r["label"]] += 1
    logger.info(f"{len(rows)} journals | labels: {dict(label_counts)}")

    # Convert to schema examples
    examples = []
    for i, r in enumerate(rows):
        feat = {
            "journal_name": r["name"],
            "issn_l": r["issn_l"],
            "works_count": r["works_count"],
            "global_cited_by_count": r["global_cited_by_count"],
            "in_degree": r["in_degree"],
            "out_degree": r["out_degree"],
            "in_citation_weight": r["in_citation_weight"],
            "out_citation_weight": r["out_citation_weight"],
            "mutual_citation_weight": r["mutual_citation_weight"],
            "citation_asymmetry": r["citation_asymmetry"],
            "mutual_citation_ratio": r["mutual_citation_ratio"],
            "n_mutual_partners": r["n_mutual_partners"],
        }
        examples.append({
            "input": json.dumps(feat),
            "output": r["label"],
            "metadata_journal_id": r["jid"],
            "metadata_journal_name": r["name"],
            "metadata_issn_l": r["issn_l"],
            "metadata_row_index": i,
            "metadata_task_type": "classification",
            "metadata_n_classes": 3,
            "metadata_class_names": "normal,self_citation,citation_stacking",
        })

    output = {
        "metadata": {
            "description": "Journal citation network for citation cartel detection (OpenAlex API, 2015-2022)",
            "source": "OpenAlex REST API + Clarivate JCR Suppression Lists",
            "task": "Classify journals as normal / self_citation / citation_stacking based on network features",
            "graph_stats": net["graph_stats"],
            "n_journals_queried": net["metadata"].get("n_journals_queried"),
        },
        "datasets": [
            {
                "dataset": "journal_citation_network",
                "examples": examples,
            }
        ],
    }

    OUT_PATH.write_text(json.dumps(output, indent=2))
    sz = OUT_PATH.stat().st_size
    logger.info(f"Saved {len(examples)} examples to {OUT_PATH} ({sz//1024} KB)")


if __name__ == "__main__":
    main()
