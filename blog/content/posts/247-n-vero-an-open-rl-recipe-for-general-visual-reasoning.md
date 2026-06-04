---
title: "[N] Vero: An Open RL Recipe for General Visual Reasoning"
date: 2026-06-04
tags: []
paper: "https://arxiv.org/abs/2604.04917"
issue: 247
issueUrl: "https://github.com/long8v/PTIR/issues/247"
summary: "(1) 600K open RL data + 30 benchmark eval suite open release (2) ablation that task-routed reward (10 type) is +5.4 vs. math-verify single (3) claim that \"data diversity + task-aware reward mitigates negative transfer of visual reasoning RL\""
---
<!-- thumbnail: figure 1 (Vero overall result/teaser) -->

[paper](https://arxiv.org/abs/2604.04917)

## TL;DR
- **I read this because.. :**
- **task :** MLLM / RL (general visual reasoning)
- Problem :** Bringing a wide range of visual reasoning from open weight VLM to RL at once, including charting / STEM / spatial / grounding, without focusing on a single domain.
- Idea:** 6 categories × 100K uniform sampling (Vero-600K) + task-routed reward branching by answer format + GSPO single stage RL
- **input/output :** `{image, question} -> <think>...</think><answer>...</answer>`
- **architecture:** Qwen3-VL-8B-Instruct/Thinking, Qwen2.5-VL-7B-Instruct, MiMo-VL-7B-SFT on top of RL as-is (frozen or not is not in the paper)
- **objective :** GSPO, asymmetric clipping ($\varepsilon_{high} > \varepsilon_{low}$), no KL. $R = (1-\alpha) R_{acc} + \alpha R_{fmt} + R_{overlong}$ ($\alpha=0.2$)
- **baseline :** Qwen3-VL-8B-Instruct, Qwen3-VL-8B-Thinking, MiMo-VL-7B-RL
- data:** Vero-600K = 59 datasets, 6 categories × 100K. filter by correctness/unambiguity/verifiability 3 criteria by ~50 examples each (filter judge = Qwen3-VL-235B-A22B-Instruct)
- **evaluation :** VeroEval 30 benchmark (Chart&OCR 6 / STEM 4 / Spatial&Action 5 / Knowledge 4 / Grounding&Counting 8 / Captioning&IF 3)
- **result :** Vero-Qwen3I-8B outperforms base by +5.3 average, Qwen3-VL-8B-Thinking by 23/30. Vero-MiMo-7B wins 3 out of 6 categories (STEM +0.5, Knowledge +5.1, Captioning +4.0) in MiMo-VL-7B-RL (closed recipe)
- **contribution :** (1) 600K open RL data + 30 benchmark eval suite open release (2) ablation that task-routed reward (10 type) is +5.4 vs. math-verify single (3) claim that "data diversity + task-aware reward mitigates negative transfer in visual reasoning RL"
- **etc. :** single stage, ~600 RL steps (≈1 epoch). KL penalty 0. 16x difference in reasoning length per category (Spatial&Action 1983 words vs Grounding/Search 125 words).

## Details

<!-- figure 1: Vero overall result teaser, 30 bench average comparison -->

### data — Vero-600K
- 59 dataset, 6 categories × 100K uniform (uniform sampling scores +0.6 to +1.0 points higher than difficulty/area/length weighting - Table 2)
- Organizing categories
  - **Chart & OCR (9)** : ChartQA, InfoVQA, CoSyn-Chart/Diagram/Table, ArxivQA, ECD-VQA, EvoChart, InfographicVQA, ReachQA
  - **STEM (13)** : CoSyn-Math, AI2D, Geo170K, GeomVerse, GeoQA+, MMK12, PathVQA, RAVEN, TQA, VisualWebInstruct, VQA-RAD, We-Math 2.0 (Pro & Std)
  - **Spatial & Action (8)** : GameQA, Magma-AITW, Magma-Mind2Web, Robo2VLM, Spatial-SSRL, ST-VQA, Visual Jigsaw 2D/3D
  - **Knowledge & Recognition (12)** : A-OKVQA, GQA, IconQA, Indoor-QA, KVG, KVQA, PopVQA, VCR, ViQuAE, Visual7W, VizWiz, VQAv2
  - **Grounding, Counting & Search (11)** : AerialVG, GroundUI, MultiHop, Objects365-QA, OOD-VQA, OS-ATLAS, Pixel Reasoner, PixMo, RefCOCOg, TallyQA, Visual Probe
  - **Captioning & IF (6)** : PixMo-AskAnything, PixMo-CapQA, PixMo-Cap, MM-RLVR-IFEval, MMIF-23K, Flickr30K
- Filtering pipelines
- ~50 samples per category for direct reporting criteria: correctness (<5% annotation error rate), unambiguity (each question has a single verifiable answer), verifiability
- automatic filter judge = `Qwen3-VL-235B-A22B-Instruct`. remove ambiguous/image-irrelevant/unverifiable question
- Results: pre→post filter average 61.3-64.1
- (not in the paper): Specify how datasets were weighted within categories X

### training recipe
- Algorithm: **GSPO** (Group Sequence Policy Optimization, asymmetric clipping). maintained entropy better than GRPO / DAPO in ablation (0.58±0.11 vs 0.50±0.11 / 0.22±0.15) with a slightly higher mean score (54.7 vs 54.3 / 54.3).
- single stage RL, **no warm-start SFT**. ~600 steps ≈ 1 epoch
- KL penalty 0
- context length: soft overlong penalty buffer $[L_{max}-2048, L_{max}]$
- temperature, etc. sampling: Qwen3 series T=0.7, Qwen2.5 series are shown in appendix Tables C2 through C3.
- SFT vs RL ablation: For the same Vero-600K, RL scores +4.4 points over SFT - not because the data itself is better, but because the RL recipe needs to work with it

### reward - task-routed (one of the core contributions)
- Total reward
  $$ R(y, y^*) = (1-\alpha) R_{acc}(y, y^*) + \alpha R_{fmt}(y) + R_{overlong}(y),\quad \alpha=0.2 $$
- overlong penalty (Eq. 4):
  $$ R_{overlong}(y) = \min\!\Big(-\frac{|y|-(L_{max}-B)}{B}\lambda,\ 0\Big),\quad B=2048,\ \lambda=1.0 $$
- format reward: `<think>...</think><answer>...</answer>` 1 for following the structure, 0 for not following the structure. Viewing format (such as not using `\boxed{...}`) is 0.5 for partial
- 10 accuracy rewards - branching by answer format
  1. string match (exact text equality)
2. multiple choice (single letter extraction)
  3. numeric → `math-verify` (symbolic parse + tolerance)
4. list string match (any-match, such as synonym)
5. ordering → full reward for correct list order, set is correct, 0.2 discount for incorrect order
  6. web action (JSON field weighted match)
7. grounding (bboxes Hungarian matching, IoU/F1 threshold 0.5)
8. clicking (point-in-box, coordinates [0,1000] normalize)
9. instruction following (percentage of constraints met)
10. **LLM-as-judge** - Qwen3-32B (thinking disabled), 1-10 points, OLMo3 judge setup variant
- ablation: math-verify single reward 51.8 → multi-route 57.2 (Table 4b). task-routed wins by +5.4 absolute score difference

> User comment (p.5, next to entity recognition `"A: Seagull"`): "Maybe entity recognition should just be an exact match."

### reward hacking & judge guideline
- All you need is an LLM judge and the model will inflate your score with self-evaluative language ("This satisfies all requirements", "exhaustively documents every... detail") + fabricated measurements
- mitigation: specify **Automatic Failure Conditions** in judge prompt - automatic 1 point if self-evaluative / meta-commentary caught. Designing reward hacks to lose
- (? What is it): How likely is this failure condition to cut through normal reasoning? I don't think I've measured the false-positive rate.

### evaluation — VeroEval 30 bench
- Chart & OCR (6): ChartQA-Pro, ChartQA, InfoVQA, CharXiv, ChartMuseum, EvoChart
- STEM (4): MMMU-Pro Standard, MMMU-Pro Vision, MathVision, MathVista-testmini
- Spatial & Action (5): Blink, ERQA, GameQA-Lite, EmbSpatial, CVBench
- Knowledge & Recognition (4): RealWorldQA, SimpleVQA, FVQA, MM-Vet V2
- Grounding, Counting & Search (8): CountBenchQA, CountQA, MME-RealWorld, VStarBench, AerialVG, VisualProbe, ScreenSpot, ScreenSpot-Pro
- Captioning & IF (3): MM-MTBench, **MIA-Bench**, MMIFEval

### result
<!-- figure: per-category bar chart, Vero vs Qwen3-VL Instruct/Thinking, MiMo -->

- Vero-Qwen3I-8B vs Qwen3-VL-8B-Instruct: **+5.3 average**.
  - Chart&OCR +8.5 / STEM +6.4 / Spatial&Action +3.7 / Knowledge +1.0 / Grounding +5.3 / Captioning +5.6
- Small gain in knowledge only - seems to be an area where the original base was already good at
- Vero-Qwen3I-8B vs Qwen3-VL-**8B-Thinking**: Wins 23 / 30 bench (Instruct base, but stronger case than Thinking base model)
- Vero-Qwen3T-8B vs Qwen3-VL-8B-Thinking: 24 / 30 (Grounding +7.2, Chart&OCR +4.2)
- Vero-MiMo-7B vs MiMo-VL-7B-RL (closed RL recipe): Wins 3 out of 6 categories with STEM +0.5, Knowledge +5.1, Captioning +4.0 - open recipe is tied with closed recipe

### ablation — cross-category transfer
- Key claim: **"data diversity + task-aware reward design mitigates negative transfer"**.
- Single-task RL often has a neutral or negative transfer to other categories. Example: RL turns on captioning alone caused Qwen2.5-VL other categories to drop by -4.4 to -35.5 points
- 6 When mixing categories, **positive cross-category transfer** is observed - i.e., adding one category helps another category
- Large difference in reasoning length by category: Spatial & Action average 1983 words vs Grounding/Search average 125 words

> User comments (p.13, next to "Spatial & Action"): "Funny, Spatial & Action needs more sentences than STEM."

### etc.
- No separation of whether the true effect of task-routed rewards is (a) due to the accuracy of the reward signal or (b) due to different reward distributions across categories, which automatically produces a curricular/balancing effect
- The RL of +4.4 in SFT vs RL ablation is fair based on the same data, but whether the hparam tuning on the SFT side was sufficient (not in the paper) is not known.
- Only the Knowledge category gain is small at +1.0 - as if the knowledge benchmark itself is an area where there is little to gain from learning with RL (factual recall).
- MiMo-VL-7B-RL wins 3 out of 6 in gyrus comparison = a bit of a burden on average. Still, "fully open recipe + 600K data to catch up with closed recipe" is the core of contribution
