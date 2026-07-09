# gen_strat_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_strat`
> Run: `run_HMncsxsr6ltD` — Hodge Decomposition for Citation Cartel Detection
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_strat_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-07-09 01:36:02 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A strategy planner (Step 3.1: GEN_STRAT in the invention loop)

Each iteration of the invention loop runs: GEN_STRAT → GEN_PLAN → GEN_ART → GEN_PAPER_TEXT → REVIEW_PAPER → UPD_HYPO
Artifact types: RESEARCH (web search), EXPERIMENT (code), DATASET (data collection), EVALUATION (metrics), PROOF (Lean 4)
State persists across iterations: strategies, plans, artifacts, paper_texts (read from the run tree)

You received the hypothesis, iteration status (current + remaining), previous iteration's strategies, available artifact types, existing artifacts, and reviewer feedback.
Your strategy governs THIS iteration only. You define what artifacts to create NOW.

Focused strategy → efficient progress. Scattered strategy → wasted iteration.
</your_role>
</ai_inventor_context>

<available_resources>
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

<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>
</available_resources>

<time_budgets>

Each artifact executor has a fixed time budget (including writing code, debugging, testing, and fixing errors):

- research: 3h
- dataset: 6h
- experiment: 6h
- evaluation: 3h
- proof: 3h

</time_budgets>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<research_methodology>
Think like a researcher planning a study for a top venue.

- All strategies run in parallel and their artifacts combine into one pool. Together they must build toward a publishable paper — each strategy contributes a distinct, necessary piece. No strategy should be a standalone island.
- Ask yourself: what would a reviewer need to see? Proper baselines, controlled comparisons, ablations that isolate what matters. Plan artifacts that preempt reviewer objections.
- Depth over breadth. One well-designed experiment with proper controls beats five shallow ones.
- Match your evaluation to your claims. Measure what the hypothesis actually asserts.
- When results are weak or partial, vary the approach before writing it off. One failed method doesn't falsify the hypothesis.
- If iterations remain, think about what the NEXT iteration will need. Leave useful building blocks — datasets, baselines, preliminary results — that future strategies can build on, refine, or compare against.
</research_methodology>

<principles>
1. FOCUS ON NOVELTY - every strategy must lead to a genuinely novel contribution
2. MAXIMIZE PARALLELIZATION - all artifacts in your strategy run in parallel
3. BUILD ON EXISTING WORK - use completed artifacts from previous iterations, learn from failures
4. ITERATE ON THE METHOD - a negative result is about the approach, not the hypothesis. Try different methods, parameters, data, or formulations within the hypothesis bounds.
5. DIAGNOSE BEFORE DECIDING - before each iteration, review what worked, what didn't, and why. Use that to choose what to try next. Gaps are action items, not conclusions.
6. SET DEPENDENCIES WISELY - depends_on is a list of {id, label} objects referencing existing artifacts; each label is a short free-text type (a word or two, e.g. "dataset", "validates", "extends") that tags how the dep is used
7. PLAN FOR DEPENDENCIES - if an artifact depends on another (e.g. experiments need datasets), ensure prerequisites exist first or plan them this iteration for the next
</principles>

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

<hypothesis>
Your strategy should advance this hypothesis.

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
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. Use it for study design, proper baselines, and the evaluation/validity norms this field demands.

- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
</available_domain_handbooks>

<iteration_status>
Current iteration: 2 of 2
Remaining (including this one): 1
</iteration_status>

<previous_strategies>
Strategies from the PREVIOUS iteration. You can CONTINUE these directions,
ADAPT based on what worked and what didn't in the artifacts produced, or PIVOT if results suggest a better path.

--- Strategy 1 ---
kind: strategy
id: gen_strat_1_idx1
title: Establish CVS and Validate Against Baselines
objective: >-
  Implement the Citation Vortex Score method using Hodge decomposition on real journal citation data and validate that it
  outperforms reciprocity ratio and CIDRE-lite baselines on the Clarivate suppression ground truth.
rationale: >-
  The CVS hypothesis hinges on a core claim: Hodge decomposition extracts a curl-based signal that captures cartel structure
  better than parameter-tuned baselines. This iteration moves from theory to empirical validation. We implement CVS on OpenAlex
  journal citation data (a large, real network spanning 250M+ papers) and directly compare precision@K and AUC-ROC against
  CIDRE-lite and reciprocity ratio using Clarivate's verified suppressed journals as ground truth. Success confirms the mechanism;
  failure provides diagnostic signal (e.g., curl is uncorrelated with cartels, or Louvain communities misalign with ground-truth
  groups) to guide iteration 2's refinements.
artifact_directions:
- id: research_iter1_dir1
  type: research
  objective: >-
    Understand Hodge decomposition applied to networks, CIDRE's dcSBM methodology, and locate the Clarivate journal suppression
    ground truth.
  approach: >-
    Search for HodgeRank papers (Jiang et al., Mathematical Programming 2011) and graph decomposition theory to understand
    sparse linear algebra formulation and implementation patterns. Fetch the CIDRE paper (Sinatra & Rosvall, Scientific Reports
    2021) to understand how dcSBM excess citation fractions are computed and what parameters control it. Search for papers
    on reciprocal citation detection and prior cartel thresholds. Locate and document Clarivate's suppressed journals list
    (expect 46+ confirmed pairs/groups) and understand its format and reliability.
  depends_on: []
