---
title: "[96] Vision GNN: An Image is Worth Graph of Nodes"
date: 2023-01-05
tags: ['backbone', '2022Q1', 'NeurIPS', 'graph']
paper: "https://arxiv.org/pdf/2206.00272.pdf"
issue: 105
issueUrl: "https://github.com/long8v/PTIR/issues/105"
---
<img width="1099" alt="image" src="https://user-images.githubusercontent.com/46675408/210682025-b056eb18-00e1-4259-ba5b-3cf8024b31e3.png">


[paper](https://arxiv.org/pdf/2206.00272.pdf), [code](https://github.com/huawei-noah/Efficient-AI-Backbones)

## TL;DR
- **I read this because.. :** NeurIPS2023
- **task :** image classification, object detection 
- **problem :** CNN은 sliding window를 하고 ViT는 image patch를 잘라서 sequential하게 넣는데 좀 더 유동적으로 보고 싶다 
- **idea :** image patch를 잘라서 이걸 node로 보고 GNN 
- **architecture :** multi-head max relative GCN + linear + BN + relu + linear + BN + FFN를 여러 층 쌓음.
- **baseline :** ResNet, CycleMLP, Swin-T
- **data :** ImageNet ILSVRC 2012, COCO2017
- **result :** tiny 모델과 비교했을 때 비슷한 flops로 sota
- **contribution :** first gnn model for image representation 
- **limitation / things I cannot understand :** ViT 대비 좋은 점을 잘 모르겠음 ;; 어차피 patch로 자르는건 똑같고 sequential하게 들어가도 연결성은 SA로 할 수 있을 것 같은데.. 크흠..

## Details
### motivation
<img width="700" alt="image" src="https://user-images.githubusercontent.com/46675408/210679374-e9d82a1c-0067-4495-914d-fa381c6a2694.png">

### Preliminaries 
- GNN in general
https://github.com/long8v/PTIR/issues/55

- over-smoothing problem
레이어가 깊어지면서 node 임베딩이 점점 비슷해지는 현상
<img width="300" alt="image" src="https://user-images.githubusercontent.com/46675408/210680797-6b7c216c-3ec8-4f93-add4-3230676ec9ce.png">

https://ydy8989.github.io/2021-03-03-GAT/


### Architecture
#### Graph Structure of Image
$H \times W \times 3$을 $N$개의 패치로 나눔.
각 패치를 feature vector $\mathrm{x}_i \in \mathbb{R}^D$로 표현하여 $X=[\mathrm{x}_1, \mathrm{x}_2, ... \mathrm{x}_N]$을 얻음
이 feature를 순서가 없는 node $\mathcal{V}={v_1, v_2, ... v_N}$으로 표현할 수 있음. 
각 node $v_i$에 대해서 K개의 가장 가까운 neighbors들 $\mathcal{N}(\mathcal{v}_i)$을 찾고 edge $e_ij$를 추가함. 
그러면 우리는 graph $\mathcal{G}=(\mathcal{V},\mathcal{E})$를 얻을 수 있고 여기에 GNN을 통과시키면 됨!
graph construction $\mathcal{G}=G(X)$라고 표기할 예정

- Graph로 표현하는 것의 장점
1) graph는 매우 일반화된 구조 표현! CNN의 grid나 ViT의 sequence는 그래프의 특정한 종류라고 볼 수 있음
2) 모양이 가변적인 복잡한 object를 표현하는데 grid나 sequence보다 그래프가 강점을 가질 수 있음
3) object는 part들의 조합(사람의 경우 머리 몸통 팔 다리)로 볼 수 있으므로 이러한 part를 조합하는데 더 강점을 가질 수 있음
4) 최신 GNN 아키텍쳐 활용 가능

#### Graph-level processing
<img width="800" alt="image" src="https://user-images.githubusercontent.com/46675408/210681975-18b87ece-2a46-4a2f-876c-7fb9a5809575.png">

feature $X \in \mathbb{R}^{n\times D}$로 시작해서 graph based feature $\mathcal{G}=G(X)$를 뽑음. 
graph convolutional layer는 neighbor node간 feature를 aggregate하면서 정보를 교환함
<img width="310" alt="image" src="https://user-images.githubusercontent.com/46675408/210683410-b7352cb4-f4ce-49e2-9e2e-812811a7c51d.png">

