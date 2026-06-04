---
title: "[N] VideoAuto-R1: Video Auto Reasoning via Thinking Once, Answering Twice"
date: 2026-06-04
tags: []
paper: "https://arxiv.org/abs/2601.05175"
issue: 248
issueUrl: "https://github.com/long8v/PTIR/issues/248"
summary: "(Authors claim) (1) quantitatively demonstrates that always-think is inefficient on video, and (2) is learned without SFT using a simple method of separating think/no-think with inference-time confidence + dual-answer reward. The real contribution seems to be bypassing the collapse of training-based auto-think with inference-side early exit."
---
<!-- thumbnail: figure 1 - thinking once, answering twice paradigm diagram -->

[paper](https://arxiv.org/abs/2601.05175), [page](https://ivul-kaust.github.io/projects/videoauto-r1/)

## TL;DR
- **I read this because.. :**
- **task :** video understanding / RL (auto-think)
- Problem :** In video QA, always-think (CoT) uses more tokens and has the same or worse accuracy (Table 1). Want to let the model decide when to think
- **idea :** "thinking once, answering twice" - first spit out an immediate answer with `\boxed{a_1}`, and if the confidence (length-normalized mean log prob) is above the threshold $\tau{=}0.97$, exit early. Otherwise, iterate `<think>...</think>` and answer again with `\boxed{a_2}`.
- **input/output :** `{video (≤256 frames), question} -> a_1 (+ optional <think> + a_2)`
- **architecture :** Qwen2.5-VL-7B-Instruct / Qwen3-VL-8B-Instruct. vision encoder frozen, projector + LLM learning. inference on Qwen3-VL up to 128K.
- **objective :** RL only (no cold-start SFT). GRPO + dual-answer reward $R = w_1 R_{task}(a_1) + w_2 R_{task}(a_2) + \lambda R_{fmt} + \alpha R_{fallback}$, $w_1{=}0.9, w_2{=}1.1, \lambda{=}1, \alpha{=}0.3$
- **baseline :** Qwen2.5-VL / Qwen3-VL base, Video-R1, Time-R1, VideoChat-R1.5, Temporal-RLT, Video-RFT, Video-RTS, VITAL, LongVILA-R1, LOVE-R1, training-based auto-think (AdaptThink-style)
- data :** RL 83K (filter from 137K). text 6.4K (DAPO-Math) / image 27.5K (ViRL, ThinkLite-Hard) / video 49.4K (Video-R1, TVBench, STI-Bench, temporal grounding)
- **evaluation :** video QA — VideoMME, MVBench, LongVideoBench, MMVU, VideoMMMU, MVP / temporal grounding — Charades-STA, ActivityNet, NExT-GQA / image — MathVista, MathVision, MathVerse, MMMU, MMMU-Pro, MM-Vet
- **result :** VideoMME 67.3 (Qwen2.5) / 71.7 (Qwen3), VideoMMMU 58.6 (+3.9 over Qwen baseline) / 65.0, MVP 39.4 (+2.9 over Video-R1), Charades-STA mIoU 60.0 / 63.7. avg response 44 tokens (vs 149~386). less gain in the perception series (VideoMME +1.3).
- Contribution :** (Author claim) (1) Quantitatively demonstrates that always-think is inefficient in video, (2) Simple method for separating think/no-think with inference-time confidence + dual-answer reward, learned without SFT. The real contribution seems to be bypassing the collapse of training-based auto-think with inference-side early exit.
- **etc. :** $\tau{=}0.97$ hyperparam determines the think ratio. It is interesting that it automatically adapts to each task as perception (MVBench 25%, VideoMME 11-40%) vs reasoning (VideoMMMU 51-53%). Claims that training-based collapses because there are few "must-think" samples in the video.

## Details

<!-- figure 1: always-think / training-based auto-think / VideoAuto-R1 comparison of the three paradigms -->

### architecture
- backbone: Qwen2.5-VL-7B-Instruct, Qwen3-VL-8B-Instruct both experimental
- vision encoder is frozen, only projector + LLM learning
- video input: max 256 frames / 4096 video tokens when training. when inferring, Qwen3-VL supports up to 128K context.

### method — thinking once, answering twice

<!-- figure 2: (a) training with dual-answer supervision (b) inference with confidence-based early exit -->

A structure that generates a sequence of three tokens at once:
1. `\boxed{a_1}` - instant answer without reasoning
2. `<think>...</think>` — internal CoT
3. `\boxed{a_2}` — reviewed answer

**early-exit on inference: immediately after generating $a_1$, look at the length-normalized mean log prob of the tokens with confidence, and if $\geq \tau$ ($\tau{=}0.97$), stop there and return $a_1$. Otherwise, generate all the way up to think + $a_2$.

**Fallback: model cannot answer a hard problem directly → learns to output `"Let's analyze the problem step by step"` in place of $a_1$, which naturally forces the think step (i.e., fallback is also absorbed into the early exit logic at inference).

### training recipe
- **stage**: RL only. no SFT. no cold-start. straight GRPO.
- **GRPO**: G=16 rollouts, temperature 1.0, lr $1{\times}10^{-6}$, $\beta{=}0.01$ (KL), batch 256, 1 epoch
- **dual-answer reward**: $R = w_1 R_{task}(a_1) + w_2 R_{task}(a_2) + \lambda R_{fmt} + \alpha R_{fallback}$
- $w_1{=}0.9, w_2{=}1.1$ → slightly favor reviewed answer
- $\alpha{=}0.3$ → fallback bonus. Reward jumping to the THINK phase on hard problems
- compute: 32 H100, ~35h

### data
- Learn with 137K → filter → 83K
- text 6.4K (DAPO-Math) / image 27.5K (ViRL, ThinkLite-Hard) / video 49.4K (Video-R1, TVBench, STI-Bench, temporal grounding)
- (not in the paper) what exactly the filtering criteria is (difficulty based or confidence based) - need to look at the text again

### result

<!-- figure 4: qualitative - an example of an initial answer of D that is corrected to C after thinking -->

Based on video QA (Table 3):
- VideoMME: 67.3 (Qwen2.5) / 71.7 (Qwen3), small gain (+1.3) because it is perception-driven
- VideoMMMU: 58.6 (+3.9), 65.0 (Qwen3) - large gains in the reasoning family
- MVP: 39.4 (+2.9 over Video-R1)
- avg response length 44 tokens vs prior reasoning model 149-386 tokens → ~3.3× shorter

temporal grounding (Table 4):
- Charades-STA mIoU 60.0 / 63.7 (Qwen3)
- ActivityNet, NExT-GQA, NExT-GQA have similar trends

image (Table 5): trained only on video, but generalized to image reasoning bench (MathVista, MathVision, MMMU, etc.).

### ablation
- **training strategy (Table 6)**: SFT only / RL no-think / RL CoT / VideoAuto-R1 comparison. RL CoT scores 56.4 in reasoning and uses 149 tokens, while VideoAuto-R1 scores 58.6 + 44 tokens.
- **training-based vs inference-based auto-think (Table 7)**: training-based collapses to a single mode (all think or all no-think). inference-side early exit is stable. Author's claim: lack of training signal due to sparse "must-think" samples in video.
- **dual-answer weight (Table 9)**: $w_1{:}w_2 = 0.9{:}1.1$ Asymmetry is better than equal weighting
- **FALLBACK BONUS**: Increasing $\alpha$ ↑ reasoning bench performance
- **threshold τ (Figure 3)**: $\tau{=}0.97$ is a robust default. τ ↑ → think ratio ↑ but accuracy gain diminishing in perception
- think-ratio (per bench): MVBench 25/31%, VideoMME 40/11%, VideoMMMU 51/53% - auto-adapts to ~30% or less for perception and 50% or more for reasoning
