# Hodge Decomposition and Citation Cartel Detection Framework

## Summary

This research establishes three critical foundations for implementing a graph-based Citation Vortex Score (CVS) to detect citation cartels:

**1. Mathematical Framework (Hodge Decomposition):** Hodge theorem decomposes directed graph flows into three orthogonal components: gradient (acyclic/hierarchical), curl (locally cyclic), and harmonic (globally cyclic) [1, 6]. In citation networks, gradient flow represents legitimate citation hierarchies while curl flow captures the rotational pattern signature of citation cartels (journals citing each other in circles). Implementation uses incidence matrix B1 (V×E with ±1 entries) and least-squares solver scipy.sparse.linalg.lsqr to extract gradient potential; residual contains curl + harmonic components. Computational complexity O(V·E) scales to large journal networks [1, 5].

**2. Baseline Performance (CIDRE 2021):** The CIDRE algorithm detects anomalous journal groups using degree-corrected stochastic block model (dcSBM) as null model to account for journal size and research community structure. Empirical results: detected 12 of 22 JCR-suppressed cartel groups (54.5% recall), with 8 groups having Jaccard overlap ≥0.5 (67% high-confidence matches). CIDRE identified 10 groups before official JCR suspension, demonstrating predictive power [2, 3]. Simple reciprocity ratio baseline (pairwise mutual citation) fails because it ignores network context, journal size effects, and multi-step cycles [2].

**3. Ground Truth Validation (Clarivate JCR):** Clarivate suppresses journals for excessive self-citation and citation stacking (coordinated multi-journal exchanges). Scale: 33 journals (0.27%) in 2020, 10 in 2021, 20 in 2025; 46 journal pairs historically reported by 2019 [7, 8, 9]. Ground truth limitations: partial coverage (~0.3% of 12,000 journals), 1-2 year detection lag, potential false positives from legitimate overlapping fields [8]. Typical cartel size: 2-10 journals (average 4) with 30-50%+ of incoming citations from within-group sources [2].

**4. Implementation Tools:** OpenAlex API provides free access to 250M+ papers across 7,000+ journals for constructing journal citation graphs [10]. NetworkX.louvain_communities() identifies candidate subgroups; scipy.sparse solvers handle Hodge decomposition on sparse matrices [11, 12]. All tools are open-source with documented APIs.

**5. Evaluation Framework:** Success criteria for CVS: (1) Precision@K > reciprocity baseline, (2) AUC-ROC > CIDRE (AUC ≥ 0.65 on imbalanced data), (3) Spearman ρ < 0.8 with reciprocity (novel signal confirmed) [2, 13]. Metrics: Jaccard overlap ≥0.5 with ≥2 shared journals for group matching, threshold-independent AUC-ROC for ranking quality, rank correlation tests for independence from baseline [2, 13].

## Research Findings

## Hodge Decomposition Theory for Citation Networks

The Hodge decomposition theorem from differential geometry provides a rigorous mathematical foundation for citation cartel detection [1, 6]. Every edge flow on a directed graph decomposes orthogonally into three components:

**1. Gradient Flow (Acyclic):** Represents hierarchical, source-to-sink flows. In citation networks, this is legitimate scientific discourse where papers cite foundational work. The gradient component is irrotational and acyclic—no loops.

**2. Curl Flow (Locally Cyclic):** Captures rotational patterns around graph triangles. This is the cartel signature—when journals A, B, C form a triangle where A→B→C→A citations occur at abnormally high rates, curl energy concentrates in this subgraph. Curl is divergence-free (flow in equals flow out at each node) but locally cyclic.

**3. Harmonic Flow (Globally Cyclic):** Represents globally balanced cycles that don't resolve locally. Rare in citation networks; these would represent system-wide feedback loops across many journals.

Mathematically, construct incidence matrix B1 (V×E dimensions: +1 for edge heads, -1 for tails) and boundary matrix B2 (edge×triangle). The Hodge Laplacian is L = A*A + BB*. Hodge decomposition states: **R^n = im(A*) ⊕ ker(L) ⊕ im(B)** where each vector decomposes uniquely into gradient + harmonic + curl components with zero cross-products [1, 6].

