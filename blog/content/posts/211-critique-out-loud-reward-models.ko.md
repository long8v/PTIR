---
title: "[191] Critique-out-Loud Reward Models"
date: 2024-12-17
tags: ['AllenAI', 'LLM', 'RL', '2024Q3']
paper: "https://arxiv.org/abs/2408.11791"
issue: 211
issueUrl: "https://github.com/long8v/PTIR/issues/211"
---

<img width="807" alt="image" src="https://github.com/user-attachments/assets/8a7d0ddd-d634-4c84-bc63-655ad39b94a4" />

[paper](https://arxiv.org/abs/2408.11791), [code](https://github.com/zankner/CLoud)

## TL;DR
- **I read this because.. :** o1 video에서 언급되어 
- **task :** reward model 개선 
- **problem :** llm-as-judge 같은 경우에 점수에 대한 해석도 하는데 reward model도 그렇게 못하나?
- **idea :** RM에게 critique까지 생성하라고 한 뒤 그 뒤에 reward head 달아서 예측하게 하자 
- **input/output :** {question, answer} -> {critique, reward score}
- **architecture :** Llama-3-8B / 70B
- **objective :** SFT loss + RM loss(Bradley-Terry Model)
- **baseline :** classic RM model
- **data :** UltraLlama(proposed. UltraFeedback + UltraInteract subset의 Prompt로 하고 Llama-3-8B-Instruct로 response 생성) + Llama-3.1.-405B-Instruct로 critique 및 judgement를 생성한걸 oracle로 사용
- **evaluation :** pairwise preference classification of Reward Bench, BoW win rate on ArenaHard
- **result :** 모든 부문에서 CLoud 기법이 효과. on policy가 off policy보다 항상 좋음. self-consistency 기법도 테스트해봤는데 reasoning에서만 좋음. 
- **contribution :** rm이 해석가능해진다는 점에서 좋은듯? 많이 쓰일지는 모르겠음.
- **etc. :**

## Details
- thumbnail

<img width="592" alt="image" src="https://github.com/user-attachments/assets/d8f7c4dc-bd23-4380-b9a7-67a2781f5718" />

간단함. critique을 생성하라고 하고 마지막 critique까지 포함하여 given으로 준뒤 reward head 달아서 학습
critique를 생성하는 SFT Loss와 RM loss 한번에 학습.
<img width="408" alt="image" src="https://github.com/user-attachments/assets/7969dea1-1cfb-4c63-b1eb-58d6117d64bc" />

($\lambda$는 8B에서 5/4, 70B에서 3/4로 찾아짐)

<img width="525" alt="image" src="https://github.com/user-attachments/assets/337510e0-85e0-4d7d-8958-27f4824c8caf" />

<img width="486" alt="image" src="https://github.com/user-attachments/assets/971bcbdb-5734-4b23-9613-b61f16c693ba" />

- training overview
<img width="562" alt="image" src="https://github.com/user-attachments/assets/5caf8768-d761-47d2-a93b-7ac5d0f31d8f" />

처음에는 oracle ciritque를 기반으로 학습.
oracle은 UltraLlama(proposed. UltraFeedback + UltraInteract subset의 Prompt로 하고 Llama-3-8B-Instruct로 response 생성) + Llama-3.1.-405B-Instruct로 critique 및 judgement를 생성. 
(Oracle judgment 생성 프롬프트)
<img width="571" alt="image" src="https://github.com/user-attachments/assets/740e24c4-5d6f-4105-8c91-a2e4ef37ae63" />

그 뒤에는 self-generated critique을 기반으로 학습. 
이걸 N번 돈 건 아니고 한번만 돈듯함?

### Result
- CLoud 기법의 효용?
<img width="585" alt="image" src="https://github.com/user-attachments/assets/6052a1ae-084a-4e2a-8d21-197453b80201" />

다 효과적인 것으로 나옴. RM만 평가하는게 맞는지는 모르겠음.

- on-policy vs off-policy
oracle critique을 계속 사용하는 방식
<img width="592" alt="image" src="https://github.com/user-attachments/assets/97a7d52a-ac2b-4698-877a-409f5027c6c2" />

On-policy가 확연히 효과가 좋음

- self-consistency 효과
reasoning(여기서는 critique)을 여러개 생성하게 한 뒤 그뒤에 달린 score를 평균내서 사용
<img width="546" alt="image" src="https://github.com/user-attachments/assets/e06de765-ffe3-4434-bb90-8121c6a90aab" />

reasoning 외에는 효과가 없었음.
외에 ArenaHard는 아예 효과가 없음

<img width="276" alt="image" src="https://github.com/user-attachments/assets/437d9d85-67e0-475c-8619-d4d42daad519" />

reasoning 중에서도 reason step이 1~2 step인 경우에만 효과가 있고 그 외에는 없었음.