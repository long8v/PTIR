---
title: "Masked Autoencoders Are Scalable Vision Learners "
date: 2022-09-07
tags: ['2021Q4', 'SSL', '25min']
paper: "https://arxiv.org/pdf/2111.06377.pdf"
issue: 69
issueUrl: "https://github.com/long8v/PTIR/issues/69"
---
<img width="957" alt="image" src="https://user-images.githubusercontent.com/46675408/188760840-4a2876df-1339-44f1-b844-5c1333e0220a.png">

[paper](https://arxiv.org/pdf/2111.06377.pdf)

## TL;DR
- **task :** self-supervised learning -> image classification / object detection / segmentation
- **problem :** I want to pretrain in a way that makes masked predictions like BERT
- **idea :** Let's do it like an autoencoder, and since images have less information in each token than text (we say spatial redundancy), let's make the mask ratio really high (75% in the paper) instead.
- **architecture :** encoder-decoder, where the encoder contains only unmasked tokens and the encoder output contains mask embeddings in their original positions, which the decoder sees and reconstructs. The encoder is ViT-L and the decoder can be of any choice, but in the paper we use a small decoder that requires about 10% of the computation of the encoder.
- **objective :** mean squared error (MSE) over masked tokens
- **baseline :** supervised learning, MoCov3, BeiT
- **data :** self-supervised pretraining with ImageNet-1K. followed by linear probing/finetuning. Finetuning with COCO, ADE20K, iNaturalists, Places.
- **result :** When transferred to another task, the SOTA
- **contribution :** simple architecture with strong result!
- **Limitations or things I don't understand :**

## Details
### Architecture
<img width="511" alt="image" src="https://user-images.githubusercontent.com/46675408/188760803-71943291-5d15-43d1-aceb-5b1203d1be37.png">

### Result
<img width="999" alt="image" src="https://user-images.githubusercontent.com/46675408/188761395-90e9d96b-8aee-4570-b6f4-124db1dc7eea.png">

better to noramalize target (normalize to the mean and variance of the entire patch)

### Comparison with other SSL methods
<img width="477" alt="image" src="https://user-images.githubusercontent.com/46675408/188761464-291fa39d-1ef8-4e8a-aa94-842732db02e3.png">

Increasing the mask ratio should also work.
<img width="494" alt="image" src="https://user-images.githubusercontent.com/46675408/188761572-4bdec991-e655-441f-a37c-0bb59468316e.png">
I can't believe I'm a zebra.

<img width="490" alt="image" src="https://user-images.githubusercontent.com/46675408/188761643-1c20261e-f6d2-4435-aa31-67f5d180f026.png">

But it works 75% of the time