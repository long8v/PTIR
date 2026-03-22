---
title: "LoRA: Low-Rank Adaptation of Large Language Models"
date: 2023-03-27
tags: ['2021Q2', 'microsoft', 'finetuning', 'LLM']
paper: "https://arxiv.org/abs/2106.09685"
issue: 114
issueUrl: "https://github.com/long8v/PTIR/issues/114"
summary: "Continued from #113 in the efficient finetuning series - Efficient finetuning without adding latency"
---
<img width="958" alt="image" src="https://user-images.githubusercontent.com/46675408/227829215-d7e166ae-4cbe-45b6-8af5-1291767849a4.png">

[paper](https://arxiv.org/abs/2106.09685)

## TL;DR
- **I read this because.. :** #113 Continuing the efficient finetuning series water
- **task :** LLM finetuning 
- **problem :** finetuning is inefficient. adaptor affects latency because the layer is added in the middle anyway.
- **idea :** approximate the updated minute of weight with low-rank and add it to the original parameter!
- **architecture :** RoBERTa, DeBERTa, GPT-2, GPT-3
- **objective :** ce loss
- **baseline :** finetuning / adaptors / pre-layer  
- **data :** GLUE, WikiSQL, MultiNLI
- **result :** better performance with a much smaller trainable parameter
- **contribution :** Efficient finetuning without adding latency
- **limitation / things I cannot understand :**

## Details

- preliminaries : Parameter-Efficient Transfer Learning for NLP
Adaptor suggestions. Finetuning is inefficient because all parameters need to be learned and stored. feature-extraction has performance limitations.
Suggest adaptors that learn downstream tasks with fewer parameters.
In this paper, we put two adaptor layers in the transformer layer.
<img width="861" alt="image" src="https://user-images.githubusercontent.com/46675408/227829077-737a0977-55e3-4b0b-8335-e3760f46d8b6.png">

<img width="878" alt="image" src="https://user-images.githubusercontent.com/46675408/227842635-404cb7ce-22a1-42f5-84aa-44295cb74555.png">


- architecture
<img width="271" alt="image" src="https://user-images.githubusercontent.com/46675408/227840115-13cc5668-26d4-4449-86f1-15707423ba8b.png">

The basic idea is that dense layers can be decomposed into lower ranks.
For any weight W, approximate $\Delta W$, the update fraction, by $BA$ $B\in\mathbb{R}^{d \times r}$, $A\in\mathbb{R}^{r \times k}$, to create a forward as follows
 
<img width="350" alt="image" src="https://user-images.githubusercontent.com/46675408/227841176-8514c5d8-a637-4289-8a5f-0603fc532cb2.png">

where A is random gaussian and B is initialized to zero, i.e., the initial BA is zero.
Delta W$ is updated with $\alpha / \gamma$, where $\alpha$ is used as a hyperparameter, like some sort of learning rate.
Apply LoRA only to the attention weights $W_q$, $W_k$, $W_v$, $W_o$, and not to MLP.

<img width="889" alt="image" src="https://user-images.githubusercontent.com/46675408/227841827-54a384d6-25d8-4799-a4d7-3230f2a9bb3e.png">

Within the limited parameter constraints, it was better to apply both $W_q$ than just $W_q$, even for rank 4, and best to apply all three.
<img width="889" alt="image" src="https://user-images.githubusercontent.com/46675408/227842059-0e225cce-709f-4317-bf8f-6202c127ab4b.png">

It worked well at very low ranks, which means that the update matrix $\Delta W$ has a very low intrinsic matrix.

- inference latency
<img width="580" alt="image" src="https://user-images.githubusercontent.com/46675408/227842685-f4736e5c-3c60-41d0-b432-f28e0d19f1ff.png">

- results
<img width="573" alt="image" src="https://user-images.githubusercontent.com/46675408/227842730-d3bc6df9-1de7-4919-b5bd-32f13e278e8d.png">

<img width="556" alt="image" src="https://user-images.githubusercontent.com/46675408/227842856-c07b5f37-95de-49ba-adea-31c149afacde.png">

<img width="577" alt="image" src="https://user-images.githubusercontent.com/46675408/227842866-0e33df61-da25-42ae-83cb-de9d33c3c5c5.png">

