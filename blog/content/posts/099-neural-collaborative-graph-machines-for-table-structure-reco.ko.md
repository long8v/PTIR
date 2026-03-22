---
title: "[90] Neural Collaborative Graph Machines for Table Structure Recognition"
date: 2022-12-22
tags: ['2021Q4', 'CVPR', 'graph', 'document']
paper: "https://arxiv.org/abs/2111.13359"
issue: 99
issueUrl: "https://github.com/long8v/PTIR/issues/99"
---
<img width="674" alt="image" src="https://user-images.githubusercontent.com/46675408/209046093-50aac421-d0fb-4fc8-a301-13574c1b8242.png">

[paper](https://arxiv.org/abs/2111.13359)

## TL;DR
- **I read this because.. :** table 관련 연구. sgg에서 쓸만한 아이디어 없을까하고 겸사겸사 읽음.
- **task :** Table Structure Recognition(TSR)
- **problem :** 테이블 표현을 위해는 3가지 modality(좌표, 이미지, 내용)가 있음. 보통 좌표가 가장 중요한 feature이나 이미지가 왜곡되어 있으면 좌표보다는 다른 modality를 활용해야 함. 이렇게 modality간의 서로 도와주도록 잘 학습하려면? 
- **idea :** early fusion도 아니고 late fusion도 아닌.. 각각 하고 다시 합치고 이걸 여러 블락으로 반복하는 아키텍쳐.
- **architecture :** 이미지 내 bbox가 node, 모든 연결을 edge로. 각 modality에 대해서 Q는 feature, K=V는 edge representation으로 하는 MHA로 feature 뽑고(Ego Context Extractor) 각 modality를 쿼리로 하고 다른 modality를 K,V로 쓰는 3개의 Cross Context Synthesizer를 다음에 붙임. 
- **objective :** 모든 node i, j에 대한 edge가 있고 이게 row, column, cell로 연결되어있는지 각각의 bce
- **baseline :** FLAG-Net, TabStr, DGCNN
- **data :** ICDAR-2013, ICDAR-2019, WTW, UNLV, SciTSR, SciTSR-COMP
- **evaluation :** Tree Edit Distance(TED), BLEU
- **result :** sota

## Details
### Motivation 
<img width="495" alt="image" src="https://user-images.githubusercontent.com/46675408/209047141-31befe01-6d06-4cd7-a153-4f743dae3818.png">

### Architecture
<img width="952" alt="image" src="https://user-images.githubusercontent.com/46675408/209047167-0df96a38-ac1a-4f1d-aa44-f36a777e1782.png">

<img width="542" alt="image" src="https://user-images.githubusercontent.com/46675408/209048074-f28842e2-c0d3-4f73-b6a9-22376624a620.png">
MHA 연산이 너무 복잡하니 [Pyramid ViT](https://arxiv.org/abs/2102.12122)에서 나왔던 Compressed MHA(CMHA) 사용

### Result
<img width="296" alt="image" src="https://user-images.githubusercontent.com/46675408/209047685-d4dfc678-1fdb-4769-8f40-4ddf2989eaa0.png">

<img width="561" alt="image" src="https://user-images.githubusercontent.com/46675408/209047708-e4ba58ec-2237-42ce-a9e1-5236f63241fb.png">

