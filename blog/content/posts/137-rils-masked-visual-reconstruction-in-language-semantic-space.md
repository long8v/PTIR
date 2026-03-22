---
title: "[125] RILS: Masked Visual Reconstruction in Language Semantic Space"
date: 2023-08-02
tags: ['CVPR', 'CLIP', '2023Q1']
paper: "https://arxiv.org/pdf/2301.06958.pdf"
issue: 137
issueUrl: "https://github.com/long8v/PTIR/issues/137"
summary: "CLIP loss related - contrastive loss + reconstruction loss. two heterogeneous losses (one specialized for vision modal only) Did you align this guy well? Like you experimented a lot and wrote well."
---
<img width="1090" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e997c45a-e089-42e1-9674-7452665f4050">

[paper](https://arxiv.org/pdf/2301.06958.pdf)

## TL;DR
- **I read this because.. :** CLIP loss related
- **task :** contrastive learning -> image classification, object detection, semantic segmentation
- **problem :** I want to do both CLIP + MAE
- **idea :** target the reconstruction not at the pixel level, but at the cosine similarity to the CLIP text feature! i.e. reconstruction on language semantic
- **input/output :** {image, text} pair
- **architecture :** ViT-B/16 and its equivalent text encoder (12 heads, 768 hid dim)
- **objective :** InfoNCE(i2t, t2i), KL(cosine similarity of reconstructed patch and text feature, cosine similarity of original image patch and text feature)
- **baseline :** CLIP, BEiT, MAE, MAE + CLIP, MAE -> CLIP, etc..
- **data :** LAION-20M, LAION-50M -> COCO, LVIS, ADE20K
- **evaluation :** ImageNet(zs, linear probing, finetuning), AP(COCO, LVIS), mIoU(ADE20K)
- **result :** better performance than other objectvie for the same condition!
- **contribution :** contrastive loss + reconstruction loss. two heterogeneous losses (one specialized for vision modal only). align this guy well? experimented a lot and wrote well.
- **etc. :**

## Details
### Overview
<img width="529" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/598ee8bd-cf62-4767-b8cc-a794c2c8a7aa">

<img width="558" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3e36c86b-a19b-4e00-b180-8fdce3dd001f">

### Masked Visual Reconstruction in Language Semantic Space
Vision Encoder / Text Encoder uses CLIPger + reconstruction uses MAE like

<img width="337" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/66c56b41-8ccb-454c-a572-c8b760061dc3">

<img width="526" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/164d67f9-7650-45ff-8267-9604cd03b7fb">

- 
<img width="171" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/87a22436-a613-4804-9264-28cd54fb2156">

- $f_i^k$ : original image feature
- $g_i^k$ : feature of image patch reconstructed with MAE
- $\theta$ : proejction in vision encoder

<img width="512" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0e9f44a5-cf71-49ac-8221-2ce93accf226">

- $z_l^T$ : text feature in text embedding space (up to text projection)
- text feature is used as a kind of "prototype"

<img width="506" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b704ee3c-69a4-4b21-b9e9-4a6118b46676">

KL divergence. $p_i^k$ is the stop gradient.

<img width="342" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d0bfbd2f-1645-46dc-8ce0-43010848481a">

The final LOSS is the weighted sum. If we say 2:1

### Result
<img width="562" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/07d3cfe4-8cc1-472c-a4de-c874dfc381c4">

- L-20M means laion only saw 20M samples

<img width="1082" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b6d8007d-11fe-4784-9183-e63d07db9e1f">

<img width="1083" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/331dca28-3fe1-4252-ab94-7cbcd4775a08">

<img width="1071" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/849d30c2-0ff6-4b9e-b4dd-3290f33bbea1">

<img width="476" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/34cf8b83-05f8-4632-9018-2558b6073550">

<img width="1067" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/aadae235-b975-43f1-a027-a9cd6778f896">

<img width="525" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a19bc4ee-1470-49bf-b578-cfdbcd5e9db6">


### Ablation 

<img width="519" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1ace0031-3ed0-4947-a3fe-f8ebc6133f33">

- Table 9: MIM -> LiT, MIM -> CLIP -> CLIP -> MIM was better than two-stage, such as MIM -> LiT, MIM -> CLIP -> MIM
- Table 10: Performance was better than doing it at the pixel level, and better than doing it with kl divergence by similarity to a random vector (high-level vision space) instead of language features. Significantly better

<img width="552" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/43364602-a2cb-4f3e-b2cf-f912087783ee">
