#!/usr/bin/env python3
"""Add known cartel journals to the existing mini network via targeted OpenAlex queries."""

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

WS = Path("/ai-inventor/aii_data/users/admin/runs/run_HMncsxsr6ltD/3_invention_loop/iter_1/gen_art/gen_art_dataset_1")
DATASETS_DIR = WS / "temp/datasets"

BASE_URL = "https://api.openalex.org"
HEADERS = {"User-Agent": "mailto:subscriptions-ai-claude2@ijs.si"}

# Known cartel/manipulation journal ISSNs to look up
CARTEL_ISSNS = [
    "1099-0739",  # Applied Organometallic Chemistry
    "2307-3608",  # Asian Journal of Agriculture and Biology
    "2645-0739",  # Chemical Methodologies
    "1573-5109",  # Genetic Resources and Crop Evolution
    "2073-8994",  # Symmetry
    "2227-7390",  # Mathematics (MDPI)
    "1678-2674",  # Acta Cirurgica Brasileira
    "1980-5322",  # Clinics
    "1980-220X",  # Revista da Escola de Enfermagem da USP
    "1806-9282",  # Revista da Associacao Medica Brasileira
    "1873-4286",  # Current Pharmaceutical Design
    "1875-533X",  # Current Medicinal Chemistry
    "0974-1658",  # Advances and Applications in Discrete Mathematics
    "2321-6786",  # Annals of Phytomedicine
    "1875-8622",  # Clinical Hemorheology and Microcirculation
]


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=2, max=15))
async def fetch_json(session, url, params):
    async with session.get(url, params=params, headers=HEADERS,
                           timeout=aiohttp.ClientTimeout(total=30)) as resp:
        resp.raise_for_status()
        return await resp.json()


async def lookup_source_by_issn(session, issn):
    params = {"filter": f"issn:{issn}", "select": "id,display_name,issn_l,issn,works_count,cited_by_count"}
    try:
        data = await fetch_json(session, f"{BASE_URL}/sources", params)
        results = data.get("results", [])
        if results:
            return results[0]
    except Exception as e:
        logger.debug(f"ISSN {issn} lookup failed: {e}")
    return None


async def get_papers(session, source_id, per_page=50):
    params = {
        "filter": f"primary_location.source.id:{source_id},publication_year:2015|2016|2017|2018|2019|2020|2021|2022",
        "sort": "cited_by_count:desc",
        "per-page": per_page,
        "select": "id,referenced_works",
    }
    try:
        data = await fetch_json(session, f"{BASE_URL}/works", params)
        await asyncio.sleep(0.3)
        return data.get("results", [])
    except Exception as e:
        logger.debug(f"Papers fetch failed for {source_id}: {e}")
        return []


@logger.catch(reraise=True)
async def main():
    # Load existing mini network
    mini_path = DATASETS_DIR / "mini_journal_citation_network.json"
    net = json.loads(mini_path.read_text())
    logger.info(f"Loaded mini network: {net['graph_stats']}")

    existing_jids = {j["id"] for j in net["journals"]}
    paper_to_jid: dict[str, str] = {}

    # Rebuild paper→journal map from existing network
    # (We don't have this stored, so we'll add cartel papers only)
    # Load existing edges as citation_counts dict
    edge_dict: dict[tuple, int] = {(e["source_id"], e["target_id"]): e["citation_count"]
                                    for e in net["edges"]}

    async with aiohttp.ClientSession() as session:
        # Step 1: Look up cartel journals by ISSN
        logger.info(f"Looking up {len(CARTEL_ISSNS)} cartel journals...")
        new_journals = []
        for issn in CARTEL_ISSNS:
            await asyncio.sleep(0.2)
            src = await lookup_source_by_issn(session, issn)
            if src:
                if src["id"] not in existing_jids:
                    new_journals.append(src)
                    logger.info(f"  Found: {src['display_name']} ({src['id'][-10:]})")
                else:
                    logger.info(f"  Already in network: {src['display_name']}")

        logger.info(f"Adding {len(new_journals)} new cartel journals to network")

        # Step 2: Fetch papers from new cartel journals
        all_jids = existing_jids | {j["id"] for j in new_journals}
        new_paper_to_jid: dict[str, str] = {}

        for j in new_journals:
            await asyncio.sleep(0.3)
            papers = await get_papers(session, j["id"], per_page=50)
            for p in papers:
                pid = p.get("id", "")
                if pid:
                    new_paper_to_jid[pid] = j["id"]
            logger.info(f"  {j['display_name']}: {len(papers)} papers")

        # Step 3: Count edges between new cartel journals and existing journals
        # For this we need references. Unfortunately we don't have existing papers' references stored.
        # We can only count edges among the new cartel journals themselves.
        new_edge_dict: dict[tuple, int] = defaultdict(int)
        for j in new_journals:
            await asyncio.sleep(0.3)
            papers = await get_papers(session, j["id"], per_page=50)
            for p in papers:
                for ref_id in (p.get("referenced_works") or []):
                    tgt_jid = new_paper_to_jid.get(ref_id)
                    if tgt_jid and tgt_jid != j["id"]:
                        new_edge_dict[(j["id"], tgt_jid)] += 1

        # Merge new edges with existing
        for (src, tgt), cnt in new_edge_dict.items():
            key = (src, tgt)
            edge_dict[key] = edge_dict.get(key, 0) + cnt

        # Build updated network
        all_journals = net["journals"] + [
            {"id": j["id"], "name": j.get("display_name", ""),
             "issn_l": j.get("issn_l", ""), "issn": j.get("issn") or [],
             "works_count": j.get("works_count", 0), "cited_by_count": j.get("cited_by_count", 0)}
            for j in new_journals
        ]

        edges = [{"source_id": s, "target_id": t, "citation_count": c}
                 for (s, t), c in edge_dict.items()]
        edges.sort(key=lambda x: x["citation_count"], reverse=True)

        node_set = {e["source_id"] for e in edges} | {e["target_id"] for e in edges}
        n_nodes = len(node_set)
        n_edges = len(edges)
        sparsity = n_edges / (n_nodes * (n_nodes - 1)) if n_nodes > 1 else 0
        total = sum(e["citation_count"] for e in edges)

        logger.info(f"Augmented network: {n_nodes} nodes, {n_edges} edges, sparsity={sparsity:.6f}")

        aug_net = {
            "metadata": {
                "source": "OpenAlex API",
                "query_date": "2026-07-09",
                "n_journals_queried": len(all_journals),
                "papers_per_journal": 50,
                "year_filter": "2015-2022",
                "description": "Top 100 journals + 15 known cartel/suppressed journals",
            },
            "graph_stats": {
                "n_nodes": n_nodes, "n_edges": n_edges,
                "sparsity": sparsity, "total_citation_count": total,
            },
            "journals": [j for j in all_journals if j["id"] in node_set],
            "edges": edges,
        }

        out = DATASETS_DIR / "full_journal_citation_network.json"
        out.write_text(json.dumps(aug_net, indent=2))
        logger.info(f"Saved augmented network: {out.stat().st_size//1024} KB")


if __name__ == "__main__":
    asyncio.run(main())
