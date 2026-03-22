---
title: "[27] Cross-Domain Few-Shot Classification via Learned Feature-Wise Transformation"
date: 2022-05-23
tags: ['few-shot', '2020Q1', 'ICLR']
paper: "https://arxiv.org/pdf/2001.08735.pdf"
issue: 32
issueUrl: "https://github.com/long8v/PTIR/issues/32"
---
<img width="847" alt="image" src="https://user-images.githubusercontent.com/46675408/169812425-e2791252-5faa-4709-a7fe-cc71509fcb5f.png">


[paper](https://arxiv.org/pdf/2001.08735.pdf), [code](https://github.com/hytseng0509/CrossDomainFewShot)

## TL;DR 
**problem :** few-shot classification은 같은 domain(=ImageNet 내에서 unseen label을 예측)에서는 잘 작동되지만, 다른 도메인으로 few-shot을 할 경우 잘 작동되지 않음(ImageNet으로 훈련된게 CUB 데이터로 few-shot test를 하면 잘 안나옴)
**solution :** feature encoder에 feature-wise transformation layer(affine 변환)를 추가하였고 이때의 하이퍼파라미터는 learning-to-learn 방법론으로 학습됨. 
**result :** MatchingNet, RelationNet, Graph Neural Network에 위의 feature-wise transformation을 적용했을 때 generalization 성능이 좋았음. 

## details 
- domain adaption / generalization의 차이는 generalization의 경우 학습 단계에서 unseen domain을 사용하지 않고 generalize 해야 함.
- 우리는 domain generalization 문제를 few-shot 셋팅에서 novel한 클래스를 분류하는 문제로 바꿈. 

### 3.1. Preliminaries
- few-shot terms
  - N_w : # of categories
  - N_s : # of labeled examples for each categories
- 아래 그림은 3 way 3 shot few shot의 예시
<img width="813" alt="image" src="https://user-images.githubusercontent.com/46675408/169812728-1c1dc722-3752-48da-9607-1f66aa0ca7b1.png">

- metric-based의 알고리즘은 feature encoder E와 metric function M으로 구성되어 있음. 
- 각 iteration에서 N_w개의 카테고리를 뽑고 task T를 만든다. input image를 X, 이에 해당하는 label을 Y라고 하고. task T는 support set인 S={(X_s, T_s)}와 query set인 {(X_q, Y_q)}로 구성된다. 
- feature encoder E는 support와 query 이미지의 feature를 뽑고 metric function M에 넣어 support image의 label을 참고하여 query image의 카테고리를 예측한다. 
<img width="326" alt="image" src="https://user-images.githubusercontent.com/46675408/169816949-89019fb0-b3af-4ba5-bc43-fb24b3ab5152.png">

- 학습 목표 함수는 query set에 대한 이미지의 classification loss이다. 
<img width="251" alt="image" src="https://user-images.githubusercontent.com/46675408/169816998-b546aedb-6ff3-46ae-926a-34608093d151.png">

- 다양한 metric-based 알고리즘의 주요한 차이점은 이미지 피쳐를 뽑는 E의 아키텍쳐에 따라 달라진다. 가령 MatchingNet은 LSTM, RelationNet은 CNN, GNN은 GCN
- 학습할 때 seen domain들로 training하고 평가는 unseen domain에 대하여 하였다.

### 3.2. feature-wise transformation layer
<img width="251" alt="image" src="https://user-images.githubusercontent.com/46675408/169821093-45bd57ed-8478-48f3-805d-369e391578ab.png">


- 우리의 목표는 unseen 데이터에 대해 generalization을 더 잘하기 위함인데, metric function M이 seen domain에 overfitting되기 쉬우므로 이를 막아줘야한다.
- 직관적으로, feature encoder E에 affine transformation을 적용하면 더 다양한 분포를 표현할 수 있을 것 같다.
- hyper parameter는 아핀 변환 파라미터를 sampling 하기 위한 standard dev를 뜻한다.
<img width="536" alt="image" src="https://user-images.githubusercontent.com/46675408/169819651-da38dd31-7527-4743-8f21-2ffba623de0b.png">

- batch norm 이후에 아래의 feature-wise transformation layer를 적용한다. 
<img width="324" alt="image" src="https://user-images.githubusercontent.com/46675408/169819934-5fd871b7-12fe-47ba-a991-bf2a5224bb5b.png">

### 3.3 Learning the feature-wise transformation layers(=FT layer)
- 위의 하이퍼파라미터를 경험적으로 선택할 수도 있겠지만 학습할 수 있도록 하고 싶다. 우리는 이를 위해 learning-to-learn 알고리즘을 디자인했다. 주요 아이디어는 FT 레이어를 적용하여 seen domain에 대해서 학습한 것이 unseen domain에 대해서도 나은 성능을 내게 하는 것이다.
<img width="831" alt="image" src="https://user-images.githubusercontent.com/46675408/170910374-2a36a16f-8e54-461d-9728-8b0c80dd2e21.png">

각 training iter t 에서 seen domain 중 sampling해서 pseudo-seen domain(ps)과 pseudo-unseen domain(pu)를 만든다. FT layer에 대해 파라미터를 적용하여 feature encoder와 metric function을 적용하고 seen domain task에 대해서만 loss를 구한다. 
<img width="450" alt="image" src="https://user-images.githubusercontent.com/46675408/170921839-e16365e7-7359-4574-b078-142357c40f6b.png">

generalization을 측정하는 단계에서는 1) 모델의 FT 레이어를 제거하고 2) pseudo-unseen task에 대해서 업데이트 된 모델의 classification loss를 구하여 계산한다. 즉, 
<img width="605" alt="image" src="https://user-images.githubusercontent.com/46675408/170922450-6d65d6c9-4ef6-468b-b244-6d0db1910012.png">

마지막으로, 위의 loss는 FT 레이어의 효율성을 반영하므로, 하이퍼 파라미터를 아래와 같이 업데이트 한다. 
<img width="294" alt="image" src="https://user-images.githubusercontent.com/46675408/170922563-608e0e1a-5fcc-4ef0-b85e-1df3da9cc456.png">

즉 metric-based model과 feature-wise transformation layer(FT)는 학습단계에서 함께 학습된다.

## Experimental Results
- FT : 경험상 고른 하이퍼파라미터로 FT layer 설정했을 때
<img width="1080" alt="image" src="https://user-images.githubusercontent.com/46675408/171078324-a96382aa-1e30-4448-afff-0b3295e38d9a.png">

- LFT : FT 레이어의 하이퍼파라미터가 학습 가능할 때, 
<img width="636" alt="image" src="https://user-images.githubusercontent.com/46675408/171078350-8228ce11-c3f5-4cde-adfa-da052a1d8d24.png">

- 도메인별 tSNE 결과. 도메인끼리 잘 섞여있음 -> cross-domain adapt를 잘할 수 있음.
<img width="651" alt="image" src="https://user-images.githubusercontent.com/46675408/171078811-8db8f500-c099-456f-b2be-222492a377b0.png">
