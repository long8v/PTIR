---
title: "[47] Recovering the Unbiased Scene Graphs from the Biased Ones"
date: 2022-08-05
tags: ['SGG', '25min', '2021Q3', 'imbalance']
paper: "https://arxiv.org/pdf/2107.02112v1.pdf"
issue: 53
issueUrl: "https://github.com/long8v/PTIR/issues/53"
---
![image](https://user-images.githubusercontent.com/46675408/182977423-ff4439ba-2b06-40f5-89c7-058e4b5a1004.png)

[paper](https://arxiv.org/pdf/2107.02112v1.pdf)

## TL;DR
- **task :** Scene Graph Generation
- **problem :** Due to the nature of SGG, it is a long tail distribution with a lot of unlabeled data and only certain relations appearing a lot.
- **idea :** Let's look at the problem from a [Positive-Unlabeled Learning](https://dodonam.tistory.com/370) perspective and divide the logit value by the frequency of all class labels.
- **architecture :** object detector + GNN?
- **objective :** cross entropy loss
- **baseline :** MOTIFS, ...
- **data :** Visual Genome, Visual Genome150
- **result :** It appears to be sgdet SOTA for the current VG150.
- Fix the **contribution :** long-tail issue
- **Limitations or things I don't understand :**

## Details
<img width="615" alt="image" src="https://user-images.githubusercontent.com/46675408/182978368-a2bdbdbd-1406-4746-bf91-f52d67377efc.png">

### Recovering the Unbiased Scene Graph
<img width="523" alt="image" src="https://user-images.githubusercontent.com/46675408/182980842-d955cef0-25a8-45bd-8b47-e15ffb4db486.png">

- s: labeled pred
- y : true pred
- r : target pred

unbiased probability 
<img width="357" alt="image" src="https://user-images.githubusercontent.com/46675408/182980885-acedbd82-7199-4840-8af8-c32658f6efd5.png">

If we assume that the probability of being labeled is independent of x (Selected Completely at Random, SCAR), we can write
<img width="326" alt="image" src="https://user-images.githubusercontent.com/46675408/182980898-650b529c-6081-446c-9904-a1e7fb7be2ed.png">

p(s=r|y=r) is eventually the ratio of labeled examples to the total class r.

### Dynamic Label Frequency Estimation
Get an estimate for p(s=r|y=r) above, i.e., the label frequency.
<img width="517" alt="image" src="https://user-images.githubusercontent.com/46675408/182981725-3db13055-f3e4-425c-9fb4-e0111b8f8df4.png">

This expression is derived from
![image](https://user-images.githubusercontent.com/46675408/182981942-34a99c05-cb17-47e2-9ab4-c973fb08969c.png)


We end up dividing the entire data by frequency by class -.-

1) it is difficult to obtain post-training estimates before inference and
2) For SGDET, there is no gt bbox, so it is difficult to estimate a valid example.

So we'll do data augmentation to get a vaild example for the tail class, and the label frequency will be estimated on a batch-by-batch basis.
We'll call this idea Dynamic Label Frequency Estimation (DLFE).
<img width="684" alt="image" src="https://user-images.githubusercontent.com/46675408/182981696-ea536cfd-96a4-48ee-92ee-77791c6a9fa6.png">


![image](https://user-images.githubusercontent.com/46675408/182977452-9e3e6f39-2137-4e0e-9c00-af1f773487bf.png)

![image](https://user-images.githubusercontent.com/46675408/182977574-55a1e9a6-0eee-426e-9365-cc63390bb1ee.png)
