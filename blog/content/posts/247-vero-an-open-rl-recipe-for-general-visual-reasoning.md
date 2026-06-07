---
title: "[224] Vero: An Open RL Recipe for General Visual Reasoning"
date: 2026-06-04
tags: []
paper: "https://arxiv.org/abs/2604.04917"
issue: 247
issueUrl: "https://github.com/long8v/PTIR/issues/247"
summary: "Open-source VLM + RL — (1) Open release of 600K open RL data + 30-benchmark evaluation suite (2) Ablation study showing that task-routed rewards (10 types) yield a +5.4 improvement compared to a single math-verified reward (3) Claim that \"negative transfer in visual reasoning RL is mitigated by data diversity and task-aware rewards\""
---
<img width="941" height="278" alt="Image" src="https://github.com/user-attachments/assets/57fb2ff8-85ec-4424-95d8-e049d8915c62" />


[paper](https://arxiv.org/abs/2604.04917)

## TL;DR
- **I read this because.. :** open source VLM + RL
- **task :** MLLM / RL (general visual reasoning)
- **problem :** open source VLM + RL
- **idea:** Explore various recipes
- **input/output :** `{image, question} -> <think>...</think><answer>...</answer>`
- **Architecture:** RL trained directly on Qwen3-VL-8B-Instruct / Thinking, Qwen2.5-VL-7B-Instruct, and MiMo-VL-7B-SFT. (The paper does not specify whether these models were frozen.)
- **objective :** GSPO, asymmetric clipping
- **baseline :** Qwen3-VL-8B-Instruct, Qwen3-VL-8B-Thinking, MiMo-VL-7B-RL
- **Data:** Vero-600K = 59 datasets, 6 categories × 100,000
- **evaluation :** VeroEval 30 benchmark (Chart&OCR 6 / STEM 4 / Spatial&Action 5 / Knowledge 4 / Grounding&Counting 8 / Captioning&IF 3)
- **Result:** Vero-Qwen3I-8B achieved an average score of +5.3 compared to the baseline and outperformed Qwen3-VL-8B-Thinking in 23 out of 30 categories. Vero-MiMo-7B outperforms MiMo-VL-7B-RL (closed recipe) in 3 out of 6 categories (STEM +0.5, Knowledge +5.1, Captioning +4.0).
- **Contribution:** (1) Open release of 600K open RL data + 30 benchmark evaluation suites (2) Ablation study showing that task-routed rewards (10 types) yield a +5.4 improvement compared to a single math-verified reward (3) The claim that "negative transfer in visual reasoning RL is mitigated by data diversity and task-aware rewards"
- **etc. :** 

## Details


### data — Vero-600K

<img width="917" height="529" alt="Image" src="https://github.com/user-attachments/assets/9ec87070-6701-47f2-8539-be0882700099" />

- Category Structure
  - **Chart & OCR (9)** : ChartQA, InfoVQA, CoSyn-Chart/Diagram/Table, ArxivQA, ECD-VQA, EvoChart, InfographicVQA, ReachQA
  - **STEM (13)** : CoSyn-Math, AI2D, Geo170K, GeomVerse, GeoQA+, MMK12, PathVQA, RAVEN, TQA, VisualWebInstruct, VQA-RAD, We-Math 2.0 (Pro & Std)
  - **Spatial & Action (8)** : GameQA, Magma-AITW, Magma-Mind2Web, Robo2VLM, Spatial-SSRL, ST-VQA, Visual Jigsaw 2D/3D
  - **Knowledge & Recognition (12)** : A-OKVQA, GQA, IconQA, Indoor-QA, KVG, KVQA, PopVQA, VCR, ViQuAE, Visual7W, VizWiz, VQAv2
  - **Grounding, Counting & Search (11)** : AerialVG, GroundUI, MultiHop, Objects365-QA, OOD-VQA, OS-ATLAS, Pixel Reasoner, PixMo, RefCOCOg, TallyQA, Visual Probe
  - **Captioning & IF (6)** : PixMo-AskAnything, PixMo-CapQA, PixMo-Cap, MM-RLVR-IFEval, MMIF-23K, Flickr30K
- data filtering 
  - <img width="905" height="380" alt="Image" src="https://github.com/user-attachments/assets/ca8da9fa-f8d3-4d66-a681-a76bd87a11c4" />
- Established criteria by reviewing approximately 50 samples per category: correctness (<5% annotation error rate), unambiguity (whether each question has a single verifiable answer), and verifiability
- Automatic filter judge = `Qwen3-VL-235B-A22B-Instruct`. Removes ambiguous, image-irrelevant, and unverifiable questions
- Results: pre→post filter average 61.3–64.1
- data mixture
- They said it would have been better to just divide it equally
  - <img width="482" height="380" alt="Image" src="https://github.com/user-attachments/assets/cac4c8ce-d8fc-4ea9-9ffc-7cba17b2bd03" />
- (Not included in the paper): Does not specify how the datasets within a category were weighted

### training recipe
- Algorithm: **GSPO** (Group Sequence Policy Optimization, asymmetric clipping). In the ablation study, it maintains entropy better than GRPO and DAPO (0.58±0.11 vs. 0.50±0.11 / 0.22±0.15) while also achieving a slightly higher average score (54.7 vs. 54.3 / 54.3).
  - <img width="439" height="167" alt="Image" src="https://github.com/user-attachments/assets/f4d0f962-fa62-4fcb-84aa-674ef357b18e" />
- Single-stage RL, **no warm-start SFT**. ~600 steps ≈ 1 epoch
- KL penalty 0
- context length: soft overlong penalty buffer $[L_{max}-2048, L_{max}]$
- SFT vs. RL ablation: On the same Vero-600K dataset, RL outperformed SFT by 4.4 points
  -  <img width="481" height="215" alt="Image" src="https://github.com/user-attachments/assets/1a996f73-3242-4f04-bdd1-f313f607d1ce" />
 

### reward 
<img width="871" height="519" alt="Image" src="https://github.com/user-attachments/assets/6af2641c-ce9e-4362-8edc-ff725b04348b" />

- Total reward
  $$ R(y, y^*) = (1-\alpha) R_{acc}(y, y^*) + \alpha R_{fmt}(y) + R_{overlong}(y),\quad \alpha=0.2 $$
- overlong penalty (Eq. 4):
  $$ R_{overlong}(y) = \min\!\Big(-\frac{|y|-(L_{max}-B)}{B}\lambda,\ 0\Big),\quad B=2048,\ \lambda=1.0 $$
- Reward format: 1 if the `<think>...</think><answer>...</answer>` structure is followed; 0 if not. For answer formats that do not use `\boxed{...}`, a partial score of 0.5 is awarded.
- **10 types of accuracy rewards** — branched by answer format
  1. string match (exact text equality)
2. Multiple choice (single-letter selection)
  3. numeric → `math-verify` (symbolic parse + tolerance)
4. List string match (any-match, such as synonyms)
5. Ordering → Full reward if the list is in the correct order; 0.2 discount if the set is correct but the order is wrong
  6. web action (JSON field weighted match)
7. Grounding (Hungarian matching of bounding boxes, IoU/F1 threshold of 0.5)
8. Clicking (point-in-box, coordinates [0,1000] normalized)
9. Instruction following (Rate of compliance with constraints)
10. **LLM-as-judge** — Qwen3-32B (disabled on thinking tasks), 1–10 points, modified OLMo3 judge setup
- ablation: 
  - <img width="415" height="146" alt="Image" src="https://github.com/user-attachments/assets/9d03cfd0-50d9-4a41-9446-2f889cdbeda0" />

- math-verify: single reward 51.8 → multi-route 57.2 (Table 4b). task-routed wins by a margin of +5.4 absolute points

### reward hacking & judge guideline
- If you use only an LLM as a judge, the model will inflate scores by using self-evaluative language ("This satisfies all requirements," "exhaustively documents every... detail") and fabricated metrics.
- Mitigation: Specify **Automatic Failure Conditions** in the judge prompt — automatically deduct 1 point if self-evaluative or meta-commentary is detected. Design the system so that reward hacking results in a loss.
- (? I wonder): Is there a chance that this failure condition could compromise normal reasoning? It doesn't seem like the false-positive rate was measured separately.

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
- Vero-MiMo-7B vs MiMo-VL-7B-RL (closed RL recipe): Out of 6 categories, it outperformed the latter in 3—STEM +0.5, Knowledge +5.1, and Captioning +4.0

### ablation — cross-category transfer
- Key claim: **"Negative transfer is mitigated through data diversity and task-aware reward design"**
- Single-task RL often results in neutral or negative transfer to other categories. For example, when training Qwen2.5-VL using only captioning, its scores on other categories drop by as much as -4.4 to -35.5 points.
- When all 6 categories are combined, **positive cross-category transfer** is observed—in other words, adding one category helps with the others as well
- Significant differences in reasoning length across categories: Spatial & Action average 1,983 words vs. Grounding/Search average 125 words
  -  <img width="453" height="377" alt="Image" src="https://github.com/user-attachments/assets/371d30ce-85cd-487e-a1cb-39b85dcba43d" />
- Interestingly, "Spatial & Action" requires more sentences than "STEM."

### etc.
- It remains unclear whether the true effectiveness of task-routed rewards stems from (a) the accuracy of the reward signal or (b) the fact that the reward distribution varies by category, thereby automatically producing curriculum and balancing effects.
- In the SFT vs. RL ablation, the fact that RL achieved a score of +4.4 is fair since it was based on the same data, but it is unclear whether sufficient hyperparameter tuning was performed for SFT (not mentioned in the paper).
- The gain in the Knowledge category is only +1.0, which is small—this is likely because the Knowledge benchmark itself is a domain (factual recall) where there is little to be gained from RL training.

