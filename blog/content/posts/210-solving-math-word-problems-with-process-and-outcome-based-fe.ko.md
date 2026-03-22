---
title: "[190] Solving math word problems with process and outcome-based feedback"
date: 2024-12-16
tags: ['DeepMind', '2022Q4', 'RL']
paper: "https://arxiv.org/abs/2211.14275"
issue: 210
issueUrl: "https://github.com/long8v/PTIR/issues/210"
---
<img width="639" alt="image" src="https://github.com/user-attachments/assets/612c3113-63dc-45e3-ba2a-b8b36be21c71" />

[paper](https://arxiv.org/abs/2211.14275)

## TL;DR
- **I read this because.. :** o1 관련 영상에서 언급되어 
- **task :** math 
- **problem :** outcome-based vs process-based 
- **idea :** GSM8K를 사용하여 1) final answer만 학습 2) human generated reasoning trace or model generated에 각 reasoning step에 대한 human correctness annotation을 추가하여 학습. 
- **architecture :** ours base-70B (비밀인듯)
- **objective :** ce (SFT) / bce (ORM / PRM) 
- **baseline :** PaLM-540B, Minerva-540B, GPT-J-6B, Codex-175B, InstructGPT-175B, GPT-175B 
- **data :** GSM8K -> (eval) GSM8K-test, MATH 
- **evaluation :** final-answer error rate / trace error rate(human annotated). MATH dataset (OOD error rate)
- **result :** 1) outcome-, process- 모두 final answer error rate는 비슷. 2) process-, outcome- RM 을 사용할 경우 둘 다 process-based feedback 생성 가능 3) trace error를 줄이기 위해서는 process-based feedback or reward model이 필요 
- **contribution :** 다양한 분석. 사실 얼마나 중요한 논문인지는 모르겠음

## Details

<img width="674" alt="image" src="https://github.com/user-attachments/assets/3b14ca49-1d43-45ab-85c9-ea2758474885" />

### training: overview
- step: new-line seperated (한 줄이 한 step)
- answer: last line 
- policy network: "each step" as an action, "all the tokens so far" as an observation
  - train with few-shot prompt, SFT,  RL 
  - reward model -> reranking하는데 사용됨 
 
### SFT
- reasoning trace까지 학습. 
- val loss 가 상승할때 까지 학습. 대략 2에폭

#### Reward model
- ORM: #209 와 비슷하게 final answer가 맞는지 틀린지에 대해 binary label로 학습
- PRM:  지금까지의 step이 맞는지 binary label로 학습
  - 이에 대한 label은 human annotated로 받음. 
- 두 개 모두 현재 policy 모델에서 나온 sample을 사용하여 학습. (temperature 1.0. K=96). 
  - ORM의 경우 SFT에서 시작, few-shot의 경우 pretrained lm에서 시작. 
  - PRM의 경우 SFT policy network에서 문제당 3개의 샘플로 어노테이션 받음.
  -  이때 문제는 SFT 예측이 틀린 애들을 위주로함. 
  - PRM의 경우 ORM 모델로 초기화하고 val loss가 변동이 좀 있어서 2000 step 이전 최적 Val Loss로 선정

#### Decoding
- 96 samples 뽑고 몇가지 디코딩 기법 적용
- self-consistency
- RM weighted decoding (==verifier voting) -- RM score만큼 weighted 해서 voting
  - highest RM score로 선정하는 것보다 약간 좋았음
 
#### RL via Expert Iteration
<img width="642" alt="image" src="https://github.com/user-attachments/assets/466caba0-9532-48ab-9c99-b3cc48c06762" />

안 읽어서 잘 모르겠으나 RL로 학습된 애를 Policy로 써서 trace들 뽑고 이를 반복하는걸 말하는듯

- SFT vs few-shot based
  - initial policy network는 SFT이거나 5-shot prompt를 한 base LM 이거나 선택의 여지가 있음

<img width="652" alt="image" src="https://github.com/user-attachments/assets/e1f1d5d7-0d66-4e02-a2cd-989306cbc809" />

- Policy Improvement
  - final-answer RL(a.k.a. self-taught reasoner)
    - 문제당 K개의 샘플을 뽑고 final-answer의 정확도로 필터링
    - SFT의 경우 문제당 하나만 선택 (이유는 없음)
  - ORM-RL
    - K개의 traces 중 ORM이 가장 높게 점수를 매긴애를 선택
  - PRM-RL
    - K(=96)개의 candidate step을 뽑고 PRM에서 가장 높은 점수를 가진 애를 선택. final answer이거나 15 스텝이 넘어가면 종료
    - few-shot base일 경우 RM은 매번 새로 학습했고 SFT의 경우 RM은 고정함

#### Data annotation
- stepwise label의 경우 생성된 모델에서 첫번째로 틀린 step을 찾으라고 함. 이 기준은 1) 표현된 내용이 부정확하거나 2) 이 step을 undo하지 않는 이상 맞는 답변으로 갈 가능성이 없는 것

### Result 
<img width="661" alt="image" src="https://github.com/user-attachments/assets/d01720cf-7055-4b0b-a99e-95c6fc61a020" />

- final answer SFT만 해도 성능이 개선된다 (3.1의 마지막 행 `SFT, Majority Voting` 22.3 vs `Few-shot+Final-Answre..` 23.5).
  - Few-shot + final-answer rl은 1~4 토큰 만큼의 Supervision을 갖지만 SFT는 Hunderes로 갖기 때문에 다르다고 분석

<img width="316" alt="image" src="https://github.com/user-attachments/assets/93426b52-958c-4a34-a4b2-5f32a457c60d" />

- ORM-superviesed reward models ~= PRM 
  - 위 그림을 보면 ORM으로 학습한 결과가 PRM label 결과와 agreement가 높은 것을 알 수 있음
  - 또한 `SFT, majority voting` tracing error 11.4 vs `SFT, ORM ranking` 4.4를 비교했을 때 ORM만으로도 trace error를 많이 줄일 수 있다고 함 
  - 다만 이 결과는 이 도메인에서만 이럴수도 잇음

<img width="338" alt="image" src="https://github.com/user-attachments/assets/526483fe-ae0d-4554-b5b4-a4532c9c8c15" />

- low trace error requires process-based feedback or reward model 
  - `Few-shot Final-answer RL,.. `과 `SFT, Majority Voting` 두개의 차이는 final answer는 거의 비슷하지만 trace error가 많이 차이 남 (19.8 vs 11.4)
  - 같은 경향성은 `Few-shot + Final Answer RL, ORM reranking` 12.4 vs  SFT, ORM / PRM reranking 4.4 - 3.4에서도 일어남
  - 하지만 여기에 `ORM-RL`을 넣으면 `few-shot + ORM RL, ORM reranking` trace error도 5.5까지 떨어짐 
  - 즉 process SFT를 하던가 reward model이 필요함

<img width="669" alt="image" src="https://github.com/user-attachments/assets/030dfbc6-7cd3-48df-b3c1-1c63dd38ee55" />

- RL 은 Few-shot 셋팅에서는 성능을 많이 개선했고 SFT에서는 적당히 개선했따.
  - 특히 RM decoding + final answer rl의 경우 거의 성능 개선이 없기도 했다. 