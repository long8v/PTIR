---
title: "[198] Kimi k1.5: Scaling Reinforcement Learning with LLMs"
date: 2025-01-23
tags: ['multimodal', 'RL', 'reasoning', '2025Q1']
paper: "https://github.com/MoonshotAI/Kimi-k1.5/blob/main/Kimi_k1.5.pdf"
issue: 219
issueUrl: "https://github.com/long8v/PTIR/issues/219"
---
![Image](https://github.com/user-attachments/assets/7d0ae2f3-30f7-4a1a-bd18-51b7c03adc43)

[paper](https://github.com/MoonshotAI/Kimi-k1.5/blob/main/Kimi_k1.5.pdf)

## TL;DR
- **I read this because.. :** deepseek-r1과 함께 언급되어. multimodal 언급.
- **task :** reasoning ability in LLM
- **problem :** 긴 reasoning이 필요한 LLM을 학습하고 싶은데 value function/ PRM/ MCTS이런거 너무 복잡하다 
- **idea :** RLOO 적용하자. reward는 verify가능한걸로 하자. prompt를 잘 만들자. 긴 context로 먼저학습하고 short는 distil 하자
- **input/output :** {q, (optional) image} -> a
- **architecture :** (proposed) kimi k1.5. 아키텍쳐나 크기는 이전 논문을 읽으면 되는건지.. 못찾겠네 
- **objective :** (pretraining, sft) ce loss -> (rl) RLOO loss with offline samples 
- **baseline :** OpenAI o1, OpenAI o1 mini, [QVQ-72B mini](https://qwenlm.github.io/blog/qvq-72b-preview/), QwQ-32B Preview
- **data :** (all proposed, not open) (PT) ?? (SFT) 1M SFT, 1M VLM SFT (CoT SFT) ? (RL) diverse / non-hackbable prompts 
- **evaluation :** AIME, MATH500, Codeforces, LiveCodeBench v5, Mathvista, MMMU
- **result :** openai 모델들보다 long, short 둘다 성능 좋음 
- **contribution :** R1보다 상세하게 prompt 정제 과정 등을 정리한듯.
- **etc. :** (성현님 comment) 

## Details
### thumbnail
- long cot
![Image](https://github.com/user-attachments/assets/621c172e-bf33-4c6e-89a4-fd1085fa4b40)

- short cot
![Image](https://github.com/user-attachments/assets/178984a0-d1f3-4aa0-b8e7-792f63633b2d)

### RL prompt set curation
3가지를 중점으로 high quality prompt를 찾았다고 함 
- diverse coverage : stem, code, general reasoning 
  - -> 이를 위해 데이터셋 별로 domain / discipline을 태깅 하고 균형잡히게 골랐다고 함 
- balanced difficulty : easy, moderate, difficult를 균형잡히게 모아야 함 
  - -> model based로 10번 중 pass rate를 보고 difficulty를 측정했다고 함 
- accurate evaluability : verifier로 하여금 객관적이고 믿을만한 평가가 가능해야함. superficial pattern / random guess에 의존하게 하면 안됨 
  - -> reward hacking을 방지하기 위해 multi-choice, true/false, proof-based question(질문에서 답을 알 수 있는것)을 제거 
  - -> 'easy-to-hack'을 제거하기 위해 CoT reasoning step 없이 답을 하게 한뒤에 8번만에 정답을 맞춘 질문들은 지웠다고 함

### Long-CoT SFT
- planning / evaluation / reflection / exploration을 하는 데이터를 넣어줬다고 함. 
- model한테 prompt를 해서 생성해줬다고함(rejection sampling). 어떤 모델을 썼는지 수량은 어떤지 잘 모르겠음. 

### Reinfocement Learning 
#### problem setting
  - planning algorithm에 비유했지만 비슷하지만 결국 flatten된 sequence of reasoning path를 학습(내가 rl background가 없어서 그런가 그냥 장황하게만 느껴짐..)
- 우리의 objective는
  - <img width="471" alt="Image" src="https://github.com/user-attachments/assets/ccdb429e-796e-47b0-8fe7-888d4544632b" />
  - 이때 $z$는 reasoning steps / $r$는 {0,1}로 떨어지는 verifiable reward

#### policy optimization
online policy mirror decent algorithm을 차용했다고? (https://www.ijcai.org/proceedings/2019/0434.pdf, https://github.com/manantomar/Mirror-Descent-Policy-Optimization // 조금 찾아보니 PPO 처럼 제약 사항 하의 최적화인데 최적화 방식이 gradient descent가 아니고 다른 것인듯 하다. 

<img width="1113" alt="Image" src="https://github.com/user-attachments/assets/7e95f5cb-a97c-49cf-81c2-cfa2bb21b6e1" />

TRPO에서 많이 본 느낌인데 나중에 천천히 봐야할듯ㅜ 


<img width="1117" alt="Image" src="https://github.com/user-attachments/assets/de896bfd-9315-43ab-a994-b4a42aa50019" />

결론적으로 gradient 는 위와 같이 되는데, policy gradient와 비슷하되 baseline이 mean of sampled reward(https://github.com/long8v/PTIR/issues/215#issuecomment-2608698801) 를 사용하는 것이 다르다.
아 그리고 원래는 online rollout을 사용했는데 여기선 reference model의 rollout을 사용했다는 것도 다른점임
"value network"자체를 지우는 것이 좋았던 이유는 긴 reasoning path를 학습하는 과정에서 value 네트워크가 있을 때 negative cot 의 중간 step들이 바로 negative advantage를 가지게되는데, 다양한 reasoning path를 학습하기 위해선 exploration도 필요하기 때문에 "RLOO"알고리즘에서 rollout을 해서 끝까지 가보는게 더 중요했던듯 하다 (!!)

#### length penalty
overthinking 방지용 

<img width="918" alt="Image" src="https://github.com/user-attachments/assets/0de3f0c3-078d-4440-ad74-8c333dacfd43" />

#### sampling 
- curriculum sampling: 난이도 낮은 것에서 점점 높도록
- prioritized sampling: 모델이 성능이 낮은 것을 중심적으로 

#### Reward Modeling for math
정답이 $a^2-4$인거나 $(a+2)(a-2)$나 같은 것인데 이를 해결하기 어려워서 math에 대해서는 RM을 사용
이때 CoT RM을 사용했다고 함 (#211) -- 800K CoT-Labeled reward model을 사용 
그냥 classic RM에 비교했을 때 84.4 -> 98.5로 성능 차이가 커서 CoT RM 썼다고 함. 

#### vision data
- real world: chart understanding, science question, graphical comprehension
- synthetic visual reasoning : clevr같은 류인듯? 
- text rendeered data: text / code / structured data

### long2short
- model merging : with long-cot model
- shortest rejection sampling : 8개 rejection sampling해서 정답을 맞춘 것 중 가장 짧은걸 sft데이터셋으로
- DPO: (chosen) short correct answer (rejected) long and wrong answer, long and correct answer
- long2short : 위의 length penalty 적용

## other training
- pretraining : Vision PT까지 한게 특이점. 이거 나중에 좀 정리해야..
- vanilla SFT: text 1M / Vision 1M 
  - seq len 23K 

### RL infrastructure
- 생략 

## Result
<img width="879" alt="Image" src="https://github.com/user-attachments/assets/3939da0b-9974-46e5-b53d-72f0cacc98c8" />
 
<img width="738" alt="Image" src="https://github.com/user-attachments/assets/41ca2e08-021b-4c3b-be21-1db25f19ef7d" />

<img width="666" alt="Image" src="https://github.com/user-attachments/assets/e6355d53-87d5-4426-9f6e-670d86b69aa8" />

- ablations

<img width="671" alt="Image" src="https://github.com/user-attachments/assets/b3846762-7094-4ff2-aa6a-1533f7e3e717" />