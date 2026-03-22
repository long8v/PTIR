---
title: "Hyperbolic Image-Text Representations"
date: 2023-09-26
tags: ['ICML', 'CLIP', '2023Q2', 'meta']
paper: "https://arxiv.org/abs/2304.09172"
issue: 144
issueUrl: "https://github.com/long8v/PTIR/issues/144"
summary: "Mentioned. there can be multiple texts representing one image. Ambiguity about this?!(Song Kang-ho, actor, man) - probably first work with CLIP in hyperbolic space?"
---
<img width="715" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a9219b68-f1ad-4ad7-bf87-d4521f817143">

[paper](https://arxiv.org/abs/2304.09172), [code](https://github.com/facebookresearch/meru)

## TL;DR
- **I read this because.. :** It is mentioned that there can be multiple texts representing one image. ambiguity about this?!(Song Kang-ho, actor, man)
- **task :** contrastive learning 
- **problem :** Text can be represented at different levels for one image (`dog standing on snow`, `puppy`, `giggle~`)
- **idea :** Let's move CLIP's embedding space to hyperbolic space instead of euclidean space.
- **input/output :** image/text -> score
- **architecture :** Same as CLIP
- **objective :** contrastive + entailment loss 
- **baseline :** CLIP trained with YFCC-100M(by SLIP)
- **data :** YFCC-100M
- **evaluation :** image text retrieval, zs-image classification
- **result :** Improved performance. The text traversed for [ROOT] on certain images became more generic.
- **contribution :** Probably the first work with CLIP in hyperbolic space?
- **etc. :**

## Details
### Motivation 
<img width="408" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/dbf3ae16-51f5-4e87-bd9f-9d8d76635547">


### Arch
<img width="388" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f935c80e-67c5-4932-876d-72f5b9a642f6">


### Lifting embeddings onto the hyperboloid
After passing through the CLIP encoder, each image and text vector comes out as an n-dimensional vector, and we apply a transformation that adds an origin 0 vector to it.
Let $v =[v_{enc}, 0]\in\mathbb{R}^{n+1}$ enter the tangent space of origin O, which satisfies the condition that it is zero and injective to zero.
We only need to compute over the space of Lorents models.
In that case, the exponential map (map vectors projecting from tangent space -> manifold) for x vectors is organized as follows.
<img width="315" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7c3d4554-2428-4b6f-a9d2-450fed946a75">

<img width="234" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0db991b1-075e-4a9c-b26e-9479f92ededd">

This means that if you take the embedding from the CLIP encoder and apply that transformation, you will end up in hyperbolic space.

The Lorents inner product is shown below, so we can use the inner product to get the similarity and add the contrastive loss
<img width="259" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/08d5c01a-a940-45b3-9a06-ba4fb29ed122">


### Entailment loss
<img width="338" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c484e682-93c8-46ec-9502-5ca4a473fe44">

Add the following loss to the contrastive loss
I'm not sure I understand the math, and my intuition for adding this loss is that when you have a {Text-image} pair, the text should entail the image.
<img width="227" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9b96acb0-23a7-41b9-9166-787401312beb">

<img width="344" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b8c08755-2b08-46ad-b01b-1609426eca71">

## Results
<img width="827" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d48d9d71-091b-484c-8aa3-ac49ada63eb3">

<img width="409" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8c16b0b2-08cc-4e29-b609-1437d5e5b94a">

- Text is more generic and widely distributed
- The two spaces are completely separate

### Ablations
<img width="411" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4bf0110a-5b2f-4f72-aafc-ece205095737">
<img width="402" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/313e6e78-1535-47bc-ac98-cb8c1475f2a9">


### Image Traverse
<img width="830" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b07c7eee-cf0d-4b75-90fb-9d929cc78564">
