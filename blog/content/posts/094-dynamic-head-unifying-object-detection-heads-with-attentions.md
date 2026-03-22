---
title: "[85] Dynamic Head: Unifying Object Detection Heads with Attentions"
date: 2022-12-01
tags: ['2021Q2', 'CVPR', 'microsoft', 'object detection']
paper: "https://arxiv.org/pdf/2106.08322.pdf"
issue: 94
issueUrl: "https://github.com/long8v/PTIR/issues/94"
summary: "Diversify your attention to each dimension."
---
![image](https://user-images.githubusercontent.com/46675408/204942143-34757d3b-07bb-4159-8b63-e5090b2094cd.png)

[paper](https://arxiv.org/pdf/2106.08322.pdf), [code](https://github.com/microsoft/DynamicHead)

## TL;DR
- **task :** object detection
- Problem :** Previous work has improved 1) scale-aware : image pyramid, feature pyramid ... 2) spatial-aware : convolution, deformable conv ... 3) task-aware : od with segmentation, two-stage, FCOS(center instead of bbox) ... but no paper has tried to do all three well!
- **idea :** Let's give attention to each of the dimensions L(=num of feature level) x S(=spatial. W x H) x C(=num of channel, task)!
- **architecture :** scale is hard sigmoid for 1x1 conv -> spatial uses deformable attention -> task is slicing the cth channel so that it is on-off for that task via max. You can put this dynamic head attention anywhere if you sandwich it between 2-stage or one-stage.
- **objective :** object detection loss
- **baseline :** Mask-RCNN, Cascade-RCNN, FCOS, ATSS, BorderDet, DETR, ... 
- **data :** MS-COCO
- **result :** Applying DyHead to the object detection model unconditionally improves performance. Almost SOTA.
- Diversify the **contribution :** attention to each dimension.
- **limitation or something I don't understand :** The shape of the result of exactly 3 attention is not drawn.

## Details
### architecture
![image](https://user-images.githubusercontent.com/46675408/204951599-1dbd26c5-82d3-4ed3-ba6d-88fe40af6c0e.png)

### Dynamic Head
![image](https://user-images.githubusercontent.com/46675408/204951688-7cb6038c-92e7-43d7-bc4c-e1fd07c86b56.png)
- $F\in R^{LxSxC}$ : feature tensor. from backbone's feature pyramid

If this is normal self-attention
![image](https://user-images.githubusercontent.com/46675408/204951859-c8a5028b-17ec-4eb8-b80f-8b8d3d12e66a.png)
This is why the dynamic head is paying attention to L, S, and C respectively!

### Scale-aware Attention
![image](https://user-images.githubusercontent.com/46675408/204951945-df7aedc2-56a5-4d24-9a7d-2e6641061274.png)

- $f$ : linear function. Implemented as a 1x1 conv
- $\sigma$ : $max(0, min(1, \frac{x+1}{2}))$

### Spatial-aware Attention 
![image](https://user-images.githubusercontent.com/46675408/204952379-8c86a7e4-c42a-4468-9fe7-6f8f728087e1.png)

Using deformable attention.
- K : # of sparse sampling locations
- $\delta p_k$ : sampling location
- $\delta m_k$ : self-learned importance scalar at location $p_k$

### Task-aware Attention
![image](https://user-images.githubusercontent.com/46675408/204952641-91512efe-394d-4bce-b603-995b7bd1ab14.png)

- $F_c$ : cth channel sliced from feature map
- $\theta$ : Global average pooling over L x S dimensions and thesholding implemented as 2 fcn -> normalizing -> sigmoid (as if omitted in the formula?)
- $\alpha$, $\beta$: output of the activation thesholding function $theta$ above.
 
![image](https://user-images.githubusercontent.com/46675408/204953143-bcb9298c-dc4d-4fbc-bf4c-481343b32af5.png)

### Generalizing to Existing Detectors
- one stage detector
Prior research shows that cls subnetworks and bbox regressors behave very differently.
Predicting cls, bbox with unified branch to backbone, unlike this conventional approach. This is thanks to DyHead!

- two stage detector
Apply DyHead before RoI pooling

## Result
![image](https://user-images.githubusercontent.com/46675408/204953599-1532a05b-cff9-423c-bd7f-387c659c9bca.png)
![image](https://user-images.githubusercontent.com/46675408/204953615-669c3e4c-3a82-4e70-8442-9d843d330e05.png)
![image](https://user-images.githubusercontent.com/46675408/204953633-059da00b-1ec0-4487-bd0d-d5fb187a0bfa.png)


## Ablation
![image](https://user-images.githubusercontent.com/46675408/204953569-dfd386b7-b700-41b6-adc8-d144d35e0628.png)


![image](https://user-images.githubusercontent.com/46675408/204953540-dc903ddc-6478-45cd-b13c-ae1ac973ddd8.png)

