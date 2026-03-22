---
title: "[6] Crossing the Format Boundary of Text and Boxes: Towards Unified Vision-Language Modeling"
date: 2022-01-18
tags: ['multimodal', '2021Q4', 'backbone', 'multitask']
paper: ""
issue: 6
issueUrl: "https://github.com/long8v/PTIR/issues/6"
---
Crossing the Format Boundary of Text and Boxes: Towards Unified Vision-Language Modeling
[arxiv](https://arxiv.org/pdf/2111.12085.pdf)
![image](https://user-images.githubusercontent.com/46675408/149867612-4e85cf87-c5ad-45e4-ad57-3f552510523e.png)

![image](https://user-images.githubusercontent.com/46675408/149868133-0b893378-d1a4-4ab5-ab02-e0498adbc823.png)
**problem :** [pix2seq](https://long8v.notion.site/pix2seq-109e93c7ebb54104bbca96f16ddc4127)는 object detection만을 위한 framework, 이를 다양한 Vision-Language 문제로 unified framework로 확장해보자
**solution :** pix2seq와 매우 유사하게 object box를 bin으로 자른 뒤, generation 방법으로 task를 품. 이미지는 이미지 인코더(CNN)에 넣고, task prefix, task input을 텍스트 인코더에 넣고 concat한 뒤 트랜스포머 인코더에 넣음, 이후 하나의 트랜스포머 디코더가 output을 generation함. Object Detection 외의 task들에 대해 output sequence를 정의함  
**result :** grounded captioning, VQA, image catptioning, object detection 등 다양한 태스크를 하나의 unified model로 풀 수 있었고, 이 중 몇개의 task는 multi-task learning으로 성능에 이득. 