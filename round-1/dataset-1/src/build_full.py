#!/usr/bin/env python3
"""Build 500-journal citation network with polite rate limits."""

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
logger.add("logs/build_full.log", rotation="30 MB", level="DEBUG")

WS = Path("/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_1/gen_art/gen_art_dataset_1")
OUT_DIR = WS / "temp/datasets"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://api.openalex.org"
HEADERS = {"User-Agent": "mailto:subscriptions-ai-claude2@ijs.si"}
SEM = 3  # Conservative to avoid rate limits
N_JOURNALS = 500
PAPERS_PER = 50
BATCH_SIZE = 30


@retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=2, min=3, max=20))
async def fetch_json(session: aiohttp.ClientSession, url: str, params: dict) -> dict:
    async with session.get(url, params=params, headers=HEADERS,
                           timeout=aiohttp.ClientTimeout(total=30)) as resp:
        resp.raise_for_status()
        return await resp.json()


async def get_journals(session, n):
    journals = []
    cursor = "*"
    while len(journals) < n:
        params = {
            "filter": "type:journal,has_issn:true",
            "sort": "cited_by_count:desc",
            "per-page": 200,
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
        await asyncio.sleep(0.2)
    return journals[:n]


async def get_papers(session, sem, source_id, per_page):
    async with sem:
        params = {
            "filter": f"primary_location.source.id:{source_id},publication_year:2015|2016|2017|2018|2019|2020|2021|2022",
            "sort": "cited_by_count:desc",
            "per-page": per_page,
            "select": "id,referenced_works",
        }
        try:
            data = await fetch_json(session, f"{BASE_URL}/works", params)
            await asyncio.sleep(0.1)
            return data.get("results", [])
        except Exception as e:
            logger.debug(f"Failed {source_id}: {type(e).__name__}")
            return []


@logger.catch(reraise=True)
async def main():
    t0 = time.time()
    sem = asyncio.Semaphore(SEM)

    connector = aiohttp.TCPConnector(limit=SEM * 2)
    async with aiohttp.ClientSession(connector=connector) as session:
        logger.info(f"Fetching top {N_JOURNALS} journals...")
        journals = await get_journals(session, N_JOURNALS)
        logger.info(f"Got {len(journals)} journals")

        jid_set = {j["id"] for j in journals}
        jmeta = {j["id"]: j for j in journals}

        paper_to_jid: dict[str, str] = {}
        jid_to_refs: dict[str, list[list[str]]] = defaultdict(list)

        success_count = 0
        for batch_start in range(0, len(journals), BATCH_SIZE):
            batch = journals[batch_start: batch_start + BATCH_SIZE]
            tasks = [get_papers(session, sem, j["id"], PAPERS_PER) for j in batch]
            results = await asyncio.gather(*tasks)

            for journal, papers in zip(batch, results):
                jid = journal["id"]
                for p in papers:
                    pid = p.get("id", "")
                    if pid:
                        paper_to_jid[pid] = jid
                    refs = p.get("referenced_works") or []
                    if refs:
                        jid_to_refs[jid].append(refs)
                if papers:
                    success_count += 1

            done = batch_start + len(batch)
            elapsed = time.time() - t0
            rate = done / elapsed
            left = (len(journals) - done) / rate if rate > 0 else 0
            logger.info(f"  {done}/{len(journals)} | {len(paper_to_jid)} papers | ~{left:.0f}s")
            await asyncio.sleep(0.3)

        logger.info(f"Indexed {len(paper_to_jid)} papers from {success_count} journals in {time.time()-t0:.1f}s")

        # Count cross-journal citations
        citations: dict[tuple, int] = defaultdict(int)
        for src_jid, ref_lists in jid_to_refs.items():
            for ref_list in ref_lists:
                for rid in ref_list:
                    tgt_jid = paper_to_jid.get(rid)
                    if tgt_jid and tgt_jid != src_jid and tgt_jid in jid_set:
                        citations[(src_jid, tgt_jid)] += 1

        edges = [{"source_id": s, "target_id": t, "citation_count": c}
                 for (s, t), c in citations.items()]
        edges.sort(key=lambda x: x["citation_count"], reverse=True)

        node_set = {e["source_id"] for e in edges} | {e["target_id"] for e in edges}
        n_nodes = len(node_set)
        n_edges = len(edges)
        sparsity = n_edges / (n_nodes * (n_nodes - 1)) if n_nodes > 1 else 0
        logger.info(f"Network: {n_nodes} nodes, {n_edges} edges, sparsity={sparsity:.6f}")

        net = {
            "metadata": {
                "source": "OpenAlex API",
                "query_date": "2026-07-09",
                "n_journals_queried": len(journals),
                "papers_per_journal": PAPERS_PER,
                "year_filter": "2015-2022",
            },
            "graph_stats": {
                "n_nodes": n_nodes,
                "n_edges": n_edges,
                "sparsity": sparsity,
                "total_citation_count": sum(e["citation_count"] for e in edges),
            },
            "journals": [
                {"id": j["id"], "name": j.get("display_name", ""),
                 "issn_l": j.get("issn_l", ""), "issn": j.get("issn") or [],
                 "works_count": j.get("works_count", 0),
                 "cited_by_count": j.get("cited_by_count", 0)}
                for j in journals if j["id"] in node_set
            ],
            "edges": edges,
        }

        out = OUT_DIR / "full_journal_citation_network.json"
        out.write_text(json.dumps(net, indent=2))
        sz = out.stat().st_size
        logger.info(f"Saved {out.name}: {sz//1024} KB in {(time.time()-t0)/60:.1f} min")


if __name__ == "__main__":
    asyncio.run(main())
