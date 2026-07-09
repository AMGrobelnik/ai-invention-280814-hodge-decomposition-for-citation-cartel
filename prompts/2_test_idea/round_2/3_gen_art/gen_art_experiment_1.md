# gen_art_experiment_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_art`
> Run: `run_HMncsxsr6ltD` — Hodge Decomposition for Citation Cartel Detection
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-07-09 01:54:47 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact executor (Step 3.3: GEN_ART in the invention loop)

Executing a plan to produce a concrete artifact.
GEN_PAPER_TEXT will use your artifact in the next paper draft.

Rigorous artifact with clear results → strong paper. Sloppy artifact → misdirected research.
</your_role>
</ai_inventor_context>

<research_methodology>
Design experiments like a researcher, not a programmer running a script.

- Every method needs a meaningful baseline — the current standard approach, not a strawman.
- Control your variables. When comparing methods, hold everything else constant.
- Results need variance, not just point estimates. A single run proves nothing.
- Implement the proposed method and baseline side-by-side in the same pipeline to eliminate implementation-level confounds.
</research_methodology>

<task>
Implement the research methodology as a production-ready experimental system.
Adapt your implementation approach based on the hypothesis and domain requirements.
</task>

<critical_requirements>
- Fully implement the methodology described in hypothesis
- Use appropriate frameworks based on research domain
- Load and process data from the specified data_filepath
- Complete working systems
- Handle all edge cases, errors, and exceptions properly
- Always implement baseline comparison method
</critical_requirements>

