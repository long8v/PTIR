---
title: "Grounding Language Models to Images for Multimodal Inputs and Outputs"
date: 2023-09-04
tags: ['ICML', '25min', '2023Q1', 'CMU']
paper: "https://arxiv.org/pdf/2301.13823.pdf"
issue: 141
issueUrl: "https://github.com/long8v/PTIR/issues/141"
summary: "https://github.com/long8v/PTIR/issues/139 mentioned while talking about it - adding new features with minimal training, no need to learn interleaved data like Flamingo!"
---
<img width="691" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5c146075-966f-4486-a01e-a76c3be238ba">

[paper](https://arxiv.org/pdf/2301.13823.pdf), [code](https://github.com/kohjingyu/fromage)

## TL;DR
- **I read this because.. :** https://github.com/long8v/PTIR/issues/139 was mentioned in a conversation about
- **task :** LVLM 
- **problem :** LIMBeR-like model that can output image -> model that can retreival in interleaved image-text
- **idea :** LIMBeR, but put a `[RET]` token at the end to make it retreivalable.
- **input/output :** image + text (concat at random with 50% probability) + image + text -> free form of text
- **architecture :** CLIP ViT-L/14 + OPT (6.7B) and train only `[RET]` with a linear function connecting the vision output (5.5M trainable parameter).
- **objective :** captioning loss + retrieval loss
- **baseline :** CLIP ViT-L/14, BLIP, Flamingo, ViLBERT, ESPER
- **data :** (train) CC3M -> (eval) VisualDialogue, Visual Story
- **evaluation :** IT2T(image/text-to-text, text-to-image)R@k, NDCG, MRR, story generation human evaluation 
- **result :** single retrieval performs worse than CLIP, but image - text
- **contribution :** Adding new features with minimal training, no need to learn interleaved data like Flamingo!
- **etc. :** CLIP text encoder is bidirectional, what does that mean? It started with CLIP, so I don't think it's that great to beat CLIP.

## Details

<img width="345" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e1af9eec-e962-4586-85bb-871e8583eeb7">


<img width="669" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/168151b4-a58b-4c38-b200-aa95d7227b8d">

<img width="590" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9b06db59-768d-4234-a7e7-20823d94a400">

<img width="306" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/54036873-145f-4623-af91-7fb393bdb510">

- result
<img width="305" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9253635f-5371-4831-bbe9-2c03fd10b900">

<img width="621" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1ea8b26c-970a-4e4e-b569-747f382dced4">

<img width="308" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/85115a9b-0a9e-4954-a618-7a8f3bf212dd">

<img width="309" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/595551c7-47e6-4d32-baee-69fbca3ed51f">