- id: dataset_iter1_dir2
  type: dataset
  objective: >-
    Build a journal-level directed weighted citation network from OpenAlex covering 2015–2022, structured and validated for
    Hodge decomposition.
  approach: >-
    Query the OpenAlex REST API (free, covers ~250M papers) to extract journal-to-journal citations: for each distinct pair
    of journals (i, j), count the number of papers published in journal i that cite papers published in journal j, aggregated
    across 2015–2022. Construct a directed weighted graph where nodes = journals, edge weights = citation counts. Output as
    JSON: {"journal_pairs": [{"source_journal_id", "target_journal_id", "total_citations"}], "journal_metadata": [{"journal_id",
    "name", "issn", "total_papers_published"}]}. Validate graph properties: sparsity (expected density < 0.01), node count
    (~5,000–15,000 journals), and hierarchical structure on average. Generate summary statistics (density, number of edges,
    largest components).
  depends_on: []
- id: experiment_iter1_dir3
  type: experiment
  objective: >-
    Implement CVS via Hodge decomposition, implement CIDRE-lite and reciprocity ratio baselines, and evaluate all three methods
    against Clarivate ground truth using precision@K and AUC-ROC.
  approach: >-
    Load the weighted citation graph from the DATASET. For Hodge decomposition: construct the incidence matrix B1 (nodes ×
    edges) and boundary matrix B2 (edges × triangles); solve the least-squares system min||B1 f_grad - f|| using scipy.sparse.linalg.lsqr
    to extract the gradient component; residual represents curl + harmonic components. Detect journal subgroups using Louvain
    community detection (networkx or igraph). For each subgroup S, compute CVS(S) = (Σ_{e∈S} ||f_curl(e)||²) / (Σ_{e∈S} ||f(e)||²).
    Implement baselines: (1) Reciprocity Ratio = average of citations_ij / citations_ji for all journal pairs in S; (2) CIDRE-lite
    = excess citation fraction relative to uniform null model (without full dcSBM fitting). Rank all subgroups descending
    by each scoring method. Obtain Clarivate suppressed journals list (ground truth). For each method, compute precision@5,
    precision@10, precision@20, and AUC-ROC by treating the subgroup rank as a continuous score. Report tabular comparison.
    Diagnose the result: if CVS > baselines, confirm the hypothesis; if CVS ≈ reciprocity ratio, conclude Hodge decomposition
    adds no information; if CVS < baselines, the curl model may not describe cartel structure.
  depends_on: []
expected_outcome: >-
  After this iteration: (1) a validated, reusable OpenAlex citation network (2015–2022) with ~5,000–15,000 journals structured
  for analysis; (2) a complete, reproducible Python implementation of Hodge decomposition, subgroup detection, and CVS scoring;
  (3) empirical comparison tables (precision@K, AUC-ROC) showing how CVS, reciprocity ratio, and CIDRE-lite rank on Clarivate
  ground truth. **If successful**: CVS achieves ≥50% recall in the top decile of subgroups and precision@20 ≥ baselines, confirming
  that curl energy is a meaningful cartel signal and validating the core hypothesis. This provides a foundation for iteration
  2's ablations (temporal robustness across years, gradient-only variants, sensitivity to Louvain parameters). **If unsuccessful**:
  we diagnose whether failure is due to (a) curl being orthogonal to cartel structure (hypothesis wrong), (b) Louvain partitions
  misaligning with ground-truth groups (method wrong), (c) insufficient OpenAlex data resolution, or (d) confounding factors,
  each suggesting a different refinement for iteration 2.
summary: >-
  Validate the core CVS hypothesis by implementing Hodge decomposition on real OpenAlex citation data (2015–2022) and comparing
  precision@K and AUC-ROC against reciprocity ratio and CIDRE-lite baselines using Clarivate-suppressed journals as ground
  truth.
</previous_strategies>

<dependency_rules>
- depends_on is a list of objects {id, label} — each entry references an existing artifact and tags how it is being used
- "id" can ONLY reference IDs from <existing_artifacts> — never IDs you are proposing (all new artifacts run in parallel)
- "label" is a SHORT free-text type label (a word or two, NOT a sentence) describing what role the dep plays — e.g. "dataset", "validates", "extends", "supersedes". Required on every dep.
- Setting depends_on provides the dependency's out_dependency_files to your artifact at execution time
- If no suitable existing artifacts exist, use empty depends_on
- New artifact IDs are assigned by the system after submission — do not invent IDs for your proposed artifacts
</dependency_rules>

<available_artifact_types>
Artifact types you can plan. Use this to choose the right types for your strategy objectives.

<artifact_types>
RESEARCH
Web research to answer key questions — like a researcher making decisions.
Runtime: LLM Agent, no code execution.
Tools: the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text).
Capabilities: Find, synthesize, and compare information across sources; survey SOTA and best practices.
Deps: REQUIRED none | OPTIONAL other RESEARCH to build on prior findings

EXPERIMENT
Run code to test hypotheses, implement methods, and collect empirical results.
Runtime: Python 3.12, UV (any pip package), isolated workspace, gradual scaling (mini → full data).
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Implement and run any code-based experiment, compare method vs baselines.
Deps: REQUIRED at least one DATASET | OPTIONAL RESEARCH for methodology guidance

DATASET
Collect, prepare, and merge datasets for experiments and analysis.
Runtime: Python 3.12, UV, isolated workspace.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-hf-datasets (HuggingFace Hub — ML datasets, many UCI/OpenML/Kaggle mirrors), aii-owid-datasets (Our World in Data — global statistics), aii-json (schema validation). Also any Python source (sklearn.datasets, openml, direct URLs, APIs) — must verify within 300MB limit.
Capabilities: Search, acquire, transform, combine, and standardize data from any available source.
Deps: REQUIRED none | OPTIONAL RESEARCH for guidance on what data to collect

EVALUATION
Evaluate experiment results with metrics, statistical analysis, and validity checks.
Runtime: Python 3.12, UV (any evaluation library), isolated workspace, gradual scaling matching experiment.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Compute any quantitative metrics and statistical tests, analyze validity and robustness.
Deps: REQUIRED at least one EXPERIMENT | OPTIONAL DATASET if reference data needed

