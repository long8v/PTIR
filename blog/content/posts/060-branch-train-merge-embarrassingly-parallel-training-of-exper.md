---
title: "Branch-Train-Merge: Embarrassingly Parallel Training of Expert Language Models"
date: 2022-08-25
tags: ['LM', 'MoE', '2022Q3', '25min']
paper: "https://arxiv.org/pdf/2208.03306.pdf"
issue: 60
issueUrl: "https://github.com/long8v/PTIR/issues/60"
---
![image](https://user-images.githubusercontent.com/46675408/186548736-7d4ffaae-1079-4434-aa4d-677fd8e24fec.png)

[paper](https://arxiv.org/pdf/2208.03306.pdf)

## TL;DR
- **task :** large language modeling, domain incremental learning
- **problem :** The idea is pretty much the same as DeMix, but I want to reduce the communication in the multi-node synchronize part.
- Idea :** Create expert LMs that do not share parameters by domain (previous MoE LMs shared only FFN) and learn using Branch-Train-Merge (BTM). The main idea of BTM is that when a new domain is introduced, the closest LMs are found, averaged, initialized, branched, trained, and added to the branch forest. When inferring, the posterior is estimated using Bayes rule to determine which domain it is, and the final prediction is a weighted sum.
- **architecture :** vanilla Transformer..
- **objective :** cross-entropy loss 
- **baseline :** Transformer LM(GPT), DeMix 
- **data :** Wikipedia, C4, StackOverflow, JavaScript, ... etc.
- **result :** Better perplexity on out-of-domain, similar performance to Transformer LM with 2.5x the size when incrementally learning on 64 domains.
- **contribution :** MoE without shared parameters.
- **Limitations or things I don't understand :**

## Details
### Batch-Train-Merge(BTM)
<img width="903" alt="image" src="https://user-images.githubusercontent.com/46675408/186549445-80d57367-7aaf-4b5a-9e26-90b1334b775b.png">

<img width="931" alt="image" src="https://user-images.githubusercontent.com/46675408/186549806-04ea8c1b-6d91-48ab-aeb5-d48d52e94203.png">


### Inference
<img width="884" alt="image" src="https://user-images.githubusercontent.com/46675408/186549699-f60d1461-a0cc-48a8-9447-f4b1e8d01bee.png">

It is correct that we should forward to all ELMs, but we can see that the ELMs selected are sparsely configured.

### Data..
<img width="888" alt="image" src="https://user-images.githubusercontent.com/46675408/186549911-a17d4fae-dd98-49a7-ab67-8624f759b644.png">

### DeMix
DeMix, 2021
- https://arxiv.org/pdf/2108.05036.pdf
![image](https://user-images.githubusercontent.com/46675408/186549102-b8c3e57a-d286-4c64-b90c-000f937d6791.png)
- problem : We want to reduce the perplexity of training a corpus of multiple domains with a single LM, where we know the domain of each piece of data.
- solution : Train an FFN (like switch Transformer) as an expert for each domain in the corpus. When a new domain is added at inference time,
You can either 1) forward all FFNs and do a bezier-weighted sum to get the result, or 2) add FFNs for that domain.
- Result: improved LM perplexity while increasing learning efficiency, showing that new domains can be added or removed without forgetting previous experts.

