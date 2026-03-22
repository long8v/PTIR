---
title: "[7] SLIP: Self-supervision meets Language-Image Pre-training"
date: 2022-01-20
tags: ['multimodal', '2021Q4', 'few-shot', 'SSL']
paper: ""
issue: 7
issueUrl: "https://github.com/long8v/PTIR/issues/7"
---
![image](https://user-images.githubusercontent.com/46675408/150263175-a405612c-b130-4a53-ab18-88b8eb199107.png)
[arxiv](https://arxiv.org/pdf/2112.12750v1.pdf), [code](https://github.com/facebookresearch/SLIP)
![image](https://user-images.githubusercontent.com/46675408/150264097-52b53432-69aa-4cbb-978c-75250a3966f1.png)

**problem :** Self-supervised-Learning이 CLIP 모델 구조에서도 잘 작동하는지 실험
**solution :** 이미지와 텍스트에 대해서는 [contrastive learning](https://openai.com/blog/clip/)을 하고, 이미지에 대해서는 [self-supervision learning](https://arxiv.org/pdf/2002.05709.pdf)을 하여 로스를 합하여 학습. 
**result :** linear prediction(=representation에 FCN 붙여서 분류하는것. linear만 학습함. BERT에서 언급하는 'feature-based learning'), zero-shot learning, end-to-end finetuning에서 SOTA