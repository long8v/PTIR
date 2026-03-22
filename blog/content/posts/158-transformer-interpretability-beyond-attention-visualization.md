---
title: "Transformer Interpretability Beyond Attention Visualization"
date: 2024-02-06
tags: ['2020Q1', 'CVPR', 'XAI']
paper: "https://arxiv.org/abs/2012.09838"
issue: 158
issueUrl: "https://github.com/long8v/PTIR/issues/158"
summary: "a.k.a TiBA. interested in explainable CLIP score. read as preliminary - as if explainabity in transformer is a slow process with attention flow."
---
<img width="733" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6c23907b-1b41-4d51-bcc8-c09c7ff270ef">

[paper](https://arxiv.org/abs/2012.09838), [code](https://github.com/hila-chefer/Transformer-Explainability)

## TL;DR
- **I read this because.. :** a.k.a TiBA. interested in explainable CLIP scores. read as preliminary
- **task :** interpertability of neural network
- **problem :** Applying the existing Layer-wise Relevance Propagation (LRP) method to a transformer requires (1) skip-connection and (2) ReLU is not used in activation, resulting in a negative result.
- Idea :** (1) change it so that both positive and negative are interchangeable, (2) add a normalization term, and (3) combine the attention and relevancy scores to get a score.
- **input/output :** image -> class // heatmap in image
- **architecture :** ViT-B, BERT
- **baseline :** rollout, raw attention, GradCAM, LRP, partial LRP
- **data :** ImageNet 2012, ImageNext-Segmentation, Movie Reviews
- **evaluation :** AUC(perturbation tests), pixel accuray / mAP / mIoU(segmentation), token-F1(Movie Reviews)
- **result :** Good performance compared to before
- **contribution :** explainabity in transformer is slow with attention flow
- **etc. :** When I read it, I recognized the person who explained it in the CVPR tutorial in the past! Also, when I looked for the paper, there was Ms. Kim who was in the XAI side, but she was a Korean woman, so I was glad to see her.

## Details
### Method
<img width="487" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ded80395-6445-48fc-bcf7-02d9fda49802">

The goal is to get the LRP-based relevance for each attention head in the transformer and combine it with the gradient for class-specific visualization.

#### Relevance and gradients
The gradient of $y_{t}$ (the output of the model for class t) over $x_j^{(n)}$, index j of input x of the nth layer by the chain rule, is defined as follows

<img width="369" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5bf5b064-94f1-4df9-907f-df92dc3114a3">

If we define $L^{(n)}(X, Y)$ as a layer operation on two tensors X, Y, then the two tensors become feature map / weight, and if we subject them to the Deep Taylor Decomposition, the relevance is obtained as follows.

<img width="387" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4e25c16a-8ffd-4f30-9bd8-b983e482c85c">

deep taylor decomposition uses taylor approximation to find relevance http://arxiv.org/abs/1512.02479
<img width="299" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/73eeb0a5-3f92-4174-b537-7eef77ddc6e6">

Approximating low output with a gradient~ Understanding only to a point

The conservative rule dictates that the sum of the relevance of the nth layer and the sum of the relevance of the (n - 1)th layer must be equal.
<img width="226" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a88d1c11-626f-4184-ba0d-03c02f65f0be">

This also comes from the paper above, and means that f(x) equals the sum of relevance.
<img width="394" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/68b2a3d6-a404-4acf-98a0-8f3d1e91a1db">

The LRP paper assumes ReLU as activation, so we only see positive values
<img width="453" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/45e59250-01e7-428a-82e0-d7515b4c31d4">

- $v^+$ : max(0, v)

But if you use something like GeLU, you can get negative results.
So I changed this to ask for kids that are just a postivie subset (...? I don't know what difference this makes)
<img width="392" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f4c11814-6d96-4022-a44d-43e690fa91a4">
<img width="189" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/55ac8076-54fe-42f9-a212-2ea801361179">

And set the very first initialization to a one-hot vector for class t

### non parametric relevance propagation
transformer has two operations that mix two feature map tensors (<=> before it was weight and feature map, which is different)
(1) skip connection (2) matrix multiplication

Given two tensors u, v, we define the two operators as follows
<img width="540" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/dd348b39-fd03-43fd-bb0a-d6be1c0e1e8c">

relevance score for leading u / relevance score for trailing v
relevance score tended to be too large on skip connections. To fix this, we added normalization

<img width="533" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0f225378-eca5-4367-9ea3-fa1812dd2470">

###  Relevance and gradient diffusion
<img width="521" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/acc4dc19-fbb2-47ae-aee9-5fe5f7c5da83">

If you use the above procedure for the self-attention operation, you will get the following result
<img width="348" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/679b6039-9330-41ba-8da9-69d211cf4018">

$A^{(b)}$ : attention map of the bth block
$E_h$: Average for heads dimension
Leaves only the positive part of the gradient.

For rollout, it simply iteratively multiplies over the attention map

<img width="479" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/595714b3-0c49-4aa5-ad8a-911eb937d78a">

### Obtaining the image relevance map
The result is a matrix C of s x s.
Each row shows how that token relates to other tokens in the relevance map
Since we only focused on the classification model in this study, we only get the relevance score for `[CLS]' token
For ViT, the sequence length s is subtracted from `[CLS]` and resized as $\sqrt{s-1} \times \sqrt{s-1}$ to resize and then interpolate to get

### Result
- qualitative
<img width="689" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9648a00d-ea19-4f8c-912d-807184cd9bc6">


- pertubation
<img width="694" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e282d2f9-bfb8-4aad-866c-caa9ca95863d">

See how the top-1 accuracy changes by masking out the ones you said were important, with positive being a gradual erasure of the important ones (lower is better).

- segmentation
<img width="679" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c882cd7a-85a3-4939-ad7a-87bc5b13b403">


- token-f1
<img width="405" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6f524055-8aa4-4bf7-9da2-b033934e1b03">

