# upd_hypo — test_idea

> Phase: `invention_loop` · round 2 · `upd_hypo`
> Run: `run_HMncsxsr6ltD` — Hodge Decomposition for Citation Cartel Detection
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `upd_hypo` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-07-09 02:19:19 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A hypothesis reviser (Step 3.6: UPD_HYPO in the invention loop)

You received the current hypothesis, all artifacts, and the paper draft.
Revise the hypothesis based on what the evidence supports.

Honest revision → focused research. Inflated confidence → wasted iteration.
</your_role>
</ai_inventor_context>

You are revising a research hypothesis based on empirical evidence gathered
during an iterative invention loop. Your role is internal reflection — honest
assessment of what the evidence supports.

SCOPE: Your ONLY output is the revised hypothesis text. You do NOT run code,
produce artifacts, fix bugs, or otherwise act on the evidence yourself — the
next iteration of the invention loop will spawn fresh artifacts based on your
revised hypothesis. Reflect on the evidence and rewrite the hypothesis;
nothing else.

PRINCIPLES:
- Ground every revision in specific artifacts and results
- Treat negative and null results as valuable contributions. If the original
  approach failed, the null result IS often the contribution — frame it as
  such (e.g. "X does not improve Y under conditions Z"). Only pivot to a
  different positive claim when the evidence actually supports one; never
  fabricate a positive narrative to mask a failed approach.
- Increase specificity as evidence accumulates
- Don't inflate confidence without strong evidence
- Preserve the core AII prompt unless evidence clearly contradicts it
- Revise hypothesis text only — never attempt to address feedback by running
  code, proposing fixes, or producing artifacts; the next loop iteration
  handles all artifact generation

<current_hypothesis>
The hypothesis as it stands. Revise it based on the evidence below.

kind: hypothesis
title: Non-Gradient Flow Score for Citation Cartel Detection
hypothesis: >-
  Citation cartels create measurable non-gradient (rotational and harmonic) components in the Hodge decomposition of journal-level
  citation flows. In legitimate citation networks, flow is predominantly gradient-driven — citations flow hierarchically from
  lower-prestige to higher-prestige journals. Citation cartels, by their mutual reinforcement loops, inject divergence-free
  cyclic flows into the network. We hypothesize that the ratio of residual (non-gradient) flow energy to total flow energy
  within a candidate subgroup of journals — the Citation Vortex Score (CVS), defined as CVS(S) = ||f - f_grad||² / ||f||²
  — is a parameter-free, interpretable cartel detector that outperforms threshold-based baselines and degree-corrected null-model
  baselines on both synthetic and real Clarivate-suppressed journal groups. Critically, CVS measures the combined curl+harmonic
  residual after gradient extraction (not pure curl alone), which is nonetheless a valid anomaly signal because cartel-induced
  mutual citation loops elevate the non-gradient fraction relative to legitimate communities. On synthetic data with 8 injected
  cartel communities (15× mutual citation boost), CVS achieves AUC-ROC=1.0 vs. 0.892 for reciprocity ratio. The method's advantage
  over degree-corrected baselines (CIDRE-lite AUC=0.0 before sign correction) stems from avoiding the dcSBM's paradoxical
  normalization of large-journal cartel signal. Future validation must confirm this advantage holds on the 17 real Clarivate-suppressed
  journal cases available in the dataset, and sensitivity analysis at realistic boost levels (2×–10×) is needed to characterize
  the detection threshold. An optional extension — explicitly separating curl from harmonic via the triangle boundary operator
  B₂ — would produce a true 'Citation Vortex Score' in the strict topological sense and strengthen the theoretical framing.
motivation: >-
  Citation cartels damage science by inflating journal impact factors artificially, misallocating funding and researcher attention.
  Existing detection methods (CIDRE, threshold reciprocity) require careful parameter tuning (dcSBM thresholds, θ, θw), depend
  on a specific null model, and operate only at the journal level. A parameter-free method grounded in a first-principles
  decomposition of network flow would be more transparent, easier to audit, and potentially more robust. The Hodge decomposition
  separates any directed graph flow into an irrotational (gradient) component and a divergence-free (curl) component in a
  unique, lossless way — providing a direct physical interpretation: cartels are flow vortices. This cross-field import from
  mathematical physics / combinatorial topology has not been applied to citation integrity.
assumptions:
- >-
  Legitimate citation flow is predominantly hierarchical (gradient-driven): journals cite higher-prestige outlets more than
  those outlets cite them back, creating directed acyclic structure on average.
- >-
  Citation cartel behavior necessarily creates mutual reinforcement loops at the journal level, generating statistically detectable
  curl flow within the cartel subgroup.
- >-
  The journal-level citation graph (edge weight = number of cross-journal citations per year) is a sufficient representation
  for detecting cartel structure without paper- or author-level resolution.
- >-
  Clarivate's list of suppressed journals provides a reliable partial ground truth against which the CVS can be validated.
investigation_approach: |-
  1. DATA: Download journal-level citation aggregates from OpenAlex (free API, covers ~250M papers). For each pair of journals (i, j), compute the annual citation count c_{ij} for a selected year window (e.g., 2015–2022). Construct a directed weighted graph G = (V, E, w) where V = journals and w(i→j) = c_{ij}.

  2. HODGE DECOMPOSITION: Represent citation flows as a 1-chain on G. Compute the Hodge decomposition using the combinatorial gradient operator B1 (incidence matrix) and the curl operator B2 (triangle boundary matrix). Solve the least-squares system to extract the gradient component f_grad and residual curl+harmonic component f_curl. This reduces to sparse linear algebra (scipy.sparse.linalg.lsqr).

  3. SUBGROUP SCORING: For each candidate subgroup S (generated by Louvain community detection on the undirected projection of G), compute CVS(S) = sum of ||f_curl(e)||^2 for edges e within S, divided by sum of ||f(e)||^2 for edges e within S. Rank all subgroups by CVS descending.

  4. BASELINE COMPARISON: Implement CIDRE-lite (reciprocity-based excess citation fraction) and a simple reciprocity ratio baseline. Compare precision@K and recall@K against Clarivate's suspension list (46+ pairs), varying K.

  5. ABLATION: Test whether gradient-only component scores also help (e.g., gradient divergence as a complementary signal for journals that only receive but never give). Test temporal robustness across years.
success_criteria: |-
  CONFIRM: CVS achieves higher precision@20 and AUC-ROC than the reciprocity ratio baseline and matches or exceeds CIDRE-lite on the Clarivate suspension ground truth — demonstrating that the curl energy signal adds information beyond raw reciprocity counts. The method should flag at least 50% of confirmed cartel groups in the top decile of CVS-ranked subgroups.

  DISCONFIRM: If CVS performance is statistically indistinguishable from a simple pairwise reciprocity ratio (citations_ij / citations_ji), then the Hodge decomposition adds no information beyond what naive edge-level symmetry already captures, and the hypothesis should be rejected. If cartel groups do not consistently appear in the high-CVS tail but instead scatter uniformly across the CVS distribution, the vortex model does not describe cartel structure.
related_works:
- >-
  CIDRE (Sinatra & Rosvall, Scientific Reports 2021): Uses a degree-corrected stochastic block model (dcSBM) as a null model
  to identify journal groups with excessive within-group citations. Core mechanism is excess citation fraction relative to
  expected under dcSBM. CVS differs fundamentally — it uses no null model at all and requires no parameter tuning; instead
  it directly decomposes the observed flow into gradient vs. curl components via linear algebra, grounded in Hodge theory
  rather than a statistical generative model.
- >-
  HodgeRank (Jiang et al., Mathematical Programming 2011): Applies Hodge decomposition to pairwise ranking data to assess
  ranking consistency globally — the curl component flags inconsistencies in ranking preferences (e.g., movie ratings). CVS
  adapts this mechanism to a completely different task: detecting anomalous subgroups rather than assessing global ranking
  quality. CVS introduces the concept of a subgroup-local curl energy ratio as a cartel score, which HodgeRank does not compute.
- >-
  Toward the Discovery of Citation Cartels (Perez-Esparrells & Lopez-Otin, Frontiers in Physics 2016): Proposes threshold-based
  detection using semantic web tools and SPARQL queries on citation count graphs. Requires arbitrary threshold choice. CVS
  is parameter-free and more computationally scalable.
- >-
  Unsupervised Anomaly Detection in Journal Citation Networks (Lazaridou et al., JCDL 2020): Uses graph autoencoders and node
  embedding reconstruction error. Deep learning black-box approach; CVS is fully interpretable and requires no training data
  or neural network.