PROOF
Formally prove mathematical statements in Lean 4 with automated iteration.
Runtime: LLM agent with Lean 4 compiler feedback loop.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-lean (proof verification, Mathlib search, tactics: ring, linarith, nlinarith, omega, simp, etc.)
Capabilities: Formally verify properties and inequalities, iterative proof development, lemma decomposition.
Deps: REQUIRED none | OPTIONAL RESEARCH for mathematical background
</artifact_types>
</available_artifact_types>

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

RESEARCH executor scope:
  Output: research_out.json with {answer, sources, follow_up_questions} + research_report.md
  DOES: Web research — search, read, synthesize information from papers/docs/APIs into a structured report
  DOES NOT: Run code, download files, execute scripts, compute anything — no shell/Python access
  Use for literature surveys, API documentation, technical specifications — pure information gathering

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results

DATASET executor scope:
  Output: data_out.json with rows of {input, output, metadata_fold, ...} — raw data only, no derived computations
  DOES: Download/generate datasets, analyze candidates to pick the best ones, standardize to JSON schema (features, labels, folds, metadata), validate schema, split into full/mini/preview
  DOES NOT: Run experiments, train models, compute derived statistics (PID/MI/correlations/synergy matrices) as final output
  If you need to COMPUTE something from data (synergy matrices, MI scores, timing benchmarks), use an EXPERIMENT artifact instead

EVALUATION executor scope:
  Output: eval_out.json with evaluation results
  DOES: Any evaluation of experiment results — metrics, statistical tests, ablations, comparisons, visualizations, robustness checks, error analysis, etc.
  DOES NOT: Implement new methods (use EXPERIMENT), collect data (use DATASET)
  This is for analyzing experiment outputs from any angle

PROOF executor scope:
  Output: Lean 4 proof files (.lean) with verified theorems
  DOES: Write and verify Lean 4 formal proofs with Mathlib, iterative compilation
  DOES NOT: Run Python experiments, collect data, do empirical analysis
  Use only when formal mathematical guarantees are needed
</artifact_executor_scope>

<artifact_planning_rules>
RESEARCH: Plan early — findings guide dataset selection, experiment design, and methodology.
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
DATASET:
- Plan for REAL third-party datasets (HuggingFace, Kaggle, direct-download URLs) — downloadable within time and size constraints
- Describe dataset criteria (domain, size, format) — executors find exact sources, but you can suggest candidates or search directions
- ALWAYS prefer real datasets over synthetic. Synthetic is a LAST RESORT only when no suitable real data exists
EVALUATION: Must depend on at least one EXPERIMENT. Focus on statistical rigor and validity checks.
PROOF: Use only when the hypothesis requires formal mathematical guarantees. Lean 4 + Mathlib.
</artifact_planning_rules>

<existing_artifacts>
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
out_dependency_files:
  file_list:
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
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
</existing_artifacts>

<current_paper>
The current paper draft — represents the research story so far.

Use this to understand what's working, what's not, and what gaps remain.
Gaps and weak results signal what to try differently — not what to conclude.

# Introduction

Academic citation networks form the foundation of scientific reputation systems. Journal Impact Factor (JIF)—the average number of citations a journal receives in a given year—directly influences funding allocation, researcher hiring, and promotion decisions [1]. This creates perverse incentives for journals to artificially inflate their citations through citation cartels: organized groups of journals coordinating excessive mutual citation exchanges to boost collective impact factors [1, 2, 3].

Citation cartels are not merely unethical; they distort the scientific record. When journals cite each other at artificially high rates, they crowd out citations to foundational work, misrepresent research importance, and redirect both reader attention and funding toward a narrow set of journals [2]. Clarivate, the authority publishing Journal Citation Reports, has suspended 33 journals (0.27% of ~12,000 tracked journals) in 2020 alone for excessive self-citation and citation stacking [3]. By 2025, that number had grown to 20 journals suspended per year [2], suggesting the problem is widespread and accelerating.

The challenge is detection. Existing methods fall into two categories, each with critical limitations. First, threshold-based approaches—identifying journal pairs with excessive mutual citations—ignore network context and miss multi-step cycles (A→B→C→A) that characterize sophisticated cartels [1]. Second, statistical null-model approaches like the degree-corrected stochastic block model (CIDRE) explicitly expect high mutual citations among large, active journals, potentially normalizing away the cartel signal [1]. Neither method is parameter-free or fully transparent.

We propose a fundamentally different approach: Citation Vortex Score (CVS), grounded in Hodge decomposition from algebraic topology. The mathematical insight is that flow on any directed graph decomposes uniquely into three orthogonal components [4]: (1) gradient flow—acyclic hierarchical citation patterns reflecting legitimate prestige hierarchies; (2) curl flow—locally rotational patterns reflecting citation cartels; and (3) harmonic flow—globally cyclic but locally consistent patterns, rare in citation systems. By measuring the ratio of curl energy to total energy within journal communities, we obtain a parameter-free, interpretable cartel score that requires no tuning and no null model.

This is a cross-domain transfer from mathematical physics and combinatorial topology. HodgeRank, a prior work applying Hodge decomposition to ranking problems, showed that ranking inconsistency manifests as curl flow [4]. The insight—that rotational flow in a network encodes coordination or anomaly—applies equally to citation behavior. We adapt this machinery to output a per-subgroup anomaly score rather than global ranking quality, introducing novelty both methodologically and in application domain.

## Summary of Contributions

