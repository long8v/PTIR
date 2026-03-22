---
title: "[192] Scaling Test-time Compute with Open Models (hf blog)"
date: 2024-12-23
tags: ['2024Q4', 'test-time-scaling', 'reasoning']
paper: "https://huggingface.co/spaces/HuggingFaceH4/blogpost-scaling-test-time-compute"
issue: 212
issueUrl: "https://github.com/long8v/PTIR/issues/212"
---
<img width="700" alt="image" src="https://github.com/user-attachments/assets/e002f812-65ad-444e-b175-748b262501ac" />

[paper](https://huggingface.co/spaces/HuggingFaceH4/blogpost-scaling-test-time-compute)

## TL;DR
- **I read this because.. :** reasoning 쪽 survey. 추천받아
- **task :** test-time scaling 해보자 
- **architecture :** Llama 3.2 1B instruct / Llama 3.2 3B instruct / Llama 3.1 70B 
- **baseline :** (infer) zero-shot CoT (PRM) Math-Shepherd
- **data :** (PRM) `RLHFlow/Llama3.1-8B-PRM-Deepseek-Data` 
- **evaluation :** Math-500 accuracy
- **result :** 
- **contribution :** 방법들 정리 및 테스트 

## Details
### Strategies for test-time compute scaling
- self-refinement
refine their own outputs or “thoughts” by identifying and correcting errors in subsequent iterations
built-in refinement 능력이 있어야 함
- Search Against a Verifier
generation model들이 multiple answer를 내고 별도의 verifier가 있어서 multiple answer중 선택하는 형태
hard coding된 verifier일 수도 있지만 일단 learned verifier를 상정(https://github.com/long8v/PTIR/issues/209)
verifier가 있으면 BoN이나 tree search에서 사용될 수 있다

<img width="727" alt="image" src="https://github.com/user-attachments/assets/69900b28-9390-4c49-b3d3-df43c31339bd" />

가능한 방법들 
- Best-of-N: Generate multiple responses per problem and assign scores to each candidate answer, typically using a reward model. Then select the answer with the highest reward (or a weighted variant discussed later). This approach emphasizes answer quality over frequency.
- Beam search: A systematic search method that explores the solution space, often combined with a [process reward model (PRM)](https://huggingface.co/papers/2211.14275) to optimise both the sampling and evaluation of intermediate steps in problem-solving. Unlike conventional reward models that produce a single score on the final answer, PRMs provide a sequence of scores, one for each step of the reasoning process. This ability to provide fine-grained feedback makes PRMs a natural fit for search methods with LLMs.
- Diverse verifier tree search (DVTS): An extension of beam search we developed that splits the initial beams into independent subtrees, which are then expanded greedily using a PRM. This method improves solution diversity and overall performance, particularly with larger test-time compute budgets.

### Experimental setup

<img width="791" alt="image" src="https://github.com/user-attachments/assets/62a87b7e-83a1-4b4e-90ba-d6ffa04e0127" />

### Result
- majority voting / Self-consistency
<img width="726" alt="image" src="https://github.com/user-attachments/assets/e4ad2284-c7ff-454a-88f0-6c37813c7dde" />


- Best-of-N
vanilla Best-of-N은 RM이 가장 높은 점수를 매긴 애를 정답으로 뽑는거고 Weighted Best-of-N는 RM의 score를 가중으로 해서 정답을 뽑을 때 선정
이때 rm score를 ORM로 하는게 일반적이지만 비교를 위해 PRM으로 사용. 

<img width="735" alt="image" src="https://github.com/user-attachments/assets/a9f76e62-9227-4bba-bfaf-af464c44dc18" />

이때 PRM은 step별로 점수가 나오기 때문에 어떤 score를 쓸지도 문제인데 이에 대해서는 [deep mind 논문](https://huggingface.co/papers/2211.14275)에서와 마찬가지로 Last가 가장 좋았음 

<img width="728" alt="image" src="https://github.com/user-attachments/assets/2551fe8b-2ac3-437e-9c46-141fe3fb9164" />

개중에는 weighted BoN이 가장 좋았다. 다만 아직 8B zs-cot를 못이긴다. 

- Beam search with process reward models
1) beam 개수 N개를 매 스텝별 유지하면서 beam search. 
2) 이때 `\n` 또는 `\n\n` 등으로 정의 된 stopping criterion을 기준으로 step을 나눔. 
3) PRM을 통해 각 step에 대한 점수를 매겨서 M개 중에 N개를 선정 함 
4) 3을 계속함
5) eos나 maximum search에 도달할 때 까지 진행함

