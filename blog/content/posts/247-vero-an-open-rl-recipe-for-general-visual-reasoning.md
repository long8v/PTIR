---
title: "[224] Vero: An Open RL Recipe for General Visual Reasoning"
date: 2026-06-04
tags: []
paper: "https://arxiv.org/abs/2604.04917"
issue: 247
issueUrl: "https://github.com/long8v/PTIR/issues/247"
summary: "(1) Open release of 600K open RL data + 30 benchmark evaluation suites (2) Ablation study showing that task-routed rewards (10 types) yield a +5.4 improvement over a single math-verified reward (3) The claim that \"negative transfer in visual reasoning RL is mitigated by data diversity and task-aware rewards\""
---
<!-- thumbnail: figure 1 (Vero overall result/teaser) -->

[paper](https://arxiv.org/abs/2604.04917)

## TL;DR
- **I read this because.. :**
- **task :** MLLM / RL (general visual reasoning)
- **Problem:** In an open-weight VLM, how can we use RL to simultaneously improve a wide range of visual reasoning tasks—such as chart recognition, STEM, spatial reasoning, and grounding—without focusing on any single domain?
- **idea:** 6 categories × 100K uniform sampling (Vero-600K) + task-routed reward that branches based on answer format + single-stage GSPO RL
- **input/output :** `{image, question} -> <think>...</think><answer>...</answer>`
- **Architecture:** RL trained directly on Qwen3-VL-8B-Instruct / Thinking, Qwen2.5-VL-7B-Instruct, and MiMo-VL-7B-SFT. (The paper does not specify whether these models were frozen.)
- **objective :** GSPO, asymmetric clipping ($\varepsilon_{high} > \varepsilon_{low}$), no KL. $R = (1-\alpha) R_{acc} + \alpha R_{fmt} + R_{overlong}$ ($\alpha=0.2$)
- **baseline :** Qwen3-VL-8B-Instruct, Qwen3-VL-8B-Thinking, MiMo-VL-7B-RL
- **Data:** Vero-600K = 59 datasets, 6 categories × 100K. Filtered by 3 criteria—correctness, unambiguity, and verifiability—in batches of ~50 examples each (filter judge = Qwen3-VL-235B-A22B-Instruct)
- **evaluation :** VeroEval 30 benchmark (Chart&OCR 6 / STEM 4 / Spatial&Action 5 / Knowledge 4 / Grounding&Counting 8 / Captioning&IF 3)
- **Result:** Vero-Qwen3I-8B achieved an average score of +5.3 compared to the base model and outperformed Qwen3-VL-8B-Thinking in 23 out of 30 categories. Vero-MiMo-7B outperforms MiMo-VL-7B-RL (closed recipe) in 3 out of 6 categories (STEM +0.5, Knowledge +5.1, Captioning +4.0).
- **Contribution:** (1) Open release of 600K open RL data + 30 benchmark evaluation suites (2) Ablation study showing that task-routed rewards (10 types) yield a +5.4 improvement compared to a single math-verified reward (3) The claim that "negative transfer in visual reasoning RL is mitigated by data diversity and task-aware rewards"
- **etc.:** single stage, ~600 RL steps (≈1 epoch). KL penalty 0. The reasoning length varies by a factor of 16 across categories (Spatial & Action: 1,983 words vs. Grounding/Search: 125 words).

## Details

<!-- Figure 1: Vero Overall Results Teaser, Comparison of 30 Bench Averages -->

### data — Vero-600K
- 59 datasets, 6 categories × 100K uniform samples (uniform sampling yields scores 0.6 to 1.0 points higher than difficulty, area, or length weighting — Table 2)
- Category Structure
  - **Chart & OCR (9)** : ChartQA, InfoVQA, CoSyn-Chart/Diagram/Table, ArxivQA, ECD-VQA, EvoChart, InfographicVQA, ReachQA
  - **STEM (13)** : CoSyn-Math, AI2D, Geo170K, GeomVerse, GeoQA+, MMK12, PathVQA, RAVEN, TQA, VisualWebInstruct, VQA-RAD, We-Math 2.0 (Pro & Std)
  - **Spatial & Action (8)** : GameQA, Magma-AITW, Magma-Mind2Web, Robo2VLM, Spatial-SSRL, ST-VQA, Visual Jigsaw 2D/3D
  - **Knowledge & Recognition (12)** : A-OKVQA, GQA, IconQA, Indoor-QA, KVG, KVQA, PopVQA, VCR, ViQuAE, Visual7W, VizWiz, VQAv2
  - **Grounding, Counting & Search (11)** : AerialVG, GroundUI, MultiHop, Objects365-QA, OOD-VQA, OS-ATLAS, Pixel Reasoner, PixMo, RefCOCOg, TallyQA, Visual Probe
  - **Captioning & IF (6)** : PixMo-AskAnything, PixMo-CapQA, PixMo-Cap, MM-RLVR-IFEval, MMIF-23K, Flickr30K
- Filtering pipeline
- Established criteria by reviewing approximately 50 samples per category: correctness (<5% annotation error rate), unambiguity (whether each question has a single verifiable answer), and verifiability
- Automatic filter judge = `Qwen3-VL-235B-A22B-Instruct`. Removes ambiguous, image-irrelevant, and unverifiable questions
- Results: pre→post filter average 61.3–64.1
- (Not included in the paper): Does not specify how the datasets within a category were weighted

### training recipe
- Algorithm: **GSPO** (Group Sequence Policy Optimization, asymmetric clipping). In the ablation study, it maintains entropy better than GRPO and DAPO (0.58±0.11 vs. 0.50±0.11 / 0.22±0.15) while also achieving a slightly higher average score (54.7 vs. 54.3 / 54.3).
- Single-stage RL, **no warm-start SFT**. ~600 steps ≈ 1 epoch
- KL penalty 0
- context length: soft overlong penalty buffer $[L_{max}-2048, L_{max}]$
- Sampling of temperature, etc.: Qwen3 series T=0.7; for the Qwen2.5 series, see Appendix Tables C2–C3
- SFT vs. RL ablation: On the same Vero-600K dataset, RL outperforms SFT by 4.4 points—meaning this is not due to the data itself being better, but rather because the RL recipe must be applied

### Reward — Task-based (one of the key contributions)
- Total reward
  $$ R(y, y^*) = (1-\alpha) R_{acc}(y, y^*) + \alpha R_{fmt}(y) + R_{overlong}(y),\quad \alpha=0.2 $$
- overlong penalty (Eq. 4):
  $$ R_{overlong}(y) = \min\!\Big(-\frac{|y|-(L_{max}-B)}{B}\lambda,\ 0\Big),\quad B=2048,\ \lambda=1.0 $$
- Reward format: 1 if the `<think>...</think><answer>...</answer>` structure is followed; 0 if not. For answer formats that do not use `\boxed{...}`, a partial score of 0.5 is awarded.
- **10 accuracy rewards** — branched by answer format
  1. string match (exact text equality)
2. Multiple choice (single-letter selection)
  3. numeric → `math-verify` (symbolic parse + tolerance)
4. List string match (any-match, such as synonyms)
5. Ordering → Full reward if the list is in the correct order; 0.2 discount if the set is correct but the order is wrong
  6. web action (JSON field weighted match)
7. Grounding (Hungarian matching of bounding boxes, IoU/F1 threshold of 0.5)
8. Clicking (point-in-box, coordinates [0,1000] normalized)
9. Instruction following (Rate of compliance with constraints)
10. **LLM-as-judge** — Qwen3-32B (disabled), 1–10 points, modified OLMo3 judge setup
- Ablation: Math-Verify single reward 51.8 → multi-route 57.2 (Table 4b). Task-routed outperforms it by an absolute score difference of +5.4.

> User comment (p. 5, next to the entity recognition `"A: Seagull"`): "Should entity recognition just be an exact match?"

### reward hacking & judge guideline
- If you use only an LLM as a judge, the model will inflate scores by using self-evaluative language ("This satisfies all requirements," "exhaustively documents every... detail") and fabricated metrics.
- Mitigation: Specify **Automatic Failure Conditions** in the judge prompt — automatically deduct 1 point if self-evaluative or meta-commentary is detected. Design the system so that reward hacking results in a loss.
- (? I wonder): Is there a chance that this failure condition could compromise valid reasoning? It doesn't seem like the false-positive rate was measured separately.

### evaluation — VeroEval 30 bench
- Chart & OCR (6): ChartQA-Pro, ChartQA, InfoVQA, CharXiv, ChartMuseum, EvoChart
- STEM (4): MMMU-Pro Standard, MMMU-Pro Vision, MathVision, MathVista-testmini
- Spatial & Action (5): Blink, ERQA, GameQA-Lite, EmbSpatial, CVBench
- Knowledge & Recognition (4): RealWorldQA, SimpleVQA, FVQA, MM-Vet V2
- Grounding, Counting & Search (8): CountBenchQA, CountQA, MME-RealWorld, VStarBench, AerialVG, VisualProbe, ScreenSpot, ScreenSpot-Pro
- Captioning & IF (3): MM-MTBench, **MIA-Bench**, MMIFEval

### result
<!-- figure: per-category bar chart, Vero vs Qwen3-VL Instruct/Thinking, MiMo -->

- Vero-Qwen3I-8B vs Qwen3-VL-8B-Instruct: **+5.3 on average**
  - Chart&OCR +8.5 / STEM +6.4 / Spatial&Action +3.7 / Knowledge +1.0 / Grounding +5.3 / Captioning +5.6
- Limited knowledge gain — It appears to be an area where the original base was already performing well.
- Vero-Qwen3I-8B vs Qwen3-VL-**8B-Thinking**: Won on the 23/30 benchmark (an example where the Instruct-based model outperforms the Thinking-based model)
- Vero-Qwen3T-8B vs Qwen3-VL-8B-Thinking: 24 / 30 (Grounding +7.2, Chart&OCR +4.2)
- Vero-MiMo-7B vs MiMo-VL-7B-RL (closed RL recipe): Out of 6 categories, it outperformed the closed recipe in 3—STEM +0.5, Knowledge +5.1, and Captioning +4.0 — when the open recipe was pitted against the closed recipe

### ablation — cross-category transfer
- Key claim: **"Negative transfer is mitigated through data diversity and task-aware reward design"**
- Single-task RL often results in neutral or negative transfer to other categories. For example, when training RL using only captioning, Qwen2.5-VL’s scores in other categories drop by as much as -4.4 to -35.5 points.
- When all 6 categories are combined, **positive cross-category transfer** is observed—that is, adding one category helps with the others as well
- Significant differences in reasoning length across categories: Spatial & Action average 1,983 words vs. Grounding/Search average 125 words

> User comment (p. 13, next to "Spatial & Action"): "Interestingly, 'Spatial & Action' requires more sentences than 'STEM.'"

### etc.
- It remains unclear whether the actual effectiveness of task-routed rewards stems from (a) the accuracy of the reward signal or (b) the fact that the reward distribution varies by category, thereby automatically producing curriculum and balancing effects.
- In the SFT vs. RL ablation, the fact that RL achieved a score of +4.4 is fair since it was based on the same data, but it is unclear whether sufficient hyperparameter tuning was performed for SFT (not mentioned in the paper).
- The gain in the Knowledge category is only +1.0, which is small—this is likely because the Knowledge benchmark itself is a domain where there is little to be gained from RL training (factual recall).
- In a comparison with MiMo-VL-7B-RL, it won 3 out of 6 times = on average, it lost slightly. Still, the core contribution is that "a fully open recipe using 600K data points was able to match the performance of a closed recipe."