- **Theoretical**: We establish that citation cartel structure—mutual reinforcement loops—corresponds to non-zero curl components in Hodge decomposition of citation flow networks. Gradient-only flow represents healthy hierarchical citation; curl flow is the mathematical signature of coordination [ARTIFACT:art_Rkxm3YsFRtot].
- **Methodological**: We introduce Citation Vortex Score (CVS), a closed-form parameter-free detector requiring no null model or threshold tuning. CVS(S) = ||f_curl(S)||² / ||f(S)||² for subgroup S, computed via sparse linear algebra in O(V·E) time [ARTIFACT:art_rxHyxG4rT2Xw].
- **Empirical**: On synthetic data with ground-truth cartels, CVS achieves AUC-ROC=1.0 vs. AUC-ROC=0.892 for reciprocity ratio and 0.0 for degree-corrected baselines, demonstrating that curl flow captures cartel signal independent of node degree [ARTIFACT:art_rxHyxG4rT2Xw].
- **Practical**: CVS shows high temporal stability (mean Spearman ρ=0.939 across multi-year windows) and integrates seamlessly with open-source tools (OpenAlex, NetworkX, SciPy) for large-scale journal network analysis [ARTIFACT:art_rxHyxG4rT2Xw].

# Related Work

## Citation Cartel Detection

The seminal work on cartel detection is CIDRE (Detecting Citation Cartels in Journal Networks) by Kojaku, Livan, and Masuda [2, 5]. CIDRE uses a degree-corrected stochastic block model (dcSBM) as a null model and identifies journal groups with excess citations relative to expected values under dcSBM. Empirically, CIDRE detected 12 of 22 JCR-suppressed cartel groups (54.5% recall), with 8 groups showing Jaccard overlap ≥0.5 with suppressed journals (67% high-confidence matches) [2]. CIDRE also demonstrated predictive power, identifying 10 groups 1–2 years before Clarivate suspension [2]. However, CIDRE requires careful choice of null model parameters and threshold selection for group identification.

Earlier work by Pérez-Esparrells and López-Otín used semantic web tools and SPARQL queries on citation count graphs, requiring arbitrary threshold choices [6]. More recent anomaly detection approaches, such as the method by Lazaridou et al., use graph autoencoders and node embedding reconstruction error, but this black-box approach lacks interpretability and requires labeled training data [7].

CVS differs fundamentally from all prior work: it requires no null model, no threshold, and no training data. Instead, it directly decomposes observed citation flow into gradient vs. curl components via linear algebra, providing an interpretable geometric signal grounded in Hodge theory.

## Hodge Theory and Network Flow

Hodge decomposition originates in differential geometry but has been adapted to discrete graphs [4, 8]. The foundational work is HodgeRank by Jiang et al., which applies Hodge decomposition to ranking data (e.g., movie ratings) [4]. HodgeRank decomposes pairwise ranking data into gradient flow (consistent with a global ranking) and residual (ranking inconsistency). The gradient component induces a consistent ranking; the curl component quantifies inconsistency [4].

Recent applications demonstrate Hodge theory's generality. Wei et al. applied Hodge decomposition to biomolecular networks to identify functional modules [9]. Sun et al. used Hodge decomposition to separate directional traffic flow (gradient) from circulation patterns (curl) in urban traffic networks, showing that curl identifies congestion bottlenecks [10]. These diverse applications—ranking, biology, traffic—suggest that curl flow is a general marker of anomalous or coordinated behavior.

Our contribution is to recognize that citation cartel behavior—the signature of coordinated journals—manifests as curl flow in the citation network. This is not an obvious connection: the mathematical structures are similar (both decompose flow on graphs), but the domain interpretation is novel.

## Network Anomaly Detection

Broader anomaly detection literature includes community detection algorithms (Louvain, Leiden, Infomap), which identify clusters in networks [11]. However, CIDRE analysis showed that standard community detection finds 3× more groups than CIDRE but with zero matches to JCR suppressions [2], indicating that legitimate research communities confound pure graph clustering. CVS addresses this by focusing on the curl/rotational structure, not just community density.

# Methods

## Problem Formulation

Let G = (V, E) be a directed weighted journal citation network where V = journals and edge weight w(i → j) = annual citations from journal i to journal j [ARTIFACT:art_oKw95zbMmpyR]. We represent citation flow as a 1-chain f : E → ℝ, mapping each edge to its citation count. A subgroup S ⊆ V induces a subflow f|_S consisting of all edges within S.

The problem: for each candidate subgroup S, compute a score indicating whether the citations within S are predominantly circular (cartels) or acyclic (legitimate hierarchies).

## Hodge Decomposition

Hodge theorem states that any flow f on G decomposes uniquely into three orthogonal components [4, 8]:

**f = f_grad + f_curl + f_harm**

where:
- **f_grad** (gradient component): acyclic, irrotational flow consistent with a global node potential φ, i.e., f_grad(i→j) = φ(j) - φ(i) for some φ : V → ℝ.
- **f_curl** (curl component): divergence-free, locally cyclic flow forming closed loops around triangles in the graph.
- **f_harm** (harmonic component): globally cyclic, locally consistent flow satisfying both closure and coclosure conditions.

### Incidence and Boundary Matrices

The decomposition is formalized using the incidence matrix B₁ (V × E dimensions):
- B₁(v, e) = +1 if v is the head of edge e
- B₁(v, e) = −1 if v is the tail of edge e
- B₁(v, e) = 0 otherwise

The gradient component satisfies f_grad = B₁ᵀφ for some potential φ. The residual r = f - f_grad contains curl + harmonic components [4, 8].

### Gradient Extraction via Least-Squares

To extract f_grad, we solve the least-squares problem:

φ* = argmin_φ ||f - B₁ᵀφ||²

This is equivalent to solving the normal equation (B₁B₁ᵀ)φ = B₁f. Using sparse least-squares solver scipy.sparse.linalg.lsqr, we efficiently compute φ* even for large networks (V, E in thousands) in O(V·E) time [ARTIFACT:art_rxHyxG4rT2Xw, 11].

The gradient component is then f_grad = B₁ᵀφ*, and the residual f_residual = f - f_grad contains the curl signal [4].

## Citation Vortex Score (CVS)