<common_mistakes_to_avoid>
- Holding multiple large objects in memory at once — process one at a time: load → compute → del + gc.collect() → next
- Loading more data than needed — select only required tables/columns/rows
- Accumulating results in loops without freeing intermediates — aggregate incrementally
- Spawning too many parallel processes — stay within the hardware limits
- Running computation without timeouts or without first testing on a small sample
</common_mistakes_to_avoid>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<workspace>
Your workspace: `/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_2/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/`:
GOOD: `/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/file.py`, `/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_experiment_1_idx2
type: experiment
title: CVS cartel detection on real networks
summary: >-
  Validate Citation Vortex Score (CVS) using Hodge decomposition on real 96-journal OpenAlex network against Clarivate ground
  truth, test robustness across community detection methods and synthetic boost levels.
runpod_compute_profile: cpu_light
implementation_pseudocode: "# Citation Vortex Score (CVS) Experiment: Real-world Validation\n# ============================================================\n\
  # Duration: 6h total (code, debug, test, full run)\n# Executor: Load network, run CVS method, compute metrics, compare baselines\n\
  \n# STAGE 1: SETUP & DATA LOADING (15 min)\n# ======================================\n1. Load dependencies\n   - import\
  \ networkx, numpy, scipy.sparse, scipy.sparse.linalg, pandas, json\n   - pip install python-louvain leiden (community detection)\n\
  \   - pip install networkx==3.2+\n\n2. Load real journal citation network from dependency artifact\n   - Input: /path/to/full_data_out.json\
  \ or full_journal_citation_network.json\n   - Parse JSON: extract nodes (journals) and weighted edges (citation counts)\n\
  \   - Build NetworkX DiGraph: nx.DiGraph() with edge weights w(i→j) = c_ij\n   - Verify: 96 nodes, 888 edges, total citations\
  \ = 2644\n\n3. Load ground truth cartel labels from cartel_ground_truth.json\n   - Parse: list of 17 cartel journal groups\
  \ (ISSNs, journal_names, suppression_years)\n   - Create ground_truth_set: set of (issn_i, issn_j) pairs for each cartel\n\
  \   - Group by cluster: record which journals belong to same cartel (for Jaccard matching)\n\n4. Create data structures\n\
  \   - node_id_map: issn → integer (for matrix indexing)\n   - node_labels: integer → issn (reverse mapping)\n   - adjacency\
  \ list: node → neighbors + edge weights\n\n# STAGE 2: HODGE DECOMPOSITION IMPLEMENTATION (60 min)\n# =====================================================\n\
  5. Implement Hodge decomposition on directed weighted graph\n   Algorithm:\n   a. Build incidence matrix B1 (|V| × |E|)\n\
  \      - Column j represents edge (u, v)\n      - Row u: +1 if u is head, -1 if u is tail, 0 otherwise\n      - Sparse format:\
  \ scipy.sparse.csr_matrix\n   \n   b. Symmetrize directed graph for decomposition\n      - For each directed edge (i→j)\
  \ with weight w_ij:\n        - Symmetric part: s_ij = (w_ij + w_ji) / 2\n        - Skew part: a_ij = (w_ij - w_ji) / 2\n\
  \      - Use skew-symmetric part for curl detection\n   \n   c. Solve least-squares to extract gradient component\n    \
  \  - Objective: minimize ||B1 @ x||^2 where x is node potential\n      - Use: scipy.sparse.linalg.lsqr(B1, flow_vector,\
  \ atol=1e-6)\n      - Solution: x* = node potentials\n      - Gradient flow f_grad[i→j] = x[j] - x[i]\n   \n   d. Compute\
  \ residual (curl + harmonic) component\n      - f_curl_residual[i→j] = f[i→j] - f_grad[i→j]\n      - Store as edge weights\
  \ in sparse format\n\n6. Helper function: hodge_decompose(digraph, flow_weights=None)\n   Input: NetworkX DiGraph, optional\
  \ custom flow weights\n   Output: {'f_grad': dict, 'f_residual': dict, 'f_total': dict}\n   - Default flow_weights: graph\
  \ edge weights (citation counts)\n   - Normalize flows to [0,1] range for comparability across subgraphs\n\n# STAGE 3: CVS\
  \ SCORING & COMMUNITY DETECTION (90 min)\n# ====================================================\n7. Implement CVS score\
  \ calculation\n   def compute_cvs(subgraph, hodge_components):\n       \"\"\"CVS(S) = sum||f_residual(e)||^2 / sum||f(e)||^2\
  \ for edges in S\"\"\"\n       residual_energy = sum(hodge_components['f_residual'][e]**2 for e in subgraph.edges())\n \
  \      total_energy = sum(hodge_components['f_total'][e]**2 for e in subgraph.edges())\n       if total_energy == 0:\n \
  \          return 0.0\n       return residual_energy / total_energy\n\n8. Run community detection (3 methods)\n   a. Louvain\
  \ (python-louvain library)\n      - Run with 10 random seeds\n      - Extract communities as subgraphs\n      - Record CVS\
  \ for each community per seed\n      - Compute mean, std, min, max CVS across seeds\n   \n   b. Leiden algorithm (leiden\
  \ library, more stable)\n      - Run with same 10 random seeds\n      - Extract communities\n      - Compute CVS, mean/std\
  \ across seeds\n   \n   c. Infomap (optional, if available; fallback to Louvain repeated)\n      - Single run (deterministic\
  \ or fixed seed)\n      - Compute CVS per community\n\n9. Rank all detected communities by CVS (descending)\n   - Global\
  \ ranking: merge communities from all 3 methods, rank by CVS\n   - Record: community_id, method, seed, cvs_score, member_journals,\
  \ size\n\n# STAGE 4: GROUND TRUTH MATCHING (45 min)\n# ========================================\n10. Implement Jaccard matching\
  \ to ground truth\n    def jaccard_overlap(detected_set, truth_set):\n        \"\"\"Jaccard = |intersection| / |union|\"\
  \"\"\n        return len(intersection) / len(union)\n    \n    Matching rule: detected community matches ground-truth cartel\
  \ if Jaccard ≥ 0.5\n\n11. Compute real-data metrics\n    a. Precision@K: Among top-K CVS-ranked communities, what fraction\
  \ match ground truth?\n       - Compute for K ∈ {5, 10, 20}\n       - Per-method breakdown\n    \n    b. Recall@K: Of 17\
  \ ground-truth cartels, how many are found in top-K?\n       - Compute for K ∈ {5, 10, 20, 50}\n    \n    c. AUC-ROC (binary\
  \ classification)\n       - For each detected community: binary label (matches truth OR not)\n       - Rank by CVS descending\n\
  \       - Plot ROC curve, compute AUC\n\n12. Generate results table (real network)\n    Columns: method | seed | community_size\
  \ | cvs_score | jaccard_overlap | matches_truth | member_journals\n    Rows: one per detected community (sorted by CVS)\n\
  \n# STAGE 5: SYNTHETIC VALIDATION (120 min)\n# ========================================\n13. Generate synthetic networks\
  \ with injected cartels\n    For each boost level b ∈ {2, 5, 10, 15}:\n        a. Copy real network\n        b. Select random\
  \ 8-journal subsets (8 random subsets per boost level)\n        c. For each subset, multiply within-subset edge weights\
  \ by factor b\n           - w_ij *= b if both i, j in subset\n        d. Save synthetic network state\n\n14. Run CVS on\
  \ each synthetic network\n    - Apply Hodge decomposition to synthetic network (new gradient/residual)\n    - Run community\
  \ detection (Louvain only for speed, 5 seeds)\n    - Rank communities by CVS\n\n15. Compute AUC-ROC for synthetic cartels\n\
  \    For each boost level:\n        - Create binary labels: 1 if community overlaps injected cartel (Jaccard ≥ 0.5), 0 else\n\
  \        - Rank by CVS descending\n        - Compute AUC\n        - Record: boost_level | num_subsets | auc_mean | auc_std\
  \ | auc_min | auc_max\n\n16. Generate AUC-vs-boost sensitivity curve\n    Plot: x-axis = boost level {2,5,10,15}, y-axis\
  \ = AUC\n    Show: mean AUC with error bars (std across 8 subsets per boost)\n    Reference: Hypothesis claimed AUC=1.0\
  \ at 15× boost\n\n# STAGE 6: BASELINE COMPARISONS (75 min)\n# =======================================\n17. Implement reciprocity\
  \ ratio baseline\n    def reciprocity_ratio(i, j):\n        \"\"\"For edge pair i↔j, ratio of mutual to total citations\"\
  \"\"\n        citations_ij = graph[i][j]['weight']\n        citations_ji = graph[j][i]['weight'] if graph.has_edge(j, i)\
  \ else 0\n        if citations_ij + citations_ji == 0:\n            return 0\n        return min(citations_ij, citations_ji)\
  \ / max(citations_ij, citations_ji)\n    \n    Score subgroups: mean reciprocity_ratio over all edges in subgroup\n    Rank\
  \ communities by reciprocity score descending\n\n18. Implement CIDRE-lite baseline\n    def cidre_lite(subgroup):\n    \
  \    \"\"\"Fraction of edges within subgroup (excess over expected)\"\"\"\n        within_edges = sum(1 for u,v in subgroup.edges()\
  \ if u,v in subgroup)\n        total_possible = len(subgroup) * (len(subgroup) - 1)\n        return within_edges / total_possible\
  \ if total_possible > 0 else 0\n    \n    **CRITICAL**: Original CIDRE uses dcSBM null model. CIDRE-lite skips this.\n \
  \   Note: Hypothesis reports CIDRE-lite AUC=0.0 before sign correction.\n    Compute both forward and sign-inverted AUC;\
  \ report both to clarify anti-correlation.\n\n19. Compare metrics: CVS vs Reciprocity vs CIDRE-lite\n    For real network:\n\
  \        - Compute all 3 baseline scores for each community\n        - Rank by each score\n        - Compute precision@5,\
  \ @10, @20 for each baseline\n        - Compute AUC-ROC for each baseline\n        - Table: baseline | precision@5 | precision@10\
  \ | precision@20 | AUC\n    \n    For synthetic networks (boost level 15× only):\n        - Compute AUC for CVS, reciprocity,\
  \ CIDRE-lite on all 8 synthetic networks\n        - Table: method | auc_mean | auc_std | auc_range\n\n# STAGE 7: STABILITY\
  \ & ROBUSTNESS (60 min)\n# =========================================\n20. Test robustness across Louvain random seeds\n\
  \    Already recorded in STAGE 3: 10 seeds per run\n    Analyze: Do top communities remain stable across seeds?\n    - Compute\
  \ mean CVS and std for top-20 communities (by mean CVS)\n    - Count: how many of top-20 (by mean) match ground truth?\n\
  \    - Comparison: Louvain stability vs Leiden stability\n\n21. Test temporal robustness (optional, if time permits)\n \
  \   If network has year labels: recompute on subsets (2015-2019, 2020-2022)\n    Rank communities by CVS in each temporal\
  \ slice\n    Does ground truth still rank high in both slices?\n\n# STAGE 8: OUTPUT & REPORTING (30 min)\n# ======================================\n\
  22. Compile results_output dictionary\n    - real_network_metrics: {precision@K, recall@K, AUC-ROC, method comparison}\n\
  \    - synthetic_validation: {auc_vs_boost table, sensitivity curve data}\n    - stability_analysis: {louvain stability\
  \ across seeds, method robustness}\n    - detailed_community_table: all communities ranked by CVS with Jaccard overlap\n\
  \    - baseline_comparison: CVS vs Reciprocity vs CIDRE-lite metrics\n    - failure_modes: (if any) communities with high\
  \ CVS but no match to truth\n\n23. Save method_out.json\n    Structure:\n    {\n      \"metadata\": {\"method\": \"CVS via\
  \ Hodge decomposition\", \"network\": \"96-journal OpenAlex\"},\n      \"real_network_results\": {...},\n      \"synthetic_results\"\
  : {...},\n      \"baseline_comparison\": {...},\n      \"stability_analysis\": {...},\n      \"plots_data\": {\"auc_vs_boost\"\
  : [...], \"roc_curve\": [...]},\n      \"top_detections\": [{community_id, cvs_score, match_to_truth, members}, ...]\n \
  \   }\n\n24. Optional visualization (if time)\n    - Plot AUC-vs-boost curve with error bars\n    - Plot ROC curve (TPR\
  \ vs FPR) for CVS and baselines\n    - Print top-20 communities ranked by CVS, with match status to ground truth\n\n# SUCCESS\
  \ CRITERIA CHECK\n# ======================\n25. Validate against hypothesis claims\n    ✓ CVS achieves higher precision@20\
  \ than reciprocity ratio?\n    ✓ CVS achieves AUC-ROC matching or exceeding CIDRE-lite on real data?\n    ✓ At least 50%\
  \ of confirmed cartel groups rank in top decile (top 20/~200 communities)?\n    ✓ Synthetic validation: AUC improves monotonically\
  \ from 2× to 15× boost?\n    ✓ Method is parameter-free (no tuning required)?\n    \n    If ANY check fails: record failure\
  \ reason and suggest fallback modifications."
fallback_plan: |-
  FALLBACK PLAN: If primary approach encounters failures

  === FAILURE SCENARIO 1: Hodge decomposition numerically unstable ===
  Problem: scipy.sparse.linalg.lsqr fails to converge or produces NaNs
  Fallback A (Recommended):
    - Use pseudoinverse instead: f_grad = pinv(B1) @ flow_vector
    - Use scipy.sparse.linalg.svds to compute truncated SVD decomposition
    - Regularize: add small L2 penalty: minimize ||B1 @ x||^2 + λ||x||^2
    - Set λ = 1e-6 * max(B1^T B1 eigenvalues) to stabilize

  Fallback B (Simplified):
    - Skip explicit gradient extraction; compute CVS as pure curl approximation
    - Use pairwise reciprocity as curl proxy: f_residual ≈ (c_ij - c_ji)^2 / (c_ij + c_ji)^2
    - This reduces CVS to a variant of reciprocity ratio but is interpretable

  === FAILURE SCENARIO 2: Community detection produces trivial partitions ===
  Problem: Louvain/Leiden finds only 1-2 giant communities (poor resolution)
  Fallback A (Recommended):
    - Run community detection on undirected projection of graph: max(c_ij, c_ji)
    - Louvain has resolution parameter γ; sweep γ ∈ {0.5, 1.0, 1.5, 2.0}
    - For each γ, compute CVS, select partition with highest modularity

  Fallback B (Simplified):
    - Use fixed-size clustering: k-means on node centrality features
    - Features: in-degree, out-degree, mutual_citation_weight, assortativity
    - Sweep k ∈ {5, 10, 15, 20, 25} and compute CVS for each

  === FAILURE SCENARIO 3: Ground truth matching poor (Jaccard < 0.3 for all) ===
  Problem: Detected communities don't align with Clarivate cartels
  Fallback A (Recommended):
    - Relax Jaccard threshold to 0.3 (looser matching)
    - Alternatively: use Sorensen–Dice coefficient instead of Jaccard
    - Investigate: Do detected high-CVS communities contain ANY cartel members?
    - Report precision/recall using both thresholds (0.5 and 0.3)

  Fallback B (Simplified):
    - Score communities by member-level ground truth instead of group-level
    - For each community, count how many members are known cartel journals
    - Rank by cartel member count instead of CVS
    - Compare: does CVS still pick up cartel members better than reciprocity?

  === FAILURE SCENARIO 4: Synthetic validation shows no clear AUC trend ===
  Problem: AUC doesn't improve monotonically with boost level (noisy curve)
  Fallback A (Recommended):
    - Increase number of synthetic subsets from 8 to 20 per boost level
    - Average AUC across all 20 to reduce variance
    - Report: median AUC + interquartile range instead of mean ± std

  Fallback B (Simplified):
    - Focus on worst-case boost (2×) and best-case (15×) only
    - Report binary result: does CVS detect 2× better than baseline? Yes/No
    - Skip intermediate boost levels to save time

  === FAILURE SCENARIO 5: Code runs out of time (>6 hours) ===
  Problem: Full 3 community detection methods × 10 seeds takes too long
  Fallback (Simplified, Priority Order):
    1. Run Louvain only (fastest), 5 seeds (not 10)
    2. Skip Leiden and Infomap for full run; run quick 1-seed test only
    3. Run synthetic validation on boost levels {5×, 15×} only (skip 2×, 10×)
    4. Skip temporal robustness (optional anyway)
    5. Skip visualization, focus on tables
    Expected savings: 2-3 hours

  === FAILURE SCENARIO 6: Missing dependencies or import errors ===
  Fallback (Immediate):
    - Try: pip install python-louvain leiden networkx==3.2 numpy scipy pandas
    - If leiden fails: skip Leiden, use Louvain + Infomap (if available)
    - If Infomap unavailable: use Louvain only with multiple resolution parameters
    - Critical: ensure scipy version ≥ 1.7 (for lsqr stability)

  === FAILURE SCENARIO 7: Real network has no matching ground truth detections ===
  Problem: All 17 ground-truth cartels scattered across middle-ranked CVS communities
  Fallback (Interpretation):
    - This would DISCONFIRM the hypothesis (vortex model doesn't hold on real data)
    - Still report full results: the negative result is scientifically valuable
    - Analyze: do high-CVS communities have ANY structural property in common?
    - Compare to reciprocity ratio: does baseline perform better on real data?

  GENERAL STRATEGY:
  - Prioritize real network validation (MUST complete)
  - Synthetic validation is secondary (helps characterize detection threshold)
  - If time-constrained: complete real-data metrics, skip deep analysis of baselines
  - Save intermediate results to CSV after each major stage so partial runs are useful
testing_plan: |-
  TESTING PLAN: Validation strategy for the CVS experiment

  === STAGE 1: UNIT TESTS (15 min) ===
  Before running full experiment, validate core components

  1. Test Hodge decomposition on toy graphs
     a. Minimal test: 3-node graph with known gradient/curl
        - Linear chain: 1→2→3 (pure gradient, curl should be ~0)
        - Triangle: 1→2→3→1 (pure curl, gradient should be ~0)
        - Expected: |f_grad| >> |f_residual| for chain, vice versa for triangle
     b. Verify: lsqr converges and solution is reasonable
        - Check: no NaN, no Inf values
        - Check: f_grad + f_residual ≈ f_total (within numerical tolerance 1e-6)

  2. Test CVS score function
     a. Synthetic subgraph with high curl: CVS should approach 1.0
     b. Synthetic subgraph with low curl: CVS should approach 0.0
     c. Edge case: empty subgraph should return 0 (no crash)

  3. Test Jaccard matching
     a. Identical sets: Jaccard = 1.0
     b. Disjoint sets: Jaccard = 0.0
     c. Partial overlap: Jaccard = 0.5 (verify boundary case)

  === STAGE 2: INTEGRATION TESTS (10 min) ===
  Test on MINI dataset to verify pipeline works end-to-end

  4. Load mini network (if available)
     - Use mini_journal_citation_network.json (subset of 96 journals)
     - Expected: <96 nodes, <888 edges, faster to debug
     - Run full pipeline: decompose → detect communities → score → match ground truth
     - Check: no crashes, all outputs are valid JSON, shapes are consistent

  5. Verify ground truth loading
     - Parse cartel_ground_truth.json correctly
     - Identify cartel journals in mini network (if any)
     - Count: how many ground-truth cases exist in mini network?

  === STAGE 3: QUICK REAL-NETWORK TEST (20 min) ===
  Test on FULL network but reduced configuration to catch bugs early

  6. Quick Hodge decomposition on real network
     - Run hodge_decompose() on full 96-journal graph
     - Check: output shapes match (|edges| × 1 for f_grad, f_residual, f_total)
     - Check: sum of f_grad + f_residual ≈ f_total (numerically stable)
     - Inspect: histogram of f_grad vs f_residual values (should show both components)

  7. Quick community detection (single method, single seed)
     - Run Louvain with 1 seed only (fast)
     - Number of communities detected: should be 5-20 (too few/too many suggests issue)
     - Check: all nodes assigned to communities, no orphans
     - Sample: pick 3 random communities, compute CVS manually, verify function

  8. Quick ground truth matching
     - Rank detected communities by CVS
     - Top 5 communities: do ANY match ground truth (Jaccard ≥ 0.5)?
     - If 0 matches in top-5, check if issue is threshold or fundamental mismatch
     - Report: preliminary precision@5 (expect >0 to proceed confidently)

  === STAGE 4: SYNTHETIC VALIDATION TEST (10 min) ===
  Test synthetic cartel injection on tiny synthetic network

  9. Create tiny synthetic network (10 nodes, inject 3-node cartel)
     - Start from real network node features (in-degree, out-degree, etc.)
     - Boost within-cartel edges by 15×
     - Run CVS decomposition
     - Check: injected cartel has HIGH CVS (>0.5 expected)
     - Check: random communities have LOW CVS (<0.2 expected)

  === STAGE 5: BASELINE SANITY CHECKS (10 min) ===

  10. Reciprocity ratio baseline
      - Hand-verify on 2-3 journal pairs: citations_ij vs citations_ji
      - Compute ratio manually, compare to function output
      - Edge case: mutual citations = 0, function should return 0 (no crash)

  11. CIDRE-lite baseline
      - Compute by hand on a 4-journal subgraph
      - Compare function output
      - Check: score is between 0 and 1

  === STAGE 6: CONTINUOUS MONITORING DURING FULL RUN ===

  12. Log checkpoints after each major stage
      - STAGE 3 (Hodge): print min/max/mean of f_grad, f_residual
      - STAGE 4 (Communities): print number of communities, CVS distribution (percentiles)
      - STAGE 4 (Ground truth): print preliminary precision@5, @10, @20
      - STAGE 5 (Synthetic): print AUC at each boost level immediately after compute
      - STAGE 6 (Baselines): print comparison table as computed

  13. Intermediate save strategy
      - After Stage 3: save hodge_components to pickle (for debugging if later stages fail)
      - After Stage 4: save detected_communities to JSON (for inspection)
      - After Stage 5: save synthetic_results to JSON (don't lose synthetic data if crash)
      - After Stage 6: save all_baselines to CSV (human-readable for manual inspection)

  14. Failure detection triggers
      - If AUC < 0.5 on real data: flag as potential method failure, investigate
      - If precision@20 < 0.2: flag as poor real-world performance
      - If synthetic AUC doesn't monotonically increase: flag as noisy validation
      - If >30% of synthetic runs crash: stop, investigate root cause

  === SUCCESS CRITERIA FOR TESTING ===
  Proceed to full run only if:
      ✓ All unit tests pass (toy graphs decompose correctly)
      ✓ Integration test on mini network completes without error
      ✓ Real network Hodge decomposition is numerically stable (no NaN/Inf)
      ✓ Community detection finds 5-20 communities (reasonable count)
      ✓ Preliminary precision@5 ≥ 0.2 (at least some ground truth detected)
      ✓ Reciprocity and CIDRE-lite baselines compute without crash
      ✓ Synthetic cartel injection shows expected CVS elevation (>0.5 in cartels)

  If ANY criterion fails: DO NOT proceed to full multi-seed run. Debug, fix, re-test.

  === EXPECTED RUNTIME ESTIMATES ===
  - Unit tests: 5 min
  - Mini network integration: 5 min
  - Real network quick test: 10 min
  - Synthetic test: 5 min
  - Baseline tests: 5 min
  - **TOTAL TEST PHASE: ~30 min**
  - Full experiment run (with all seeds): ~5 hours 30 min
  - Total: 6 hours (as budgeted)
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_oKw95zbMmpyR
type: dataset
title: Journal Citation Network for Cartel Detection
summary: |-
  Dataset: journal_citation_network — a directed weighted journal-level citation network constructed from the OpenAlex REST API (free, no authentication required). The network covers publications from 2015–2022 across 96 high-impact journals (top 100 by global citation count, sourced via GET /sources sorted by cited_by_count:desc), with 888 directed edges representing cross-journal citation counts aggregated from 2,924 sampled papers. The closed-world construction algorithm is: (1) fetch top N journals; (2) for each journal fetch top-cited papers with referenced_works; (3) build paper→journal map; (4) count edges by looking up each referenced_work in the map — total API calls = N+1, no expensive resolution step.

  Each example corresponds to one journal node. The input field is a JSON string of per-journal network features: journal_name, issn_l, works_count, global_cited_by_count, in_degree, out_degree, in_citation_weight, out_citation_weight, mutual_citation_weight (sum of bidirectional citation counts — high values signal potential cartel behavior), citation_asymmetry (positive = net receiver / prestigious journal), mutual_citation_ratio (fraction of citations that are mutual), n_mutual_partners. The output field is 'normal' for the 96 top journals (none are on Clarivate's suppression list).

  The cartel ground truth is stored in temp/datasets/cartel_ground_truth.json: 17 verified cases from Clarivate JCR annual suppression lists (2013, 2018, 2024, 2025), including 12 citation-stacking cartels (e.g. the 2013 Brazilian cartel of 4 journals, 2025 MDPI/Wiley/Springer cases) and 5 self-citation cases. The research methodology is unsupervised anomaly detection — Hodge decomposition and Louvain community detection applied to the citation graph to find anomalous mutual-citation clusters, which are then validated against the ground truth suppression list. Graph statistics: 96 nodes, 888 edges, sparsity=0.097 (dense among top journals as expected), total citation count=2644.
workspace_path: >-
  /ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Web search (Serper), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-image-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
</skills>
</available_resources>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. Use it for framework choices, implementation patterns, agent orchestration.

- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-python, aii-long-running-tasks, aii-json, aii-file-size-limit, aii-use-hardware, aii-parallel-computing.
TODO 2. Read preview files from dependencies to understand data structure. Use ALL datasets provided — do not skip or select a subset. Read domain handbook if applicable (see <available_domain_handbooks>). Test basic functionality with 'uv run'.
TODO 3. Fully implement our method AND baseline (comparison) as described in artifact plan in './method.py'. Use exp_gen_sol_out.json schema in aii-json skill for output format validation. Include everything specified in the artifact plan, but you may also implement additional relevant methods or analysis beyond what's listed. Be very attentive to meticulously and exhaustively fix any errors in your code.
</todos>
```

