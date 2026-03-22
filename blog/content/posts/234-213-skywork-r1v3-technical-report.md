---
title: "[213] Skywork-R1V3 Technical Report"
date: 2025-07-11
tags: ['MLLM', 'reasoning', '2025Q3']
paper: "https://arxiv.org/abs/2507.06167"
issue: 234
issueUrl: "https://github.com/long8v/PTIR/issues/234"
summary: "It's a skywork series and we're talking about entropy. - Propose critical token entropy metrics, emphasize connector role, provide RL analysis and ablation"
---
<img width="880" height="271" alt="Image" src="https://github.com/user-attachments/assets/293ec347-db40-4f3f-95cf-e839eb12851a" />

[paper](https://arxiv.org/abs/2507.06167), [model](https://huggingface.co/Skywork/Skywork-R1V3-38B), [code](https://github.com/SkyworkAI/Skywork-R1V)

## TL;DR
- **I read this because.. :** It's a skywork series, and it talks about entropy.
- **task :** multimodal reasoning model 
- **problem :** The gap with the closed model of MLLM is bigger
- **IDEA :** Continuation of the previous series (https://github.com/long8v/PTIR/issues/232) where we only want to learn projectors. A paper with several recipes and analysis.
- **input/output :** {image/text, prompt} -> {reasoning, answer}
-  **architecture :** InternVL-38B 
-  **objective :** CE loss (SFT), GRPO loss (RL), entropy-guided checkpoint selection
-  **baseline :** InternVL3-78B, Qwen2.5-VL-72B, GPT-4o, Claude 3.7, QVQ-72B
- **data :** cold-start STEM QA (12K), math RL data (15K), multi-domain connector tuning (10K)
- **evaluation :** 20+ benchmarks (MMMU, MathVista, LogicVista, PhyX, etc.) using VLMEvalKit
- **result :** SOTA among open-source (MMMU 76.0%), demonstrating reasoning transfer and generalization
- **contribution :** Proposed critical token entropy metric, highlighted connector role, provided RL analysis and ablation
- **etc. :** slow-thinking > fast-thinking, reasoning hallucination issue found, connector tuning is only effective

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
- Use vlmevalkit, but refine it a bit per task, and will open source it soon
  - <img width="656" height="379" alt="Image" src="https://github.com/user-attachments/assets/dc1c6d06-6154-4acf-bd2f-98977c2d18f6" />

- Empirical Analysis on Reinforcement Learning
  - Critical Token Entropy Indicates Reasoning Ability
  - <img width="678" height="245" alt="Image" src="https://github.com/user-attachments/assets/b4967224-0064-453e-b29f-c8adbe923949" />
- If you only do cold start CoT SFT, you are only pretending to reason and not really activating generalizable reasoning capabilities (repeating existing patterns rather than truly activating generalizable reasoning capabilities).
- To measure this, they calculated the entropy of critical tokens (wait, alteratively, etc.) and used it to measure checkpointing (which correlates well with MMMU performance)
- The Connector Module Activation is Vital in RL
  - <img width="631" height="264" alt="Image" src="https://github.com/user-attachments/assets/f0382d82-083f-4c20-957e-552f7a5390ba" />
- The Distribution Shift in Curriculum Learning Hinder Generalization
  - <img width="627" height="270" alt="Image" src="https://github.com/user-attachments/assets/b03a3188-6e78-4f5b-8733-094001177e99" />
- We moved from K12 -> competition difficulty once, and performance on high difficulty tends to increase, but normal difficulty tends to decrease, while pyhsics and logics remain the same.
- Complex skills, special patterns, and high-level strategies required for hard problems tend to clash at a normal level.
- Component freeze ablation in the process of learning multiple domains after the RL stage
  - <img width="581" height="115" alt="Image" src="https://github.com/user-attachments/assets/0e77b185-fbb8-4aa5-8ba0-bca3dd4dd733" />

- Discussion
 - <img width="515" height="131" alt="Image" src="https://github.com/user-attachments/assets/0351366f-a18a-4334-ace5-218bbfe4cae9" />
- In-domain (mathvista) and out-of-domain (mmmu) performance differences between SFT and RL with math-only
- SFT does not generalize, RL does (https://github.com/long8v/PTIR/issues/230)
- thinking budget
  -  <img width="638" height="428" alt="Image" src="https://github.com/user-attachments/assets/9081565b-dcda-4548-9e44-c5eb8ac6d576" />
  - <img width="607" height="103" alt="Image" src="https://github.com/user-attachments/assets/b681cb06-95d8-4ab1-88fa-51e0b143886d" />
- Hallucination in Skywork-R1V3’s Chain-of-Thought Impairs Reasoning Performance 
  - <img width="445" height="284" alt="Image" src="https://github.com/user-attachments/assets/169199b5-d6f6-4b61-adff-bb608f8cc0b2" />
- Analysis on Entropy Token in Visual Reasoning Task
  - <img width="439" height="226" alt="Image" src="https://github.com/user-attachments/assets/cecb558d-6f9a-421e-b3d8-239f966dda18" />
- As training progresses, the overall entropy of tokens decreases (determinisitic termination), but the probability of tokens with high entropy increases.
- In other words, it will be trained in the direction of more delibration tokens such as wait, ...
  - The Entropy Mechanism of Reinforcement Learning for Reasoning Language Models https://arxiv.org/pdf/2505.22617
  - Beyond the 80/20 Rule: High-Entropy Minority Tokens Drive Effective Reinforcement Learning for LLM Reasoninghttps://arxiv.org/abs/2506.01939