For a candidate subgroup S ⊆ V, define the Citation Vortex Score as:

**CVS(S) = ||f_residual(S)||² / ||f(S)||²**

where:
- f(S) = sum of squared flow magnitudes on edges within S
- f_residual(S) = sum of squared residual magnitudes on edges within S

CVS is a ratio in [0, 1]:
- **CVS → 0**: Flow is predominantly acyclic (gradient-driven), indicating a legitimate research community.
- **CVS → 1**: Flow is predominantly non-gradient (curl + harmonic), indicating rotational/circular patterns characteristic of citation cartels.

CVS requires no tuning: the only "parameter" is the choice of subgroups S, which we obtain from community detection (Louvain algorithm on undirected projection of G). All subsequent computation is deterministic [ARTIFACT:art_rxHyxG4rT2Xw].

## Baseline Methods

We compare CVS against two baselines:

### Reciprocity Ratio
For each subgroup S, compute the pairwise reciprocity as the mean of min(c_ij, c_ji) / max(c_ij, c_ji) across all journal pairs (i, j) ∈ S [ARTIFACT:art_rxHyxG4rT2Xw]. High ratios indicate balanced mutual citation. This baseline captures only pairwise symmetry and ignores network structure, multi-step cycles, and journal size effects.

### CIDRE-lite (Degree-Corrected Null Model)
For each subgroup S, compute excess citation fraction: (observed - expected_under_dcSBM) / expected_under_dcSBM, where expected values come from a degree-corrected stochastic block model [2]. This is a simplified version of the full CIDRE algorithm without tuned threshold selection.

# Experiments

## Dataset and Experimental Setup

We construct a citation network from OpenAlex data covering 2015–2022 [12]. The dataset includes 96 high-impact journals (top ~100 by global citation count) with 888 directed edges representing annual cross-journal citation counts, aggregated from 2,924 sampled papers [ARTIFACT:art_oKw95zbMmpyR]. The network is dense (sparsity 0.097), reflecting expected high connectivity among top-tier journals. Total citation count: 2,644 edges [ARTIFACT:art_oKw95zbMmpyR].

To create ground-truth labels, we construct a synthetic dataset by (1) starting with the 500-journal OpenAlex network with 25 communities of ~20 journals each; (2) injecting 8 synthetic citation cartels of 4 journals each with a 15× boost to mutual citation rates as ground truth; (3) running Louvain community detection to obtain 23 candidate subgroups [ARTIFACT:art_rxHyxG4rT2Xw]. This yields an imbalanced dataset: 8 cartel communities, 15 legitimate communities.

We evaluate all three methods (CVS, reciprocity ratio, CIDRE-lite) on the same 23 communities.

## Results

### Primary Metrics: Precision@K and AUC-ROC

Figure 1 shows the ranking performance of all three methods.

[FIGURE:fig_ranking_auc]

CVS achieves perfect discrimination on the synthetic dataset [ARTIFACT:art_rxHyxG4rT2Xw]:
- **AUC-ROC = 1.000** (perfect ranking of cartels vs. legitimate groups)
- **Precision@5 = 1.0** (all top 5 ranked groups are cartels)
- **Precision@10 = 0.8** (8 of 10 top groups are cartels)
- **Average Precision (AP) = 1.0**
- **Top-Decile Precision = 1.0** (all groups in top 10% are cartels)

Reciprocity Ratio achieves moderate performance [ARTIFACT:art_rxHyxG4rT2Xw]:
- **AUC-ROC = 0.892**
- **Precision@5 = 1.0** (all top 5 are cartels)
- **Precision@10 = 0.6** (6 of 10 top are cartels)
- **AP = 0.865**

CIDRE-lite fails completely [ARTIFACT:art_rxHyxG4rT2Xw]:
- **AUC-ROC = 0.0** (anti-correlated with cartel labels)
- **Precision@5 = 0.0** (no cartels in top 5)
- **Precision@10 = 0.0** (no cartels in top 10)
- **AP = 0.220**

The failure of CIDRE-lite reveals a critical insight: degree-corrected null models assume that high mutual citation is expected among large, active journals (cartel groups). By design, dcSBM normalizes away the signal, making it worse than random. CVS avoids this trap by decomposing flow directly, independent of degree.

### Temporal Stability

We test whether CVS rankings remain stable across non-overlapping year windows (2015–2017, 2017–2019, 2019–2021) [ARTIFACT:art_rxHyxG4rT2Xw]. Figure 2 shows strong temporal consistency:

[FIGURE:fig_temporal_stability]

- **2015–2017 vs. 2017–2019**: Spearman ρ = 0.919
- **2017–2019 vs. 2019–2021**: Spearman ρ = 0.937
- **2015–2017 vs. 2019–2021**: Spearman ρ = 0.904
- **Mean Spearman ρ = 0.939**

This high correlation (ρ > 0.9) indicates that CVS rankings are robust across multi-year windows, suggesting the method captures stable structural properties of the network rather than year-specific noise.

### Independence from Reciprocity Baseline

To confirm that CVS captures novel signal beyond pairwise reciprocity, we compute Spearman rank correlation between CVS and reciprocity ratio scores across all 23 communities:

**Spearman ρ(CVS, Reciprocity) = 0.65**

A correlation of 0.65 indicates moderate but non-trivial dependence. CVS and reciprocity rank communities differently: CVS identifies cartels via rotational structure, while reciprocity only counts bidirectional edges. This difference is crucial for cartels using multi-step cycles.

## Diagnostic: Why CIDRE-lite Fails

The failure of degree-corrected null models highlights a fundamental limitation. In the synthetic dataset, injected cartels are high-degree subgroups (many edges, many citations). The dcSBM null model explicitly expects high within-community citation rates for high-degree communities, normalizing away the cartel signal. Figure 3 illustrates this:

[FIGURE:fig_cidre_failure]

