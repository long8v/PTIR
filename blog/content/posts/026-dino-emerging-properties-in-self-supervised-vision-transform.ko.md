---
title: "[24] DINO: Emerging Properties in Self-Supervised Vision Transformers"
date: 2022-04-26
tags: ['ViT', 'SSL', '2021Q2', 'facebook']
paper: "https://arxiv.org/pdf/2104.14294.pdf"
issue: 26
issueUrl: "https://github.com/long8v/PTIR/issues/26"
---
<img width="788" alt="image" src="https://user-images.githubusercontent.com/46675408/165205620-c23a58ca-a094-4012-84e2-cf98cff09faf.png">

[paper](https://arxiv.org/pdf/2104.14294.pdf) [code](https://github.com/facebookresearch/dino)

## Abstract 
SSL을 convnet에서 하는것과 달리 ViT에 하면 다른 특성이 있지 않을까? 
1) self-supervised ViT feature는 supervised나 convnet과 달리 이미지의 semantic segmentation에 대한 explicit한 정보를 가지고 있다.
<img width="1022" alt="image" src="https://user-images.githubusercontent.com/46675408/165208051-5b500bd3-2c0d-4727-9275-f42e306dfad6.png">

2) 이러한 feature들은 kNN 분류를 위한 훌륭한 피쳐여서, 작은 ViT에서도 ImageNet top-1 78.3%의 정확도를 달성했다.


우리는 또한 1) momentum encoder* 2) multi-crop training 3) small patches with ViT의 사용의 중요성을 밝혀냈고, 이러한 발견을 바탕으로 DINO(self-distillation with no labels)를 제안한다. DINO + ViT linear evaluation을 했을 때, ImageNet top-1 80.1%의 정확도를 달성했다.
*MoCo : Momentum contrast for unsupervised visual representation learning. 그냥 teacher network가 업데이트 된다는 뜻임.


## Introduction
ViT가 convnet에 대응할만한 성능을 냈지만, 장점이 명확하지 않았다: 더 많은 계산을 필요로 하고, 더 많은 학습 데이터를 필요로 하며, ViT의 피쳐들이 특수한 속성을가지고 있지 않았다. 우리는 이 논문에서 비전에서의 Transformer의 성공은 supervision이 있는 학습이 아닌, NLP 처럼 self-supervised 학습에 있는 것을 보이고 싶다. 
비전에서 SSL 방법은 대개 비슷한 구조를 가지고 있으나, trivial solution(=collapse)를 피하거나 성능을 늘리기 위해 조금씩 다른 요소를 가지고 있다. 우리는 이러한 연구들을 ViT feature에 적용해보려고 한다. 
<img width="373" alt="image" src="https://user-images.githubusercontent.com/46675408/165209334-21883bd0-8513-450e-938c-8f0f2e7abdc9.png">


적용 후 abstract에서 설명한 특성들을 발견했고, 이를 기반으로 DINO를 제안한다. DINO는 momentum encoder을 포함한 네트워크로 teacher network의 output을 바로 예측하고 일반적인 크로스 엔트로피로 학습된다. DINO는 teacher output을 centering / sharpening만 해도 일반적으로 잘 작동했는데, 이는 다른 네트워크들이 predictor, advanced norm, contrastive loss를 쓰는 것과 달리 매우 간단하고 유동적이다. 
DINO와 small patch ViT를 결합한 여러가지 실험들을 해봤고, GPU 자원이 얼마나 풍족한지에 따라 다양한 실험을 해봤다.

## Approach
### SSL with Knowledge Distillation 
<img width="555" alt="image" src="https://user-images.githubusercontent.com/46675408/165217019-2afa8065-b9c1-4476-9610-46d07249c2ae.png">

DINO는 최신 SSL의 전체적인 구조를 따라가며, 또 knowledge distillation(KD)와도 유사한 점이 있다. 
KD는 teach network의 output이 주어졌을 때, student network의 output이 이를 따라가도록 학습하는 방식이다. input image x가 주어졌을 때, K 차원의 output 확률인 P_s는 softmax를 통해 normalization이 된다. 
<img width="439" alt="image" src="https://user-images.githubusercontent.com/46675408/165211594-19e42968-0766-4cd3-a912-8757952317d7.png">

