---
title: "[209] SFT Memorizes, RL Generalizes: A Comparative Study of Foundation Model Post-training"
date: 2025-05-21
tags: ['google', 'RL', 'Berkley', '2025Q1']
paper: "https://arxiv.org/pdf/2501.17161#page=11&zoom=100,384,536"
issue: 230
issueUrl: "https://github.com/long8v/PTIR/issues/230"
---
![Image](https://github.com/user-attachments/assets/97d87cd8-6221-49f5-8ffb-661d4b02f324)

[paper](https://arxiv.org/pdf/2501.17161#page=11&zoom=100,384,536), [page](https://tianzhechu.com/SFTvsRL/)

## TL;DR
- **I read this because.. :** SFT를 너무 많이 하는게 안좋나? + [RL4VLM](https://rl4vlm.github.io/) 저자 후속 연구 
- **task :** card game(GeneralPoints), real-world navigation([V-IRL](https://virl-platform.github.io/))
- **problem :** SFT vs RL의 data memorization 현상에 대한 분석
- **idea :** rule이나 환경을 조금 바꾼 out-of-distribution을 만든 뒤 성능이 어떻게 바뀌는지 분석
- **input/output :** {prompt, (image), previous prediction and result..} -> verifier output 
- **architecture :** Llama-3.2-Vision-11B
- **objective :** SFT loss -> PPO loss
- **baseline :** base model, (V-IRL) chatgpt, claude..
- **data :** (SFT) expert data가 있다는 것 같음 
- **evaluation :** success rate
- **result :** 1) in-domian은 SFT > RL. SFT는 OOD가 떨어지는데 RL은 유지되거나 개선됨 2) instruction following을 하기 위한 SFT는 되어야 함 3) sequential revision으로 넣어주는게 성능에 영향 4) V-IRL은 sota 달성 
- **contribution :** 너무 복잡하지 않고 이해하기 쉬운 Task로 systemically 분석
- **etc. :** VLM도 해줘서 고마웡 ㅜ

## Details
- thumbnail

<img width="367" alt="Image" src="https://github.com/user-attachments/assets/90c52132-e5d0-4a98-bb43-9b4cf46c910f" />

### task 
  - GeneralPoints (4개의 카드를 사용하여 사칙연산을 통해 24를 만드는게임) : LLM / VLM 
    - <img width="728" alt="Image" src="https://github.com/user-attachments/assets/1b64f17f-d303-4c90-b9b6-3a2fcf390ccc" />
    - OOD 
       - Q,K,V를 10으로 보기 vs 11,12,13으로 보기
       - 검정색 카드에서 sampling / 빨간색 카드에서 sampling
  - V-IRL
    -  <img width="691" alt="Image" src="https://github.com/user-attachments/assets/41b83f25-3308-49ae-9572-c1d3ff4e5d80" />
    - city 돌아다니면서 navigation 하는 태스크
    - OOD : 
      - action이 왼쪽으로 돌기 등으로 바뀜.
      - city를 바꿈 
   
- sequential revision input
<img width="688" alt="Image" src="https://github.com/user-attachments/assets/350f21c7-bf84-4830-abf4-43b5a94bb74d" />

### training
  - SFT -> RL
  - RL은 PPO
  - reasoning은 따로 없고 바로 정답 return하는 형태임
  - verifier는 rule-based로 보임 
    - <img width="325" alt="Image" src="https://github.com/user-attachments/assets/34c868b9-3c89-4148-ad79-7cb280457197" />

### result 
- ood performance 
<img width="696" alt="Image" src="https://github.com/user-attachments/assets/43cfedf0-c844-442e-8731-cc09c7671af7" />

학습이 진행됨에 따라 OOD 성능이 RL > SFT 
SFT는 유지되는 것 없이 크게 악화됨 

<img width="665" alt="Image" src="https://github.com/user-attachments/assets/610fb8c1-86e8-4862-ab29-aba522a1119b" />

- visual OOD에 대한 result 

<img width="671" alt="Image" src="https://github.com/user-attachments/assets/36797866-f6dc-48f8-af05-48a56d823884" />


- SFT is necessary for RL training when the backbone model does not follow instructions.
<img width="337" alt="Image" src="https://github.com/user-attachments/assets/1b27663d-7b5d-4322-ae5d-5a0376d39f40" />

- Scaling up verification improves generalization.

<img width="330" alt="Image" src="https://github.com/user-attachments/assets/d5eec6f2-dc95-43d5-bbe3-b61204c21844" />

+2.15% (3 steps), +2.99% (5 steps), +5.99% (10 steps).
<->  one verification step, we only observe a marginal improvement of +0.48% in OOD performance improvement.