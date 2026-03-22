---
title: "[134] Asynchronous Methods for Deep Reinforcement Learning"
date: 2023-10-18
tags: ['2016', 'DeepMind', 'RL']
paper: "https://arxiv.org/pdf/1602.01783.pdf"
issue: 146
issueUrl: "https://github.com/long8v/PTIR/issues/146"
---
<img width="679" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8fbd0472-8614-4760-8eb5-bf50b1cbfad7">

[paper](https://arxiv.org/pdf/1602.01783.pdf)

## TL;DR
- **I read this because.. :** 남종대 가을학기 수업에서 읽으라고 추천받음
- **task :** Deep Reinforcement Learning 
- **problem :** online RL이 unstable함. 이를 해결하기 위해 replay buffer(이전의 trasition에서 s, a, s'를 가져오는 것) 등이 고안되었으나 이는 off-line RL algorithm에만 국한됨
- **idea :** multiple agent를 parallel하게 실행해서 배치로 묶어서 업데이트 하자! 
- **input/output :** trajectory / policy 
- **architecture :** one-step Q-learning, one-step Sarsa, multi-step Q-learning, proposed A3C(actor-critic). Value 또는 policy network는 FFN or LSTM로 구성
- **objective :** policy $\phi$를 따랐을 때 advantage(value based), policy를 따랐을 때 reward의 expectation(policy based) + policy의 entropy를 loss term에 추가하니까 더 안정적
- **baseline :** one-step Q-learning, one-step Sarsa, multi-step Q-learning, advantage actor-critic
- **data :** Atari 2600, TORCS, Mujoco, Labyrinth
- **evaluation :** score, data efficiency, stability 
- **result :** 높은 score. 빠른 수렴. 더 적은 training step으로 더 높은 성능(data efficiency). 다른애들은 GPU만 쓰는데 얘는 CPU multi core만 씀 
- **contribution :** 지금 이 시점에서 보기엔 간단한 아이디어로 좋은 성능 
- **etc. :** 그 유명한 A3C가 이거군... RL은 모델 이름이 다 개성이 넘친당.. gorilla, REINFORCE, A3C, ... 

## Details
### introduction
- online RL agent가 만나는 데이터들의 문제점
  - non-stationary: 시계열에서 말하는 정상성? time step에 따라 분포가 달라진다?
  - strongly correlated: 이것도 시계열에서 말하는 것? 이전 time step (t-1)에 의해 t가 무슨 연관성을 갖나봄
이를 해결하기 위해 고안된게 다른 time step에 대해서 replay buffer, data batched, randomly sample 하는게 있었다 
근데 이렇게 하면 자연스럽게 off-policy 방법으로 국한된당. 이전의 transition은 이전의 policy를 따르고 있는 결과이기 때문이다

### Reinforcement Learning Background 
우리가 RL에서 하려는 건 environment $\epsilon$과 상호작용하는 agent가 있을 때, time step t의 $s_t$이 주어졌을 때 action $a_t$를 도출하는 policy $\pi$가 있을 때 discount factor $\gamma$로 할인된 $R_t=\sum_{k=0}^{\infty} \gamma^k r_{t+k}$을 최대화하는 것!

이때 action value Q는 아래와 같이 표현되고 $Q^\pi (s) = \mathbb{E}[R_t|s_t =s, a]$ 이는 policy $\pi$를 따랐을 때 state s에서 action a를 취할 때 sum of reward의 기대값이다. 
value of state s도 유사하게 아래와 같이 표현된다. $V^\pi (s) = \mathbb{E}[R_t|s_t =s ] $이는 policy $\pi$를 따랐을 때 state s의  sum of reward의 기대값이다. 

여기까지가 RL의 기본 셋팅! 
여기서 value-based model-free method를 쓰면 $Q(s,a;\theta)$를 바로 NN로 근사한다. 이게 Q-learning. 
그럼 우리는 optimal $Q^*(s,a)$를 NN의 파라미터 $\theta$로 바로 근사하면 된다. 이때 우리의 loss는
<img width="310" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2072ea7e-9276-4121-9ee5-cdbf6101b009">
~아 좀 헷갈리는뎅.. state s, a에서 전이되는 s'를 maximize하는 a'를 최대화하는 $\theta$를 구하니까 policy도 구할 수 있는건가 Q만 구해서 뭐에 쓰는거지? Q를 구하면 policy도 자동으로 구해지는건강 (Q를 최대화하는 a를 구하면 되니까?)~
~RL은 언제나 policy network가 있음! Q는 (t+1) 시점 이후로의 reward를 근사하는 값!~
q-learning에서는 network는 암시적으로 설정되는듯. 별도의 policy network가 있는 것이 아님. 원래의 이해가 맞음(24.08.21)

이때 Q-learning의 단점은 reward를 얻는 (s, a) pair만 직접 영향을 받고 다른 (s, a) pair들은 비간접적으로 영향을 받아서 학습이 느리다. 이를 해결하기 위해 나온 것이 n-step Q-learning. 이건 할인 ratio $\gamma$를 적용해서 다른 time step까지 현재 reward에 영향을 주게 하는 것인듯?
<img width="318" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/455bc139-d2f9-48c3-bf2c-fafa89ab6412">

이렇게 하면 single reward $r$이 이전의 state action pair에도 직접적으로 영향을 줄 수 있게 된다.

반대로 policy-based model들은 policy $\pi(a|s, \theta)$를 바로 parametrize한다. 이때의 loss는 $\mathbb{E}[R_t]$이다(gradient ascent)
REINFOCE 류들이 이렇게 하는데 $\theta$를 아래와 같이 구하고
<img width="120" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/412a224b-5ed1-423a-b1cc-6514b93b92bc">

이게 variance가 높아서 이를 낮추려고 bias term을 빼게 된다.
<img width="184" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/99ed0561-014a-4f1f-a080-79029cfbfd96">

이때 이 bias term을 V로 근사해서 구하면 더 variance가 낮아지는데 이게 바로 actor-critic architecture다
<img width="103" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a56151e3-9b38-4bee-89bc-16413aa6ac2a">

### Asynchronous RL Framework
multi-thread를 써서 asynchronous하게 하면 된다.
- one-step Q-learning의 pseudo-code는 아래와 같다.
<img width="335" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4d0931b2-ec47-4638-a494-3e6c9733cd6b">

별거 없고 그냥 thread T개 일 때까지 grad accum 했다가 한번에 업데이트하는거~

- n-step Q-Learning 
<img width="596" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/81028dd4-2ff8-4835-a7bf-449245933539">

<img width="328" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9b67ab52-42b3-4c23-95a7-738a0b7a525b">

위의 말 무슨 말인지 모르겠음 원래는 과거로 가야되는데 미래로 간다..?
$t_max$일 때 까지 exploration 한 다음에 한번에 업데이트하는 듯 하다. 

- Asynchronous advantage actor-critic
advantage actor-critic에 multi-thread 추가 + policy의 entropy를 Loss에 추가
<img width="596" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ca3623a3-982c-4bdc-b97d-ed1623ce0cd5">

학습은 RMSProp 사용 

### Result 
<img width="685" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0168e7bf-8e1a-49bf-9b9f-b420f765acc6">

- Data Efficiency
<img width="673" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5a1963fe-eef8-409e-946f-6fd2208100ec">

이론적으로는 같은 sample 개수를 봤을 때 동일성능이 나오면 좋음. 근데 우린 multi-thread 쓰니까 4개 thread쓰면 wall-clock time이 4배 단축되는 효과!
그런데 추가로 놀랍게도 Q-learning과 sarsa 알고리즘의 경우 동일 샘플 개수 대비 성능이 더 좋았다고. one-step method보다 bias를 줄여서? 