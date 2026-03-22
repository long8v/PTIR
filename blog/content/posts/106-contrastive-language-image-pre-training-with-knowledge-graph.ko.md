---
title: "[97] Contrastive Language-Image Pre-Training with Knowledge Graph"
date: 2023-01-12
tags: ['multimodal', 'NeurIPS', 'graph', '2022Q4', 'CLIP']
paper: "https://arxiv.org/pdf/2210.08901.pdf"
issue: 106
issueUrl: "https://github.com/long8v/PTIR/issues/106"
---
<img width="877" alt="image" src="https://user-images.githubusercontent.com/46675408/211960424-46599d7f-f26e-4512-b607-8643ad8699c5.png">

[paper](https://arxiv.org/pdf/2210.08901.pdf)

## TL;DR
- **I read this because.. :** NeurIPS 2023, graph 
- **task :** multi-modal training -> image retrieval, VQA, Visual Entailment, Image Classification, GLUE
- **problem :** CLIP은 너무 간단하게 "match", "not matched" 두 레이블로만 있어서 텍스트와 이미지간의 semantic한 정보를 담고 있지 않다
- **idea :** CLIP + knowlege graph. 인풋이 텍스트-이미지 페어가 아니라 {head, relation, tail} triplet을 받음. head나 Tail은 이미지 또는 텍스트 둘다 될 수 있음.
- **architecture :** CLIP 아키텍쳐를 가져가되, pooling을 하지 않고 concat + Transformer Encoder 쌓아서 Feature 뽑음
- **objective :** triplet에서 relation 또는 tail(또는 Head)을 지우고 예측하도록 함. 1) relation을 지울 땐 그냥 분류 문제(E2R loss) 2) tail을 지웠을 땐 tail의 표현과 head, relation의 표현이 같은 triplet을 가지고 있을 경우 가까워지도록(E2E Loss) 3) GNN 붙여서 tail에 대한 표현이 GNN 통과한 표현과 트랜스포머에 대한 표현이 비슷해지도록(E2G Loss) 4) CLIP teacher와의 KL divergence로 KD(KD Loss)
- **baseline :** CLIP, UNITER, OSCAR, ViLT, ... 외 다수
- **data :** VisualSem(WordNet + ImageNet), Visual Genome, ConceptNet, COCO Caption, CC3M
- **result :** SOTA. 
- **contribution :** triplet 형태의 데이터를 CLIP 학습할 수 있게 formulation.

## Details
### Motivation
<img width="835" alt="image" src="https://user-images.githubusercontent.com/46675408/211961885-63b95840-cd79-4ce6-8641-af2dbf9cf52b.png">

### Dataset
<img width="839" alt="image" src="https://user-images.githubusercontent.com/46675408/211961950-28b1b1bf-d432-4c3e-9743-bdf34515ebfb.png">

추가로 이미지-텍스트 페어의 경우 `is a image of`, `is a caption of`와 같이 relation을 임의로 지정해서 triplet으로 만듦

### Architecture
<img width="838" alt="image" src="https://user-images.githubusercontent.com/46675408/211961912-5c0d14a0-8c6f-4125-b54a-4a867b3369a0.png">

<img width="415" alt="image" src="https://user-images.githubusercontent.com/46675408/211962089-2f62a308-b9fb-4664-acdb-0da003e24fa6.png">

- $f$는 text 나 image encoder 
<img width="486" alt="image" src="https://user-images.githubusercontent.com/46675408/211962067-af2d7b97-7aa2-4b11-9b7e-3995ce115ff0.png">

<img width="396" alt="image" src="https://user-images.githubusercontent.com/46675408/211962200-dda25450-f7a9-4323-8ace-d49503078d78.png">

<img width="464" alt="image" src="https://user-images.githubusercontent.com/46675408/211962243-1ec14f2e-5454-46c8-a01c-e4a93e65c834.png">

relation에 대한 표현은 그냥 인덱싱하면 됨

### Loss
- Triplet based loss
mlm 처럼 Triplet 요소의 일부를 가려놓고 맞추라고 할거임
#### E2E loss
entity (head or tail)을 가려놨을 경우 아래와 같이 loss 추정
<img width="549" alt="image" src="https://user-images.githubusercontent.com/46675408/211962354-e64ae389-a947-45b4-91d4-0dc1faf4d482.png">

가리는건 그냥 0 벡터 cat하는 형식
![image](https://user-images.githubusercontent.com/46675408/212609518-9bdb555c-0770-4504-937e-bcca388c3415.png)

tail의 표현과 해당 tail과 같은 triplet에 속해있는 Head, relation의 표현이 가까워지도록 하는 것

#### E2R loss
relation 맞추는건 그냥 분류문제
<img width="680" alt="image" src="https://user-images.githubusercontent.com/46675408/211962569-41599d64-bf6e-4c51-af6f-85286d268f29.png">

- Graph-based loss
GNN 통과시킨거랑 transformer 통과시킨거랑 entity 표현이 비슷해지도록 
<img width="547" alt="image" src="https://user-images.githubusercontent.com/46675408/211962628-fb105f96-2db4-42a8-a2d0-d91d469cae88.png">

#### Continuous Learning
Pretrained CLIP의 결과와 KL Divergence 
<img width="319" alt="image" src="https://user-images.githubusercontent.com/46675408/211962751-d47d70be-029d-4818-88d8-487b73c965c4.png">

### Experiement setup
<img width="827" alt="image" src="https://user-images.githubusercontent.com/46675408/211962833-f1566f63-98ea-47ee-96d3-95ae32518d1f.png">

## Result
### Image Retrieval
<img width="817" alt="image" src="https://user-images.githubusercontent.com/46675408/211962882-2ffb9c79-e506-4801-8f59-7c9848a099a3.png">
 
### VQA, SNLI_VE
<img width="504" alt="image" src="https://user-images.githubusercontent.com/46675408/211962919-fa1fedc0-394a-4bd5-9d9c-2e50cfe4be46.png">

snli_ve는 이런 데이터라고 하넹
<img width="932" alt="image" src="https://user-images.githubusercontent.com/46675408/211962957-d42401c7-429d-42a2-a392-22b04fd23d6a.png">
https://github.com/necla-ml/SNLI-VE

### GLUE
<img width="843" alt="image" src="https://user-images.githubusercontent.com/46675408/211963018-d63a2d3e-219a-4056-be22-d553e7fcf4df.png">

### Image Classification
<img width="258" alt="image" src="https://user-images.githubusercontent.com/46675408/211963030-cab368b5-aff9-44ea-bfbf-026dbbe02ea2.png">

### Ablation
![image](https://user-images.githubusercontent.com/46675408/212609593-486fbaf6-37a4-41b8-bb4b-af7dbd66e9f1.png)

- CLIP + KG보다 성능이 좋넹

### motivation에서 나온 문제를 해결했나?
![image](https://user-images.githubusercontent.com/46675408/212616863-98e8f00a-b3ea-472d-a508-c146ae791738.png)

VQA에서 색깔과 같은 property를 가진 VQA에 대해서만 평가를 다시 해봤는데 성능이 더 좋았다고 한다