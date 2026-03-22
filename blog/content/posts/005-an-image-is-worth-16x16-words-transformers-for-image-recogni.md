---
title: "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale"
date: 2022-01-13
tags: ['ViT', 'backbone', '2021Q1', 're-read']
paper: "https://arxiv.org/pdf/2010.11929.pdf"
issue: 5
issueUrl: "https://github.com/long8v/PTIR/issues/5"
---
![image](https://user-images.githubusercontent.com/46675408/149278862-fd941e4a-54b0-40da-89cb-13c1c60bd4b8.png)
[paper](https://arxiv.org/pdf/2010.11929.pdf)
[paper summary](https://long8v.notion.site/ViT-9e25358e194e45b484a0b10ea6b570e9)
[implementation](https://github.com/google-research/vision_transformer)

**problem :** Solve the image classification problem with a fully self-attentive structure, minimizing changes to the existing Transformer structure.
**Solution :** Cut the image into P x P patches, flatten them, and make them D-dimensional with a linear projection. Put the resulting patch embedding into the transformer encoder input. Pretrain the MLP on the output by adding `[CLS]` tokens, then fine-tune by changing only the classification MLP.
**Result :** It performed worse than the ResNet family on small data, but when trained on large data, it learned faster than ResNet and outperformed the SOTA