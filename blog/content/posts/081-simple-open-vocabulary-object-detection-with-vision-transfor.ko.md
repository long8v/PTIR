---
title: "[73] Simple Open-Vocabulary Object Detection with Vision Transformers"
date: 2022-11-03
tags: ['google', 'object detection', '2022Q2', '25min', 'ECCV', 'OV']
paper: "https://arxiv.org/abs/2205.06230"
issue: 81
issueUrl: "https://github.com/long8v/PTIR/issues/81"
---
![image](https://user-images.githubusercontent.com/46675408/199692356-2662b5d1-51f0-4468-8df0-a4e40edc99fe.png)

[paper](https://arxiv.org/abs/2205.06230)

## TL;DR
- **task :** open vocab object detection
- **problem :** novel한 class에 대한 od annotation이 없음
- **idea :** CLIP 임베딩을 사용하자
- **architecture :** CLIP을 사용하여 class를 text embedding으로 만들어주고 ViT의 토큰들을 query로 삼아서 bipartite matching을 한 뒤 DETR loss를 주어서 학습. 
- **objective :** DETR loss but sigmoid focal loss for class label
- **baseline :** ViLD, GLIP 
- **data :** OI, VG, Object 365 -> LVIS(long-tail)
- **result :** GLIP 보다 좋아보임
- **contribution :** 아주 간단한 아키텍쳐로 Open vocab OD를 풀었다
- **limitation or 이해 안되는 부분 :** GLIP이 Open vocab용으로 만들어진게 아닐듯?

## Details
### Architecture
![image](https://user-images.githubusercontent.com/46675408/199862460-f5157dd3-8883-4d32-ad9f-fb84ea9491a3.png)

### training details
- 처음에 각 이미지 토큰에서 한 bbox Prediction의 x, y가 해당 이미지 토큰 좌표 안에 있도록 초기화하니 성능이 더 빠르게 수렴
- 다양한 augmentation / cleaning 적용

### zero-shot performance
![image](https://user-images.githubusercontent.com/46675408/199862435-79c06c1a-72ae-44b6-a47a-f53442052be9.png)

### one-shot image-conditioned result
![image](https://user-images.githubusercontent.com/46675408/199862130-5725c07e-f6c5-456e-8c21-c4e8362791cf.png)

### one-/few-shot performance
![image](https://user-images.githubusercontent.com/46675408/199862334-ec207fad-3799-4532-a7de-7768ceb5a747.png)
