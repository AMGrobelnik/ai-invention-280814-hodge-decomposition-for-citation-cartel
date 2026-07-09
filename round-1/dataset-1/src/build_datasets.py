#!/usr/bin/env python3
"""Build journal-level citation network from OpenAlex API (efficient closed-world approach).

Algorithm (N+1 API calls total):
1. Fetch top N journals (1 paginated API call)
2. For each journal, fetch K papers with referenced_works (N concurrent calls)
3. Build paper_id -> journal_id map from step 2
4. Count cross-journal citations by looking up referenced_works in the map (no extra calls)
"""

import asyncio
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

import aiohttp
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/build_datasets.log", rotation="30 MB", level="DEBUG")

WS = Path("/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_1/gen_art/gen_art_dataset_1")
OUT_DIR = WS / "temp/datasets"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://api.openalex.org"
HEADERS = {"User-Agent": "mailto:subscriptions-ai-claude2@ijs.si"}
SEMAPHORE_LIMIT = 8


CARTEL_JOURNALS = {
    "Applied Organometallic Chemistry": {"issn": "1099-0739", "reason": "citation_stacking", "year": 2025},
    "Asian Journal of Agriculture and Biology": {"issn": "2307-3608", "reason": "citation_stacking", "year": 2025},
    "Chemical Methodologies": {"issn": "2645-0739", "reason": "citation_stacking", "year": 2025},
    "Genetic Resources and Crop Evolution": {"issn": "1573-5109", "reason": "citation_stacking", "year": 2025},
    "Symmetry": {"issn": "2073-8994", "reason": "citation_stacking", "year": 2024},
    "Mathematics": {"issn": "2227-7390", "reason": "citation_stacking", "year": 2024},
    "Acta Cirurgica Brasileira": {"issn": "1678-2674", "reason": "citation_stacking", "year": 2013},
    "Clinics": {"issn": "1980-5322", "reason": "citation_stacking", "year": 2013},
    "Revista da Escola de Enfermagem da USP": {"issn": "1980-220X", "reason": "citation_stacking", "year": 2013},
    "Revista da Associacao Medica Brasileira": {"issn": "1806-9282", "reason": "citation_stacking", "year": 2013},
    "Current Pharmaceutical Design": {"issn": "1873-4286", "reason": "citation_stacking", "year": 2018},
    "Current Medicinal Chemistry": {"issn": "1875-533X", "reason": "citation_stacking", "year": 2018},
    "Advances and Applications in Discrete Mathematics": {"issn": "0974-1658", "reason": "self_citation", "year": 2025},
    "Annals of Phytomedicine-An International Journal": {"issn": "2321-6786", "reason": "self_citation", "year": 2025},
    "Clinical Hemorheology and Microcirculation": {"issn": "1875-8622", "reason": "self_citation", "year": 2025},
    "Lobachevskii Journal of Mathematics": {"issn": "1818-9962", "reason": "self_citation", "year": 2025},
    "Journal of Earthquake and Tsunami": {"issn": "1793-7116", "reason": "self_citation", "year": 2025},
}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def fetch_json(session: aiohttp.ClientSession, url: str, params: dict) -> dict:
    async with session.get(url, params=params, headers=HEADERS,
                           timeout=aiohttp.ClientTimeout(total=30)) as resp:
        resp.raise_for_status()
        return await resp.json()


async def get_top_journals(session: aiohttp.ClientSession, n: int) -> list[dict]:
    """Fetch top n journals by cited_by_count with pagination."""
    journals = []
    cursor = "*"
    per_page = 200
    logger.info(f"Fetching top {n} journals...")
    while len(journals) < n:
        params = {
            "filter": "type:journal,has_issn:true",
            "sort": "cited_by_count:desc",
            "per-page": per_page,
            "cursor": cursor,
            "select": "id,display_name,issn_l,issn,works_count,cited_by_count",
        }
        data = await fetch_json(session, f"{BASE_URL}/sources", params)
        results = data.get("results", [])
        if not results:
            break
        journals.extend(results)
        cursor = data.get("meta", {}).get("next_cursor", "")
        if not cursor:
            break
        await asyncio.sleep(0.12)
    return journals[:n]


