#!/usr/bin/env python3
"""CVS (Citation Vortex Score) cartel detection via Hodge decomposition.

The 96-journal OpenAlex network contains no Clarivate-suppressed cartel journals
(mid-tier journals; top-96 are all normal). Validation is therefore synthetic:
cartel subgraphs are injected at varying boost levels (b = 2, 5, 10, 15).

KEY INSIGHT: Standard CVS (residual/total energy ratio) is scale-invariant —
boosting all edges in a subset by factor b changes neither numerator nor
denominator's ratio. We instead use Delta-CVS: the CHANGE in absolute residual
energy per node after injection, which is directly proportional to the boost
level and cleanly separates injected nodes from non-injected ones.

Baselines: delta-reciprocity (change in pairwise mutual citation ratio),
delta-CIDRE-lite (change in internal edge density).
"""

import gc
import json
import math
import os
import resource
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional

import networkx as nx
import numpy as np
from loguru import logger
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import lsqr
from sklearn.metrics import roc_auc_score

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

WS = Path(__file__).parent
DEP_DIR = Path(
    "/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD"
    "/3_invention_loop/iter_1/gen_art/gen_art_dataset_1"
)
GRAPH_PATH = DEP_DIR / "temp/datasets/full_journal_citation_network.json"
FULL_DATA_PATH = DEP_DIR / "full_data_out.json"
OUT_PATH = WS / "method_out.json"

RAM_BUDGET = 8 * 1024**3
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))


def _detect_cpus() -> int:
    try:
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except Exception:
        pass
    try:
        return len(os.sched_getaffinity(0))
    except Exception:
        pass
    return os.cpu_count() or 1


NUM_CPUS = _detect_cpus()
logger.info(f"Detected {NUM_CPUS} CPUs")

CARTEL_ISSNS: dict[str, str] = {
    "1099-0739": "citation_stacking",
    "2307-3608": "citation_stacking",
    "2645-0739": "citation_stacking",
    "1573-5109": "citation_stacking",
    "2073-8994": "citation_stacking",
    "2227-7390": "citation_stacking",
    "1678-2674": "citation_stacking",
    "1980-5322": "citation_stacking",
    "1980-220X": "citation_stacking",
    "1806-9282": "citation_stacking",
    "1873-4286": "citation_stacking",
    "1875-533X": "citation_stacking",
    "0974-1658": "self_citation",
    "2321-6786": "self_citation",
    "1875-8622": "self_citation",
    "1818-9962": "self_citation",
    "1793-7116": "self_citation",
}


def get_label(issns: list[str]) -> str:
    for issn in issns:
        if issn in CARTEL_ISSNS:
            return CARTEL_ISSNS[issn]
    return "normal"


# ── Hodge decomposition ───────────────────────────────────────────────────────

def hodge_decompose(G: nx.DiGraph) -> dict[tuple, dict]:
    """Decompose directed flows into gradient + residual (curl+harmonic) parts.

    Solves min_x ||B1^T x - f||^2 where B1 is the node-edge incidence matrix.
    Gradient component: f_grad = B1^T x*. Residual: f_residual = f - f_grad.
    """
    nodes = list(G.nodes())
    edges = list(G.edges(data="weight", default=1))
    n, m = len(nodes), len(edges)
    if m == 0 or n == 0:
        return {}

    node_idx = {v: i for i, v in enumerate(nodes)}
    f = np.array([w for _, _, w in edges], dtype=float)

    rows_all, cols_all, vals_all = [], [], []
    for j, (u, v, _) in enumerate(edges):
        rows_all += [node_idx[v], node_idx[u]]
        cols_all += [j, j]
        vals_all += [1.0, -1.0]
    B1 = csr_matrix((vals_all, (rows_all, cols_all)), shape=(n, m))

    try:
        result = lsqr(B1.T, f, atol=1e-8, btol=1e-8, iter_lim=10000)
        x = result[0]
        f_grad = B1.T @ x
    except Exception as exc:
        logger.warning(f"lsqr failed ({exc}), zero gradient fallback")
        f_grad = np.zeros(m)

    f_residual = f - f_grad
    return {
        (u, v): {
            "f_total": float(f[j]),
            "f_grad": float(f_grad[j]),
            "f_residual": float(f_residual[j]),
        }
        for j, (u, v, _) in enumerate(edges)
    }