- >-
  XRP Remittance Hodge Decomposition (Fujiwara et al., 2022): Applies Hodge decomposition globally to a cryptocurrency ledger
  to identify hierarchical vs. circular money flows at the network level. Does not define subgroup-level curl scores for anomaly
  detection and does not address citation networks or cartel identification.
inspiration: >-
  The inspiration comes from a Level 3 (methodological) cross-domain transfer from mathematical physics and combinatorial
  topology into citation network analysis. In fluid dynamics, any vector field can be uniquely decomposed (Helmholtz decomposition)
  into an irrotational gradient part and a divergence-free curl/rotational part. Exactly this decomposition exists for directed
  graph flows — the Hodge decomposition on simplicial complexes. HodgeRank applied this to ranking problems. The key transfer
  insight: what is called 'ranking inconsistency' in HodgeRank is precisely what is called 'circular mutual citation' in citation
  cartel literature. The same mathematical object (curl flow) describes both phenomena. Adapting the decomposition to output
  a per-subgroup anomaly score (CVS) — rather than a global ranking assessment — is the novel methodological step. Secondary
  inspiration: wash-trading detection in cryptocurrency markets, which identifies closed transaction cycles; the Hodge curl
  component is a principled, continuous generalization of cycle counting.
terms:
- term: Hodge Decomposition
  definition: >-
    A unique orthogonal decomposition of any flow defined on the edges of a directed graph into three components: (1) gradient
    flow — consistent with a global node potential, analogous to water flowing downhill; (2) curl flow — locally cyclic, forming
    closed loops around triangles in the graph; (3) harmonic flow — globally cyclic but locally consistent. Computed via sparse
    least-squares on the graph incidence and boundary matrices.
- term: Citation Vortex Score (CVS)
  definition: >-
    The ratio of curl flow energy to total flow energy within a candidate subgroup of journals: CVS(S) = Σ_{e∈S} f_curl(e)²
    / Σ_{e∈S} f(e)². A high CVS indicates that most citation flow within the group is circular rather than hierarchical, which
    is the mathematical signature of a citation cartel.
- term: Gradient Flow
  definition: >-
    The component of citation flow that is consistent with a global prestige ranking: journal A cites journal B more than
    B cites A, suggesting B is more prestigious. This is the expected, healthy pattern in citation networks.
- term: Curl Flow
  definition: >-
    The component of citation flow that forms closed loops: A cites B, B cites C, C cites A. This is irreconcilable with any
    global linear ranking and represents coordinated reciprocal behavior — the hallmark of a citation cartel.
- term: Citation Cartel
  definition: >-
    A group of journals (or authors) that coordinate to cite each other at rates far exceeding what subject overlap or normal
    scholarly interaction would predict, with the goal of artificially inflating their Journal Impact Factor or h-index.
- term: Incidence Matrix (B1)
  definition: >-
    A matrix encoding the directed graph structure, where each column represents an edge and each row represents a node; entry
    is +1 if the node is the edge head, -1 if it is the tail. Used in Hodge decomposition to solve for the gradient potential.
summary: >-
  We propose detecting citation cartels by applying Hodge decomposition to journal-level citation flow graphs, extracting
  a parameter-free Citation Vortex Score (CVS) that measures how much of each subgroup's citation activity is circular (curl)
  rather than hierarchical (gradient). Unlike CIDRE and other methods, CVS requires no null model or threshold tuning and
  provides a direct physical interpretation — cartels are vortices in the citation flow field.
_relation_rationale: >-
  Same Hodge frame; reframed CVS as curl+harmonic residual, added real-data validation requirement.
_confidence_delta: decreased
_key_changes:
- >-
  Reframed CVS as measuring non-gradient (curl+harmonic residual) flow rather than claiming it measures pure curl flow — the
  current implementation does not separate curl from harmonic, so the 'vortex' framing is aspirational pending B₂ computation.
- >-
  Added explicit requirement for real-data validation against the 17 Clarivate ground-truth cases from cartel_ground_truth.json,
  which the experiment never used.
- >-
  Flagged that CIDRE-lite AUC=0.0 reflects sign inversion (perfect anti-correlation), not random failure — the baseline comparison
  must correct for this to be scientifically valid.
- >-
  Added requirement for sensitivity analysis across boost magnitudes (2×, 5×, 10×, 15×) to move beyond the toy 15× synthetic
  setting.
- >-
  Preserved the core claim that non-gradient flow is an effective cartel signal and that degree-corrected null models paradoxically
  suppress the signal for large cartel journals.
- >-
  Flagged optional path to true curl separation via B₂ as a strengthening extension, not a prerequisite for the core contribution.
relation_type: evolution
</current_hypothesis>

<all_artifacts>
Complete set of research artifacts across all iterations.

--- Item 1 ---
id: art_Rkxm3YsFRtot
type: research
title: Hodge Decomposition and Citation Cartel Detection Framework
summary: |-
  This research establishes three critical foundations for implementing a graph-based Citation Vortex Score (CVS) to detect citation cartels:

  **1. Mathematical Framework (Hodge Decomposition):** Hodge theorem decomposes directed graph flows into three orthogonal components: gradient (acyclic/hierarchical), curl (locally cyclic), and harmonic (globally cyclic) [1, 6]. In citation networks, gradient flow represents legitimate citation hierarchies while curl flow captures the rotational pattern signature of citation cartels (journals citing each other in circles). Implementation uses incidence matrix B1 (V×E with ±1 entries) and least-squares solver scipy.sparse.linalg.lsqr to extract gradient potential; residual contains curl + harmonic components. Computational complexity O(V·E) scales to large journal networks [1, 5].

  **2. Baseline Performance (CIDRE 2021):** The CIDRE algorithm detects anomalous journal groups using degree-corrected stochastic block model (dcSBM) as null model to account for journal size and research community structure. Empirical results: detected 12 of 22 JCR-suppressed cartel groups (54.5% recall), with 8 groups having Jaccard overlap ≥0.5 (67% high-confidence matches). CIDRE identified 10 groups before official JCR suspension, demonstrating predictive power [2, 3]. Simple reciprocity ratio baseline (pairwise mutual citation) fails because it ignores network context, journal size effects, and multi-step cycles [2].

  **3. Ground Truth Validation (Clarivate JCR):** Clarivate suppresses journals for excessive self-citation and citation stacking (coordinated multi-journal exchanges). Scale: 33 journals (0.27%) in 2020, 10 in 2021, 20 in 2025; 46 journal pairs historically reported by 2019 [7, 8, 9]. Ground truth limitations: partial coverage (~0.3% of 12,000 journals), 1-2 year detection lag, potential false positives from legitimate overlapping fields [8]. Typical cartel size: 2-10 journals (average 4) with 30-50%+ of incoming citations from within-group sources [2].

  **4. Implementation Tools:** OpenAlex API provides free access to 250M+ papers across 7,000+ journals for constructing journal citation graphs [10]. NetworkX.louvain_communities() identifies candidate subgroups; scipy.sparse solvers handle Hodge decomposition on sparse matrices [11, 12]. All tools are open-source with documented APIs.

  **5. Evaluation Framework:** Success criteria for CVS: (1) Precision@K > reciprocity baseline, (2) AUC-ROC > CIDRE (AUC ≥ 0.65 on imbalanced data), (3) Spearman ρ < 0.8 with reciprocity (novel signal confirmed) [2, 13]. Metrics: Jaccard overlap ≥0.5 with ≥2 shared journals for group matching, threshold-independent AUC-ROC for ranking quality, rank correlation tests for independence from baseline [2, 13].
workspace_path: >-
  /ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 2 ---
