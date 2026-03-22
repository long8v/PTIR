---
title: "[30] CoCa: Contrastive Captioners are Image-Text Foundation Models"
date: 2022-06-22
tags: ['multimodal', 'backbone', 'google', '2022Q2']
paper: "https://arxiv.org/pdf/2205.01917.pdf"
issue: 35
issueUrl: "https://github.com/long8v/PTIR/issues/35"
---

<img width="569" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d6619610-f504-44de-9f19-4edf14d63dd4">

[paper](https://arxiv.org/pdf/2205.01917.pdf)

## TL;DR
**problem :** 좋은 vision backbone 만들기. 분류 레이블에 대한 이미지 프리트레이닝, 이미지-텍스트 pair를 받아 contrastive loss로 학습되는 dual-encoder model, image 인코더가 있고 text decoder가 cross-attention으로 이미지 피쳐를 받아 classification, VQA등을 하는 encoder-decoder model 세개를 통합하여 scratch 부터 학습할 수 있는 모델을 만들고 싶다.  
**solution :** 이미지 텍스트 페어가 주어졌을 때, 이미지 인코더 텍스트 디코더 따로 인풋을 받고 이미지 인코더에서 나온 마지막 토큰과 텍스트 디코더의 cls-token으로 contrastive loss, 텍스트 디코더 위에 이미지 인풋과 크로스 어텐션이 있는 multi-model text decoder를 쌓은 뒤 captioning loss. 두 loss의 합으로 프리트레이닝
**result :** 다양한 task 에서 SOTA
<img width="695" alt="image" src="https://user-images.githubusercontent.com/46675408/174938121-bafee08b-8737-4fba-8283-7e97ee94e1d0.png">



## Details
- **Architecture**
<img width="1005" alt="image" src="https://user-images.githubusercontent.com/46675408/174954322-7af62fef-0524-4892-94d1-50331d76977e.png">

- **loss**

captioning loss
![image](https://user-images.githubusercontent.com/46675408/175834167-8856741f-5aab-49cc-8a18-05bfde05d5ce.png)

dual encoder contrastive loss
![image](https://user-images.githubusercontent.com/46675408/175834151-b1fe8137-5010-40f6-bab4-c85eacb2617b.png)
 

- **Attentional Poolers** : contrastive loss를 계산할 때, 이미지에서 하나의 토큰만을 사용하지만 인코더-디코더의 캡셔닝 태스크를 할때는 전체 이미지 토큰 시퀀스를 사용한다. 이는 예비실험에서 visual recognition task를 할 때에는 하나의 pooled image가 더 성능이 좋았고, 멀티모달을 할 때에는 region-level feature를 참고하면 좋아서 더 많은 토큰을 보는 것이 유리했기 때문이다. 이 때문에 task-specific attentional pooling을 사용하여 downstream task마다 다른 visual representation을 할 수 있게 했다. pooler는 n개의 learnable query를 가진 single multi-head attention 레이어이다. (이때 key와 value는 encoder output) 이를 통해 두개의 다른 loss에 대해, 다른 길이의 쿼리를 갖게 학습될 수 있다. 자연스럽게 이 learnable query는 task adaptor 역할도 하게 된다. 
