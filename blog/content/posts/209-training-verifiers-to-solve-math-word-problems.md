---
title: "Training Verifiers to Solve Math Word Problems"
date: 2024-12-09
tags: ['2021Q4', 'openAI', '25min', 'RL']
paper: "https://arxiv.org/abs/2110.14168"
issue: 209
issueUrl: "https://github.com/long8v/PTIR/issues/209"
summary: "Output Reward Model (ORM) is mentioned a lot. Not sure if you mean this paper exactly, but it's from the Omega PRM paper. - GSM8K proposal / Multi-step math reasoning problem solved? / Predecessor of RFT...?"
---

<img width="800" alt="image" src="https://github.com/user-attachments/assets/c06a5170-7f25-4f6c-bc12-43709eedd8d4">

[paper](https://arxiv.org/abs/2110.14168)

## TL;DR
- **I read this because.. :** ORM (Output Reward Model) is mentioned a lot. I don't know if this is the exact paper you are referring to, but it is from the Omega PRM paper.
- **task :** LLM in math problem solving
- **problem :** LM has made a lot of progress, but it still can't do multi-step mathematical reasoning.
- Idea:** Propose data. After finetuning, take 100 samples, label them and train a verifier. After that, make several inferences and select the one that scores high on the verifier as the final answer.
- **architecture :** GPT3 6B / 175B
- **objective :** Scalar head for CE loss / verifier (maybe bce loss?)
- **baseline :** finetuning 
- **data :** GSM8K (proposed)
- **evaluation :** test solve ratio
- **result :** 175B finetuned over 6B
- **contribution :** gsm8k proposal / Multi-step math reasoning problem solved? / Predecessor of RFT...?
- **etc. :**

## Details

<img width="700" alt="image" src="https://github.com/user-attachments/assets/a95a3761-cfa5-4214-9d7d-a969f68410af">

<img width="700" alt="image" src="https://github.com/user-attachments/assets/2a731caa-1f0c-40d9-969a-5085793c963c">

<img width="700" alt="image" src="https://github.com/user-attachments/assets/6f5352eb-b58d-4f7f-a4c1-0d63e3c64cb5">

Fast overfitting for 100 Guess. Only letting people see 2 epochs
<img width="700" alt="image" src="https://github.com/user-attachments/assets/b016c2ae-4940-40f6-9491-bb538cb4557f">
