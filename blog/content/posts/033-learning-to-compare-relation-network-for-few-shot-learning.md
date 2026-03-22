---
title: "Learning to Compare: Relation Network for Few-Shot Learning"
date: 2022-05-31
tags: ['few-shot', 'zero-shot', '2018', 'CVPR']
paper: "https://arxiv.org/abs/1711.06025"
issue: 33
issueUrl: "https://github.com/long8v/PTIR/issues/33"
---
<img width="978" alt="image" src="https://user-images.githubusercontent.com/46675408/171096866-65d5c5be-d072-409d-b10b-093b197463f6.png">

[paper](https://arxiv.org/abs/1711.06025)

## TL;DR
**problem :** In an image classification task, I want a new class to perform well without any fine-tuning even if there are few data for it (few-shot classification).
**solution :** 1) Apply episode training to train with C classes as the support set and the remaining classes as the query set 2) Train an encoder that extracts features from the image and a relation module that combines the extracted query with the support and predicts whether the two vectors are related (0~1) 3) The loss is 1 if the two query-support sets come from the same class, or 0 and the MSE between the relation.
**result :** A unified, simple, effective architecture for few-shot / zero-shot while improving few-shot performance.

## Details

### episode training
<img width="483" alt="image" src="https://user-images.githubusercontent.com/46675408/171098141-376f8642-9334-466c-be13-168441829812.png">

### model architecture
<img width="816" alt="image" src="https://user-images.githubusercontent.com/46675408/171097841-9eea444b-75b9-46e1-b0ef-1f616b248d92.png">

<img width="358" alt="image" src="https://user-images.githubusercontent.com/46675408/171098808-95196aed-8e5d-4090-8c75-f2fd540e2e5d.png">

<img width="280" alt="image" src="https://user-images.githubusercontent.com/46675408/171098824-9655bde9-c531-4b44-b040-043780e39555.png">

### zero-shot learning
It is similar to one-shot in that we are given a single vector for a given class C, but unlike one-shot, the support set is not an image but a semantic class embedding (e.g., textual information in the case of CUB data). This means that the same case of zero-shot can be applied to ZSL by changing the support set to cover a separate modality.

### why effective? 
Previous studies have been ineffective because they only learn features and the metric is fixed to euclidean or cosine.

### result


