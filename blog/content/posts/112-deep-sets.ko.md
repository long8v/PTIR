---
title: "[103] Deep Sets"
date: 2023-03-20
tags: ['NeurIPS', '2017']
paper: "https://arxiv.org/pdf/1703.06114.pdf"
issue: 112
issueUrl: "https://github.com/long8v/PTIR/issues/112"
---
<img width="661" alt="image" src="https://user-images.githubusercontent.com/46675408/226218804-5a30ac66-5794-4a12-b862-6d9aae85dbef.png">

[paper](https://arxiv.org/pdf/1703.06114.pdf)

## TL;DR
- **I read this because.. :** https://github.com/long8v/PTIR/issues/82 이랑 다른 논문에서 언급되는걸 종종 봄. 두 단어 제목 간지
- **task :** input이나 output이 순서와 상관없는 set인 task들. 1) 모수의 분포 parameter 추정 2) 숫자들 나열하고 총합 구하기 3) point cloud classification 4) 어떤 단어 set의 concept / cluster와 가까운 단어들 찾기 5) 이미지와 관련된 tag들을 모두 찾기 
- **problem :** permutation invariant task들을 푸는 deep network가 가져야 하는 특성이 뭐가 있는지 알아보자.
- **architecture :** $f(x)=\sigma(\lambda I \mathbf{x} + \gamma \text{maxpool}(\mathbf{x})1)$
- **result :** 하나의 arch로 각각 특성화된 모델과 유사하거나 더 나은 성능
- **contribution :** set input output에 대한 이론적 특성 분석, 다양한 application에서 성능 확인
- **limitation / things I cannot understand :** 

## Details
### Permutation Invariance and Equivarnce
**Problem Definition**

function f는 set의 순서와 상관없이 permutaion invariant해야 한다.

<img width="279" alt="image" src="https://user-images.githubusercontent.com/46675408/226219598-2bc457f8-655e-4c9d-9c8e-820c07b0eb99.png">

- $\pi$ : permutation

**Structure**

set $X$를 받는 function f(X)는 아래와 같은 form으로 decompose될 때 pemutation invariant하다
<img width="105" alt="image" src="https://user-images.githubusercontent.com/46675408/226221330-995fb348-634a-48c3-b5ef-50576852ea70.png">

어떤 function $f_\theta : \mathbb{R}^M \rightarrow \mathbb{R}^M$일 때,
- $\sigma$ : nonlinearity function
- $\theta \in \mathbb{R}^{M\times M}$
$f_\theta(\mathbf{x})=\sigma(\theta\mathbf{x})$ 일 때, $\theta$의 대각선 요소가 같고 대각선 요소가 아닌 것들이 tie되어 있을 때 permutation equivarant 하다. 
<img width="597" alt="image" src="https://user-images.githubusercontent.com/46675408/226221400-0674052a-a274-4884-9535-a6ec40b5da9c.png">

수식 보니까 그냥 diagonal 만 빼고 다 같은 값이고 diagnoal 끼리도 다 같으면 되는듯
lambda * torch.eyes(5) + gamma * torch.ones(5,5)

$\mathbf{x}$까지 넣으면
$f(x)=\lambda Ix \mathbf{(11^T)x})$
input Ix와 x의 summation에다가 nonlinearity 취한게 permutation invariant하다(summation이 permutation과 상관없으니)

### Deep Sets
위에서 정리한 특성들을 univeral approximator로 바꾸면 된다. 즉, $\phi$와 $\rho$를 polynomial로 근사하면 된다 
즉 1) 각각의 instance $x_m$은 어떤 표현 $\phi(x_m)$으로 바뀌고 2) 그 표현들은 $\rho$ network에 따라 처리된 뒤 더해지게 된다.
어떤 메타정보 $z$가 있을 경우 위의 네트워크들이 condition이 있는 mapping $\phi(x_m|z)$로 표현되게 된다.

**Equivariant model**
<img width="125" alt="image" src="https://user-images.githubusercontent.com/46675408/226222009-7e3e7ba0-5e68-467a-8cc2-4659ee0bb339.png">


이를 다른 연산으로 치환하면 아래와 같이할 수 있는데,

<img width="237" alt="image" src="https://user-images.githubusercontent.com/46675408/226221930-4e3a1b7d-dbdd-4be5-8883-7a40bea5c1c5.png">

max-pool이 sum과 비슷하게 교환법칙이 성립하기 때문이다. 실제 적용해봤을 때 sum보다 Max연산이 더 성능이 좋았다. 

### Applications and Empirical Results
- 정규분포 난수를 보여주고 모수 통계 추정
<img width="749" alt="image" src="https://user-images.githubusercontent.com/46675408/226503764-0aca5e4d-bf48-4b1f-a022-31783e8c8da7.png">

- 숫자들 나열 보여주고 summation 구하라 함
text / mnist 이미지
<img width="373" alt="image" src="https://user-images.githubusercontent.com/46675408/226503814-0fb31e45-c747-4af2-8f21-a338b07c7ffe.png">

학습할 때는 최대 10개 보여주고 test 시에는 100개까지 보여줌
Deep Set이 RNN 계열과 달리 일반화가 잘됨

- point cloud classification
<img width="379" alt="image" src="https://user-images.githubusercontent.com/46675408/226503995-fd502f23-216e-463c-9aac-80142b99e874.png">

LiDAR에서 측정되는 point들은 순서가 딱히 없음. 

- text set expansion
cheetah, tiger가 주어졌을 때 비슷한 concept을 가진 puma를 뽑는 태스크. unsupervised
<img width="744" alt="image" src="https://user-images.githubusercontent.com/46675408/226504270-af1e67a9-bba1-4ae9-9fbd-30a0c34d95f2.png">

- image tagging
특정 이미지에 해당하는 텍스트 태그들을 모두 달기
학습할 때는 태그들 몇개를 주고 나머지 태그들을 예측하라고 하고 테스트 시에는 이미지만 주고 태그들을 예측하도록 했음
각 요소(이미지와 태그)를 인코딩 하는 네트워크 하나, 그 요소들의 합을 통해 set의 점수를 구하는 네트워크가 하나 있음.
-> 그러면 모든 set의 조합의 score를 구해서 best를 뽑은건가? 모르겠음
<img width="304" alt="image" src="https://user-images.githubusercontent.com/46675408/226504360-4fbbfd79-24ab-4818-a221-e54191d8ce19.png">

- anomaly detection
CelebA에 이미지와 그 이미지에 해당하는 tag들이 달려있는데 태그별로 이미지 모아놓고 한개만 다른 그룹에서 이미지 뽑음.
이미지 시퀀스를 받고 마지막 softmax 레이어에서 몇번째가 잘못된 이미지인지 예측하도록 함.
Deep sets을 쓰면 test의 70%를 맞췄는데 FCN을 쓴 basline은 random guess 수준의 성능.
<img width="755" alt="image" src="https://user-images.githubusercontent.com/46675408/226504493-cf2812fc-f630-418a-9bbd-55ef1a2b8198.png">


- 후속연구?
http://proceedings.mlr.press/v97/lee19d/lee19d.pdf
pooling 대신에 attention 연산으로!

