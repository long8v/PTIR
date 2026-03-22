---
title: "[46] ReFormer: The Relational Transformer for Image Captioning"
date: 2022-08-03
tags: ['SGG', '2021Q3', 'captioning']
paper: "https://arxiv.org/pdf/2107.14178.pdf"
issue: 52
issueUrl: "https://github.com/long8v/PTIR/issues/52"
---
![image](https://user-images.githubusercontent.com/46675408/182570807-e92c1bbb-479d-4301-9dff-88ba79cd624d.png)

[paper](https://arxiv.org/pdf/2107.14178.pdf)

## TL;DR
- **task :** image captioning and SGG
- **problem :** 이미지 내 scene graph를 활용해서 캡셔닝을 하면 도움이 되어서 외부 SGG + GCN을 활용해서 input으로 넣어준다. 그런데 (1) loss를 relation과 관련된 loss가 아니라 image captioning loss(=MLE)를 쓰는게 encoder를 충분히 학습시키지 못하고 (2) encoder만 따로 떼서 relation을 뽑을 수 있는 형태가 아니어서 범용성도 떨어지고 설명가능성도 떨어진다. 
- **idea :** 하나의 트랜스포머 모델로 image captioning과 scene graph generator 같이 하자!
- **architecture :** FasterRCNN으로 bbox 뽑고 Transformer encoder으로 self-attention 거친 output 으로 m(m-1) 해서 relation prediction 하고 transformer encoder의 L층의 hidden vector weighted sum해서 decoder로 넘겨주고 token prediction.
- **objective :** cross-entropy loss for SGG / MLE for captioning. 
- **baseline :** IMP, MOTIFS, VCTree(for SGG)
- **data :** COCO(image captioning), Visual Genome -> COCO랑 Visual Genome이랑 겹치는 이미지들도 있는데 아주 소수임.
- **result :** image captioning과 SGG 모두 SOTA
- **contribution :** SGG + captioning in one model!
- **limitation :** SGG도 sota인게 신기함.

## Details
### A Relational Encoding Learning Idea
![image](https://user-images.githubusercontent.com/46675408/182572329-7d286170-18a3-489d-8de4-8a9e7bcc729a.png)

보통의 captioning objective는 아래와 같음
![image](https://user-images.githubusercontent.com/46675408/182575885-10a20277-73a8-4aec-9b72-75e4274e1e9b.png)

y는 토큰들 $x$는 이미지의 visual feature.
captioning을 할 때 scene graph 정보를 넣어주기 위해서는 일단 image feature x를 어떤 pretrained SGG에 넣어서 그래프를 뽑고, 이 그래프를 GCN에 넣어서 잘 임베딩 한다음에 그 임베딩과 이미지 feature를 concat해서 captioning input에 넣어주는 형식으로 진행했음. 
이 때 objective가 SGG가 아니라 captioning에 걸리고, encoder가 정보 딱히 안뽑아도 decoder가 강하면 성능이 어느 정도 잘 나온다는 연구들이 있어서 이 encoder에서 relation을 잘 임베딩 뽑도록 학습되는지에 대한 의문이 듦

### Architecture
![image](https://user-images.githubusercontent.com/46675408/182586575-69233f0c-8481-4690-8989-0fe6b81d635b.png)

#### Encoder Architecture
Encoder의 경우 bbox 정보와 CNN에서 뽑은 결과, box label의 GloVe 벡터를 인풋으로 넣어주고 트랜스포머 인코더 태우고, m(m-1)쌍을 relation 벡터랑 concat해서 어떤 relation인지 softmax로 뽑았다.

#### Weighted Decoder for Image Captioning 
decoding할 때는 transformer의 모든 레이어의 output vector를 weighted sum한 것이 주어졌을 때 token prediction으로 바꾸었다. 
![image](https://user-images.githubusercontent.com/46675408/182587123-3f8624f7-a761-402b-a7ca-5228c8393064.png)

### Sequential Training with Inferred Labels
(i) Visual Genome에 대해 Faster RCNN 학습
(ii) Visual Genome에 대해 학습된 Faster RCNN을 가지고 Encoder 학습
(iii) encoder 학습 된 뒤, COCO dataset에 대해 encoder - caption decoder 같이 학습

caption loss와 SGG loss weighted sum 해봤다. ablation 해보니 caption loss만 건 것보다 성능이 안좋았다.
![image](https://user-images.githubusercontent.com/46675408/182588768-a249b6b6-65da-49ba-a4ba-5daab02bfae6.png)

### Results
#### SGG
![image](https://user-images.githubusercontent.com/46675408/182742322-9e0c93d4-0cff-45a8-9e3d-388bea856a24.png)

c.f. two-stage SGG 비교
Predicate classification(PredCLS) : given GT bbox and cls, predict predicates
Scene graph classification(SGCLS) : given GT bbox, predict predicates and object class
SGDet = SGGen인듯

|SGDet|R@20|R@50|R@100|
|--|--|--|--|
|Reformer(here)|25.4|**33.0**|37.2|
|Seq2Seq https://github.com/long8v/PTIR/issues/50|22.1|30.9|34.4|
|BGT-Net(GRU) https://github.com/long8v/PTIR/issues/51|**25.5**|32.8|**37.3**|
|RTN https://github.com/long8v/PTIR/issues/49|22.5|29.0|33.1|

|SGCls|R@20|R@50|R@100|
|--|--|--|--|
|Reformer(here)|36.6|40.1|41.1|
|Seq2Seq https://github.com/long8v/PTIR/issues/50|34.5|38.3|39.0|
|BGT-Net(GRU) https://github.com/long8v/PTIR/issues/51|41.7|**45.9**|**47.1**|
|RTN https://github.com/long8v/PTIR/issues/49|**43.8**|44.0|44.0|

#### Captioning
![image](https://user-images.githubusercontent.com/46675408/182742392-575d1547-255c-4f9a-b2f1-9be1723079c0.png)

#### Ablation for captioning
![image](https://user-images.githubusercontent.com/46675408/182742504-42e2361c-dfc4-4f74-8e68-b584a53a7c3d.png)
