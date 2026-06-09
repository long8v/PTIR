---
title: "[225] VideoAuto-R1: Video Auto Reasoning via Thinking Once, Answering Twice"
date: 2026-06-09
tags: []
paper: "https://arxiv.org/abs/2601.05175"
issue: 249
issueUrl: "https://github.com/long8v/PTIR/issues/249"
summary: "video + think — Ablation studies show that \"always-think\" is not the answer. However, it would be more accurate to say that auto-mode is efficient rather than that it improves absolute performance. The framing of \"confidence-based early-exit gating\" is elegant."
---
<img width="847" height="263" alt="Image" src="https://github.com/user-attachments/assets/04d9a7fe-8354-487f-848e-6941ae3693d7" />


[paper](https://arxiv.org/abs/2601.05175)

## TL;DR
- **I read this because.. :** video + think 
- **task :** video reasoning 
- **Problem:** CoT isn't always helpful in video QA—how can we train the model to achieve a good balance?
- **idea:** When training, always have the model give an immediate answer and then a second answer after thinking. During inference, assign a confidence score based on the log probability of the answer token, and then enable the "think" step.
- **input/output :** {video, question} -> {initial boxed answer, (optional reasoning), reviewed boxed answer}
- **Architecture:** Qwen2.5-VL-7B-Instruct / Qwen3-VL-8B-Instruct. Visual encoder frozen; only the projector and LLM were trained. Maximum of 4096 video tokens and 256 frames.
- **Objective:** GRPO. Start RL immediately without a cold-start SFT.
- **Baseline:** Video-R1 (primarily spatial learning), Time-R1, VideoChat-R1, VideoChat-R1.5, VITAL, LongVILA-R1, LOVE-R1 / base Qwen2.5-VL-7B, Qwen3-VL-8B.
- **Data:** RL 83K (removed 8 rollouts—all-correct and all-wrong—from 137K). text 6.4K (DAPO-Math) / image 27.5K (ViRL, ThinkLite-Hard) / video 49.4K (Video-R1, TVBench, STI-Bench, MMR-VBench, Charades-STA, ActivityNet, Time-R1, NExT-GQA)
- **evaluation :** VideoMME, MVBench, LongVideoBench, MMVU, VideoMMMU, MVP, Charades-STA, ActivityNet, NExT-GQA + image bench (MathVista, MathVision, MathVerse, MMMU, MMMU-Pro, MM-Vet). 
- **Result:** A clear win in terms of inference efficiency. Results are mixed in terms of accuracy. On reasoning benchmarks like VideoMMMU, the "think" activation rate is 51%, with a gain of +3.9. On LongVideoBench, MMVU, and VideoMME, performance is mostly flat or even slightly lower.
- **Contribution:** The ablation study demonstrates that "always-think" is not the answer. However, it is more accurate to view the auto-mode as efficient rather than one that improves absolute performance. The framing of "confidence-based early-exit gating" is elegant.
- **etc.:** I wonder if it makes studying more efficient.
- CVPR 2026. It’s a bit surprising that they didn’t use cold-start SFT—it seems they maintained instruction following by using the instruction-tuned model as-is. KAUST group.

## Details

<img width="1116" height="591" alt="Image" src="https://github.com/user-attachments/assets/93958127-4785-442e-8998-71ef9096473a" />


### motivation

<img width="1142" height="460" alt="Image" src="https://github.com/user-attachments/assets/586d816c-a701-4362-84a0-fd18bc16ccc0" />

- benchmarks
  - VideoMME 
- [VideoMMMU](https://arxiv.org/pdf/2501.13826): Lecture video. It is essentially very similar to the Text Reasoning Benchmark.
- [LongVideoBench](https://arxiv.org/pdf/2407.15754): Hmm, it’s underperforming on LongVideoBench too.  => This seems to be because the benchmark itself focuses primarily on perception and relationships.
- [MMVU](https://arxiv.org/pdf/2501.12380): Unlike VideoMMMU, this is a benchmark that requires knowledge, even though the videos aren't lectures. -- I'm not really sure why the COT is so low for this one.
  - Charades-STA: temporal grounding task 
- models
  - [Video-R1](https://arxiv.org/pdf/2503.21776) / Qwen2.5-VL-7B / Video-R1-CoT-165k (SFT / distil from Qwen2.5-VL-72B-Instruct) + Video-R1-260k (RL) / https://github.com/tulerfeng/Video-R1  
  - [Time-R1](https://arxiv.org/pdf/2503.13377) / Qwen2.5-VL-7B / temporal Grounding   
  - [VideoChat-R1](https://arxiv.org/abs/2504.06958) / spatio-temporal perception
  - [VideoChat-R1.5](https://arxiv.org/abs/2509.21100) / VTTS-80K (15K temporal + 30K spatial clues, 80K Think annotations, 50K QA), Iterative Perception + GRPO
- Below is what cc hallucinated...
- Based on Temporal-RLT / Qwen-VL-2.5-7B / MCQA (semantic reasoning) + temporal grounding (tIoU), dual reward + sample/selection/dynamic data / https://arxiv.org/abs/2506.01908 / https://huggingface.co/datasets/appletea2333/temporal_r1
- Video-RFT / Qwen2.5-VL (3B/7B) / VideoRFT-CoT-102K (SFT) + VideoRFT-RL-310K (RL), built in-house using a multi-expert, cognition-inspired CoT pipeline -- wen2.5-VL-72B-Instruct / https://huggingface.co/datasets/QiWang98/VideoRFT-Data
   - Video-RTS / Qwen2.5-VL-7B / ?
    - VITAL / (VITAL-7B; ByteDance·Tsinghua) /  MTVR-CoT-72k (SFT) + MTVR-RL-110k (RL), DGRPO(difficulty-aware GRPO) / https://huggingface.co/datasets/zhang9302002/MultiTaskVideoReasoning
- [LongVILA-R1](https://arxiv.org/abs/2507.07966)/ VILA/NVILA series / LongVideo-Reason 104K QA (sports, games, vlogs, etc.); 36K Long-CoT-SFT, 68K + additional 102K video data for RL (figures vary by version: 52K/18K/33K+110K, etc.)
    - [LOVE-R1](https://arxiv.org/abs/2509.24786)  / Qwen2.5-VL / Zoom in data



### method

<img width="1164" height="469" alt="Image" src="https://github.com/user-attachments/assets/2bf89d59-c5cf-40f6-a088-59673e0fd551" />

- two-pass decoding, with the format explicitly defined as `answer → think → answer`
- 1st pass: The system prompt is set to "FIRST: Output your initial answer inside the first `\boxed{...}` without any analysis or explanations." If the model cannot produce an answer, it is instructed to output `\boxed{Let's analyze the problem step by step.}` — that is, the model must express its intention to defer by generating the corresponding tokens.
- confidence: The length-normalized mean log probability of the answer tokens within the first `\boxed{}`. Gating is performed by comparing this value to the threshold $\tau$.
- If the confidence is high and it is not a fallback string → early exit (think omitted).
  - <img width="402" height="81" alt="Image" src="https://github.com/user-attachments/assets/1a8b3a68-5029-4552-82d7-99c153ed3775" />
- If confidence is low or it is a fallback string → THEN: generate a think trace, then place the reviewed answer $a_2$ in the second `\boxed{}`.
- No "think" or "no-think" labeling during training — gating is determined only at inference time. Existing approaches like AdaptThink explicitly mix "think" and "no-think" samples during on-policy training, but this is said to introduce issues with data balancing and hyperparameter sensitivity.
- reward
  - $R = w_1 R_{\text{task}}(a_1) + w_2 R_{\text{task}}(a_2) + \lambda R_{\text{fmt}} + \alpha R_{\text{fallback}}$
- $w_1 = 0.9, w_2 = 1.1$ — Since $w_2 > w_1 \geq 0$, the reviewed answer is assigned a higher weight, leading to refinement. The ratio of 0.9:1.1 is specified in the main text.
- $\lambda_{\text{fmt}} = 1.0$ — reward for maintaining the "answer → think → answer" format
- $\alpha = 0.3$ (fallback bonus): An additional reward when $a_1$ is exactly "Let's analyze the problem step by step" and $a_2$ is the correct answer. In other words, it provides an incentive for the model to determine that "this requires reasoning."
- task reward
- QA: binary {0, 1} (math-verify or string match)
  - temporal grounding: continuous [0, 1] (temporal IoU)
- Grounding QA: Both [0, 2]

If this training is successful, the model will learn to consistently produce a "concise first answer + reasoned second answer" pattern.

### data
- 137K → 83K (removed entries where all 8 rollouts were either all correct or all incorrect)
- text 6.4K — DAPO-Math
- image 27.5K — ViRL, ThinkLite-Hard
- video 49.4K — Video-R1, TVBench, STI-Bench, MMR-VBench, Charades-STA, ActivityNet, Time-R1, NExT-GQA

### training recipe
- GRPO, 32× H100, 35 hours, 1 epoch, batch size 256
- KL penalty coefficient $\beta = 0.01$ (no dropout)
- 4096 video token / max 256 frame

### result

<img width="1127" height="628" alt="Image" src="https://github.com/user-attachments/assets/1d7fee4f-fce0-4f1e-a047-8fceda30bc68" />

- Performance on perception benchmarks is mostly average or even slightly below average. Compared to the Qwen3-VL-8B base model, VideoMME scores dropped from 72.5 to 71.7, and LongVideoBench from 67.6 to 67.4 — on perception- and relation-focused benchmarks like LongVideoBench, "thinking" doesn't seem to help much. Although LongVideoBench includes referred reasoning by definition, this is likely because frame-grounded perception ultimately plays a larger role.
- Improvements were observed in VideoMMMU and Charades-STA (temporal grounding). There are also cases where "think" directly helps, such as Charades-STA 59.8.
- VideoAuto-R1's own think ratio is 41% / average response length is 44 tokens — the efficiency gain is clear.
- However, in terms of accuracy, rather than simply stating that it "performs better" than "always-think," it would be more accurate to say that it provides "much shorter responses with similar accuracy."


<img width="1145" height="511" alt="Image" src="https://github.com/user-attachments/assets/0dbcb9f2-0026-45bb-8a4c-3d086fd7f9fd" />

<img width="1164" height="777" alt="Image" src="https://github.com/user-attachments/assets/d1fb80bd-7f00-421c-a4e1-e0f4d2df174f" />