이때 temperature 파라미터인 \tau_s는 output distribution의 sharpness를 결정한다. teacher network가 주어졌을 때, 우리는 student network에 대해 cross entropy 를 최소화하는 방향으로 학습된다. 
<img width="488" alt="image" src="https://user-images.githubusercontent.com/46675408/165212527-c4a76837-c327-4f66-b1f3-2173f5ba7f49.png">

우리는 이 loss를 SSL로 옮겨가는 과정을 보일 것이다. 첫째로, multi-crop 접근을 통해 distorted view 또는 crop 형태로 V개의 다른 이미지 셋를 만든다. 이 이미지 셋은 두개의 global view(전체 이미지)를 가지고 있고 많은 저 차원의 local view 이미지를 가지고 있다. 크롭된 이미지들은 student 네트워크를 학습하고, global view는 teacher를 통과시킨 뒤, "local-to-global" correspondence를 이루도록 한다. 즉 우리의 loss는 다시 쓰면, 
<img width="477" alt="image" src="https://user-images.githubusercontent.com/46675408/165213145-5dc46003-e4ba-4f9e-8d52-c46a355e8b50.png">

이때의 V의 개수는 몇개여도 상관없으며 2여도 된다. 우리는 이미지의 50%이상을 차지하는 224 x 224 사이즈의 global view와 96 x 96 사이즈의 local view를 정의했다. 두 네트워크는 같은 구조이나 파라미터는 다르며, student network의 파라미터만 SGD로 학습된다.

