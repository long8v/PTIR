---
title: "[36] SGTR: End-to-end Scene Graph Generation with Transformer"
date: 2022-07-19
tags: ['2022Q1', 'CVPR', 'SGG', 'graph', 'one-stage']
paper: "https://openaccess.thecvf.com/content/CVPR2022/papers/Li_SGTR_End-to-End_Scene_Graph_Generation_With_Transformer_CVPR_2022_paper.pdf"
issue: 41
issueUrl: "https://github.com/long8v/PTIR/issues/41"
---
![image](https://user-images.githubusercontent.com/46675408/179683280-c3249640-3773-400a-8fa7-e37eccf2dd14.png)

[paper](https://openaccess.thecvf.com/content/CVPR2022/papers/Li_SGTR_End-to-End_Scene_Graph_Generation_With_Transformer_CVPR_2022_paper.pdf), [code](https://github.com/Scarecrow0/SGTR)

## TL;DR
- **task :** one-stage SGG  
- **problem :** N entity proposal -> O(n**2) predicate proposal -> inefficient!
- **idea :** SGG 문제를 bipartite graph로 풀어보자. entity, predicate를 node로 보고 directed edge로 연결해서 표현해보자!
![image](https://user-images.githubusercontent.com/46675408/179701271-c5dd4052-589d-41f0-9cb1-9e9ab54d5f59.png)
- **architecture :** 일단 DETR처럼 ResNet으로 visual feature 뽑고, learnable query로 entity node를 만듦. predicate node의 경우 visual feature와 뽑힌 entity node의 임베딩을 concat하여 attention. 이것들을 가지고 predicate / entity indicator들 각각을 위에서 나온 부산물들로 cross attention 한 뒤 L층 위에서는 fusion 해가면서 레이어 쌓음. 최종적으로 나오는 output에 대해서 bipartite graph로 다시 만들어서 최종 output 포맷으로 만듦. 
- **objective :** entity에 대한 loss(=DETR loss) + predicate에 대한 loss. predicate는 matching matrix를 만들고 hungarian으로 찾고, entity들의 localization + categories, predicate와 관련된 object들의 localization + relation의 categories에 대한 loss 
- **baseline :**  FCSGG, ...
- **data :** Visual Genome, Open Image V6
- **result :** SOTA with more efficient inference
- **contribution :** transformer 구조로 graph 문제를 tackle? subject / object 안 나눈 것이랑 O(n**2)이 아닌 것? 아 근데 구조가 너무 복잡함..

## Details
### Architecture
![image](https://user-images.githubusercontent.com/46675408/179873763-283d44b4-fcc3-4439-ab53-564773b46a1b.png)

#### 1) Backbone and Entity Node Generator
DETR처럼 ResNet 거치고 나온 feature들 transformer로 넣음. viusl feature Z가 나옴.
DETR decoder 처럼 entity들 learnable query로 넣음. 각각은 feature map Z와 함께 들어와서 entity의 bbox B와 class score인 P와 
관련된 feature representation H를 내뱉음.
<img width="651" alt="image" src="https://user-images.githubusercontent.com/46675408/179874155-8eabe1d6-fe9d-474a-8edb-88388ad27564.png">

#### 2) Predicate Node Generator 
- predicate encoder 
predicate-specific한 image feature를 뽑기 위해 Transformer encoder 사용. 결과로 Z^p가 나옴.
- predicate query initialization
그냥 learnable query넣으면 compositional property를 못담으니, subject와 object의 query를 concat해서 넣어줌.
<img width="173" alt="image" src="https://user-images.githubusercontent.com/46675408/179874585-c382ac9d-b25b-470b-817f-fc03a185d1a7.png">

그리고 이 query에 대한 표현을 학습 할때에는 1에서 나온 feature H와 bbox B를 같이 넣어서 attention을 해줌.
<img width="583" alt="image" src="https://user-images.githubusercontent.com/46675408/179874695-836137fb-24f6-470f-98df-42f2e451053d.png">

<img width="638" alt="image" src="https://user-images.githubusercontent.com/46675408/179874879-3877c716-26c0-40ff-a3e1-9ac5e973db1d.png">

#### 3) Structural Predicate Node Generator 
위에서 받은 matrix로 최종 attention 연산을 하 것임
a) predicate sub-decoder 
image feature들로부터 predicate 표현을 뽑는 것
![image](https://user-images.githubusercontent.com/46675408/179881187-51a40e68-dc75-410a-9b72-125fc617b6db.png)

b) entity indicator sub-decoders
predicate query들에 맞게 entity indicator들을 뽑는것
<img width="568" alt="image" src="https://user-images.githubusercontent.com/46675408/179875140-e8e4f91c-62c8-42d0-b783-75dd0600d780.png">

c) predicate indicator fusion 
predicate와 indicator를 연결시키기 위해 layer 위층에 서로를 참고할 수 있도록 하는것. 
![image](https://user-images.githubusercontent.com/46675408/179881224-2d10a22e-3883-4a01-a7ee-a23262477a0a.png)


이 과정을 통해 결론적으로 나오는 output은 아래와 같음.
<img width="578" alt="image" src="https://user-images.githubusercontent.com/46675408/179875264-8d3a8d36-c611-4a85-b2fa-8f91686aac38.png">

predicate에 대한 class 분류와 predicate와 관련된 subject, object의 bbox + categories

### Bipartite Graph Assembling
N개의 엔티티와 N_r개의 predicate로 구성된 bipartite graph로 바꿔줘야 함. entity node와 predicate node간의 adjacency matrix를 만든 뒤, correspondence matrix를 만듦. 
![image](https://user-images.githubusercontent.com/46675408/179880794-af2711bb-2b16-4320-ac5f-9e0e222fc2bd.png)

그림에서 보듯이 entity, subject(연두색), object(파란색)이 있고 이 거리들로 matching!
가령 subject에 대한 예를 들자면?
![image](https://user-images.githubusercontent.com/46675408/179881021-3c67577f-1757-4c30-b8e8-16e0246f514d.png)

entity와 subject 간의 거리를 아래와 같이 정의해주고 distance matrix top K개만 뽑는다.
![image](https://user-images.githubusercontent.com/46675408/179880981-1963820e-b3a9-4676-bcb2-1436aee65d47.png)


### Learning and Inference
![image](https://user-images.githubusercontent.com/46675408/179880930-5accd49e-c013-4ace-b7c0-51e3f4ee596d.png)

DETR entity generator loss.
entity indicator에 대한 localization + classification loss,
predicate와 관련된 entity에 대한 localization, predicate에 대한 classification loss

### Results
![image](https://user-images.githubusercontent.com/46675408/179887018-ddfc6876-45b8-4237-b462-e6bda0efcd17.png)


## 잡생각 / 질문
- visual 정보와 object의 location 정보를 꾸역꾸역 넣어줬는데 안넣으면 안돼서 그러지 않았을까?