---
title: "[83] Variance Networks: When Expectation Does Not Meet Your Expectations"
date: 2022-11-25
tags: ['2018', 'ICLR', 'uncertainty', 'later..', 'bayesian']
paper: "https://arxiv.org/abs/1803.03764"
issue: 92
issueUrl: "https://github.com/long8v/PTIR/issues/92"
---
<img width="1020" alt="image" src="https://user-images.githubusercontent.com/46675408/203890454-09882ec3-c607-476c-bac2-2bd428cf0bb1.png">

[paper](https://arxiv.org/abs/1803.03764)

## TL;DR
- **task :** stochastic DNN => image classification, reinforcement learning, adversarial example
- **idea :** 평균이 아니라 분산만 학습되는 stochastic layer를 만들어볼까?
- **architecture :** LeNet-5-Caffe
- **objective :**  각 태스크에 맞는 objective
- **baseline :**VGG-like architecture, Deterministic Policy
- **data :** CIFAR-10, CIFAR-100
- **result :** ? 
- **contribution :** ?
- **limitation or 이해 안되는 부분 :** 나중에 시간 많을 때 다시 읽어야지

## Details
### DNN in stochastic setting
- stochastic layer, stochastic optimization texhinques 등의 방법이 있음
- reduce overfitting, estimate uncertainty, more efficient exploration for reinforcement learning에 쓰임 
- stochastic model을 학습하는건 일종의 Bayesian model로 해석이 가능하다
- 그 중에 한 가지 방법은 deterministic weight $w_{ij}$를 $\hat w_{ij} \sim q(\hat w_{ij}|\phi_{ij})$로 바꾸는 것이다. 그럼 학습 중에는 이 weight에 대한 single point estimation이 아니라 weight의 분포에 대해 학습을 하는 형태이다.
- 그러나 test에는 결국 이 weight의 분포에 대한 평균을 내서 쓰고, 이 과정에서 "mean propagation", "weight scaling rule"같은 것들이 쓰인다.

### Stochastic Neural Network
DNN은 결국 object x와 weights W가 주어졌을 때 target T를 예측하는 것. 
여기서 stochastic neural network 중 weight W가 parametric distribution $q(W|\phi)$로부터 sampling되는 모델을 상정해보자.
학습을 진행하면서 $\phi$가 training data (X, T)에 의해 학습되고 regularization term $R(\phi)$도 추가 된다. 즉 아래와 같이 쓸 수 있다. 
<img width="488" alt="image" src="https://user-images.githubusercontent.com/46675408/203891750-81f1df66-e643-4848-871d-f877d127520a.png">
이 모델을 학습하는 과정에서는 binary dropout, variational dropout, dropout-connection 같은 기법이 쓰이는데, 여기서 정확한 $E_{q(W|\phi)}p(t|x,W)$를 구하는 것이 보통 intractable하다. 그래서 보통 K개의 sample을 뽑아서 평균을 내는 방식으로 근사하는데 이를 "test-time averaing"이라고 한다.
<img width="762" alt="image" src="https://user-images.githubusercontent.com/46675408/203891763-5dc136b6-44cb-4868-9aaa-f2319c55bd7f.png">
조금더 효율적으로 계산하기 위해서 $\hat W_k$가 아니라 $E_qW$를 구하는 식으로 하는데 이를 "weight scaling rule"이라고 한다.
<img width="391" alt="image" src="https://user-images.githubusercontent.com/46675408/203891773-6112d056-8f91-4bf2-8083-864ce555f8fb.png">
여기서 본 논문에서는 $E_qW=0$인 레이어를 상정하려고 하는데, 그렇게 되면 p(t|x, EW=0)이므로 매번 weight scaling rule을 쓰면 random guess하는 꼴이 된다(그래서 얘네는 weight scaling rule을 안쓰겠지?). 평균값에는 정보가 없고 분산에만 정보가 저장되므로 이러한 레이어를 "variance layers"로 하고 "variance network"로 정의하고자 한다.

### Variance Layer
activation되는게 $\mu_{ij}$에는 의존하지 않고 variance에만 의존하여 된다.
<img width="755" alt="image" src="https://user-images.githubusercontent.com/46675408/203892552-bd1a0006-ecd3-4b1e-a3d3-bb691e95794a.png">

### Result
classification / reinforcement learning / adversarial example에서 좋은 결과 
<img width="505" alt="image" src="https://user-images.githubusercontent.com/46675408/203892704-b40111c4-040e-41b0-90f2-44c5c076696c.png">
<img width="416" alt="image" src="https://user-images.githubusercontent.com/46675408/203892717-fdd8c58c-7dfe-40f5-9837-f8ca98e89c7f.png">
<img width="426" alt="image" src="https://user-images.githubusercontent.com/46675408/203892728-9d240e17-182c-478e-be50-b7b0ad69f7be.png">
