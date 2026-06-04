---
title: "[N] VideoAuto-R1: Video Auto Reasoning via Thinking Once, Answering Twice"
date: 2026-06-04
tags: []
paper: "https://arxiv.org/abs/2601.05175"
issue: 248
issueUrl: "https://github.com/long8v/PTIR/issues/248"
---
<!-- thumbnail: figure 1 — thinking once, answering twice 패러다임 다이어그램 -->

[paper](https://arxiv.org/abs/2601.05175), [page](https://ivul-kaust.github.io/projects/videoauto-r1/)

## TL;DR
- **I read this because.. :**
- **task :** video understanding / RL (auto-think)
- **problem :** video QA에서 always-think (CoT) 가 토큰만 더 쓰고 정확도는 동등하거나 떨어짐 (Table 1). 언제 think 할지를 모델이 스스로 정하게 하고 싶음
- **idea :** "thinking once, answering twice" — 먼저 `\boxed{a_1}` 으로 즉답을 뱉고, confidence (length-normalized mean log prob) 가 threshold $\tau{=}0.97$ 이상이면 early exit. 아니면 `<think>...</think>` 돌고 `\boxed{a_2}` 로 다시 답함
- **input/output :** `{video (≤256 frames), question} -> a_1 (+ optional <think> + a_2)`
- **architecture :** Qwen2.5-VL-7B-Instruct / Qwen3-VL-8B-Instruct. vision encoder frozen, projector + LLM 학습. inference 시 Qwen3-VL은 128K 까지
- **objective :** RL only (cold-start SFT 없음). GRPO + dual-answer reward $R = w_1 R_{task}(a_1) + w_2 R_{task}(a_2) + \lambda R_{fmt} + \alpha R_{fallback}$, $w_1{=}0.9, w_2{=}1.1, \lambda{=}1, \alpha{=}0.3$
- **baseline :** Qwen2.5-VL / Qwen3-VL base, Video-R1, Time-R1, VideoChat-R1.5, Temporal-RLT, Video-RFT, Video-RTS, VITAL, LongVILA-R1, LOVE-R1, training-based auto-think (AdaptThink-style)
- **data :** RL 83K (137K에서 filter). text 6.4K (DAPO-Math) / image 27.5K (ViRL, ThinkLite-Hard) / video 49.4K (Video-R1, TVBench, STI-Bench, temporal grounding)
- **evaluation :** video QA — VideoMME, MVBench, LongVideoBench, MMVU, VideoMMMU, MVP / temporal grounding — Charades-STA, ActivityNet, NExT-GQA / image — MathVista, MathVision, MathVerse, MMMU, MMMU-Pro, MM-Vet
- **result :** VideoMME 67.3 (Qwen2.5) / 71.7 (Qwen3), VideoMMMU 58.6 (+3.9 over Qwen baseline) / 65.0, MVP 39.4 (+2.9 over Video-R1), Charades-STA mIoU 60.0 / 63.7. avg response 44 tokens (vs 149~386). perception 계열 (VideoMME +1.3) 에선 gain 적음
- **contribution :** (저자 claim) (1) video 에서 always-think 가 inefficient 함을 정량으로 보이고 (2) inference-time confidence 로 think/no-think 를 갈라치는 단순한 방법 + dual-answer reward 로 SFT 없이도 학습됨. 진짜 기여는 training-based auto-think 가 collapse 하는 걸 inference-side early exit 으로 우회한 부분인 듯
- **etc. :** $\tau{=}0.97$ 이라는 hyperparam 하나에 think ratio 가 다 결정됨. perception (MVBench 25%, VideoMME 11~40%) vs reasoning (VideoMMMU 51~53%) 으로 task 별로 자동 적응되는 게 신기함. "must-think" sample 이 video 에 거의 없어서 training-based 가 collapse 한다고 주장

## Details

<!-- figure 1: always-think / training-based auto-think / VideoAuto-R1 세 paradigm 비교 -->

### architecture
- backbone: Qwen2.5-VL-7B-Instruct, Qwen3-VL-8B-Instruct 둘 다 실험
- vision encoder는 frozen, projector + LLM 만 학습
- video input: train 시 max 256 frames / 4096 video tokens. inference 시 Qwen3-VL 은 128K context 까지

### method — thinking once, answering twice

<!-- figure 2: (a) training with dual-answer supervision (b) inference with confidence-based early exit -->

세 토큰 시퀀스를 한 번에 생성하는 구조:
1. `\boxed{a_1}` — reasoning 없이 즉답
2. `<think>...</think>` — internal CoT
3. `\boxed{a_2}` — reviewed answer

**inference 시 early-exit**: $a_1$ 생성 직후 token 들의 length-normalized mean log prob 를 confidence 로 보고, $\geq \tau$ ($\tau{=}0.97$) 이면 거기서 끊고 $a_1$ 반환. 아니면 think + $a_2$ 까지 끝까지 생성.

**fallback**: 어려운 문제는 모델이 직답을 못함 → $a_1$ 자리에 `"Let's analyze the problem step by step"` 을 출력하도록 학습. 이게 출력되면 자연스럽게 think 단계로 강제됨 (즉 fallback 도 inference 시 early exit logic 안으로 흡수됨).

### training recipe
- **stage**: SFT 없이 RL only. cold-start 없이 바로 GRPO
- **GRPO**: G=16 rollouts, temperature 1.0, lr $1{\times}10^{-6}$, $\beta{=}0.01$ (KL), batch 256, 1 epoch
- **dual-answer reward**: $R = w_1 R_{task}(a_1) + w_2 R_{task}(a_2) + \lambda R_{fmt} + \alpha R_{fallback}$
  - $w_1{=}0.9, w_2{=}1.1$ → reviewed answer 를 살짝 더 우대
  - $\alpha{=}0.3$ → fallback bonus. 어려운 문제에서 think 단계로 넘기는 걸 reward
- compute: 32 H100, ~35h

### data
- 137K → filter → 83K 로 학습
- text 6.4K (DAPO-Math) / image 27.5K (ViRL, ThinkLite-Hard) / video 49.4K (Video-R1, TVBench, STI-Bench, temporal grounding)
- (논문에 없음) filtering 기준이 정확히 뭔지 (난이도 기반인지 confidence 기반인지) — 본문 다시 봐야 함

### result

<!-- figure 4: qualitative — 초기 답 D 였다가 think 거치며 C 로 교정되는 예시 -->

video QA (Table 3) 기준:
- VideoMME: 67.3 (Qwen2.5) / 71.7 (Qwen3), perception 위주라 gain 작음 (+1.3)
- VideoMMMU: 58.6 (+3.9), 65.0 (Qwen3) — reasoning 계열에서 gain 큼
- MVP: 39.4 (+2.9 over Video-R1)
- avg response length 44 tokens vs prior reasoning model 149~386 토큰 → ~3.3× 단축

temporal grounding (Table 4):
- Charades-STA mIoU 60.0 / 63.7 (Qwen3)
- ActivityNet, NExT-GQA 도 비슷한 trend

image (Table 5): video 에서만 학습했는데 image reasoning bench 에서도 generalization 됨 (MathVista, MathVision, MMMU 류).

### ablation
- **training strategy (Table 6)**: SFT only / RL no-think / RL CoT / VideoAuto-R1 비교. RL CoT 가 reasoning 에서 56.4 인데 149 토큰 쓰는 반면, VideoAuto-R1 은 58.6 + 44 토큰
- **training-based vs inference-based auto-think (Table 7)**: training-based 는 single mode (전부 think 또는 전부 no-think) 로 collapse. inference-side early exit 이 안정적. 저자 주장: video 에는 "must-think" sample 이 드물어서 training signal 부족
- **dual-answer weight (Table 9)**: $w_1{:}w_2 = 0.9{:}1.1$ 비대칭이 동등 weighting 보다 좋음
- **fallback bonus**: $\alpha$ 키우면 reasoning bench 성능 ↑
- **threshold τ (Figure 3)**: $\tau{=}0.97$ 이 robust default. τ ↑ → think ratio ↑ 인데 perception 에선 accuracy gain diminishing
- think-ratio (per bench): MVBench 25/31%, VideoMME 40/11%, VideoMMMU 51/53% — perception 은 ~30% 이하, reasoning 은 50% 이상으로 자동 적응
