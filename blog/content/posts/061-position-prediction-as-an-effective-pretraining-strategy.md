---
title: "Position Prediction as an Effective Pretraining Strategy"
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
- **idea :** Don't put PE in input, predict it in output!
- **architecture :** Basically ViT. cross-attention where m context patches are drawn out of n patches, Q=all patches, K=V=context patches.
- **objective :** Cross Entropy Loss
- **baseline :** ResNext, ViT-S, MOCOv3, MAE
- **data :** CIFAR-100, ImageNet, ImagNet-1K
- **result :** Efficient pretraining (without looking at all patches), better performance than ViT-S or MOCO at 100 epochs (but lower than ResNeXT). Performance is lower than MAE, but when I ensemble it, it performs better than MAE trained on 1600 epochs, claiming that it trained a different representation.
- **contribution :** simple! 
- **Limitations or things I don't understand :**

## Details
![image](https://user-images.githubusercontent.com/46675408/186793523-fc30e3e1-dd8c-485e-b713-01ae2c5956da.png)


![image](https://user-images.githubusercontent.com/46675408/186793302-a25b3010-5d5c-4679-9a4b-ab2993f8cf8b.png)

![image](https://user-images.githubusercontent.com/46675408/186793691-a9ec88fb-d6c4-492c-b8c4-9e80852ea394.png)

![image](https://user-images.githubusercontent.com/46675408/186793869-65e56f2b-5695-49f8-838b-e24792094998.png)
