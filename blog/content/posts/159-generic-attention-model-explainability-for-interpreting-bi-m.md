---
title: "[147] Generic Attention-model Explainability for Interpreting Bi-Modal and Encoder-Decoder Transformers"
date: 2024-02-07
tags: ['ICCV', '2021Q1', 'XAI']
paper: "https://arxiv.org/pdf/2103.15679.pdf"
issue: 159
issueUrl: "https://github.com/long8v/PTIR/issues/159"
summary: "aka. CheferCAM. interested in explainable CLIP scores. I published [colab](https://github.com/hila-chefer/Transformer-MM-Explainability?tab=readme-ov-file) in this paper repo and you can visualize results by token. - Cross-attention, co-attention also explainable work. ICCV oral."
---
<img width="800" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4e361620-0bf8-4a65-a970-ce13930e5619">

[paper](https://arxiv.org/pdf/2103.15679.pdf), [code](https://github.com/hila-chefer/Transformer-MM-Explainability)

## TL;DR
- **I read this because.. :** aka. CheferCAM. interested in explainable CLIP scores. published [colab](https://github.com/hila-chefer/Transformer-MM-Explainability?tab=readme-ov-file) in this paper repo and you can visualize the results by token.
- **task :** explainability in neural network
- **problem :** I want to do not only self-attention in the previous TiBA(https://github.com/long8v/PTIR/issues/158), but also co-attention, enocder-decoder structure in multi-modal environment.
- **idea :** write gradient for attention map instead of gradient for previous output (==LRP)
- **input/output :** model // heatmap for text or vision tokens
- **architecture :** ViT, VisualBERT, LXMERT, DETR
- **baseline :** rollout, raw attention, Grad-CAM, Partial LRP, TiBA
- **evaluation :** perturbation(both in image and text token for VisualBERT), weakly, semantic segmentation 
- **result :** Better performance than its predecessor
- **contribution :** cross-attention, co-attention work that also makes the work explainable. ICCV oral
- **etc. :** Before deep taylor decomposition is something tired, but if I ignore that and just read this paper, I don't need theoretical content and it seems clean... and the performance is good. On the contrary, there is no theoretical content, so it feels a bit clunky. In the case of CLIP, the final output is embedding, but then it seems that it is not a visualization for CLIPscore...? colab It seems like you need to look closely.

## Details
### some notation
- i is an image token
- T is a text token
- A^{tt}$ is the self-attention between texts / $A^{ii}$ is the self-attention between images
- Let $A^{ti}$ be the multimodal attention interaction

### Relevancy initialization 
We're going to initialize/update the relevancy map
<img width="204" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/259fbe15-c283-4b4b-b2f4-ea05ac3de234">

Before SA, they have no interaction with each other, so $R^{ii}$, $R^{tt}$ are identities. $R^{it}$ is a zero tensor.

### Relevancy update rules 
We'll update relavancy with attention map A
Average across heads and use gradient as per predecessor

<img width="191" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/15a4432f-5b48-48b0-a2f0-6e22090b0ced">

where $\delta A$ is the differentiation of $y_t$, the output for the class t we want to visualize, with A. Leave only the positives before taking the average (clamp) (there is no particular reason for this, it just follows its predecessor)
<img width="84" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/abbf39c8-a96e-4630-a0d5-15b00b83395f"> 

<img width="394" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/abbf6034-e02c-4f9a-9c90-a9bee83b37c1">

The relevance update for self attention works like this
where s is the query token and q is the key token.

Here, $R^{xx}$ can be separated into two parts: $I$, the initialization, and $\hat{R}^{xx}$, the residual after subtracting $I$.
Because $\hat{R}^{xx}$ uses a gradient, the numbers are absolutely small. To fix this, we normalize the rows so that they sum to 1.
<img width="243" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/90485988-dfe2-4213-888b-aa4308f4be17">

For co-attention / cross-attention, define the update rule as follows
<img width="265" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/eeb97b96-f622-47e0-9e39-4b9f031e7390">

### Obtaining classification relevancies
The relevancy map corresponds to the rows of the [CLS] token, for example, the first row of $R^{tt}$ for text and the first row of $R^{ti}$ for images.

### Adaptation to attention type
<img width="832" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3212fb8c-49f1-4323-b36e-6f4a1f5c1663">


- When tokens from both modalities are concatenated and enter the SA: can be made into a Relevancy map of rows ($R^{i+t}$) corresponding to [cls] tokens in the whole $R^{(i+t, i+t)}$.
- Both modalities are SA first and exchange information with each other as CAs (co-attention): The propagation described above must be done. The relavancy map can then be viewed in the same way as the relevancy in the classification model
- Encoder-decoder structure: cross-attention is only in one direction, so equation 11 is not needed

## Result
<img width="985" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/07e3b379-abdc-46a0-82b1-422cc600dcaa">

<img width="860" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1fc2e554-0807-4c48-a29b-8e479280c96d">
<img width="862" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/217c53f0-808f-438d-ad84-cc6887cc8ba4">
<img width="839" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/11211d48-c74b-47d2-9888-08656f8e1cb9">
<img width="838" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e6d338ae-adbf-4cc5-a2ce-52dc981913be">