### [2] HUMAN-USER prompt · 2026-07-09 01:54:47 UTC

```
Propose a simple, novel graph-based method for detecting citation cartels in academic networks and validate it.
```

### [3] SKILL-INPUT — aii-python · 2026-07-09 01:55:11 UTC

The agent loaded the **aii-python** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-python
description: Python coding standards for experiment and evaluation scripts. Covers environment setup, logging, error handling, and code structure.
---

## Environment Setup

- Python 3.12+
- **NEVER use `pip` or `.venv/bin/pip`** — they are not installed. Use `uv` for ALL package operations:
  ```bash
  uv venv .venv --python=3.12
  source .venv/bin/activate  # or: .venv/bin/python script.py
  uv pip install pandas loguru  # NOT: pip install
  ```
- Create `.toml` file with dependencies, create uv `.venv` and activate it
- NO inline dependencies (no `# /// script` headers)

## Logging

Use `loguru` for all logging. Add a file sink alongside stdout.

```python
from loguru import logger
import sys

logger.remove()  # Remove default handler
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")
```

Rules:
- Log every major step (data loading, processing start/end, results)
- If applicable, log every LLM API call input and output
- Truncate long outputs in logs (add truncation logic for potentially large strings)
- Use `logger.error()` in except blocks (traceback auto-captured)

