---
title: "[55] Position Prediction as an Effective Pretraining Strategy"
date: 2022-08-26
tags: ['ViT', 'PE', '2022Q2', '25min', 'apple']
paper: "https://arxiv.org/pdf/2207.07611.pdf"
issue: 61
issueUrl: "https://github.com/long8v/PTIR/issues/61"
---
![image](https://user-images.githubusercontent.com/46675408/186793487-69b6a699-6206-4a60-b0b1-01964a20cf63.png)

[paper](https://arxiv.org/pdf/2207.07611.pdf)

## TL;DR
- **task :** image pretraining
- **problem :** simple and effective pretraining 
- **idea :** PE를 input에 넣어주지 말고 output으로 예측하도록 하자!
- **architecture :** 기본적으로 ViT. n개의 patch 중에 m개의 context patch를 뽑고 Q=all patches, K=V=context patches인 cross-attention.
- **objective :** Cross Entropy Loss
- **baseline :** ResNext, ViT-S, MOCOv3, MAE
- **data :** CIFAR-100, ImageNet, ImagNet-1K
- **result :** 효율적인 프리트레이닝(모든 patch를 안봐서), 100에폭에서 ViT-S나 MOCO보다 좋은 성능.(ResNeXT보단 낮음). MAE보다도 성능이 낮은데 앙상블 했더니 1600에폭 학습한 MAE 보다 성능이 더 좋았다고 하면서 다른 representation을 학습한거라고 주장
- **contribution :** simple! 
- **limitation or 이해 안되는 부분 :** 

## Details
![image](https://user-images.githubusercontent.com/46675408/186793523-fc30e3e1-dd8c-485e-b713-01ae2c5956da.png)


![image](https://user-images.githubusercontent.com/46675408/186793302-a25b3010-5d5c-4679-9a4b-ab2993f8cf8b.png)

![image](https://user-images.githubusercontent.com/46675408/186793691-a9ec88fb-d6c4-492c-b8c4-9e80852ea394.png)

![image](https://user-images.githubusercontent.com/46675408/186793869-65e56f2b-5695-49f8-838b-e24792094998.png)