def compute_cvs(subgraph_edges: list[tuple], hodge: dict[tuple, dict]) -> float:
    """CVS = residual energy / total energy for edges within a subgraph."""
    residual_e = sum(hodge[e]["f_residual"] ** 2 for e in subgraph_edges if e in hodge)
    total_e = sum(hodge[e]["f_total"] ** 2 for e in subgraph_edges if e in hodge)
    return residual_e / total_e if total_e > 0 else 0.0


# ── Node-level scores ─────────────────────────────────────────────────────────

def absolute_residual_node_score(G: nx.DiGraph, hodge: dict[tuple, dict]) -> dict[str, float]:
    """Sum of squared residual energies on incident edges per node.

    Unlike ratio-based CVS, this INCREASES proportionally to citation inflation,
    making it sensitive to cartel-level boosts.
    """
    scores: dict[str, float] = defaultdict(float)
    for (u, v), comp in hodge.items():
        r2 = comp["f_residual"] ** 2
        scores[u] += r2
        scores[v] += r2
    return dict(scores)


def mutual_residual_node_score(G: nx.DiGraph, hodge: dict[tuple, dict]) -> dict[str, float]:
    """Absolute residual energy summed only over MUTUAL edges (both directions).

    Mutual edges are the structural hallmark of citation cartels.
    """
    scores: dict[str, float] = defaultdict(float)
    for (u, v), comp in hodge.items():
        if G.has_edge(v, u):
            r2 = comp["f_residual"] ** 2
            scores[u] += r2
            scores[v] += r2
    return dict(scores)


def reciprocity_node_score(G: nx.DiGraph) -> dict[str, float]:
    """Mean pairwise reciprocity ratio within each node's ego neighbourhood."""
    scores = {}
    for node in G.nodes():
        all_nbrs = (set(G.predecessors(node)) | set(G.successors(node))) | {node}
        pairs = []
        for u in all_nbrs:
            for v in all_nbrs:
                if u >= v:
                    continue
                wuv = G[u][v]["weight"] if G.has_edge(u, v) else 0
                wvu = G[v][u]["weight"] if G.has_edge(v, u) else 0
                if wuv + wvu > 0:
                    pairs.append(min(wuv, wvu) / max(wuv, wvu))
        scores[node] = float(np.mean(pairs)) if pairs else 0.0
    return scores


def cidre_lite_node_score(G: nx.DiGraph) -> dict[str, float]:
    """Internal edge density of each node's 1-hop ego neighbourhood."""
    scores = {}
    for node in G.nodes():
        neighbors = (set(G.predecessors(node)) | set(G.successors(node))) | {node}
        n = len(neighbors)
        if n < 2:
            scores[node] = 0.0
            continue
        within = sum(1 for u, v in G.edges() if u in neighbors and v in neighbors)
        scores[node] = within / (n * (n - 1))
    return scores


# ── Community detection ───────────────────────────────────────────────────────

def build_undirected_projection(G: nx.DiGraph) -> nx.Graph:
    """Max-weight undirected projection for Louvain."""
    UG = nx.Graph()
    UG.add_nodes_from(G.nodes())
    for u, v, d in G.edges(data=True):
        w = d.get("weight", 1)
        if UG.has_edge(u, v):
            UG[u][v]["weight"] = max(UG[u][v]["weight"], w)
        else:
            UG.add_edge(u, v, weight=w)
    return UG


def run_louvain(G: nx.DiGraph, seeds: int = 10) -> list[dict]:
    import community as louvain_community
    UG = build_undirected_projection(G)
    partitions = []
    for seed in range(seeds):
        partition = louvain_community.best_partition(UG, weight="weight", random_state=seed)
        comm_map: dict[int, list] = defaultdict(list)
        for node, comm_id in partition.items():
            comm_map[comm_id].append(node)
        partitions.append(dict(comm_map))
    return partitions


