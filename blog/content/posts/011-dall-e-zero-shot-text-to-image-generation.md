---
title: "[11] DALL-E : Zero-Shot Text-to-Image Generation"
date: 2022-02-07
tags: ['multimodal', '2021Q1', 'zero-shot', 'openAI']
paper: "https://arxiv.org/pdf/2102.12092.pdf"
issue: 11
issueUrl: "https://github.com/long8v/PTIR/issues/11"
---
![image](https://user-images.githubusercontent.com/46675408/154877540-b65707d5-3324-430b-bf8e-e51fbe4962ce.png)
[paper](https://arxiv.org/pdf/2102.12092.pdf), [article](https://openai.com/blog/dall-e/), [code](https://github.com/openai/dall-e)

## TL;DR
- **task :** zero-shot text-to-image generation
- **problem :** generation models increase model size, but text-to-image has limited data
- Idea :** Crawl the internet to create a huge text-image pair (MS-COCO) and increase the model size. Use discreteVAE to efficiently encode the images.
- **architecture :** encode images to code with discreteVAE + encode text to make it auto-regressive
- **objective :** cross-entropy loss
- **baseline :** AttnGAN, DM-GAN, DF-GAN
- **data :** 3.3M MS-COCO
- **result :** [FID](https://wandb.ai/wandb_fc/korean/reports/-Frechet-Inception-distance-FID-GANs---Vmlldzo0MzQ3Mzc)(=Frechet Inception Distance) for SOTA. overwhelmingly superior to DF-GAN in human evaluation.
- **contribution :** A very large image generation model.

## Details
- 12 billion parameters, dataset is 250 million text-image pair data
### Method
- Training on a pixel-by-pixel basis is 1) too computationally intensive, and 2) when likelihood is applied, it focuses on short-range relationships, modeling only high-frequency details and not human-identifiable low-frequencies.
- To solve this, we broke it down into two steps
- The first step uses a discrete VAE (dVAE) to divide the 256 x 256 RGB image into a grid with 32 x 32 image tokens, allowing each element to have 8192 values. This reduces the context size by a factor of 192 without significantly degrading the image quality of the transformer.
- After compressing with dVAE and reconstructing, the result is
![image](https://user-images.githubusercontent.com/46675408/152714226-be3a3a23-7377-4515-bef6-d305e0f62982.png)
- In the second step, 256 BPE-encoded texts were concatenated with 32 x 32 = 1024 image tokens to autoregressively learn text and images.
- These overall steps can be viewed as maximizing the evidence lower bound (ELB) of the joint probability between image x, caption y, and token z encoded in dVAE.
<img width="349" alt="image" src="https://user-images.githubusercontent.com/46675408/162875434-0a95508e-eabf-4579-bc6c-5e3f5f691a1d.png">
 
- In other words, if we factorize as above and get the ELB value of this value, it is as follows
<img width="514" alt="image" src="https://user-images.githubusercontent.com/46675408/162875698-fcb01cdd-8ca8-42f9-9431-b79fc1ea7f01.png">
<img width="476" alt="image" src="https://user-images.githubusercontent.com/46675408/162875921-895b7f8b-3910-43a6-8cb0-684dda028027.png">

- Interpreting the expression, the goal is to maximize the likelihood of the image given the caption and image token in the dVAE, while minimizing the KL divergence between the probability distribution of the caption text and image token given the image in the dVAE and the joint probability of the caption and image token given the image through the transformer.
- This is the theoretical ELB where beta should be 1, but in our experiments we found that it performed well at larger scales.

#### Step One: Learning the Visual Codebook
Train the dVAE by maximizing the ELB over $\phi$ and $\theta$.
The code is 32 x 32 in size with $K$=8192 and $p_\psi$ is uniformly distributed.
I used gumbel softmax to smooth out the gradient where the code was discrete and not differentiable.

The $p\theta$ was evaluated with a log-laplace (absolute value instead of squared at the exponential part of the normal distribution) distribution.

#### Stage Two: Learning the Prior
The text was BPE encoded to a maximum length of 256, and the image was argmaxed with dVAE encoder logit to get 1024 tokens.
We concatenated the two encodings and fed them into the transformer decoder, and if the text was smaller than 256, we trained each `[PAD]` token according to 256 positions. -> More robust to OOD catpions.
I used cross-entropy loss and multiplied the loss for text and images by 1/8 and 7/8.