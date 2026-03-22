---
title: "[193] Scaling of Search and Learning: A Roadmap to Reproduce o1 from Reinforcement Learning Perspective"
date: 2024-12-30
tags: ['survey', '2024Q4', 'reasoning']
paper: "https://arxiv.org/abs/2412.14135"
issue: 213
issueUrl: "https://github.com/long8v/PTIR/issues/213"
---
<img width="598" alt="image" src="https://github.com/user-attachments/assets/7281294c-6a9a-40dc-b17c-0ba18d330008" />


[paper](https://arxiv.org/abs/2412.14135)

## TL;DR
- **I read this because.. :** survey paper. 추천받아

## Details
<img width="564" alt="image" src="https://github.com/user-attachments/assets/63e40752-0434-401c-a956-619e8981b829" />

search, learning, policy initialization, reward로 나누어서 설명

### Policy Initialization 

<img width="792" alt="image" src="https://github.com/user-attachments/assets/00bce291-1a51-49d4-8f59-53ce8831963b" />

<img width="923" alt="image" src="https://github.com/user-attachments/assets/a3640e4b-c076-44e4-b32c-cf3c93767328" />

o1을 보면 human-like한 Reasoning behavior들을 가지고 있음.
<img width="900" alt="image" src="https://github.com/user-attachments/assets/1e732c12-e838-4732-9a89-1738b96f64b4" />

alternative proposal 관련된 연구로는 divergent CoT란 연구가 있음 (https://arxiv.org/abs/2407.03181)
여러가지 cot를 sequence로 엮어서 inference 시키는 것 (o1 journey에 journey learning이랑 비슷 or 뒤에 나올 sequence search랑 비슷)

### Reward Design

<img width="713" alt="image" src="https://github.com/user-attachments/assets/e75eafd1-a489-4ced-8b31-b4cf605b7e8f" />


일단 가장 크게 나누면 ORM / PRM이 있음
<img width="901" alt="image" src="https://github.com/user-attachments/assets/dd9635d3-5ad7-40c1-81c9-d74ccbef23c6" />

ORM은 #209 이 대표적이고 PRM은 ligthman et al.이 대표적인듯.
PRM에서 process는 토큰( https://arxiv.org/abs/2404.12358 )이 될 수도있고 step이 될수도 있음. 

**reward from env** 
- from realistic env
code의 경우 compiler나 intepreter로
- from simulator environment
수학문제에 대해 verifier를 학습해서 test time에 사용하는 것도 일종의 simulator.
reward signal을 학습하는건 좋은데 rm을 학습한 policy와 현재 Policy가 달라지면서 distribution shift 문제가 생김
이를 해결하기 위해 world model(=transition까지 학습)이 언급되기도함
- from ai judgment

**reward from data**
- learn from preference data
DPO / PPO RM 학습
- learn from expert data
inverse reinforcement learning이 rl에서는 많이 쓰이는데 llm에는 제대로 도입된 바가 없음. 
preference data와 달리 구하기가 쉬우나 adversarial training이 필요해서 학습이 조금 까다로움 

**reward shaping**
llm의 reward는 가장 마지막 토큰에 나와서 이걸 뿌려주는걸 reward shaping이라고 함 
q-value를 사용하는 문헌들이 나왔으나 이건 policy dependant하기 때문에 좋지 않다는 문헌 또한 나왔음
potential based reward shaping이 전통적으로 rl에서 reward shaping해주는 방식임 (https://people.eecs.berkeley.edu/~pabbeel/cs287-fa09/readings/NgHaradaRussell-shaping-ICML1999.pdf)
<img width="424" alt="image" src="https://github.com/user-attachments/assets/8d405d3a-990e-42e5-8743-ffbf2c4cf3ae" />

https://arxiv.org/pdf/2410.08146 가 비슷한 접근법으로 orm으로 prm을 만들어주었고, dpo가 이미 potential based reward shaping을 해준다는 연구도 나옴(https://arxiv.org/abs/2404.12358)

**o1에 대한 추측**
reward model 여러개를 쓰고 있을 것 같음 - 수학에서는 prm을 쓰고 있지 않을까?
few-shot sample에 ft이 가능한것을 보아 매우 강건한 rm을 가지고 있을 것 같음
value head를 쓰기보다 llm 생성을 하면서 Reward를 generate하고 있을 것 같음 
(추측들에 대한 이유는 잘 모르겟음..)


### Search
<img width="805" alt="image" src="https://github.com/user-attachments/assets/b1de85b0-6d0e-4ec4-94b6-5124489522e7" />

<img width="907" alt="image" src="https://github.com/user-attachments/assets/be51f4eb-984e-4a3c-88ed-7da7745a711a" />

**BoN sampling**
여러개 샘플링 한 뒤 RM을 사용하여 best를 뽑아내는 방법
speculatvie rejection 등등 연구들 있음

**Beam Search**
널리 사용됨.
DPO에서 나오는 token-level reward를 가지고 search(TreeBoN), value model의 value를 가지고 search 등등 여러가지 후속연구가 있음
이러한 reward guided search는 다운스트림 태스크에 더 잘 align된다고 알려져있음

<img width="872" alt="image" src="https://github.com/user-attachments/assets/cc53f770-fd85-45ef-988f-425598105959" />

**Monte Carlo Tree Search**
large search space에서 유리. selection, expansion, evaluation, backprop을 반복하면서 explore / exploit 하는 알고리즘. 이걸 token-, step-, solution- 레벨로 하는 연구들이 있음. (읽어보진 않음)
그 외에 dfs, bfs, a*, tree-of-thought, best-first-search 등 여러 서치 방법이 쓰일 수 있음

**Sequential Revision**
과거 정답을 refine하는 식으로 sequential하게 하는 방식을 sequential revision으로 칭함 
SELF-REFINE or snell et al.이 대표적인 연구인듯.
이게 진짜 효과적인지는 논란의 여지가 있는데, external feedback없이는 self-correct할 수 있는 능력이 없다고 하는 주장(https://arxiv.org/abs/2310.01798, iclr)도 있고, 반대로 generation보다 discern하는게 더 쉬워서(https://aligned.substack.com/p/ai-assisted-human-feedback) 잘 될 수 있다고 얘기하는 주장도 있음. (ft없이 zs로 얘기하는듯)

**tree search + sequential revision**
https://arxiv.org/abs/2406.07394 이 연구가 대표적
snell et al이 n개의 sample에 대해 sequntial revision을 한뒤 verifier로 BoN 결합 

**o1에 대한 추측**
train-time search에선 tree search or BoN으로 데이터를 만들었을 거라고 추측.
그리고 코드/수학 같은 도메인에 대해서 external environment를 사용하여 만들었을거라고 추측
teset-time search에 대해선 sequential revision을 사용한것으로 보이고 tree search는 Infer에 쓰기엔 overhead가 너무 심해서 안쓰였을 것으로 보임 

### learning
<img width="632" alt="image" src="https://github.com/user-attachments/assets/a74ad66b-aadf-47d4-ad7f-5ef5685bcd43" />


**o1에 대한 추측**
behavior cloning이 더 효과적이어서 이거 먼저 하고 그 다음에 dpo or ppo를 했을 것.
이를 반복적으로 하면서 성능을 개선 시켰을 것으로 추정 (llama3 #205 와 비슷하게)

