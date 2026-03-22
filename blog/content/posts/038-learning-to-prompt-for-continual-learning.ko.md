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
옛날 데이터들을 1% 정도 , external memory로 저장해서
Pseudo Rehearsal : 과거 샘플들을 generate
https://ffighting.tistory.com/entry/iCaRL-%ED%95%B5%EC%8B%AC-%EB%A6%AC%EB%B7%B0

**Regularization-based methods**
파라미터가 너무 바뀌지 않도록 제약을 줌

**Parameter isolation**
각 class seg 별로 모델을 학습하고 그 파라미터들을 어떻게 합칠지 나중에 고민

## TL;DR
- **task :** class incremental learning / domain incremental learning / task-agnostic learning
- **problem :** catastrophic forgetting. 
- **idea :** prompt learning ! 이미지가 주어졌을 때 전체 M개의 prompt pool 중에 N개의 가까운 prompt를 뽑고(Learning to Prompt, L2P), ViT 비전 토큰 앞에 prepend해서 이미지 분류. 
- **architecture :** ViT-B/16
- **objective :** CrossEntropyLoss + diversifying prompt-selection.  
- **baseline :** CIL variants(finetuning sequentially, BiC, EWC, DER++..)
- **data :** split CIFAR100, 5-datasets
- **result :** SOTA. 그냥 iid finetuning보단 낮음. 
- **contribution :** 간단한 아이디어/아키텍쳐로 SOTA. 

## ETC.
- [continual learning papers](
https://ffighting.tistory.com/entry/Incremental-Continual-learning-%EC%84%A4%EB%AA%85-%EC%84%B1%EB%8A%A5%EC%B8%A1%EC%A0%95%EB%B0%A9%EC%8B%9D-%EC%97%B0%EA%B5%AC%ED%9D%90%EB%A6%84#Dynamic%20structure%20%EB%B0%A9%EC%8B%9D) 