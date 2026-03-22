---
title: "[194] Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters"
date: 2025-01-03
tags: ['DeepMind', '2024Q3', 'reasoning']
paper: "https://arxiv.org/abs/2408.03314"
issue: 214
issueUrl: "https://github.com/long8v/PTIR/issues/214"
---
<img width="975" alt="image" src="https://github.com/user-attachments/assets/ce60aa20-2c3f-4833-9c0c-07cbbab95788" />

[paper](https://arxiv.org/abs/2408.03314)

## TL;DR
- **I read this because.. :** #213 에서 자꾸 언급되어 
- **task :** test time scaling in LLM 
- **problem :** test-time scaling 기법에 대한 분석.
- **architecture :** PaLM-2 (340B) // llama 2 family (pretraining <-> test time 볼때)
- **data :** (PRM) PRM800K prompt를 가지고 PaLM-2 + monte carlo roll-out으로 새로 만듦
- **evaluation :** MATH test split (500)
- **contribution :**

## Details
- thumbnail
<img width="981" alt="image" src="https://github.com/user-attachments/assets/fa14336f-d5d4-4d90-87ca-068dd80cb218" />

### test-time scale up 
중요한 것은 한정된 "inference cost"내에서 가장 효과적으로 쓸 수 있는 방법임.
해서 **"test-time compute-optimal scaling strategy"**가 들어감. 
<img width="470" alt="image" src="https://github.com/user-attachments/assets/2f5f7eea-cc85-4c02-9077-9ed1a75c9d9b" />

정해진 test-time compute 자원 $N$내에서 test-time hyper-param $\theta$를 prompt $q$에 대해서 최적을 찾아야 함.
이러한 최적은 question의 난이도에 따라 방법이 달라진다는 직관이 있음.
그렇다면 이 난이도를 어떻게 측정할 것인가에 대해서는 model의 2048 샘플 중에 pass@1 rate를 가지고 난이도를 측정하여 5개의 bin으로 나눌 수 있음 (-- oracle difficulty)
그런데 실제로 infer 상황에서는 gt를 모르기 때문에 final answer에 대한 learned verifier의 점수의 평균을 가지고 실행할 수 있음 (--model-predicted difficulty)
이런 방식으로 난이도를 나눈 뒤에 적합한 test-time scaling 방법으로 측정해야되기 때문에 이러한 방법 자체도 추가로 드는 cost임

### scaling test-time compute with verifier
ORM도 써보았지만 PRM이 consistently outperform해서 PRM을 썼다고 함 
#### training PRM
- data 
  - lightman et al.이 제공한 PRM800K가 있긴 하지만 PalM 2를 학습하는데 GPT generated 쓰는게 ineffective하다고 관찰. 
  - Math Shepherd을 따라 monte carlo rollout을 가지고 각 스텝에 대한 reward를 구하고 이걸 value로 사용. 
  - 베이스 모델에 few-shot prompt를 주어서 질문당 16개의 PRM을 생성. 16개의 monte carlo rollout을 시행하고 parsable한 answer가 안나오는건 지워버림.
- training
  - PRM은 이 0~1사이의 soft value를 예측하는 bce로 학습되는 binary classifier가 있는 형태.
  - val loss early stopping했다고 써있어서 몇 에폭한지 모르겠음
- aggregation
  - step-wise: last가 가장 좋았다고 함
  - intesr-answer: PRM 을 verifier로 사용한 "best-of-N-weighted"로 썼다고 함.  
- search
  - BoN weighted
  - beam search: N beams; M beam width
  - lookahed search: beam search와 달리 N개의 beam에 대해 K step 앞에 가보고 그 step의 PRM value로 beam serach하는 것 
    - stochastic을 없애기 위해 temperature = 0  
    - MCTS에서 stochastic(exploration)한 걸 뺀 버전이라고 하면 됨 
 

<img width="943" alt="image" src="https://github.com/user-attachments/assets/4663f04d-6433-41ea-8ca8-0207b41149ab" />

- result 
<img width="985" alt="image" src="https://github.com/user-attachments/assets/ce5f4029-d1b0-43b7-8b4a-f07997b26e06" />

(left)
작은 buget일 땐 beam search >> BoN. 높아질 땐 BoN이 좋기도 
lookahead 가 다른 방법에 비해 같은 cost대비 그렇게 좋지 않은데 simulating cost가 크기 때문에 그런듯. 가령 길게 생성하더라도 한두스텝만에 끝낼 수 있는 문제를 계속 탐험하는 것이 발견되곤 했음

<img width="627" alt="image" src="https://github.com/user-attachments/assets/65c6915e-132d-4ec7-9dc7-4af2ce0af11c" />

(right)
난이도가 쉬운 경우에는 BoN이 좋았고 높은 경우엔 beam search가 좋았음. -- 이는 직관과 맞는데 어려운 문제는 fisrt place에서 잘 나오기 어려워서 search가 필요하고 난이도가 쉬운 경우에는 beam-search가 over optimization하는 경향이 있음. 
그리고 가장 어려운 문제는 다 결과가 안좋았는데  (test-time scaling이 효과가 없었다는 뜻일듯) 이는 어려운문제에 대해 verifier가 정확한 해결을 하지 못하고 오히려 beam search를 통해 spurious features를 강화하는 꼴이 되어 성능이 더 안좋아진 것으로 추정함. -- 흠...

<img width="505" alt="image" src="https://github.com/user-attachments/assets/f73f4e59-0af4-4a41-b429-dad812d9e986" />
optimal 방법으로 하면 성능이 더 좋음

### Refining the proposal distribution
sequential refinement 등 처럼 sequential하게 생성하게 하는 것 
<img width="969" alt="image" src="https://github.com/user-attachments/assets/7c668027-4638-45b0-b05a-1f69e095ec20" />

rescursive introspection (https://arxiv.org/abs/2407.18219, RiSE)와 비슷한 접근법으로 하되, 직관상 "수정한 정답"이 "틀린 오답"가 가까울 때,  이런 refinement 학습에 효과적일 것이기 때문에 그런 chr edit distance로 오답을 골라내는 골라내는 작업을 했고, 자원이 부족해서 원래는 on-policy multi-turn(=sequential)하게 뽑아야하는데 그냥 병렬로 뽑은 뒤에 이어붙이는 식으로 했음. 
이때 오답 개수는 0~4개 사이에서 하나 샘플링해서 사용했음.

<img width="925" alt="image" src="https://github.com/user-attachments/assets/ab00a5e7-50a6-403c-8f09-58ed423e571e" />

inference할 때 맞는 정답을 내뱉어도 또 고치고 오답으로 하는 경우가 38% 있었음. 이런 현상 때문에 sequential하게 정답을 여러개 뽑으면 이걸가지고 majority voting or verifier 
(왼쪽) sequence길이가 길어질 수록 pass@1이 늘어나는 현상
(오른쪽) parallel voting 보다 compute 자원이 늘어날 때 성능이 더 좋음

### trade off sequential or parallel test-time compute
직관은 sequential은 쉬운 문제에 대해서 더 잘 될 것 같고 (왜냐면 처음에 방법에서 수정하는 방식이니) parallel은 어려운 문제에서 다양한 시도를 해봐야하니 어려운 문제에 대해서 더 잘 될 것 같음. 즉 이를 둘다 쓰는게 가장 좋을 것 같음. 
<img width="957" alt="image" src="https://github.com/user-attachments/assets/682282e2-cbd3-4f4b-9a78-c5d30708bc90" />

(오른쪽) 난이도가 낮을 때는 그냥 sequential로 하는게 좋았지만 높아질 때는 적정한 비율이 있었음. (parallel이 무조건 또 좋은 건 아니네)

이것도 optimal값이 있음
<img width="475" alt="image" src="https://github.com/user-attachments/assets/b76375a8-01d3-4c23-8a75-0c06c947a97d" />

### tradeoff betweentes-time vs pretraining (잘 이해 못함)

<img width="951" alt="image" src="https://github.com/user-attachments/assets/feb201c2-05d6-456d-b6e2-e3b4a2bbec2d" />

- 별이 최대 14배 많은 파라미터로 학습된 프리트레이닝 모델.
- 가로축은 6 * # parm * # tokens for pretraining (==max length?? 이해를 잘 못함) / 2 * N * total # of generated in inference time 
- 난이도가 높을수록 pretraining compute를 늘리는게 좋다는 결론