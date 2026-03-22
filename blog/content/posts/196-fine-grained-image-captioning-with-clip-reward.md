---
title: "[177] Fine-grained Image Captioning with CLIP Reward"
date: 2024-09-06
tags: ['2022Q2', '25min', 'RL', 'NAACL']
paper: "https://arxiv.org/abs/2205.13115"
issue: 196
issueUrl: "https://github.com/long8v/PTIR/issues/196"
summary: "CLIP reward - motivation -- experimentation -- evaluation goes well together"
---

<img width="1054" alt="image" src="https://github.com/user-attachments/assets/76f80648-0e4d-460c-9e99-ab26816d9295">

[paper](https://arxiv.org/abs/2205.13115), [code](https://github.com/j-min/CLIP-Caption-Reward)

## TL;DR
- **I read this because.. :** CLIP reward
- **task :** captioning with reward 
- **problem :** Existing metrics (cider, ..) are based on captions that are annotated for the most salient objects, so they don't capture fine-grained information.
- Idea :** Use CLIP-Score as a reward
- **input/output :** image -> caption 
- **architecture :** CLIP-Res50 + encoder-decoder transformer(6 layer)
- **objective :** REINFORCE objective with CLIP-S
- **baseline :** MLE, CIDEr, CLIP-S, CIDEr-CLIP-S, CLIP-S + Grammar
- **data :** MS COCO  karpathy split 
- **evaluation :** Text-Based(BLEU, CIDEr, METOR, ROUGE-L, BERT-S), Image Based(CLIP-S, RefCLIP-S), T2I retrieval, FineCapEval(proposed), human eval
- **result :** Naturally worse than text based, but dominant performance on Image eval. Better than MLE and CIDEr based, especially on FineCapEval, a benchmark for fine details such as background.
- **contribution :** motivation -- experimentation -- good at evaluation
- **etc. :** LM as an agent has been around for a long time,, let's read some old papers,,

## Details
<img width="522" alt="image" src="https://github.com/user-attachments/assets/279db3e0-51d0-4b3e-8051-f29b0059f4d2">

### Preliminary
The idea of viewing the captioning model as a kind of agent rather than teacher-forcing originated in this paper
Sequence Level Training with Recurrent Neural Networks(ICLR'16, https://arxiv.org/pdf/1511.06732)
<img width="875" alt="image" src="https://github.com/user-attachments/assets/1d5c2e58-c917-482e-81d9-c819f7c202cb">

Captioning model using REINFORCE algorithm with BLEU, ROUGE-L as rewards
Subtracting the baseline because the reward has too much variance is described in the paper
Self-critical Sequence Training for Image Captioning(CVPR'16 https://arxiv.org/pdf/1612.00563)
<img width="526" alt="image" src="https://github.com/user-attachments/assets/088da421-4b2c-4108-81dc-786e59429aaa">

Above is the general formula for REINFORCE with baseline, with $r(w^s)$ as the sampling decoding and b as the reward of the greedy decoded sequence

### proposed

<img width="506" alt="image" src="https://github.com/user-attachments/assets/99d71330-8ff5-4a8b-a7a9-7e762662da7e">


<img width="474" alt="image" src="https://github.com/user-attachments/assets/0a2513a5-30ea-42ff-b057-d41d839f9e69">

<img width="500" alt="image" src="https://github.com/user-attachments/assets/e22be4ec-7582-48b8-b495-8087dbfee7f3">

- $R(I,c)=CLIP-S(I,c)$

However, the CLIP text encoder is not very good at grammar and sometimes generates ungrammatical captions.
So, we randomly generate a sentence that is intentionally ungrammatical and put it as a head to make a binary prediction about whether it is grammatical or not. We also added the grammar score of the generated caption to the reward

<img width="475" alt="image" src="https://github.com/user-attachments/assets/2d72fdbd-792a-403d-9660-3ea206eb7fc0">

Learn 15 epochs with MLE first, then 25 epochs with each reward

### Result 

<img width="1015" alt="image" src="https://github.com/user-attachments/assets/35fc3a6a-a69b-41f4-be3c-dfe42b942921">

proposed FineCapEval

<img width="1002" alt="image" src="https://github.com/user-attachments/assets/ff35ce3e-d6da-431f-8c5c-a4adec23598f">

Human evaluation result 
<img width="987" alt="image" src="https://github.com/user-attachments/assets/bfa3fa4c-d0ff-4264-954f-3c43ec4be196">

