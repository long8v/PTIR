---
title: "[64] Open-Vocabulary DETR with Conditional Matching"
date: 2022-09-16
tags: ['2022Q1', 'object detection', 'ECCV', 'OV']
paper: "https://arxiv.org/pdf/2203.11876.pdf"
issue: 70
issueUrl: "https://github.com/long8v/PTIR/issues/70"
---
![image](https://user-images.githubusercontent.com/46675408/190539295-4c529608-d944-41af-a00a-0141fca1e64e.png)

[paper](https://arxiv.org/pdf/2203.11876.pdf)

## TL;DR
- **task :** open vocab object detection
- **problem :** 기존의 object detection 모델들은 closed set으로 예측하여 확장성이 어렵다. 이를 해결하기 위한 open vocab object detection 들은 PRN을 먼저 하고 class 예측을 해서 새로운 class에 대한 bbox 예측이 어렵다. 
- **idea :** DETR을 사용하여 end2end로 object detection을 해보자! class로 사용하고 있던걸 CLIP을 사용하여 텍스트 임베딩으로 보내자.
- **architecture :** image와 text(=class)를 CLIP을 통해 임베딩을 한 뒤에 object queries와 합해주어 conditional query를 만든다. 한 이미지에 여러 object가 나올 수 있으니 N개로 복사해준다. 이후 bipartite matching은 `[obj]`, `[no obj]`가 아니라 input image와 conditional query가 주어졌을 때 `[matched]`, `[not matched]`로 하게 된다. 
- **objective :** bce(match / not match) + bbox loss(gIoU, L1) + embedding reconstruction loss(L1)
- **baseline :** OVR-CNN, ViLD
- **data :** COCO, ELVIS
- **result :** OV OD 모델 대비 그냥 AP, novel 클래스에 대한 AP 둘다 SOTA
- **contribution :** end2end open vocab object detection
- **limitation or 이해 안되는 부분 :** 모든 base class / novel class에 대한 임베딩을 이미 가지고 있고(논문에서 말하는 R개), 그거랑 다 매칭을 해서 예측을 하는게 맞나? 헷갈림. 그럼 학습할 때는 in batch negative 이런 식으로 하려나? 

## Details
![image](https://user-images.githubusercontent.com/46675408/190544655-18a54b9b-0a8b-4e92-83df-d871f59bd1f7.png)

![image](https://user-images.githubusercontent.com/46675408/190543790-fe5390a2-b60e-4d7a-a3f0-7b4d0c577703.png)

![image](https://user-images.githubusercontent.com/46675408/190545375-38c5a12c-9ec0-45a3-a212-bc675309e0bb.png)

![image](https://user-images.githubusercontent.com/46675408/190544759-af96aa73-b4e7-4105-8bdf-05e5cba854f4.png)

