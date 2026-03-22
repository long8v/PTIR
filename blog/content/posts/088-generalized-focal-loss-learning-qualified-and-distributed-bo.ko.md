---
title: "[80] Generalized Focal Loss: Learning Qualified and Distributed Bounding Boxes for Dense Object Detection"
date: 2022-11-17
tags: ['2020Q3', 'object detection', 'imbalance', 'uncertainty']
paper: "https://arxiv.org/pdf/2006.04388.pdf"
issue: 88
issueUrl: "https://github.com/long8v/PTIR/issues/88"
---
![image](https://user-images.githubusercontent.com/46675408/202342641-7a10ba5a-2708-41d5-89ac-01e8760801f8.png)

[paper](https://arxiv.org/pdf/2006.04388.pdf)

## TL;DR
- **task :** dense object detection with localization score
- **problem :** 기존의 localization score를 뽑는 work들은 1) 학습할 때 IoU score 브랜치를 따로 학습하다가 infer할 때 결합해서 train - infer 간의 괴리가 생겼고 2) localization quality가 positive에만 부과되어서 negative sample도 IoU score가 매우 높게 나오는 경우가 있었으며 3) bbox 분포에 대한 가정이 Dirac-Delta이거나 gaussian으로 너무 단순했다.
- **idea :** 학습 때 category와 IoU score를 결합하여 smooth한 target을 주어 학습-추론 괴리를 없애고 bbox에 대한 분포도 학습하게 하여 분포의 강한 제약을 없애자
- **architecture :** ResNet with FPN + ???
- **objective :** 1) focal loss의 $(1-p_t)^\gamma$ 대신에 target 과의 거리 term인 $|y-\sigma|^\beta$를 곱해주고 2) 학습한 discrete 분포에 대한 값도 반영해줌 => Generalized Focal Loss
- **baseline :** w/o quality branch, IoU branch, centerness-guided, IoU guided
- **data :** COCO
- **result :** quality branch 없는 것보단 성능이 좋고 나머지는 IoU-branch에 뒤지는게 몇개 있는데 대부분 개선
- **contribution :**
- **limitation or 이해 안되는 부분 :** Distribution Focal Loss 부분은 잘 이해 안되고 여기서 실험한 아키텍쳐가 어떻게 되는지도 잘 모르겠음. 그냥  ResNet + FPN 에다가 모든 픽셀에 bbox 예측하는건가? ATSS는 무엇인가

## Details
### 기존 방법의 문제점
![image](https://user-images.githubusercontent.com/46675408/202345248-21e15ad3-d891-495e-b79c-6c6e1775b4d4.png)

![image](https://user-images.githubusercontent.com/46675408/202345664-f1cba8af-0c60-4a04-8fa1-8d0eb890b94d.png)

### Generalized Focal Loss의 주요 아이디어
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