### Teacher Network 
KD와 달리 우리는 사적지식이 없으므로 teacher를 가지고 있지 않다. 그러므로 과거의 student network를 통해 배운다. 우리는 teacher network를 업데이트 하는 방법을 여러가지 실험해보았는데 epoch 동안 freeze하는게 성능이 놀랍게도 좋았다. 우리는 exponential moving average(EMA)를 사용하였다. (like #25 ) 
<img width="200" alt="image" src="https://user-images.githubusercontent.com/46675408/165214132-03a1a7fa-807d-44c5-a6e7-f6f48a26bff4.png">

이때 \lambda는 0.996에서 cosine으로 1까지 올라가도록 스케쥴했다. 이런 EMA 방법론은 Polyak-Ruppert Averaging(?) 처럼 앙상블하는 효과가 있었다. 

### Network architecture
NN g는 backbone인 f(ViT나 ResNet)과 projection head(h)로 이루어져있다. downstream task에 쓰이는 feature는 backbone f의 output이다. h는 3층의 MLP이고 hid_dim은 2048, l2 norm으로 이루어져있다. (SwAV와 같은 구조라고 함) ViT는 batch norm을 어디에도 사용하지 않았다. 

### Avoiding collapse.
SSL 방법론들은 collapse를 피하기 위해 다양한 방식을 취한다. DINO 역시 norm들을 통해 안정화시킬 수 있으나, teacher output의 momentum을 centering + sharpening하는 것만으로도 model collapse를 막을 수 있었다. centering은 한 차원이 dominate해지는 것을 막으며, uniform distribution으로 collapse하는 것을 장려하며, sharpening은 반대의 역할을 한다. 두 operation을 같이 하면, collapse를 막으며 균형을 맞출 수 있다.
<img width="174" alt="image" src="https://user-images.githubusercontent.com/46675408/165216641-48b1ebb1-d0ff-4938-adc0-2b98c3b30ec1.png">
centering은 teacher에 bias term c를 추가하는 걸로 해석할 수 있다. center c는 EMA와 함께 학습된다. 

<img width="387" alt="image" src="https://user-images.githubusercontent.com/46675408/165216708-318b0c44-d940-4312-bd6b-c5baa7a0b6d6.png">

## Result
### Main Result 
<img width="441" alt="image" src="https://user-images.githubusercontent.com/46675408/165216986-23c05bc9-41ba-45b0-9fbb-9565cf54437c.png">

- BYOL, MoCov2, SwAV 이김.
- DINO에 ViT를 적용했을 때, linear probing한 결과나 KNN만 한거나 거의 비슷한데(74.5 vs 77.0) 이는 DINO + Convnet에서는 나타나지 않은 현상으로 ViT 아키텍쳐의 특징이라고 할 수 있다. 
- patch size를 16으로 하는 것보다 8로 하는게 성능이 가장 좋았다. 

### Properties of ViT trained with SSL
nearest neighbor search, object location에 관련된 정보를 담고 있는지, 다른 다운스트림 태스크에 대한 transferability에 대해 DINO feature의 성질들을 평가해보았다.  
- image retrieval 
query, image가 주어졌을 때 이미지 retrieval하는 task
<img width="540" alt="image" src="https://user-images.githubusercontent.com/46675408/165217962-9a9b2fce-b46d-4551-9292-2377af9c6110.png">

- copy detection  
blur, insertion, print and scan으로 뭉개진 이미지를 recognize하는 task. 
<img width="543" alt="image" src="https://user-images.githubusercontent.com/46675408/165217986-cf728db3-2ecd-4d05-b68a-389392b28c5f.png">

- segmentation
<img width="466" alt="image" src="https://user-images.githubusercontent.com/46675408/165218514-9bf03ac5-896d-401f-85aa-347da6435031.png">

각 ViT/s 를 DINO로 학습한 모델에 대해 last layer에 각 head들의 `[cls]` 토큰의 self-attention을 시각화하니 아래와 같이 segmentation 정보를 가지고 있음.
<img width="461" alt="image" src="https://user-images.githubusercontent.com/46675408/165218490-52a5c7b5-d321-4f17-944d-ffcb78968dec.png">
 
supervision ViT으로 학습한 것보다 DINO가 더 segmentation 성능이 좋음. 아래는 self attention map에서 상위 60%만 남긴것
<img width="561" alt="image" src="https://user-images.githubusercontent.com/46675408/165218277-63ad721d-2e6b-46cd-8194-54fcdece26b8.png">

- transfer learning 
<img width="525" alt="image" src="https://user-images.githubusercontent.com/46675408/165218241-2d7630a9-96b2-477a-af1d-fb0252cc2abe.png">

## Ablation 
### Importance of components
<img width="454" alt="image" src="https://user-images.githubusercontent.com/46675408/165219492-d4598c8a-b8ca-451e-a45c-968f5f5a4cc2.png">


### Effect of patch size
<img width="452" alt="image" src="https://user-images.githubusercontent.com/46675408/165219463-c3dfb085-8daa-4386-b513-2bc16502d044.png">

패치사이즈가 작아지면 파라미터는 그대로지만 throughput은 늘어난다. 패치사이즈는 작을 수록 성능이 좋았다.

### Analyzing training dynamic
<img width="436" alt="image" src="https://user-images.githubusercontent.com/46675408/165219434-47c15262-57a2-4a1d-8093-c39c72993efc.png">

### Avoiding Collapse
<img width="426" alt="image" src="https://user-images.githubusercontent.com/46675408/165219184-2834b4c7-da14-4fa7-b3dd-95ed06264abc.png">

Cross Entropy를 KL divergence와 엔트로피 두개의 term으로 나누어 그래프를 그려보았다. sharpening, centering 둘 중 하나라도 없으면 KL divergence가 0으로 간다. 즉 항상 constant한 output이 나온다는 뜻이므로, collapse가 발생한다,
반면에 entropy는 sharpening만 했을땐 0으로 수렴하고, centering만 했을땐 -log(1/K)로 수렴하는데 이는 둘이 다른 방향의 collapse를 한다는 뜻을 의미한다. 즉 두개의 연산이 서로 균형을 맞추어야 한다.

<img width="418" alt="image" src="https://user-images.githubusercontent.com/46675408/165218923-15242e35-1325-4a98-855f-6fc4e3772928.png">

