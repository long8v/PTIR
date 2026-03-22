---
title: "[170] Unpacking DPO and PPO: Disentangling Best Practices for Learning from Preference Feedback"
date: 2024-08-27
tags: ['RL', 'AI2', '2024Q2']
paper: "https://arxiv.org/abs/2406.09279"
issue: 189
issueUrl: "https://github.com/long8v/PTIR/issues/189"
---
<img width="606" alt="image" src="https://github.com/user-attachments/assets/62f328b2-1cae-4ff1-8235-328c5dbf3e6f">

[paper](https://arxiv.org/abs/2406.09279)

## TL;DR
- **I read this because.. :** PPO / DPO 비교 논문 
- **task :** RL
- **problem :** PPO, DPO, RM 모델의 크기, RM data, PPO에서 prompt(어떤 질문을 주고 rollout 시킬건지) 등에 대한 ablation
- **architecture :** TULU 2 13B(LLama2 finetuned)
- **objective :** PPO / DPO loss 
- **baseline :** TULU 2 SFT
- **data :** preference data human-annotated(HH-RLHF, HelpSteer, Chatbot Arena 2023-4, AlpacaFarm human, PRM600k), Web-scraping(SHP-2, StackExchange), synthetic(Ultra-Feedback, Nectrar, Orca, Capybara, AlapacaFarm GPT-4) 
- **evaluation :** factuality(MMLU), reasoning(GSM8k, Big Bench Hard), truthfulness(TruthfulQA), coding(HumanEval+, MBPP+), safety(ToxiGen, XSTest), instruction folloiwng(AlpacaEval 1,2, IFEval) 
- **result :** 1) DPO보다 PPO가 좋다 2) RM은 클수록 좋지만 RM 지표가 꼭 다운 스트림에서 좋은 것은 아니다 3) 질 좋고 양좋은 synthetic preference data가 좋다 4) 그중에는 finegrained 성적(항목별 점수)를 내는 Ultra-F가 좋다 5) RLHF로 늘어나는 것은 Truthfulness, instruction following 능력이다 6) PPO에서는 reasoning, coding, safety가 늘어났다. 7) prompt는 down stream task에 맞게 다양화하면 좋으나 작은 RM에 대해선 generalize를 못해서 일반화를 하지 못했다. 
- **contribution :**
- **etc. :**

## Details
- overall 
<img width="818" alt="image" src="https://github.com/user-attachments/assets/1f258475-0a81-4c50-a28a-ba4b2b49e8d8">

- PPO vs DPO 
<img width="800" alt="image" src="https://github.com/user-attachments/assets/e0b3e610-8fbf-40e2-8b65-d4bbefefe3e3">

 - Preference data for DPO
<img width="726" alt="image" src="https://github.com/user-attachments/assets/6b5bce62-010a-4bbe-bc20-080d86db1a26">

DPO에서 synthetic >> human 으로 나옴. 
수량이 비슷한 경우에도 그렇네.. human보다 synthetic이 더 일관적인건가?
개중에는 UltraFeedback (fine-grained하게 영역별로 점수를 낸 것)이 가장 효과가 좋았음. 

- DPO vs PPO
 
<img width="721" alt="image" src="https://github.com/user-attachments/assets/5f3d13de-a6c5-435d-9299-0367a4c008a6">

DPO 대비 두드러지는 부문은 reasoning, coding, safety 
특히 stackexchange 같은 crawled data가 DPO에서는 coding 실력을 늘리지 못했는데 PPO는 늘렸음. 
PPO가 chain-of-thought 능력이 더 뛰어난 것 같고 이로 이해 reasoning 능력이 늘어난게 아닐까 하는 분석

- reward model
<img width="717" alt="image" src="https://github.com/user-attachments/assets/119393d6-ceda-432d-8ef2-db2dcb5ec40e">

Mix가 가장 성능이 좋았던 UltraFeedback을 포함한 데이터셋으로 RM을 한건데 더 많은 Reward dataset을 쓰는게 RM 지표 상 성능이 좋았음.
reward model 자체의 평가랑 PPO 까지 갔을 때 평가가 상응하지 않았음.  
13B Mix RM이 가장 좋게 나온 지표도 있었는데 실제로 그렇지 않았음. 70B RM이 13B모델 보다 rm 지표는 상당히 좋았는데, PPO에서의 성능은 개선이 없거나 거의 비슷했음.

- policy training prompt 
<img width="728" alt="image" src="https://github.com/user-attachments/assets/4db92739-945b-4dd4-94aa-38f0b42d1c74">

PPO 학습 시 사용되는 prompt는 downstream에 가까울 수록 좋았음. 

