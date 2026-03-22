---
title: "[98] Bridging the Gap between Object and Image-level Representations for Open-Vocabulary Detection"
date: 2023-01-17
tags: ['NeurIPS', 'object detection', '2022Q3', 'CLIP']
paper: "https://arxiv.org/pdf/2207.03482.pdf"
issue: 107
issueUrl: "https://github.com/long8v/PTIR/issues/107"
summary: "NeurIPS, open-vocab object detection - proposes a learning framework that utilizes image-level data for detection"
---
![image](https://user-images.githubusercontent.com/46675408/212799192-850dd722-1d29-400a-8629-61399d1014cf.png)

[paper](https://arxiv.org/pdf/2207.03482.pdf)

## TL;DR
- **I read this because.. :** NeurIPS, open-vocab object detection
- **task :** open-vocab object detection
- Problem :** CLIP is an image-level representation and is not aligned well for the detection task.
- **idea :** 1) Extend vocab by creating pseudo-label with image classification dataset with class agnostic Object detection model 2) KD to make region feature and CLIP close 3) Tie the weight of 1 and 2 since they are moving in opposite directions.
- **architecture :** Faster RCNN's Region proposal, but instead of a classifier, we put the image feature into the CLIP image encoder and classify it as closest to the CLIP text embedding of `a photo of {category}`.
- **objective :** 1) point-wise embedding matching loss 2) inter-embedding relationship matching loss 3) image-level supervision loss 
- **baseline :** supervised, OVR-CNN, ViLD, RegionCLIP, Detic ...
- **data :** COCO, LVIS v1.0, ImageNet-21K, COCO-captions, LMDET
- **evaluation :** $AP_{base}$, $AP_{novel}$
- **result :** Decent performance
- **contribution :** Propose a learning framework that utilizes image-level data for detection
- **limitation / things I cannot understand :**

## Details
### Preliminaries
- Multimodal ViT (MViT)
https://arxiv.org/pdf/2111.11430.pdf
class-agnostic object detector
![image](https://user-images.githubusercontent.com/46675408/212798794-37e8c0c7-3043-44d8-87d5-91f0a2fdf67b.png)

![image](https://user-images.githubusercontent.com/46675408/212799059-94be0c40-88f0-4000-a5b2-bf8b09204b61.png)

### Detection Pipeline 
![image](https://user-images.githubusercontent.com/46675408/212805314-81fac2b3-0e86-4461-8965-8561153db476.png)

![image](https://user-images.githubusercontent.com/46675408/212805420-4edf96f0-f09c-4aaf-a725-53f3237432a7.png)

![image](https://user-images.githubusercontent.com/46675408/212805441-e32b9f77-9b71-4437-9ab2-a014e7d5b31d.png)


### Loss
-  Point-wise embedding matching loss
![image](https://user-images.githubusercontent.com/46675408/212805517-b4f1723f-fa9e-4001-b896-b557d4282525.png)

- Inter-embedding relationship matching loss
![image](https://user-images.githubusercontent.com/46675408/212805553-b266b8ab-7fe2-412e-b0cb-a5978d863727.png)

- Image-level Supervision with Pseudo Box Labels
...

-  Weight Transfer Function
![image](https://user-images.githubusercontent.com/46675408/212805629-0afafaba-60a4-4bdc-a8f9-44bfd2b45f26.png)

### Result
![image](https://user-images.githubusercontent.com/46675408/212805715-b8dddc51-0e94-4087-94c9-6ae5d99030ae.png)

![image](https://user-images.githubusercontent.com/46675408/212805732-eaa06f0c-b34b-46a2-b616-bffa6c6e5ade.png)
