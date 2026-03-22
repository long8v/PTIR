---
title: "[177] Fine-grained Image Captioning with CLIP Reward"
date: 2024-09-06
tags: ['2022Q2', '25min', 'RL', 'NAACL']
paper: "https://arxiv.org/abs/2205.13115"
issue: 196
issueUrl: "https://github.com/long8v/PTIR/issues/196"
---

<img width="1054" alt="image" src="https://github.com/user-attachments/assets/76f80648-0e4d-460c-9e99-ab26816d9295">

[paper](https://arxiv.org/abs/2205.13115), [code](https://github.com/j-min/CLIP-Caption-Reward)

## TL;DR
- **I read this because.. :** CLIP reward
- **task :** captioning with reward 
- **problem :** 기존의 metric(cider, ..)들은 가장 salient한 object에 대해 annotate 되어있는 캡션을 기반으로 하므로 finegrained한 정보를 담지 못한다
- **idea :** CLIP-Score를 reward로 사용하자
- **input/output :** image -> caption 
- **architecture :** CLIP-Res50 + encoder-decoder transformer(6 layer)
- **objective :** REINFORCE objective with CLIP-S
- **baseline :** MLE, CIDEr, CLIP-S, CIDEr-CLIP-S, CLIP-S + Grammar
- **data :** MS COCO  karpathy split 
- **evaluation :** Text-Based(BLEU, CIDEr, METOR, ROUGE-L, BERT-S), Image Based(CLIP-S, RefCLIP-S), T2I retrieval, FineCapEval(proposed), human eval
- **result :** text based보단 당연히 안좋지만 Image eval에 대해서는 우세한 성적. 특히 background 등 세밀한 부분에 대한 벤치마크인 FineCapEval에서 MLE, CIDEr based보다 좋은 성적 
- **contribution :** motivation -- 실험 -- 평가가 잘 이어짐
- **etc. :** LM을 agent로 보는게 옛날부터 있었구나,, 옛날 논문도 좀 읽자,,

## Details
<img width="522" alt="image" src="https://github.com/user-attachments/assets/279db3e0-51d0-4b3e-8051-f29b0059f4d2">

### Preliminary
teacher-forcing 이 아니라 captioning model을 일종의 agent로 보는 것의 원류는 이 논문
Sequence Level Training with Recurrent Neural Networks(ICLR'16, https://arxiv.org/pdf/1511.06732)
<img width="875" alt="image" src="https://github.com/user-attachments/assets/1d5c2e58-c917-482e-81d9-c819f7c202cb">

REINFORCE 알고리즘으로 BLEU, ROUGE-L 를 reward로 하는 captioning model
reward가 variance가 너무 커서 베이스라인을 빼는건 아래 논문 
Self-critical Sequence Training for Image Captioning(CVPR'16 https://arxiv.org/pdf/1612.00563)
<img width="526" alt="image" src="https://github.com/user-attachments/assets/088da421-4b2c-4108-81dc-786e59429aaa">

위는 REINFORCE with baseline에 대한 일반적인 수식이고 $r(w^s)$는 샘플링 decoding, b는 greedy decode한 sequence의 reward를 사용함 

### proposed

<img width="506" alt="image" src="https://github.com/user-attachments/assets/99d71330-8ff5-4a8b-a7a9-7e762662da7e">


<img width="474" alt="image" src="https://github.com/user-attachments/assets/0a2513a5-30ea-42ff-b057-d41d839f9e69">

<img width="500" alt="image" src="https://github.com/user-attachments/assets/e22be4ec-7582-48b8-b495-8087dbfee7f3">

- $R(I,c)=CLIP-S(I,c)$

근데 이렇게 할경우 CLIP text encoder가 문법에 대해서는 약해서 문법이 틀린 캡션을 생성하는 경우가 있었음.
그래서 일부러 문법을 틀리게한 문장을 임의로 만들어서 문법이 맞는지 안맞는지에 대해 head로 붙여 binary로 예측하게 함. 그리고 생성된 캡션의 grammar 점수도 Reward에 추가함 

<img width="475" alt="image" src="https://github.com/user-attachments/assets/2d72fdbd-792a-403d-9660-3ea206eb7fc0">

MLE로 15에폭 먼저 학습하고 25 에폭은 각각의 Reward로 학습 

### Result 

<img width="1015" alt="image" src="https://github.com/user-attachments/assets/35fc3a6a-a69b-41f4-be3c-dfe42b942921">

proposed FineCapEval

<img width="1002" alt="image" src="https://github.com/user-attachments/assets/ff35ce3e-d6da-431f-8c5c-a4adec23598f">

Human evaluation result 
<img width="987" alt="image" src="https://github.com/user-attachments/assets/bfa3fa4c-d0ff-4264-954f-3c43ec4be196">