async def get_journal_papers(
    session: aiohttp.ClientSession,
    sem: asyncio.Semaphore,
    source_id: str,
    per_page: int,
) -> list[dict]:
    """Get top cited papers from a journal with their referenced_works."""
    async with sem:
        params = {
            "filter": f"primary_location.source.id:{source_id},publication_year:2015|2016|2017|2018|2019|2020|2021|2022",
            "sort": "cited_by_count:desc",
            "per-page": per_page,
            "select": "id,referenced_works",
        }
        try:
            data = await fetch_json(session, f"{BASE_URL}/works", params)
            return data.get("results", [])
        except Exception as e:
            logger.debug(f"Failed {source_id}: {e}")
            return []


@logger.catch(reraise=True)
async def build_citation_network(n_journals: int = 1000, papers_per_journal: int = 50) -> dict:
    """Build journal citation matrix using closed-world efficient approach."""
    sem = asyncio.Semaphore(SEMAPHORE_LIMIT)

    async with aiohttp.ClientSession() as session:
        # Step 1: Get top journals
        journals = await get_top_journals(session, n=n_journals)
        logger.info(f"Got {len(journals)} journals")

        journal_ids_set = {j["id"] for j in journals}
        journal_meta = {j["id"]: j for j in journals}

        # Step 2: Concurrent paper fetch for ALL journals
        logger.info(f"Fetching papers from {len(journals)} journals concurrently (batch 50)...")
        t0 = time.time()

        # Run in batches to avoid too much memory / connection pressure
        paper_to_journal: dict[str, str] = {}
        journal_papers: dict[str, list[list[str]]] = defaultdict(list)  # journal_id -> [[ref_ids]]

        batch_size = 50
        for batch_start in range(0, len(journals), batch_size):
            batch = journals[batch_start: batch_start + batch_size]
            tasks = [get_journal_papers(session, sem, j["id"], papers_per_journal) for j in batch]
            results = await asyncio.gather(*tasks)

            for journal, papers in zip(batch, results):
                jid = journal["id"]
                for paper in papers:
                    pid = paper.get("id", "")
                    if pid:
                        paper_to_journal[pid] = jid
                    refs = paper.get("referenced_works", []) or []
                    if refs:
                        journal_papers[jid].append(refs)

            elapsed = time.time() - t0
            done = batch_start + len(batch)
            rate = done / elapsed
            remaining = (len(journals) - done) / rate if rate > 0 else 0
            logger.info(f"  {done}/{len(journals)} journals | {len(paper_to_journal)} papers indexed | ~{remaining:.0f}s left")

        logger.info(f"Indexed {len(paper_to_journal)} papers from {len(journals)} journals in {time.time()-t0:.1f}s")

        # Step 3: Count cross-journal citations (no API calls needed)
        citation_counts: dict[tuple[str, str], int] = defaultdict(int)
        for src_jid, ref_lists in journal_papers.items():
            for ref_list in ref_lists:
                for ref_id in ref_list:
                    tgt_jid = paper_to_journal.get(ref_id)
                    if tgt_jid and tgt_jid != src_jid and tgt_jid in journal_ids_set:
                        citation_counts[(src_jid, tgt_jid)] += 1

        edges = [
            {"source_id": src, "target_id": tgt, "citation_count": cnt}
            for (src, tgt), cnt in citation_counts.items()
        ]
        edges.sort(key=lambda x: x["citation_count"], reverse=True)

        # Stats
        node_set = set()
        for e in edges:
            node_set.add(e["source_id"])
            node_set.add(e["target_id"])
        n_nodes = len(node_set)
        n_edges = len(edges)
        sparsity = n_edges / (n_nodes * (n_nodes - 1)) if n_nodes > 1 else 0
        total_cites = sum(e["citation_count"] for e in edges)
        logger.info(f"Network: {n_nodes} nodes, {n_edges} edges, sparsity={sparsity:.6f}")

        return {
            "metadata": {
                "source": "OpenAlex API",
                "query_date": "2026-07-09",
                "n_journals_queried": len(journals),
                "papers_per_journal": papers_per_journal,
                "year_filter": "2015-2022",
                "description": "Directed weighted journal-level citation network.",
            },
            "graph_stats": {
                "n_nodes": n_nodes,
                "n_edges": n_edges,
                "sparsity": sparsity,
                "total_citation_count": total_cites,
            },
            "journals": [
                {
                    "id": j["id"],
                    "name": j.get("display_name", ""),
                    "issn_l": j.get("issn_l", ""),
                    "issn": j.get("issn") or [],
                    "works_count": j.get("works_count", 0),
                    "cited_by_count": j.get("cited_by_count", 0),
                }
                for j in journals
                if j["id"] in node_set
            ],
            "edges": edges,
        }


