---
title: "[85] Dynamic Head: Unifying Object Detection Heads with Attentions"
date: 2022-12-01
tags: ['2021Q2', 'CVPR', 'microsoft', 'object detection']
paper: "https://arxiv.org/pdf/2106.08322.pdf"
issue: 94
issueUrl: "https://github.com/long8v/PTIR/issues/94"
---
![image](https://user-images.githubusercontent.com/46675408/204942143-34757d3b-07bb-4159-8b63-e5090b2094cd.png)

[paper](https://arxiv.org/pdf/2106.08322.pdf), [code](https://github.com/microsoft/DynamicHead)

## TL;DR
- **task :** object detection
- **problem :** 이전의 연구들은 1) scale-aware : image pyramid, feature pyramid ... 2) spatial-aware : convolution, deformable conv ... 3) task-aware : od with segmentation, two-stage, FCOS(center instead of bbox) ... 한 각각을 개선하는 연구들을 냈지만 세개를 모두 잘 하고자하는 논문은 없었다!
- **idea :** L(=num of feature level) x S(=spatial. W x H) x C(=num of channel, task) 차원에 대해 각각 attention을 걸어주자!
- **architecture :** scale은 1x1 conv에 hard sigmoid -> spatial은 deformable attention 사용 -> task는 c번째 채널 슬라이싱해서 max를 통해 해당 태스크에 on-off 되도록 설정. 이 dynamic head attention을 2-stage나 one-stage에 중간에 끼워넣으면 어디에나 넣을 수 있음.
- **objective :** object detection loss
- **baseline :** Mask-RCNN, Cascade-RCNN, FCOS, ATSS, BorderDet, DETR, ... 
- **data :** MS-COCO
- **result :** object detection 모델에 DyHead를 적용하면 성능이 무조건 좋아짐. 거의 SOTA.
- **contribution :** attention을 각 차원에 대해 하면서 다양화.
- **limitation or 이해 안되는 부분 :** 정확히 3번의 attention 결과물의 shape이 그려지진 않넹

## Details
### architecture
![image](https://user-images.githubusercontent.com/46675408/204951599-1dbd26c5-82d3-4ed3-ba6d-88fe40af6c0e.png)

### Dynamic Head
![image](https://user-images.githubusercontent.com/46675408/204951688-7cb6038c-92e7-43d7-bc4c-e1fd07c86b56.png)
- $F\in R^{LxSxC}$ : feature tensor. backbone의 feature pyramid에서 나온거

이게 보통의 self-attention이라고 한다면
![image](https://user-images.githubusercontent.com/46675408/204951859-c8a5028b-17ec-4eb8-b80f-8b8d3d12e66a.png)
이럻게 L, S, C에 대해 각각 attention하는게 dynamic head!

### Scale-aware Attention
![image](https://user-images.githubusercontent.com/46675408/204951945-df7aedc2-56a5-4d24-9a7d-2e6641061274.png)

- $f$ : linear function. 1x1 conv로 구현됨
- $\sigma$ : $max(0, min(1, \frac{x+1}{2}))$

### Spatial-aware Attention 
![image](https://user-images.githubusercontent.com/46675408/204952379-8c86a7e4-c42a-4468-9fe7-6f8f728087e1.png)

deformable attention 사용.
- K : # of sparse sampling locations
- $\delta p_k$ : sampling location
- $\delta m_k$ : self-learned importance scalar at location $p_k$

### Task-aware Attention
![image](https://user-images.githubusercontent.com/46675408/204952641-91512efe-394d-4bce-b603-995b7bd1ab14.png)

- $F_c$ : feature map에서 c번째 채널 슬라이싱한거
- $\theta$ : L x S차원에 대해 Global average pooling하고 2 fcn -> normalizing -> sigmoid로 thesholding 구현되어있음 (수식에 생략된듯?)
- $\alpha$, $\beta$ : 위의 activation thesholding function $theta$의 output.
 
![image](https://user-images.githubusercontent.com/46675408/204953143-bcb9298c-dc4d-4fbc-bf4c-481343b32af5.png)

### Generalizing to Existing Detectors
- one stage detector
cls subnetwork와 bbox regressor는 매우 다르게 행동한다는 선행연구.
이러한 conventional approach와 다르게 backbone에 Unified branch로 cls, bbox를 예측함. 이는 DyHead덕분!

- two stage detector
RoI pooling 하기 전에 DyHead 적용

## Result
![image](https://user-images.githubusercontent.com/46675408/204953599-1532a05b-cff9-423c-bd7f-387c659c9bca.png)
![image](https://user-images.githubusercontent.com/46675408/204953615-669c3e4c-3a82-4e70-8442-9d843d330e05.png)
![image](https://user-images.githubusercontent.com/46675408/204953633-059da00b-1ec0-4487-bd0d-d5fb187a0bfa.png)


## Ablation
![image](https://user-images.githubusercontent.com/46675408/204953569-dfd386b7-b700-41b6-adc8-d144d35e0628.png)


![image](https://user-images.githubusercontent.com/46675408/204953540-dc903ddc-6478-45cd-b13c-ae1ac973ddd8.png)

