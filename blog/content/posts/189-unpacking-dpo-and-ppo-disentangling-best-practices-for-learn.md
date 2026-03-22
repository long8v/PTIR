---
title: "Unpacking DPO and PPO: Disentangling Best Practices for Learning from Preference Feedback"
date: 2024-08-27
tags: ['RL', 'AI2', '2024Q2']
paper: "https://arxiv.org/abs/2406.09279"
issue: 189
issueUrl: "https://github.com/long8v/PTIR/issues/189"
summary: "PPO / DPO comparison paper - 1) PPO is better than DPO 2) Bigger RM is better, but RM metrics are not necessarily good downstream 3) Good quality and quantity of synthetic preference data is good 4) Among them, Ultra-F with finegrained grades (itemized scores) is good 5) What increases with RLHF is Truthfulness, instruction following ability 6) PPO increases reasoning, coding, safety. 7) Prompts should be diversified to suit the downstream task, but it was not possible to generalize for small RMs."
---
<img width="606" alt="image" src="https://github.com/user-attachments/assets/62f328b2-1cae-4ff1-8235-328c5dbf3e6f">

[paper](https://arxiv.org/abs/2406.09279)

## TL;DR
- **I read this because... :** PPO / DPO Comparison Paper
- **task :** RL
- **problem :** Ablation of PPO, DPO, RM model size, RM data, prompt in PPO (what questions to ask and roll out), etc.
- **architecture :** TULU 2 13B(LLama2 finetuned)
- **objective :** PPO / DPO loss 
- **baseline :** TULU 2 SFT
- **data :** preference data human-annotated(HH-RLHF, HelpSteer, Chatbot Arena 2023-4, AlpacaFarm human, PRM600k), Web-scraping(SHP-2, StackExchange), synthetic(Ultra-Feedback, Nectrar, Orca, Capybara, AlapacaFarm GPT-4) 
- **evaluation :** factuality(MMLU), reasoning(GSM8k, Big Bench Hard), truthfulness(TruthfulQA), coding(HumanEval+, MBPP+), safety(ToxiGen, XSTest), instruction folloiwng(AlpacaEval 1,2, IFEval) 
- **result :** 1) PPO is better than DPO 2) Bigger RM is better, but RM metrics are not necessarily good downstream 3) Good quality and quantity of synthetic preference data is good 4) Among them, Ultra-F with fine-grained grades (itemized scores) is good 5) RLHF increases Truthfulness, instruction following ability 6) PPO increases reasoning, coding, safety. 7) Prompts should be diversified to suit the downstream task, but it was not possible to generalize for small RMs.
- **contribution :**
- **etc. :**

## Details
- overall 
<img width="818" alt="image" src="https://github.com/user-attachments/assets/1f258475-0a81-4c50-a28a-ba4b2b49e8d8">

- PPO vs DPO 
<img width="800" alt="image" src="https://github.com/user-attachments/assets/e0b3e610-8fbf-40e2-8b65-d4bbefefe3e3">

 - Preference data for DPO
<img width="726" alt="image" src="https://github.com/user-attachments/assets/6b5bce62-010a-4bbe-bc20-080d86db1a26">

Coming out of the DPO as synthetic >> human.
Even when quantities are similar... Is synthetic more consistent than human?
UltraFeedback (fine-grained, domain-specific scoring) worked best for us.

- DPO vs PPO
 
<img width="721" alt="image" src="https://github.com/user-attachments/assets/5f3d13de-a6c5-435d-9299-0367a4c008a6">

Compared to DPO, the areas that stand out are reasoning, coding, safety
Especially with crawled data like stackexchange, I didn't increase my coding skills in DPO, but I did in PPO.
PPOs seem to have better chain-of-thought skills, which may be due to increased comprehension reasoning.

- reward model
<img width="717" alt="image" src="https://github.com/user-attachments/assets/119393d6-ceda-432d-8ef2-db2dcb5ec40e">

RM was run with datasets including UltraFeedback, where Mix performed best, but using more Reward datasets performed better on RM metrics.
The evaluation of the reward model itself and the evaluation when going to the PPO did not correspond.
Some metrics showed 13B Mix RM as the best, when in fact it was not. The 70B RM had significantly better RM metrics than the 13B model, but the performance in PPO was no better or about the same.

- policy training prompt 
<img width="728" alt="image" src="https://github.com/user-attachments/assets/4db92739-945b-4dd4-94aa-38f0b42d1c74">

The prompt used for learning PPOs should be closer to downstream.

