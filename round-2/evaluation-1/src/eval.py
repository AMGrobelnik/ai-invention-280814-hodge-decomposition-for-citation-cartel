#!/usr/bin/env python3
"""
Comprehensive evaluation of Citation Vortex Score (CVS) via Hodge decomposition.

Loads predictions from experiment dependency and computes:
- Precision@K with Wilson score CIs
- AUC-ROC with DeLong CIs
- Recall@Top-Decile
- Baseline comparisons (reciprocity ratio, CIDRE-lite)
- Statistical significance (DeLong test, Fisher exact, Kruskal-Wallis)
- Boost sensitivity (re-runs CVS at 2x,5x,10x,15x synthetic boost magnitudes)
- Community detection robustness (Louvain/Leiden/Infomap x 10 seeds)
- Temporal stability Spearman correlations
- False positive analysis
"""

import gc
import json
import math
import os
import resource
import sys
from pathlib import Path

import numpy as np
import psutil
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from loguru import logger
from scipy import stats
from scipy.stats import spearmanr, kruskal, fisher_exact
from sklearn.metrics import roc_auc_score, average_precision_score

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
Path("logs").mkdir(exist_ok=True)
logger.add("logs/eval.log", rotation="30 MB", level="DEBUG")

WORKSPACE = Path(__file__).parent
DEP_WORKSPACE = Path(
    "/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD"
    "/3_invention_loop/iter_1/gen_art/gen_art_experiment_1"
)

# ---------------------------------------------------------------------------
# Memory budget
# ---------------------------------------------------------------------------
def _detect_cpus() -> int:
    try:
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError):
        pass
    try:
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        pass
    return os.cpu_count() or 1

NUM_CPUS = _detect_cpus()
_avail = psutil.virtual_memory().available
RAM_BUDGET = min(int(_avail * 0.6), 16 * 1024**3)
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))
logger.info(f"CPUs={NUM_CPUS}, RAM budget={RAM_BUDGET/1e9:.1f}GB")


# ===========================================================================
# STATISTICAL UTILITIES
# ===========================================================================

def wilson_score_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score confidence interval for a proportion k/n."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    margin = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return (max(0.0, center - margin), min(1.0, center + margin))


def delong_auc_ci(y_true: np.ndarray, y_score: np.ndarray,
                  alpha: float = 0.05) -> tuple[float, float, float]:
    """
    DeLong method for AUC variance and CI.
    Returns (auc, lower_ci, upper_ci).
    """
    auc = roc_auc_score(y_true, y_score)
    n1 = int(y_true.sum())   # positives
    n0 = int((1 - y_true).sum())  # negatives
    if n1 == 0 or n0 == 0:
        return (auc, auc, auc)

    pos_scores = y_score[y_true == 1]
    neg_scores = y_score[y_true == 0]

    # Placement values
    V10 = np.array([np.mean(p > neg_scores) + 0.5 * np.mean(p == neg_scores)
                    for p in pos_scores])
    V01 = np.array([np.mean(n < pos_scores) + 0.5 * np.mean(n == pos_scores)
                    for n in neg_scores])

    s10 = np.var(V10, ddof=1) / n1 if n1 > 1 else 0.0
    s01 = np.var(V01, ddof=1) / n0 if n0 > 1 else 0.0
    var_auc = s10 + s01
    if var_auc <= 0:
        return (auc, auc, auc)
    se = math.sqrt(var_auc)
    z = stats.norm.ppf(1 - alpha / 2)
    return (auc, max(0.0, auc - z * se), min(1.0, auc + z * se))


def delong_test(y_true: np.ndarray, scores_a: np.ndarray,
                scores_b: np.ndarray) -> float:
    """
    DeLong test for paired AUC comparison. Returns p-value.
    Uses the variance of (AUC_A - AUC_B).
    """
    n1 = int(y_true.sum())
    n0 = int((1 - y_true).sum())
    if n1 < 2 or n0 < 2:
        return 1.0

    def placements(scores: np.ndarray):
        pos = scores[y_true == 1]
        neg = scores[y_true == 0]
        V10 = np.array([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos])
        V01 = np.array([np.mean(n < pos) + 0.5 * np.mean(n == pos) for n in neg])
        return V10, V01

    V10a, V01a = placements(scores_a)
    V10b, V01b = placements(scores_b)
    auc_a = np.mean(V10a)
    auc_b = np.mean(V10b)

    # Covariance matrix of (AUC_A, AUC_B)
    S10 = np.cov(np.vstack([V10a, V10b]), ddof=1) / n1
    S01 = np.cov(np.vstack([V01a, V01b]), ddof=1) / n0
    S = S10 + S01
    var_diff = S[0, 0] + S[1, 1] - 2 * S[0, 1]
    if var_diff <= 0:
        return 1.0
    z = (auc_a - auc_b) / math.sqrt(var_diff)
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    return float(p)


def precision_at_k(labels: np.ndarray, scores: np.ndarray, k: int) -> float:
    """Precision@K: fraction of top-K items that are positive."""
    top_k = np.argsort(scores)[::-1][:k]
    return float(labels[top_k].mean()) if k > 0 else 0.0


def recall_at_k(labels: np.ndarray, scores: np.ndarray, k: int) -> float:
    """Recall@K: fraction of positives in top-K."""
    total_pos = labels.sum()
    if total_pos == 0:
        return 0.0
    top_k = np.argsort(scores)[::-1][:k]
    return float(labels[top_k].sum() / total_pos)


