---
title: "[126] ViLT: Vision-and-Language Transformer Without Convolution or Region Supervision"
date: 2023-08-09
tags: ['multimodal', '2021Q1', '25min', 'kakao']
paper: "https://arxiv.org/pdf/2102.03334.pdf"
issue: 138
issueUrl: "https://github.com/long8v/PTIR/issues/138"
summary: "I tried to read fine-grained CLIP and saw it quoted. - Minimize complex design for each modality"
---

<img width="892" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4da317f3-56b6-4c18-857d-6a37a67e8883">

[paper](https://arxiv.org/pdf/2102.03334.pdf), [code](https://github.com/dandelin/vilt) 

## TL;DR
- **I read this because.. :** fine-grained CLIP I tried to read it, saw it was quoted, and read it.
- **task :** VLM model -> VQAv2, NLVR2, retrieval
- **problem :** Selecting and training features with image -> CNN -> region takes too long.
- **idea :** Let's just put the projection directly into the multi-modal Transformer after patching like ViT and use it.
- **input/output :** {image, text} -> matching score, masked token prediction
- **architecture :** Transformer encoder 
- **objective :** Image-Text matching, 
- **baseline :** pixelBERT, ViLBERT, OSCAR, VisualBERT
- **data :** MSCOCO, VG, GCC, SBU
- **evaluation :** evaluation for each
- **result :** 10x faster runtime reduction and similar or better performance
- **contribution :** Minimized complex design for each modality.
- **etc. :**

## Details
### Motivation
<img width="423" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2434236b-82b9-41ed-9e0e-a7d9733489da">

<img width="825" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b42d1d83-f725-4def-8ea6-aeec1bcd16b6">


### Word Patch Alignment
<img width="170" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/239ee8f0-9426-4622-b88e-a92b39cc6e62">

What's going on here?
This is almost the same as the previous [UNITER: UNIVERSAL Image-TExt Representation Learning](https://arxiv.org/pdf/1909.11740.pdf), except we used patch instead of region.
<img width="308" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/df6e618c-5360-46ee-bea9-617fbf881cd2">

We don't give direct word-region supervision, but we use an algorithm called [Optimal Transport] (https://en.wikipedia.org/wiki/Transportation_theory_(mathematics)) to find the cost of minimizing the transport between image embedding and word embedding, and add it as a loss to get better alignment.

<img width="707" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f2c8e029-6bee-4ffd-bb67-5c5c510b5216">

- c: distance. using cosine similarity.
- $T\in \mathbb{R}^{T\times K}$ : transport plan. learned to optimize alignment between $w$ and $v$. learned to optimize alignment between $w$ and $v$. Learned to optimize alignment between $w$ and $v$.

The difficulty here is how to find this minimum distance, so we approximate it with a complicated method called IPOT, which approximates the wasserstein distance.
This partial implementation can be found [here](https://github.com/dandelin/ViLT/blob/762fd3975c180db6fc88f577cf39549983fa373a/vilt/modules/objectives.py#L38-L87)

<img width="851" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/aebe332a-f82e-472f-b367-87cac0dc0188">

This result -> Is it because of WPA?
