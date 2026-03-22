---
title: "[111] Perceiver IO: A General Architecture for Structured Inputs & Outputs"
date: 2023-04-24
tags: ['multimodal', '2021Q2', 'ICLR', 'DeepMind', 'MTL']
paper: "https://arxiv.org/pdf/2107.14795.pdf"
issue: 120
issueUrl: "https://github.com/long8v/PTIR/issues/120"
---
<img width="612" alt="image" src="https://user-images.githubusercontent.com/46675408/233893986-33a2b0e1-0be8-4621-80c1-324f37170a13.png">

[paper](https://arxiv.org/pdf/2107.14795.pdf)

## TL;DR
- **I read this because.. :** CS330 강의에서 언급됨. #118 에서도 Perceiver 사용했다고 해서 IO 붙은건 뭐가 다르지 하고 봄
- **task :** image classification, language modeling, optical flow, StarCraft II, ...
- **problem :** 각각의 도메인 / 태스크에 대한 모델들이 각각 있음. 하나의 NN으로 처리하면 인생이 편할텐데
- **idea :** transformer encoder-decoder 구조인데 Perceiver구조(CA로 input modality가 들어가는 형태) + output query를 사용하자
- **input :** (encoder) N x D차원의 latent array (decoder) positional embedding or task embedding 
- **output :** (encoder) context vector (decoder) class(for image classification), token id(for MLM), ... 
- **architecture :** 근데 encoder가 Perceiver 형태(텍스트, 이미지, 비디오등이 CA로 들어가는) / decoder는 encoder context vector랑 output query간의 CA만 있는 
- **objective :** 각 태스크에 맞는 목표 함수
- **baseline :** GLUE(BERT), Image Classification(ViT-B), Optical Flow(PWCNet, RAFT), StarCraft(Transformer), AudioSet Classification(Perceiver IO)
- **data :** English Wikipedia + C4, ImageNet, JFT.... 
- **result :** GLUE에서 BERT랑 동일 FLOPS 대비 더 나은 성능. Optical flowㅂ도 베이스라인 대비 몇개 Metric 대비 좋은 성능. 나머지는 성능이 그럭저럭이지 best는 아님.
- **contribution :** 상당히 많은 modality에 대해 test. decoder에 task embedding / PE embedding을 넣는 방식이 contribution point가 아닌가?! 나머지는 막 새로운 느낌은 아닌듯
- **etc. :**

## Details
### Architecture
<img width="589" alt="image" src="https://user-images.githubusercontent.com/46675408/233895628-bfc16f01-c231-4e01-aa73-0c381353a332.png">

### Output Queries
<img width="581" alt="image" src="https://user-images.githubusercontent.com/46675408/233895652-0370dc94-0b20-41fb-9497-9c392e603ad0.png">

- 이미지 분류 같은 classification은 그냥 task embedding
- multi task인 경우 task embedding 들 여러개 
- MLM의 경우 2048개의 Positional Embedding

### 아키텍쳐 세부
<img width="584" alt="image" src="https://user-images.githubusercontent.com/46675408/233895694-1a84bc85-81dc-4b94-9eac-df5dd8519e22.png">


### Result 
- task들 
<img width="1041" alt="image" src="https://user-images.githubusercontent.com/46675408/233896560-049ca9da-f2ee-481f-9e9f-592ec7ddd6af.png">


- GLUE
<img width="577" alt="image" src="https://user-images.githubusercontent.com/46675408/233895675-a9c83357-985b-4adb-ab36-9404c748f5eb.png">

introduction에서도 그렇고 UTF-8 byte로 한 걸 강조하는데 이것자체는 contribution인진 모르겠고(BBPE 같은 선행연구가 있으니?)
얘 때문에 max_len이 길어지는데 $$O(n**2)$$이 안되고 구조상 linear하게 복잡도가 늘어나는게 contribution인듯!
이 표에서도 그렇고 BERT보다 파라미터는 훨 큰데 FLOPS가 더 낮음. 파라미터는 hidden dim을 줄이고 Depth를 엄청 늘렸넹 이건 왜지
BERT랑 비교했을 때 max_len을 512 -> 2048로 늘렸고 vocab size는 256로 줄였다고 함. 

- image classification
<img width="588" alt="image" src="https://user-images.githubusercontent.com/46675408/233895750-3bc96675-3cf4-4b04-8ab9-1093b1b8cb20.png">

ViT-B/16와 비교했을 때 딱히 좋아보이진 않는뎅.. 일단 ViT보단 안좋은듯 성능
JFT pretraining 한게 86.4점인데 ViT-H/14의 88.6점이랑 차이가 좀 있어보인당(파라미터 수는 1/3이긴 함)
결국 최종적인 best 성능은 Conv 붙인 것도 좀 그럼
그 외 일단 전작 Perceiver보다 좋아졌다 정도 볼 수 있는듯?

- AudioSet Classification
<img width="585" alt="image" src="https://user-images.githubusercontent.com/46675408/233895709-da9aa669-36d3-4689-a7e0-c704f0e2f69a.png">

- StarCraft II
<img width="570" alt="image" src="https://user-images.githubusercontent.com/46675408/233895724-061bea35-a8de-4e82-87fc-8c2ff10ff17a.png">



