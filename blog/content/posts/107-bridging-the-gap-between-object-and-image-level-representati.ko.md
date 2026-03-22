---
title: "[98] Bridging the Gap between Object and Image-level Representations for Open-Vocabulary Detection"
date: 2023-01-17
tags: ['NeurIPS', 'object detection', '2022Q3', 'CLIP']
paper: "https://arxiv.org/pdf/2207.03482.pdf"
issue: 107
issueUrl: "https://github.com/long8v/PTIR/issues/107"
---
![image](https://user-images.githubusercontent.com/46675408/212799192-850dd722-1d29-400a-8629-61399d1014cf.png)

[paper](https://arxiv.org/pdf/2207.03482.pdf)

## TL;DR
- **I read this because.. :** NeurIPS, open-vocab object detection
- **task :** open-vocab object detection
- **problem :** CLIP은 이미지 레벨의 표현이어서 detection task를 잘 하도록 align이 되어있지 않다.
- **idea :** 1) class agnostic한 Object detection 모델로 image classification dataset으로 pseudo-label을 만들어 vocab을 확장하자 2) region feature와 CLIP이 가까워 지도록 KD를 하자 3) 1, 2가 반대 방향으로 움직이니 둘의 weight를 tie 시키자 
- **architecture :** Faster RCNN에서 Region proposal한거에다가 classifier 대신 image feature를 CLIP image encoder에 넣고 `a photo of {category}`의 CLIP text embedding과 가장 가까운 것으로 분류하는 방식
- **objective :** 1) point-wise embedding matching loss 2) inter-embedding relationship matching loss 3) image-level supervision loss 
- **baseline :** supervised, OVR-CNN, ViLD, RegionCLIP, Detic ...
- **data :** COCO, LVIS v1.0, ImageNet-21K, COCO-captions, LMDET
- **evaluation :** $AP_{base}$, $AP_{novel}$
- **result :** 괜찮은 성능
- **contribution :** image-level data를 detection에 활용하는 학습 프레임워크 제안 
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