이를 좀더 구체적으로 쓰면 node $x_i$에 대해 neighbor 정보를 aggregate를 해서 $x_i'$을 만드는걸로 볼 수 있음.
우리는 max-relative graph convolution을 사용할 것임
<img width="500" alt="image" src="https://user-images.githubusercontent.com/46675408/210683965-f1c0e4ed-948e-480b-89dd-16c6a84c07b2.png">

aggregate할 때 feature의 차이에 max를 취해서 aggregate 하는 것 

여기에 multi-head operation을 쓰려고 함. feature diversity때문에 도입.
<img width="500" alt="image" src="https://user-images.githubusercontent.com/46675408/210683997-fb610ba7-39ed-4b60-ac38-3f3249c30ba5.png">

#### ViG block
이전의 GC의 경우 반복적으로 graph convolution layer를 진행하면서 node features간의 차이가 없어지고 성능 저하가 일어남.
<img width="300" alt="image" src="https://user-images.githubusercontent.com/46675408/210684153-86e386f4-c194-4daa-8c44-ea6895b247b4.png">

그래서 ViG block은 feature transformation과 nonlinear activation을 더 추가하려고 함.
GCN 레이어 이후에 linear layer를 넣고 nonlinear activation도 넣음. + FFN도 추가함
<img width="458" alt="image" src="https://user-images.githubusercontent.com/46675408/210684360-680debe1-04c4-4fc3-93f4-74cb5263855d.png">
<img width="288" alt="image" src="https://user-images.githubusercontent.com/46675408/210684375-5294eed7-1c6e-4352-89f1-b53cd20e1b3e.png">

이렇게 하니까 diversity가 ResGCN보다 좋았음. (위의 figure 3)

### Network Architecture
#### Isotropic architecture
ViT나 ResMLP처럼 feature가 모두 같은 size인 모델
<img width="728" alt="image" src="https://user-images.githubusercontent.com/46675408/210685336-bda52b8a-b1ae-4a22-bddf-68460887071c.png">

#### Pyamid architecture
ResNet이나 PVT처럼 feature가 점점 작아지는 형태

<img width="729" alt="image" src="https://user-images.githubusercontent.com/46675408/210685357-16d3d959-7c0d-4bcc-b82e-bd716926fa3f.png">

#### PE

<img width="153" alt="image" src="https://user-images.githubusercontent.com/46675408/210685406-67662806-49a2-4afa-afff-169eeda7ba7b.png">
absolute pe 더함 

### Result
#### Experiment detail
<img width="589" alt="image" src="https://user-images.githubusercontent.com/46675408/210685069-c8b21e02-f358-49f8-a0ad-d5e2fbe70149.png">

#### Result for isotropic
<img width="1024" alt="image" src="https://user-images.githubusercontent.com/46675408/210685144-3ed42751-6fcb-459c-b284-4762425cf1b6.png">

#### Result for Pyramid
<img width="807" alt="image" src="https://user-images.githubusercontent.com/46675408/210685202-2c1012f7-a2b2-4dd3-a6a6-ddc46843ccf2.png">

#### Object Detection result

<img width="728" alt="image" src="https://user-images.githubusercontent.com/46675408/210685561-3765fa9f-1a18-48ab-a6c6-9145fbaf741c.png">

### visualization
<img width="739" alt="image" src="https://user-images.githubusercontent.com/46675408/210685474-7d0b1eb7-ce50-4e00-8f0d-3a74dbe7ae63.png">


### etc


- max relative graph convolution

DeepGCNs: Can GCNs Go as Deep as CNNs? https://arxiv.org/pdf/1904.03751.pdf 에서 제안
ResNet이랑 비슷한 느낌의 논문인데, 위의 over-smoothing 현상 때문에 대부분의 GCN 모델들은 4레이어 이하였음
이를 해결하기 위해 GCN을 깊게 쌓으려면 어떻게 하면 되는가?를 주제로 한 논문
1) residual / dense connection 
<img width="506" alt="image" src="https://user-images.githubusercontent.com/46675408/211227213-99e1b5e6-16a7-4aed-bd61-505d56f78b73.png">

2) dilation
<img width="501" alt="image" src="https://user-images.githubusercontent.com/46675408/211227225-1b31b571-edbb-4405-ac54-ea8732038099.png">
