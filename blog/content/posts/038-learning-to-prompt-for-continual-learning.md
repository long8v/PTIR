---
title: "[33] Learning to Prompt for Continual Learning"
date: 2022-07-13
tags: ['2021Q4', 'google', 'CVPR', 'continual learning']
paper: "https://arxiv.org/pdf/2112.08654.pdf"
issue: 38
issueUrl: "https://github.com/long8v/PTIR/issues/38"
---
<img width="1407" alt="image" src="https://user-images.githubusercontent.com/46675408/178699787-23cc2115-59a8-47eb-953b-19ae51eaeffb.png">

[paper](https://arxiv.org/pdf/2112.08654.pdf), [blog](https://ai.googleblog.com/2022/04/learning-to-prompt-for-continual.html)

## Details
### Preliminaries 
- Continual Learning
https://engineering-ladder.tistory.com/94
- Taxonomy of Continual Learning 
![image](https://user-images.githubusercontent.com/46675408/178900418-47cca380-821e-4876-b23f-4e4cca501392.png)


**Replay methods**
Save about 1% of the old data to external memory and use the
Pseudo Rehearsal: generate historical samples
https://ffighting.tistory.com/entry/iCaRL-%ED%95%B5%EC%8B%AC-%EB%A6%AC%EB%B7%B0

**Regularization-based methods**
Constrain parameters so they don't change too much

**Parameter isolation**
Train a model for each class seg and think about how to combine its parameters later

## TL;DR
- **task :** class incremental learning / domain incremental learning / task-agnostic learning
- **problem :** catastrophic forgetting. 
- **idea :** prompt learning ! Given an image, pick N close prompts out of a pool of M prompts (Learning to Prompt, L2P) and prepend them in front of a ViT vision token to classify the image.
- **architecture :** ViT-B/16
- **objective :** CrossEntropyLoss + diversifying prompt-selection.  
- **baseline :** CIL variants(finetuning sequentially, BiC, EWC, DER++..)
- **data :** split CIFAR100, 5-datasets
- **result :** SOTA. just lower than iid finetuning.
- **contribution :** Contribute to SOTA with a simple idea/architecture.

## ETC.
- [continual learning papers](
https://ffighting.tistory.com/entry/Incremental-Continual-learning-%EC%84%A4%EB%AA%85-%EC%84%B1%EB%8A%A5%EC%B8%A1%EC%A0%95%EB%B0%A9%EC%8B%9D-%EC%97%B0%EA%B5%AC%ED%9D%90%EB%A6%84#Dynamic%20structure%20%EB%B0%A9%EC%8B%9D) 