---
title: "Sigmoid Loss for Language Image Pre-Training"
date: 2024-03-12
tags: ['25min', 'CLIP', '2023Q1']
paper: "https://arxiv.org/ftp/arxiv/papers/2303/2303.15343.pdf"
issue: 164
issueUrl: "https://github.com/long8v/PTIR/issues/164"
summary: "Regarding CLIPScore, is the score of SigLIP much different from the one trained with softmax? I'm curious about the loss part and the effect - sigmoid loss suggestion. Various ablation experiments."
---
<img width="981" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f0ae6e83-f4b8-4d63-a167-5bd050db47b4">

[paper](https://arxiv.org/ftp/arxiv/papers/2303/2303.15343.pdf), [code](https://github.com/google-research/big_vision)

## TL;DR
- **I read this because.. :** Regarding CLIPScore, is SigLIP's score much different from the one trained with softmax? I was curious about the loss part and its effect.
- **task :** CLIP
- **problem :** The softmax in the InfoNCE function is learning unstable, and the process of summing negative pairs in the denominator involves all-gather, which causes learning inefficiency.
- **idea:** sigmoid loss suggestion. See more below
- **input/output :** {image, text} -> score
- **architecture :** ViT-B/16, (LiT setting) ViT-B/8, ViT-g/14
- **objective :** Sigmoid Loss
- **baseline :** CLIP, OpenCLIP, EVA-CLIP, CLIPA-v2
- **data :** WebLI dataset using only English image and text pairs
- **evaluation :** ImageNet-1k / COCO R@1 
- **result :** Better performance than the comparison group.  Data is different. ㅋㅋ 자세히 못봤지만 step수 맞았겠죠....
- **contribution :** Sigmoid loss proposal. Various ablation experiments.
- **etc. :**

## Details
### Sigmoid Loss
Existing InfoNCEs
<img width="448" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a2026a48-3f24-4084-a323-07edbdf331b1">

Here, the summation is done twice with each axis for image -> text / text -> image.

<img width="350" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/87b87103-71d4-455c-b301-1df8b13ce7f3">

Proposed sigmoid loss, where $z_{ij}$ is a label that is 1 for positive and -1 for negative.
Since there are too many negatives, we put $t'$, $b$ to solve the imbalance, which is initialized to log10 and -10.

At first glance, I wonder if it's different from the softmax operation because it needs to calculate all negatives.
<img width="979" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4b694b37-bd4f-4d5e-9d92-8eebf3cf1337">

Chunking in this way means that for softmax, we need to all_gather the features to compute the denominator. However, for sigmoid loss, the negative pair is included in the loss, but we don't need the negative pair for the positive pair, so we can just chunk it and forward it, which is more efficient.

<img width="700" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e6cc8dab-249c-491b-a773-83db69d49931">

Better than softmax on LiT settings, better than softmax for moderately small bs on just CLIP settings.

### Performance

<img width="350" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3f7c1945-d072-433c-92db-f447e5ea4b84">

<img width="695" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/11554026-aa35-4d68-920b-f08e292a2994">


### Ablations
<img width="692" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8bd9aa8d-a39b-4ad3-a957-8ea82452e14e">

Said to be more robust to perturbations

<img width="694" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9d6ecb2b-1967-498c-ac1c-bfab9be51e1e">

- hard: a strategy for masking hard samples
- Hard, matched pairs: masking reduces the number of pairs you actually see when training, so you'll have a smaller sample size

Wondering if there's a better benchmark for hard negatives
