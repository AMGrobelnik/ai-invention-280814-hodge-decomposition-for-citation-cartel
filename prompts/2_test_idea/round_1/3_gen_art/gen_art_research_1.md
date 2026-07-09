# gen_art_research_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_art`
> Run: `run_HMncsxsr6ltD` — Hodge Decomposition for Citation Cartel Detection
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_research_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-07-09 00:38:37 UTC

````
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

<task>
Conduct thorough, unbiased research on the given topic.
Adapt your investigation approach based on the research question and domain.
</task>

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

<critical_requirements>
1. SOURCE DIVERSITY - Consult MANY sources (10+), not just the first few results
2. AVOID SELECTION BIAS - Actively seek contradicting viewpoints, not just confirming ones
3. TRIANGULATE - Cross-reference claims across multiple independent sources
4. ACKNOWLEDGE UNCERTAINTY - Be honest about confidence levels and limitations
5. SYNTHESIZE - Produce a coherent answer that accounts for conflicting evidence
</critical_requirements>

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

Read and STRICTLY follow these skills: aii-web-tools.

<workspace>
Your workspace: `/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_1/gen_art/gen_art_research_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_1/gen_art/gen_art_research_1/`:
GOOD: `/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_1/gen_art/gen_art_research_1/file.py`, `/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_1/gen_art/gen_art_research_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. Use it for prior work and the field's landscape to ground your research.

- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
</available_domain_handbooks>

<artifact_plan>
id: gen_plan_research_1_idx1
type: research
title: Hodge Decomposition, CIDRE, and Ground Truth Research
summary: >-
  Comprehensive research plan to understand Hodge decomposition theory for citation networks, CIDRE methodology and baseline
  metrics, Clarivate suppression ground truth data, and implementation patterns for sparse linear algebra and community detection.
runpod_compute_profile: cpu_light
question: >-
  What mathematical framework, baseline methodologies, and validation ground truth are needed to implement and validate the
  Citation Vortex Score for detecting citation cartels?
research_plan: |-
  ## Phase 1: Hodge Decomposition Theory & Implementation (45 mins)

  ### Step 1.1: Mathematical Foundation
  - Research the Hodge decomposition theorem as applied to directed graphs (Jiang et al., Mathematical Programming 2011)
  - Understand the three orthogonal components: gradient flow (irrotational), curl flow (divergence-free), and harmonic flow (globally cyclic)
  - Document the key insight: gradient flow is acyclic/hierarchical (legitimate citations), curl flow is cyclic/rotational (cartel signatures)
  - Search for: "Hodge decomposition directed graphs", "HodgeRank incidence matrix", "combinatorial Hodge theory graph flow"

  ### Step 1.2: Sparse Linear Algebra Implementation Pattern
  - Understand the computational algorithm:
    1. Construct incidence matrix B1 (V × E matrix, +1 for edge heads, -1 for tails)
    2. Construct boundary matrix B2 (edge × triangle matrix for curl computation)
    3. Solve least-squares system using scipy.sparse.linalg.lsqr to extract gradient potential
    4. Residual = curl + harmonic components
  - Document matrix dimensions and sparsity patterns for 1000+ journal networks
  - Search for: "scipy.sparse.linalg LSQR implementation", "incidence matrix directed graph python", "boundary operator simplicial complex"

  ### Step 1.3: Reference Implementation Patterns
  - Study existing HodgeRank implementations or adjacency-to-Hodge conversion patterns
  - Identify numerical stability considerations (condition number, regularization if needed)
  - Document expected computational complexity O(V·E) for sparse solve
  - Search for: "HodgeRank implementation ranking", "Hodge Laplacian computation"

  ---

  ## Phase 2: CIDRE Methodology & Baselines (40 mins)

  ### Step 2.1: CIDRE Algorithm Deep Dive
  - Understand degree-corrected stochastic block model (dcSBM) as null model:
    - dcSBM preserves per-journal citation out-degree and in-degree (controls for journal size/activity)
    - Generates randomized networks respecting block structure (journal communities)
    - Computes excess citation fraction: (observed - expected_under_dcSBM) / expected_under_dcSBM
  - Document how CIDRE ranks journal groups by excess citation strength
  - Key parameters: dcSBM block structure (from community detection), number of Monte Carlo samples for expected value
  - Search for: "CIDRE dcSBM null model parameters", "degree-corrected stochastic block model citation networks"

  ### Step 2.2: CIDRE Performance Metrics
  - Confirm empirical results from CIDRE paper:
    - Detected 12 of 22 JCR-suppressed cartel groups (54% recall)
    - Overlap scores ≥0.8 for 8 groups (67% high-confidence matches)
    - Identified 10 groups earlier than JCR suspension (predictive power)
  - Document precision-recall tradeoff: threshold-dependent detection (excess citation fraction cutoff)
  - Search for: "CIDRE cartel detection precision recall", "CIDRE evaluation metrics results"

  ### Step 2.3: Reciprocity Ratio Baseline
  - Simple pairwise method: for each journal pair (i,j), compute reciprocity_ratio = min(c_ij, c_ji) / max(c_ij, c_ji)
  - High reciprocity_ratio → suspicious pair (strong mutual citation)
  - This is the "naive edge-level symmetry" baseline that CVS must outperform
  - Document why this is insufficient: ignores network context, doesn't account for journal size, no hierarchical signal
  - Search for: "reciprocal citation detection academic", "citation symmetry cartel baseline"

  ---

  ## Phase 3: Clarivate Suppression Ground Truth (35 mins)

  ### Step 3.1: Suppression List & Format
  - Locate Clarivate's official suppression list (Journal Citation Reports)
  - Document structure: journal pairs or groups suppressed in specific years (2015–2022)
  - Key data points:
    - 33 journals suppressed in 2020 (0.27% of ~12,000 total)
    - 10 journals in 2021, 3 in 2022, 17 in 2024, 20 in 2025
    - Suppression reason: excessive self-citation and/or citation stacking
  - Search for: "Clarivate Journal Citation Reports suppression list", "JCR suppressed journals 2020 2021 2022 names"

  ### Step 3.2: Ground Truth Reliability & Limitations
  - Assess reliability: Clarivate uses internal methods (not published), likely combines reciprocity + statistical thresholds
  - Known limitations:
    - Partial ground truth: only detected/acted-on cartels (false negatives: undetected cartels remain active)
    - Delayed detection: 1-2 year lag between cartel formation and suspension
    - May include false positives: legitimate journal pairs in overlapping fields suppressed by threshold
  - Document expected cartel group size: 2–10 journals per group (CIDRE findings: avg 4)
  - Search for: "Clarivate suppression criteria methodology", "JCR citation stacking definition"

  ### Step 3.3: Integration with Research
  - Identify specific years of suppression data to use (recommend 2015–2022 for 7-year overlap with OpenAlex coverage)
  - Plan evaluation: treat suppressed groups as positive labels, rank all detected groups by CVS, compute precision@K and AUC-ROC
  - Document manual verification step: review top-ranked groups to confirm cartel behavior
  - Search for: "Clarivate suppressed journals 2015-2022 full list", "citation cartel confirmation validation"

  ---

  ## Phase 4: Data & Implementation Infrastructure (30 mins)

  ### Step 4.1: Journal-Level Citation Graph Construction
  - OpenAlex API:
    - Free, ~250M papers, covers >7,000 active journals
    - Returns work records with journal metadata and cited_by_count
    - Python access via pyopenalex or direct HTTP + requests
  - Data collection strategy:
    1. Query OpenAlex for all works by journal (filter by journal ID or ISSN)
    2. For each year window (e.g., 2015–2022), aggregate: for each (source_journal, target_journal) pair, sum citations
    3. Construct weighted directed graph: nodes = journals, edge weight = annual citation count
  - Search for: "OpenAlex API journal citations tutorial", "OpenAlex python pyopenalex example"

  ### Step 4.2: Community Detection Implementation
  - Louvain algorithm (standard for citation networks):
    - Available in NetworkX: networkx.algorithms.community.louvain_communities()
    - Also available in python-louvain package: community.best_partition()
    - Input: undirected projection of citation network (ignore edge directions to find structural communities)
    - Output: partition dict mapping journal_id → community_id
  - Alternatives: Leiden (faster, better quality), Infomap (information-theoretic)
  - For CVS: use undirected projection to find candidate subgroups S, then compute CVS(S) on directed flow
  - Search for: "Louvain community detection NetworkX", "networkx.louvain_communities documentation"

  ### Step 4.3: Sparse Matrix & Solver Setup
  - scipy.sparse.coo_matrix or csr_matrix for incidence/boundary matrices
  - scipy.sparse.linalg.lsqr for least-squares solve (handles singular/near-singular systems)
  - numpy for dense vector operations (gradient potential, curl energy calculation)
  - Validation: check matrix rank, condition number, solution residuals
  - Search for: "scipy sparse matrix performance large graphs", "scipy.sparse.linalg.lsqr convergence"

  ---

  ## Phase 5: Evaluation Plan & Metrics (20 mins)

  ### Step 5.1: Success Criteria Operationalization
  - **CONFIRM hypothesis:** CVS achieves precision@20 > reciprocity baseline AND AUC-ROC > CIDRE-lite baseline
    - Precision@20: among top-20 ranked subgroups by CVS, what % overlap with suppressed groups (overlap ≥0.5)?
    - AUC-ROC: rank all subgroups by CVS score, plot ROC curve (true positive rate vs false positive rate)
    - Comparison targets: reciprocity ratio baseline (simple pairwise), CIDRE excess citation fraction method
  - Threshold: at least 50% of confirmed cartel groups in top decile (top 10% by CVS)
  - Search for: "precision@K metric definition anomaly detection", "AUC-ROC imbalanced datasets"

  ### Step 5.2: Failure Scenarios & Robustness Tests
  - **DISCONFIRM hypothesis:** if CVS is statistically indistinguishable from reciprocity ratio (Pearson ρ > 0.95, same ranking order), then Hodge decomposition adds no information
  - Temporal robustness: test CVS on different year windows (2015–2018, 2018–2022, rolling windows)
  - Subgroup robustness: compare CVS rankings across different community detection algorithms (Louvain vs Leiden vs Infomap)
  - Ablation study: gradient flow divergence as complementary signal (journals that cite but are not cited)
  - Search for: "statistical significance hypothesis testing ROC curves", "Spearman Kendall correlation ranking similarity"

  ### Step 5.3: Metrics Implementation Checklist
  - Overlap score: Jaccard(detected_group, suppressed_group) = |intersection| / |union|
  - Energy ratio: CVS(S) = Σ_e∈S f_curl(e)² / Σ_e∈S f(e)²  (normalized energy)
  - Rank correlation: Spearman ρ between CVS ranking and reciprocity ranking → detect if confounded
  - Cumulative gain chart: % of suppressed groups recovered vs % of journals reviewed

  ---

  ## Summary of Key Findings & Integration Points

  1. **Hodge Decomposition is Implementable:** Jiang et al. 2011 provides the algorithm; scipy.sparse.linalg.lsqr is the standard solver. Estimated complexity O(V·E) for journal networks with ~500–5000 nodes.

  2. **CIDRE Provides Strong Baseline:** 54% recall on JCR suppressions; excess citation fraction method is parameter-tuned (dcSBM thresholds). CVS must exceed this to justify novel methodology.

  3. **Clarivate Ground Truth is Reliable but Partial:** 33–20 suppressed journals/pairs per year (2020–2025); likely reflects ~0.3% of active journal ecosystem. Sufficient for validation if combined with temporal overlap (CIDRE detected 10 groups before JCR suppression).

  4. **Implementation Path is Clear:** OpenAlex API for data, NetworkX for graphs, scipy.sparse for linear algebra, python-louvain for communities. All open-source, documented, no special infrastructure needed.

  5. **Evaluation Must Be Rigorous:** Precision@K, AUC-ROC, and Spearman ρ correlation tests required to claim CVS outperforms baselines. Ablation and robustness tests non-negotiable to avoid overfitting to Clarivate's specific year.
explanation: >-
  This research establishes the mathematical, methodological, and empirical foundations needed for the executor to implement
  CVS. It answers three critical questions: (1) How is Hodge decomposition computed on directed graphs using sparse linear
  algebra? (2) What are the performance benchmarks for CIDRE and the reciprocity baseline that CVS must beat? (3) Where is
  the Clarivate ground truth and how reliable is it? The plan provides concrete technical details (matrix construction, scipy
  APIs, library names), performance metrics from prior work (CIDRE: 54% recall, 12/22 groups detected), and a clear evaluation
  strategy (precision@K, AUC-ROC, Spearman correlation vs baselines). This enables the executor to write correct code, choose
  appropriate parameters, and validate results against published benchmarks, avoiding false positives and ensuring the hypothesis
  test is rigorous and publishable.
</artifact_plan>

<investigation_process>
1. DIVERGE: Brainstorm multiple angles/framings of the question before searching. Think across fields — what adjacent domains might have relevant insights?
2. SEARCH: Multiple queries per angle with different phrasings to discover the landscape
3. FETCH: Read promising URLs at high level. Snippets are NOT enough — fetch full pages
4. DETAIL: aii-web-tools fetch_grep for specifics from key pages/PDFs
5. CONTRAST: Actively try to disprove your emerging conclusions. Search with different phrasings, "[topic] criticism", "[topic] limitations". Check across fields — the same finding may exist under different names
6. SYNTHESIZE: Integrate into balanced conclusion
7. ITERATE: Expect to repeat steps 2-6 if findings are incomplete or one-sided. Don't settle on first results
8. SUMMARIZE: Output JSON must include 'title' and 'summary' fields
</investigation_process>

<output_requirements>
- Write research_out.json to your workspace with all findings
- Provide your finding as clear prose WITH NUMBERED CITATIONS
- EVERY factual claim must have a citation number in brackets: [1], [2], [1, 3], etc.
- Include BOTH supporting AND contradicting evidence
- Be explicit about confidence level and what would change it
- End with follow-up questions for further investigation
</output_requirements>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

Research everything specified in the artifact plan, but you may also investigate additional relevant aspects beyond what's listed. Investigate this question thoroughly.

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ResearchExpectedFiles": {
      "description": "All expected output files from research artifact.",
      "properties": {
        "output": {
          "description": "Path to research output JSON. Example: 'research_out.json'",
          "title": "Output",
          "type": "string"
        }
      },
      "required": [
        "output"
      ],
      "title": "ResearchExpectedFiles",
      "type": "object"
    },
    "Source": {
      "description": "A source used in the research.",
      "properties": {
        "index": {
          "description": "Citation number (1, 2, 3, ...)",
          "title": "Index",
          "type": "integer"
        },
        "url": {
          "description": "Full URL of the source",
          "title": "Url",
          "type": "string"
        },
        "title": {
          "description": "Title of the article/page",
          "title": "Title",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this source contributed",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "index",
        "url",
        "title",
        "summary"
      ],
      "title": "Source",
      "type": "object"
    }
  },
  "description": "Research artifact \u2014 structured output + file metadata.\n\nConducts thorough web research using the aii-web-tools skill.\nReturns structured JSON output with citations.",
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
      "$ref": "#/$defs/ResearchExpectedFiles",
      "description": "All output files you created. Must include research_out.json with your research findings."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    },
    "answer": {
      "description": "Comprehensive answer with NUMBERED CITATIONS. Cite sources by number: 'Claim [1].' or 'According to [2, 3]...'",
      "title": "Answer",
      "type": "string"
    },
    "sources": {
      "description": "All sources used, with index matching citation numbers in answer",
      "items": {
        "$ref": "#/$defs/Source"
      },
      "title": "Sources",
      "type": "array"
    },
    "follow_up_questions": {
      "description": "2-3 follow-up questions that emerged from the investigation",
      "items": {
        "type": "string"
      },
      "title": "Follow Up Questions",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files",
    "answer",
    "sources",
    "follow_up_questions"
  ],
  "title": "ResearchArtifact",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-07-09 00:38:37 UTC

```
Propose a simple, novel graph-based method for detecting citation cartels in academic networks and validate it.
```

### [3] SKILL-INPUT — aii-web-tools · 2026-07-09 00:38:45 UTC

The agent loaded the **aii-web-tools** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-web-tools
description: "Web research toolkit: web search (Serper/Google), web page fetch as markdown (HTML and PDF), and regex grep over full page/PDF text. Use whenever a task needs to search the web, read a page, mine a paper/PDF, verify citations, or extract exact quotes, numbers, or methodology from a URL."
---

## Web tools

You have three web capabilities: **search**, **fetch**, and **grep** (exact
regex extraction over a full page or PDF).

**Pick where they come from, in this order:**

1. **If you have built-in `WebSearch` / `WebFetch` tools, PREFER those over the
   scripts below.** They may be **deferred tools** (listed by name but with
   schemas not yet loaded) — if so, call `ToolSearch("select:WebSearch,WebFetch")`
   ONCE to load them, then use them normally. Do not skip them just because they
   need that one extra load step; they are the preferred path. Pair them with the
   `aii_web_tools__fetch_grep` script below when you need exact text / numbers /
   methodology that a summary would miss, or when reading a PDF.
2. **Only if you have NO built-in `WebSearch` / `WebFetch`** (e.g. the OpenHands
   backend), use the scripts in this skill (below). They are our own
   implementations — Serper.dev for search, html2text + PyMuPDF for fetch, and
   regex grep over the full document text. They work without any built-in web
   tools.

Workflow either way: **search** (discover) → **fetch** (read for the gist) →
**grep** (pull exact details / read PDFs).

---

## Running the scripts

Run every script with the skill's pre-provisioned interpreter (it already has
`requests`, `html2text`, `pymupdf`, `python-dotenv`). Set `PY` once:

```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-web-tools"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

