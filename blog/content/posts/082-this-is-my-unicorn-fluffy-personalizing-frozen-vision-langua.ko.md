---
title: "[74] “This is my unicorn, Fluffy”: Personalizing frozen vision-language representations"
date: 2022-11-04
tags: ['dataset', '2022Q3', '25min', 'ECCV', 'nvidia', 'CLIP']
paper: "https://arxiv.org/pdf/2204.01694.pdf"
issue: 82
issueUrl: "https://github.com/long8v/PTIR/issues/82"
---
<img width="700" alt="image" src="https://user-images.githubusercontent.com/46675408/199869384-2af5d03d-5f98-4fc2-b30e-4b862cad9529.png">

[paper](https://arxiv.org/pdf/2204.01694.pdf)

## TL;DR
- **task :** personalized vision and language => personalized image retrieval/object detection/segmentation 
- **problem :** user-specific한 object를 효율적으로 학습하고 싶다. CLIP에 adaptor를 추가하는 방식은 이전 class들의 성능을 악화시키는 효과가 있음. 
- **idea :** 새로운 concept을 새로운 vocab으로 추가하여 학습 하자! 이를 위해 1) 이미지가 주어졌을 때 input word embedding을 찾는 inverse function을 학습하고 2) 새 concept의 이미지 몇장을 inverse function을 통과시켜 새 concept의 word embedding을 초기화한다 3) 새 concept의 textual 정보를 가지고 finetuning한다.
- **architecture :** CLIP
- **objective :** 이미지 인코더를 통과한 임베딩과 `A photo of a [new vocab]`의 임베딩이 가까워지도록, 새 concept의 super-concept과의 임베딩은 멀어지도록 학습 
- **baseline :** Adapter, text-only CLIP, COLLIE 
- **data :** Youtube-VOS, DeepFashion2(both introduced in this paper)
- **result :** SOTA
- **contribution :** 새로운 태스크 제안. 효율적인 아키텍쳐!
- **limitation or 이해 안되는 부분 :** CLIP 다시 읽어야될듯? Deep Sets?

## Details
### new setup, personalized vision & language
<img width="600" alt="image" src="https://user-images.githubusercontent.com/46675408/200228860-b6f1697d-391b-4591-8733-37284323564d.png">

- pretrained model h(S, I)에 새로운 sentence S와 이미지 I가 들어감. 
- 새로운 concept인 C가 들어가서 V' = V U C 로 학습될 수 있도록 하길 원함
- 학습 시에는 concept C에 대한 몇개의 이미지와 새로운 컨셉에 대한 설명 텍스트(e.g. "mug", "short sleeve top")가 주어짐

### Adaptor vs new vocab 추가
<img width="600" alt="image" src="https://user-images.githubusercontent.com/46675408/200228887-06682e8f-1452-4b0e-b2cf-7b19d0946e6a.png">


새로운 vocab을 추가하지 않으면 이전 class에 대한 encoder output이 뭉개진다. 우리의 텍스트임베딩이 새로운 컨셉을 품을 수 있을 정도로 크다는 가정으로 모델이 시작

### Architecture
<img width="600" alt="image" src="https://user-images.githubusercontent.com/46675408/200228555-647a2d9a-2ebe-4f1e-a309-9b09778f31ca.png">

DeepSets이란 네트워크로 inverse mapping function 학습

### Loss
<img width="600" alt="image" src="https://user-images.githubusercontent.com/46675408/200228607-2a01a20e-9a1e-49c8-9e76-9c2145d4c023.png">