id: art_oKw95zbMmpyR
type: dataset
title: Journal Citation Network for Cartel Detection
summary: |-
  Dataset: journal_citation_network — a directed weighted journal-level citation network constructed from the OpenAlex REST API (free, no authentication required). The network covers publications from 2015–2022 across 96 high-impact journals (top 100 by global citation count, sourced via GET /sources sorted by cited_by_count:desc), with 888 directed edges representing cross-journal citation counts aggregated from 2,924 sampled papers. The closed-world construction algorithm is: (1) fetch top N journals; (2) for each journal fetch top-cited papers with referenced_works; (3) build paper→journal map; (4) count edges by looking up each referenced_work in the map — total API calls = N+1, no expensive resolution step.

  Each example corresponds to one journal node. The input field is a JSON string of per-journal network features: journal_name, issn_l, works_count, global_cited_by_count, in_degree, out_degree, in_citation_weight, out_citation_weight, mutual_citation_weight (sum of bidirectional citation counts — high values signal potential cartel behavior), citation_asymmetry (positive = net receiver / prestigious journal), mutual_citation_ratio (fraction of citations that are mutual), n_mutual_partners. The output field is 'normal' for the 96 top journals (none are on Clarivate's suppression list).

  The cartel ground truth is stored in temp/datasets/cartel_ground_truth.json: 17 verified cases from Clarivate JCR annual suppression lists (2013, 2018, 2024, 2025), including 12 citation-stacking cartels (e.g. the 2013 Brazilian cartel of 4 journals, 2025 MDPI/Wiley/Springer cases) and 5 self-citation cases. The research methodology is unsupervised anomaly detection — Hodge decomposition and Louvain community detection applied to the citation graph to find anomalous mutual-citation clusters, which are then validated against the ground truth suppression list. Graph statistics: 96 nodes, 888 edges, sparsity=0.097 (dense among top journals as expected), total citation count=2644.
workspace_path: >-
  /ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 3 ---
id: art_rxHyxG4rT2Xw
type: experiment
title: Citation Cartel Detection via Hodge Flow Decomposition
summary: |-
  This experiment implements the Citation Vortex Score (CVS), a novel method for detecting citation cartels in academic journal networks using Hodge decomposition. The core idea is that citation cartels create cyclic (rotational) citation flows — journals citing each other in loops — which manifest as the 'curl' component in Hodge's decomposition of the edge-flow vector on the citation graph.

  METHOD: CVS decomposes the observed citation flow f on a directed journal citation graph into gradient (f_grad = B1^T @ phi, solved via sparse least-squares) and residual (f_residual = f - f_grad) components. For each detected community S, CVS(S) = ||f_residual(S)||^2 / ||f(S)||^2 — the fraction of within-community flow that is 'curl-like' (non-gradient). High CVS indicates rotational, cartel-like citation behavior.

  BASELINES: (1) Reciprocity Ratio: mean(min(c_ij/c_ji, c_ji/c_ij)) across journal pairs in each community — measures how balanced mutual citations are. (2) CIDRE-lite: excess citations above a degree-corrected null model (E[c_ij] = out_i * in_j / total), normalized by total within-community citations.

  DATA: A 500-journal synthetic citation network with hierarchical community structure (25 communities of ~20 journals each), augmented with real OpenAlex journal citation data. Eight synthetic citation cartels (4 journals each) were injected with a 15x mutual citation boost as ground truth.

  RESULTS (23 communities, 8 cartel / 15 legitimate):
  - CVS: AUC-ROC=1.000, P@5=1.000, P@10=0.800, AP=1.000
  - Reciprocity Ratio: AUC-ROC=0.892, P@5=1.000, P@10=0.600, AP=0.865
  - CIDRE-lite: AUC-ROC=0.000 (anti-correlated), P@5=0.000, AP=0.220
  - Temporal stability: mean Spearman r=0.939 across 4 time windows

  DIAGNOSIS: CVS outperforms both baselines. Reciprocity Ratio captures some signal but is less discriminative. CIDRE-lite fails because the degree-corrected null model expects high mutual citations for high-degree (cartel) journals, normalizing away the cartel signal — this is a genuine limitation of degree-correction in the presence of citation manipulation.

  CONCLUSION: Hodge decomposition provides a principled geometric lens for cartel detection. The curl component uniquely captures the rotational structure of citation manipulation independently of node degree, making CVS robust where degree-corrected baselines fail.
workspace_path: >-
  /ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_1/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 4 ---
id: art_dqMP5SU9PDKR
type: research
in_dependencies:
- id: art_Rkxm3YsFRtot
  label: theoretical foundation
title: Hodge Decomposition, B₂ Operators, and CIDRE for Citation Cartels
summary: >-
  This research establishes that **true curl-harmonic separation via B₂ triangle boundary operators is scientifically novel,
  computationally feasible, and worth implementing for citation cartel detection**. Key findings: (1) HLSAD (2025) validates
  Hodge Laplacians on simplicial complexes; directed extension is novel but mathematically sound [1]. (2) CIDRE's degree-corrected
  stochastic block model achieves 54.5% recall on JCR suppressions by controlling for journal size and research communities
  [3]. (3) Reciprocity ratio baseline fails completely (~0% recall) due to ignoring network context [3]. (4) B₂-based Curl-Vortex
  Score (CVS) separates locally cyclic (cartel signature) from globally cyclic (legitimate feedback) flows, offering potential
  improvement over CIDRE's conflated residual [1, 2, 6]. (5) Computational cost is ~1-3 minutes per year on standard CPU;
  all required tools (scipy.sparse.linalg, NetworkX, OpenAlex) are production-ready [4, 5]. (6) Main implementation risk is
  directed graph B₂ orientation handling; mitigable via careful definition and validation on synthetic cartels. (7) Success
  criteria are clear: exceed CIDRE's 54.5% recall while maintaining ≥50% precision on JCR suppressions.
workspace_path: >-
  /ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_2/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 5 ---
id: art_hakO60eWu4mW
type: experiment
in_dependencies:
- id: art_oKw95zbMmpyR
  label: citation network
title: Hodge Decomposition for Citation Cartel Detection
summary: |-
  Experiment: CVS (Citation Vortex Score) cartel detection via Hodge decomposition on the 96-journal OpenAlex citation network.

  METHOD: Hodge decomposition splits directed citation flows into (1) a gradient component explaining prestige-driven citations and (2) a residual (curl+harmonic) component capturing unexplained circulation. The Citation Vortex Score (CVS) of a subgraph is residual_energy / total_energy. For node-level scoring we use Delta-CVS: the change in absolute residual energy per node after cartel injection, which avoids the scale-invariance issue of the ratio-based CVS.

  KEY FINDING: The top-96 journals by citation count contain no Clarivate-suppressed cartel journals (those are mid-tier), so validation is fully synthetic. Synthetic cartel injection at boost levels 2x-15x within same-field community subsets yields:
    - Delta-CVS AUC: 0.921-0.954 (strongly detects injected cartels)
    - Delta-Reciprocity AUC: ~0.50 (random, no signal)
    - Delta-CIDRE-lite AUC: 0.500 (random, no signal)

  Hodge decomposition statistics: 77.7% of total citation energy is residual (circulation), confirming that top journals have substantial unexplained mutual citation patterns beyond prestige gradients.

  NETWORK: 96 nodes, 888 directed edges, 5 Louvain communities (seed 0), community CVS range 0.63-0.92.

  BASELINES: Reciprocity ratio (mean min/max pairwise citation ratio) and CIDRE-lite (internal edge density) both score ~0.50 AUC on synthetic validation vs Delta-CVS at 0.92+. This confirms the Hodge decomposition provides a signal not captured by simpler mutual-citation metrics.

  OUTPUT FORMAT: Per-journal predictions (predict_cvs, predict_reciprocity, predict_cidre_lite) plus rich metadata fields (absolute_residual_energy, mutual_residual_energy, community_cvs, reciprocity_score, cidre_lite_score). All 96 journals included.
workspace_path: >-
  /ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 6 ---
id: art_d8F9xLleMApN
type: evaluation
in_dependencies:
- id: art_rxHyxG4rT2Xw
  label: CVS baseline results
title: 'CVS Citation Cartel Detection: Statistical Validation'
summary: |-
  Comprehensive statistical evaluation of Citation Vortex Score (CVS) via Hodge decomposition for citation cartel detection.

  DATA: 23 communities (8 cartel, 15 legitimate) from a 500-journal synthetic network augmented with real OpenAlex data. Ground truth: 8 synthetic cartels injected at specified boost magnitudes.

  PRIMARY RESULTS:
  - CVS: AUC-ROC=1.000 [1.000, 1.000], P@5=1.000, P@10=0.800, P@20=0.400, Recall@Top-Decile=1.000
  - Reciprocity Ratio baseline: AUC-ROC=0.892 [0.751, 1.000], P@5=1.000, P@10=0.600
  - CIDRE-lite baseline: AUC-ROC=0.000 (anti-correlated with cartel labels)
  - DeLong test CVS vs Reciprocity: p=0.130; CVS vs CIDRE: p=1.000 (CIDRE performs no better than chance)

  ROBUSTNESS:
  - Boost sensitivity: CVS AUC rises from 0.560 (2x boost) → 0.690 (5x) → 0.940 (10x) → 0.988 (15x); reciprocity plateaus at ~0.79
  - Community detection: Louvain/Leiden/Infomap all achieve mean AUC=1.000 across 10 seeds each; CV=0.000 per method; Kruskal-Wallis H=0.0, p=1.0 (methods statistically indistinguishable)
  - Temporal stability: mean Spearman ρ=0.939 [0.920, 0.957] across 6 window pairs

  ERROR ANALYSIS:
  - 12 false positives in top-20 ranked communities (all legitimate communities with high natural reciprocity)
  - 8 true positives correctly identified in top-20
  - Threshold sensitivity analysis over 20 CVS cutpoints provided
  - Recall by rank bin: all 8 cartels fall in top 10% of CVS rankings

  CONCLUSION: CVS hypothesis confirmed. CVS achieves perfect AUC on this dataset and is robust to community detection method choice. The method dominates both baselines and maintains high temporal stability. Main limitation: at low boost magnitudes (2x), CVS performance drops substantially (AUC=0.56), suggesting practical deployment requires cartels with at least 5-10x citation amplification.
workspace_path: >-
  /ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</all_artifacts>

<new_artifacts_this_iteration>
These 3 artifacts were created THIS iteration.

id: art_dqMP5SU9PDKR
type: research
in_dependencies:
- id: art_Rkxm3YsFRtot
  label: theoretical foundation
title: Hodge Decomposition, B₂ Operators, and CIDRE for Citation Cartels
summary: >-
  This research establishes that **true curl-harmonic separation via B₂ triangle boundary operators is scientifically novel,
  computationally feasible, and worth implementing for citation cartel detection**. Key findings: (1) HLSAD (2025) validates
  Hodge Laplacians on simplicial complexes; directed extension is novel but mathematically sound [1]. (2) CIDRE's degree-corrected
  stochastic block model achieves 54.5% recall on JCR suppressions by controlling for journal size and research communities
  [3]. (3) Reciprocity ratio baseline fails completely (~0% recall) due to ignoring network context [3]. (4) B₂-based Curl-Vortex
  Score (CVS) separates locally cyclic (cartel signature) from globally cyclic (legitimate feedback) flows, offering potential
  improvement over CIDRE's conflated residual [1, 2, 6]. (5) Computational cost is ~1-3 minutes per year on standard CPU;
  all required tools (scipy.sparse.linalg, NetworkX, OpenAlex) are production-ready [4, 5]. (6) Main implementation risk is
  directed graph B₂ orientation handling; mitigable via careful definition and validation on synthetic cartels. (7) Success
  criteria are clear: exceed CIDRE's 54.5% recall while maintaining ≥50% precision on JCR suppressions.
workspace_path: >-
  /ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_2/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

id: art_hakO60eWu4mW
type: experiment
in_dependencies:
- id: art_oKw95zbMmpyR
  label: citation network
title: Hodge Decomposition for Citation Cartel Detection
summary: |-
  Experiment: CVS (Citation Vortex Score) cartel detection via Hodge decomposition on the 96-journal OpenAlex citation network.

  METHOD: Hodge decomposition splits directed citation flows into (1) a gradient component explaining prestige-driven citations and (2) a residual (curl+harmonic) component capturing unexplained circulation. The Citation Vortex Score (CVS) of a subgraph is residual_energy / total_energy. For node-level scoring we use Delta-CVS: the change in absolute residual energy per node after cartel injection, which avoids the scale-invariance issue of the ratio-based CVS.

  KEY FINDING: The top-96 journals by citation count contain no Clarivate-suppressed cartel journals (those are mid-tier), so validation is fully synthetic. Synthetic cartel injection at boost levels 2x-15x within same-field community subsets yields:
    - Delta-CVS AUC: 0.921-0.954 (strongly detects injected cartels)
    - Delta-Reciprocity AUC: ~0.50 (random, no signal)
    - Delta-CIDRE-lite AUC: 0.500 (random, no signal)

  Hodge decomposition statistics: 77.7% of total citation energy is residual (circulation), confirming that top journals have substantial unexplained mutual citation patterns beyond prestige gradients.

  NETWORK: 96 nodes, 888 directed edges, 5 Louvain communities (seed 0), community CVS range 0.63-0.92.

  BASELINES: Reciprocity ratio (mean min/max pairwise citation ratio) and CIDRE-lite (internal edge density) both score ~0.50 AUC on synthetic validation vs Delta-CVS at 0.92+. This confirms the Hodge decomposition provides a signal not captured by simpler mutual-citation metrics.

  OUTPUT FORMAT: Per-journal predictions (predict_cvs, predict_reciprocity, predict_cidre_lite) plus rich metadata fields (absolute_residual_energy, mutual_residual_energy, community_cvs, reciprocity_score, cidre_lite_score). All 96 journals included.
workspace_path: >-
  /ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

id: art_d8F9xLleMApN
type: evaluation
in_dependencies:
- id: art_rxHyxG4rT2Xw
  label: CVS baseline results
title: 'CVS Citation Cartel Detection: Statistical Validation'
summary: |-
  Comprehensive statistical evaluation of Citation Vortex Score (CVS) via Hodge decomposition for citation cartel detection.

  DATA: 23 communities (8 cartel, 15 legitimate) from a 500-journal synthetic network augmented with real OpenAlex data. Ground truth: 8 synthetic cartels injected at specified boost magnitudes.

  PRIMARY RESULTS:
  - CVS: AUC-ROC=1.000 [1.000, 1.000], P@5=1.000, P@10=0.800, P@20=0.400, Recall@Top-Decile=1.000
  - Reciprocity Ratio baseline: AUC-ROC=0.892 [0.751, 1.000], P@5=1.000, P@10=0.600
  - CIDRE-lite baseline: AUC-ROC=0.000 (anti-correlated with cartel labels)
  - DeLong test CVS vs Reciprocity: p=0.130; CVS vs CIDRE: p=1.000 (CIDRE performs no better than chance)

  ROBUSTNESS:
  - Boost sensitivity: CVS AUC rises from 0.560 (2x boost) → 0.690 (5x) → 0.940 (10x) → 0.988 (15x); reciprocity plateaus at ~0.79
  - Community detection: Louvain/Leiden/Infomap all achieve mean AUC=1.000 across 10 seeds each; CV=0.000 per method; Kruskal-Wallis H=0.0, p=1.0 (methods statistically indistinguishable)
  - Temporal stability: mean Spearman ρ=0.939 [0.920, 0.957] across 6 window pairs

  ERROR ANALYSIS:
  - 12 false positives in top-20 ranked communities (all legitimate communities with high natural reciprocity)
  - 8 true positives correctly identified in top-20
  - Threshold sensitivity analysis over 20 CVS cutpoints provided
  - Recall by rank bin: all 8 cartels fall in top 10% of CVS rankings

  CONCLUSION: CVS hypothesis confirmed. CVS achieves perfect AUC on this dataset and is robust to community detection method choice. The method dominates both baselines and maintains high temporal stability. Main limitation: at low boost magnitudes (2x), CVS performance drops substantially (AUC=0.56), suggesting practical deployment requires cartels with at least 5-10x citation amplification.
workspace_path: >-
  /ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</new_artifacts_this_iteration>

<current_paper>
The paper draft from this iteration — represents the current state of the research story.

# Introduction

Academic citation networks form the foundation of scientific reputation and resource allocation. The Journal Impact Factor (JIF)—the mean number of citations a journal receives annually—directly influences research funding, hiring decisions, and institutional rankings. This high-stakes system creates perverse incentives: organized groups of journals can artificially inflate their impact factors through citation cartels—coordinated networks of mutual citation exchanges at artificially high rates. Clarivate, the authority publishing Journal Citation Reports, has suspended approximately 20 journals annually in recent years for excessive self-citation and citation stacking, suggesting the problem is widespread and accelerating [1].

Citation cartels damage science in multiple ways. They crowd out citations to foundational work, misrepresent research importance, and redirect both reader attention and funding toward a narrow set of journals. A typical cartel comprises 2–10 journals, with 30–50% or more of incoming citations from within-group sources—far above normal disciplinary norms [1].

The scientific challenge is detection. Existing methods fall into two categories, each with critical limitations. **Threshold-based approaches** identify journal pairs with excessive mutual citations, but ignore network context and miss multi-step cycles (A→B→C→A) that characterize sophisticated cartels. **Statistical null-model approaches** like the degree-corrected stochastic block model (dcSBM, used in CIDRE) explicitly expect high mutual citations among large, active journals, potentially normalizing away the cartel signal by design [1]. Neither method is parameter-free or fully transparent.

We propose a fundamentally different approach: **Citation Vortex Score (CVS)**, grounded in Hodge decomposition from algebraic topology. The mathematical insight is that flow on any directed graph decomposes uniquely into three orthogonal components: (1) **gradient flow**—acyclic hierarchical patterns reflecting legitimate prestige hierarchies; (2) **curl flow**—locally rotational patterns reflecting citation cartels; and (3) **harmonic flow**—globally cyclic but locally consistent patterns. By measuring the ratio of non-gradient (residual) energy to total energy within journal communities, we obtain a parameter-free, interpretable cartel score requiring no null model tuning and no training data.

This is a cross-domain transfer from mathematical physics and combinatorial topology. HodgeRank, a prior work applying Hodge decomposition to ranking problems, showed that ranking inconsistency manifests as rotational (curl-like) flow [2]. The insight—that rotational flow in a network encodes coordination or anomaly—applies equally to citation behavior. We adapt this machinery to output a per-subgroup anomaly score rather than a global ranking quality assessment, introducing both methodological and application-domain novelty.

[FIGURE:fig_1]

## Summary of Contributions

- **Theoretical**: We establish that citation cartel structure—mutual reinforcement loops—corresponds to high non-gradient components in Hodge decomposition of citation flow networks. Gradient-only flow represents healthy hierarchical citation; non-gradient (curl + harmonic) residuals reveal coordinated behavior [3].
- **Methodological**: We introduce Citation Vortex Score (CVS), a closed-form parameter-free detector requiring no null model or threshold tuning. CVS(S) = ||f_residual(S)||² / ||f(S)||² for subgroup S, computed via sparse linear algebra in O(V·E) time [4].
- **Empirical**: On synthetic data with ground-truth cartels (15× citation boost), CVS achieves AUC-ROC=1.0 vs. 0.892 for reciprocity ratio and 0.0 for degree-corrected baselines, demonstrating that residual flow captures cartel signal independent of node degree [4, 5].
- **Robustness**: CVS shows high temporal stability (mean Spearman ρ=0.939 across multi-year windows) and robustness across community detection methods (Louvain, Leiden, Infomap all achieve identical performance) [4, 5].
- **Practical**: CVS integrates seamlessly with open-source tools (OpenAlex, NetworkX, SciPy) and scales to large journal networks (O(V·E) complexity; <3 minutes for 7000 journals) [4].

# Related Work

## Citation Cartel Detection

The seminal work on cartel detection is CIDRE (Detecting Citation Cartels in Journal Networks) by Kojaku, Livan, and Masuda [1]. CIDRE uses a degree-corrected stochastic block model (dcSBM) as a null model, identifying journal groups with excess citations relative to expected values under dcSBM. Empirically, CIDRE detected 12 of 22 JCR-suppressed cartel groups (54.5% recall), with 8 groups showing Jaccard overlap ≥0.5 with suppressed journals [1]. CIDRE also demonstrated predictive power, identifying 10 groups 1–2 years before Clarivate suspension [1]. However, CIDRE requires careful null model parameter tuning and threshold selection for group identification.

Earlier work by Pérez-Esparrells and López-Otín used semantic web tools and SPARQL queries on citation count graphs, requiring arbitrary threshold choices [6]. More recent anomaly detection approaches, such as methods using graph autoencoders and node embedding reconstruction error, lack interpretability and require labeled training data [7].

CVS differs fundamentally from all prior work: it requires no null model, no threshold, and no training data. Instead, it directly decomposes observed citation flow into gradient versus non-gradient components via linear algebra, providing an interpretable geometric signal grounded in Hodge theory.

## Hodge Theory and Network Flow Decomposition

Hodge decomposition originates in differential geometry but has been adapted to discrete graphs [2, 8, 9]. The foundational work is HodgeRank by Jiang et al., which applies Hodge decomposition to ranking data (e.g., movie ratings) [2]. HodgeRank decomposes pairwise ranking data into gradient flow (consistent with a global ranking) and residual (ranking inconsistency). The residual component, while combining curl and harmonic flows, quantifies total inconsistency [2].

Recent applications demonstrate Hodge theory's generality across domains. Frantzen & Schaub (2025) apply Hodge decomposition to simplicial complexes for anomaly detection (HLSAD), showing superior performance on datasets with higher-order structure [10]. Hodge decomposition has been applied to biomolecular networks to identify functional modules [11] and to urban traffic flows to separate directional flow (gradient) from circulation patterns (curl), showing that curl identifies congestion bottlenecks [12]. These diverse applications suggest that non-gradient flow is a general marker of anomalous or coordinated behavior.

Our contribution is to recognize that citation cartel behavior—the signature of coordinated journals—manifests as elevated non-gradient flow in the citation network. This is not obvious: while the mathematical structures are similar (both decompose flow on graphs), the domain interpretation and per-subgroup scoring methodology are novel.

## Network Anomaly Detection

Broader anomaly detection literature includes community detection algorithms (Louvain, Leiden, Infomap), which identify clusters in networks [13]. However, CIDRE analysis showed that standard community detection finds 3× more groups than CIDRE but with zero matches to JCR suppressions [1], indicating that legitimate research communities confound pure graph clustering. CVS addresses this by focusing on flow residual structure, not just community density. Unlike pure clustering, CVS measures a specific topological signal (non-gradient flow) known to be elevated in coordinated structures.

# Methods

## Problem Formulation

Let G = (V, E) be a directed weighted journal citation network where V = journals and edge weight w(i → j) = annual citations from journal i to journal j [3]. We represent citation flow as a 1-chain f : E → ℝ, mapping each edge to its citation count. A subgroup S ⊆ V induces a subflow f|_S consisting of all edges within S.

The problem: for each candidate subgroup S, compute a score indicating whether citations within S are predominantly acyclic (gradient-driven, legitimate) or contain significant non-gradient (circulation, anomalous) components.

## Hodge Decomposition on Directed Graphs

Hodge theorem states that any flow f on a directed graph G decomposes uniquely into orthogonal components. On a directed graph, this decomposition is formalized using the incidence matrix B₁ (dimensions V × E):

- B₁(v, e) = +1 if v is the head of edge e
- B₁(v, e) = −1 if v is the tail of edge e  
- B₁(v, e) = 0 otherwise

The **gradient component** satisfies f_grad = B₁ᵀφ for some potential φ : V → ℝ. Gradient flow represents citations flowing from lower-prestige to higher-prestige journals, consistent with a global ranking.

The **residual component** r = f - f_grad contains the non-gradient (curl + harmonic) flows. This residual captures circular citation patterns that cannot be explained by any global journal prestige ranking.

### Gradient Extraction via Least-Squares

To extract f_grad, we solve the least-squares problem:

```
φ* = argmin_φ ||f - B₁ᵀφ||²
```

This is equivalent to solving the normal equation (B₁B₁ᵀ)φ = B₁f. Using the sparse least-squares solver scipy.sparse.linalg.lsqr, we efficiently compute φ* even for large networks (V, E in thousands) in O(V·E) time [4].

The gradient component is then f_grad = B₁ᵀφ*, and the residual f_residual = f - f_grad contains the non-gradient signal.

## Citation Vortex Score (CVS)

For a candidate subgroup S ⊆ V, define the Citation Vortex Score as:

```
CVS(S) = ||f_residual(S)||² / ||f(S)||²
```

where:
- ||f(S)||² = sum of squared flow magnitudes on edges within S
- ||f_residual(S)||² = sum of squared residual magnitudes on edges within S

CVS is a ratio in [0, 1]:
- **CVS → 0**: Flow is predominantly acyclic (gradient-driven), indicating a legitimate research community.
- **CVS → 1**: Flow is predominantly non-gradient (circulation), indicating rotational patterns characteristic of citation cartels.

CVS requires no tuning: the only "parameter" is the choice of subgroups S, which we obtain from community detection (Louvain algorithm on the undirected projection of G). All subsequent computation is deterministic [4].

**Relationship to Hodge theory**: The residual component f_residual = f - f_grad contains both curl (locally cyclic, triangular inconsistency) and harmonic (globally cyclic, balanced feedback) flows. While a complete topological interpretation would require explicit curl/harmonic separation via triangle boundary operators B₂ (advanced extension), the combined non-gradient fraction is nonetheless a valid cartel signal: cartels inject circulation (either curl or harmonic) that elevates the residual fraction above normal community levels.

## Baseline Methods

We compare CVS against two baselines:

### Reciprocity Ratio
For each subgroup S, compute the pairwise reciprocity as the mean of min(c_ij, c_ji) / max(c_ij, c_ji) across all journal pairs (i, j) ∈ S [4]. High ratios indicate balanced mutual citation. This baseline captures only pairwise symmetry and ignores network structure, multi-step cycles, and journal size effects.

### CIDRE-lite (Degree-Corrected Null Model)
For each subgroup S, compute the excess citation fraction under a simplified degree-corrected stochastic block model: (observed - expected) / expected [1]. This represents the baseline approach using a null model assumption. Unlike the full CIDRE algorithm, we use Louvain community detection for subgroup identification (rather than CIDRE's internal block inference) to isolate the null-model comparison.

# Experiments

## Dataset and Experimental Setup

We evaluate CVS on a synthetic dataset with ground-truth labels. The synthetic setup allows controlled evaluation before deployment on real (partially-labeled) cartel data.

**Construction**: Starting with a 500-journal network built from OpenAlex data (2015–2022), we: (1) construct the undirected projection of the citation graph; (2) run Louvain community detection to obtain 23 candidate subgroups (ranging from 4–40 journals, mean ~22 journals per group); (3) inject synthetic cartels by selecting 8 of the 23 communities and boosting mutual citation rates by 15× [5].

This yields an imbalanced dataset: 8 cartel communities (cartels), 15 legitimate communities. The 15× boost was chosen to represent a realistic cartel signal: empirically, confirmed cartels show 5–50× amplification relative to normal discipline norms [1].

**Sensitivity analysis**: We also evaluate at boost levels 2×, 5×, 10× to characterize detection performance at varying signal strengths [5].

We evaluate all three methods (CVS, reciprocity ratio, CIDRE-lite) on the same 23 communities using identical community detection (Louvain with seed 0).

## Primary Results: Ranking Performance

[FIGURE:fig_2]

On the 15× boost synthetic dataset, CVS achieves near-perfect discrimination [4, 5]:
- **AUC-ROC = 1.000** (perfect ranking of cartels vs. legitimate groups; 95% CI [1.000, 1.000])
- **Precision@5 = 1.000** (all top 5 ranked groups are cartels)
- **Precision@10 = 0.800** (8 of 10 top groups are cartels)
- **Precision@20 = 0.400** (8 of 20 top groups are cartels; remaining 12 are false positives—legitimate communities with naturally high citation density)
- **Average Precision = 1.000**
- **Recall@Top-Decile = 0.25** (2.3 of 8 cartels in top 10% of ranking; however, all 8 cartels appear in top 35% of communities by CVS ranking)

Reciprocity Ratio achieves moderate performance [4, 5]:
- **AUC-ROC = 0.892** (95% CI [0.751, 1.000])
- **Precision@5 = 1.000**, **Precision@10 = 0.600**
- **Average Precision = 0.865**
- DeLong test vs. CVS: p=0.130 (trend toward CVS superiority, not statistically significant at α=0.05 given small sample size)

CIDRE-lite fails completely [4, 5]:
- **AUC-ROC = 0.000** (95% CI [0.000, 0.000]) — anti-correlated with cartel labels
- **Precision@5 = 0.000**, **Precision@10 = 0.000**
- **Average Precision = 0.220**
- DeLong test vs. CVS: p=1.000 (CIDRE-lite performs no better than random)

### Interpreting CIDRE-lite Failure

The failure of CIDRE-lite reveals a critical insight: degree-corrected null models assume that high within-community citation rates are expected for large, high-activity communities. By design, dcSBM normalizes away the cartel signal. In our synthetic data, injected cartels are high-degree subgroups (many edges, large citation counts). The dcSBM expectation is also high, making the excess fraction small or even negative, despite absolute citation levels being anomalous. CVS avoids this trap by decomposing flow directly, independent of degree assumptions [4, 5].

## Robustness Analysis

### Community Detection Method Independence

We test whether CVS rankings remain stable across different community detection algorithms [5]:
- **Louvain**: Mean AUC = 1.000 across 10 random seeds; CV = 0.0
- **Leiden**: Mean AUC = 1.000 across 10 random seeds; CV = 0.0
- **Infomap**: Mean AUC = 1.000 across 10 random seeds; CV = 0.0
- **Kruskal-Wallis H-test**: H = 0.0, p = 1.0 (no significant difference among methods)

This demonstrates that CVS is robust to community detection algorithm choice, a key robustness property [5].

### Temporal Stability

We test whether CVS rankings remain stable across non-overlapping year windows (2015–2017, 2017–2019, 2019–2021) [4, 5]:
- **2015–2017 vs. 2017–2019**: Spearman ρ = 0.919
- **2017–2019 vs. 2019–2021**: Spearman ρ = 0.937
- **2015–2017 vs. 2019–2021**: Spearman ρ = 0.904
- **Mean Spearman ρ = 0.939** (95% CI [0.920, 0.957])

This high correlation (ρ > 0.9) indicates that CVS rankings are robust across multi-year windows, suggesting the method captures stable structural properties of the network rather than year-specific noise [5].

### Signal Strength Sensitivity

[FIGURE:fig_3]

We evaluate how CVS performance degrades as the cartel injection strength decreases [5]:
- **2× boost**: CVS AUC = 0.559 (barely above random); Reciprocity AUC = 0.762
- **5× boost**: CVS AUC = 0.690; Reciprocity AUC = 0.798  
- **10× boost**: CVS AUC = 0.940; Reciprocity AUC = 0.798
- **15× boost**: CVS AUC = 0.988; Reciprocity AUC = 0.786

CVS sensitivity increases nonlinearly with boost level: at weak signals (2–5×), reciprocity outperforms CVS; at realistic strong signals (10–15×), CVS dominates. This suggests CVS is tuned for high-amplitude cartels. The crossover at ~7× boost represents a practical detection threshold: cartels must amplify citations by ≥7–10× for CVS to reliably exceed reciprocity-based detection [5].

### Independence from Reciprocity Baseline

To confirm that CVS captures novel signal beyond pairwise reciprocity, we compute Spearman rank correlation between CVS and reciprocity ratio scores across all 23 communities:

**Spearman ρ(CVS, Reciprocity) = 0.65**

A correlation of 0.65 indicates moderate but non-trivial dependence. CVS and reciprocity rank communities differently: CVS identifies cartels via flow residual structure, while reciprocity only counts bidirectional edges. This difference is crucial: cartels using multi-step cycles and complex mutual citation patterns will have different CVS and reciprocity rankings [4].

## Error Analysis

The 12 false positives in the top-20 ranked communities are all legitimate communities with naturally high reciprocal citation rates. These arise from high-activity research fields where journals cite each other at elevated rates due to subject overlap, not coordination. This represents the fundamental challenge in cartel detection: distinguishing anomalous coordination from legitimate dense citation communities. Future work on field-normalized baselines would address this limitation.

# Discussion

## Limitations

1. **Synthetic Ground Truth**: Our evaluation uses injected synthetic cartels rather than real Clarivate-suppressed groups. While synthetic setup allows controlled ground truth, the 15× boost may not reflect realistic cartel subtlety. Real cartels may employ more sophisticated strategies (spreading mutations across time, mimicking field citations), and CVS performance on actual JCR data remains to be validated.

2. **Subgroup Sensitivity**: CVS depends on the choice of subgroups S. While we demonstrate robustness across three major community detection algorithms, different algorithms may still identify different subgroups. A systematic ablation with many detection methods and parameter variations would strengthen robustness claims. Additionally, we use Louvain on the undirected projection, which discards directed information; methods leveraging directed structure (e.g., Infomap on directed graphs) may identify more cartel-relevant partitions.

3. **Field-Specific Citation Density**: Legitimate research communities in specialized fields (rare disease journals, regional studies) naturally have high reciprocal citation rates and elevated non-gradient flow. Without field-normalized baselines, CVS may produce false positives in high-collaboration disciplines. Developing discipline-specific curl expectations would reduce false positives but requires additional training data or domain expertise.

4. **Signal Strength Threshold**: The sensitivity analysis reveals that CVS performance drops substantially at weak signal levels (AUC=0.56 at 2× boost). This suggests practical deployment requires cartels with substantial citation amplification (10×+). Real cartels may operate more subtly, and CVS could miss low-amplitude manipulation. Trade-off: higher sensitivity could be achieved by lowering thresholds, but this would increase false positives on legitimate dense communities.

5. **Real-World Validation**: Ground truth for real cartels is incomplete. Clarivate's suppression list captures only ~0.3% of 12,000 journals annually; many actual cartels may operate undetected. CVS evaluation on real data must use this noisy ground truth, and comparison metrics (recall, precision) will have inherent measurement error.

## Relationship to CIDRE

CIDRE achieved 54.5% recall on JCR-suppressed groups, representing the current state-of-the-art on real data. CVS's perfect AUC on synthetic data suggests it *could* exceed CIDRE on real data, but real validation is essential. Key differences:

- **Transparency**: CVS has no tunable parameters; CIDRE requires threshold selection and null model tuning. This makes CVS easier to audit and deploy.
- **Robustness to degree**: CVS's independence from degree assumptions makes it robust to journal size variations; CIDRE's dcSBM can paradoxically miss large-scale cartels that the null model expects.
- **Interpretability**: CVS has geometric meaning (non-gradient flow = circulation patterns); CIDRE's excess citation fraction is more opaque.
- **Methodological novelty**: CVS introduces a new topological signal (Hodge decomposition) to cartel detection; CIDRE builds on established stochastic block model framework.

However, CIDRE's full algorithm includes internal threshold-tuned subgroup extraction and multi-year predictive tracking, which we simplified to Louvain in this work. A fully fair comparison would implement complete CIDRE alongside our CVS.

## Technical Remarks

**Curl vs. Harmonic Decomposition**: The current CVS implementation measures combined (curl + harmonic) non-gradient flow. A more refined approach would explicitly separate curl (locally cyclic) from harmonic (globally cyclic) components via the triangle boundary operator B₂. This requires constructing directed triangles in the citation graph and computing the Hodge Laplacian's full spectral decomposition. Recent work (HLSAD, 2025) validates this approach on simplicial complexes; extending to directed citation graphs is scientifically novel but requires additional implementation complexity [10]. The current residual metric is nonetheless a valid cartel signal, as both curl and harmonic components are elevated in coordinated structures.

**Scalability**: The algorithm scales as O(V·E) for gradient extraction via least-squares, O(E^1.5) for triangle enumeration (if curl separation is added), and O(E·log(E)) for community detection. For the full OpenAlex network (7000 journals, ~50k citation edges), total runtime is estimated at 1–3 minutes per year on standard CPU hardware. Parallelization of independent years or permutations can further reduce wall-clock time [4].

# Conclusion

Citation cartels threaten scientific integrity, yet existing detection methods require parameter tuning or rely on null models that can paradoxically ignore cartel signals in large journals. We introduce Citation Vortex Score, a parameter-free detector grounded in Hodge decomposition—a mathematical framework from algebraic topology. CVS measures the non-gradient (circulation) component of citation flow within journal communities, recognizing that cartels inject anomalous flow patterns into citation networks.

On synthetic data with ground-truth cartels, CVS achieves perfect discrimination (AUC-ROC=1.0) compared to reciprocity ratio (0.892) and degree-corrected null models (0.0). High temporal stability (mean Spearman ρ=0.939) across multi-year windows and robustness across community detection algorithms suggest the method captures stable structural properties. CVS requires no threshold tuning, no null model, and no training data—only basic sparse linear algebra and community detection from standard open-source tools (NetworkX, SciPy, OpenAlex).

Real-world validation on Clarivate's suppression lists remains future work, but the synthetic results and theoretical grounding are promising. More broadly, this work demonstrates that Hodge theory—long used in topology and ranking—offers a fresh lens for anomaly detection in networks. The same non-gradient-flow signature could apply to detecting wash-trading in cryptocurrency markets, coordinated bot networks in social media, or collusive behavior in supply chains. Hodge decomposition provides a general-purpose tool for identifying coordination in any flow network.

# References

[1] Kojaku, S., Livan, G., & Masuda, N. (2021). Detecting anomalous citation groups in journal networks. *Scientific Reports*, 11, 14524. https://doi.org/10.1038/s41598-021-93572-3

[2] Jiang, X., Lim, L.-H., Yao, Y., & Ye, Y. (2011). Statistical ranking and combinatorial Hodge theory. *Mathematical Programming*, 127(1), 203–244. https://doi.org/10.1007/s10107-010-0420-4

[3] Frantzen, M. & Schaub, M. T. (2025). HLSAD: Hodge Laplacian-based Simplicial Anomaly Detection. *KDD 2025*. https://arxiv.org/abs/2305.08869

[4] Priem, J., et al. (2023). OpenAlex: A fully-open index of scholarly metadata. ArXiv preprint. https://arxiv.org/abs/2307.15661

[5] Newman, M. E. J. (2003). The structure and function of complex networks. *SIAM Review*, 45(2), 167–256. https://doi.org/10.1137/S003614450342480

[6] Pérez-Esparrells, M. & López-Otín, C. (2016). Toward the discovery of citation cartels. *Frontiers in Physics*, 4, 8. https://doi.org/10.3389/fphy.2016.00008

[7] Lazaridou, M., Karachristos, T., & Vakali, A. (2020). Unsupervised anomaly detection in journal citation networks. In *Proceedings of the ACM/IEEE Joint Conference on Digital Libraries* (pp. 159–168).

[8] Lim, L.-H. (2024). Hodge Laplacians on graphs: A tutorial. *SIAM Review*, 66(3), 547–580. https://doi.org/10.1137/23M1582103

[9] Wei, R. K. J., Wee, J., Laurent, V., & Xia, K. (2022). Hodge theory-based biomolecular data analysis. *Scientific Reports*, 12, 8267. https://doi.org/10.1038/s41598-022-12877-z

[10] Sun, Y., Nagaraj, V., & Plis, S. M. (2024). Hodge decomposition for urban traffic flow analysis. *arXiv preprint arXiv:2509.17203*. https://doi.org/10.48550/arXiv.2509.17203

[11] Battiston, S., Clusaka, V., Estrada, E., et al. (2020). Structural measures for multiplex networks. *Physical Review E*, 113, 032306. https://doi.org/10.1103/PhysRevE.113.032306

[12] NetworkX (2024). NetworkX: Network analysis in Python. https://networkx.org

[13] SciPy (2024). SciPy sparse linear algebra documentation. https://docs.scipy.org/doc/scipy/reference/sparse.linalg.html

</current_paper>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

- [MAJOR] (evidence) The evaluation remains entirely synthetic. Despite having 17 Clarivate-verified cartel cases in the dataset artifact (art_oKw95zbMmpyR, cartel_ground_truth.json, covering 2013, 2018, 2024, 2025 suppression lists), the paper never evaluates CVS against real ground truth. The 15× synthetic boost is far above the 5–50× range mentioned for real cartels, and the 500-journal network with only 23 communities is a small, controlled setting. An AUC=1.0 on a 23-community synthetic problem with a strong injected signal does not constitute evidence that CVS works in practice.
  Action: Apply CVS to the real 96-journal OpenAlex network and compute overlap with the 17 Clarivate-suppressed journals. Even if the overlap is modest, report it honestly: partial real-data validation is far stronger than perfect synthetic performance. Use the same Jaccard ≥ 0.5 overlap criterion as CIDRE to enable a head-to-head comparison on real data.
- [MAJOR] (evidence) The CIDRE-lite AUC=0.0 result is mischaracterized as 'failure.' AUC=0.0 means perfect anti-correlation — the baseline ranks cartels dead last, which implies that inverting the score gives AUC=1.0. The paper says this 'reveals a critical insight' about degree-correction normalizing away cartel signals, but this interpretation is inconsistent with the reported Average Precision=0.220. If AUC=0.0 means all cartels are ranked last, then Average Precision for cartels should be near 0 (not 0.220). There is a numerical inconsistency that has not been resolved.
  Action: Recompute and reconcile CIDRE-lite metrics. If AUC truly equals 0.0, report that inverting the score gives AUC=1.0 and explain why (large, high-degree communities get the highest CIDRE-lite scores by design, and injected cartels are placed in high-degree communities). If there is a sign error in the implementation, fix it and report the corrected baseline. Either way, the current framing ('CIDRE-lite fails completely') is misleading.
- [MAJOR] (rigor) In-text citations [4] and [5] are used throughout to support experimental claims (e.g., 'AUC-ROC=1.000 [4, 5]', 'Spearman ρ=0.939 [4, 5]', 'O(V·E) time [4]') but bibliography [4] is the OpenAlex paper and [5] is Newman's 2003 complex networks review. These clearly do not support the cited claims. The in-text [4] and [5] appear to be artifact pipeline IDs that were never replaced with proper references. This affects essentially every experimental result in the paper.
  Action: Replace all in-text artifact citations [4] and [5] with proper bibliographic references or Supplementary Material pointers. Experimental results should cite the methods/experiments sections or dedicated supplementary material, not general-purpose papers about network science or OpenAlex. Do a full citation audit before resubmission.
- [MAJOR] (methodology) The name 'Citation Vortex Score' implies measurement of vorticity (curl component), but CVS measures combined non-gradient flow (curl + harmonic). This mismatch between name and implementation is still present despite the previous review flagging it. The limitations section now acknowledges this gap, but the introduction, contributions, and conclusion still use language implying curl-specific detection ('rotational patterns', 'Citation Vortex', 'circulation'). Harmonic flow captures globally cyclic but locally consistent patterns — this is not the same as cartel-like local circular citation. If harmonic flow dominates the residual, CVS will pick up on legitimate global citation cycles rather than coordinated cartel behavior.
  Action: Either: (a) implement B₂-based curl/harmonic separation to validate that curl (not harmonic) dominates CVS scores in cartel communities — this is the stronger scientific path and would make the contribution genuinely novel; or (b) rename to 'Citation Residual Score' and rewrite the theoretical framing to make honest claims about non-gradient flow detection without implying curl specificity. The name, abstract, and contributions section must all be internally consistent.
- [MINOR] (evidence) The Recall@Top-Decile metric shows conflicting values between the contributions summary (0.25, meaning 2.3 of 8 cartels in top 10%) and the error analysis discussion (all 8 cartels appear in top 35% of communities). These are not contradictory if 10% ≈ 2.3 communities, but the framing is confusing — a top decile of 23 communities is only 2.3 communities, making the metric nearly meaningless as stated.
  Action: Replace Recall@Top-Decile with Recall@K for K=5,10,15,20 communities, which is more meaningful at this dataset size. These values are already reported for precision; add the corresponding recall values to complete the picture.
- [MINOR] (scope) The claimed scalability to 7,000 journals with '<3 minutes' runtime is unsubstantiated by experiment. The evaluation is conducted on a 500-journal network. No runtime table or scaling curve is provided.
  Action: Add a brief scaling experiment: run CVS on networks of 100, 500, 1000, and 5000 journal nodes and report wall-clock time. This is a one-day implementation task that would convert a claim into evidence.
- [MINOR] (clarity) The relationship between the 96-journal real OpenAlex network (used in artifact art_hakO60eWu4mW) and the 500-journal synthetic network (used in the main experiments) is still not fully clear. The paper says the 500-journal network is 'built from OpenAlex data' but the exact construction procedure is not described — did the real 96-journal network seed the synthetic one, or are they independent?
  Action: Add one sentence in the Experiments section clarifying the relationship: 'The 500-journal network was constructed by augmenting real OpenAlex citation data with synthetic community structure, then injecting cartels. The 96-journal real network was used only for feature distribution analysis and not for cartel detection evaluation.'
</reviewer_feedback>



<task>
IMPORTANT: Your ONLY output is the revised hypothesis text. Do NOT run code, produce artifacts,
fix bugs, or attempt to address the evidence yourself — the next iteration of the invention loop
will generate fresh artifacts based on your revised hypothesis. Reflect and rewrite; nothing else.

Do NOT generate a completely new hypothesis. Take the current hypothesis and REVISE it
to incorporate new evidence. Keep the core idea — refine, narrow, or strengthen it.

1. Does the evidence support the hypothesis? Narrow or broaden scope as needed.
2. Which claims now have strong evidence? Which are still unsupported?
3. Should the hypothesis become more specific based on what we've learned?
4. If reviewer feedback is provided, address the critiques directly.

STABILITY IS OK: If progress is good and evidence supports the current direction, keep the
hypothesis similar or identical. Only make substantive changes when evidence clearly calls for
them — e.g., contradictory results, fundamental reviewer critiques, or findings that refine scope.

You must also classify two kinds of edges in the research trace:

(A) The H↔H edge — how does this revised hypothesis relate to the previous one?
    Set `relation_type` (Moulines's structuralist typology) to one of:
    - "evolution": refining specialised claims, same conceptual frame
    - "embedding": previous hypothesis is now a special case of a broader frame
    - "replacement": rejecting the previous frame entirely (Kuhnian shift)
    Set `relation_rationale` to a brief justification (≤120 chars).

(B) The A↔A edges — for each artifact created THIS iteration, classify each of its
    `in_dependencies` (predecessor → dependent) using MultiCite's citation-function
    typology (Lauscher et al., NAACL 2022) — emit one entry in `artifact_relations`
    per (predecessor, dependent) pair. Predecessors are ALWAYS artifacts from EARLIER
    iterations — artifacts within one iteration run in parallel and cannot depend on
    each other, so never emit a relation between two same-iteration artifacts (it
    will be dropped):
    - "background": predecessor is treated as background context
    - "motivation": predecessor motivated this artifact's research
    - "uses": this artifact uses the predecessor's data, method, or output
    - "extends": this artifact extends the predecessor
    - "similarities": this artifact's results agree with the predecessor's
    - "differences": this artifact's results disagree with the predecessor's
    Each `relation_rationale` must be ≤120 characters.

Output the COMPLETE revised hypothesis (with the H↔H relation fields) AND the full
list of A↔A `artifact_relations` for this iteration's new artifacts.
</task><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ArtifactRelation": {
      "description": "One typed A\u2194A edge between a dependent artifact and one of its in_dependencies.\n\nMultiCite citation-function typology (Lauscher et al., NAACL 2022),\nreduced to 6 plain-English types.",
      "properties": {
        "from_id": {
          "description": "ID of the predecessor artifact (the one being depended on)",
          "title": "From Id",
          "type": "string"
        },
        "to_id": {
          "description": "ID of the dependent artifact (the new artifact this iteration)",
          "title": "To Id",
          "type": "string"
        },
        "relation_type": {
          "description": "MultiCite citation-function type for the predecessor\u2192dependent edge: 'background' \u2014 predecessor is treated as background context; 'motivation' \u2014 predecessor motivated this artifact's research; 'uses' \u2014 this artifact uses the predecessor's data, method, or output; 'extends' \u2014 this artifact extends the predecessor; 'similarities' \u2014 this artifact's results agree with the predecessor's; 'differences' \u2014 this artifact's results disagree with the predecessor's.",
          "enum": [
            "background",
            "motivation",
            "uses",
            "extends",
            "similarities",
            "differences"
          ],
          "title": "Relation Type",
          "type": "string"
        },
        "relation_rationale": {
          "description": "Brief rationale for this relation type (one short line, max 120 characters).",
          "maxLength": 120,
          "title": "Relation Rationale",
          "type": "string"
        }
      },
      "required": [
        "from_id",
        "to_id",
        "relation_type",
        "relation_rationale"
      ],
      "title": "ArtifactRelation",
      "type": "object"
    }
  },
  "description": "Revised hypothesis after reviewing iteration results.\n\nOutput matches the hypothesis dict structure so it can replace the\noriginal hypothesis in subsequent iterations.",
  "properties": {
    "title": {
      "description": "Revised hypothesis title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); may be unchanged if still accurate.",
      "title": "Title",
      "type": "string"
    },
    "hypothesis": {
      "description": "Revised hypothesis statement \u2014 what we now believe based on evidence",
      "title": "Hypothesis",
      "type": "string"
    },
    "relation_rationale": {
      "description": "Brief rationale for the H\u2194H revision type (one short line, max 120 characters).",
      "maxLength": 120,
      "title": "Relation Rationale",
      "type": "string"
    },
    "confidence_delta": {
      "description": "How confidence changed: 'increased', 'decreased', or 'unchanged'",
      "title": "Confidence Delta",
      "type": "string"
    },
    "key_changes": {
      "description": "Bullet list of specific changes made to the hypothesis",
      "items": {
        "type": "string"
      },
      "title": "Key Changes",
      "type": "array"
    },
    "relation_type": {
      "description": "Moulines's structuralist typology of this hypothesis revision: 'evolution' \u2014 refining specialised claims while keeping the same conceptual frame; 'embedding' \u2014 the previous hypothesis is now a special case of a broader frame; 'replacement' \u2014 rejecting the previous frame entirely (incommensurable, Kuhnian revolution).",
      "enum": [
        "evolution",
        "embedding",
        "replacement"
      ],
      "title": "Relation Type",
      "type": "string"
    },
    "artifact_relations": {
      "description": "Typed A\u2194A edges for this iteration's new artifacts. Emit one entry per (predecessor \u2192 dependent) edge for every in_dependency on each artifact produced this iteration.",
      "items": {
        "$ref": "#/$defs/ArtifactRelation"
      },
      "title": "Artifact Relations",
      "type": "array"
    }
  },
  "required": [
    "title",
    "hypothesis",
    "relation_rationale",
    "confidence_delta",
    "key_changes",
    "relation_type"
  ],
  "title": "RevisedHypothesis",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-07-09 02:19:19 UTC

```
Propose a simple, novel graph-based method for detecting citation cartels in academic networks and validate it.
```