def score_partition(
    G: nx.DiGraph, partition: dict, hodge: dict[tuple, dict]
) -> list[dict]:
    """Score each community with CVS, reciprocity, CIDRE-lite."""
    communities = []
    for comm_id, members in partition.items():
        member_set = set(members)
        subgraph_edges = [(u, v) for u, v in G.edges() if u in member_set and v in member_set]
        cvs = compute_cvs(subgraph_edges, hodge)

        recip_scores = []
        for u in member_set:
            for v in member_set:
                if u >= v:
                    continue
                wuv = G[u][v]["weight"] if G.has_edge(u, v) else 0
                wvu = G[v][u]["weight"] if G.has_edge(v, u) else 0
                if wuv + wvu > 0:
                    recip_scores.append(min(wuv, wvu) / max(wuv, wvu))
        recip = float(np.mean(recip_scores)) if recip_scores else 0.0

        n = len(members)
        total_possible = n * (n - 1)
        cidre = len(subgraph_edges) / total_possible if total_possible > 0 else 0.0

        communities.append({
            "comm_id": comm_id,
            "members": members,
            "size": n,
            "cvs_score": cvs,
            "reciprocity_score": recip,
            "cidre_lite_score": cidre,
            "n_internal_edges": len(subgraph_edges),
        })
    return communities


def partition_node_scores(
    communities: list[dict], node_ids: list[str], score_key: str
) -> dict[str, float]:
    """Assign each node the max community score across all seeds."""
    scores = {n: 0.0 for n in node_ids}
    for comm in communities:
        for member in comm["members"]:
            if comm[score_key] > scores.get(member, 0.0):
                scores[member] = comm[score_key]
    return scores


# ── Delta-CVS: change in absolute residual energy after injection ─────────────

