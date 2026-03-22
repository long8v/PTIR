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

**Problem :** ViT performs worse than CNN on small datasets. Poor local-feature capture, attention structure is not designed for vision
**Solution :** The input to the Transformer is not just a token, but the result of the T2T module. The T2T module takes an n x n cropped image, puts it into the Transformer, and structures the token out so that it has w and h like the image again. It then concatenates adjacent tokens into a patch, concatenates each patch, and passes it to the next T2T module. This is repeated n times, and the result is trained into an efficient Transformer backbone.
**Result :** Outperforms CNNs and ViTs of similar or larger size in image classification.
**Feelings :** ViT initially said that it does not have inductive bias, but in the end, I saw that models that borrowed the structure of CNN learn faster, so inductive bias is necessary for fast learning.(For large datasets, it is better because it learns such inductive bias during the learning process) Nevertheless, the reason why transformer is better than CNN is that it can be parallelized... or multi-modal...?
**details :** [paper summary](https://long8v.notion.site/T2T-ViT-1ce0286783bf42dea959bfc6ed8247b3)