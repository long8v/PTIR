---
title: "Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters"
date: 2025-01-03
tags: ['DeepMind', '2024Q3', 'reasoning']
paper: "https://arxiv.org/abs/2408.03314"
issue: 214
issueUrl: "https://github.com/long8v/PTIR/issues/214"
summary: "It is repeatedly mentioned in #213"
---
<img width="975" alt="image" src="https://github.com/user-attachments/assets/ce60aa20-2c3f-4833-9c0c-07cbbab95788" />

[paper](https://arxiv.org/abs/2408.03314)

## TL;DR
- **I read this because.. :** #213 keeps referring back to
- **task :** test time scaling in LLM 
- **problem :** Analysis of test-time scaling techniques.
- **architecture :** PaLM-2 (340B) // llama 2 family (when viewing pretraining <-> test time)
- **data :** (PRM) Create new with PaLM-2 + monte carlo roll-out with PRM800K prompt
- **evaluation :** MATH test split (500)
- **contribution :**

## Details
- thumbnail
<img width="981" alt="image" src="https://github.com/user-attachments/assets/fa14336f-d5d4-4d90-87ca-068dd80cb218" />

### test-time scale up 
What matters is how you can spend it most effectively within your limited "inference cost".
with **"test-time compute-optimal scaling strategy"**.
<img width="470" alt="image" src="https://github.com/user-attachments/assets/2f5f7eea-cc85-4c02-9077-9ed1a75c9d9b" />

Find the optimal test-time hyper-param $\theta$ for prompt $q$ within a given test-time compute resource $N$.
The intuition is that this optimization depends on the difficulty of the question.
If so, how do we measure this difficulty, we can divide it into 5 bins by measuring the difficulty with a pass@1 rate among the 2048 samples in the model (-- oracle difficulty)
But in the actual infer situation, we don't know gt, so we can run with the average of the scores of the learned verifiers for the final answer (--model-predicted difficulty)
This is an additional cost in itself, as you need to divide the difficulty in this way and then measure it with a suitable test-time scaling method.

### scaling test-time compute with verifier
Tried ORMs, but PRM consistently outperformed them, so they went with PRM
#### training PRM
- data 
- Observed that GPT-generated writes are ineffective for learning PalM 2, even with the PRM800K provided by lightman et al.
- Follow Math Shepherd and have a monte carlo rollout to find the reward for each step and use it as the value.
- Generate 16 PRMs per question by giving the base model a few-shot prompt. Run 16 monte carlo rollouts and discard those that don't produce a parsable answer.
- training
- A PRM is a binary classifier trained with a bce that predicts a soft value between 0 and 1.
- I don't know how many epoxies because it says val loss early stopping
- aggregation
- step-wise: last was best
- intesr-answer: You wrote "best-of-N-weighted" with PRM as verifier.
- search
  - BoN weighted
  - beam search: N beams; M beam width
- lookahed search: Unlike beam search, lookahed search goes K steps ahead for N beams and serachs beams with the PRM value of that step.
- To eliminate the stochastic, temperature = 0
- Think of it as MCTS minus stochastic (exploration)
 

<img width="943" alt="image" src="https://github.com/user-attachments/assets/4663f04d-6433-41ea-8ca8-0207b41149ab" />

- result 
<img width="985" alt="image" src="https://github.com/user-attachments/assets/ce5f4029-d1b0-43b7-8b4a-f07997b26e06" />

(left)
For small bugets, beam search >> BoN. For larger bugets, BoN is good.
lookahead is not as good for the same cost as other methods, possibly due to the high simulating cost. For example, we found that we kept exploring problems that could be solved in one or two steps, even if we created a long one.

<img width="627" alt="image" src="https://github.com/user-attachments/assets/65c6915e-132d-4ec7-9dc7-4af2ce0af11c" />

(right)
BoN was better for easy difficulty and beam search was better for high difficulty. -- This is intuitive: harder problems are harder to get out of fisrt place, so search is needed, and beam-search tends to over-optimize on easy difficulties.
And all of the hardest problems performed badly (as if test-time scaling didn't work), which suggests that the verifier didn't solve the hard problems correctly and ended up reinforcing spurious features through beam search, which made the performance worse. -- Hmm...

<img width="505" alt="image" src="https://github.com/user-attachments/assets/f73f4e59-0af4-4a41-b429-dad812d9e986" />
Performance is better when done the optimal way

### Refining the proposal distribution
Have them generate sequentially, like sequential refinement, etc.
<img width="969" alt="image" src="https://github.com/user-attachments/assets/7c668027-4638-45b0-b05a-1f69e095ec20" />

We took a similar approach to rescursive introspection (https://arxiv.org/abs/2407.18219, RiSE), but intuitively, when the "corrected answer" is close to the "wrong answer", it will be effective for learning refinement, so we did a pruning operation to pick out the wrong answers with such a chr edit distance, and due to lack of resources, we just did it in parallel and then concatenated them, even though we should have done it on-policy multi-turn (=sequential).
The number of incorrect answers was sampled one at a time between 0 and 4.

<img width="925" alt="image" src="https://github.com/user-attachments/assets/ab00a5e7-50a6-403c-8f09-58ed423e571e" />

When inferring, 38% of the time, even if the answer is correct, it is corrected again and again. Because of this phenomenon, if you get multiple correct answers in sequence, you can take this and use majority voting or verifier
(left) Increasing pass@1 as sequence length increases
(Right) Better performance with more compute resources than parallel voting

### trade off sequential or parallel test-time compute
The intuition is that sequential will work better for easy problems (because that's how you fix it in the method in the first place) and parallel will work better for hard problems because you need to try different things, so it's best to use both.
<img width="957" alt="image" src="https://github.com/user-attachments/assets/682282e2-cbd3-4f4b-9a78-c5d30708bc90" />

(right) At lower difficulties, it was better to just do sequential, but at higher difficulties, there was a good ratio. (parallel is not always better)

This also has an optimal value
<img width="475" alt="image" src="https://github.com/user-attachments/assets/b76375a8-01d3-4c23-8a75-0c06c947a97d" />

### tradeoff betwentes-time vs pretraining (not sure I understand)

<img width="951" alt="image" src="https://github.com/user-attachments/assets/feb201c2-05d6-456d-b6e2-e3b4a2bbec2d" />

- Pre-trained models trained with up to 14 times as many parameters as stars.
- The horizontal axis is 6 * # parm * # tokens for pretraining (==max length?? I don't understand) / 2*N * total # of generated in inference time
- The conclusion is that the higher the difficulty, the better the pretraining compute