---
title: "[178] RLAIF-V: Aligning MLLMs through Open-Source AI Feedback for Super GPT-4V Trustworthiness"
date: 2024-09-23
tags: ['RL', 'MLLM', '2024Q2']
paper: "https://arxiv.org/pdf/2405.17220"
issue: 197
issueUrl: "https://github.com/long8v/PTIR/issues/197"
summary: "RLHF-V Successor - Quickly Glue RLAIF to VLM!"
---
![image](https://github.com/user-attachments/assets/06dc30a8-03d1-4cb2-a384-49c734fb1098)


[paper](https://arxiv.org/pdf/2405.17220), [code](https://github.com/RLHF-V/RLAIF-V)

## TL;DR
- **I read this because.. :** RLHF-V Successor
- **task :** vision-RLHF 
- **problem :** human annotated preference data is not scalable
- Idea :** Get evaluated by peer LVLMs. Let's divide the reward into logical units and turn it into a binary question and score it as correct or incorrect.
- **input/output :** {image, question} -> answer
- **architecture :** LLaVA 1.5, OmniLMM
- **objective :** DPO loss
- **baseline :** VCD, Less-is-more, LURE, QEWEn-VL, LLaVA-NeXT, Minigemini, HA-DPO, POVID, LLaVA-RLHF, Silikie, RLHF-V
- **data :** image - instruction from {MSCOCO, ShareGPT-4V, MovieNet, GoogleLandmark v2, VQA v2, OKVQA, TextVQA} => DPO data
- **evaluation :** trustworthiness(Object Halbench, MMHal-Bench, MHumanEval, AMBER), helpfulness(LLaVA Bench, MMStar) 
- **result :** Performance beyond GPT-4V in trustworthiness.
- **contribution :** Quickly glue RLAIF to VLM!
- **etc. :** iterative alignment, etc. ... seems like a lot of work

## Details
### performance 
![image](https://github.com/user-attachments/assets/0cb4887c-7a8e-463f-b01c-2cbd9ffc99b1)

### RLAIF-V
![image](https://github.com/user-attachments/assets/25cf0fbf-269e-4236-bbdc-beedb8de141e)

1) response generation 
Using a different seed to generate n answers for the targeted model

2) response evaluation
- divide
Because the answer is long and contains multiple statements, we break it into atomic statements.

- conquer
Turn each claim into a binary question to measure its trustworthiness (the unconditional answer is yes).
It then asks the labeler model a question and scores the answer.

- combine
Find the final score S as $-n_{rej}$ when $n_{rej}$ answers to the claim are marked with more answers
It then finds the two answer pairs with the difference in score and samples up to two pairs per instruction.
At this point, filtering process, etc. made no sense.

3) iterative alignment
If you simply apply DPO, there is a "distribution shift problem" where the model output distribution changes during the training process. (Citation for this is Scaling Laws for Reward Model Overoptimization)
To address this, we propose an iterative alignment that iterates through Training -> DPO data collection -> Training
![image](https://github.com/user-attachments/assets/cbd2733a-cacf-4917-9b72-de290992c5b7)

Generate with the most recent instruction model $M_i$ and use the divide-and-conquer strategy above to create pairs, learn them, and repeat

### Experiment 
- hparams
  - base models
- LLaVA 1.5 as the instruction model -- the corresponding labeler model is LLaVA-NeXT (Nous-Hermes-2-Yi-34B)
- OmniLMM -- The corresponding Labeler model is the same Labeler model (no-RLHF)
  - 4 epochs, lr 5e-7, beta 0.1, bs 8
  - 4 iterations (4K instrctions)
- 8 I'm learning 7B /12B with A100 and I'm having trouble with
    - data collection 48h / 50h 
- training takes 6h / 8h

### Result
![image](https://github.com/user-attachments/assets/f3f4c3e0-9fec-473a-aa07-09fc9e20d06c)

### analysis
#### deconfounded strategy
Ablation of scoring with divide-and-conquer strategies
![image](https://github.com/user-attachments/assets/9e32cf0e-4b95-41af-8594-223995d99aaf)

- RLHF-V trained with fine-grained human feedback
- adapted is the preferred response replaced with human annotation

ours came out the best.
The rlhf-v data is a fine-grained correction of Muffin inference results, while adapted is rewritten by humans, so the performance difference is quite large.
I wondered, is it really that important to use your own inference results when doing DPO?

- Self rewarding vs divide-and-conquer
Self-rewarding simply asks the labeler to give a long prompt and score the response.
![image](https://github.com/user-attachments/assets/0c4b7715-2727-44bd-a4eb-124157201a0f)

Your suggestion definitely worked.

- iterative alignment 
![image](https://github.com/user-attachments/assets/2bdc3a10-0663-4b00-899b-c45e67a97b4b)

The performance of the non-iterative alignment method seemed to saturate quickly.


- data source // multiple lvlm
Performance was consistently better when written with other data
![image](https://github.com/user-attachments/assets/957c5953-c845-42fa-92c8-0c0ec9758255)
 
It worked well with a variety of Lvlms, with OmniLMM performing the best.
