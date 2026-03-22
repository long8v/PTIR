---
title: "[168] Proximal Policy Optimization Algorithms"
date: 2024-08-21
tags: ['2017', 'RL']
paper: "https://arxiv.org/pdf/1707.06347"
issue: 187
issueUrl: "https://github.com/long8v/PTIR/issues/187"
---
<img width="703" alt="image" src="https://github.com/user-attachments/assets/ad3ddfeb-d439-4c96-b841-2353465edc1a">

[paper](https://arxiv.org/pdf/1707.06347)

## TL;DR
- **I read this because.. :** 배경지식 차
- **task :** RL 
- **problem :** q-learning은 너무 불안정하고, trpo 는 상대적으로 복잡. data efficient하고 sclable한 arch?
- **idea :** KL divergence term 대신에 clipping을 사용하자. step size $\beta$를 adaptive하게 변동시키자 
- **input/output :** state -> action 
- **architecture :** MLP 
- **objective :** $L^{CLIP}(\theta) = \hat{\mathbb{E}}_t \left[ \min(r_t(\theta)\hat{A}_t, \text{clip}(r_t(\theta), 1 - \epsilon, 1 + \epsilon)\hat{A}_t) \right]$
- **baseline :** loss(no clipping, KL penalty), A2C, CEM, TRPO
- **data :** OpenAI Gym(Mujoco), human control task(Roboschool), Atari
- **evaluation :** 몰라
- **result :** 좋다
- **contribution :** 간단하고 직관적인 loss.. 사실 이 논문만 보면 직관적인 이해가 되어서 굳이 그 전 내용을 알았어야 하는 생각도.. ㅎㅎ
- **etc. :**

## Details
### preliminary 
- policy gradient method
<img width="232" alt="image" src="https://github.com/user-attachments/assets/764d9bf8-cacd-4c12-9437-9784439ede96">

policy network에 대한 gradient를 advantage에 가중하여 미분하는 형태
여기서 E는 sample을 뽑아서 그냥 평균 취하는 형태

<img width="272" alt="image" src="https://github.com/user-attachments/assets/b7cab011-36d4-423a-aa6b-79e3f1e849c5">

loss는 이러한 policy를 따르는 trajectory에 대한 advantage 가중합의 기대값이 최대가 되도록 하면 된다
그러나 large policy update가 될 경우 성능이 좋지 않다

- Trust Region methods
TRPO는 대리 함수를 사용하여 성능 개선이 보장되는 policy update를 할 수 있는 surrogate 함수를 증명했고(https://github.com/long8v/PTIR/issues/154) 이는 policy가 업데이트 될 때의 제약이 생겨서 결론적으로 아래와 같이 new, old policy network의 importance weight와 advantage가 곱해진 형태 
<img width="367" alt="image" src="https://github.com/user-attachments/assets/e1489535-f648-4625-aef6-f77c6c7a0b9d">

실제로는 제약이 아니라 penalty term을 추가함 여기서 $beta$는 하이퍼파라미터임. 
<img width="460" alt="image" src="https://github.com/user-attachments/assets/610aa2b5-8f85-4906-a5a7-26f12bc02638">

이 논문에서 말하는 TRPO의 문제점은 $\beta$가 하나로 골라질 수 없다 정도인듯.

### Clipped Surrogate Objective
<img width="367" alt="image" src="https://github.com/user-attachments/assets/a7a3deb0-4cdc-4eb7-ba81-feb095a2dc3e">

<img width="415" alt="image" src="https://github.com/user-attachments/assets/f04bf66e-ec62-45b1-92dd-503eae6cf1b6">

결론적으로 $r_t(\theta) = \frac{\pi_\theta(a_t | s_t)}{\pi_{\theta_{old}}(a_t | s_t)}$가 너무 크거나 작지 않도록 clip했다고 보면 됨 

<img width="703" alt="image" src="https://github.com/user-attachments/assets/f6307ca3-f047-4b01-befe-d245209c85d8">


이렇게 하니 policy network의 변동이 적었다고 함

<img width="724" alt="image" src="https://github.com/user-attachments/assets/c6337d1e-19bf-4381-9d65-d04f6c6c2eee">

#### Adaptive KL Penalty Coefficient

<img width="635" alt="image" src="https://github.com/user-attachments/assets/6b51ff1b-6408-4d9e-ab0a-1a298efa1919">

아이참 이것도 아주 직관적이고 간단하다.. 

#### Algorithm
위에는 policy에 대한 gradient 업데이트를 어떻게 할지 정한거고 외의 것들은 괜찮은 것들 갖다 씀. 
V(s)를 도입하여 reward의 variance 줄임. 즉 policy surrogate와 value function error term을 추가함. 여기에 exploration 더 많이 하라고 entropy bonus를 추가해줌. 
<img width="699" alt="image" src="https://github.com/user-attachments/assets/f4cbd1e4-cfdb-4f1d-82c7-ffd458abde0a">

advantage는 현재 할인된 Reward의 summation에서 현재의 V를 빼고 미래의 V를 할인해서 더함.
<img width="445" alt="image" src="https://github.com/user-attachments/assets/5911be64-718a-4253-a56b-d6e00104e3e7">

잘 기억 안나는데.. fixed time step에서 bias // vairance를 최적화하는 기법을 써서 아래와 같이 구함 
<img width="372" alt="image" src="https://github.com/user-attachments/assets/b88e172e-c25e-489b-8fea-41d28be3d6d3">


### Experiments
- loss term
<img width="723" alt="image" src="https://github.com/user-attachments/assets/07cbe885-9056-4e59-ab1e-d74f0318112b">

-  other RL algorithms
봐도 모르쥬 ㅎ
<img width="716" alt="image" src="https://github.com/user-attachments/assets/3cb58942-489f-4be1-97f6-e00cfecb2fd3">