## Error Handling

- Wrap major operations in try/except blocks
- Use `@logger.catch(reraise=True)` decorator on main functions — without `reraise=True`, the script exits 0 even on uncaught exceptions, hiding failures from downstream consumers
- Use explicit exception types, not bare `except:`
- Never silently swallow exceptions — always log them

```python
@logger.catch(reraise=True)
def main():
    try:
        data = load_data(path)
    except FileNotFoundError:
        logger.error("Data file not found")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON in data file")
        raise
```

## Code Structure

- Use `pathlib.Path` for file operations: `Path("data/input.json").read_text()` not `open(...).read()`
- Use type hints for function signatures
- Use keyword arguments for functions with more than 4 parameters
- No hardcoded paths — derive from script location or accept as arguments

## Script Pattern

Standard pattern for experiment/evaluation scripts:

```python
#!/usr/bin/env python3
"""Brief description of what this script does."""

from loguru import logger
from pathlib import Path
import json
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

@logger.catch(reraise=True)
def main():
    # Load data
    data_path = Path("full_data_out.json")
    logger.info(f"Loading data from {data_path}")
    data = json.loads(data_path.read_text())
    logger.info(f"Loaded {len(data['examples'])} examples")

    # Process
    results = []
    for i, example in enumerate(data["examples"]):
        try:
            result = process(example)
            results.append(result)
        except Exception:
            logger.error(f"Failed on example {i}")
            continue

    # Save output
    output = {"examples": results}
    Path("method_out.json").write_text(json.dumps(output, indent=2))
    logger.info(f"Saved {len(results)} results")

if __name__ == "__main__":
    main()
```
````

### [4] SKILL-INPUT — aii-long-running-tasks · 2026-07-09 01:55:15 UTC

The agent loaded the **aii-long-running-tasks** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-long-running-tasks
description: Gradual scaling pattern for long-running autonomous tasks. Use when running experiments, evaluations, or any code that processes data at increasing scale with runtime checks.
---

## Core Principles

1. **Time budget first**: Read your time/runtime constraints before running anything. Set every Bash timeout to fit within the budget.
2. **Start small, scale up**: Run on minimal input first, fix errors, then increase scale.
3. **Extrapolate before scaling**: Use recorded runtimes to predict whether the next step fits in the budget. Don't guess — calculate.
4. **Background execution**: For anything that takes >1 min, run in background (`run_in_background=true`) and do useful work while waiting.
5. **Stop early if needed**: Quality results on less data beats a timeout or crash. It's always acceptable to stop at a smaller scale.

---

## Gradual Scaling Sequence

Run code at increasing data sizes, checking runtime at each step.

Substitute your actual file names:
- `{mini_file}` — mini JSON (3 examples) from dependency workspace
- `{full_file}` — full dataset from dependency workspace
- `{script}` — your processing script (e.g., `./method.py`, `./eval.py`)
- `{schema}` — JSON schema to validate output against

**STEP 1 — MINI DATA:** Run `{script}` on `{mini_file}`. Do NOT truncate logs. Fix all errors. Validate output against `{schema}`. Verify you are NOT using mock scripts, mock data, or mock APIs.

**STEP 2 — 10 EXAMPLES:** Modify `{script}` to load only the first 10 examples from `{full_file}`. Run and fix errors. Validate schema. Record the runtime.

**STEP 3 — 50 EXAMPLES:** Load first 50 examples from `{full_file}`. Run and fix errors. Record runtime. **EXTRAPOLATE**: Using runtimes from steps 2-3, estimate time per example. Calculate how many examples fit in your remaining time budget. If 50 already used most of the budget, stop here.

**STEP 4 — 100 EXAMPLES (if budget allows):** Load first 100 examples. Run and fix errors. Record runtime. Re-extrapolate with the new data point.

**STEP 5 — 200 EXAMPLES (if budget allows):** Load first 200 examples from `{full_file}`. Run and fix errors. Record runtime.

**STEP 6 — MAXIMIZE:** Using all recorded runtimes, extrapolate time-per-example (it may not be perfectly linear — account for overhead). Calculate the maximum number of examples that fits within your remaining time budget with a 10% safety margin. Load that many (or all if they fit). Run and validate.

## Final Testing Phase

After completing the scaling sequence, redo the entire sequence **one more time** up to your final example count:

mini → 10 → 50 → 100 → 200 → max

At each scale: look for issues, fix problems, validate output, ensure it completes within time limits.

---

## Background Execution

For any step that takes >1 min, run as a **background task**:

1. Launch with Bash `run_in_background=true`
2. While it runs, use the time productively:
   - Sanity-check previous outputs
   - Verify file integrity (correct field names, non-empty values)
   - Review code for edge cases at larger scale
   - Prepare the next step
3. Check back on the background task to get results
4. If it failed, fix errors and re-run

---

## Resource Limits

Set hard RAM and CPU time limits so code fails fast instead of crashing the system. Read limits from `<hardware>` and leave headroom for the OS (e.g., if 16GB total, cap at 14GB).

Python example using stdlib `resource` module:
```python
import resource
resource.setrlimit(resource.RLIMIT_AS, (14 * 1024**3, 14 * 1024**3))  # 14GB RAM
resource.setrlimit(resource.RLIMIT_CPU, (3600, 3600))  # 1 hour CPU time
```
Exceeding RAM raises `MemoryError`. Exceeding CPU time sends `SIGKILL`.

## Monitoring

At each step, record runtime AND check resource usage (`free -h` for RAM, `top -bn1 | head -5` for CPU). If memory usage is climbing toward the limit or CPU is pegged, stop and investigate before scaling further.
````

### [5] SKILL-INPUT — aii-json · 2026-07-09 01:55:21 UTC

The agent loaded the **aii-json** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-json
description: JSON validation and formatting toolkit. Validate JSON files against schemas for experiment pipelines, and generate full/mini/preview versions of JSON datasets. Use for validating pipeline outputs, checking schema compliance, or creating size-optimized JSON variants.
---

## Contents

- Validating JSON (schema validation against experiment schemas)
- Formatting JSON (generate full/mini/preview versions)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Validating JSON

Validate JSON files against predefined schemas for experiment-based hypothesis selection, data collection, solution generation, and evaluation.

### Quick Start

1. Read the schema spec you need to adhere to (e.g., `schemas/exp_eval_sol_out.json`)
2. Create your output file following that schema structure
3. Validate:

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /path/to/eval_out.json
```

### Script: aii_json_validate_schema.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /tmp/eval_out.json
```

**Parallel execution (multiple validations):**

IMPORTANT: When validating multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_validate_schema.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --format {1} --file {2}' ::: 'exp_sel_data_out' 'exp_gen_sol_out' 'exp_eval_sol_out' :::+ '/tmp/full_data_out.json' '/tmp/method_out.json' '/tmp/eval_out.json'
```

**Example output (success):**
```
Validating: aii_json_validate_schema.py
Format: exp_eval_sol_out

✓ Validation PASSED
```

**Example output (failure):**
```
Validating: aii_json_validate_schema.py
Format: exp_sel_data_out

✗ Validation FAILED

Errors:
  Path: datasets → 0 → examples → 0
  Error: 'output' is a required property
  Validator: required
```

**Parameters:**

`--format` (required)
- Format type to validate against
- Determines which schema to use

`--file` (required)
- Path to JSON file to validate
- Must be valid JSON
- **Always pass an absolute path.** Relative paths resolve from the
  ability server's CWD (typically ``/ai-inventor/aii_server``), not from
  your agent workspace, so ``data_out/x.json`` will silently look in the
  wrong directory and fail with "Could not load JSON file". The validate
  endpoint also accepts a ``workspace_dir`` arg if you need to keep a
  relative path — pass your workspace path there.

**Tips:**
- Fix errors in your JSON and rerun validation until it passes

### Schema Files

Schemas are stored in `.claude/skills/aii-json/schemas/`:

**Hypothesis Selection & Evaluation:**
- `sel_hypo_out.json` - Hypothesis Selection output (all hypotheses with selected flags)
- `feasibility_eval_all.json` - All hypotheses with feasibility scores
- `feasibility_eval_top.json` - Top 5 most feasible hypotheses
- `novelty_research_one.json` - Single hypothesis novelty research arguments with citations
- `novelty_eval_all.json` - All hypotheses with novelty scores
- `novelty_eval_top.json` - Single best selected hypothesis

**Experiment Pipeline:**
- `exp_sel_data_out.json` - Experiment Data Selection format
- `exp_gen_sol_out.json` - Experiment Solution Generation format
- `exp_eval_sol_out.json` - Experiment Solution Evaluation format

---

## Formatting JSON

Generate three size-optimized versions of a JSON file for efficient development and preview:
- **full**: Identical to original (all data)
- **mini**: First 3 items only (for quick testing)
- **preview**: Mini + all strings truncated to 200 chars (for quick inspection)

### Quick Start

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

### Script: aii_json_format_mini_preview.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

**Parallel execution (multiple files):**

IMPORTANT: When formatting multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_format_mini_preview.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --input {}' ::: 'full_data_out.json' 'method_out.json' 'eval_out.json'
```

