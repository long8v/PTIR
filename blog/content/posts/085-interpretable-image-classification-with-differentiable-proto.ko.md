---
title: "[77] Interpretable Image Classification with Differentiable Prototype Assignment"
date: 2022-11-09
tags: ['2022Q3', 'ECCV', 'XAI']
paper: "https://arxiv.org/abs/2112.02902"
issue: 85
issueUrl: "https://github.com/long8v/PTIR/issues/85"
---
<img width="988" alt="image" src="https://user-images.githubusercontent.com/46675408/200740122-30475a8a-4f84-492d-a8c9-4fd306d15091.png">

[paper](https://arxiv.org/abs/2112.02902)

## TL;DR
- **task :** case-based reasoning 
- **problem :** 기존 ProtoPNet은 클래스 별로 prototype을 가정하고 있고 optimization이 여러 단계로 나누어져 있고 class을 결정할 때 prototype이 없는지를 보고 결정하기 때문에 prototype이 vague해진다. 
- **idea :** 1) 클래스 사이의 prototype을 share 할 수 있도록 하자 2) prototype이 class에 할당되는걸 미분가능하게 만들자 3) background 등이 prototype으로 만들어지지 않게 focal similarity function을 정의하자 
- **architecture :** ProtoPNet과 똑같이 생김. CNN => prototype과 focal similarity 구하고 => soft assign with gumbel softmax => pooling => classifier
- **objective :** CE loss(h 학습) + orthgonality loss
- **baseline :** ProtoPNet 
- **data :** CUB-200-2011, Standford Cars Data  
- **result :** SOTA, capture more salient features 
- **contribution :** reduce prototypes 
- **limitation or 이해 안되는 부분 :** fig 3이 정확히 이해는 안되네.. prototype pool은 공유할텐데 class 별로 slot이 따로 있고 그 prototype들로 분류가 되는건가.. 

## Details
### Preliminaries: ProtoPNet(prototypical part network)
[This Looks Like That: Deep Learning for Interpretable Image Recognition](https://arxiv.org/pdf/1806.10574.pdf)
이 이미지가 왜 이 클래스로 분류됐는가를 visualize 하고 싶음.
<img width="728" alt="image" src="https://user-images.githubusercontent.com/46675408/200739394-422cac33-6576-42f8-b2ae-4c8675c73e07.png">

이미지 x가 주어졌을 때 CNN으로 f(x)를 뽑고 CNN output으로 H x W x D가 나옴
동시에 m개의 prototype은 $H_1$ x $W_1$ x D shape을 가지는데 이 prototype은 H, W보다 작아야 함.
이때 D차원은 같은데 height, width가 작으므로 각 prototype이 CNN patch처럼 사용되어 activation map을 구할 수 있음

<img width="625" alt="image" src="https://user-images.githubusercontent.com/46675408/200739415-e5119553-d331-43e4-bf9d-08322ba2bd4e.png">

전체적인 ProtoPNet 구조는 위와 같음. 
학습은 3단계로 나누어지는데
(1) Stochastice gradient descent(SGD) of layers before last layer
prototype P와 convolution filter를 학습하는 loss. 마지막 분류 loss와 prototype과 convolution output 내의 patch들의 최소거리가 같은 클래스일 경우 가까워지도록, 다른 클래스일 경우 멀어지도록 학습함
<img width="719" alt="image" src="https://user-images.githubusercontent.com/46675408/200739532-7b8bcc35-7863-4af4-aecc-2b27d99a7c22.png">

(2) Projection of prototypes
prototype이 같은 클래스 내 가장 가까운 패치가 프로토타입이 되도록 할당함 
<img width="593" alt="image" src="https://user-images.githubusercontent.com/46675408/200739733-c74e70ff-2b28-43e1-9bc6-f4439fceee26.png">

(3) Convex optimization of last layer
prototype과 CNN은 freeze 시키고 h에 대한 matrix를 학습 
<img width="509" alt="image" src="https://user-images.githubusercontent.com/46675408/200739835-3338cbbf-aa87-4c24-b998-af62c3f8adb0.png">

- 모델이 분류를 하는 로직
<img width="1409" alt="image" src="https://user-images.githubusercontent.com/46675408/200740394-1db4df0d-993d-4208-b911-9707ae54e88c.png">

- CAM이나 part attention과 다른 점 
<img width="1240" alt="image" src="https://user-images.githubusercontent.com/46675408/200740420-2ae3cabb-d846-477b-8b6d-babc39844c1f.png">

### motivation 
<img width="1030" alt="image" src="https://user-images.githubusercontent.com/46675408/200740577-979ed099-14df-42e3-8b8e-3cf94729d3f1.png">

### Architecture
<img width="1026" alt="image" src="https://user-images.githubusercontent.com/46675408/200740957-d76b21d0-d130-4427-bb9c-ae06739c80a9.png">

각 class들은 K개의 slot을 가지고 있어서 거기에 shared prototype을 할당할 수 있음

이미지 x가 주어졌을 때 CNN(=f(x))으로 output H x W x D를 뽑음
이는 D 차원의 벡터가 H x W개 있는 것으로 해석 할 수 있음. 그 D차원의 벡터를 k번째 slot에 대해 유사도를 구해서 할당할 수 있음

#### Focal similarity 
ProtoPNet과 같은 이전 연구들은 유사도를 아래와 같이 구했음 
<img width="308" alt="image" src="https://user-images.githubusercontent.com/46675408/200741464-c7890e76-2704-4609-8d91-3f1fee9dfb71.png">

<img width="253" alt="image" src="https://user-images.githubusercontent.com/46675408/200741575-5927fd74-2677-43cd-8a05-f0cc9f07abfe.png">

근데 이렇게 들어가면 (1) f(x)의 patch들인 z가 모두 prototype으로 유사하도록, 즉 background에만 집중하도록 될 수 있고 (2) 이미지에서 activated된 요소에만 gradient가 가는 효과가 있음. 이를 방지하기 위해 focal similiarity를 제안함 
<img width="483" alt="image" src="https://user-images.githubusercontent.com/46675408/200741686-95d91487-6bcf-48e6-92e9-8ee9619dad6b.png">

<img width="1008" alt="image" src="https://user-images.githubusercontent.com/46675408/200742058-0a90fc04-f110-4287-8cbe-95ae40722386.png">

#### Assigning one prototype per slot
prototype을 hard하게 assign하지 않고 soft하게 주고 gradient가 흐를 수 있게 하도록 gumbel-softmax로 구함

<img width="583" alt="image" src="https://user-images.githubusercontent.com/46675408/200743507-eb892c51-d77f-4694-8ba8-0a13273557e4.png">

이때 한 slot에 여러 prototype이 들어가지 않도록 loss를 추가적으로 줌
<img width="393" alt="image" src="https://user-images.githubusercontent.com/46675408/200742122-810671f0-bc43-43a1-9d95-8b8e27685e11.png">
