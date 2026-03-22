---
title: "[215] Group Sequence Policy Optimization"
date: 2025-08-01
tags: ['LLM', 'RL', '2025Q3']
paper: "https://arxiv.org/abs/2507.18071v2"
issue: 236
issueUrl: "https://github.com/long8v/PTIR/issues/236"
---
<img width="1058" height="278" alt="Image" src="https://github.com/user-attachments/assets/ad1ad42b-ff14-4afb-ad76-27a5b9ddba10" />

[paper](https://arxiv.org/abs/2507.18071v2)

## TL;DR
- **I read this because:** GRPO 대안으로 나오면서 바이럴 
- **Task:** large reasoning model 
- **Problem:** 기존 GRPO 알고리즘의 토큰 단위 importance ratio로 인한 훈련 불안정성과 model collapse 문제 
- **Idea:** 토큰 단위가 아닌 시퀀스 단위의 importance ratio 사용으로 안정적인 RL 훈련 구현
- **Input/Output:** query ->  {reasoning, answer}
- **Architecture:** Qwen3-30B-A3B-Base
- **Objective:** GSPO(proposed)
- **Baseline:** GRPO
- **Data:** RL training on math (AIME'24), coding (LiveCodeBench, CodeForces) tasks
- **Evaluation:** Training stability, efficiency metrics, downstream task performance
- **Result:** Superior training stability, 효율성, MoE 모델 안정화, Qwen3 모델 성능 크게 개선
- **Contribution:** 시퀀스 단위 importance sampling으로 RL 훈련 안정화, MoE RL 훈련 단순화
- **Etc:** Alibaba Qwen팀에서 개발, 실제 Qwen3 모델에 적용되어 성능 향상 달성

## Details

### Problem Analysis
- GRPO 

<img width="646" height="169" alt="Image" src="https://github.com/user-attachments/assets/7b5520fc-650f-44e0-9362-23ff8455ae00" />

여기서 $w_{i,t}$는 원래 분포인 $\pi_{tar}$에서 샘플링하지 않았기 때문에 이 확률을 보정해주는 형태 
보통의 importance sampling은 N을 1보다 크게 주고 평균을 주어 하는 것이 일반적임. 

<img width="274" height="41" alt="Image" src="https://github.com/user-attachments/assets/925e7908-4527-4268-98ed-3df9f42a8af7" />

그런데 GRPO에선 1) 하나의 sample로 2) (전체 확률분포가 아닌) next token probability에 대해서만 구하기 때문에 모델이 noise에 매우 민감해지는 결과를 냄.
또한 이러한 noise가 긴 시퀀스에 누적되면서 noise가 더 커져서 한번 잘못 수렴하면 돌이키기 어렵고 hparam(clipping hparam, rl prompt, .. 등)에 매우 민감하게 됨. 
또한 reward는 한 시퀀스에 대해 나오는데 optimization objective는 token 단위로 오는 불일치가 있음.

### GSPO Algorithm

<img width="1314" height="431" alt="Image" src="https://github.com/user-attachments/assets/043f9042-2e43-4ec3-a926-af48d6a3e163" />

- 토큰 단위가 아닌 시퀀스 전체에 대한 clipping 결정
- 모든 토큰에 동일한 가중치 적용
- $s_i$를 $|y_i|$의 길이로 나눠주면서 length normalize (길이와 상관없이 clip range를 비슷하게 가져가기 위해서)

gradient

<img width="1297" height="323" alt="Image" src="https://github.com/user-attachments/assets/81ffa8dc-fd1d-4a77-8c1c-518266807460" />

<img width="1327" height="262" alt="Image" src="https://github.com/user-attachments/assets/458c75da-c5a9-4f24-ad25-eb528c44603b" />

### Experimental Results
**Training Efficiency**:

<img width="855" height="520" alt="Image" src="https://github.com/user-attachments/assets/9dcabfcc-9154-4cf1-8aaf-acf1a88e4b53" />

- GRPO 대비 더 높은 training reward 달성
- 동일 계산량에서 더 나은 성능
- 더 안정적인 수렴 곡선
- AIME'24, LiveCodeBench, CodeForces 에서 더 나은 벤치 성능 

**Clipping Analysis**:

<img width="576" height="197" alt="Image" src="https://github.com/user-attachments/assets/9f880325-aa9e-4c66-bb90-9c823d52e9cb" />

- GSPO: 15% 토큰 clipping
- GRPO: 0.13% 토큰 clipping
- 역설적으로 더 많은 clipping이 더 좋은 성능으로 이어짐

### MoE Training Benefits
MoE-Qwen3를 GRPO로 학습할 때 불안정한 경향성이 있었는데 이는 이전의 policy에서 activate된 expert와 현재 policy에서 activate된 Expert가 달라지면서 Importance ratio의 변동성이 훨씬 커져서임
이를 해결하기 위해 $\pi _{old}$에 대해 activate 된 expert를 cache해두고 $\pi$ 와 $\pi _{old}$가 같은 expert를 가지도록 하는 trick을 짬.

<img width="1041" height="405" alt="Image" src="https://github.com/user-attachments/assets/bb165550-2bc9-460d-9091-889a33ba9245" />

<img width="1041" height="334" alt="Image" src="https://github.com/user-attachments/assets/2582acc5-c98e-4930-bc0a-e4fd3222acb0" />

그것보다 GSPO가 더 좋았음. 이로인한 복잡도가 낮아짐.

### Benefit of GSPO for RL Infrastructure
rollout은 sglang, vllm으로 하고 training engine은 megatron으로 하면서 정밀도 이슈 때문에 old policy에 대한 likelihood를 다시 계산했어야 했음. (old policy는 업데이트 되는 대상이 아니라서 원래는 안해도 됨)
그러나 token-level likelihood에 비해 sequence-level likelihood는 정밀도에 민감하지 않아서 재계산 하지 않아도 됨 
이로 인해  partial rollout and multi-turn RL and in the training-inference disaggregated frameworks 상황에서 조금 더 효율성이 좋음 

c.f. DAPO
normalize에 대한 부분이라 내용이 다름 

<img width="655" height="139" alt="Image" src="https://github.com/user-attachments/assets/97efd436-977d-4e40-9c42-1c0c94ce9168" />