**Example output:**
```
Generated 3 versions:
  Full (50 items): /path/to/full_method_out.json
  Mini (3 items): /path/to/mini_method_out.json
  Preview (3 items, truncated): /path/to/preview_method_out.json
```

**Parameters:**

`--input` (required)
- Path to input JSON file
- Must have a top-level array
- Example: `method_out.json`, `full_data_out.json`

`--output-dir` (optional)
- Output directory for generated files
- Default: same directory as input file
- Files are prefixed with `full_`, `mini_`, `preview_`

**Output Files:**

All three files use the same base name with different prefixes:
- `full_{basename}.json` - Complete dataset (identical to original)
- `mini_{basename}.json` - First 3 array items only
- `preview_{basename}.json` - First 3 items with strings truncated to 200 chars

**Tips:**
- Input JSON must have a top-level array structure
- String truncation is recursive (applies to nested objects and arrays)
- Use preview files for quick inspection without reading large datasets
- Use mini files for developing/testing code before running on full dataset

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [6] SKILL-INPUT — aii-use-hardware · 2026-07-09 01:55:21 UTC

The agent loaded the **aii-use-hardware** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-use-hardware
description: Detect hardware and use it responsibly. Covers CPU/RAM/GPU detection, memory-safe data processing, and resource-aware computation.
---