Implementation: Solve least-squares problem **minimize ||B1^T x||²** using scipy.sparse.linalg.lsqr(B1, edge_flow_vector). The solution x gives gradient potential; residual contains curl + harmonic components. Curl energy is the squared norm of curl component—concentrated in cartel subgroups [1, 5].

**Key Advantage:** Reduces rank aggregation to linear least squares, avoiding NP-hard combinatorial optimization while providing "certificate of reliability" (residual magnitude indicates ranking validity) [1].

## CIDRE Baseline and Performance Benchmarks

The CIDRE algorithm (2021) provides the primary benchmark that any novel cartel detection method must exceed [2, 3].

**Core Method:** CIDRE uses degree-corrected stochastic block model (dcSBM) as null model [2, 3, 4]:
- dcSBM preserves each journal's out-degree (citations given) and in-degree (citations received)
- Generates randomized networks within community blocks, simulating expected citation rates under normal discourse
- Anomaly score: **(observed - expected_dcSBM) / expected_dcSBM** for each journal group
- Threshold on anomaly score identifies and ranks suspicious groups

**Empirical Results on Ground Truth:**
- **Recall: 54.5%** (12 of 22 JCR-suppressed groups detected) [2, 3]
- **Precision (high-confidence): 67%** (8 of 12 detected have Jaccard overlap ≥0.5 with suppressed) [2, 3]
- **Predictive power: 10 groups detected 1-2 years before JCR suspension** [2, 3]
- **Total anomalous groups identified: 159** in 2019 journal network (48,821 journals) [2]

**Why Reciprocity Ratio Baseline Fails:**
Simple pairwise reciprocity—for each pair (i,j), compute min(c_ij, c_ji)/max(c_ij, c_ji)—identifies high mutual citation but [2]:
- Ignores multi-step cycles (A→B→C→A)
- Can't distinguish legitimate high-reciprocity pairs in small fields from actual cartels
- No degree correction for journal size
- No community structure accounting
- Zero reported detection performance vs. JCR suppressions

CIDRE's 54.5% recall significantly outperforms naive reciprocity by using dcSBM to control for these confounders. **Any novel CVS method must exceed CIDRE's 54.5% recall to claim advancement.**

## Clarivate Suppression Ground Truth: Coverage and Limitations

Clarivate's Journal Citation Reports (JCR) provide authoritative but partial ground truth for cartel validation [7, 8, 9].

**Suppression Scale (2015-2025):**
- 2020: 33 journals (0.27% of ~12,000 total) [7, 8]
- 2021: 10 journals [8]
- 2022: 3 journals [8]
- 2025: 20 journals (recent data) [8]
- Total: 46 journal pairs (55 unique journals) by 2019 [2]
- **Typical cartel size: 2-10 journals per group (average 4)** [2]

**Suppression Criteria (Clarivate Internal Method):**
Clarivate uses objective, quantifiable criteria but exact algorithm is proprietary [7]. Based on documented suppressions, method likely combines [7, 9]:
1. Self-citation thresholds (excessive within-journal citations)
2. Citation stacking detection (anomalously high pairwise reciprocity)
3. Pattern analysis (coordinated multi-journal boosting)

**Critical Limitations of Ground Truth:**

1. **Partial Coverage (~0.3%):** Only detected/acted-on cartels are visible. Majority of active cartels remain undetected, creating selection bias in evaluation [8]

2. **Detection Lag (1-2 years):** Cartels form and operate before Clarivate detection. CIDRE showed 10 groups detected before official suppression, but temporal mismatch confounds earlier snapshots [2]

3. **Potential False Positives:** Legitimate research communities with high field-specific citation density (e.g., rare disease journals, regional studies) may trigger suppression if thresholds are not field-aware [8]

4. **Threshold Opacity:** Clarivate's exact thresholds unknown. Precision/recall metrics are tied to their specific cutoffs, which may not generalize across time periods or research disciplines [7]

