---
title: "[84] DiffusionDet: Diffusion Model for Object Detection"
date: 2022-11-29
tags: ['object detection', 'generative', '2022Q4']
paper: "https://arxiv.org/abs/2211.09788"
issue: 93
issueUrl: "https://github.com/long8v/PTIR/issues/93"
---
<img width="828" alt="image" src="https://user-images.githubusercontent.com/46675408/204419010-28ef23ac-f9de-4fc5-aa02-76522ef5bb51.png">

[paper](https://arxiv.org/abs/2211.09788)

## TL;DR
- **task :** object detection 
- **problem :** 대부분의 object detection 모델 들은 anchor box와 같은 미리 정의된 object candidate들에 의존하고 DETR류도 object query 개념이 있어서 학습보다 더 많은 개수의 object를 뽑을 수 없음.
- **idea :** diffusion을 사용해서 image bbox를 뽑자!
- **architecture :** GT bbox + gaussian noise를 encoder(ResNet-50, Swin-b)에 넣고 RoI pooling으로 feature 뽑음 decoder는 feature와 이전 step에서의 bbox를 받고 bbox / cls 예측
- **objective :** hungarian loss(=DETR loss)
- **baseline :** DETR, deformable DETR, Sparse R-CNN
- **data :** MS-COCO, LVIS
- **result :** SOTA ?!
- **contribution :** diffusion을 Object detection에 적용한 첫 논문
- **limitation or 이해 안되는 부분 :** 디퓨전을 안읽어서 정확히는 이해가 안된다만 성능이 나오는게 신기 ㅋㅋ 심지어 SOTA라니? 결과를 뭔가 좋아보이려고 장치를 쓴건가

## Details
### motivation
<img width="525" alt="image" src="https://user-images.githubusercontent.com/46675408/204426794-153190d3-f88e-4801-814d-2594fdea9ced.png">
<img width="508" alt="image" src="https://user-images.githubusercontent.com/46675408/204426808-69d45e0c-eb31-4842-a8a4-27c3ca17d60f.png">

### Preliminaries : diffusion model
<img width="339" alt="image" src="https://user-images.githubusercontent.com/46675408/204426917-866384b2-e3d4-43bc-a989-d606c46c0b6e.png">

- $z_0$ : data sample
- $z_t$ : latent noisy sample
- $t$ : step
- $\bar a_t$ =  
<img width="300" alt="image" src="https://user-images.githubusercontent.com/46675408/204427152-cd223671-0808-4a5c-a4e6-6ae988960687.png">

학습되는 loss는 neural network $f_\theta$의 결과값과 $z_0$의 MSE
<img width="300" alt="image" src="https://user-images.githubusercontent.com/46675408/204427548-c438c9a5-4f5c-4981-9346-c711ac5a3fdf.png">

이 논문에서 $z_0$는 GT bbox. 

### architecture
<img width="529" alt="image" src="https://user-images.githubusercontent.com/46675408/204426854-dce7af56-9dc7-4552-915c-2ec7e2acaf2a.png">

- encoder 
ResNet, Swin에 Feature pyramid 적용
- decoder
sparse R-CNN #58 과 비슷하게 proposal box들을 crop해서 RoI feature로 사용 

#### Sparse R-CNN과 차이
(1) random bbox로 시작하기 때문에 infer단계에서 학습에서 사용한 bbox 개수보다 더 많이 사용할 수 있음
(2) sparse RCNN과 달리 첫번째 RoI pooling한 feature만 받음
(3) detector head를 재사용 

### Training
GT + gaussian noise 추가해서 Noisy bbox로 만들고 이걸로 시작.
<img width="504" alt="image" src="https://user-images.githubusercontent.com/46675408/204427990-043ea095-93f7-4c55-b27b-4caadcce5153.png">

- padding : GT bbox 개수가 다 다르니까 패딩해준다. 1) gt bbox 복사 2) 랜덤 박스 3) 이미지 크기의 박스 등으로 패딩해봤는데 가우시안 랜덤 박스 패딩이 제일 좋았음
- box corruption : noise $a_t$는 step t에 따라 점점 줄어든다. signal-to-noise ratio(?)가 중요했는데 image generation보다 더 높은 signal scaling value를 가져야했다.
- training losses : DETR loss 썼다. 

### Inference 
그냥 랜덤 가우시안 bbox로 시작
<img width="519" alt="image" src="https://user-images.githubusercontent.com/46675408/204428014-7f15bbfb-e489-4caa-a388-92e2b310905e.png">
 
- ddim : bbox 뽑고 다음 스텝으로 넘겨줄 때 DDIM(이전 step 뿐 아니라 초기값까지 줘야하는 모델, DDPM과 달리 non-markov)을 사용했다.
- box_renewal : step t에서 구린 bbox들을 score로 filtering해서 random box로 바꿔줬다.
 
### Result
- COCO 2017
<img width="509" alt="image" src="https://user-images.githubusercontent.com/46675408/204426670-ff90f689-43e9-4bf6-9806-2125d9c6bf8a.png">

- LVIS v1.0 val
<img width="524" alt="image" src="https://user-images.githubusercontent.com/46675408/204426742-26838bc1-2e76-4bcd-9872-318400ef0a1c.png">
