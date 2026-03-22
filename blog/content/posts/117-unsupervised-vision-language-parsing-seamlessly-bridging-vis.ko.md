---
title: "[108] Unsupervised Vision-Language Parsing: Seamlessly Bridging Visual Scene Graphs with Language Structures via Dependency Relationships"
date: 2023-04-04
tags: ['2022Q1', 'dataset', 'CVPR', 'graph']
paper: "https://arxiv.org/abs/2203.14260"
issue: 117
issueUrl: "https://github.com/long8v/PTIR/issues/117"
---
<img width="674" alt="image" src="https://user-images.githubusercontent.com/46675408/229678142-edfc0956-350f-4961-9400-2a71a1979c22.png">

[paper](https://arxiv.org/abs/2203.14260), [code](https://github.com/LouChao98/VLGAE)

## TL;DR
- **I read this because.. :** SG로 또 뭐 할 수 있을까? SG annotation은 한계가 있다. caption 또는 image - text pair에서 scene graph parsing 할 수 있을까?
- **task :** (proposed) 이미지와 caption이 주어졌을 때 caption에 대한 dependancy tree 만들고 tree내 object에 대한 bbox 까지 예측
- **idea :** encoder - decoder 형태
- **architecture :** text는 word embedding + pos embedidng concat하고 image는 object 먼저 뽑은 다음에 attribtue / relation 예측하게 한 뒤에 attention 해서 context encoding 만듦. context encoding을 받고 parse tree와 tag sequence를 생성. 
- **objective :** MLE로 EM + contrastive loss(각 node의 표현과 image I가 positive인지 negative인지)
- **baseline :** DMV(dependancy structure induction), MAF(Visual Grounding)
- **data :** (proposed) VLParse
- **evaluation :** Directed / Undirected Dependency Accuracy(DDA/UDA), Zero-Order Alignment Accuracy(caption 내 "a table"이 bbox로 잘 매칭되었는지?, IoU + attribute 까지 맞춰야), First/Second-Order Alignment Accuracy(first는 caption내 text가 맞으면 되고 second는 caption text랑 연결된 object bbox의 관계까지 맞는지=zero + first 합친거)
- **result :** Language Structure Induction / Evaluation on Visual Phrase Grounding task랑 비교했을 때 성능 더 좋음
- **contribution :** 새로운 데이터셋 / 베이스라인 제안
- **limitation / things I cannot understand :** decoder 아키텍쳐를 뭘로 썼다는건지.. 
 
## Details
<img width="634" alt="image" src="https://user-images.githubusercontent.com/46675408/229679674-7554c4c0-25d8-4faf-b316-45610d2c70ed.png">

introduction에 있는 그림인데 실제로는 Scene Graph를 생성하지는 않음. 그냥 데이터 만들 때 scene graph 데이터를 활용하긴 함

### proposed data: `VLParse`
<img width="630" alt="image" src="https://user-images.githubusercontent.com/46675408/229679768-cba2c477-6c2e-4bad-a65b-c2d0218dbbfa.png">

<img width="604" alt="image" src="https://user-images.githubusercontent.com/46675408/229679812-9ce154e0-806d-4fda-a332-cea676616fe3.png">

휴리스틱 + human refinement로 만듦

## proposed task: Unsupervised Vision-Language Parsing

input : image $\mathbf{I}$, sentence $\mathbf{w} = {w_1, w_2, ... w_N}$
output : parse tree $\mathbf{pt}$. 각 object는 box region도 예측해야함. 이 논문에서는 faster rcnn으로 candidates들 뽑고 mapping 시킴.

<img width="1245" alt="image" src="https://user-images.githubusercontent.com/46675408/229680304-361d43e5-2fa0-498a-b577-1df74b47eb36.png">

### architecture
 **Feature Extraction**
- Visual Feature
  - Faster RCNN -> RoI -> $\\{ V_i^o \\}^M_{i=1}$는 node `OBJECT`의 feature
  - 각각의 `OBJECT` node는 `ATTRIBUTE`라는 tag가 붙음. 이는 $v_i^a= MLP(v_i^o)$로 만들어짐
  - 두개의 `OBJECT`에 대해서 우리는 $RELATIONSHIP$이라는 zero-order node 추가 $v^img_{i->j,0}%$
  - `OBJECT`의 feature 말고는 모두 random initialize 
- Textual Feature
  - 각각의 단어 $w_i$에 대해서 POS tag embedding과 pretrained word embedding을 cat해서 사용
  - 두 단어 사이의 representation $w_{i->j}$에 대해서는 Biaffine score로 구함
<img width="320" alt="image" src="https://user-images.githubusercontent.com/46675408/232656235-443c2f1e-6ce0-43d5-a25f-91bb0d79d9ce.png">
 
**Structure Construction**
- encoder 
  - text feature와 visual feature를 attention 연산을 해서 contextual encoding c를 만듦
  - caption에 있는 token들 $\\{w_i\\}$와 Scene graph 표현인 $\\{v_i, v_{i->j}\\}$$에 대해 attention 연산을 한뒤 이를 다 더해 context vector $c_i$를 만든다
  - $Q=v_i, K=w_i, V=w_i$인듯. 
<img width="133" alt="image" src="https://user-images.githubusercontent.com/46675408/232657783-d6ea9ed2-2d39-4305-9e21-b30e728093db.png">

  - 모든 $c_i$에 대해 average pooling을 헤사 전체적인 context vector $s$를 만든다
- decoder 
  - tag sequence $t$와 parse tree $\mathbf{pt}$를 만든다. dynamic programming을 사용하여 parse tree를 만든다

**Cross-Modality Matching**
-  matching score
<img width="245" alt="image" src="https://user-images.githubusercontent.com/46675408/232660242-1ddc2d69-e76c-467f-a849-32a6bbda2480.png">

<img width="282" alt="image" src="https://user-images.githubusercontent.com/46675408/232660275-54123eb8-7f5c-4394-85fc-4739bb4b9a6b.png">

위의 걸로 posterior 구할 수 있음
<img width="302" alt="image" src="https://user-images.githubusercontent.com/46675408/232660293-23d6cbd5-98a4-451b-a698-41466aea0f69.png">


### Learning

**MLE loss**
<img width="517" alt="image" src="https://user-images.githubusercontent.com/46675408/229680481-17f3bac6-c138-485d-8510-739c1b8c941f.png">

- $t_i$ : tag sequence. 
- $\mathbf{pt}$ : parse tree.
이때 MLE loss는 target 없이 EM 알고리즘으로 학습됨!
E step : $\theta$가 주어졌을 때 parse tree들 생성
M step : parse tree가 주어졌을 때 $\theta$를 likelihood 관점에서 gradient descent로 학습

여기서 tag란 dependancy parsing을 tag로 표현하는 방법론인듯

<img width="453" alt="image" src="https://user-images.githubusercontent.com/46675408/232661643-90e22b0f-2c1e-44ea-ba90-bbae3c7b28d4.png">

c.f. [Parsing as Tagging](https://aclanthology.org/2020.lrec-1.643.pdf)

<img width="404" alt="image" src="https://user-images.githubusercontent.com/46675408/232658588-d9d2cad4-bde6-4db7-8e71-a917311fd9cf.png">


**Contrastive loss**
<img width="545" alt="image" src="https://user-images.githubusercontent.com/46675408/229680403-17b63e62-7c41-4353-a65a-6e11e9b5ad2b.png">

 - $\mathbf{\hat{I}}$ : negative image 
 - $c$ : contextual encoding. $c_i = \sum Attn(w_i, v_i)w_i$
 - $w_i$ : caption 내 i번째 token
 - $v_i$ : object의 image feature.
 - sim 함수는 그냥 내적으로 정의 

**Inference**
<img width="319" alt="image" src="https://user-images.githubusercontent.com/46675408/229680977-15be1390-d29c-4679-a65e-1910add3f551.png">

가능한 모든 Parse tree를 만들고 가장 likelihood가 높은걸 찾음
그리고 각 contextual encoding c와 가장 가까운 $v$를 찾으면 scene graph도 만들 수 있음(Relation은 caption에 있는 relation이겠징?)

<img width="347" alt="image" src="https://user-images.githubusercontent.com/46675408/229681043-ed7087af-ea77-4356-9a50-d70186de38b6.png">


### Result 
<img width="1286" alt="image" src="https://user-images.githubusercontent.com/46675408/229681274-4f84b297-ce67-4d2e-8326-0c257c812f41.png">

- caption에 대한 gt structure는 없기 때문에 external parser로 만들고 Visually Grounded Neural Syntax Acquisition https://arxiv.org/pdf/1906.02890.pdf 를 사용했다

etc.
    - model 부분 마저 읽고 정리하기
    - visual grounding에는 SGG가 쓰이나?
        - https://github.com/TheShadow29/awesome-grounding
        - 데이터셋으로는 Flickr30k Entities / RefCOCO/RefCOCO+/RefCOCOg가 많이 쓰인당 VG도 있는듯
        - sgg + image가 주어졌을 때 object location을 하는 scene-graph grounding이라는 연구가 있는데 뭐에 쓰이는지는 잘..
            - https://openaccess.thecvf.com/content/WACV2023/papers/Tripathi_Grounding_Scene_Graphs_on_Natural_Images_via_Visio-Lingual_Message_Passing_WACV_2023_paper.pdf
        - 딱히 그렇지 않은듯. 
