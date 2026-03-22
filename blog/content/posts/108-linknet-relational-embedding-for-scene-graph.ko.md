---
title: "[99] LinkNet: Relational Embedding for Scene Graph"
date: 2023-01-18
tags: ['NeurIPS', '2017', 'SGG']
paper: "https://arxiv.org/abs/1707.03718"
issue: 108
issueUrl: "https://github.com/long8v/PTIR/issues/108"
---

![image](https://user-images.githubusercontent.com/46675408/213080672-ab8303f9-c05f-4748-ac9e-9dbcdb669668.png)

[paper](https://arxiv.org/abs/1707.03718)

## TL;DR
- **I read this because.. :** SGG two-stage 초기 논문
- **task :** two-stage SGG
- **problem :** 선행 연구들 중 하나. 이 논문 전에 neural motfis, #104, SGG with iterative message passing 정도 있었던 듯
- **idea :** 각 오브젝트들을 강화된 embedding으로 만들어서 예측하자!
- **architecture :** Faster-RCNN + object를 표현하는 임베딩을 만들고 이걸로 $O(n^2)$개 pair에 대해 relation cls 분류. global feature + od가 뽑은 cls에 대한 임베딩 + RoI visual feature + relative geometric 정보들이 들어감. 
- **objective :** 1) 이미지 레벨에서 object class를 multi-label loss 2) 각 object에 대해 cls loss 3) relation classification loss 
- **baseline :**  neural motfis, #104, SGG with iterative message passing 
- **data :** Visual Genome
- **evaluation :** SGdet, SGcls, PredCls
- **result :** sota
- **contribution :** simple !

## Details
### Architecture
![image](https://user-images.githubusercontent.com/46675408/213084978-cd97c25a-3d7f-4183-9e81-c924e216093a.png)

- Global Context Encoding Module
feature에 대해 AvgPool 한 뒤에 FC 붙여서 multi-label classification 

- Relation Embedding Module 
Obejct feature $O_i$를 만드는데 OD가 예측한 cls $l_i$의 임베딩과 RoI pooling으로 뽑은 feature, image 전체의 context feature $c$를 해서 임베딩을 만들고, FCN을 쌓아서 cls를 예측한다

![image](https://user-images.githubusercontent.com/46675408/213085357-635b889e-0b3b-46c5-82fc-2705dd5896c9.png)

![image](https://user-images.githubusercontent.com/46675408/213085624-2078a27e-04b5-4b22-910e-9ca6f0b08457.png)

![image](https://user-images.githubusercontent.com/46675408/213085664-2b418863-fde0-428d-a028-1a911dc57920.png)

relation을 구할 때 geometric feature도 넣어준다
![image](https://user-images.githubusercontent.com/46675408/213085699-659b7f28-23b3-47fd-8936-0528bff1bcb6.png)

### Loss
![image](https://user-images.githubusercontent.com/46675408/213085803-edc0d96a-ef81-4129-aaf0-72acd297ce08.png)


### Result 
![image](https://user-images.githubusercontent.com/46675408/213085764-89a5bb0d-691b-4dfc-b2d1-f4c19197fb2c.png)
