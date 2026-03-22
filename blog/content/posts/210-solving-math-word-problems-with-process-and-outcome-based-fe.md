---
title: "Solving math word problems with process and outcome-based feedback"
date: 2024-12-16
tags: ['DeepMind', '2022Q4', 'RL']
paper: "https://arxiv.org/abs/2211.14275"
issue: 210
issueUrl: "https://github.com/long8v/PTIR/issues/210"
summary: "Mentioned in a video about O1 - various analyses. Not sure how important the paper actually is"
---
<img width="639" alt="image" src="https://github.com/user-attachments/assets/612c3113-63dc-45e3-ba2a-b8b36be21c71" />

[paper](https://arxiv.org/abs/2211.14275)

## TL;DR
- **I read this because.. :** o1 It was mentioned in a video about it, so I thought I'd check it out.
- **task :** math 
- **problem :** outcome-based vs process-based 
- **idea:** Use GSM8K to 1) learn only the final answer 2) learn by adding human correctness annotations for each reasoning step to the human generated reasoning trace or model generated.
- **architecture :** ours base-70B (like it's a secret)
- **objective :** ce (SFT) / bce (ORM / PRM) 
- **baseline :** PaLM-540B, Minerva-540B, GPT-J-6B, Codex-175B, InstructGPT-175B, GPT-175B 
- **data :** GSM8K -> (eval) GSM8K-test, MATH 
- **evaluation :** final-answer error rate / trace error rate(human annotated). MATH dataset (OOD error rate)
- **result :** 1) outcome-, process- both have similar final answer error rate. 2) both process- and outcome- RMs can generate process-based feedback 3) process-based feedback or reward model is needed to reduce trace error
- **contribution :** Lots of analysis. Not sure how important the paper actually is

## Details

<img width="674" alt="image" src="https://github.com/user-attachments/assets/3b14ca49-1d43-45ab-85c9-ea2758474885" />

### training: overview
- step: new-line seperated (one line is one step)
- answer: last line 
- policy network: "each step" as an action, "all the tokens so far" as an observation
  - train with few-shot prompt, SFT,  RL 
- reward model -> used for reranking
 
### SFT
- Learn to reasoning trace.
- Learn until val loss rises. Approximate width of 2

#### Reward model
- ORM: Similar to #209, learn with binary labels for whether the final answer is correct or incorrect
- PRM: Learn from binary labels if the step so far is correct
- These are labeled as human annotated.
- Both are trained using samples from the current policy model. (temperature 1.0. K=96).
- Starting from SFT for ORM, starting from pretrained lm for few-shot.
- For PRM, annotated with 3 samples per question from the SFT policy network.
- The problem is centered on kids with incorrect SFT predictions.
- For PRM, initialize with ORM model and select optimal val loss before 2000 steps because val loss fluctuates a bit

#### Decoding
- Take 96 samples and apply some decoding techniques
- self-consistency
- RM weighted decoding (==verifier voting) -- voting weighted by RM score
- Slightly better than the highest RM score
 
#### RL via Expert Iteration
<img width="642" alt="image" src="https://github.com/user-attachments/assets/466caba0-9532-48ab-9c99-b3cc48c06762" />

I haven't read it, so I'm not sure, but it seems like you're talking about using a kid trained with RL as a policy to pull traces and repeat it.

- SFT vs few-shot based
- initial policy network is SFT or base LM with 5-shot prompt, or optional

<img width="652" alt="image" src="https://github.com/user-attachments/assets/e1f1d5d7-0d66-4e02-a2cd-989306cbc809" />

- Policy Improvement
  - final-answer RL(a.k.a. self-taught reasoner)
- Draw K samples per question and filter by accuracy of final-answer
- For SFT, select only one per question (no reason)
  - ORM-RL
- Select the app that the ORM scored highest out of K traces
  - PRM-RL
- Draw K (=96) candidate steps and choose the one with the highest score in PRM. Exit if final answer or after 15 steps
- For a few-shot base, RM is retrained each time, and for SFT, RM is fixed.

#### Data annotation
- For stepwise labels, it asks to find the first incorrect step in the generated model. This criterion is based on 1) the representation is incorrect, or 2) there is no possibility to get to the correct answer without undoing this step.

### Result 
<img width="661" alt="image" src="https://github.com/user-attachments/assets/d01720cf-7055-4b0b-a99e-95c6fc61a020" />

- The final answer SFT alone improves performance (last row of 3.1, `SFT, Majority Voting` 22.3 vs `Few-shot+Final-Answre..` 23.5).
- Analyzed that Few-shot + final-answer rl is different because it has 1-4 tokens worth of supervision, while SFT has Hunderes.

<img width="316" alt="image" src="https://github.com/user-attachments/assets/93426b52-958c-4a34-a4b2-5f32a457c60d" />

- ORM-superviesed reward models ~= PRM 
- In the figure above, we can see that the results trained with ORM have a high agreement with the PRM label results
- Also, when comparing `SFT, majority voting` tracing error 11.4 vs `SFT, ORM ranking` 4.4, it was found that ORM alone can reduce trace errors significantly.
- However, this result may only be true for this domain.

<img width="338" alt="image" src="https://github.com/user-attachments/assets/526483fe-ae0d-4554-b5b4-a4532c9c8c15" />

- low trace error requires process-based feedback or reward model 
- The difference between `Few-shot Final-answer RL,... ' and `SFT, Majority Voting`, the final answer is almost the same, but the trace error is much different (19.8 vs 11.4).
- The same trend occurs for `Few-shot + Final Answer RL, ORM reranking` 12.4 vs SFT, ORM / PRM reranking 4.4 - 3.4
- But if we put `ORM-RL` here, the `few-shot + ORM RL, ORM reranking` trace error also drops to 5.5
- This means you either need a process SFT or a reward model

<img width="669" alt="image" src="https://github.com/user-attachments/assets/030dfbc6-7cd3-48df-b3c1-1c63dd38ee55" />

- RL improves performance significantly in the Few-shot setting and moderately in SFT.
- In particular, for RM decoding + final answer rl, there was almost no performance improvement.