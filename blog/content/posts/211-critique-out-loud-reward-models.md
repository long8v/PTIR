---
title: "Critique-out-Loud Reward Models"
date: 2024-12-17
tags: ['AllenAI', 'LLM', 'RL', '2024Q3']
paper: "https://arxiv.org/abs/2408.11791"
issue: 211
issueUrl: "https://github.com/long8v/PTIR/issues/211"
summary: "Mentioned in O1 video - seems good in that it makes RM interpretable? Not sure if it will be used much."
---

<img width="807" alt="image" src="https://github.com/user-attachments/assets/8a7d0ddd-d634-4c84-bc63-655ad39b94a4" />

[paper](https://arxiv.org/abs/2408.11791), [code](https://github.com/zankner/CLoud)

## TL;DR
- **I read this because.. :** o1 It was mentioned in the video that the
- **task :** Improve reward model
- **PROBLEM :** I can interpret scores in cases like llm-as-judge, can't reward model do the same?
- **idea :** Have RM create a critique and then put a reward head behind it to predict it.
- **input/output :** {question, answer} -> {critique, reward score}
- **architecture :** Llama-3-8B / 70B
- **objective :** SFT loss + RM loss(Bradley-Terry Model)
- **baseline :** classic RM model
- **data :** UltraLlama (proposed. UltraFeedback + UltraInteract subset as Prompt and Llama-3-8B-Instruct to generate response) + Llama-3.1.-405B-Instruct to generate critique and judgment as oracle
- **evaluation :** pairwise preference classification of Reward Bench, BoW win rate on ArenaHard
- **result :** CLoud technique works in all categories. On policy is always better than off policy. I also tested self-consistency technique, but it is only good for reasoning.
- **contribution :** Good because it makes rm interpretable? Not sure if it will be used much.
- **etc. :**

## Details
- thumbnail

<img width="592" alt="image" src="https://github.com/user-attachments/assets/d8f7c4dc-bd23-4380-b9a7-67a2781f5718" />

Simple. Tell it to create a critique, give it as a given, including the last critique, and attach a reward head to it.
Learn SFT loss and RM loss at once to generate critiques.
<img width="408" alt="image" src="https://github.com/user-attachments/assets/7969dea1-1cfb-4c63-b1eb-58d6117d64bc" />

($\lambda$ is found as 5/4 in 8B and 3/4 in 70B)

<img width="525" alt="image" src="https://github.com/user-attachments/assets/337510e0-85e0-4d7d-8958-27f4824c8caf" />

<img width="486" alt="image" src="https://github.com/user-attachments/assets/971bcbdb-5734-4b23-9613-b61f16c693ba" />

- training overview
<img width="562" alt="image" src="https://github.com/user-attachments/assets/5caf8768-d761-47d2-a93b-7ac5d0f31d8f" />

Initially learning based on oracle ciritque.
oracle uses UltraLlama (proposed. UltraFeedback + UltraInteract subset as Prompt and Llama-3-8B-Instruct to generate response) + Llama-3.1.-405B-Instruct to generate critique and judgment.
(Oracle judgment creation prompt)
<img width="571" alt="image" src="https://github.com/user-attachments/assets/740e24c4-5d6f-4105-8c91-a2e4ef37ae63" />

This is followed by learning based on self-generated critique.
Do you feel like you've only done this once, not N times?

### Result
- What's the point of cloud techniques?
<img width="585" alt="image" src="https://github.com/user-attachments/assets/6052a1ae-084a-4e2a-8d21-197453b80201" />

All are found to be effective. I don't know if it's right to evaluate only RM.

- on-policy vs off-policy
How to continue using oracle critique
<img width="592" alt="image" src="https://github.com/user-attachments/assets/97a7d52a-ac2b-4698-877a-409f5027c6c2" />

On-policy is clearly more effective

- Self-consistency effects
Have them generate multiple reasoning (in this case, critique) and then average the scores behind them.
<img width="546" alt="image" src="https://github.com/user-attachments/assets/e06de765-ffe3-4434-bb90-8121c6a90aab" />

Didn't work except for reasoning.
In addition, ArenaHard has no effect at all

<img width="276" alt="image" src="https://github.com/user-attachments/assets/437d9d85-67e0-475c-8619-d4d42daad519" />

Among the reasoning, it only worked if the reason step was 1 or 2 steps, otherwise none.