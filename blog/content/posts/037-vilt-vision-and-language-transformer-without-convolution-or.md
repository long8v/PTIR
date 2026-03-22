---
title: "ViLT: Vision-and-Language Transformer Without Convolution or Region Supervision"
date: 2022-06-28
tags: ['multimodal', '2021Q2', 'naver']
paper: "https://arxiv.org/pdf/2102.03334.pdf"
issue: 37
issueUrl: "https://github.com/long8v/PTIR/issues/37"
---
![image](https://user-images.githubusercontent.com/46675408/176077410-1ff5fe50-f2bb-49dd-a84b-35013951ecd9.png)

[paper](https://arxiv.org/pdf/2102.03334.pdf), [code](https://github.com/dandelin/vilt)

## TL;DR
- **task :** Vision-and-Language Pretraining(VLP) 
- **problem :** In the existing VLP, CNN backbone, object detector are required and visual encoder is heavy, which is good for performance but not suitable for real application.
- Idea :** Create a unified VLP model without CNN.
- architecture :** visual embeddings like ViT and word embeddings like BERT. The embeddings from each encoder are combined with their modal-type embeddings and put into a single transformer encoder and trained with the output as the pretraining task below.
- **objective :** Image Text Matching (replace an image in an image-text pair with another image with 50% probability and learn binary whether the original pair is correct), MLM, whole word masking (masking the original word, not token by token. Masking only the center in `gi`, `##raf`, `##fe` allows prediction based on textual information without visual information).
- **baseline :** ViLBERT, UNITER, PixelBERT ... 
- **result :** time(ms) by 4-60x over the benchmark, while also improving performance by a factor of a
- **contribution :** 1) Improved runtime/efficiency by making it without deep visual encoder 2) Similar performance with simple architecture without region features or deep convolution 3) Showed that word masking, image augmentation improve VLP performance
- **data :** (pretraining) MSCOCO, Visual Genome, [SBU captions](https://www.cs.virginia.edu/~vicente/sbucaptions/), Google Conceptual Captions 
![image](https://user-images.githubusercontent.com/46675408/176082305-b7b3d3e3-e7ea-4b7a-a4d6-47d9cd3fbb42.png)
(downstream)
VQA v2, NLVR2 (Natural Language for Visual Reasoning, binary classification when given two images and a relationship between them (triplet) and given a question,)
Retrieval MSCOCO, Flickr30k for image-to-text, text-to-image retrieval

## Details
![image](https://user-images.githubusercontent.com/46675408/176084187-1146128d-f6b9-4d1d-b904-62fd5f3dd3fc.png)
