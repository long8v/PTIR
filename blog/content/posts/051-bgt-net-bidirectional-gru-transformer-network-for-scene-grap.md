---
title: "BGT-Net: Bidirectional GRU Transformer Network for Scene Graph Generation"
date: 2022-08-03
tags: ['2021Q4', 'SGG', 'graph']
paper: "https://arxiv.org/pdf/2109.05346.pdf"
issue: 51
issueUrl: "https://github.com/long8v/PTIR/issues/51"
---
![image](https://user-images.githubusercontent.com/46675408/182501380-7d17e1f2-c3db-4ef8-bc05-5f4070b520ae.png)

[paper](https://arxiv.org/pdf/2109.05346.pdf)

## TL;DR
- **task :** two-stage SGG
- **PROBLEM :** Let's learn objects and the relationships between them well.
- **idea :** Let's use bi-GRU to communicate between objects.
- **architecture :** FasterRCNN for objects and visual / coordinate / class features and put them into bi-GRU. Put the hidden output for each object into a transformer encoder. Predict relation by pruning and frying for n(n-1) pairs of objects.
- **objective :** cross-entropy loss
- **baseline :** Neural Motif, IMP, Graph R-CNN
- **data :** Visual Genome
- **result :** SOTA
- **contribution :** Not sure.
- **Limitations or things I don't understand :** If you make n region proposals, you'll get $O(n^2)$ as many

## Details
### Architecture
![image](https://user-images.githubusercontent.com/46675408/182502012-023b78c7-e36f-41f2-9386-999ecf157b93.png)

object proposal to predict a relation, which is described in Section 3.3 BA.
$d = W_p * u_{i,j}$
- $u_{i,j}$ union feature of a 2048-dimensional subjet-object pair? It doesn't say how it was created.

$p_{i,j} = softmax(W_r(o_i'*o_j'*u_{i,j}) + d \odot \tilde p_{i->j}$

- $\odot$ is the HadaMard Product
- is
![image](https://user-images.githubusercontent.com/46675408/182503496-f50517f8-ce7a-4ab9-8250-53bee9b345d3.png)

Finally, argmaxed to get the relation.
![image](https://user-images.githubusercontent.com/46675408/182503536-099f0952-7028-43fb-a046-d8649797a596.png)
 
#### Frequency Softening 
Since the VG dataset is long-tailed, take the log of the probability of the last softmax step
![image](https://user-images.githubusercontent.com/46675408/182502545-695d98a1-9ab4-4135-9a9f-d11519a4321e.png)



### Results
![image](https://user-images.githubusercontent.com/46675408/182502220-47f9e0a4-7e3b-4e86-8179-a983f94259ec.png)