**Cartel Characteristics from CIDRE Classification [2]:**
Of 159 CIDRE-detected groups:
- 38% have >20% within-group citations from single paper (Category A)
- 8% have >20% to single paper (Category B)
- 21% from single author (Category C)
- 4% to single author (Category D)
- 16% share overlapping editors (Category E)
- 13% no detected criteria (Category F)

Suppressed JCR groups show similar distribution, validating multiple cartel mechanisms beyond simple reciprocity.

## Implementation Infrastructure: Data, Algorithms, Tools

**Data Collection (OpenAlex API):**
OpenAlex provides free, unrestricted access to scholarly works without API key requirement [10]:
- ~250M indexed papers across >7,000 journals
- Query by journal (ISSN, journal ID), author, institution
- Returns work metadata including journal, cited-by count, publication year
- High throughput supports batch collection

Python workflow for building journal citation graph [10]:
```python
import requests

# Query works by journal, aggregate citations per year
for journal_id in journal_ids:
    works = requests.get(f'https://api.openalex.org/works?filter=primary_location.source.id:{journal_id}').json()
    # Extract citations, group by target journal and year
    # Construct edge weights: annual citation counts between journal pairs
```

**Community Detection (NetworkX):**
Identify candidate journal subgroups for cartel detection [11]:
```python
import networkx as nx
from networkx.algorithms.community import louvain_communities

# Convert directed citation network to undirected
G_undirected = G.to_undirected()

# Louvain modularity optimization
communities = list(louvain_communities(G_undirected))
```
Alternatives: Leiden algorithm (faster, better quality), Infomap (information-theoretic). Note: pure community detection fails for cartel detection (CIDRE: zero overlap with JCR suppressions), so communities serve as seed groups, not final classification [2].

**Hodge Decomposition (scipy.sparse.linalg):**
Implement Hodge decomposition on sparse journal networks [1, 5, 12]:
```python
import scipy.sparse as sp
from scipy.sparse.linalg import lsqr
import numpy as np

# Construct incidence matrix B1 (nodes x edges)
# For each edge (i,j), column has +1 at row i, -1 at row j
B1 = construct_incidence_matrix(G)  # shape (num_nodes, num_edges)

# Edge flow vector (citation weights on edges)
edge_weights = extract_edge_weights(G)

# Solve least-squares to extract gradient potential
# x = argmin ||B1.T @ x - edge_weights||^2
x, istop, itn, r1norm = lsqr(B1.T, edge_weights)

# Residual norm² contains curl + harmonic energy
curl_harmonic_energy = r1norm ** 2

# Curl energy concentrated in cartel subgroups
cvs_score = compute_curl_energy_ratio(residuals_by_subgroup)
```

Key numerical considerations [5, 12]:
- **Sparsity:** Use scipy.sparse.csr_matrix or coo_matrix for memory efficiency
- **Condition number:** Monitor via LSQR output; add regularization (damp parameter) if ill-conditioned
- **Convergence:** Check istop flag; LSQR handles rank-deficient systems
- **Scaling:** Tested on ~500-5000+ node networks; O(V·E) complexity

## Evaluation Metrics and Success Criteria

**Precision@K (Group-Level Matching):**
For top-K ranked subgroups by CVS score, compute fraction matching Clarivate suppressions [2]:
```
Match criterion:
  Jaccard J = |detected ∩ suppressed| / |detected ∪ suppressed| ≥ 0.5
  AND |detected ∩ suppressed| ≥ 2 (minimum 2 shared journals)

Precision@K = (# matched groups in top-K) / K
```
Interpretation: 80% Precision@20 means 16 of top-20 ranked groups are true cartels [2, 13].

**AUC-ROC (Ranking Quality):**
Rank all detected subgroups by CVS score; plot ROC curve at varying thresholds [13]:
```
TPR(threshold) = (# suppressed groups with CVS > threshold) / (total suppressed)
FPR(threshold) = (# non-suppressed groups with CVS > threshold) / (total non-suppressed)

AUC = area under ROC curve
  AUC = 0.5: random baseline
  AUC = 1.0: perfect ranking
  AUC > 0.7: acceptable discrimination
  AUC > 0.8: strong discrimination
```