def build_ground_truth() -> dict:
    cases = []
    for name, meta in CARTEL_JOURNALS.items():
        cases.append({
            "journal_name": name,
            "issn": meta["issn"],
            "reason": meta["reason"],
            "suppression_year": meta["year"],
            "is_cartel": meta["reason"] == "citation_stacking",
            "source": "Clarivate JCR Suppression List",
        })
    stacking = [c for c in cases if c["is_cartel"]]
    logger.info(f"Ground truth: {len(stacking)} citation stacking, {len(cases)-len(stacking)} self-citation journals")
    return {
        "metadata": {
            "description": "Known citation cartel and manipulation cases from Clarivate JCR annual suppression lists",
            "sources": [
                "Clarivate JCR 2025 (Retraction Watch 2025-06-18)",
                "Clarivate JCR 2024 (Retraction Watch 2024-06-27)",
                "Clarivate JCR 2018 (Scholarly Kitchen 2018-06-27)",
                "Brazilian citation cartel 2013 (CWTS BLOG)",
            ],
        },
        "stats": {
            "total_cases": len(cases),
            "citation_stacking_cases": len(stacking),
            "self_citation_cases": len(cases) - len(stacking),
        },
        "cartel_journals": cases,
    }


@logger.catch(reraise=True)
async def main():
    t0 = time.time()

    # Mini test: 100 journals, 30 papers each
    logger.info("=== MINI: 100 journals, 30 papers each ===")
    mini = await build_citation_network(n_journals=100, papers_per_journal=30)
    p = OUT_DIR / "mini_journal_citation_network.json"
    p.write_text(json.dumps(mini, indent=2))
    mini_elapsed = time.time() - t0
    logger.info(f"Mini: {mini['graph_stats']} | {mini_elapsed:.1f}s | {p.stat().st_size/1024:.0f} KB")

    # Extrapolate to full run
    per_journal = mini_elapsed / 100
    for target in [500, 1000, 2000, 3000]:
        logger.info(f"  Estimate {target} journals: {per_journal*target/60:.1f} min")

    # Full run: 2000 journals, 50 papers each (within ~10 min budget)
    logger.info("=== FULL: 2000 journals, 50 papers each ===")
    full = await build_citation_network(n_journals=2000, papers_per_journal=50)
    p2 = OUT_DIR / "full_journal_citation_network.json"
    p2.write_text(json.dumps(full, indent=2))
    logger.info(f"Full: {full['graph_stats']} | {(time.time()-t0)/60:.1f} min | {p2.stat().st_size/1024/1024:.1f} MB")

    # Ground truth
    gt = build_ground_truth()
    p3 = OUT_DIR / "cartel_ground_truth.json"
    p3.write_text(json.dumps(gt, indent=2))
    logger.info(f"Ground truth saved: {p3}")

    logger.info(f"Total: {(time.time()-t0)/60:.1f} min")


if __name__ == "__main__":
    asyncio.run(main())
