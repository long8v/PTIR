---
title: "[200] Advancing Language Model Reasoning through Reinforcement Learning and Inference Scaling"
date: 2025-02-03
tags: ['25min', 'RL', '2025Q1', 'THU']
paper: "https://arxiv.org/abs/2501.11651"
issue: 221
issueUrl: "https://github.com/long8v/PTIR/issues/221"
---
<img width="572" alt="Image" src="https://github.com/user-attachments/assets/7251c675-ec9a-4662-965c-60b8885c48a6" />

[paper](https://arxiv.org/abs/2501.11651), [github](https://github.com/THUDM/T1)

## TL;DR
- **I read this because.. :** 요즘 대세인 answer만으로 reward를 주는 접근론 
- **task :** RL reasoning
- **problem :** scale RL 
- **idea :** 1) cot sft 데이터를 잘 만들자 2) exploration 을 많이 시키자(temperature when exploration, entropy bonus) 3) 정답 + undesirable 행동에 대해서만 reward를 주자 
- **input/output :** Q -> A
- **architecture :** Qwen2.5-32B 
- **objective :** 1 or 0 reward  + RLOO + entropy bonus 
- **baseline :** QwQ-32B-preview 
- **data :** MATH-train, NuminaMATH
- **evaluation :** MATH500, AIME2024, Omni-math-500
- **result :** QwQ-32B-preview 보다 높은 성능 
- **contribution :** 다양한 ablation과 방법론도 #220 과 대동소이 
- **etc. :** 지금 다시 보니 on-policy도 많이 강조한듯?

## Details
### overall pipeline 
<img width="932" alt="Image" src="https://github.com/user-attachments/assets/9d415a57-bcfe-48b3-b03a-83e5f733d069" />

저기서 정답은 ground truth와 비교하여 맞으면 1 아니면 0 

- Initializing Policy with CoT for Reasoning
다양한 llm을 사용하여 prompt x에 대한 다양한 attempt를 모음. 

- scaling response sampling with high temperature
temperature를 1 이상으로 주어 다양한 response가 나오도록 함 
RLOO를 사용하여 reward scaling 
<img width="368" alt="Image" src="https://github.com/user-attachments/assets/20a25134-9c1d-4c95-9176-509623dea1cc" />

- auxiliary entropy bonus 

<img width="917" alt="Image" src="https://github.com/user-attachments/assets/56f7e8cf-ac3d-420e-877b-d1553d6a65a3" />

- on-policy kl divergence 

<img width="1075" alt="Image" src="https://github.com/user-attachments/assets/11fb733e-ffd3-4cee-8069-fa9233cd1c1d" />

kl divergence term에 대해서도 scaling을 적용함 

<img width="429" alt="Image" src="https://github.com/user-attachments/assets/bf0b33c6-3777-4a1d-a7d8-eb04ce3b0740" />

reference model에 ema 적용

- Penalizing Unexpected Patterns in RL Training
<img width="566" alt="Image" src="https://github.com/user-attachments/assets/39852320-48b5-4b81-9acd-0d1e875cb06c" />

repeated / overlong answer에 대해 reward에 -1를 더해줌. 이건 rule based (n-gram 반복등)으로 탐지했음


### details 
- data construction
  - MATH, NuminaMATH를 SFT / RL 용으로 나눔
  - sft 데이터에 대해서 추가적인 필터링 적용  -- 너무 쉽거나 noisy 데이터 제거. 
  - 16개의 response를 생성한 뒤 정답률 0.3 이하인 애들만 남김
 

### result
- overall results
<img width="1063" alt="Image" src="https://github.com/user-attachments/assets/7e1bc003-0244-4cfb-8187-c4d220eac566" />

- ablation on sampling more

<img width="1083" alt="Image" src="https://github.com/user-attachments/assets/edd06011-8afb-479e-8872-ebc599798f61" />

sampling K를 늘리면 답변길이도 늘어나고 정확도도 늘어남. (a), (b)
또한 같은 reward에 대비하여 KL divergence가 작고 늘어나는 속도도 느림 (c) -- 이게 왜 좋은거지?

<img width="1070" alt="Image" src="https://github.com/user-attachments/assets/2fd77f0c-21e4-489e-b389-2336c4fb1847" />

최종적인 성능 

- exploration

<img width="989" alt="Image" src="https://github.com/user-attachments/assets/dfdc92fa-ab94-4283-9821-05589f2fac96" />

<img width="965" alt="Image" src="https://github.com/user-attachments/assets/d3174a41-e63f-413f-8f7a-318f31df5546" />

1.2가 최적. 너무 크면 안좋았음.

- penalty reward

<img width="1018" alt="Image" src="https://github.com/user-attachments/assets/6554f873-fb7b-427d-8cd3-ac03d23b556b" />

