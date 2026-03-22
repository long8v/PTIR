---
title: "Simple Open-Vocabulary Object Detection with Vision Transformers"
date: 2022-11-03
tags: ['google', 'object detection', '2022Q2', '25min', 'ECCV', 'OV']
paper: "https://arxiv.org/abs/2205.06230"
issue: 81
issueUrl: "https://github.com/long8v/PTIR/issues/81"
summary: "Solving Open vocab OD with a very simple architecture"
---
![image](https://user-images.githubusercontent.com/46675408/199692356-2662b5d1-51f0-4468-8df0-a4e40edc99fe.png)

[paper](https://arxiv.org/abs/2205.06230)

## TL;DR
- **task :** open vocab object detection
- **problem :** no od annotation for novel class
- **idea :** Use CLIP embedding
- **architecture :** CLIP is used to make the class as text embedding, and the tokens of ViT as query, bipartite matching, and DETR loss are used to learn.
- **objective :** DETR loss but sigmoid focal loss for class label
- **baseline :** ViLD, GLIP 
- **data :** OI, VG, Object 365 -> LVIS(long-tail)
- **result :** looks better than GLIP
- **contribution :** Solved Open vocab OD with very simple architecture
- **limitation or something I don't understand :** GLIP is not made for Open vocab?

## Details
### Architecture
![image](https://user-images.githubusercontent.com/46675408/199862460-f5157dd3-8883-4d32-ad9f-fb84ea9491a3.png)

### training details
- Initializing one bbox Prediction on each image token so that its x, y are within the coordinates of that image token initially converges faster
- Apply various augmentation / cleaning

### zero-shot performance
![image](https://user-images.githubusercontent.com/46675408/199862435-79c06c1a-72ae-44b6-a47a-f53442052be9.png)

### one-shot image-conditioned result
![image](https://user-images.githubusercontent.com/46675408/199862130-5725c07e-f6c5-456e-8c21-c4e8362791cf.png)

### one-/few-shot performance
![image](https://user-images.githubusercontent.com/46675408/199862334-ec207fad-3799-4532-a7de-7768ceb5a747.png)
