---
title: "[53] InfoGAN: Interpretable Representation Learning by Information Maximizing Generative Adversarial Nets"
date: 2022-08-20
tags: ['openAI', '2016', 'fundamental', 'generative']
paper: "https://arxiv.org/abs/1606.03657"
issue: 59
issueUrl: "https://github.com/long8v/PTIR/issues/59"
---
<img width="834" alt="image" src="https://user-images.githubusercontent.com/46675408/185729655-502f78c2-cd8e-4b1d-b6f7-ca84cfb26737.png">

[paper](https://arxiv.org/abs/1606.03657)

## TL;DR
- **task :** unsupervised learning 
- **problem :** unsupervised manner로 representation learning을 하고 싶은데, 이 때 중요한 특성들(숫자, 눈의 색)을 disentangle을 하고 싶다. generative model의 경우 완벽한 생성을 하지만 representation은 엉망인 경우가 많다. 
- **idea :** 어떤 structured latent variable $c$와 generator distribution $G(z, c)$의 mutual information(=MI)이 높도록 loss에 추가. MI는 ELBO처럼 lower bound가 생기고 이때 posterior는 neural network로 근사함.
- **architecture :** generative model은 DCGAN, CNN을 share하는데 위에 FCN 하나 더 붙여서 $Q(c|x)$가 나오도록 함.
- **objective :** GAN loss - mutual information loss
- **baseline :** vanilla GAN
- **data :** MNIST, DC-IGN, Street View House Number(SVHN), CelebA
- **result :** code를 바꿔가면 생성물도 해석가능하게 바뀌는것을 확인. 그냥 GAN을 c에 대해 학습하도록 하면 mutual information이 InfoGAN만큼 최대화되지는 않음. 
- **contribution :** GAN with interpretable latent vector! 
- **limitation or 이해 안되는 부분 :**
> 1. category c를 넣어줄 때 랜덤으로 하는데  어떻게 하나의 인덱스가 하나의 digit과 관련을 가질 수 있는걸까? 예를 들어서 1 이미지 들어왔을 때 c가 3번일때도 5번일때도 똑같이 그걸 복원하고, 반대로 1이 들어올 떄나 2가 들어올때나 c가 5번일수도 있잖슴.. 어쨌든 c를 고려한 generation이 되면서 가능한건가?

-> GAN이라 이미지가 '1'로 들어갔다는건 없음!  즉, VAE 처럼 Reconstruct하는게 아니라 주어진 이미지가 fake인지 real인지 구분하면서 학습되는거임! 그러므로 어떤 latent code c가 3으로 들어갔으면 3같은 그림이 나오도록 mutual information을 넣어주는 듯. 즉 걱정하는 상황은 없는듯. 

> 2. c로 들어가는 category와 continuous의 개수를 정할수는 있지만 애초에 각각이 뭘 배울지는 정할 수 없는거 아닌가?? 왜 정할 수 있는것처럼 해놨지?? 사후적으로 알게되는게 아닌지.…

-> 정할 수 없는게 맞는듯. 결과론적으로 해석했을 때 우리가 생각하는 feature들을 code들이 잘 담고 있다고 썰을 푼거 인듯.

## Details
### mutual information
<img width="384" alt="image" src="https://user-images.githubusercontent.com/46675408/185787557-74f38e2c-176f-4810-95a6-05a05d6e812a.png">

X와 Y가 독립이어서 $P_{X,Y}(x,y)=P_X(x)P_Y(y)$면, 
<img width="410" alt="image" src="https://user-images.githubusercontent.com/46675408/185787349-d01a4bc2-f105-40f1-8a4c-33d06971e3fd.png">

엔트로피에 대한 식으로 쓰면
<img width="529" alt="image" src="https://user-images.githubusercontent.com/46675408/185787340-e72cb18d-a088-4750-b335-314a9006a4a9.png">


### Variatitonal Mutual Information Maximization
<img width="779" alt="image" src="https://user-images.githubusercontent.com/46675408/185787402-648ef165-f596-4f86-871d-3b0041e277b2.png">

여기서 posterior Q에 대해 sample을 뽑아야 하는 부분이 있는데 아래 lemma를 통해 sample도 안해도 됨.

<img width="887" alt="image" src="https://user-images.githubusercontent.com/46675408/185787485-587b5579-552a-452a-85e6-743e4907643d.png">

해석하자면 어떤 함수 f(x, y)를 x와 x가 주어졌을 때의 y에 대해 기대값을 구하면 x와 x가 주어졌을때 y와, x'(y가 주어졌을 때의 x)에 대해 f(x' y)기대값을 구한 것과 같다.

우리의 lower bound는 아래와 같이 정의됨
<img width="606" alt="image" src="https://user-images.githubusercontent.com/46675408/185787503-05b27562-e5ed-4b2e-b7f1-845a85c5fdae.png">

최종적인 loss는 GAN loss에 mutual information lower bound를 뺀 것! (MI는 높을 수록 좋음)
<img width="518" alt="image" src="https://user-images.githubusercontent.com/46675408/185787518-4dde4981-eb61-4a18-ac40-58dfd21c1889.png">