hparm은 아래와 같음
- N﻿ beams in compute scalings of 4, 16, 64, 256
- Fixed beam width m = 4
- Sampling with temperature T=0.8﻿
- Up to 40 iterations, i.e. a tree of maximum depth with 40 steps.
<img width="753" alt="image" src="https://github.com/user-attachments/assets/7a0abd94-aa74-4c0d-a0ba-54e8425ed5bb" />

이렇게 하니까 8B를 이겼고 절대적인 MATH 점수 자체도 괜찮은 편이라고 함 (CS PhD 점수 평균이 0.4라고 함(엄청 어렵네..))

- when beam search works well?
<img width="744" alt="image" src="https://github.com/user-attachments/assets/f85f0342-ba33-4aff-a035-9d31c64bc6ee" />

전반적으로 Majority voting 은 계산 복잡도 대비 가장 구림.
어려울 수록 beam search가 더 잘하지만 난이도 1~2에 대해서는 BoN이나 심지어 majority voting 보다 안좋음 

- DVTS: boosting performance with diversity
<img width="693" alt="image" src="https://github.com/user-attachments/assets/cbf046d5-8408-45b1-8bd4-2af8d77d7ad6" />

tree 랑 뭐가 다르냐면 M개를 확장할 때 tree를 독립적으로 키우는게 다른듯 (e.g. "A world" vs "A happy" 이렇게 두개의 path가 살아 있을 때 N개를 뽑을 때 A world가 더 유망해서 N개가 뽑힐 수 있는데, 그렇게 말고 독립적으로 N개를 나눠서 expand하는 기법인듯)

<img width="727" alt="image" src="https://github.com/user-attachments/assets/453f9bc8-c5f8-4a29-a725-14285a26c10c" />

이렇게 했을 때 answer개수가 커질 때 scaling이 더 잘됨! 
<img width="704" alt="image" src="https://github.com/user-attachments/assets/887a1984-a7eb-4e4b-ae05-c5e082b20076" />

난이도별로 분리했을 때 DVTS는 난이도가 낮고 N이 클 때 더 잘하고 beam search는 난이도에 상관없이 N이 작을 때 더 잘했다
추가로 가장 어려운 난이도에서는 beam search가 전반적으로 더 잘하넹

- compute optimal scaling
<img width="482" alt="image" src="https://github.com/user-attachments/assets/d1419039-3af6-451d-999f-e0c11ec24c38" />

given compute budget N일 때 strategy를 선택할 수 있으면 좋을텐데 해서 나온 개념
이걸 구하기가 어렵기 때문에 딥마인드 연구에서는 그냥 난이도는 주어진걸로 보고 각 난이도에서 가장 잘하는 접근법을 뽑은 뒤 이걸로 선택하는 (??) 전략을 취했다고 함 
이렇게 했을 때 성능 

<img width="739" alt="image" src="https://github.com/user-attachments/assets/a10c327c-6a20-4ae3-82e2-cd45c8e9093d" />

- Scaling up to larger models
<img width="736" alt="image" src="https://github.com/user-attachments/assets/ccf2458f-d9c4-48e2-bc7e-a9b8ac924e7d" />

- next steps
1) The Power of Strong Verifiers:
Strong verifiers play a critical role in enhancing performance. However, their current limitations are apparent, as highlighted in benchmarks like ProcessBench. Improving the robustness and generalization of verifiers will be crucial for advancing these methods.

2) The Challenge of Self-Verification:
The ultimate goal—or "holy grail"—is achieving self-verification, where models can validate their own outputs autonomously. This approach appears to be what models like o1 are doing, but remains difficult to implement in practice. Unlike standard supervised fine-tuning (SFT), self-verification demands more nuanced strategies. The recent DeepMind paper on self-verification and Score sheds light on this challenge and offers a pathway for future research.

3) Integrating “Thoughts” into the Process:
Incorporating explicit intermediate steps or “thoughts” during generation could further enhance reasoning and decision-making. By integrating structured reasoning into the search process, we may unlock better performance on complex tasks.

4) Search as a Data Generation Tool:
This method can also serve as a powerful data generation process, creating high-quality training datasets. For example, fine-tuning models like Llama 1B on correct traces produced by search could yield significant gains. This on-policy approach resembles techniques like ReST or V-StaR but with the added benefits of search, offering a promising direction for iterative improvement.

5) A Call for More PRMs:
Open process reward models (PRMs) are relatively rare, limiting their broader application. Developing and sharing more PRMs for different domains is a critical area where the community can contribute significantly.

6) Expanding Beyond Verifiable Domains:
While current methods excel in domains like math and code, where solutions are inherently verifiable, extending these techniques to other areas remains a major challenge. How can we adapt these strategies for less structured or subjective tasks? This is a vital question for future exploration.

