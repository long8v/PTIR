---
title: "[213] Skywork-R1V3 Technical Report"
date: 2025-07-11
tags: ['MLLM', 'reasoning', '2025Q3']
paper: "https://arxiv.org/abs/2507.06167"
issue: 234
issueUrl: "https://github.com/long8v/PTIR/issues/234"
---
<img width="880" height="271" alt="Image" src="https://github.com/user-attachments/assets/293ec347-db40-4f3f-95cf-e839eb12851a" />

[paper](https://arxiv.org/abs/2507.06167), [model](https://huggingface.co/Skywork/Skywork-R1V3-38B), [code](https://github.com/SkyworkAI/Skywork-R1V)

## TL;DR
- **I read this because.. :** skywork 시리즈인데 entropy 얘기가 있어서.
- **task :** multimodal reasoning model 
- **problem :** MLLM의 closed model과의 gap이 더 큼 
- **idea :** projector만 학습하고자 하는 것은 이전 시리즈(https://github.com/long8v/PTIR/issues/232) 와 이어짐. 여러 가지 레시피와 분석을 넣은 논문.
- **input/output :** {image/text, prompt} -> {reasoning, answer}
-  **architecture :** InternVL-38B 
-  **objective :** CE loss (SFT), GRPO loss (RL), entropy-guided checkpoint selection
-  **baseline :** InternVL3-78B, Qwen2.5-VL-72B, GPT-4o, Claude 3.7, QVQ-72B
- **data :** cold-start STEM QA (12K), math RL data (15K), multi-domain connector tuning (10K)
-  **evaluation :** 20+ benchmarks (MMMU, MathVista, LogicVista, PhyX 등) using VLMEvalKit
- **result :** open-source 중 SOTA (MMMU 76.0%), reasoning transfer와 generalization 입증
-  **contribution :** critical token entropy 지표 제안, connector 역할 강조, RL 분석 및 ablation 제공
- **etc. :** slow-thinking > fast-thinking, reasoning hallucination 이슈 발견, connector tuning만 효과적

## details
- thumbnail

<img width="841" height="470" alt="Image" src="https://github.com/user-attachments/assets/1a1b2720-90e8-4884-a976-0cc006abafb6" />

- data preparation
  - <img width="867" height="294" alt="Image" src="https://github.com/user-attachments/assets/faabd0c2-993d-4d21-95d7-05327761ee02" /> 
  - LongCoT:  20K Chinese high-school difficulty -- Skywork r1v2 rejection sampling (final answer) --> 12K 
  - GRPO : K-12 level 15K high quality math data --> entire multi-choice, fill-in-the-blank 
  - Data for connector only : 20 domains 10K
  - <img width="836" height="160" alt="Image" src="https://github.com/user-attachments/assets/0b5dd479-fd80-487b-b60a-b130d0ab826c" /> 

- Post-Training Recipes
  - reward: format, accuracy reward
  - cold start sft
    -  thousands of cold-start samples from an early internal version of Skywork-R1V2
    - employed the Skywork-VL-Reward (Wang et al., 2025d) alongside GPT-4o to filter rambling and overly
lengthy samples, resulting in a refined cold-start dataset 
- vision lanuage benchmark performance
  - vlmevalkit을 사용하되 task별로 조금 가다듬었다고 하는데 곧 오픈소스할거라고 함 
  - <img width="656" height="379" alt="Image" src="https://github.com/user-attachments/assets/dc1c6d06-6154-4acf-bd2f-98977c2d18f6" />

- Empirical Analysis on Reinforcement Learning
  - Critical Token Entropy Indicates Reasoning Ability
  - <img width="678" height="245" alt="Image" src="https://github.com/user-attachments/assets/b4967224-0064-453e-b29f-c8adbe923949" />
  - cold start CoT SFT만 하는 경우 reasoning을 하는 척만 하고 실제로는 generalizable reasoning 능력은 발현되고 있지 않다고 함( repeating existing patterns rather than truly activating generalizable reasoning capabilities) 
  - 이를 측정하기 위해 critical token(wait, alteratively 등)의 entropy를 계산하고 이를 체크포인트 측정하는데 사용했다고 함 (mmmu 성능과 correlation이 높음)
- The Connector Module Activation is Vital in RL
  - <img width="631" height="264" alt="Image" src="https://github.com/user-attachments/assets/f0382d82-083f-4c20-957e-552f7a5390ba" />
- The Distribution Shift in Curriculum Learning Hinder Generalization
  - <img width="627" height="270" alt="Image" src="https://github.com/user-attachments/assets/b03a3188-6e78-4f5b-8733-094001177e99" />
  - K12 -> competition 난이도로 한번 옮기는 작업을 했는데 높은 난이도에 대한 성능은 오르나 normal 난이도는 떨어지고 pyhsics, logics는 유지되는 경향성.
  - hard problem에서 필요한 복잡한 skill, special pattern, high-level strategy가 normal level에선 충돌하는듯한 경향성 
- RL stage 이후에 여러 도메인 학습하는 공정에서 component freeze ablation
  - <img width="581" height="115" alt="Image" src="https://github.com/user-attachments/assets/0e77b185-fbb8-4aa5-8ba0-bca3dd4dd733" />

- Discussion
 - <img width="515" height="131" alt="Image" src="https://github.com/user-attachments/assets/0351366f-a18a-4334-ace5-218bbfe4cae9" />
 - math-only로 SFT와 RL을 했을 때의 in-domain (mathvista), out-of-domain (mmmu) 성능 차이
 - SFT는 generalize가 안되고 RL은 됨 (https://github.com/long8v/PTIR/issues/230)
- thinking budget
  -  <img width="638" height="428" alt="Image" src="https://github.com/user-attachments/assets/9081565b-dcda-4548-9e44-c5eb8ac6d576" />
  - <img width="607" height="103" alt="Image" src="https://github.com/user-attachments/assets/b681cb06-95d8-4ab1-88fa-51e0b143886d" />
- Hallucination in Skywork-R1V3’s Chain-of-Thought Impairs Reasoning Performance 
  - <img width="445" height="284" alt="Image" src="https://github.com/user-attachments/assets/169199b5-d6f6-4b61-adff-bb608f8cc0b2" />
- Analysis on Entropy Token in Visual Reasoning Task
  - <img width="439" height="226" alt="Image" src="https://github.com/user-attachments/assets/cecb558d-6f9a-421e-b3d8-239f966dda18" />
  - 학습이 진행됨에 따라 전반적인 토큰의 엔트로피는 낮아지나(determinisitic 해지나) 높은 엔트로피를 가진 토큰들의 확률은 높아짐.
  - 즉, wait, ... 과 같은 delibration token들이 더 많이 나오는 방향으로 학습됨 
  - The Entropy Mechanism of Reinforcement Learning for Reasoning Language Models https://arxiv.org/pdf/2505.22617
  - Beyond the 80/20 Rule: High-Entropy Minority Tokens Drive Effective Reinforcement Learning for LLM Reasoninghttps://arxiv.org/abs/2506.01939