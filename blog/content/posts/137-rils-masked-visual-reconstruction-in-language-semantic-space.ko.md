---
title: "[125] RILS: Masked Visual Reconstruction in Language Semantic Space"
date: 2023-08-02
tags: ['CVPR', 'CLIP', '2023Q1']
paper: "https://arxiv.org/pdf/2301.06958.pdf"
issue: 137
issueUrl: "https://github.com/long8v/PTIR/issues/137"
---
<img width="1090" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e997c45a-e089-42e1-9674-7452665f4050">

[paper](https://arxiv.org/pdf/2301.06958.pdf)

## TL;DR
- **I read this because.. :** CLIP loss 관련
- **task :** contrastive learning -> image classification, object detection, semantic segmentation
- **problem :** CLIP + MAE 둘다 하고 싶당 
- **idea :** reconsturction의 target을 pixel level이 아니라 CLIP text feature와의 cosine similiarity로 해보자! 즉 language semantic에서의 reconstruction
- **input/output :** {image, text} pair
- **architecture :** ViT-B/16과 그에 상응하는 text encoder(12 heads, 768 hid dim)
- **objective :** InfoNCE(i2t, t2i), KL(recontructed patch와 text feature의 cosine similiarity, original image patch와 text feature의 cosine similarity)
- **baseline :** CLIP, BEiT, MAE, MAE + CLIP, MAE -> CLIP, etc..
- **data :** LAION-20M, LAION-50M -> COCO, LVIS, ADE20K
- **evaluation :** ImageNet(zs, linear probing, finetuning), AP(COCO, LVIS), mIoU(ADE20K)
- **result :** 같은 조건 다른 objectvie 들보다 더 좋은 성능! 
- **contribution :** contrastive loss + reconstruction loss. 두개의 이질적인 loss였는데 (하나는 vision modal에만 특화된) 얘를 잘 align을 했다? 실험을 많이 했고 writing도 잘한듯..
- **etc. :**

## Details
### Overview
<img width="529" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/598ee8bd-cf62-4767-b8cc-a794c2c8a7aa">

<img width="558" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3e36c86b-a19b-4e00-b180-8fdce3dd001f">

### Masked Visual Reconstruction in Language Semantic Space
Vision Encoder / Text Encoder는 CLIP거 사용 + reconstruction은 MAE처럼

<img width="337" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/66c56b41-8ccb-454c-a572-c8b760061dc3">

<img width="526" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/164d67f9-7650-45ff-8267-9604cd03b7fb">

- 
<img width="171" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/87a22436-a613-4804-9264-28cd54fb2156">

- $f_i^k$ : original image feature
- $g_i^k$ : MAE로 reconstruct된 image patch의 feature
- $\theta$ : proejction in vision encoder

<img width="512" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0e9f44a5-cf71-49ac-8221-2ce93accf226">

- $z_l^T$ : text embedding space에 있는(text projection 까지 한) text feature 
- text feature가 일종의 "prototype"처럼 사용됨

<img width="506" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b704ee3c-69a4-4b21-b9e9-4a6118b46676">

KL divergence. $p_i^k$는 stop gradient.

<img width="342" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d0bfbd2f-1645-46dc-8ce0-43010848481a">

최종 loss는 가중합. 2:1로 했다고

### Result
<img width="562" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/07d3cfe4-8cc1-472c-a4de-c874dfc381c4">

- L-20M은 laion에서 20M의 sample만 봤다는 뜻

<img width="1082" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b6d8007d-11fe-4784-9183-e63d07db9e1f">

<img width="1083" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/331dca28-3fe1-4252-ab94-7cbcd4775a08">

<img width="1071" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/849d30c2-0ff6-4b9e-b4dd-3290f33bbea1">

<img width="476" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/34cf8b83-05f8-4632-9018-2558b6073550">

<img width="1067" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/aadae235-b975-43f1-a027-a9cd6778f896">

<img width="525" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a19bc4ee-1470-49bf-b578-cfdbcd5e9db6">


### Ablation 

<img width="519" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1ace0031-3ed0-4947-a3fe-f8ebc6133f33">

- Table 9 : MIM -> LiT, MIM -> CLIP -> CLIP -> MIM 과 같은 two-stage보다 더 좋았다
- Table 10 : pixel level에서 하는 것보다, 그리고 language feature대신의 임의의 벡터와의 유사도로 kl divergence하는 것(high-level vision space)로 하는 것보다 성능이 더 좋았다. 유의미하게 좋넹

<img width="552" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/43364602-a2cb-4f3e-b2cf-f912087783ee">