For each community, we plot (1) observed within-community citation count vs. (2) expected count under dcSBM. Legitimate communities (red) scatter around the diagonal (observed ≈ expected). Cartel communities (blue) are far above the diagonal (observed >> expected). However, because cartels are high-degree, the dcSBM *expectation* is also high, making the excess fraction small, even though they are anomalous in absolute terms.

CVS avoids this by measuring curl flow directly: regardless of degree, circular flow indicates anomaly.

# Discussion

## Limitations

1. **Synthetic Ground Truth**: Our evaluation uses injected synthetic cartels rather than real Clarivate-suppressed groups. While the synthetic setup allows for controlled ground truth, the 15× boost may not reflect realistic cartel behavior. Real cartels may employ subtler strategies, and CVS performance on actual JCR data remains to be validated.

2. **Subgroup Sensitivity**: CVS depends on the choice of subgroups S. We use Louvain community detection, which is heuristic-based. Different community detection algorithms (Leiden, Infomap) may identify different subgroups, potentially altering CVS rankings. A systematic ablation across multiple community detection methods would strengthen robustness claims.

3. **Field-Specific Citation Density**: Legitimate research communities in specialized fields (rare disease journals, regional studies) naturally have high reciprocal citation rates. Curl energy in these fields may be legitimately high, leading to false positives. Field-normalized baselines would be valuable but are not yet implemented.

4. **Harmonic Component**: The residual f_residual = f - f_grad contains both curl and harmonic components. We treat them together as "non-gradient flow," but harmonic flow (globally cyclic, locally consistent) may have different interpretation. Separating curl from harmonic via triangle boundary operators (B₂) could refine the method.

## Comparison to CIDRE

CIDRE achieved 54.5% recall on JCR-suppressed groups, which is the current state-of-the-art. CVS's perfect performance on synthetic data suggests it could potentially exceed CIDRE on real data, but real validation is essential. Key differences:

- **Transparency**: CVS has no tunable parameters; CIDRE requires threshold selection. This makes CVS easier to audit and deploy.
- **Robustness**: CVS's independence from degree assumptions makes it robust to journal size variations; CIDRE's dcSBM can miss large-scale cartels that the null model expects.
- **Interpretability**: CVS has geometric meaning (curl flow = rotational patterns); CIDRE's excess citation fraction is more opaque.

However, CIDRE's full algorithm includes threshold-tuned subgroup extraction, which we simplified to Louvain. A fair comparison would implement full CIDRE with its internal group selection.

## Future Work

1. **Real Validation**: Evaluate CVS against Clarivate's full suppression list (46+ journal pairs) to confirm performance on real cartels.
2. **Field Normalization**: Develop discipline-specific curl baselines (e.g., expected curl in high-collaboration fields) to reduce false positives.
3. **Temporal Analysis**: Apply CVS retrospectively to multi-year windows to track cartel formation and dissolution over time.
4. **Harmonic Decomposition**: Implement explicit separation of harmonic and curl components using boundary operators for refined interpretation.
5. **Scalability**: Test CVS on the full OpenAlex network (7,000+ journals) to confirm O(V·E) scaling.

# Conclusion

Citation cartels threaten scientific integrity, yet existing detection methods require parameter tuning or rely on null models that can paradoxically ignore cartel signals. We introduce Citation Vortex Score, a parameter-free detector grounded in Hodge decomposition—a mathematical framework from algebraic topology. CVS measures the rotational (curl) component of citation flow within journal communities, recognizing that cartels are flow vortices in the citation network.

On synthetic data with ground-truth cartels, CVS achieves perfect discrimination (AUC-ROC=1.0) compared to reciprocity ratio (0.892) and degree-corrected null models (0.0). High temporal stability (Spearman ρ=0.939) across multi-year windows suggests robustness. CVS requires no threshold tuning, no null model, and no training data—only basic sparse linear algebra and community detection, both available in standard open-source tools.

The method's real-world validation on Clarivate's suppression lists remains future work, but the synthetic results are promising. More broadly, this work demonstrates that Hodge theory—long used in topology and ranking—offers a fresh lens for anomaly detection in networks. The same rotational-flow signature could apply to detecting wash-trading in cryptocurrency markets, coordinated bot networks in social media, or collusive behavior in economic supply chains.

## References

[1] Jiang, X., Lim, L., Yao, Y., & Ye, Y. (2011). Statistical ranking and combinatorial Hodge theory. Mathematical Programming, 127(1), 203–244. https://doi.org/10.1007/s10107-010-0420-4

[2] Kojaku, S., Livan, G., & Masuda, N. (2021). Detecting anomalous citation groups in journal networks. Scientific Reports, 11, 14524. https://doi.org/10.1038/s41598-021-93572-3

[3] Clarivate (2025). Journal Citation Reports 2025: Suppressed journals list. https://clarivate.com

[4] Lim, L. (2024). Hodge Laplacians on graphs: A tutorial. https://www.math.ucdavis.edu/~saito/data/tensor/lim_hodge-lap-review.pdf

[5] Perez-Esparrells, M., & López-Otín, C. (2016). Toward the discovery of citation cartels. Frontiers in Physics, 4, 8. https://doi.org/10.3389/fphy.2016.00008

[6] Lazaridou, M., Karachristos, T., & Vakali, A. (2020). Unsupervised anomaly detection in journal citation networks. In Proceedings of the ACM/IEEE Joint Conference on Digital Libraries (pp. 159–168).

[7] Wei, R. K. J., Wee, J., Laurent, V., & Xia, K. (2022). Hodge theory-based biomolecular data analysis. Scientific Reports, 12, 8267. https://doi.org/10.1038/s41598-022-12877-z

[8] Sun, Y. (2025). Hodge decomposition for urban traffic flow. arXiv preprint 2509.17203. https://doi.org/10.48550/arXiv.2509.17203

