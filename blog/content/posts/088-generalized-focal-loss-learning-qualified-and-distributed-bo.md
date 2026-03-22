---
title: "Generalized Focal Loss: Learning Qualified and Distributed Bounding Boxes for Dense Object Detection"
date: 2022-11-17
tags: ['2020Q3', 'object detection', 'imbalance', 'uncertainty']
paper: "https://arxiv.org/pdf/2006.04388.pdf"
issue: 88
issueUrl: "https://github.com/long8v/PTIR/issues/88"
summary: "It performs better than no quality branch, and there are a few things that are behind IoU-branch, but most of them are improved."
---
![image](https://user-images.githubusercontent.com/46675408/202342641-7a10ba5a-2708-41d5-89ac-01e8760801f8.png)

[paper](https://arxiv.org/pdf/2006.04388.pdf)

## TL;DR
- **task :** dense object detection with localization score
- Problem :** Existing localization score extraction works 1) separately learn the IoU score branches when training and combine them when inferring, resulting in a gap between train and infer, 2) impose localization quality only on positives, resulting in very high IoU scores for negative samples, and 3) assume the bbox distribution is Dirac-Delta or gaussian, which is too simple.
- **idea :** Combine category and IoU score when learning to give a smooth target to eliminate the learning-inference gap, and also learn the distribution over bboxes to eliminate the strong constraint of the distribution.
- **architecture :** ResNet with FPN + ???
- **objective :** 1) multiply the focal loss by $|y-\sigma|^\beta$, the distance term from the target, instead of $(1-p_t)^\gamma$ and 2) also reflect the value for the discrete distribution learned => Generalized Focal Loss
- **baseline :** w/o quality branch, IoU branch, centerness-guided, IoU guided
- **data :** COCO
- **result :** better performance than no quality branch, and most of the rest are better than IoU-branch with a few exceptions.
- **contribution :**
- **Limitations or things I don't understand :** I don't really understand the Distribution Focal Loss part and I'm not sure what the architecture you experimented with here is. Is it just ResNet + FPN plus bbox prediction for every pixel? What is ATSS?

## Details
### Problems with traditional methods
![image](https://user-images.githubusercontent.com/46675408/202345248-21e15ad3-d891-495e-b79c-6c6e1775b4d4.png)

![image](https://user-images.githubusercontent.com/46675408/202345664-f1cba8af-0c60-4a04-8fa1-8d0eb890b94d.png)

### Key Ideas in Generalized Focal Loss
![image](https://user-images.githubusercontent.com/46675408/202345326-3ad3e99d-1abe-4411-a32d-4530766c265c.png)

- focal loss 
![image](https://user-images.githubusercontent.com/46675408/202345361-561dfebd-9beb-4c7c-8e28-b3dd09ac426e.png)

- quality focal loss 
![image](https://user-images.githubusercontent.com/46675408/202345533-4c98f024-c846-4684-ad9e-76f6ccad2638.png)

- distribution focal loss 
![image](https://user-images.githubusercontent.com/46675408/202345867-9b049a8c-e2a1-42ad-93e9-fbc2ec85a576.png)

![image](https://user-images.githubusercontent.com/46675408/202345425-9a55fe04-c465-4951-bc09-034d3da517b3.png)

- generalized focal loss
![image](https://user-images.githubusercontent.com/46675408/202345470-40c40cab-4bef-4c06-a87c-67d6fe423b53.png)

### Result
![image](https://user-images.githubusercontent.com/46675408/202345601-c28818f7-db5a-42bf-8810-1ff83ef8500f.png)
