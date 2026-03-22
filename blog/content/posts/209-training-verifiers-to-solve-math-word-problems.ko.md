---
title: "[189] Training Verifiers to Solve Math Word Problems"
date: 2024-12-09
tags: ['2021Q4', 'openAI', '25min', 'RL']
paper: "https://arxiv.org/abs/2110.14168"
issue: 209
issueUrl: "https://github.com/long8v/PTIR/issues/209"
---

<img width="800" alt="image" src="https://github.com/user-attachments/assets/c06a5170-7f25-4f6c-bc12-43709eedd8d4">

[paper](https://arxiv.org/abs/2110.14168)

## TL;DR
- **I read this because.. :** ORM(Output Reward Model)이 많이 언급되어. 정확히 이 논문을 말하는지 모르겠지만 Omega PRM논문에서 인용함. 
- **task :** 수학 문제 푸는 LLM
- **problem :** LM 많은 발전이 있었지만 multi-step mathematical reasoning 여전히 못한다. 
- **idea :** 데이터 제안. finetuning후 100개의 sample을 뽑고 label을 매긴 뒤 verifier 학습. 이후 Inference를 여러개 하고 verifier에서 높은 점수를 얻은 것을 최종 정답으로 선택. 
- **architecture :** GPT3 6B / 175B
- **objective :** CE loss / verifier의 경우 Scalar head (bce loss일듯?)
- **baseline :** finetuning 
- **data :** GSM8K (proposed)
- **evaluation :** test solve ratio
- **result :** 175B finetuned 보다 6B 
- **contribution :** gsm8k 제안 / Multi-step math reasoning 문제 해결? / RFT의 전신..? 
- **etc. :**

## Details

<img width="700" alt="image" src="https://github.com/user-attachments/assets/a95a3761-cfa5-4214-9d7d-a969f68410af">

<img width="700" alt="image" src="https://github.com/user-attachments/assets/2a731caa-1f0c-40d9-969a-5085793c963c">

<img width="700" alt="image" src="https://github.com/user-attachments/assets/6f5352eb-b58d-4f7f-a4c1-0d63e3c64cb5">

100 Guess의 경우 빠르게 overfitting. 2 epoch만 보게 함 
<img width="700" alt="image" src="https://github.com/user-attachments/assets/b016c2ae-4940-40f6-9491-bb538cb4557f">