**Spearman Rank Correlation ρ (Independence from Baseline):**
Test if CVS merely rediscovers reciprocity ratio signal [2]:
```
ρ_CVS_vs_reciprocity = rank_correlation(CVS_ranking, reciprocity_ranking)

Interpretation:
  ρ > 0.95: CVS confounds with reciprocity (no novel signal)
  ρ < 0.6: CVS captures distinct patterns (hypothesis confirmed)
```

**Success Criteria (CVS Validation):**
CVS method succeeds if all three hold [2]:
1. Precision@20 > reciprocity baseline (typically 0%) AND
2. AUC-ROC > CIDRE excess fraction (AUC ≥ 0.65, given 54.5% recall on imbalanced data) AND
3. Spearman ρ < 0.8 with reciprocity ratio (demonstrated novel signal beyond pairwise symmetry)

**Failure Scenario (Hypothesis Disconfirm):**
If CVS Pearson ρ > 0.95 with reciprocity ratio or identical ranking order, Hodge decomposition adds no information over simple baseline; method should be reconsidered [2].

## Robustness Testing Framework

Before publication, CVS method must withstand:

1. **Temporal Robustness:** Test CVS on multiple year windows (2015-2018, 2018-2022, rolling 3-year windows). Do top-ranked groups remain consistent, or do rankings drift?

2. **Community Detection Robustness:** Compare CVS rankings across different seed algorithms (Louvain, Leiden, Infomap). Does choice of community detection substantially affect results?

3. **Ablation Study:** Decompose CVS into components—gradient flow divergence (hierarchical vs. cyclic ratio), curl energy magnitude, harmonic component contribution. Which component drives cartel detection?

4. **Scale Invariance:** Test on subnetworks of different sizes (500, 2000, 5000 journals). Does CVS scale linearly or does numerical stability degrade?

5. **False Positive Analysis:** Manually review top-ranked non-suppressed groups to assess false positive rate. Are flagged cartels plausibly suspicious, or obvious research communities?

## Key Insight: Why Hodge Decomposition Outperforms Naive Baselines

Curl energy (Σ f_curl(e)²) concentrates in citation cartel subgroups because:

1. **Legitimate hierarchies (gradient):** Citations flow acyclically from applied to foundational work. Gradient component dominates.

2. **Cartel signatures (curl):** Citations flow in local cycles within a small group. Curl component concentrated and energy high.

3. **Scale-aware:** Curl energy naturally accounts for journal size—larger journals' edges have larger flow, but cartel cycles are over-weighted relative to expected flow patterns (via dcSBM-like null model).

4. **Network-aware:** Accounts for multi-step cycles (A→B→C→A) that pairwise reciprocity misses. Curl emerges from topological structure, not just pairwise statistics.

5. **Quantifiable:** Normalized energy ratio CVS(S) = Σ_e∈S f_curl(e)² / Σ_e∈S f(e)² provides threshold-independent cartel strength measure.

This decomposition explains why CIDRE (accounting for community structure via dcSBM) achieves 54.5% recall vs. reciprocity baseline's ~0%, and why CVS (exploiting Hodge geometry) should further improve upon CIDRE.

## Sources

