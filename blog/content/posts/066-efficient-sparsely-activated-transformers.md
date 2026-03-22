---
title: "Efficient Sparsely Activated Transformers"
date: 2022-09-02
tags: ['MoE', '2022Q3', '25min', 'AutoML']
paper: "https://arxiv.org/pdf/2208.14580.pdf"
issue: 66
issueUrl: "https://github.com/long8v/PTIR/issues/66"
---

![image](https://user-images.githubusercontent.com/46675408/188034202-71ddef7d-3317-4e0e-8ee0-84480a3ec0b8.png)

[paper](https://arxiv.org/pdf/2208.14580.pdf)

## TL;DR
- **task :** lanugage modeling
- **problem :** The transformer is too large and heavy. It would be nice to have the network configure itself to meet the inference latency goal.
- Idea:** Design FFN, MHA, MoE FFN layer of Transfomer-XL given the latency of NAS writing.
- **architecture:** Transformer-XL, using GumbelSoftmax when NAS selects blocks + reinforcement based search.
- **objective :** cross-entropy loss + latent loss (= probability of each super block being selected and the latency of that super block), with latency loss only added if it is higher than the target latency.
- **baseline :** Transformer-XL, PAR Transformer, Sandwich Transformer
- **data :** wt103, enwiki8
- **Result :** 2x faster latency for similar performance. Higher normalized latency compared to PPL for the same size model with MoE in iso-parametric setting.
- **contribution :** NAS for inference latency 
- **limitation or something I don't understand :** MHA doesn't want to touch MoE...it says wuzzling -> runtime overhead introduced by dynamic behavior, but I don't know what it means.

## Details
- latency for each layer of the transformer
![image](https://user-images.githubusercontent.com/46675408/188034371-070796c9-2cba-46fe-8284-44eb1c5d97dd.png)

- MSA / FFN Comparison of latency when changing each hyperparameter
![image](https://user-images.githubusercontent.com/46675408/188034413-343792ea-f36a-4d6b-8235-6e9c8f798032.png)

- Model architecture configurations discovered by the NAS
![image](https://user-images.githubusercontent.com/46675408/188034380-9391629d-6551-4b21-af08-4e811abffa8e.png)

Reducing the number and dimension of MHA layers and adding MoEs or FFNs.

- MoE
![image](https://user-images.githubusercontent.com/46675408/188036741-7b5d2c76-a45c-4be8-a7cc-5341fa68cf15.png)

- search space for NAS
![image](https://user-images.githubusercontent.com/46675408/188036769-8b71ca8e-2166-4431-ba98-e1c2be035ca0.png)
