---
title: "[88] Relation Networks for Object Detection"
date: 2022-12-11
tags: ['2017', 'microsoft', 'object detection']
paper: "https://arxiv.org/pdf/1711.11575.pdf"
issue: 97
issueUrl: "https://github.com/long8v/PTIR/issues/97"
---
<img width="882" alt="image" src="https://user-images.githubusercontent.com/46675408/206889321-305e953d-21cd-4a18-b01a-7e476a227b45.png">

[paper](https://arxiv.org/pdf/1711.11575.pdf)

## TL;DR
- **I read this because.. :** #58 에서 언급됨. 이름이 SGG랑 관련돼있을 것 같은 느낌
- **task :** object detection
- **problem :** object내의 relation을 모델링하면 object recognition을 더 잘할 것 같다는 직관은 있었으나 이를 증명한 연구는 없었음. sota object detection 연구는 각 instance를 각각 모델링함.
- **idea :** attention module을 사용해서 object 간의 relation을 구하고 이를 weighted sum해서 벡터를 강화하자
- **architecture :** CNN -> RPN -> RoI -> FC -> object relation module -> fc -> object relation module -> cls / bbox prediction -> duplicate removal network 
- **objective :** bce for duplicate removal network, cross entropy loss
- **baseline :** fasterRCNN, feature pyramid network(FPN), deformable convolutional network(DCN) 
- **data :** COCO
- **evaluation :** mAP, mAP50, mAP75 
- **result :** SOTA. mAP에서 best, threshold 0.5로 학습하면 mAP50 best, 0.75로 하면 mAP75 best
- **contribution :** first fully end-to-end object detector (without NMS)
- **limitation / things I cannot understand :** duplicate removal network 

## Details

<img width="587" alt="image" src="https://user-images.githubusercontent.com/46675408/206889763-634f8f44-e026-461d-b341-8eeebe69f742.png">


### Object Relation Module

<img width="573" alt="image" src="https://user-images.githubusercontent.com/46675408/206889765-dc3186a6-c6dd-446a-8e09-5020e62a9e65.png">


<img width="363" alt="image" src="https://user-images.githubusercontent.com/46675408/206889783-3f6b7fa2-b597-4701-9963-2e5d01c326d3.png">

- $f_R$ : relation feature
- $f_G$ : geometric feature
- $f_A$ : appearance feature 
- $w_{mn}$ : m번째 object가 n번째 object에 얼마나 영향을 주는지?

<img width="320" alt="image" src="https://user-images.githubusercontent.com/46675408/206889917-fd3c9baf-78d3-46e6-8f1b-87861c6f6b54.png">

$w_A^{mn}$은 그냥 scaled dot attention이랑 비슷
<img width="320" alt="image" src="https://user-images.githubusercontent.com/46675408/206890005-c27114f0-213b-46a5-aee8-bb118c7471ee.png">

$w_G^{mn}$는 feature를 뽑고(두개를 합쳐서 $\varepsilon_G$)  sine/cosine으로 임베딩 시킨 뒤에 $W_g$ 곱해주고 ReLU 취해서 구해짐
<img width="366" alt="image" src="https://user-images.githubusercontent.com/46675408/206890055-5782b4b1-2397-429c-b109-0deaa409bfcb.png">

뽑는 feature
<img width="488" alt="image" src="https://user-images.githubusercontent.com/46675408/206890035-1a00f7f4-1234-4b8e-be49-23883210e26d.png">

최종적으로 $f^n_a$는 저렇게 뽑은 nm개의 object relation을 concat해서 나온다. 

### Relation for Instance Recognition
<img width="589" alt="image" src="https://user-images.githubusercontent.com/46675408/206890153-0c154814-ef2e-4573-859b-4e4539eae289.png">

### Relation for Duplicate Removal 
<img width="550" alt="image" src="https://user-images.githubusercontent.com/46675408/206890161-7adaf234-65a5-47e6-9459-1c49d2ab2780.png">

별거 아니고 그냥 {0, 1} 로 예측하는거. 근데 relation module이 있으니 중복을 잘 제거할 수 있을듯.
- rank feature : score로 바로 예측하는 것보다 rank를 구하고 embedding 하는게 좋았다.
- threshold에 따라 correct, duplicate를 label로 주는데 이 theshold를 뭘로 주냐에 따라 AP50, AP75..의 best가 달랐음

## Result
<img width="1024" alt="image" src="https://user-images.githubusercontent.com/46675408/206890236-e04f1516-b3cf-4b7f-ac09-a6b4197779e6.png">

<img width="384" alt="image" src="https://user-images.githubusercontent.com/46675408/206890241-8f28d971-ab27-491b-9845-c90aefd987ce.png">


<img width="568" alt="image" src="https://user-images.githubusercontent.com/46675408/206890228-85e23fb2-2ab7-4c9c-aac2-5e76d86ba90d.png">