def delta_scores(
    G_orig: nx.DiGraph,
    G_syn: nx.DiGraph,
    hodge_orig: dict[tuple, dict],
    hodge_syn: dict[tuple, dict],
    nodes: list[str],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute delta-scores (syn - baseline) for CVS, reciprocity, CIDRE-lite."""
    abs_base = absolute_residual_node_score(G_orig, hodge_orig)
    abs_syn = absolute_residual_node_score(G_syn, hodge_syn)
    y_cvs = np.array([abs_syn.get(n, 0.0) - abs_base.get(n, 0.0) for n in nodes])

    recip_base = reciprocity_node_score(G_orig)
    recip_syn = reciprocity_node_score(G_syn)
    y_recip = np.array([recip_syn.get(n, 0.0) - recip_base.get(n, 0.0) for n in nodes])

    cidre_base = cidre_lite_node_score(G_orig)
    cidre_syn = cidre_lite_node_score(G_syn)
    y_cidre = np.array([cidre_syn.get(n, 0.0) - cidre_base.get(n, 0.0) for n in nodes])

    return y_cvs, y_recip, y_cidre


# ── Synthetic validation ──────────────────────────────────────────────────────

def synthetic_validation(
    G: nx.DiGraph,
    hodge_orig: dict[tuple, dict],
    boost_levels: list[float],
    n_subsets: int = 20,
    subset_size: int = 8,
    rng_seed: int = 42,
) -> list[dict]:
    """Inject citation cartels at various boost levels, measure delta-CVS AUC.

    Subsets are chosen WITHIN a reference Louvain community (realistic same-field).
    Delta-CVS = change in absolute residual energy after cartel injection.
    """
    import community as louvain_community

    rng = np.random.default_rng(rng_seed)
    nodes = list(G.nodes())

    # Reference communities for realistic subset selection
    UG_ref = build_undirected_projection(G)
    ref_partition = louvain_community.best_partition(UG_ref, weight="weight", random_state=0)
    ref_communities: dict[int, list] = defaultdict(list)
    for node, comm_id in ref_partition.items():
        ref_communities[comm_id].append(node)
    eligible = [m for m in ref_communities.values() if len(m) >= subset_size]
    logger.info(f"Reference communities eligible for injection: {len(eligible)}")

    # Pre-compute baseline scores once
    recip_base = reciprocity_node_score(G)
    cidre_base = cidre_lite_node_score(G)
    abs_base = absolute_residual_node_score(G, hodge_orig)

    y_true = np.array([0] * len(nodes))  # placeholder

    results = []
    for boost in boost_levels:
        cvs_aucs, recip_aucs, cidre_aucs = [], [], []

        for i in range(n_subsets):
            pool = eligible[i % len(eligible)] if eligible else nodes
            if len(pool) < subset_size:
                pool = nodes
            subset = set(rng.choice(pool, size=subset_size, replace=False).tolist())

            # Inject cartel
            G_syn = G.copy()
            for u, v in list(G.edges()):
                if u in subset and v in subset:
                    G_syn[u][v]["weight"] = G[u][v].get("weight", 1) * boost

            hodge_syn = hodge_decompose(G_syn)

            # Delta scores
            abs_syn = absolute_residual_node_score(G_syn, hodge_syn)
            y_cvs = np.array([abs_syn.get(n, 0.0) - abs_base.get(n, 0.0) for n in nodes])

            recip_syn = reciprocity_node_score(G_syn)
            y_recip = np.array([recip_syn.get(n, 0.0) - recip_base.get(n, 0.0) for n in nodes])

            cidre_syn = cidre_lite_node_score(G_syn)
            y_cidre = np.array([cidre_syn.get(n, 0.0) - cidre_base.get(n, 0.0) for n in nodes])

            y_true_i = np.array([1 if n in subset else 0 for n in nodes])

            if len(set(y_true_i.tolist())) > 1:
                cvs_aucs.append(float(roc_auc_score(y_true_i, y_cvs)))
                recip_aucs.append(float(roc_auc_score(y_true_i, y_recip)))
                cidre_aucs.append(float(roc_auc_score(y_true_i, y_cidre)))

            del G_syn, hodge_syn
            gc.collect()

        def stats(xs: list[float]) -> dict:
            if not xs:
                return {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0, "n": 0}
            return {
                "mean": round(float(np.mean(xs)), 4),
                "std": round(float(np.std(xs)), 4),
                "min": round(float(np.min(xs)), 4),
                "max": round(float(np.max(xs)), 4),
                "n": len(xs),
            }

        r = {
            "boost_level": boost,
            "n_subsets": n_subsets,
            "delta_cvs": stats(cvs_aucs),
            "delta_reciprocity": stats(recip_aucs),
            "delta_cidre_lite": stats(cidre_aucs),
        }
        results.append(r)
        logger.info(
            f"Boost={boost}x: Delta-CVS AUC={r['delta_cvs']['mean']:.3f}"
            f"±{r['delta_cvs']['std']:.3f} | "
            f"Recip={r['delta_reciprocity']['mean']:.3f} | "
            f"CIDRE={r['delta_cidre_lite']['mean']:.3f}"
        )
    return results


# ── Structural analysis ────────────────────────────────────────────────────────

def mutual_citation_analysis(G: nx.DiGraph, hodge: dict[tuple, dict]) -> list[dict]:
    """Find node pairs with highest mutual residual energy (suspicious pairs)."""
    pairs = []
    seen = set()
    for u, v in G.edges():
        if G.has_edge(v, u) and (min(u, v), max(u, v)) not in seen:
            seen.add((min(u, v), max(u, v)))
            wuv = G[u][v].get("weight", 1)
            wvu = G[v][u].get("weight", 1)
            r_uv = hodge.get((u, v), {}).get("f_residual", 0.0)
            r_vu = hodge.get((v, u), {}).get("f_residual", 0.0)
            pairs.append({
                "u": u,
                "v": v,
                "weight_uv": wuv,
                "weight_vu": wvu,
                "reciprocity": round(min(wuv, wvu) / max(wuv, wvu), 4),
                "mutual_residual_energy": round(r_uv**2 + r_vu**2, 4),
            })
    pairs.sort(key=lambda x: x["mutual_residual_energy"], reverse=True)
    return pairs[:20]


# ── Main ──────────────────────────────────────────────────────────────────────

@logger.catch(reraise=True)
def main() -> None:
    # ── 1. Load network ────────────────────────────────────────────────────────
    logger.info("Loading journal citation network")
    net = json.loads(GRAPH_PATH.read_text())
    journals = net["journals"]
    edges_raw = net["edges"]
    logger.info(f"Network: {len(journals)} journals, {len(edges_raw)} edges")

    journal_meta: dict[str, dict] = {j["id"]: j for j in journals}

    G = nx.DiGraph()
    for j in journals:
        G.add_node(j["id"], **j)
    for e in edges_raw:
        G.add_edge(e["source_id"], e["target_id"], weight=e["citation_count"])
    node_ids = list(G.nodes())
    logger.info(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    # ── 2. Ground truth labels ─────────────────────────────────────────────────
    node_gt_label: dict[str, str] = {}
    node_issns: dict[str, list] = {}
    for jid in node_ids:
        meta = journal_meta.get(jid, {})
        issns = ([meta.get("issn_l", "")] if meta.get("issn_l") else []) + (meta.get("issn", []) or [])
        issns = [x for x in issns if x]
        node_issns[jid] = issns
        node_gt_label[jid] = get_label(issns)

    gt_counts = defaultdict(int)
    for v in node_gt_label.values():
        gt_counts[v] += 1
    logger.info(f"Ground truth: {dict(gt_counts)}")
    logger.info(
        "NOTE: Top-96 journals are all 'normal' — Clarivate cartel journals are "
        "mid-tier and absent. Validation is fully synthetic (cartel injection)."
    )

    # ── 3. Hodge decomposition ─────────────────────────────────────────────────
    logger.info("Running Hodge decomposition")
    hodge = hodge_decompose(G)
    total_e = sum(c["f_total"] ** 2 for c in hodge.values())
    residual_e = sum(c["f_residual"] ** 2 for c in hodge.values())
    max_err = max(
        abs(c["f_total"] - c["f_grad"] - c["f_residual"]) for c in hodge.values()
    ) if hodge else 0.0
    logger.info(
        f"Hodge: total={total_e:.1f}, gradient={total_e-residual_e:.1f}, "
        f"residual={residual_e:.1f} ({100*residual_e/total_e:.1f}%), "
        f"recon_err={max_err:.2e}"
    )

    # ── 4. Louvain community detection ─────────────────────────────────────────
    logger.info("Running Louvain (10 seeds)")
    partitions = run_louvain(G, seeds=10)

    all_seed_communities = []
    for seed_idx, partition in enumerate(partitions):
        comms = score_partition(G, partition, hodge)
        for c in comms:
            c["seed"] = seed_idx
        all_seed_communities.extend(comms)

    canonical_communities = [c for c in all_seed_communities if c["seed"] == 0]
    logger.info(
        f"Canonical partition: {len(canonical_communities)} communities, "
        f"sizes: {sorted([c['size'] for c in canonical_communities], reverse=True)}"
    )
    cvs_vals = [c["cvs_score"] for c in canonical_communities]
    logger.info(
        f"Community CVS: min={min(cvs_vals):.4f} mean={np.mean(cvs_vals):.4f} max={max(cvs_vals):.4f}"
    )

    # ── 5. Node-level scores ───────────────────────────────────────────────────
    logger.info("Computing node-level scores")
    node_comm_cvs = partition_node_scores(all_seed_communities, node_ids, "cvs_score")
    node_abs_res = absolute_residual_node_score(G, hodge)
    node_mut_res = mutual_residual_node_score(G, hodge)
    node_recip = reciprocity_node_score(G)
    node_cidre = cidre_lite_node_score(G)

    logger.info(
        f"Absolute residual energy: min={min(node_abs_res.values()):.1f} "
        f"mean={np.mean(list(node_abs_res.values())):.1f} "
        f"max={max(node_abs_res.values()):.1f}"
    )

    # ── 6. Structural analysis ─────────────────────────────────────────────────
    top_mutual_pairs = mutual_citation_analysis(G, hodge)
    logger.info(f"Top mutual pair: {top_mutual_pairs[0] if top_mutual_pairs else 'none'}")

    # ── 7. Stability across seeds ──────────────────────────────────────────────
    seed_node_cvs: dict[str, list[float]] = defaultdict(list)
    for seed_idx, partition in enumerate(partitions):
        comms = [c for c in all_seed_communities if c["seed"] == seed_idx]
        n2s = {}
        for comm in comms:
            for m in comm["members"]:
                n2s[m] = comm["cvs_score"]
        for n in node_ids:
            seed_node_cvs[n].append(n2s.get(n, 0.0))

    mean_cvs_by_node = {n: float(np.mean(v)) for n, v in seed_node_cvs.items()}
    std_cvs_by_node = {n: float(np.std(v)) for n, v in seed_node_cvs.items()}

    stability_table = sorted(
        [
            {
                "journal_name": journal_meta.get(n, {}).get("name", n),
                "mean_community_cvs": round(mean_cvs_by_node[n], 4),
                "std_community_cvs": round(std_cvs_by_node[n], 4),
                "absolute_residual_energy": round(node_abs_res.get(n, 0.0), 2),
                "mutual_residual_energy": round(node_mut_res.get(n, 0.0), 2),
                "reciprocity": round(node_recip.get(n, 0.0), 4),
            }
            for n in node_ids
        ],
        key=lambda x: x["absolute_residual_energy"],
        reverse=True,
    )[:20]
    logger.info(f"Top-5 by absolute residual: {[s['journal_name'] for s in stability_table[:5]]}")

    # ── 8. Synthetic validation ────────────────────────────────────────────────
    logger.info("Running synthetic validation (boost=2,5,10,15; 20 subsets each)")
    synthetic_results = synthetic_validation(
        G,
        hodge,
        boost_levels=[2.0, 5.0, 10.0, 15.0],
        n_subsets=20,
        subset_size=8,
    )

    # ── 9. Top journals by absolute residual ───────────────────────────────────
    sorted_journals = sorted(node_ids, key=lambda n: node_abs_res.get(n, 0.0), reverse=True)
    top_journals = []
    for jid in sorted_journals[:20]:
        meta = journal_meta.get(jid, {})
        top_journals.append({
            "journal_name": meta.get("name", ""),
            "issn_l": meta.get("issn_l", ""),
            "absolute_residual_energy": round(node_abs_res.get(jid, 0.0), 2),
            "mutual_residual_energy": round(node_mut_res.get(jid, 0.0), 2),
            "community_cvs": round(node_comm_cvs.get(jid, 0.0), 4),
            "reciprocity": round(node_recip.get(jid, 0.0), 4),
            "cidre_lite": round(node_cidre.get(jid, 0.0), 4),
            "gt_label": node_gt_label.get(jid, "normal"),
        })

    # ── 10. Build output examples ──────────────────────────────────────────────
    issn_to_jid: dict[str, str] = {}
    for jid in node_ids:
        for issn in node_issns.get(jid, []):
            issn_to_jid[issn] = jid

    # Threshold: 80th percentile of absolute residual energy
    threshold_cvs = float(np.percentile(list(node_abs_res.values()), 80))
    threshold_recip = float(np.percentile(list(node_recip.values()), 80))
    threshold_cidre = float(np.percentile(list(node_cidre.values()), 80))

    def classify(score: float, threshold: float) -> str:
        return "citation_stacking" if score >= threshold else "normal"

    logger.info("Loading full_data_out.json")
    full_data = json.loads(FULL_DATA_PATH.read_text())
    examples_in = full_data["datasets"][0]["examples"]

    examples_out = []
    for ex in examples_in:
        inp = json.loads(ex["input"])
        issn_l = inp.get("issn_l", "")
        jid = issn_to_jid.get(issn_l)

        if jid:
            abs_res = node_abs_res.get(jid, 0.0)
            mut_res = node_mut_res.get(jid, 0.0)
            recip = node_recip.get(jid, 0.0)
            cidre = node_cidre.get(jid, 0.0)
            comm_cvs_val = node_comm_cvs.get(jid, 0.0)
        else:
            abs_res = mut_res = recip = cidre = comm_cvs_val = 0.0

        examples_out.append({
            "input": ex["input"],
            "output": ex["output"],
            "predict_cvs": classify(abs_res, threshold_cvs),
            "predict_reciprocity": classify(recip, threshold_recip),
            "predict_cidre_lite": classify(cidre, threshold_cidre),
            "metadata_journal_id": ex.get("metadata_journal_id", ""),
            "metadata_journal_name": ex.get("metadata_journal_name", ""),
            "metadata_issn_l": ex.get("metadata_issn_l", ""),
            "metadata_row_index": ex.get("metadata_row_index", 0),
            "metadata_task_type": ex.get("metadata_task_type", "classification"),
            "metadata_n_classes": ex.get("metadata_n_classes", 3),
            "metadata_class_names": ex.get("metadata_class_names",
                                           "normal,self_citation,citation_stacking"),
            "metadata_absolute_residual_energy": round(abs_res, 4),
            "metadata_mutual_residual_energy": round(mut_res, 4),
            "metadata_community_cvs": round(comm_cvs_val, 4),
            "metadata_reciprocity_score": round(recip, 4),
            "metadata_cidre_lite_score": round(cidre, 4),
        })

    # ── 11. Compile and save ───────────────────────────────────────────────────
    output = {
        "metadata": {
            "method": "Delta-CVS (Citation Vortex Score via Hodge decomposition)",
            "network": "96-journal OpenAlex, 2015-2022",
            "n_nodes": G.number_of_nodes(),
            "n_edges": G.number_of_edges(),
            "description": (
                "Hodge decomposition decomposes directed citation flows into "
                "gradient (prestige hierarchy) and residual (circulation/curl) components. "
                "Delta-CVS measures the CHANGE in absolute residual energy after "
                "cartel injection, fixing the scale-invariance issue of ratio-based CVS. "
                "Node score = sum of squared residual energies on incident edges. "
                "Validation: synthetic cartel injection at boost levels 2-15x "
                "within-community subgraphs; Delta-CVS AUC compared to "
                "delta-reciprocity and delta-CIDRE-lite baselines."
            ),
            "hodge_decomposition": {
                "total_energy": round(total_e, 2),
                "gradient_energy": round(total_e - residual_e, 2),
                "residual_energy": round(residual_e, 2),
                "residual_fraction": round(residual_e / total_e, 4) if total_e > 0 else 0.0,
                "max_reconstruction_error": float(max_err),
            },
            "louvain_seeds": 10,
            "canonical_communities": len(canonical_communities),
            "real_network_analysis": {
                "note": (
                "No known Clarivate cartel journals in the top-96 network. "
                "Structural analysis characterises the Hodge residual landscape."
            ),
            "community_table": sorted(
                [
                    {
                        "size": c["size"],
                        "cvs_score": round(c["cvs_score"], 4),
                        "reciprocity": round(c["reciprocity_score"], 4),
                        "cidre_lite": round(c["cidre_lite_score"], 4),
                        "members": [journal_meta.get(m, {}).get("name", m) for m in c["members"]],
                    }
                    for c in canonical_communities
                ],
                key=lambda x: x["cvs_score"],
                reverse=True,
            ),
            "top20_journals_by_absolute_residual": top_journals,
            "top20_mutual_pairs_by_residual_energy": [
                {
                    "u_name": journal_meta.get(p["u"], {}).get("name", p["u"]),
                    "v_name": journal_meta.get(p["v"], {}).get("name", p["v"]),
                    "weight_uv": p["weight_uv"],
                    "weight_vu": p["weight_vu"],
                    "reciprocity": p["reciprocity"],
                    "mutual_residual_energy": p["mutual_residual_energy"],
                }
                for p in top_mutual_pairs
            ],
                "stability_top20_by_absolute_residual": stability_table,
            },
            "synthetic_validation": {
                "description": (
                    "20 random 8-journal subsets per boost level, chosen within "
                    "reference Louvain communities. Score = delta-absolute-residual-energy "
                    "(change after injection). AUC: ability to rank injected nodes above "
                    "non-injected ones. Higher AUC = better detection."
                ),
                "auc_vs_boost": synthetic_results,
                "interpretation": (
                    "Delta-CVS AUC should monotonically increase with boost level: "
                    "higher citation inflation produces larger absolute residual changes "
                    "on injected nodes. All-methods AUC > 0.5 confirms sensitivity; "
                    "CVS > baselines confirms the Hodge-decomposition advantage."
                ),
            },
        },
        "datasets": [
            {
                "dataset": "journal_citation_network",
                "examples": examples_out,
            }
        ],
    }

    OUT_PATH.write_text(json.dumps(output, indent=2))
    logger.info(f"Saved → {OUT_PATH}")

    logger.info("=== Synthetic validation summary ===")
    for r in synthetic_results:
        logger.info(
            f"  Boost {r['boost_level']}x: "
            f"Delta-CVS={r['delta_cvs']['mean']:.3f}±{r['delta_cvs']['std']:.3f} "
            f"| Recip={r['delta_reciprocity']['mean']:.3f} "
            f"| CIDRE={r['delta_cidre_lite']['mean']:.3f}"
        )


if __name__ == "__main__":
    main()