### 1. Search the web (Serper.dev / Google)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation LLM" --max-results 10
```

Returns ranked title / URL / snippet lines. Use it first to scan the
landscape; snippets are for discovery only — fetch a page before judging it.

### 2. Fetch a page as markdown (HTML or PDF)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "https://arxiv.org/abs/2303.11366" --max-chars 10000
```

`--max-chars` caps output (default 10000); `--char-offset N` pages further in.
Handles PDFs transparently via PyMuPDF.

### 3. Grep a page or PDF (exact regex extraction)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" grep --url "https://arxiv.org/pdf/2303.11366" --pattern "verbal reinforcement" --max-matches 20 --context-chars 200
```

Returns only the matching sections with surrounding context — the right tool
for exact numbers, table values, methodology, or long PDFs where a summary
would lose the detail. `-i` for case-insensitive.

**Parallelize** independent searches/fetches in one turn; only sequence a
fetch after the search that produced its URL.

---

## Notes

- The scripts call our ability server. If a script prints
  `Ability service not available`, the server is down — say so rather than
  silently improvising a different search method.
- Do **not** hand-roll your own `requests`/scraping for search when these
  tools are available: Serper returns clean Google results and the fetch/grep
  scripts already handle HTML, PDFs, and encoding.
````

### [4] SYSTEM-USER prompt · 2026-07-09 00:44:45 UTC

```
<validation-feedback>
Attempt 1 failed validation.

Schema validation found 2 problems — fix ALL of them at once:
  - at `layman_summary`: 'Comprehensive research on mathematical theory (Hodge decomposition), state-of-the-art baseline methods (CIDRE achieving 54.5% recall), and validation ground truth (Clarivate suppression data with ~0.3% detection rate) needed to build and validate a novel Citation Vortex Score for detecting suspicious citation exchanges between academic journals.' is too long (at most 250 characters, got 347)
  - at `title`: 'Hodge Decomposition, CIDRE Baseline, and Clarivate Ground Truth for Citation Cartel Detection' is too long (at most 90 characters, got 93)
Every required field must be present and every field type must match the schema.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```
