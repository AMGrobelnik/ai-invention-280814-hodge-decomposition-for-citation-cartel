# Prompts

Complete, auto-generated record of **every prompt the AI Inventor system gave each agent** across this run — generated at repository-upload time so it captures all steps.

- Run: `run_HMncsxsr6ltD` — Hodge Decomposition for Citation Cartel Detection

Each prompt is labelled by type and timestamped, with its full untruncated body:

- **SYSTEM-USER** — the pipeline-generated role/instruction prompt placed in the user slot.
- **HUMAN-USER** — the task / human-typed message into the agent stream.
- **SKILL-INPUT** — a skill the agent loaded; its `SKILL.md` instructions, verbatim.

Layout mirrors the run's module tree: one folder per high-level phase, a `round_N/` per iteration where the phase iterates, then each module — a single-task module is one `.md` file, a parallel module (gen_plan / gen_art / gen_viz / gen_demo_art) is a folder with one `.md` per task.

## Index

- **1. create_idea** — `hypo_loop`
  - round_1
    - `prompts/1_create_idea/round_1/1_gen_hypo.md` — 3 prompt(s)
    - `prompts/1_create_idea/round_1/2_review_hypo.md` — 3 prompt(s)
- **2. test_idea** — `invention_loop`
  - round_1
    - `prompts/2_test_idea/round_1/1_gen_strat.md` — 2 prompt(s)
    - `2_gen_plan/` — 3 task(s)
      - `prompts/2_test_idea/round_1/2_gen_plan/gen_plan_dataset_1.md` — 3 prompt(s)
      - `prompts/2_test_idea/round_1/2_gen_plan/gen_plan_experiment_1.md` — 3 prompt(s)
      - `prompts/2_test_idea/round_1/2_gen_plan/gen_plan_research_1.md` — 3 prompt(s)
    - `3_gen_art/` — 3 task(s)
      - `prompts/2_test_idea/round_1/3_gen_art/gen_art_dataset_1.md` — 16 prompt(s)
      - `prompts/2_test_idea/round_1/3_gen_art/gen_art_experiment_1.md` — 12 prompt(s)
      - `prompts/2_test_idea/round_1/3_gen_art/gen_art_research_1.md` — 4 prompt(s)
    - `prompts/2_test_idea/round_1/4_gen_paper_text.md` — 5 prompt(s)
    - `prompts/2_test_idea/round_1/5_review_paper.md` — 3 prompt(s)
    - `prompts/2_test_idea/round_1/6_upd_hypo.md` — 3 prompt(s)
  - round_2
    - `prompts/2_test_idea/round_2/1_gen_strat.md` — 3 prompt(s)
    - `2_gen_plan/` — 3 task(s)
      - `prompts/2_test_idea/round_2/2_gen_plan/gen_plan_evaluation_1.md` — 7 prompt(s)
      - `prompts/2_test_idea/round_2/2_gen_plan/gen_plan_experiment_1.md` — 3 prompt(s)
      - `prompts/2_test_idea/round_2/2_gen_plan/gen_plan_research_1.md` — 3 prompt(s)
    - `3_gen_art/` — 3 task(s)
      - `prompts/2_test_idea/round_2/3_gen_art/gen_art_evaluation_1.md` — 10 prompt(s)
      - `prompts/2_test_idea/round_2/3_gen_art/gen_art_experiment_1.md` — 9 prompt(s)
      - `prompts/2_test_idea/round_2/3_gen_art/gen_art_research_1.md` — 4 prompt(s)
    - `prompts/2_test_idea/round_2/4_gen_paper_text.md` — 5 prompt(s)
    - `prompts/2_test_idea/round_2/5_review_paper.md` — 3 prompt(s)
    - `prompts/2_test_idea/round_2/6_upd_hypo.md` — 2 prompt(s)
- **3. report_results** — `gen_paper_repo`
  - `1_gen_viz/` — 3 task(s)
    - `prompts/3_report_results/1_gen_viz/gen_viz_1.md` — 5 prompt(s)
    - `prompts/3_report_results/1_gen_viz/gen_viz_2.md` — 6 prompt(s)
    - `prompts/3_report_results/1_gen_viz/gen_viz_3.md` — 6 prompt(s)
  - `2_gen_demo_art/` — 4 task(s)
    - `prompts/3_report_results/2_gen_demo_art/gen_demo_art_dataset_1.md` — 12 prompt(s)
    - `prompts/3_report_results/2_gen_demo_art/gen_demo_art_evaluation_1.md` — 4 prompt(s)
    - `prompts/3_report_results/2_gen_demo_art/gen_demo_art_experiment_1.md` — 9 prompt(s)
    - `prompts/3_report_results/2_gen_demo_art/gen_demo_art_experiment_2.md` — 3 prompt(s)
  - `prompts/3_report_results/3_gen_full_paper.md` — 10 prompt(s)
