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

**problem :** Experiment to see if self-supervised-learning works well with CLIP model structure
**solution :** Use [contrastive learning](https://openai.com/blog/clip/) for images and text, and [self-supervision learning](https://arxiv.org/pdf/2002.05709.pdf) for images to combine the losses.
**result :** linear prediction (=classification by attaching FCN to a representation. Only linear is learned. 'feature-based learning' as mentioned in BERT), zero-shot learning, end-to-end finetuning to SOTA