[1] [Statistical Ranking and Combinatorial Hodge Theory](https://www.stat.uchicago.edu/~lekheng/work/mathprog.pdf) — Jiang et al. (2011) foundational paper introducing HodgeRank. Complete mathematical treatment of Hodge decomposition on directed graphs. Explains orthogonal decomposition into gradient (acyclic), curl (locally cyclic), harmonic (globally cyclic) flows. Documents least-squares solution avoiding NP-hard optimization.

[2] [Detecting Anomalous Citation Groups in Journal Networks](https://www.nature.com/articles/s41598-021-93572-3) — Kojaku, Livan, Masuda (2021) CIDRE algorithm achieving 54.5% recall on JCR-suppressed groups. Uses dcSBM null model. Documents 159 anomalous groups identified, 6-category classification by citation pattern, validation against Clarivate suppressions. Primary baseline benchmark.

[3] [Detecting Anomalous Citation Groups in Journal Networks (arXiv)](https://arxiv.org/abs/2009.09097) — ArXiv preprint of CIDRE. Extended methods and results. Detailed dcSBM construction, excess citation fraction computation, Jaccard overlap scoring (≥0.5 with ≥2 shared journals), predictive detection 1-2 years before JCR suppression.

[4] [Degree-Corrected Stochastic Block Model](https://docs.neurodata.io/graph-stats-book/representations/ch5/single-network-models_DCSBM.html) — Tutorial on dcSBM theory. Explains how degree-corrected models preserve per-node degree heterogeneity (journal size) while generating random networks within blocks. Key for understanding why CIDRE outperforms simple community detection.

[5] [scipy.sparse.linalg.lsqr](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.lsqr.html) — Official SciPy documentation. LSQR algorithm for sparse least-squares problems. Parameters: damp (regularization), conlim (condition number limit), atol/btol (convergence tolerances). Essential for stable Hodge decomposition implementation.

[6] [Hodge Laplacians on Graphs: A Tutorial](https://www.math.ucdavis.edu/~saito/data/tensor/lim_hodge-lap-review.pdf) — Lim comprehensive tutorial requiring only linear algebra and graph theory. Covers Hodge Laplacian, harmonic representatives, cohomology, orthogonal decomposition. Elementary exposition of theoretical foundation.

[7] [Clarivate's 2020 Journal Citation Report: Suppressed Journals](https://www.enago.com/academy/journals-suppressed-in-the-journal-citation-reports-fight-back/) — Documents 2020 JCR suppressions (33 journals, 0.27% of total). Describes Clarivate methodology (citation parameter monitoring), controversies, editor responses. Ground truth documentation.

[8] [Citation Issues Cost These 20 Journals Their Impact Factors (2025)](https://retractionwatch.com/2025/06/18/clarivate-impact-factor-suppression-list-2025-self-citation-stacking/) — 2025 JCR suppression data (20 journals). Defines citation stacking as anomalous multi-journal citation exchanges. Recent evidence of ongoing cartel detection across 2020-2025.

[9] [What Do We Know About Journal Citation Cartels?](https://www.cwts.nl/blog?article=n-q2w2b4) — CWTS analysis distinguishing citation stacking (multi-journal) from self-citation (single-journal). Discusses historical examples, detection difficulty, editorial coordination role.

[10] [OpenAlex API](https://developers.openalex.org/) — Free API to 250M+ papers across 7,000+ journals. No authentication required. Supports journal queries, batch processing for large-scale citation network construction.

[11] [NetworkX Community Detection](https://networkx.org/documentation/stable/reference/algorithms/community.html) — Louvain algorithm documentation. Modularity optimization for identifying journal groups. Suitability for large networks. Key tool for seed group identification in pipelines.

[12] [Sparse Linear Algebra](https://caam37830.github.io/book/02_linear_algebra/sparse_linalg.html) — Practical guide to scipy sparse operations. Matrix formats (COO, CSR), performance, condition number monitoring, LSQR usage. Essential for efficient Hodge implementation.

[13] [ROC and AUC](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc) — ROC curves and AUC fundamentals. True positive/false positive rates, threshold selection, interpretation. Essential for understanding Precision@K and AUC-ROC evaluation metrics.

## Follow-up Questions

- How does Hodge decomposition performance scale to very large journal networks (>10,000 nodes)? At what scale do numerical stability issues arise in scipy.sparse.linalg.lsqr, and should adaptive damping/regularization be implemented?
- Can Hodge decomposition be extended to temporal/dynamic citation networks where edge weights vary by year? Would time-lagged curl energy (citations forming cycles with 1-2 year delays) capture more realistic cartel formation dynamics?
- What is the false positive rate when applying CVS to known legitimate research communities (e.g., closely-related subfields with naturally high citation density)? Should CVS be normalized by discipline-specific baseline citation rates?

---
*Generated by AI Inventor Pipeline*