[9] OpenAlex (2023). OpenAlex: A fully-open index of scholarly metadata. https://openalex.org

[10] NetworkX (2024). NetworkX: Network analysis in Python. https://networkx.org

[11] SciPy (2024). SciPy sparse linear algebra documentation. https://docs.scipy.org/doc/scipy/

[12] Massey, J. (2023). Citation integrity and academic networks. Nature Reviews Methods Primers, 3, 22.
</current_paper>

<reviewer_feedback>
Paper reviewer feedback from the previous iteration. Your strategy MUST address these critiques.
Prioritize major issues — these are the most impactful improvements to make.

- [MAJOR] (methodology) CVS does not measure curl flow. The formula CVS(S) = ||f - f_grad||²/||f||² measures the fraction of non-gradient flow, which is the sum of curl AND harmonic components (f_residual = f_curl + f_harm). The paper's theoretical contribution—'citation cartel structure corresponds to non-zero curl components'—requires curl to be separated from harmonic flow. This requires computing the triangle boundary operator B₂ and using the Hodge Laplacian L₁ = B₁ᵀB₁ + B₂B₂ᵀ to obtain the true curl projection. The current implementation skips this step, making the 'Citation Vortex' framing mathematically unjustified. The paper acknowledges this in the limitations section but does not adjust the main claims accordingly.
  Action: Either implement explicit harmonic/curl separation: compute B₂ from triangles in the citation graph, then project f_residual onto ker(B₂ᵀ)⊥ for curl and ker(B₂ᵀ) for harmonic; or reframe the contribution honestly as 'non-gradient flow score' throughout the paper and revise all theoretical claims. The former is scientifically stronger; the latter preserves integrity.
- [MAJOR] (evidence) The entire quantitative evaluation rests on a single synthetic dataset with an artificially large 15× citation boost injected into 8 of 23 communities. This is a toy setting: AUC=1.0 is expected for any flow-sensitive method given such a strong signal. There is no evaluation on real Clarivate-suppressed journals, despite the paper having access to 17 ground-truth cases (art_oKw95zbMmpyR mentions cartel_ground_truth.json with verified suppressions from 2013, 2018, 2024, 2025). The real OpenAlex 96-journal network is built but never used for the core detection evaluation—only for data construction.
  Action: Run CVS on the real 96-journal OpenAlex network with the 17 Clarivate ground-truth cases. Even partial overlap (e.g., matching 3-4 suppressed groups) would be a significant real-data result. Additionally, test sensitivity to boost magnitude: report AUC as a function of the injection multiplier (2×, 5×, 10×, 15×) to characterize the method's detection threshold and show it remains competitive at realistic signal levels.
- [MAJOR] (evidence) The CIDRE-lite AUC=0.0 is reported as 'failure' but actually indicates perfect anti-correlation—CIDRE-lite ranks cartels dead last, which means inverting the score would give AUC=1.0. The paper misinterprets this as failure rather than sign inversion. Furthermore, CIDRE-lite is not CIDRE: it omits CIDRE's internal group selection and threshold tuning, which are core algorithmic components. Comparing against a deliberately weakened baseline is not scientifically valid, especially when the real CIDRE achieves 54.5% recall on actual JCR suppressions.
  Action: Acknowledge that CIDRE-lite's AUC=0.0 reflects sign inversion, not random failure, and report 1-AUC=1.0 for completeness. Either implement full CIDRE with proper threshold selection (code is available at github.com/skojaku/cidre) or replace with a different baseline. Do not compare CVS's synthetic AUC against CIDRE's real-world 54.5% recall as if they were on the same benchmark.
- [MAJOR] (rigor) The reference list contains systematic numbering errors that misattribute foundational claims. In-text [1] is cited for citation cartel detection but bibliography [1] is the HodgeRank paper (Jiang et al. 2011). In-text [4] describes 'HodgeRank by Jiang et al.' but bibliography [4] is 'Lim 2024 Hodge Laplacians on graphs'—a different paper. The Sun et al. traffic paper is cited as [10] in body but appears as [8] in the bibliography. These are not typos but structural errors that would prevent any reader from verifying cited claims.
  Action: Re-audit all citations. Specifically: assign Jiang et al. 2011 to [4] (the HodgeRank reference), move Lim 2024 to a separate reference number, fix the Sun traffic paper to a consistent number, and review every in-text citation number against the bibliography. Use a reference manager (BibTeX) to prevent future errors.
- [MINOR] (novelty) The application of Hodge decomposition to anomaly detection is not entirely new. A 2025 paper (arXiv:2603.10850) applies Hodge decomposition to identify anomalies in serverless platforms, also using the curl component as an anomaly signal. The paper should acknowledge and differentiate from this and any other work applying Hodge decomposition to network anomaly detection beyond the ranking and domain-specific applications already cited.
  Action: Search for recent work applying Hodge decomposition to network anomaly detection (2022-2026) and add a paragraph in Related Work distinguishing CVS from these approaches. The citation network application remains novel, but the general idea of curl=anomaly is increasingly established.
- [MINOR] (scope) The 500-journal synthetic network is small. The paper claims O(V·E) scalability and mentions the full OpenAlex network has 7,000+ journals, but no scaling experiment is reported. Claims about practical deployment at scale are unsubstantiated.
  Action: Add a runtime plot showing CVS computation time as a function of network size (100, 500, 1000, 5000 journals) to support the scalability claim. This is straightforward to generate and would make the practical contribution more credible.
- [MINOR] (methodology) CVS scores depend on Louvain community detection, which is non-deterministic (random seed) and may produce different partitions across runs. No ablation across community detection methods (Leiden, Infomap) or random seeds is reported, making it unclear whether the AUC=1.0 result is sensitive to partitioning choices.
  Action: Run CVS with at least 3 community detection methods (Louvain, Leiden, Infomap) and report AUC mean and variance. Also report across 10+ random seeds for Louvain to characterize stability to initialization.
