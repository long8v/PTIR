---
title: "[101] Multi-Task Learning Using Uncertainty to Weigh Losses for Scene Geometry and Semantics"
date: 2023-01-31
tags: ['2017', 'uncertainty', 'MTL']
paper: "https://arxiv.org/pdf/1705.07115.pdf"
issue: 110
issueUrl: "https://github.com/long8v/PTIR/issues/110"
---

![image](https://user-images.githubusercontent.com/46675408/215653791-b58ffbc0-85d6-4b18-941e-994821a91bf3.png)

[paper](https://arxiv.org/pdf/1705.07115.pdf)

## TL;DR
- **I read this because.. :** multi-task learning with uncertainty!
- **task :** semantic segmentation, instance segmentation, pixel-wise metric depth
- **problem :** 이전의 멀티태스크 접근법은 loss들의 가중합인데 이 가중에 따라 성능이 매우 예민하게 움직인다.
- **idea :** output y에 대해 가우시안으로 가정하고 MLE에 따라 추정하면 $\sigma$에 의해 각 task 자체의 noise와 상대적인 weight를 구할 수 있다. 즉 model weight $W$와 task dependent $\sigma_{task}$를 같이 최적화하자. 
- **architecture :** DeepLab V3(ResNet101 -> Atrous Spatial Pyramid Pooling) + 3개 태스크에 맞는 decoder 
- **objective :** CE(semantic segmentation), L1(instance segmentation, depth estimation)
- **baseline :** task specific model, weighted multi-task model
- **data :** CityScapes benchmark, depth image는 SGM이라는 모델로 pseudo-label 사용
- **evaluation :** IoU, Instance Mean Error, Inverse Depth Mean Error
- **result :** 3개의 태스크로 학습한게 segmentation, depth 예측에서 sota. instance segmentation은 2개로 학습한 곳에서 sota
- **contribution :** 3 태스크로 학습한 모델이 처음이라고 하넹
- **limitation / things I cannot understand :** 대충 결론적으로 보면 학습 가능한 weight 추가하고 이게 널뛰기 되지 않도록 Regularization term 추가한건데 mle 관점으로 해석되니까 보기에 아름답넹

## Details
### motivation
<img width="846" alt="image" src="https://user-images.githubusercontent.com/46675408/215655493-2142014e-58e0-4cd1-b600-fa86a5321bc2.png">

multi-task loss weight에 따라 성능이 널뛰기 함

### Architecture 
<img width="1054" alt="image" src="https://user-images.githubusercontent.com/46675408/215655442-7f6f61e5-3faf-4b82-bc8f-f2a944e28382.png">

### Homoscedastic uncertainty as task-dependent uncertainty
- Epistemic uncertainty 
  - model에 의한 uncertainty, training data의 부족으로 인한 Uncertainty 
- Aleatroic uncertainty
  - 데이터에 의한 uncertainty, data가 표현할 수 없는 정보에 대한 uncertainty. 
    - Data-dependent, Hetroscedatic 
      - input data와 모델 아웃풋에 의해 결정되는 uncertainty 
    - Task-dependent, Homoscedastic
      - input data에 의존하지 않는 uncertainty

뭐라는지 안와닿네.. 어쨌든 이 논문에서는 마지막 task-dependent uncertainty에 대해 측정할거임

### Multi-task likelihoods 
뉴럴네트워크의 아웃풋을 $f^W(x)$라고 하자. regression 문제에서는 Output을 가우시안을 따르는 걸로 가정할 수 있음
<img width="257" alt="image" src="https://user-images.githubusercontent.com/46675408/215656416-377887fb-7340-4a6e-84ae-721638cf510d.png">

이때 $\sigma$는 Noise scalar

분류문제에 대해서는 softmax를 취해서 확률분포로 만듦
<img width="275" alt="image" src="https://user-images.githubusercontent.com/46675408/215656530-321eaa70-88b3-4db3-857b-6ed76b06a058.png">

multiple-model output에 대해서는 factorize해서 이렇게 표현할 수 있음.
<img width="385" alt="image" src="https://user-images.githubusercontent.com/46675408/215656673-738cca2d-b5ea-4c36-a86f-69de95c05679.png">

maximum likelihood estimation에 따르면 Log likelihood는 이렇게 쓸 수 있음
<img width="361" alt="image" src="https://user-images.githubusercontent.com/46675408/215656721-42f2d8cf-34b4-45fd-bf2c-f612cad95376.png">

두개의 gaussian을 따르는 모델 아웃풋에 대한 Log likehlihood에 대해서는 아래와 같이 쓸 수 있음
<img width="421" alt="image" src="https://user-images.githubusercontent.com/46675408/215656841-4eca4df1-6229-41eb-9b66-1658bbb68ac4.png">

이는 이제 $\mathcal{L}(W, \sigma_1, \sigma_2)$에 대한 minimisation 문제로 볼 수 있음
<img width="415" alt="image" src="https://user-images.githubusercontent.com/46675408/215657073-9c4987a1-d418-4f47-a98e-e0e42fb9d6fa.png">

이렇게 되면 $\sigma_1$, $\sigma_2$는 각 loss 1, 2의 상대적인 Weight가 되고, 마지막 항인 $log\sigma_1\sigma_2$는 regularization term이 된다.

분류 문제에 대해서는 scalar $\sigma$로 scale된 softmax로 확장시켜서 보자.
<img width="304" alt="image" src="https://user-images.githubusercontent.com/46675408/215657323-111469cb-108c-40b0-a991-8f4e378acb63.png">

이렇게 되면 log likelihood는 아래와 같은 꼴이 되고,
<img width="376" alt="image" src="https://user-images.githubusercontent.com/46675408/215657358-935f3fed-93cc-4028-bbf4-19722e72f407.png">

이는 다시 joint loss를 학습하는 모양이 된다. 
<img width="421" alt="image" src="https://user-images.githubusercontent.com/46675408/215657402-20df2c11-c00e-4c7f-b9d2-98b23951e4d2.png">

역시 여기서도 $\sigma_1$, $\sigma_2$가 모델의 상대적인 weight로 볼 수 있다.

### Result
<img width="861" alt="image" src="https://user-images.githubusercontent.com/46675408/215657662-2d77eb5f-2412-4207-8e8b-f6e97df8e5f5.png">

<img width="863" alt="image" src="https://user-images.githubusercontent.com/46675408/215657679-715a60ec-ab07-4932-a971-de186588a2ea.png">

