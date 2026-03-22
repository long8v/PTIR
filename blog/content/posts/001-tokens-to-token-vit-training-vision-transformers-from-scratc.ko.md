---
title: "[1] Tokens-to-Token ViT: Training Vision Transformers from Scratch on ImageNet"
date: 2022-01-05
tags: ['2021Q4', 'ViT', 'backbone']
paper: "https://arxiv.org/pdf/2101.11986.pdf"
issue: 1
issueUrl: "https://github.com/long8v/PTIR/issues/1"
---
![image](https://user-images.githubusercontent.com/46675408/148156445-1c949ffe-3318-46ef-8cad-bce4862ad4d2.png)
[paper](https://arxiv.org/pdf/2101.11986.pdf)

**Problem :** ViT는 작은 데이터셋에서의 성능이 CNN 보다 떨어짐. local-feature를 잘 못잡고, attention 구조가 비전을 위해 설계되지 않음
**Solution :** Transformer에 넣는 input을 단순 토큰이 아니라, T2T module의 결과를 사용함. T2T 모듈는 n x n 으로 자른 이미지를 Transformer에 넣고 그 token out들을 다시 이미지처럼 w, h가 있도록 구조화 시킴. 이후 인접한 토큰끼리 한 패치로 만들어 각 패치를 concat한 뒤 다음 T2T 모듈로 넘김. 이렇게 n번을 반복하여 나온 것을 효율화된 트랜스포머 backbone에 학습.
**Result :** 유사하거나 더 큰 규모의 CNN이나 ViT보다 이미지 분류에서 성능 우위.
**느낀점 :** ViT가 처음엔 inductive bias가 없다면서 나왔는데, 결국 CNN의 구조들을 차용한 모델들이 더 빠르게 학습하는것을 보니 inductive bias는 빠르게 학습하기 위해 필요하다.(큰 데이터셋에 대해선 학습 과정에서 그런 inductive bias를 알아서 학습하니 더 낫나보다) 그럼에도 CNN보다 transformer가 나은 이유는 결국 병렬화..? 혹은 multi-modal 가능..?
**details :** [paper summary](https://long8v.notion.site/T2T-ViT-1ce0286783bf42dea959bfc6ed8247b3)