- [MINOR] (clarity) The paper's dataset description conflates two different networks: the real 96-journal OpenAlex network (used for data construction) and the synthetic 500-journal network (used for evaluation). The reader must piece this together from scattered references to both. The experimental setup section does not make this distinction clear upfront.
  Action: Add a paragraph at the start of the Experiments section explicitly distinguishing: (a) the real OpenAlex network (96 journals, used for feature analysis only) and (b) the synthetic evaluation network (500 journals, 8 injected cartels, used for all AUC/precision metrics). State what each dataset is used for.
</reviewer_feedback>

<task>
Generate 1 research strategy for THIS iteration.

**ARTIFACT LIMIT: Each strategy may contain AT MOST 3 artifact directions.** Focus on the highest-impact artifacts. Quality over quantity.

Each strategy should:
1. Define a clear OBJECTIVE - what novel contribution we're building toward
2. Plan artifacts to execute NOW - specify type, objective, approach, and depends_on for each
3. Account for parallel execution - all strategies and all planned artifacts run simultaneously, their artifacts are combined into one shared pool


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
    "ArtifactDep": {
      "description": "A single dependency on an existing artifact, with a short type label.\n\n``id`` and ``label`` are LLM-generated at strategy time. ``label`` is free-text but\nshort \u2014 a word or two naming the type of dependency, not a sentence.\n\n``relation_type`` and ``relation_rationale`` are populated later, in upd_hypo,\nusing the MultiCite citation-function typology (Lauscher et al., NAACL 2022).\nThey are absent at strategy time and may stay absent for legacy runs.",
      "properties": {
        "id": {
          "description": "ID of an existing artifact this artifact depends on",
          "title": "Id",
          "type": "string"
        },
        "label": {
          "description": "Short free-text label naming the type of this dependency (a word or two, not a sentence)",
          "title": "Label",
          "type": "string"
        }
      },
      "required": [
        "id",
        "label"
      ],
      "title": "ArtifactDep",
      "type": "object"
    },
    "ArtifactDirection": {
      "description": "High-level direction for an artifact to execute this iteration.\n\nID is code-assigned (LLMPrompt only \u2014 visible in prompts, not LLM-generated).",
      "properties": {
        "type": {
          "description": "Type of artifact to create",
          "enum": [
            "experiment",
            "research",
            "proof",
            "evaluation",
            "dataset"
          ],
          "title": "Type",
          "type": "string"
        },
        "objective": {
          "description": "What we want to achieve with this artifact",
          "title": "Objective",
          "type": "string"
        },
        "approach": {
          "description": "High-level direction/method",
          "title": "Approach",
          "type": "string"
        },
        "depends_on": {
          "description": "Existing artifacts this depends on, each with a short type label",
          "items": {
            "$ref": "#/$defs/ArtifactDep"
          },
          "title": "Depends On",
          "type": "array"
        }
      },
      "required": [
        "type",
        "objective",
        "approach"
      ],
      "title": "ArtifactDirection",
      "type": "object"
    },
    "Strategy": {
      "description": "A research strategy.\n\nContent fields have LLMPrompt + LLMStructOut markers.\n``id`` is code-assigned (LLMPrompt only \u2014 visible in prompts, not LLM-generated).\n\nID format: gen_strat_idx{N}",
      "properties": {
        "title": {
          "description": "Strategy name in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
          "title": "Title",
          "type": "string"
        },
        "objective": {
          "description": "The novel contribution we're building toward",
          "title": "Objective",
          "type": "string"
        },
        "rationale": {
          "description": "Why this strategy is promising",
          "title": "Rationale",
          "type": "string"
        },
        "artifact_directions": {
          "description": "Artifacts to execute THIS iteration",
          "items": {
            "$ref": "#/$defs/ArtifactDirection"
          },
          "title": "Artifact Directions",
          "type": "array"
        },
        "expected_outcome": {
          "description": "What we'll have after this iteration's artifacts complete",
          "title": "Expected Outcome",
          "type": "string"
        },
        "summary": {
          "default": "",
          "description": "Brief summary of the strategy and its expected contribution",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "title",
        "objective",
        "rationale",
        "artifact_directions",
        "expected_outcome"
      ],
      "title": "Strategy",
      "type": "object"
    }
  },
  "description": "Top-level wrapper for LLM strategy generation output.",
  "properties": {
    "strategies": {
      "description": "List of generated strategies",
      "items": {
        "$ref": "#/$defs/Strategy"
      },
      "title": "Strategies",
      "type": "array"
    }
  },
  "required": [
    "strategies"
  ],
  "title": "Strategies",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-07-09 01:36:02 UTC

```
Propose a simple, novel graph-based method for detecting citation cartels in academic networks and validate it.
```

### [3] SYSTEM-USER prompt · 2026-07-09 01:37:47 UTC

```
<verification_results>
Your previous response had issues that need fixing:

DEPENDENCY ERRORS (depends_on can ONLY reference IDs from <existing_artifacts>):
  - Strategy 1: Artifact 'experiment_iter2_dir2' (experiment): dependency 'art_rxHyxG4rT2Xw' has type 'experiment' which is not allowed (allowed: {'research', 'dataset'})

</verification_results>

<task>
Fix ALL issues above and regenerate your strategies:

1. Fix dependency errors:
   - depends_on is a list of {id, label} objects — every entry MUST have a non-empty short label
   - id can ONLY reference IDs from <existing_artifacts>
   - You CANNOT reference artifacts you are proposing in this strategy as dependencies (they all run in parallel)
   - Follow the dependency type rules (e.g., experiments require datasets)
   - If no suitable existing artifacts exist, use depends_on: []

Output the corrected JSON with the fixed strategies.
</task>
```
