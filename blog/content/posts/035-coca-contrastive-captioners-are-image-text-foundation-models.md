---
title: "CoCa: Contrastive Captioners are Image-Text Foundation Models"
date: 2022-06-22
tags: ['multimodal', 'backbone', 'google', '2022Q2']
paper: "https://arxiv.org/pdf/2205.01917.pdf"
issue: 35
issueUrl: "https://github.com/long8v/PTIR/issues/35"
---

<img width="569" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d6619610-f504-44de-9f19-4edf14d63dd4">

[paper](https://arxiv.org/pdf/2205.01917.pdf)

## TL;DR
**PROBLEM :** Creating a good vision backbone. I want to create a model that can be trained from scratch by integrating three types of image pretraining for classification labels, a dual-encoder model that receives image-text pairs and is trained with contrastive loss, and an encoder-decoder model that has an image encoder and a text decoder that receives image features with cross-attention for classification, VQA, etc.
**solution :** Given an image-text pair, contrastive loss with the last token from the image encoder and the cls-token from the text decoder, stacking a multi-model text decoder with cross-attention with the image input on top of the text decoder, and captioning loss with the last token from the image encoder and the cls-token from the text decoder. Pretrain with the sum of the two losses.
**result :** SOTA on various tasks in SOTA
<img width="695" alt="image" src="https://user-images.githubusercontent.com/46675408/174938121-bafee08b-8737-4fba-8283-7e97ee94e1d0.png">



## Details
- **Architecture**
<img width="1005" alt="image" src="https://user-images.githubusercontent.com/46675408/174954322-7af62fef-0524-4892-94d1-50331d76977e.png">

- **loss**

captioning loss
![image](https://user-images.githubusercontent.com/46675408/175834167-8856741f-5aab-49cc-8a18-05bfde05d5ce.png)

dual encoder contrastive loss
![image](https://user-images.githubusercontent.com/46675408/175834151-b1fe8137-5010-40f6-bab4-c85eacb2617b.png)
 

- Attentional Poolers: When calculating contrast loss, we use only one token from the image, but when performing the encoder-decoder's capturing task, we use the entire image token sequence. This is because in preliminary experiments, a single pooled image performed better in the visual recognition task, and in the multimodal task, it is advantageous to see more tokens because it is good to refer to region-level features. For this reason, we used task-specific attentional pooling to allow different visual representations for each downstream task. The pooler is a single multi-head attention layer with n learnable queries. (where key and value are encoder output) This allows it to be trained to have different length queries for two different losses. Naturally, this learnable query also acts as a task adaptor.
