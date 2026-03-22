---
title: "[105] LoRA: Low-Rank Adaptation of Large Language Models"
date: 2023-03-27
tags: ['2021Q2', 'microsoft', 'finetuning', 'LLM']
paper: "https://arxiv.org/abs/2106.09685"
issue: 114
issueUrl: "https://github.com/long8v/PTIR/issues/114"
---
<img width="958" alt="image" src="https://user-images.githubusercontent.com/46675408/227829215-d7e166ae-4cbe-45b6-8af5-1291767849a4.png">

[paper](https://arxiv.org/abs/2106.09685)

## TL;DR
- **I read this because.. :** #113 에 이어서 efficient finetuning 시리즈 물
- **task :** LLM finetuning 
- **problem :** finetuning은 비효율적. adaptor는 어쨌든 레이어가 중간에 추가되기 때문에 latency에 영향.
- **idea :** weight의 업데이트 분을 low-rank 로 근사하여 원래 파라미터에 더하자!
- **architecture :** RoBERTa, DeBERTa, GPT-2, GPT-3
- **objective :** ce loss
- **baseline :** finetuning / adaptors / pre-layer  
- **data :** GLUE, WikiSQL, MultiNLI
- **result :** 훨씬 더 작은 trainable parameter로 더 나은 성능
- **contribution :** latency 추가 없이 효율적인 finetuning 
- **limitation / things I cannot understand :**

## Details

- preliminaries : Parameter-Efficient Transfer Learning for NLP
Adaptor를 제안. finetuning은 모든 파라미터를 학습하고 저장해야되어서 비효율적. feature-extraction은 성능의 한계.
downstream task들을 더 적은 파라미터로 학습하는 adaptor 제안. 
이 논문에서는 트랜스포머 레이어에 두개의 adaptor layer를 넣음.
<img width="861" alt="image" src="https://user-images.githubusercontent.com/46675408/227829077-737a0977-55e3-4b0b-8335-e3760f46d8b6.png">

<img width="878" alt="image" src="https://user-images.githubusercontent.com/46675408/227842635-404cb7ce-22a1-42f5-84aa-44295cb74555.png">


- architecture
<img width="271" alt="image" src="https://user-images.githubusercontent.com/46675408/227840115-13cc5668-26d4-4449-86f1-15707423ba8b.png">

기본적인 아이디어는 dense한 layer가 더 낮은 rank로 decompose될 수 있다는 아이디어.
어떤 weight W의 update 분인 $\Delta W$를 $BA$ $B\in\mathbb{R}^{d \times r}$, $A\in\mathbb{R}^{r \times k}$로 근사해서 forward를 아래와 같이 만듦
 
<img width="350" alt="image" src="https://user-images.githubusercontent.com/46675408/227841176-8514c5d8-a637-4289-8a5f-0603fc532cb2.png">

이때 A는 random gaussian으로 B는 zero로 initialize됨. 즉 초기 BA는 0이 됨.
$\Delta W$는 $\alpha / \gamma$로 업데이트 되는데 $\alpha$가 일종의 learning rate처럼 하이퍼파라미터처럼 사용함.
LoRA를 attention을 위한 weight들인 $W_q$, $W_k$, $W_v$, $W_o$에만 적용하고 MLP에는 적용하지 않음.

<img width="889" alt="image" src="https://user-images.githubusercontent.com/46675408/227841827-54a384d6-25d8-4799-a4d7-3230f2a9bb3e.png">

제한된 파라미터 제약 안에서 $W_q$만 적용하는 것보다 rank 4더라도 둘다 적용하는게 좋았고 셋다 적용하는게 가장 좋았음. 
<img width="889" alt="image" src="https://user-images.githubusercontent.com/46675408/227842059-0e225cce-709f-4317-bf8f-6202c127ab4b.png">

매우 낮은 rank에서도 잘 작동했고 이는 update matrix $\Delta W$ 가 매우 낮은 intrinsic matrix를 가지고 있다는 뜻임.

- inference latency
<img width="580" alt="image" src="https://user-images.githubusercontent.com/46675408/227842685-f4736e5c-3c60-41d0-b432-f28e0d19f1ff.png">

- results
<img width="573" alt="image" src="https://user-images.githubusercontent.com/46675408/227842730-d3bc6df9-1de7-4919-b5bd-32f13e278e8d.png">

<img width="556" alt="image" src="https://user-images.githubusercontent.com/46675408/227842856-c07b5f37-95de-49ba-adea-31c149afacde.png">

<img width="577" alt="image" src="https://user-images.githubusercontent.com/46675408/227842866-0e33df61-da25-42ae-83cb-de9d33c3c5c5.png">

