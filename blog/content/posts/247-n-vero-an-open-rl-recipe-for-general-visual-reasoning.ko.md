---
title: "[N] Vero: An Open RL Recipe for General Visual Reasoning"
date: 2026-06-04
tags: []
paper: "https://arxiv.org/abs/2604.04917"
issue: 247
issueUrl: "https://github.com/long8v/PTIR/issues/247"
---
<!-- thumbnail: figure 1 (Vero overall result/teaser) -->

[paper](https://arxiv.org/abs/2604.04917)

## TL;DR
- **I read this because.. :**
- **task :** MLLM / RL (general visual reasoning)
- **problem :** open weight VLM 에서 단일 도메인에 치중하지 않고 chart / STEM / spatial / grounding 등 넓은 범위의 visual reasoning 을 RL 로 한 번에 끌어올리기
- **idea :** 6 카테고리 × 100K 균등 sampling (Vero-600K) + answer 형식별로 분기되는 task-routed reward + GSPO 단일 stage RL
- **input/output :** `{image, question} -> <think>...</think><answer>...</answer>`
- **architecture :** Qwen3-VL-8B-Instruct / Thinking, Qwen2.5-VL-7B-Instruct, MiMo-VL-7B-SFT 위에 그대로 RL. (frozen 여부는 논문에 없음)
- **objective :** GSPO, asymmetric clipping ($\varepsilon_{high} > \varepsilon_{low}$), no KL. $R = (1-\alpha) R_{acc} + \alpha R_{fmt} + R_{overlong}$ ($\alpha=0.2$)
- **baseline :** Qwen3-VL-8B-Instruct, Qwen3-VL-8B-Thinking, MiMo-VL-7B-RL
- **data :** Vero-600K = 59 dataset, 6 카테고리 × 100K. ~50 example 씩 correctness / unambiguity / verifiability 3 기준으로 필터 (filter judge = Qwen3-VL-235B-A22B-Instruct)
- **evaluation :** VeroEval 30 benchmark (Chart&OCR 6 / STEM 4 / Spatial&Action 5 / Knowledge 4 / Grounding&Counting 8 / Captioning&IF 3)
- **result :** Vero-Qwen3I-8B 가 base 대비 +5.3 average, Qwen3-VL-8B-Thinking 까지 23/30 에서 능가. Vero-MiMo-7B 가 MiMo-VL-7B-RL (closed recipe) 의 6 카테고리 중 3개 (STEM +0.5, Knowledge +5.1, Captioning +4.0) 에서 이김
- **contribution :** (1) 600K open RL data + 30 benchmark eval suite open release (2) task-routed reward (10 type) 가 math-verify 단일 대비 +5.4 라는 ablation (3) "data diversity + task-aware reward 로 visual reasoning RL 의 negative transfer 가 완화된다" 라는 주장
- **etc. :** single stage, ~600 RL step (≈1 epoch). KL penalty 0. category 별 reasoning length 가 16배 차이 (Spatial&Action 1983 단어 vs Grounding/Search 125 단어).

## Details

<!-- figure 1: Vero overall result teaser, 30 bench 평균 비교 -->

### data — Vero-600K
- 59 dataset, 6 카테고리 × 100K 균등 (uniform sampling 이 difficulty / area / length weighting 보다 +0.6~+1.0 점 더 높음 — Table 2)
- 카테고리 구성
  - **Chart & OCR (9)** : ChartQA, InfoVQA, CoSyn-Chart/Diagram/Table, ArxivQA, ECD-VQA, EvoChart, InfographicVQA, ReachQA
  - **STEM (13)** : CoSyn-Math, AI2D, Geo170K, GeomVerse, GeoQA+, MMK12, PathVQA, RAVEN, TQA, VisualWebInstruct, VQA-RAD, We-Math 2.0 (Pro & Std)
  - **Spatial & Action (8)** : GameQA, Magma-AITW, Magma-Mind2Web, Robo2VLM, Spatial-SSRL, ST-VQA, Visual Jigsaw 2D/3D
  - **Knowledge & Recognition (12)** : A-OKVQA, GQA, IconQA, Indoor-QA, KVG, KVQA, PopVQA, VCR, ViQuAE, Visual7W, VizWiz, VQAv2
  - **Grounding, Counting & Search (11)** : AerialVG, GroundUI, MultiHop, Objects365-QA, OOD-VQA, OS-ATLAS, Pixel Reasoner, PixMo, RefCOCOg, TallyQA, Visual Probe
  - **Captioning & IF (6)** : PixMo-AskAnything, PixMo-CapQA, PixMo-Cap, MM-RLVR-IFEval, MMIF-23K, Flickr30K
- 필터링 파이프라인
  - 카테고리당 ~50 sample 씩 직접 보고 기준 정함: correctness (<5% annotation error rate), unambiguity (각 질문이 단일 verifiable answer 가지는지), verifiability
  - automatic filter judge = `Qwen3-VL-235B-A22B-Instruct`. ambiguous / image-irrelevant / unverifiable question 제거
  - 결과: pre→post filter 평균 61.3–64.1
- (논문에 없음): 카테고리 안에서 dataset 끼리는 어떻게 weighting 했는지 명시 X

### training recipe
- algorithm: **GSPO** (Group Sequence Policy Optimization, asymmetric clipping). ablation 에서 GRPO / DAPO 보다 entropy 더 잘 유지 (0.58±0.11 vs 0.50±0.11 / 0.22±0.15) 하면서 평균 score 도 약간 더 높음 (54.7 vs 54.3 / 54.3)
- single stage RL, **warm-start SFT 없음**. ~600 step ≈ 1 epoch
- KL penalty 0
- context length: soft overlong penalty buffer $[L_{max}-2048, L_{max}]$
- temperature 등 sampling: Qwen3 계열 T=0.7, Qwen2.5 계열은 appendix Table C2~C3
- SFT vs RL ablation: 같은 Vero-600K 에 대해 RL 이 SFT 보다 +4.4 점 — 즉 데이터 자체가 좋아서가 아니라 RL recipe 가 같이 작동해야 됨

### reward — task-routed (핵심 contribution 중 하나)
- 전체 reward
  $$ R(y, y^*) = (1-\alpha) R_{acc}(y, y^*) + \alpha R_{fmt}(y) + R_{overlong}(y),\quad \alpha=0.2 $$
- overlong penalty (Eq. 4):
  $$ R_{overlong}(y) = \min\!\Big(-\frac{|y|-(L_{max}-B)}{B}\lambda,\ 0\Big),\quad B=2048,\ \lambda=1.0 $$
- format reward: `<think>...</think><answer>...</answer>` 구조 지키면 1, 안 지키면 0. 보기 형식 (`\boxed{...}` 안 쓴 경우 등) 은 0.5 로 partial
- **10 가지 accuracy reward** — answer 형식별로 분기
  1. string match (exact text equality)
  2. multiple choice (single letter 추출)
  3. numeric → `math-verify` (symbolic parse + tolerance)
  4. list string match (synonym 등 any-match)
  5. ordering → 정확한 list 순서면 full reward, set 은 맞고 순서 틀리면 0.2 discount
  6. web action (JSON field weighted match)
  7. grounding (bbox 들 Hungarian matching, IoU/F1 threshold 0.5)
  8. clicking (point-in-box, 좌표 [0,1000] normalize)
  9. instruction following (제약 충족 비율)
  10. **LLM-as-judge** — Qwen3-32B (thinking disabled), 1~10 점, OLMo3 judge setup 변형
- ablation: math-verify 단일 reward 51.8 → multi-route 57.2 (Table 4b). task-routed 가 +5.4 절대점수 차이로 이김

> 사용자 코멘트 (p.5, entity recognition `"A: Seagull"` 옆): "entity recognition은 그냥 exact match로 해야되나."

### reward hacking & judge guideline
- LLM judge 만 두면 모델이 self-evaluative language ("This satisfies all requirements", "exhaustively documents every... detail") + fabricated measurement 박아서 점수 inflate 시킴
- mitigation: judge prompt 에 **Automatic Failure Conditions** 명시 — self-evaluative / meta-commentary 가 잡히면 자동 1점. 보상 해킹이 손해보는 쪽으로 가도록 설계
- (? 뭘까): 이 failure condition 이 정상적인 reasoning 까지 깎을 가능성은? false-positive rate 는 따로 안 잰 듯

### evaluation — VeroEval 30 bench
- Chart & OCR (6): ChartQA-Pro, ChartQA, InfoVQA, CharXiv, ChartMuseum, EvoChart
- STEM (4): MMMU-Pro Standard, MMMU-Pro Vision, MathVision, MathVista-testmini
- Spatial & Action (5): Blink, ERQA, GameQA-Lite, EmbSpatial, CVBench
- Knowledge & Recognition (4): RealWorldQA, SimpleVQA, FVQA, MM-Vet V2
- Grounding, Counting & Search (8): CountBenchQA, CountQA, MME-RealWorld, VStarBench, AerialVG, VisualProbe, ScreenSpot, ScreenSpot-Pro
- Captioning & IF (3): MM-MTBench, **MIA-Bench**, MMIFEval

### result
<!-- figure: per-category bar chart, Vero vs Qwen3-VL Instruct/Thinking, MiMo -->

- Vero-Qwen3I-8B vs Qwen3-VL-8B-Instruct: **+5.3 평균**
  - Chart&OCR +8.5 / STEM +6.4 / Spatial&Action +3.7 / Knowledge +1.0 / Grounding +5.3 / Captioning +5.6
  - Knowledge 만 gain 작음 — 원래 base 가 이미 잘하던 영역으로 보임
- Vero-Qwen3I-8B vs Qwen3-VL-**8B-Thinking**: 23 / 30 bench 에서 이김 (Instruct base 인데 Thinking base 모델보다 강한 케이스)
- Vero-Qwen3T-8B vs Qwen3-VL-8B-Thinking: 24 / 30 (Grounding +7.2, Chart&OCR +4.2)
- Vero-MiMo-7B vs MiMo-VL-7B-RL (closed RL recipe): 6 카테고리 중 STEM +0.5, Knowledge +5.1, Captioning +4.0 으로 3개 이김 — 오픈 레시피가 클로즈드 레시피랑 붙음

### ablation — cross-category transfer
- 핵심 주장: **"data diversity + task-aware reward design 으로 negative transfer 가 완화된다"**
- single-task RL 은 흔히 다른 카테고리에 neutral 또는 negative transfer. 예: Captioning 만으로 RL 돌리면 Qwen2.5-VL 다른 카테고리가 -4.4 ~ -35.5 점까지 떨어짐
- 6 카테고리 다 섞으면 **positive cross-category transfer** 가 관찰됨 — 즉 한 카테고리 추가하는 게 다른 카테고리에서도 도움
- 카테고리별 reasoning length 차이가 큼: Spatial & Action 평균 1983 단어 vs Grounding/Search 평균 125 단어

> 사용자 코멘트 (p.13, "Spatial & Action" 옆): "재밌게도 STEM 보다 Spatial & Action이 더 문장이 많이 필요하네"

### etc.
- task-routed reward 의 진짜 효과가 (a) reward signal 의 정확도 때문인지 (b) 카테고리별로 reward 분포가 달라서 자동으로 curriculum / balancing 효과 내는 건지 분리 안 되어 있음
- SFT vs RL ablation 에서 RL 이 +4.4 인 건 동일 데이터 기준이라 fair 하지만, SFT 쪽 hparam tuning 이 충분했는지는 (논문에 없음)
- Knowledge 카테고리 gain 만 +1.0 으로 작은데 — knowledge benchmark 자체가 RL 로 학습해서 얻을 게 적은 (factual recall) 영역이라 그런 듯
- MiMo-VL-7B-RL 이랑 비교에서 6 중 3 이김 = 평균으론 약간 짐. 그래도 "fully open recipe + 600K data 로 closed recipe 따라잡힘" 이라는 게 contribution 의 핵심
