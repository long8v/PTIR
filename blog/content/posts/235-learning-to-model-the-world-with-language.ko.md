---
title: "[214] Learning to Model the World With Language"
date: 2025-07-17
tags: ['ICML', 'RL', '2023Q3', 'WORLD-MODEL']
paper: "https://arxiv.org/pdf/2308.01399"
issue: 235
issueUrl: "https://github.com/long8v/PTIR/issues/235"
---
<img width="731" height="152" alt="Image" src="https://github.com/user-attachments/assets/89b7f195-bb42-45ef-8505-a05859ea4b23" />

[paper](https://arxiv.org/pdf/2308.01399)

## TL;DR
- **I read this because.. :** agent + VLM 검색하다가 나옴. gaming rl에 관심 있어서. ICML'24 oral
- **task :** world modeling, embodied agent(language instruction을 수행하는 agent)
- **problem :** 기존 방식은 language가 주어지고 행동을 하는 식이지만 real-world는 실제로 language, action, video 가 연속적으로 input/output 되는 것에 가까움
- **idea :** language를 instruction 뿐 아니라 지식을 습득하고 미래를 예측하는데 사용할 수 있지 않을까?
- **input/output :** (world model) {video, text, action} -> {representation of future, (optional) language} (agent) state -> action 
- **architecture :** (vision encoder) strided image encoder (vision decoder) strided image decoder (text embedding) embedding from scratch or T5 (sequence modeling) GRU /// (policy model) DreamerV3
- **objective :** (world model) reconstruction error + regularization + next representation prediction (policy model) maximize expected reward 
- **baseline :** (model-free RL) IMPALA, R2D2,  (task-specific model) EMMA (Messenger)
- **data :** (world model) replay buffer from {homegrid, messenger, vln-ce, langroom} (pretraining) messenger manual(in-domain), tiny stories(general)
- **evaluation :** HomeGrid (proposed), Messenger, VLM-CE, LangRoom (proposed)
- **result :** 
- **contribution :** streaming 으로 들어오는 정보에 대해 효과적인 world model 학습 (single "text" modality pretraining 이 가장 contribution 인듯?) -- 외의 world model + actor-critic 이랑 같이 학습하는 건 dreamer v3(https://arxiv.org/abs/2301.04104)의 contribution인듯하다. 
- **etc. :**

## Details

<img width="986" height="445" alt="Image" src="https://github.com/user-attachments/assets/94dd13f5-174e-4a8c-a352-5036e77d198b" />

<img width="1014" height="547" alt="Image" src="https://github.com/user-attachments/assets/c4264c59-edcf-4780-8617-9e014ae7ac0f" />

### problem setting
- action: $a_t$ -- discrete action
- reward $r_t$
- episode end $c_t$ ($c_t$=0 when ends)
- observation $o_t$ -> multimodal observation (visual $x_t$, textual $l_t$)

<img width="493" height="594" alt="Image" src="https://github.com/user-attachments/assets/2b332119-9149-470a-a4bc-7f26f6b1c809" />


<img width="700" height="321" alt="Image" src="https://github.com/user-attachments/assets/15958fa9-e22f-4a50-8ffd-a216f851a9c3" />

### world model learning
  - <img width="504" height="128" alt="Image" src="https://github.com/user-attachments/assets/f37f5b70-3b5a-4f7f-a623-80895230c0fd" />
  - Recurrent State Space Model(RSSM) -- GRU 기반의 sequence model을 사용
  - $z_t$ : reresentation representation -> $\hat{z_{t+1}}$를 예측
  - $h_t$ : recurrent state
- multimodal representation
  -  variational autoencoder objective로 $z_t$로 압축. 이후 $z_t$에 대해 reward $\hat r_t$와 $\hat c_t$도 예측. 
  - <img width="515" height="176" alt="Image" src="https://github.com/user-attachments/assets/38bfc0c6-45a7-4cbb-b11c-848626c4cbde" />
  - 추가로 $z_t$와 $\hat z_t$가 너무 달라지지 않도록 regularize 추가
- future prediction 
  - <img width="497" height="42" alt="Image" src="https://github.com/user-attachments/assets/8308dbee-f3c6-4972-9886-7d1bb419ddd1" />
  - 현재의 model state $z_{t-1}$, $h_{t-1}$에서 모델이 예측한 $\hat {z_t}$가 실제 다음 step의 $z_t$와 match 되도록 학습. 
  - world model이 미래의 표현에 대한 $\hat z_t$를 예측하게 함으로서 미래의 image, language, reward를 예측하고 다양한 multiple modalities의 correlation을 학습하도록 함
- single modality pretraining
  -  world model은 offline으로도 학습할 수 있기 때문에 text-only, video-only data로 world model을 학습할 수 있음
  - text only의 경우 image, action input을 zero로 두고 decoder loss coefficient를 0으로 두면 pretraining을 할 수 있음. 
  - language modeling loss와 달리 다음의 representation을 예측하는 방식으로 학습됨 
  - actor, critic 을 초기화한 뒤 각각의 modality 에 대해 이와 같이 pretraining 할 수 있음
  
### policy learning
- actor-critic 으로 Dreamer V3의 구조를 그대로 가져감

<img width="451" height="24" alt="Image" src="https://github.com/user-attachments/assets/79db9c84-0401-4d80-be2f-ee8964089928" />

 ### experiment
- RQ1: {image, language}를 timestep 별 pair로 넣는 것이 더 좋을 것이다
- RQ2: 학습할 때 다양한 language를 사용하기 때문에 model-free baseline과 비교했을 대 다양한 종류의 language를 넣었을 때 성능이 괜찮을 것이다.
- RQ3: instruction을 world model에 넣는 것은 language-conditioned policy를 사용하는것보다 나쁘지 않을 것이다. 
- RQ4: multimodal generative model을 통해 grounded language generation과 offline text-only data 학습이 가능함을 보임

- RQ1: {image, language}를 timestep 별 pair로 넣는 것이 더 좋을 것이다
  - <img width="539" height="378" alt="Image" src="https://github.com/user-attachments/assets/a062dd81-d5ce-405f-82cc-e346ef82eae9" />
  - language conditioned인 다른 베이스라인(~10M) 대비 Dynalang 이 가장 좋았음.

- RQ2 & 3:
  - language instruction 외에도 language hint가 있는 환경인 HomeGrid를 제안.
  - <img width="780" height="563" alt="Image" src="https://github.com/user-attachments/assets/eb8dcac4-e830-4351-bbe8-2043ec8ffef8" />
  - 100 step 내에 퀘스트를 많이 성공하는 것이 reward 
  - future observation : object가 어디있는지 
  - dynamics : 쓰레기통을 열려면 어떤 행동을 해야하는지 
  - correction: 현재 목표와의 거리가 멀어지면 "no, turn around"와 같이 말해줌
  - 힌트를 받았을 때 더 좋은 성능을 내고, task-only instruction에서도 더 좋은 성능을 냄. 
  - <img width="790" height="153" alt="Image" src="https://github.com/user-attachments/assets/c1105eef-9278-4429-b225-314ad424f9e5" />
- game manual이 제공되어 있는 Messenger game에 대한 성능 
 - <img width="1085" height="249" alt="Image" src="https://github.com/user-attachments/assets/4184a948-4989-4d9c-89cc-458457f8d61f" />

- Vision language navigation continuous environment 
  - <img width="771" height="216" alt="Image" src="https://github.com/user-attachments/assets/5f910a70-db6f-4958-8887-c94978d92793" />
  - 길을 찾는 task이고 조금 더 action이 low-level인 셋팅이 continuous environment 
  - goal과의 거리와 관련된 dense reward를 받고, 성공하면 성공 reward를 받는 형태 
  - 아니 r2d2는 아예 성공을 못하자나 ㅋㅋ 베이스라인이 이게 맞나
- LangRoom : embodied question answering 
  - 중간에 language 생성도 할 수 있는지 보여줌
  - 질답을 하되 perception을 통해 utterance가 이루어지는 셋팅 
  - <img width="786" height="203" alt="Image" src="https://github.com/user-attachments/assets/67da1aa7-f931-4544-9e75-ade8a5d6759e" />
  - 이때 vocab size를 너무 늘리면 prior 없이는 성능이 수렴하지 못했음 
  - <img width="397" height="258" alt="Image" src="https://github.com/user-attachments/assets/5073042a-bfdd-4cd9-94ec-ca9fc8fc2b3b" />
  - 이를 해결 하기 위해 world model에 entropy regularizer를 추가해서 이를 해결함 
  - <img width="513" height="53" alt="Image" src="https://github.com/user-attachments/assets/25c8b624-3224-48f3-bf35-65173c559b1e" />
- text-only pretraining
  - 여태까지는 experience online에 대한 실험이었고 offline도 필요하다고 생각해서 text only pretraining 을 해봄. 
  - <img width="386" height="229" alt="Image" src="https://github.com/user-attachments/assets/1658e95b-ab22-49b0-8359-414513e5fa72" />
  - in-domain 은  manuals from Messenger S2 games 
  - domain-general text는 GPT-4로 생성된 2M short story
  - T5를 쓰는 것보다 one-hot from scratch로 general domain에 대해 학습하는 것이 더 성능이 좋았음.

  
---
- actor model config
  - <img width="1069" height="687" alt="Image" src="https://github.com/user-attachments/assets/3e10ebf3-1fec-4724-903b-fad88b2fc20b" />

  