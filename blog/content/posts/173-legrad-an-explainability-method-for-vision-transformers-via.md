---
title: "LeGrad: An Explainability Method for Vision Transformers via Feature Formation Sensitivity"
date: 2024-05-06
tags: ['CLIP', 'XAI', '2024Q2']
paper: "https://arxiv.org/pdf/2404.03214"
issue: 173
issueUrl: "https://github.com/long8v/PTIR/issues/173"
summary: "Chefer sent me an email because I follow him in scholar (so convenient!) - A model with good use of all layers. Model scale shows different aspects of the model depending on the layer."
---

<img width="456" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4a1d0df5-c763-4096-b497-413d3b1c21dd">

[paper](https://arxiv.org/pdf/2404.03214), [code](https://github.com/WalBouss/LeGrad)

## TL;DR
- **I read this because.. :** I follow Chefer in scholar, so he sends me emails (so convenient!)
- **task :** explainability in CLIP
- Problem :** Explanatory Power in CLIP Models
- **IDEA :** Find the derivative for the hidden representation of all layers and use it to calculate the
- **input/output :** {image, text} -> layer explainability maps
- **architecture :** CLIP ViT-B/16, -L/14, -H/14, -BigG/14, SigLIP
- **baseline :** LRP, Partial-LRP, rollout, Raw attention, GradCAM, CheferCAM, TextSpan
- **data :** ImageNet-S, OpenImage V7, ImageNet(perturbation)
- **evaluation :** segmentation (pixel acc, mIoU, mAP), ov segmentation(p-mIoU), perturbation test(neg, pos accuracy)
- **result :** SOTA.
- **contribution :** A model that uses all layers well. Model scale shows different aspects of the model depending on the layer.
- I don't know why sensitivity is in the title, maybe it's because I'm just reading it roughly?

## Details
<img width="659" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/08a3d3a2-4f62-49fc-aded-962d968318e2">

### Methodology 
The final output of ViT looks like this
<img width="146" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c9fcb65a-bb2f-4d4c-b42b-a2e7c5b58d2d">

where $\bar{z}$ is the pooled representaion (cls pool, attention pool)
Of these, the activation for our target class $c$ is called $s$.
Let's call $A$ the attention map for this, and differentiate with respect to the attention map to get the following map
<img width="286" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b28b3aaf-40a5-4f03-b28d-a75a2fa46835">

Takes ReLU and averages it by layer / head / patch(n).
<img width="408" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/88c7caee-97a5-4e1c-9717-91b7ca301013">
 
Reshape again except for the cls token and do min-max normalization
<img width="367" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8915f440-0a78-4bf0-b983-a6f83213d6de">

Find $s^{l}$ for all layers in this way and create a map as a derivative of it
<img width="500" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c321b21c-e4d3-43bf-ae8b-3b7f2f63b82f">

<img width="432" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/584944f6-ce6e-4050-a3e9-b762116dfa9d">

This is summation, not matrix multiplication, per layer
<img width="326" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/734b8cdc-6e88-47b4-8cd3-2a0cc50cd35e">

What's different about Chefer 21? https://github.com/long8v/PTIR/issues/159#issuecomment-1933470637
- You don't differentiate on the final output, you differentiate on the representation and inner product of the layer! (Most major)
- image_relevance = R[:, 0, 1:] : LeGrad clears CLS tokens rather last, while chefer uses a representation for CLS tokens. For $n \times n$, LeGrad writes a summation over all the last rows, while chefer writes the one that got caught in CLS
- chefer has something to initialize with identity matrix to represent residual connection, but there is no such thing


### Result 
<img width="501" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8dc2afef-c520-46f1-83ed-381678b10b23">

#### Perturbation result 
<img width="488" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/982ff1e2-9e27-4907-b94f-64ae8501c9c8">

### Layer Ablation
<img width="578" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1d35783a-5137-4366-bfc9-5feb8d3a2c1b">

For small models, it was good to use only the last few layers, but as the model gets bigger, more layers should be used

<img width="595" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5bd8d595-b174-43b8-9f4c-90410b9fea70">

#### ReLU ablation
<img width="758" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a14eafbb-7cfa-4d0d-a222-4c4b0b48cfdc">

It was good to have ReLU on. Not having it on doesn't make it much worse.

#### Qualitative 
<img width="652" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/cde7599a-aef0-433b-983b-e3ab537ca989">

