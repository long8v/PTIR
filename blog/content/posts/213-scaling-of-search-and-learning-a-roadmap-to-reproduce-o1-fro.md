---
title: "[193] Scaling of Search and Learning: A Roadmap to Reproduce o1 from Reinforcement Learning Perspective"
date: 2024-12-30
tags: ['survey', '2024Q4', 'reasoning']
paper: "https://arxiv.org/abs/2412.14135"
issue: 213
issueUrl: "https://github.com/long8v/PTIR/issues/213"
summary: "survey paper. recommended"
---
<img width="598" alt="image" src="https://github.com/user-attachments/assets/7281294c-6a9a-40dc-b17c-0ba18d330008" />


[paper](https://arxiv.org/abs/2412.14135)

## TL;DR
- **I read this because.. :** survey paper. recommended by

## Details
<img width="564" alt="image" src="https://github.com/user-attachments/assets/63e40752-0434-401c-a956-619e8981b829" />

Divided into search, learning, policy initialization, and reward.

### Policy Initialization 

<img width="792" alt="image" src="https://github.com/user-attachments/assets/00bce291-1a51-49d4-8f59-53ce8831963b" />

<img width="923" alt="image" src="https://github.com/user-attachments/assets/a3640e4b-c076-44e4-b32c-cf3c93767328" />

o1 has human-like reasoning behaviors.
<img width="900" alt="image" src="https://github.com/user-attachments/assets/1e732c12-e838-4732-9a89-1738b96f64b4" />

An alternative proposal Related research includes a study called divergent CoT (https://arxiv.org/abs/2407.03181)
Inferring multiple COTs in a sequence (similar to journey learning in o1 journey or sequence search later)

### Reward Design

<img width="713" alt="image" src="https://github.com/user-attachments/assets/e75eafd1-a489-4ced-8b31-b4cf605b7e8f" />


Once you break it down into its largest pieces, you have ORM/PRM
<img width="901" alt="image" src="https://github.com/user-attachments/assets/dd9635d3-5ad7-40c1-81c9-d74ccbef23c6" />

ORMs are represented by #209 and PRMs are represented by ligthman et al.
In PRM, process can be a token ( https://arxiv.org/abs/2404.12358 ) or a step.

**reward from env** 
- from realistic env
For code, the compiler or intepreter can use the
- from simulator environment
Learning a verifier for a math problem and using it at test time is a kind of simulator.
Learning the reward signal is good, but the current policy is different from the policy that learned RM, causing a distribution shift problem.
To solve this, the world model (=learn until transition) is sometimes mentioned
- from ai judgment

**reward from data**
- learn from preference data
DPO / PPO RM learning
- learn from expert data
Inverse reinforcement learning is used a lot in RL, but hasn't been properly introduced in LLM.
Unlike preference data, it's easy to obtain but a bit tricky to learn because it requires adversarial training

**reward shaping**
LLM's reward comes in the last token and sprinkling it is called reward shaping.
There is some literature that uses q-values, but there is also literature that says this is not good because it is policy dependent.
Potential based reward shaping is how RL has traditionally shaped rewards (https://people.eecs.berkeley.edu/~pabbeel/cs287-fa09/readings/NgHaradaRussell-shaping-ICML1999.pdf)
<img width="424" alt="image" src="https://github.com/user-attachments/assets/8d405d3a-990e-42e5-8743-ffbf2c4cf3ae" />

https://arxiv.org/pdf/2410.08146 has created a PRM with an ORM with a similar approach, and there's research showing that DPOs already do potential-based reward shaping (https://arxiv.org/abs/2404.12358).

**Conjecture about O1
I'm guessing you're using multiple reward models - in math you're using PRMs, right?
Seems to have a very robust RM as FT is possible on a few-shot sample
Looks like we're generating reward while creating LLM rather than writing value head
(Not sure about the reasoning behind the guesses...)


### Search
<img width="805" alt="image" src="https://github.com/user-attachments/assets/b1de85b0-6d0e-4ec4-94b6-5124489522e7" />

<img width="907" alt="image" src="https://github.com/user-attachments/assets/be51f4eb-984e-4a3c-88ed-7da7745a711a" />

**BoN sampling**
How to sample multiple data points and use RM to pick the best one
There are studies on speculatvie rejection, etc.

**Beam Search**
Widely used.
There are various follow-up studies such as search(TreeBoN) with token-level reward from DPO, search with value from value model, etc.
This reward guided search is said to better align with downstream tasks

<img width="872" alt="image" src="https://github.com/user-attachments/assets/cc53f770-fd85-45ef-988f-425598105959" />

**Monte Carlo Tree Search**
Advantageous in large search space. Algorithms that iterate through selection, expansion, evaluation, backprop to explore/exploit. There are studies that do this at the token-, step-, and solution-level. (I haven't read them)
Other search methods may include dfs, bfs, a*, tree-of-thought, best-first-search, etc.

**Sequential Revision**
Sequentially refining past answers is called sequential revision.
SELF-REFINE or snell et al. are representative studies.
Whether it really works is debatable, with some arguing that it doesn't have the ability to self-correct without external feedback (https://arxiv.org/abs/2310.01798, ICLR), and others saying that it's easier to discern than to generate (https://aligned.substack.com/p/ai-assisted-human-feedback), so it could work. (like talking about zs without ft)

**tree search + sequential revision**
https://arxiv.org/abs/2406.07394 This study is representative of the
snell et al sequntial revision on n samples and combine BoN as verifier

**Conjecture about O1
In train-time search, we assume that the data was created with tree search or BoN.
And for domains like code/math, I'm guessing you used external environment to create it.
For teset-time search, sequential revision was used and tree search was not used because it was too overhead to use for Infer.

### learning
<img width="632" alt="image" src="https://github.com/user-attachments/assets/a74ad66b-aadf-47d4-ad7f-5ef5685bcd43" />


**Conjecture about O1
Behavior cloning is more effective, so I would have done this first and then DPO or PPO.
I did this iteratively and presumably improved performance (similar to llama3 #205)