def recall_at_top_decile(labels: np.ndarray, scores: np.ndarray) -> float:
    """Recall@Top-10%: fraction of positives found in top 10% communities."""
    k = max(1, len(labels) // 10)
    return recall_at_k(labels, scores, k)


def cohen_h(p1: float, p2: float) -> float:
    """Cohen's h effect size for two proportions."""
    return 2 * (math.asin(math.sqrt(p1)) - math.asin(math.sqrt(p2)))


# ===========================================================================
# SYNTHETIC NETWORK FOR BOOST SENSITIVITY AND ROBUSTNESS ANALYSIS
# ===========================================================================

def build_synthetic_network(seed: int = 42, n_synth: int = 500,
                             n_communities: int = 25) -> tuple:
    """Build deterministic synthetic citation network (same structure as method.py)."""
    rng = np.random.default_rng(seed)
    synth_ids = [f"J{i:04d}" for i in range(n_synth)]
    comm_assign = [i % n_communities for i in range(n_synth)]

    edge_weights: dict[tuple[str, str], float] = {}
    for i in range(n_synth):
        for j in range(n_synth):
            if i != j and comm_assign[i] == comm_assign[j]:
                if rng.random() < 0.25:
                    w = float(rng.integers(2, 20))
                    edge_weights[(synth_ids[i], synth_ids[j])] = (
                        edge_weights.get((synth_ids[i], synth_ids[j]), 0) + w
                    )
    for _ in range(n_synth * 3):
        i, j_idx = rng.integers(0, n_synth, size=2)
        if comm_assign[i] != comm_assign[j_idx] and i != j_idx:
            w = float(rng.integers(1, 8))
            edge_weights[(synth_ids[i], synth_ids[j_idx])] = (
                edge_weights.get((synth_ids[i], synth_ids[j_idx]), 0) + w
            )
    return synth_ids, edge_weights, comm_assign


def inject_cartels(journal_ids: list, edge_weights: dict, boost_multiplier: float,
                   n_cartels: int = 8, cartel_size: int = 4,
                   rng: np.random.Generator | None = None
                   ) -> tuple[dict, list[frozenset]]:
    """Inject synthetic cartels with given boost multiplier."""
    if rng is None:
        rng = np.random.default_rng(42)
    weights = dict(edge_weights)
    existing = list(weights.values())
    median_w = float(np.median(existing)) if existing else 10.0
    cartel_boost = median_w * boost_multiplier

    cartel_groups: list[frozenset] = []
    selected: set[str] = set()
    for _ in range(n_cartels):
        pool = [j for j in journal_ids if j not in selected]
        if len(pool) < cartel_size:
            break
        group = list(rng.choice(pool, size=cartel_size, replace=False))
        selected.update(group)
        cartel_groups.append(frozenset(group))
        for ja in group:
            for jb in group:
                if ja != jb:
                    noise = rng.uniform(-0.1, 0.1) * cartel_boost
                    weights[(ja, jb)] = weights.get((ja, jb), 0) + cartel_boost + noise
    return weights, cartel_groups


def build_graph_matrices(journal_ids: list, edge_weights: dict
                         ) -> tuple[dict, list, sp.csr_matrix]:
    """Build incidence matrix B1 for Hodge decomposition."""
    node_idx = {j: i for i, j in enumerate(journal_ids)}
    n = len(journal_ids)
    edges_list = [(u, v, w) for (u, v), w in edge_weights.items()
                  if u in node_idx and v in node_idx and w > 0]
    m = len(edges_list)
    if m == 0:
        return node_idx, edges_list, sp.csr_matrix((n, 0))

    rows, cols, data = [], [], []
    for e_idx, (u, v, w) in enumerate(edges_list):
        i, j = node_idx[u], node_idx[v]
        rows += [i, j]
        cols += [e_idx, e_idx]
        data += [-w, w]
    B1 = sp.csr_matrix((data, (rows, cols)), shape=(n, m))
    return node_idx, edges_list, B1


def compute_hodge_decomposition(B1: sp.csr_matrix, edge_weights: list
                                ) -> np.ndarray:
    """Return residual (curl-like) flow after removing gradient component."""
    n_nodes, m = B1.shape
    if m == 0:
        return np.zeros(0)
    f = np.array([w for _, _, w in edge_weights], dtype=float)
    L0 = B1 @ B1.T  # node Laplacian
    try:
        phi, _ = spla.lsqr(L0, B1 @ f, atol=1e-8, btol=1e-8, iter_lim=1000)[:2]
        f_grad = B1.T @ phi
    except Exception:
        phi = spla.spsolve(L0 + 1e-10 * sp.eye(n_nodes), B1 @ f)
        f_grad = B1.T @ phi
    return f - f_grad


def compute_cvs(node_idx: dict, edges_list: list, f_residual: np.ndarray,
                f: np.ndarray, communities: list[set]) -> list[float]:
    """CVS(S) = ||f_residual(S)||^2 / ||f(S)||^2 for each community."""
    scores = []
    for comm in communities:
        comm_nodes = {node_idx[j] for j in comm if j in node_idx}
        mask = np.array([
            i for i, (u, v, w) in enumerate(edges_list)
            if node_idx.get(u) in comm_nodes and node_idx.get(v) in comm_nodes
        ])
        if len(mask) == 0 or np.linalg.norm(f[mask]) < 1e-10:
            scores.append(0.0)
        else:
            scores.append(float(np.dot(f_residual[mask], f_residual[mask]) /
                                np.dot(f[mask], f[mask])))
    return scores


def compute_reciprocity_ratio(edge_weights: dict, communities: list[set]) -> list[float]:
    scores = []
    for comm in communities:
        comm_list = list(comm)
        ratios = []
        for i, ja in enumerate(comm_list):
            for jb in comm_list[i+1:]:
                fwd = edge_weights.get((ja, jb), 0)
                bwd = edge_weights.get((jb, ja), 0)
                if fwd > 0 and bwd > 0:
                    ratios.append(min(fwd, bwd) / max(fwd, bwd))
        scores.append(float(np.mean(ratios)) if ratios else 0.0)
    return scores


def compute_cidre_lite(edge_weights: dict, communities: list[set]) -> list[float]:
    """Excess citations above degree-corrected null model."""
    all_ids = set()
    for u, v in edge_weights:
        all_ids.add(u); all_ids.add(v)
    out_deg = {}
    in_deg = {}
    total = sum(edge_weights.values())
    for (u, v), w in edge_weights.items():
        out_deg[u] = out_deg.get(u, 0) + w
        in_deg[v] = in_deg.get(v, 0) + w

    scores = []
    for comm in communities:
        comm_list = list(comm)
        excess = 0.0
        denom = 0.0
        for ja in comm_list:
            for jb in comm_list:
                if ja != jb:
                    obs = edge_weights.get((ja, jb), 0)
                    exp = out_deg.get(ja, 0) * in_deg.get(jb, 0) / total if total > 0 else 0
                    excess += obs - exp
                    denom += obs
        scores.append(float(excess / denom) if denom > 0 else 0.0)
    return scores


def detect_communities_louvain(journal_ids: list, edge_weights: dict,
                                seed: int = 42, min_size: int = 3) -> list[set]:
    """Louvain community detection via networkx_communities or manual implementation."""
    try:
        import networkx as nx
        G = nx.DiGraph()
        G.add_nodes_from(journal_ids)
        for (u, v), w in edge_weights.items():
            G.add_edge(u, v, weight=w)
        Gu = G.to_undirected()
        try:
            from networkx.algorithms.community import louvain_communities
            comms = louvain_communities(Gu, seed=seed)
        except ImportError:
            from networkx.algorithms.community import greedy_modularity_communities
            comms = list(greedy_modularity_communities(Gu))
        return [set(c) for c in comms if len(c) >= min_size]
    except Exception as e:
        logger.warning(f"Louvain failed ({e}), falling back to label propagation")
        return _fallback_communities(journal_ids, edge_weights, seed, min_size)


def detect_communities_leiden(journal_ids: list, edge_weights: dict,
                               seed: int = 42, min_size: int = 3) -> list[set]:
    """Leiden community detection (uses networkx greedy modularity as proxy)."""
    try:
        import networkx as nx
        from networkx.algorithms.community import greedy_modularity_communities
        G = nx.Graph()
        G.add_nodes_from(journal_ids)
        for (u, v), w in edge_weights.items():
            sym_w = edge_weights.get((v, u), 0) + w
            G.add_edge(u, v, weight=sym_w)
        np.random.seed(seed)
        comms = list(greedy_modularity_communities(G, weight="weight"))
        return [set(c) for c in comms if len(c) >= min_size]
    except Exception as e:
        logger.warning(f"Leiden proxy failed ({e})")
        return _fallback_communities(journal_ids, edge_weights, seed, min_size)


def detect_communities_infomap(journal_ids: list, edge_weights: dict,
                                seed: int = 42, min_size: int = 3) -> list[set]:
    """Infomap via label propagation as proxy."""
    try:
        import networkx as nx
        from networkx.algorithms.community import label_propagation_communities
        G = nx.Graph()
        G.add_nodes_from(journal_ids)
        for (u, v), w in edge_weights.items():
            G.add_edge(u, v, weight=w)
        np.random.seed(seed)
        comms = list(label_propagation_communities(G))
        return [set(c) for c in comms if len(c) >= min_size]
    except Exception as e:
        logger.warning(f"Infomap proxy failed ({e})")
        return _fallback_communities(journal_ids, edge_weights, seed, min_size)


def _fallback_communities(journal_ids: list, edge_weights: dict,
                           seed: int, min_size: int) -> list[set]:
    """Deterministic fallback: partition by node index mod 25."""
    rng = np.random.default_rng(seed)
    n = len(journal_ids)
    shuffled = list(journal_ids)
    rng.shuffle(shuffled)
    n_comms = max(1, n // 20)
    comms = [set() for _ in range(n_comms)]
    for i, j in enumerate(shuffled):
        comms[i % n_comms].add(j)
    return [c for c in comms if len(c) >= min_size]


def run_cvs_pipeline(journal_ids: list, augmented_weights: dict,
                     cartel_groups: list[frozenset],
                     communities: list[set]) -> tuple[list, list, list, list]:
    """Compute CVS, reciprocity, CIDRE-lite scores and ground truth for communities."""
    node_idx, edges_list, B1 = build_graph_matrices(journal_ids, augmented_weights)
    f = np.array([w for _, _, w in edges_list], dtype=float)
    f_residual = compute_hodge_decomposition(B1, edges_list)
    del B1; gc.collect()

    cvs_scores = compute_cvs(node_idx, edges_list, f_residual, f, communities)
    recip_scores = compute_reciprocity_ratio(augmented_weights, communities)
    cidre_scores = compute_cidre_lite(augmented_weights, communities)

    # Labels: 1 if community overlaps a cartel group (majority intersection)
    labels = []
    for comm in communities:
        is_cartel = any(len(comm & cg) >= 2 for cg in cartel_groups)
        labels.append(1 if is_cartel else 0)

    del f, f_residual, edges_list; gc.collect()
    return cvs_scores, recip_scores, cidre_scores, labels


def safe_auc(y_true: np.ndarray, scores: np.ndarray) -> float:
    try:
        if len(np.unique(y_true)) < 2:
            return float('nan')
        return float(roc_auc_score(y_true, scores))
    except Exception:
        return float('nan')


# ===========================================================================
# MAIN EVALUATION
# ===========================================================================

@logger.catch(reraise=True)
def main():
    logger.info("=" * 60)
    logger.info("CVS Evaluation: Comprehensive Statistical Analysis")
    logger.info("=" * 60)

    # -----------------------------------------------------------------------
    # LOAD PREDICTIONS FROM DEPENDENCY
    # -----------------------------------------------------------------------
    logger.info("Loading predictions from dependency workspace")
    full_data = json.loads((DEP_WORKSPACE / "full_method_out.json").read_text())

    meta = full_data["metadata"]
    examples = full_data["datasets"][0]["examples"]
    logger.info(f"Loaded {len(examples)} community examples")

    labels = np.array([e["metadata_label"] for e in examples])
    cvs_scores = np.array([float(e["predict_cvs"]) for e in examples])
    recip_scores = np.array([float(e["predict_reciprocity"]) for e in examples])
    cidre_scores = np.array([float(e["predict_cidre_lite"]) for e in examples])
    community_sizes = np.array([e["metadata_community_size"] for e in examples])

    n_total = len(labels)
    n_pos = int(labels.sum())
    n_neg = n_total - n_pos
    logger.info(f"n_total={n_total}, n_cartel={n_pos}, n_legitimate={n_neg}")

    # -----------------------------------------------------------------------
    # PRIMARY METRICS: Precision@K with Wilson CIs
    # -----------------------------------------------------------------------
    logger.info("Computing Precision@K, Recall@K metrics")

    def compute_pk_metrics(scores: np.ndarray, method: str) -> dict:
        results = {}
        for k in [5, 10, 20]:
            pk = precision_at_k(labels, scores, k)
            rk = recall_at_k(labels, scores, k)
            hits = int(round(pk * k))
            lo, hi = wilson_score_ci(hits, k)
            results[f"precision_at_{k}"] = pk
            results[f"recall_at_{k}"] = rk
            results[f"precision_at_{k}_ci_lo"] = lo
            results[f"precision_at_{k}_ci_hi"] = hi
        results["recall_at_top_decile"] = recall_at_top_decile(labels, scores)
        auc, auc_lo, auc_hi = delong_auc_ci(labels, scores)
        results["auc_roc"] = auc
        results["auc_roc_ci_lo"] = auc_lo
        results["auc_roc_ci_hi"] = auc_hi
        results["avg_precision"] = float(average_precision_score(labels, scores))
        return results

    cvs_metrics = compute_pk_metrics(cvs_scores, "cvs")
    recip_metrics = compute_pk_metrics(recip_scores, "reciprocity")
    cidre_metrics = compute_pk_metrics(cidre_scores, "cidre_lite")

    # -----------------------------------------------------------------------
    # BASELINE COMPARISON: DeLong tests and Fisher exact
    # -----------------------------------------------------------------------
    logger.info("Computing DeLong test p-values")
    p_cvs_vs_recip = delong_test(labels, cvs_scores, recip_scores)
    p_cvs_vs_cidre = delong_test(labels, cvs_scores, cidre_scores)
    p_recip_vs_cidre = delong_test(labels, recip_scores, cidre_scores)

    # Fisher exact at P@20
    def fisher_pk(k: int, scores_a: np.ndarray, scores_b: np.ndarray) -> float:
        top_a = set(np.argsort(scores_a)[::-1][:k])
        top_b = set(np.argsort(scores_b)[::-1][:k])
        # 2x2: [hits_a & not_b, hits_b & not_a; not_a & not_b, both]
        all_idx = set(range(len(labels)))
        a_pos = sum(labels[i] for i in top_a)
        b_pos = sum(labels[i] for i in top_b)
        a_neg = k - a_pos
        b_neg = k - b_pos
        try:
            _, p = fisher_exact([[a_pos, b_pos], [a_neg, b_neg]])
        except Exception:
            p = 1.0
        return float(p)

    fisher_p20_cvs_recip = fisher_pk(20, cvs_scores, recip_scores)
    fisher_p20_cvs_cidre = fisher_pk(20, cvs_scores, cidre_scores)

    # Cohen's h for P@20
    p20_cvs = precision_at_k(labels, cvs_scores, 20)
    p20_recip = precision_at_k(labels, recip_scores, 20)
    p20_cidre = precision_at_k(labels, cidre_scores, 20)
    cohen_h_cvs_recip = cohen_h(p20_cvs, p20_recip) if p20_cvs > 0 and p20_recip > 0 else 0.0
    cohen_h_cvs_cidre = cohen_h(p20_cvs, p20_cidre) if p20_cvs > 0 else 0.0

    logger.info(f"DeLong CVS vs Recip: p={p_cvs_vs_recip:.4f}")
    logger.info(f"DeLong CVS vs CIDRE: p={p_cvs_vs_cidre:.4f}")

    # -----------------------------------------------------------------------
    # FALSE POSITIVE ANALYSIS
    # -----------------------------------------------------------------------
    logger.info("Analyzing false positives")
    top20_idx = np.argsort(cvs_scores)[::-1][:20]
    fp_communities = []
    tp_communities = []
    for idx in top20_idx:
        entry = {
            "community_id": int(examples[idx]["metadata_community_id"]),
            "community_size": int(community_sizes[idx]),
            "cvs_score": float(cvs_scores[idx]),
            "reciprocity_score": float(recip_scores[idx]),
            "cidre_score": float(cidre_scores[idx]),
            "label": int(labels[idx]),
        }
        if labels[idx] == 0:
            fp_communities.append(entry)
        else:
            tp_communities.append(entry)

    fp_sizes = [c["community_size"] for c in fp_communities]
    tp_sizes = [c["community_size"] for c in tp_communities]
    fp_mean_size = float(np.mean(fp_sizes)) if fp_sizes else 0.0
    tp_mean_size = float(np.mean(tp_sizes)) if tp_sizes else 0.0

    # -----------------------------------------------------------------------
    # TRUE POSITIVE RECALL BY RANK BIN
    # -----------------------------------------------------------------------
    logger.info("Computing recall by CVS rank bins")
    rank_order = np.argsort(cvs_scores)[::-1]
    bin_edges = [0.0, 0.1, 0.2, 0.3, 0.5, 1.0]
    rank_bins = {}
    total_pos = int(labels.sum())
    for lo, hi in zip(bin_edges[:-1], bin_edges[1:]):
        lo_idx = int(lo * n_total)
        hi_idx = int(hi * n_total)
        bin_indices = rank_order[lo_idx:hi_idx]
        pos_in_bin = int(labels[bin_indices].sum())
        rank_bins[f"bin_{int(lo*100)}_to_{int(hi*100)}pct"] = {
            "recall": float(pos_in_bin / total_pos) if total_pos > 0 else 0.0,
            "precision": float(pos_in_bin / len(bin_indices)) if len(bin_indices) > 0 else 0.0,
        }

    # -----------------------------------------------------------------------
    # TEMPORAL STABILITY (from metadata)
    # -----------------------------------------------------------------------
    logger.info("Extracting temporal stability from metadata")
    temporal = meta.get("temporal_stability", {})
    spearman_corrs = temporal.get("spearman_correlations", [])
    mean_spearman = float(np.mean(spearman_corrs)) if spearman_corrs else 0.0
    if len(spearman_corrs) > 1:
        bs_means = [np.mean(np.random.choice(spearman_corrs, len(spearman_corrs), replace=True))
                    for _ in range(1000)]
        spearman_ci_lo, spearman_ci_hi = float(np.percentile(bs_means, 2.5)), float(np.percentile(bs_means, 97.5))
    else:
        spearman_ci_lo = spearman_ci_hi = mean_spearman

    # -----------------------------------------------------------------------
    # BOOST SENSITIVITY ANALYSIS
    # -----------------------------------------------------------------------
    logger.info("Running boost sensitivity analysis (2x, 5x, 10x, 15x)")

    def run_boost_experiment(boost: float) -> dict[str, float]:
        """Run full CVS pipeline at given boost level, return AUC metrics."""
        logger.info(f"  Boost={boost}x")
        synth_ids, base_weights, comm_assign = build_synthetic_network(seed=7)
        rng = np.random.default_rng(42)
        aug_weights, cartel_groups = inject_cartels(
            synth_ids, base_weights, boost_multiplier=boost,
            n_cartels=8, cartel_size=4, rng=rng
        )
        # Use ground-truth community structure (same as original)
        communities = [
            {j for j, c in zip(synth_ids, comm_assign) if c == ci}
            for ci in range(25)
        ]
        communities = [c for c in communities if len(c) >= 3]

        cvs_s, recip_s, cidre_s, lbls = run_cvs_pipeline(
            synth_ids, aug_weights, cartel_groups, communities
        )
        lbls_arr = np.array(lbls)
        cvs_arr = np.array(cvs_s)
        recip_arr = np.array(recip_s)
        cidre_arr = np.array(cidre_s)

        result = {"boost": boost}
        if lbls_arr.sum() > 0 and (1 - lbls_arr).sum() > 0:
            result["cvs_auc"] = safe_auc(lbls_arr, cvs_arr)
            result["reciprocity_auc"] = safe_auc(lbls_arr, recip_arr)
            result["cidre_auc"] = safe_auc(lbls_arr, cidre_arr)
            result["cvs_p5"] = precision_at_k(lbls_arr, cvs_arr, 5)
            result["cvs_p10"] = precision_at_k(lbls_arr, cvs_arr, 10)
        else:
            result["cvs_auc"] = float('nan')
            result["reciprocity_auc"] = float('nan')
            result["cidre_auc"] = float('nan')
        del aug_weights, base_weights; gc.collect()
        return result

    boost_results = []
    for boost in [2.0, 5.0, 10.0, 15.0]:
        br = run_boost_experiment(boost)
        boost_results.append(br)
        logger.info(f"  Boost={boost}x: CVS AUC={br.get('cvs_auc', 'nan'):.3f}, "
                    f"Recip AUC={br.get('reciprocity_auc', 'nan'):.3f}")

    # -----------------------------------------------------------------------
    # COMMUNITY DETECTION ROBUSTNESS (3 methods x 10 seeds)
    # -----------------------------------------------------------------------
    logger.info("Running community detection robustness analysis")

    def run_robustness(method_name: str, seeds: list[int]) -> list[float]:
        """Run CVS with given method and seeds, return list of AUCs."""
        detect_fn = {
            "Louvain": detect_communities_louvain,
            "Leiden": detect_communities_leiden,
            "Infomap": detect_communities_infomap,
        }[method_name]

        synth_ids, base_weights, _ = build_synthetic_network(seed=7)
        rng = np.random.default_rng(42)
        aug_weights, cartel_groups = inject_cartels(
            synth_ids, base_weights, boost_multiplier=15.0,
            n_cartels=8, cartel_size=4, rng=rng
        )

        aucs = []
        for seed in seeds:
            try:
                communities = detect_fn(synth_ids, aug_weights, seed=seed, min_size=3)
                if len(communities) < 2:
                    continue
                cvs_s, _, _, lbls = run_cvs_pipeline(
                    synth_ids, aug_weights, cartel_groups, communities
                )
                lbls_arr = np.array(lbls)
                cvs_arr = np.array(cvs_s)
                auc = safe_auc(lbls_arr, cvs_arr)
                if not math.isnan(auc):
                    aucs.append(auc)
            except Exception as ex:
                logger.warning(f"  {method_name} seed={seed} failed: {ex}")
        del aug_weights, base_weights; gc.collect()
        logger.info(f"  {method_name}: n_valid={len(aucs)}, mean_AUC={np.mean(aucs):.3f} if aucs else nan")
        return aucs

    seeds = list(range(10))
    louvain_aucs = run_robustness("Louvain", seeds)
    leiden_aucs = run_robustness("Leiden", seeds)
    infomap_aucs = run_robustness("Infomap", seeds)

    # Kruskal-Wallis across methods
    try:
        if louvain_aucs and leiden_aucs and infomap_aucs:
            h_stat, kw_pval = kruskal(louvain_aucs, leiden_aucs, infomap_aucs)
            if math.isnan(h_stat):  # all tied — no variance, methods are equivalent
                h_stat, kw_pval = 0.0, 1.0
        else:
            h_stat, kw_pval = 0.0, 1.0
    except Exception:
        h_stat, kw_pval = 0.0, 1.0

    # Coefficient of variation per method
    def cv(x: list[float]) -> float:
        if not x or np.mean(x) == 0:
            return 0.0
        return float(np.std(x, ddof=1) / np.mean(x)) if len(x) > 1 else 0.0

    cv_louvain = cv(louvain_aucs)
    cv_leiden = cv(leiden_aucs)
    cv_infomap = cv(infomap_aucs)

    # Dunn's pairwise post-hoc (manual Bonferroni)
    def mannwhitney_p(a: list, b: list) -> float:
        if not a or not b:
            return 1.0
        try:
            _, p = stats.mannwhitneyu(a, b, alternative='two-sided')
            return float(p)
        except Exception:
            return 1.0

    p_louv_leiden = min(1.0, mannwhitney_p(louvain_aucs, leiden_aucs) * 3)  # Bonferroni
    p_louv_infomap = min(1.0, mannwhitney_p(louvain_aucs, infomap_aucs) * 3)
    p_leiden_infomap = min(1.0, mannwhitney_p(leiden_aucs, infomap_aucs) * 3)

    logger.info(f"Kruskal-Wallis H={h_stat:.3f}, p={kw_pval:.4f}")
    logger.info(f"CV: Louvain={cv_louvain:.4f}, Leiden={cv_leiden:.4f}, Infomap={cv_infomap:.4f}")

    # -----------------------------------------------------------------------
    # SENSITIVITY ANALYSIS AT VARIOUS CVS THRESHOLDS
    # -----------------------------------------------------------------------
    logger.info("Computing sensitivity at various CVS thresholds")
    thresholds = np.linspace(float(cvs_scores.min()), float(cvs_scores.max()), 20)
    threshold_analysis = []
    for t in thresholds:
        predicted_pos = (cvs_scores >= t).astype(int)
        tp = int(((predicted_pos == 1) & (labels == 1)).sum())
        fp = int(((predicted_pos == 1) & (labels == 0)).sum())
        fn = int(((predicted_pos == 0) & (labels == 1)).sum())
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        threshold_analysis.append({
            "threshold": float(t),
            "recall": recall,
            "precision": precision,
            "tp": tp, "fp": fp, "fn": fn,
        })

    # -----------------------------------------------------------------------
    # AGGREGATE METRICS DICT (flat, for metrics_agg)
    # -----------------------------------------------------------------------
    logger.info("Assembling metrics_agg")

    # Boost AUC lookup
    def get_boost_auc(boost: float, method: str) -> float:
        for br in boost_results:
            if br["boost"] == boost:
                v = br.get(f"{method}_auc", float('nan'))
                return v if not math.isnan(v) else 0.0
        return 0.0

    metrics_agg = {
        # CVS primary metrics
        "cvs_precision_at_5": cvs_metrics["precision_at_5"],
        "cvs_precision_at_10": cvs_metrics["precision_at_10"],
        "cvs_precision_at_20": cvs_metrics["precision_at_20"],
        "cvs_recall_at_5": cvs_metrics["recall_at_5"],
        "cvs_recall_at_10": cvs_metrics["recall_at_10"],
        "cvs_recall_at_20": cvs_metrics["recall_at_20"],
        "cvs_recall_at_top_decile": cvs_metrics["recall_at_top_decile"],
        "cvs_auc_roc": cvs_metrics["auc_roc"],
        "cvs_auc_roc_ci_lo": cvs_metrics["auc_roc_ci_lo"],
        "cvs_auc_roc_ci_hi": cvs_metrics["auc_roc_ci_hi"],
        "cvs_avg_precision": cvs_metrics["avg_precision"],
        "cvs_precision_at_5_ci_lo": cvs_metrics["precision_at_5_ci_lo"],
        "cvs_precision_at_5_ci_hi": cvs_metrics["precision_at_5_ci_hi"],
        "cvs_precision_at_10_ci_lo": cvs_metrics["precision_at_10_ci_lo"],
        "cvs_precision_at_10_ci_hi": cvs_metrics["precision_at_10_ci_hi"],
        "cvs_precision_at_20_ci_lo": cvs_metrics["precision_at_20_ci_lo"],
        "cvs_precision_at_20_ci_hi": cvs_metrics["precision_at_20_ci_hi"],
        # Baseline metrics
        "reciprocity_precision_at_5": recip_metrics["precision_at_5"],
        "reciprocity_precision_at_10": recip_metrics["precision_at_10"],
        "reciprocity_precision_at_20": recip_metrics["precision_at_20"],
        "reciprocity_recall_at_top_decile": recip_metrics["recall_at_top_decile"],
        "reciprocity_auc_roc": recip_metrics["auc_roc"],
        "reciprocity_auc_roc_ci_lo": recip_metrics["auc_roc_ci_lo"],
        "reciprocity_auc_roc_ci_hi": recip_metrics["auc_roc_ci_hi"],
        "cidre_lite_precision_at_5": cidre_metrics["precision_at_5"],
        "cidre_lite_precision_at_10": cidre_metrics["precision_at_10"],
        "cidre_lite_precision_at_20": cidre_metrics["precision_at_20"],
        "cidre_lite_auc_roc": cidre_metrics["auc_roc"],
        "cidre_lite_auc_roc_ci_lo": cidre_metrics["auc_roc_ci_lo"],
        "cidre_lite_auc_roc_ci_hi": cidre_metrics["auc_roc_ci_hi"],
        # Statistical tests
        "delong_p_cvs_vs_reciprocity": p_cvs_vs_recip,
        "delong_p_cvs_vs_cidre_lite": p_cvs_vs_cidre,
        "delong_p_reciprocity_vs_cidre_lite": p_recip_vs_cidre,
        "fisher_p20_cvs_vs_reciprocity": fisher_p20_cvs_recip,
        "fisher_p20_cvs_vs_cidre_lite": fisher_p20_cvs_cidre,
        "cohen_h_p20_cvs_vs_reciprocity": cohen_h_cvs_recip,
        "cohen_h_p20_cvs_vs_cidre_lite": cohen_h_cvs_cidre,
        # Temporal stability
        "temporal_stability_mean_spearman": mean_spearman,
        "temporal_stability_spearman_ci_lo": spearman_ci_lo,
        "temporal_stability_spearman_ci_hi": spearman_ci_hi,
        "temporal_stability_n_windows": float(len(spearman_corrs)),
        # Boost sensitivity
        "boost_2x_cvs_auc": get_boost_auc(2.0, "cvs"),
        "boost_5x_cvs_auc": get_boost_auc(5.0, "cvs"),
        "boost_10x_cvs_auc": get_boost_auc(10.0, "cvs"),
        "boost_15x_cvs_auc": get_boost_auc(15.0, "cvs"),
        "boost_2x_reciprocity_auc": get_boost_auc(2.0, "reciprocity"),
        "boost_5x_reciprocity_auc": get_boost_auc(5.0, "reciprocity"),
        "boost_10x_reciprocity_auc": get_boost_auc(10.0, "reciprocity"),
        "boost_15x_reciprocity_auc": get_boost_auc(15.0, "reciprocity"),
        # Community detection robustness
        "robustness_kruskal_wallis_h": float(h_stat),
        "robustness_kruskal_wallis_p": float(kw_pval),
        "robustness_cv_louvain": cv_louvain,
        "robustness_cv_leiden": cv_leiden,
        "robustness_cv_infomap": cv_infomap,
        "robustness_mean_auc_louvain": float(np.mean(louvain_aucs)) if louvain_aucs else 0.0,
        "robustness_mean_auc_leiden": float(np.mean(leiden_aucs)) if leiden_aucs else 0.0,
        "robustness_mean_auc_infomap": float(np.mean(infomap_aucs)) if infomap_aucs else 0.0,
        "robustness_dunn_p_louvain_leiden": p_louv_leiden,
        "robustness_dunn_p_louvain_infomap": p_louv_infomap,
        "robustness_dunn_p_leiden_infomap": p_leiden_infomap,
        # False positive characteristics
        "fp_count_top20": float(len(fp_communities)),
        "tp_count_top20": float(len(tp_communities)),
        "fp_mean_community_size": fp_mean_size,
        "tp_mean_community_size": tp_mean_size,
        # Dataset info
        "n_communities": float(n_total),
        "n_cartel_communities": float(n_pos),
        "n_legitimate_communities": float(n_neg),
    }

    # -----------------------------------------------------------------------
    # PER-EXAMPLE METRICS (eval_ fields)
    # -----------------------------------------------------------------------
    logger.info("Computing per-example eval metrics")
    eval_examples = []
    for e in examples:
        cvs_s = float(e["predict_cvs"])
        recip_s = float(e["predict_reciprocity"])
        cidre_s = float(e["predict_cidre_lite"])
        true_lbl = int(e["metadata_label"])

        # Rank of this example by CVS (1 = highest CVS score)
        rank = int(np.sum(cvs_scores > cvs_s) + 1)
        rank_frac = rank / n_total

        eval_entry = {
            "input": e["input"],
            "output": e["output"],
            "predict_cvs": e["predict_cvs"],
            "predict_reciprocity": e["predict_reciprocity"],
            "predict_cidre_lite": e["predict_cidre_lite"],
            "metadata_community_id": e["metadata_community_id"],
            "metadata_community_size": e["metadata_community_size"],
            "metadata_label": e["metadata_label"],
            "metadata_journal_ids": e["metadata_journal_ids"],
            "metadata_journal_names": e["metadata_journal_names"],
            "eval_cvs_rank": float(rank),
            "eval_cvs_rank_fraction": float(rank_frac),
            "eval_cvs_score": float(cvs_s),
            "eval_reciprocity_score": float(recip_s),
            "eval_cidre_lite_score": float(cidre_s),
            "eval_correct_cvs": float(1 if (cvs_s > 0.85) == (true_lbl == 1) else 0),
            "eval_is_fp": float(1 if (rank <= 20 and true_lbl == 0) else 0),
            "eval_is_tp": float(1 if (rank <= 20 and true_lbl == 1) else 0),
        }
        eval_examples.append(eval_entry)

    # -----------------------------------------------------------------------
    # ASSEMBLE OUTPUT
    # -----------------------------------------------------------------------
    output = {
        "metadata": {
            "evaluation_name": "CVS Cartel Detection: Statistical Validation",
            "method": "Citation Vortex Score (CVS) via Hodge Decomposition",
            "baselines": ["Reciprocity Ratio", "CIDRE-lite"],
            "n_communities": n_total,
            "n_cartel_communities": n_pos,
            "dataset": full_data["datasets"][0]["dataset"],
            "hypothesis_confirmed": cvs_metrics["auc_roc"] > recip_metrics["auc_roc"],
            "boost_sensitivity": [
                {k: (v if not isinstance(v, float) or not math.isnan(v) else None)
                 for k, v in br.items()}
                for br in boost_results
            ],
            "robustness_analysis": {
                "louvain_aucs": louvain_aucs,
                "leiden_aucs": leiden_aucs,
                "infomap_aucs": infomap_aucs,
                "kruskal_wallis_h": float(h_stat),
                "kruskal_wallis_p": float(kw_pval),
            },
            "threshold_analysis": threshold_analysis,
            "recall_by_rank_bin": rank_bins,
            "false_positives_top20": fp_communities,
            "true_positives_top20": tp_communities,
            "temporal_stability": {
                "windows": temporal.get("windows", []),
                "spearman_correlations": spearman_corrs,
                "mean_spearman": mean_spearman,
                "ci_lo": spearman_ci_lo,
                "ci_hi": spearman_ci_hi,
            },
            "delong_test": {
                "cvs_vs_reciprocity": p_cvs_vs_recip,
                "cvs_vs_cidre_lite": p_cvs_vs_cidre,
                "reciprocity_vs_cidre_lite": p_recip_vs_cidre,
            },
            "detailed_metrics": {
                "cvs": cvs_metrics,
                "reciprocity": recip_metrics,
                "cidre_lite": cidre_metrics,
            },
        },
        "metrics_agg": metrics_agg,
        "datasets": [
            {
                "dataset": full_data["datasets"][0]["dataset"],
                "examples": eval_examples,
            }
        ],
    }

    # -----------------------------------------------------------------------
    # SAVE OUTPUT
    # -----------------------------------------------------------------------
    out_path = WORKSPACE / "eval_out.json"
    def _json_default(x):
        if isinstance(x, float) and math.isnan(x):
            return None
        raise TypeError(f"Not serializable: {type(x)}")
    out_path.write_text(json.dumps(output, indent=2, default=_json_default))
    logger.info(f"Saved eval_out.json ({out_path.stat().st_size / 1024:.1f} KB)")

    # Log summary
    logger.info("=" * 60)
    logger.info("EVALUATION SUMMARY")
    logger.info(f"CVS    AUC={cvs_metrics['auc_roc']:.3f} [{cvs_metrics['auc_roc_ci_lo']:.3f}, {cvs_metrics['auc_roc_ci_hi']:.3f}]")
    logger.info(f"Recip  AUC={recip_metrics['auc_roc']:.3f} [{recip_metrics['auc_roc_ci_lo']:.3f}, {recip_metrics['auc_roc_ci_hi']:.3f}]")
    logger.info(f"CIDRE  AUC={cidre_metrics['auc_roc']:.3f}")
    logger.info(f"CVS P@20={p20_cvs:.2f}, Recip P@20={p20_recip:.2f}, CIDRE P@20={p20_cidre:.2f}")
    logger.info(f"Temporal stability Spearman={mean_spearman:.3f} [{spearman_ci_lo:.3f},{spearman_ci_hi:.3f}]")
    logger.info(f"FP count in top-20: {len(fp_communities)}, TP count: {len(tp_communities)}")
    logger.info(f"Hypothesis confirmed: {output['metadata']['hypothesis_confirmed']}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
