---
title: "[225] VideoAuto-R1: Video Auto Reasoning via Thinking Once, Answering Twice"
date: 2026-06-09
tags: []
paper: "https://arxiv.org/abs/2601.05175"
issue: 249
issueUrl: "https://github.com/long8v/PTIR/issues/249"
---
<img width="847" height="263" alt="Image" src="https://github.com/user-attachments/assets/04d9a7fe-8354-487f-848e-6941ae3693d7" />


[paper](https://arxiv.org/abs/2601.05175)

## TL;DR
- **I read this because.. :** video + think 
- **task :** video reasoning 
- **problem :** CoT가 video QA에서 항상 도움되지 않음 -- 어떻게 균형 잡히게 학습 할 것인가? 
- **idea :** 학습할 때 무조건 즉답 과 Think 후 대답 두번 하게 함. inference 시에는 answer token의 log prob으로 confidence 매긴 후 think를 enable하게 함 
- **input/output :** {video, question} -> {initial boxed answer, (optional reasoning), reviewed boxed answer}
- **architecture :** Qwen2.5-VL-7B-Instruct / Qwen3-VL-8B-Instruct. visual encoder frozen, projector + LLM만 학습. 최대 4096 video token, 256 frame.
- **objective :** GRPO. cold-start SFT 없이 바로 RL.
- **baseline :** Video-R1 (주로 spatial 위주 학습), Time-R1, VideoChat-R1, VideoChat-R1.5, VITAL, LongVILA-R1, LOVE-R1 / base Qwen2.5-VL-7B, Qwen3-VL-8B. 
- **data :** RL 83K (137K에서 8 rollout all-correct/all-wrong 제거). text 6.4K (DAPO-Math) / image 27.5K (ViRL, ThinkLite-Hard) / video 49.4K (Video-R1, TVBench, STI-Bench, MMR-VBench, Charades-STA, ActivityNet, Time-R1, NExT-GQA)
- **evaluation :** VideoMME, MVBench, LongVideoBench, MMVU, VideoMMMU, MVP, Charades-STA, ActivityNet, NExT-GQA + image bench (MathVista, MathVision, MathVerse, MMMU, MMMU-Pro, MM-Vet). 
- **result :** inference 시 효율 측면에서 확실한 win. 정확도 측면은 mixed. VideoMMMU 같은 reasoning bench는 think 켜지는 비율 51%, gain +3.9. LongVideoBench / MMVU / VideoMME 는 거의 평이하거나 오히려 살짝 떨어짐.
- **contribution :** "always-think"가 답이 아니라는 걸 ablation으로 보임. 다만 auto-mode 가 absolute 성능을 올린다기보단 efficient하다고 보는 게 정확. confidence 기반 early-exit gating이라는 framing이 깔끔함.
- **etc. :** 학습을 할 때 더 효율적인지가 궁금하네
- CVPR 2026. cold-start SFT 없는 게 좀 신기 — instruction-tuned 모델 그대로 써서 instruction following이 유지되는 듯. KAUST 그룹.

## Details

<img width="1116" height="591" alt="Image" src="https://github.com/user-attachments/assets/93958127-4785-442e-8998-71ef9096473a" />


### motivation

<img width="1142" height="460" alt="Image" src="https://github.com/user-attachments/assets/586d816c-a701-4362-84a0-fd18bc16ccc0" />

- benchmarks
  - VideoMME 
  - [VideoMMMU](https://arxiv.org/pdf/2501.13826): lecture 영상. 사실상 text reasoning bench와 거의 비슷함 
  - [LongVideoBench](https://arxiv.org/pdf/2407.15754): 흠 long video bench 에서도 떨어지네.  => 벤치마크의 능력 자체는 perception + relation 위주여서 인듯 함. 
  - [MMVU](https://arxiv.org/pdf/2501.12380): VideoMMMU와 달리 비디오가 lecture는 아니지만 지식을 요하는 벤치. -- 얘는 왜 cot가 낮은지 잘 모르겠음
  - Charades-STA: temporal grounding task 
- models
  - [Video-R1](https://arxiv.org/pdf/2503.21776) / Qwen2.5-VL-7B / Video-R1-CoT-165k (SFT / distil from Qwen2.5-VL-72B-Instruct) + Video-R1-260k (RL) / https://github.com/tulerfeng/Video-R1  
  - [Time-R1](https://arxiv.org/pdf/2503.13377) / Qwen2.5-VL-7B / temporal Grounding   
  - [VideoChat-R1](https://arxiv.org/abs/2504.06958) / spatio-temporal perception
  - [VideoChat-R1.5](https://arxiv.org/abs/2509.21100) / VTTS-80K (15K temporal + 30K spatial clues, 80K Think annotations, 50K QA), Iterative Perception + GRPO
  - 아래는 cc가 halluci한거 .. 
    - Temporal-RLT / Qwen-VL-2.5-7B / MCQA(semantic reasoning) + temporal grounding(tIoU) 기반, dual reward + sample /selection/dynamic data / https://arxiv.org/abs/2506.01908 / https://huggingface.co/datasets/appletea2333/temporal_r1  
  - Video-RFT / Qwen2.5-VL (3B/7B) / VideoRFT-CoT-102K (SFT) + VideoRFT-RL-310K (RL), multi-expert·cognition-inspired CoT 파이프라인으로 자체 구축 -- wen2.5-VL-72B-Instruct / https://huggingface.co/datasets/QiWang98/VideoRFT-Data
    - Video-RTS / Qwen2.5-VL-7B / ?
    - VITAL / (VITAL-7B; ByteDance·Tsinghua) /  MTVR-CoT-72k (SFT) + MTVR-RL-110k (RL), DGRPO(difficulty-aware GRPO) / https://huggingface.co/datasets/zhang9302002/MultiTaskVideoReasoning
    - [LongVILA-R1](https://arxiv.org/abs/2507.07966)/ VILA/NVILA 계열 /  LongVideo-Reason 104K QA (sports/games/vlogs 등); 36K Long-CoT-SFT, 68K + 추가 102K video data로 RL (버전별로 52K/18K/33K+110K 등 수치 변동)
    - [LOVE-R1](https://arxiv.org/abs/2509.24786)  / Qwen2.5-VL / Zoom in data



### method

<img width="1164" height="469" alt="Image" src="https://github.com/user-attachments/assets/2bf89d59-c5cf-40f6-a088-59673e0fd551" />

- two-pass decoding, format은 명시적으로 `answer → think → answer`
  - 1st pass: system prompt가 "FIRST: Output your initial answer inside the first `\boxed{...}` without any analysis or explanations" 로 강제. answer를 못 낼 것 같으면 `\boxed{Let's analyze the problem step by step.}` 를 출력하도록 지시 — 즉 모델이 스스로 defer 의사를 토큰으로 표현.
  - confidence: 첫 번째 `\boxed{}` 안 answer 토큰들의 length-normalized mean log probability. threshold $\tau$ 와 비교해서 gating.
  - confidence 높고 fallback 문자열이 아니면 → early-exit (think 생략).
  - <img width="402" height="81" alt="Image" src="https://github.com/user-attachments/assets/1a8b3a68-5029-4552-82d7-99c153ed3775" />
  - confidence 낮거나 fallback 문자열이면 → THEN: think trace 생성 후 두 번째 `\boxed{}` 에 reviewed answer $a_2$.
  - 학습 중 think / no-think 라벨링 없음 — gating은 inference time에만 결정. AdaptThink 같은 기존 접근은 on-policy training 중 think/no-think 샘플을 명시적으로 섞는데, 그건 data balancing과 hyperparameter sensitivity 이슈가 있다고 함.
- reward
  - $R = w_1 R_{\text{task}}(a_1) + w_2 R_{\text{task}}(a_2) + \lambda R_{\text{fmt}} + \alpha R_{\text{fallback}}$
  - $w_1 = 0.9, w_2 = 1.1$ — $w_2 > w_1 \geq 0$ 로 reviewed answer에 더 큰 weight 부여, refinement 유도. ratio 0.9:1.1 이 본문에 명시.
  - $\lambda_{\text{fmt}} = 1.0$ — answer → think → answer 포맷 유지 reward
  - $\alpha = 0.3$ (fallback bonus): $a_1$ 이 정확히 "Let's analyze the problem step by step" 이고 $a_2$ 가 정답일 때 추가 보상. 즉 모델이 "이건 reasoning 필요하다" 고 판단하는 행위 자체에 인센티브.
- task reward
  - QA: binary {0, 1} (math-verify 또는 string match)
  - temporal grounding: continuous [0, 1] (temporal IoU)
  - grounding QA: 둘 합 [0, 2]

이 학습이 잘 되면 모델이 "concise first answer + reasoned second answer" 를 안정적으로 내는 패턴을 학습함.

### data
- 137K → 83K (8 rollout 다 맞거나 다 틀린 거 제거)
- text 6.4K — DAPO-Math
- image 27.5K — ViRL, ThinkLite-Hard
- video 49.4K — Video-R1, TVBench, STI-Bench, MMR-VBench, Charades-STA, ActivityNet, Time-R1, NExT-GQA

### training recipe
- GRPO, 32× H100, 35시간, 1 epoch, batch size 256
- KL penalty coefficient $\beta = 0.01$ (제거 안 함)
- 4096 video token / max 256 frame

### result

<img width="1127" height="628" alt="Image" src="https://github.com/user-attachments/assets/1d7fee4f-fce0-4f1e-a047-8fceda30bc68" />

- perception bench는 거의 평이하거나 오히려 약간 떨어짐. Qwen3-VL-8B base 기준 VideoMME 72.5 → 71.7, LongVideoBench 67.6 → 67.4 — long video bench 같은 perception+relation 위주 벤치는 thinking이 별 도움 안 됨. LongVideoBench 정의상 referred reasoning이 들어가긴 하지만 결국 frame-grounded perception 비중이 커서 그럴 듯.
- VideoMMMU  와 Charades-STA (temporal grounding) 에선 개선. Charades-STA 59.8 처럼 think가 직접 도움 되는 케이스도 있음.
- VideoAuto-R1 자체의 think ratio 41% / 평균 응답 길이 44 token — efficiency gain은 확실.
  - 다만 정확도 측면에서 보면 always-think 대비 한 줄로 "성능이 더 좋다" 라고 단언하기보단, "비슷한 정확도에 훨씬 짧은 응답" 으로 보는 게 정확.


<img width="1145" height="511" alt="Image" src="https://github.com/user-attachments/assets/0dbcb9f2-0026-45bb-8a4c-3d086fd7f9fd" />

<img width="1164" height="777" alt="Image" src="https://github.com/user-attachments/assets/d1fb80bd-7f00-421c-a4e1-e0f4d2df174f" />

- MVBench (perception 위주) — mean prob 94.8, think 25%, gain +0.1
- VideoMMMU (reasoning heavy) — mean prob 87.4, think 51%, gain +4.0
→ 어려운 태스크에서 think 켜지는 자동 gating이 의도대로 동작.

- Table 7:
  - reward weight ablation (Table 7 부근): $w_1 : w_2 = 0.9 : 1.1$ 이 최적. $w_1 > w_2$ 로 가면 모델이 reasoning 안 거치고 일찍 답을 굳히려 함.