**Step 1** — Run `bash scripts/get_hardware.sh` (relative to this skill's directory).

Read the `=== CGROUP ===` section carefully. If `Type: cgroup v1` or `cgroup v2`:
- You are in a **container with hard resource limits**. Exceeding them = OOM kill, no recovery.
- **Never** use `psutil.virtual_memory().total`, `free -h`, `/proc/meminfo`, `os.cpu_count()`, or `nproc` for resource limits — these report **host** values, not your container's allocation.
- **Always** read limits from the cgroup paths shown in the output, or use the Python helpers below.
- For **runtime memory monitoring**, read current usage from cgroup too:
  - v2: `/sys/fs/cgroup/memory.current`
  - v1: `/sys/fs/cgroup/memory/memory.usage_in_bytes`

**Step 2** — Use Step 1 results to pick package variants **before** installing.

Defaults often target the most powerful environment — PyPI's `torch` ships with CUDA libs even on CPU-only hosts. Wrong variant = wasted disk, slow setup, possible import-time failures.

If `=== GPU ===` shows `No GPU`, install torch's CPU build (skips ~4.5GB of CUDA libs):
```bash
uv pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
```
Same idea for any library whose wheel selection depends on detected hardware (GPU/CPU-only builds, architecture-specific wheels).

After install, sanity-check imports right away (`python -c "import torch"`). Disk-pressure or interrupted installs leave half-built wheels (e.g. `libtorch_global_deps.so` missing) — catch these before the experiment runs.

**Step 3** — Set Python constants from the Step 1 results:
```python
import os, math, torch, psutil
from pathlib import Path

def _detect_cpus() -> int:
    """Detect actual CPU allocation (containers/pods/bare metal)."""
    try:  # cgroups v2 quota
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError): pass
    try:  # cgroups v1 quota
        q = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us").read_text())
        p = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").read_text())
        if q > 0:
            return math.ceil(q / p)
    except (FileNotFoundError, ValueError): pass
    try:  # CPU affinity (cpuset — used by RunPod, Docker --cpuset-cpus)
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError): pass
    return os.cpu_count() or 1

def _container_ram_gb() -> float | None:
    """Read RAM limit from cgroup (containers/pods)."""
    for p in ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]:
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except (FileNotFoundError, ValueError): pass
    return None

NUM_CPUS = _detect_cpus()
HAS_GPU = torch.cuda.is_available()
VRAM_GB = torch.cuda.get_device_properties(0).total_mem / 1e9 if HAS_GPU else 0
DEVICE = torch.device("cuda" if HAS_GPU else "cpu")
TOTAL_RAM_GB = _container_ram_gb() or psutil.virtual_memory().total / 1e9
AVAILABLE_RAM_GB = min(psutil.virtual_memory().available / 1e9, TOTAL_RAM_GB)
```

## Step 4 — Set Memory Limits

OOM kills the entire container. **Every script MUST set RAM and VRAM limits at startup.**

Decide the budget based on what the script actually needs. Estimate data size × 2-5x for in-memory overhead, then add ~50% breathing room for temporaries. You may use up to 90% of available RAM/VRAM, but **scale gradually** — start small (e.g. 30-50%), verify it works, then increase toward the limit. Never exceed 90% to keep a buffer for the OS, system processes, and the agent runtime itself. Going over crashes the container/machine with no recovery.

```python
import resource, psutil

_avail = psutil.virtual_memory().available
RAM_BUDGET = ???  # YOU decide: estimate what this script needs (in bytes)
assert RAM_BUDGET < _avail, f"Budget {RAM_BUDGET/1e9:.1f}GB > available {_avail/1e9:.1f}GB"
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))  # 3x: virtual > RSS; raises MemoryError on exceed

if HAS_GPU:
    _free, _total = torch.cuda.mem_get_info(0)
    VRAM_BUDGET = ???  # YOU decide: estimate GPU memory needs
    torch.cuda.set_per_process_memory_fraction(min(VRAM_BUDGET / _total, 0.95))  # raises OutOfMemoryError on exceed
```

## Memory-Safe Data Processing

- **One at a time**: load one large object → process → `del obj; gc.collect()` → next
- **Load only what you need**: select specific tables/columns/rows, not entire databases
- **Test small first**: run on a sample before scaling to full data to estimate memory/time
- **Free intermediates in loops**: don't accumulate large results — aggregate incrementally
- **Size before loading**: check file/dataset size before loading; if it's >30% of `RAM_BUDGET`, chunk it

## Common Mistakes (from real crashes)

- **Skipping this skill entirely** — loading data with no RAM detection, no limits, no budget. Container OOM-killed, all agents lost.
- **Using `psutil.virtual_memory().total` instead of `_container_ram_gb()`** — reports host RAM (e.g. 66 GB) when container limit is 28 GB. You MUST use the cgroup-aware functions above.
- **Loading all tables from a multi-table database at once** — one agent loaded 14 RelBench tables simultaneously, spiked past container limit.
- **Setting no memory limits** — without `resource.setrlimit` (RAM) and `set_per_process_memory_fraction` (VRAM), a runaway script OOM-kills the container instead of raising a catchable error.
- **Using `os.cpu_count()` directly** — returns host CPUs (e.g. 192) instead of container limit (e.g. 4) on RunPod/Docker. Always use `_detect_cpus()` above which checks cgroup quota → CPU affinity → `os.cpu_count()` in order.

## Hardware Use

- Keep these results in mind for ALL subsequent tasks — don't assume more than detected
- GPU if available and parallelizable, multiprocessing if multiple CPUs
- Push available resources to their full potential — don't leave hardware idle
````

### [7] SKILL-INPUT — aii-parallel-computing · 2026-07-09 01:55:25 UTC

The agent loaded the **aii-parallel-computing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-parallel-computing
description: "CRITICAL PERFORMANCE SKILL. Maximize hardware utilization for compute-intensive tasks. Covers GPU acceleration, CPU parallelism, and async I/O. The difference between hours of failure and minutes of success. Use whenever writing ANY script that processes data, makes API calls, or does computation."
---

**ALWAYS parallelize. Sequential processing is unacceptable for any non-trivial workload.** A sequential script doing 1000 API calls takes hours and fails halfway. An async version finishes in minutes with proper error handling. ALWAYS ask: "Can this run in parallel?" — the answer is almost always yes.

Read aii-use-hardware skill first → get `NUM_CPUS`, `HAS_GPU`, `VRAM_GB`, `device`. Set `NUM_WORKERS` proportional to available CPU capacity — check `psutil.cpu_percent(interval=1)` and scale accordingly (e.g. 30% used → use ~70% of cores).

## Decision Tree (follow strictly)

- **I/O-bound** (API calls, downloads, web, file reads) → `asyncio` + `aiohttp` with `Semaphore(NUM_WORKERS * 4)`. NEVER do sequential HTTP requests in a loop.
- **CPU-bound, vectorizable** → GPU available: PyTorch on device / No GPU: NumPy vectorized ops. NEVER loop over array elements in Python.
- **CPU-bound, independent items** → `ProcessPoolExecutor(max_workers=NUM_WORKERS)`. NEVER process items one-by-one when they're independent.
- **Sequential** → only acceptable when items have data dependencies (each depends on the previous result).

## GPU Rules

- Use up to 90% of available VRAM — scale gradually (start small, increase after each successful run, keep 10% buffer)
- Move to device → compute → move back: `torch.tensor(data, device=device)` → `.cpu().numpy()`
- OOM fallback: catch `torch.cuda.OutOfMemoryError` → `empty_cache()` → halve batch size → retry on GPU. Keep reducing until it fits. Stay on GPU.
- Batch large data: chunk it, `del batch` between iterations to free VRAM

## Parallelism Rules

- **CPU-bound**: `ProcessPoolExecutor` + `as_completed`, pre-allocate result list indexed by submission order
- **I/O-bound**: `asyncio` + `aiohttp`, `Semaphore(NUM_WORKERS * 4)`, single shared `ClientSession`, `asyncio.gather(*tasks, return_exceptions=True)`
- Always add `tenacity` retries for transient failures, always set timeouts on HTTP requests
- **CRITICAL — `ProcessPoolExecutor` start method**: Default `fork` deadlocks with loguru (and any threading library). ALWAYS pass `mp_context=multiprocessing.get_context("spawn")` when constructing `ProcessPoolExecutor` in any script that uses loguru, threading, or async I/O. Example:
  ```python
  import multiprocessing as mp
  from concurrent.futures import ProcessPoolExecutor
  with ProcessPoolExecutor(max_workers=N, mp_context=mp.get_context("spawn")) as pool:
      ...
  ```
````

### [8] SYSTEM-USER prompt · 2026-07-09 02:09:15 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_2/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/`:
GOOD: `/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/file.py`, `/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_experiment_1_idx2
type: experiment
title: CVS cartel detection on real networks
summary: >-
  Validate Citation Vortex Score (CVS) using Hodge decomposition on real 96-journal OpenAlex network against Clarivate ground
  truth, test robustness across community detection methods and synthetic boost levels.
runpod_compute_profile: cpu_light
implementation_pseudocode: "# Citation Vortex Score (CVS) Experiment: Real-world Validation\n# ============================================================\n\
  # Duration: 6h total (code, debug, test, full run)\n# Executor: Load network, run CVS method, compute metrics, compare baselines\n\
  \n# STAGE 1: SETUP & DATA LOADING (15 min)\n# ======================================\n1. Load dependencies\n   - import\
  \ networkx, numpy, scipy.sparse, scipy.sparse.linalg, pandas, json\n   - pip install python-louvain leiden (community detection)\n\
  \   - pip install networkx==3.2+\n\n2. Load real journal citation network from dependency artifact\n   - Input: /path/to/full_data_out.json\
  \ or full_journal_citation_network.json\n   - Parse JSON: extract nodes (journals) and weighted edges (citation counts)\n\
  \   - Build NetworkX DiGraph: nx.DiGraph() with edge weights w(i→j) = c_ij\n   - Verify: 96 nodes, 888 edges, total citations\
  \ = 2644\n\n3. Load ground truth cartel labels from cartel_ground_truth.json\n   - Parse: list of 17 cartel journal groups\
  \ (ISSNs, journal_names, suppression_years)\n   - Create ground_truth_set: set of (issn_i, issn_j) pairs for each cartel\n\
  \   - Group by cluster: record which journals belong to same cartel (for Jaccard matching)\n\n4. Create data structures\n\
  \   - node_id_map: issn → integer (for matrix indexing)\n   - node_labels: integer → issn (reverse mapping)\n   - adjacency\
  \ list: node → neighbors + edge weights\n\n# STAGE 2: HODGE DECOMPOSITION IMPLEMENTATION (60 min)\n# =====================================================\n\
  5. Implement Hodge decomposition on directed weighted graph\n   Algorithm:\n   a. Build incidence matrix B1 (|V| × |E|)\n\
  \      - Column j represents edge (u, v)\n      - Row u: +1 if u is head, -1 if u is tail, 0 otherwise\n      - Sparse format:\
  \ scipy.sparse.csr_matrix\n   \n   b. Symmetrize directed graph for decomposition\n      - For each directed edge (i→j)\
  \ with weight w_ij:\n        - Symmetric part: s_ij = (w_ij + w_ji) / 2\n        - Skew part: a_ij = (w_ij - w_ji) / 2\n\
  \      - Use skew-symmetric part for curl detection\n   \n   c. Solve least-squares to extract gradient component\n    \
  \  - Objective: minimize ||B1 @ x||^2 where x is node potential\n      - Use: scipy.sparse.linalg.lsqr(B1, flow_vector,\
  \ atol=1e-6)\n      - Solution: x* = node potentials\n      - Gradient flow f_grad[i→j] = x[j] - x[i]\n   \n   d. Compute\
  \ residual (curl + harmonic) component\n      - f_curl_residual[i→j] = f[i→j] - f_grad[i→j]\n      - Store as edge weights\
  \ in sparse format\n\n6. Helper function: hodge_decompose(digraph, flow_weights=None)\n   Input: NetworkX DiGraph, optional\
  \ custom flow weights\n   Output: {'f_grad': dict, 'f_residual': dict, 'f_total': dict}\n   - Default flow_weights: graph\
  \ edge weights (citation counts)\n   - Normalize flows to [0,1] range for comparability across subgraphs\n\n# STAGE 3: CVS\
  \ SCORING & COMMUNITY DETECTION (90 min)\n# ====================================================\n7. Implement CVS score\
  \ calculation\n   def compute_cvs(subgraph, hodge_components):\n       \"\"\"CVS(S) = sum||f_residual(e)||^2 / sum||f(e)||^2\
  \ for edges in S\"\"\"\n       residual_energy = sum(hodge_components['f_residual'][e]**2 for e in subgraph.edges())\n \
  \      total_energy = sum(hodge_components['f_total'][e]**2 for e in subgraph.edges())\n       if total_energy == 0:\n \
  \          return 0.0\n       return residual_energy / total_energy\n\n8. Run community detection (3 methods)\n   a. Louvain\
  \ (python-louvain library)\n      - Run with 10 random seeds\n      - Extract communities as subgraphs\n      - Record CVS\
  \ for each community per seed\n      - Compute mean, std, min, max CVS across seeds\n   \n   b. Leiden algorithm (leiden\
  \ library, more stable)\n      - Run with same 10 random seeds\n      - Extract communities\n      - Compute CVS, mean/std\
  \ across seeds\n   \n   c. Infomap (optional, if available; fallback to Louvain repeated)\n      - Single run (deterministic\
  \ or fixed seed)\n      - Compute CVS per community\n\n9. Rank all detected communities by CVS (descending)\n   - Global\
  \ ranking: merge communities from all 3 methods, rank by CVS\n   - Record: community_id, method, seed, cvs_score, member_journals,\
  \ size\n\n# STAGE 4: GROUND TRUTH MATCHING (45 min)\n# ========================================\n10. Implement Jaccard matching\
  \ to ground truth\n    def jaccard_overlap(detected_set, truth_set):\n        \"\"\"Jaccard = |intersection| / |union|\"\
  \"\"\n        return len(intersection) / len(union)\n    \n    Matching rule: detected community matches ground-truth cartel\
  \ if Jaccard ≥ 0.5\n\n11. Compute real-data metrics\n    a. Precision@K: Among top-K CVS-ranked communities, what fraction\
  \ match ground truth?\n       - Compute for K ∈ {5, 10, 20}\n       - Per-method breakdown\n    \n    b. Recall@K: Of 17\
  \ ground-truth cartels, how many are found in top-K?\n       - Compute for K ∈ {5, 10, 20, 50}\n    \n    c. AUC-ROC (binary\
  \ classification)\n       - For each detected community: binary label (matches truth OR not)\n       - Rank by CVS descending\n\
  \       - Plot ROC curve, compute AUC\n\n12. Generate results table (real network)\n    Columns: method | seed | community_size\
  \ | cvs_score | jaccard_overlap | matches_truth | member_journals\n    Rows: one per detected community (sorted by CVS)\n\
  \n# STAGE 5: SYNTHETIC VALIDATION (120 min)\n# ========================================\n13. Generate synthetic networks\
  \ with injected cartels\n    For each boost level b ∈ {2, 5, 10, 15}:\n        a. Copy real network\n        b. Select random\
  \ 8-journal subsets (8 random subsets per boost level)\n        c. For each subset, multiply within-subset edge weights\
  \ by factor b\n           - w_ij *= b if both i, j in subset\n        d. Save synthetic network state\n\n14. Run CVS on\
  \ each synthetic network\n    - Apply Hodge decomposition to synthetic network (new gradient/residual)\n    - Run community\
  \ detection (Louvain only for speed, 5 seeds)\n    - Rank communities by CVS\n\n15. Compute AUC-ROC for synthetic cartels\n\
  \    For each boost level:\n        - Create binary labels: 1 if community overlaps injected cartel (Jaccard ≥ 0.5), 0 else\n\
  \        - Rank by CVS descending\n        - Compute AUC\n        - Record: boost_level | num_subsets | auc_mean | auc_std\
  \ | auc_min | auc_max\n\n16. Generate AUC-vs-boost sensitivity curve\n    Plot: x-axis = boost level {2,5,10,15}, y-axis\
  \ = AUC\n    Show: mean AUC with error bars (std across 8 subsets per boost)\n    Reference: Hypothesis claimed AUC=1.0\
  \ at 15× boost\n\n# STAGE 6: BASELINE COMPARISONS (75 min)\n# =======================================\n17. Implement reciprocity\
  \ ratio baseline\n    def reciprocity_ratio(i, j):\n        \"\"\"For edge pair i↔j, ratio of mutual to total citations\"\
  \"\"\n        citations_ij = graph[i][j]['weight']\n        citations_ji = graph[j][i]['weight'] if graph.has_edge(j, i)\
  \ else 0\n        if citations_ij + citations_ji == 0:\n            return 0\n        return min(citations_ij, citations_ji)\
  \ / max(citations_ij, citations_ji)\n    \n    Score subgroups: mean reciprocity_ratio over all edges in subgroup\n    Rank\
  \ communities by reciprocity score descending\n\n18. Implement CIDRE-lite baseline\n    def cidre_lite(subgroup):\n    \
  \    \"\"\"Fraction of edges within subgroup (excess over expected)\"\"\"\n        within_edges = sum(1 for u,v in subgroup.edges()\
  \ if u,v in subgroup)\n        total_possible = len(subgroup) * (len(subgroup) - 1)\n        return within_edges / total_possible\
  \ if total_possible > 0 else 0\n    \n    **CRITICAL**: Original CIDRE uses dcSBM null model. CIDRE-lite skips this.\n \
  \   Note: Hypothesis reports CIDRE-lite AUC=0.0 before sign correction.\n    Compute both forward and sign-inverted AUC;\
  \ report both to clarify anti-correlation.\n\n19. Compare metrics: CVS vs Reciprocity vs CIDRE-lite\n    For real network:\n\
  \        - Compute all 3 baseline scores for each community\n        - Rank by each score\n        - Compute precision@5,\
  \ @10, @20 for each baseline\n        - Compute AUC-ROC for each baseline\n        - Table: baseline | precision@5 | precision@10\
  \ | precision@20 | AUC\n    \n    For synthetic networks (boost level 15× only):\n        - Compute AUC for CVS, reciprocity,\
  \ CIDRE-lite on all 8 synthetic networks\n        - Table: method | auc_mean | auc_std | auc_range\n\n# STAGE 7: STABILITY\
  \ & ROBUSTNESS (60 min)\n# =========================================\n20. Test robustness across Louvain random seeds\n\
  \    Already recorded in STAGE 3: 10 seeds per run\n    Analyze: Do top communities remain stable across seeds?\n    - Compute\
  \ mean CVS and std for top-20 communities (by mean CVS)\n    - Count: how many of top-20 (by mean) match ground truth?\n\
  \    - Comparison: Louvain stability vs Leiden stability\n\n21. Test temporal robustness (optional, if time permits)\n \
  \   If network has year labels: recompute on subsets (2015-2019, 2020-2022)\n    Rank communities by CVS in each temporal\
  \ slice\n    Does ground truth still rank high in both slices?\n\n# STAGE 8: OUTPUT & REPORTING (30 min)\n# ======================================\n\
  22. Compile results_output dictionary\n    - real_network_metrics: {precision@K, recall@K, AUC-ROC, method comparison}\n\
  \    - synthetic_validation: {auc_vs_boost table, sensitivity curve data}\n    - stability_analysis: {louvain stability\
  \ across seeds, method robustness}\n    - detailed_community_table: all communities ranked by CVS with Jaccard overlap\n\
  \    - baseline_comparison: CVS vs Reciprocity vs CIDRE-lite metrics\n    - failure_modes: (if any) communities with high\
  \ CVS but no match to truth\n\n23. Save method_out.json\n    Structure:\n    {\n      \"metadata\": {\"method\": \"CVS via\
  \ Hodge decomposition\", \"network\": \"96-journal OpenAlex\"},\n      \"real_network_results\": {...},\n      \"synthetic_results\"\
  : {...},\n      \"baseline_comparison\": {...},\n      \"stability_analysis\": {...},\n      \"plots_data\": {\"auc_vs_boost\"\
  : [...], \"roc_curve\": [...]},\n      \"top_detections\": [{community_id, cvs_score, match_to_truth, members}, ...]\n \
  \   }\n\n24. Optional visualization (if time)\n    - Plot AUC-vs-boost curve with error bars\n    - Plot ROC curve (TPR\
  \ vs FPR) for CVS and baselines\n    - Print top-20 communities ranked by CVS, with match status to ground truth\n\n# SUCCESS\
  \ CRITERIA CHECK\n# ======================\n25. Validate against hypothesis claims\n    ✓ CVS achieves higher precision@20\
  \ than reciprocity ratio?\n    ✓ CVS achieves AUC-ROC matching or exceeding CIDRE-lite on real data?\n    ✓ At least 50%\
  \ of confirmed cartel groups rank in top decile (top 20/~200 communities)?\n    ✓ Synthetic validation: AUC improves monotonically\
  \ from 2× to 15× boost?\n    ✓ Method is parameter-free (no tuning required)?\n    \n    If ANY check fails: record failure\
  \ reason and suggest fallback modifications."
fallback_plan: |-
  FALLBACK PLAN: If primary approach encounters failures

  === FAILURE SCENARIO 1: Hodge decomposition numerically unstable ===
  Problem: scipy.sparse.linalg.lsqr fails to converge or produces NaNs
  Fallback A (Recommended):
    - Use pseudoinverse instead: f_grad = pinv(B1) @ flow_vector
    - Use scipy.sparse.linalg.svds to compute truncated SVD decomposition
    - Regularize: add small L2 penalty: minimize ||B1 @ x||^2 + λ||x||^2
    - Set λ = 1e-6 * max(B1^T B1 eigenvalues) to stabilize

  Fallback B (Simplified):
    - Skip explicit gradient extraction; compute CVS as pure curl approximation
    - Use pairwise reciprocity as curl proxy: f_residual ≈ (c_ij - c_ji)^2 / (c_ij + c_ji)^2
    - This reduces CVS to a variant of reciprocity ratio but is interpretable

  === FAILURE SCENARIO 2: Community detection produces trivial partitions ===
  Problem: Louvain/Leiden finds only 1-2 giant communities (poor resolution)
  Fallback A (Recommended):
    - Run community detection on undirected projection of graph: max(c_ij, c_ji)
    - Louvain has resolution parameter γ; sweep γ ∈ {0.5, 1.0, 1.5, 2.0}
    - For each γ, compute CVS, select partition with highest modularity

  Fallback B (Simplified):
    - Use fixed-size clustering: k-means on node centrality features
    - Features: in-degree, out-degree, mutual_citation_weight, assortativity
    - Sweep k ∈ {5, 10, 15, 20, 25} and compute CVS for each

  === FAILURE SCENARIO 3: Ground truth matching poor (Jaccard < 0.3 for all) ===
  Problem: Detected communities don't align with Clarivate cartels
  Fallback A (Recommended):
    - Relax Jaccard threshold to 0.3 (looser matching)
    - Alternatively: use Sorensen–Dice coefficient instead of Jaccard
    - Investigate: Do detected high-CVS communities contain ANY cartel members?
    - Report precision/recall using both thresholds (0.5 and 0.3)

  Fallback B (Simplified):
    - Score communities by member-level ground truth instead of group-level
    - For each community, count how many members are known cartel journals
    - Rank by cartel member count instead of CVS
    - Compare: does CVS still pick up cartel members better than reciprocity?

  === FAILURE SCENARIO 4: Synthetic validation shows no clear AUC trend ===
  Problem: AUC doesn't improve monotonically with boost level (noisy curve)
  Fallback A (Recommended):
    - Increase number of synthetic subsets from 8 to 20 per boost level
    - Average AUC across all 20 to reduce variance
    - Report: median AUC + interquartile range instead of mean ± std

  Fallback B (Simplified):
    - Focus on worst-case boost (2×) and best-case (15×) only
    - Report binary result: does CVS detect 2× better than baseline? Yes/No
    - Skip intermediate boost levels to save time

  === FAILURE SCENARIO 5: Code runs out of time (>6 hours) ===
  Problem: Full 3 community detection methods × 10 seeds takes too long
  Fallback (Simplified, Priority Order):
    1. Run Louvain only (fastest), 5 seeds (not 10)
    2. Skip Leiden and Infomap for full run; run quick 1-seed test only
    3. Run synthetic validation on boost levels {5×, 15×} only (skip 2×, 10×)
    4. Skip temporal robustness (optional anyway)
    5. Skip visualization, focus on tables
    Expected savings: 2-3 hours

  === FAILURE SCENARIO 6: Missing dependencies or import errors ===
  Fallback (Immediate):
    - Try: pip install python-louvain leiden networkx==3.2 numpy scipy pandas
    - If leiden fails: skip Leiden, use Louvain + Infomap (if available)
    - If Infomap unavailable: use Louvain only with multiple resolution parameters
    - Critical: ensure scipy version ≥ 1.7 (for lsqr stability)

  === FAILURE SCENARIO 7: Real network has no matching ground truth detections ===
  Problem: All 17 ground-truth cartels scattered across middle-ranked CVS communities
  Fallback (Interpretation):
    - This would DISCONFIRM the hypothesis (vortex model doesn't hold on real data)
    - Still report full results: the negative result is scientifically valuable
    - Analyze: do high-CVS communities have ANY structural property in common?
    - Compare to reciprocity ratio: does baseline perform better on real data?

  GENERAL STRATEGY:
  - Prioritize real network validation (MUST complete)
  - Synthetic validation is secondary (helps characterize detection threshold)
  - If time-constrained: complete real-data metrics, skip deep analysis of baselines
  - Save intermediate results to CSV after each major stage so partial runs are useful
testing_plan: |-
  TESTING PLAN: Validation strategy for the CVS experiment

  === STAGE 1: UNIT TESTS (15 min) ===
  Before running full experiment, validate core components

  1. Test Hodge decomposition on toy graphs
     a. Minimal test: 3-node graph with known gradient/curl
        - Linear chain: 1→2→3 (pure gradient, curl should be ~0)
        - Triangle: 1→2→3→1 (pure curl, gradient should be ~0)
        - Expected: |f_grad| >> |f_residual| for chain, vice versa for triangle
     b. Verify: lsqr converges and solution is reasonable
        - Check: no NaN, no Inf values
        - Check: f_grad + f_residual ≈ f_total (within numerical tolerance 1e-6)

  2. Test CVS score function
     a. Synthetic subgraph with high curl: CVS should approach 1.0
     b. Synthetic subgraph with low curl: CVS should approach 0.0
     c. Edge case: empty subgraph should return 0 (no crash)

  3. Test Jaccard matching
     a. Identical sets: Jaccard = 1.0
     b. Disjoint sets: Jaccard = 0.0
     c. Partial overlap: Jaccard = 0.5 (verify boundary case)

  === STAGE 2: INTEGRATION TESTS (10 min) ===
  Test on MINI dataset to verify pipeline works end-to-end

  4. Load mini network (if available)
     - Use mini_journal_citation_network.json (subset of 96 journals)
     - Expected: <96 nodes, <888 edges, faster to debug
     - Run full pipeline: decompose → detect communities → score → match ground truth
     - Check: no crashes, all outputs are valid JSON, shapes are consistent

  5. Verify ground truth loading
     - Parse cartel_ground_truth.json correctly
     - Identify cartel journals in mini network (if any)
     - Count: how many ground-truth cases exist in mini network?

  === STAGE 3: QUICK REAL-NETWORK TEST (20 min) ===
  Test on FULL network but reduced configuration to catch bugs early

  6. Quick Hodge decomposition on real network
     - Run hodge_decompose() on full 96-journal graph
     - Check: output shapes match (|edges| × 1 for f_grad, f_residual, f_total)
     - Check: sum of f_grad + f_residual ≈ f_total (numerically stable)
     - Inspect: histogram of f_grad vs f_residual values (should show both components)

  7. Quick community detection (single method, single seed)
     - Run Louvain with 1 seed only (fast)
     - Number of communities detected: should be 5-20 (too few/too many suggests issue)
     - Check: all nodes assigned to communities, no orphans
     - Sample: pick 3 random communities, compute CVS manually, verify function

  8. Quick ground truth matching
     - Rank detected communities by CVS
     - Top 5 communities: do ANY match ground truth (Jaccard ≥ 0.5)?
     - If 0 matches in top-5, check if issue is threshold or fundamental mismatch
     - Report: preliminary precision@5 (expect >0 to proceed confidently)

  === STAGE 4: SYNTHETIC VALIDATION TEST (10 min) ===
  Test synthetic cartel injection on tiny synthetic network

  9. Create tiny synthetic network (10 nodes, inject 3-node cartel)
     - Start from real network node features (in-degree, out-degree, etc.)
     - Boost within-cartel edges by 15×
     - Run CVS decomposition
     - Check: injected cartel has HIGH CVS (>0.5 expected)
     - Check: random communities have LOW CVS (<0.2 expected)

  === STAGE 5: BASELINE SANITY CHECKS (10 min) ===

  10. Reciprocity ratio baseline
      - Hand-verify on 2-3 journal pairs: citations_ij vs citations_ji
      - Compute ratio manually, compare to function output
      - Edge case: mutual citations = 0, function should return 0 (no crash)

  11. CIDRE-lite baseline
      - Compute by hand on a 4-journal subgraph
      - Compare function output
      - Check: score is between 0 and 1

  === STAGE 6: CONTINUOUS MONITORING DURING FULL RUN ===

  12. Log checkpoints after each major stage
      - STAGE 3 (Hodge): print min/max/mean of f_grad, f_residual
      - STAGE 4 (Communities): print number of communities, CVS distribution (percentiles)
      - STAGE 4 (Ground truth): print preliminary precision@5, @10, @20
      - STAGE 5 (Synthetic): print AUC at each boost level immediately after compute
      - STAGE 6 (Baselines): print comparison table as computed

  13. Intermediate save strategy
      - After Stage 3: save hodge_components to pickle (for debugging if later stages fail)
      - After Stage 4: save detected_communities to JSON (for inspection)
      - After Stage 5: save synthetic_results to JSON (don't lose synthetic data if crash)
      - After Stage 6: save all_baselines to CSV (human-readable for manual inspection)

  14. Failure detection triggers
      - If AUC < 0.5 on real data: flag as potential method failure, investigate
      - If precision@20 < 0.2: flag as poor real-world performance
      - If synthetic AUC doesn't monotonically increase: flag as noisy validation
      - If >30% of synthetic runs crash: stop, investigate root cause

  === SUCCESS CRITERIA FOR TESTING ===
  Proceed to full run only if:
      ✓ All unit tests pass (toy graphs decompose correctly)
      ✓ Integration test on mini network completes without error
      ✓ Real network Hodge decomposition is numerically stable (no NaN/Inf)
      ✓ Community detection finds 5-20 communities (reasonable count)
      ✓ Preliminary precision@5 ≥ 0.2 (at least some ground truth detected)
      ✓ Reciprocity and CIDRE-lite baselines compute without crash
      ✓ Synthetic cartel injection shows expected CVS elevation (>0.5 in cartels)

  If ANY criterion fails: DO NOT proceed to full multi-seed run. Debug, fix, re-test.

  === EXPECTED RUNTIME ESTIMATES ===
  - Unit tests: 5 min
  - Mini network integration: 5 min
  - Real network quick test: 10 min
  - Synthetic test: 5 min
  - Baseline tests: 5 min
  - **TOTAL TEST PHASE: ~30 min**
  - Full experiment run (with all seeds): ~5 hours 30 min
  - Total: 6 hours (as budgeted)
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_oKw95zbMmpyR
type: dataset
title: Journal Citation Network for Cartel Detection
summary: |-
  Dataset: journal_citation_network — a directed weighted journal-level citation network constructed from the OpenAlex REST API (free, no authentication required). The network covers publications from 2015–2022 across 96 high-impact journals (top 100 by global citation count, sourced via GET /sources sorted by cited_by_count:desc), with 888 directed edges representing cross-journal citation counts aggregated from 2,924 sampled papers. The closed-world construction algorithm is: (1) fetch top N journals; (2) for each journal fetch top-cited papers with referenced_works; (3) build paper→journal map; (4) count edges by looking up each referenced_work in the map — total API calls = N+1, no expensive resolution step.

  Each example corresponds to one journal node. The input field is a JSON string of per-journal network features: journal_name, issn_l, works_count, global_cited_by_count, in_degree, out_degree, in_citation_weight, out_citation_weight, mutual_citation_weight (sum of bidirectional citation counts — high values signal potential cartel behavior), citation_asymmetry (positive = net receiver / prestigious journal), mutual_citation_ratio (fraction of citations that are mutual), n_mutual_partners. The output field is 'normal' for the 96 top journals (none are on Clarivate's suppression list).

  The cartel ground truth is stored in temp/datasets/cartel_ground_truth.json: 17 verified cases from Clarivate JCR annual suppression lists (2013, 2018, 2024, 2025), including 12 citation-stacking cartels (e.g. the 2013 Brazilian cartel of 4 journals, 2025 MDPI/Wiley/Springer cases) and 5 self-citation cases. The research methodology is unsupervised anomaly detection — Hodge decomposition and Louvain community detection applied to the citation graph to find anomalous mutual-citation clusters, which are then validated against the ground truth suppression list. Graph statistics: 96 nodes, 888 edges, sparsity=0.097 (dense among top journals as expected), total citation count=2644.
workspace_path: >-
  /ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Web search (Serper), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-image-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
</skills>
</available_resources>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. Use it for framework choices, implementation patterns, agent orchestration.

- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Use aii-json skill's format script with `--input method_out.json` to generate full, mini, and preview versions. If not in your workspace (see <workspace> above), copy them there. Run 'ls -lh' to verify these three files exist (DO NOT read them).
TODO 2. Apply aii-file-size-limit skill's file size check procedure (100MB limit) to method_out.json and full_method_out.json.
TODO 3. Ensure a `pyproject.toml` exists in your workspace with ALL dependencies pinned to the exact versions installed in your .venv (run `.venv/bin/pip freeze` to get them). This is required for reproducibility. The [project] section must include name, version, requires-python, and a dependencies list with pinned versions (e.g. `numpy==2.0.2`, not `numpy>=2.0`).
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ExperimentExpectedFiles": {
      "description": "All expected output files from experiment artifact.",
      "properties": {
        "script": {
          "description": "Path to method.py script. Example: 'method.py'",
          "title": "Script",
          "type": "string"
        },
        "full_output": {
          "description": "Full method output JSON file. Example: 'full_method_out.json'",
          "title": "Full Output",
          "type": "string"
        },
        "mini_output": {
          "description": "Mini method output JSON file. Example: 'mini_method_out.json'",
          "title": "Mini Output",
          "type": "string"
        },
        "preview_output": {
          "description": "Preview method output JSON file. Example: 'preview_method_out.json'",
          "title": "Preview Output",
          "type": "string"
        }
      },
      "required": [
        "script",
        "full_output",
        "mini_output",
        "preview_output"
      ],
      "title": "ExperimentExpectedFiles",
      "type": "object"
    }
  },
  "description": "Experiment artifact \u2014 structured output + file metadata.\n\nImplements research methodology with baseline comparison.\nProduces method.py and method_out.json files.",
  "properties": {
    "title": {
      "default": "",
      "description": "Artifact title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); describe the content, not a status.",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/ExperimentExpectedFiles",
      "description": "All output files you created. Must include method.py script plus full/mini/preview method output JSON files."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files"
  ],
  "title": "ExperimentArtifact",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [9] SYSTEM-USER prompt · 2026-07-09 02:10:44 UTC

```
<validation-feedback>
Attempt 1 failed validation.

Schema validation found 1 problem — fix ALL of them at once:
  - at `layman_summary`: "We detect citation cartels in academic journals by decomposing citation flows into 'prestige' and 'circulation' parts using Hodge theory, then measuring how much unexplained circular citation each journal participates in — a Delta-CVS score that outperforms baseline methods with AUC 0.92-0.95." is too long (at most 250 characters, got 294)
Every required field must be present and every field type must match the schema.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```
