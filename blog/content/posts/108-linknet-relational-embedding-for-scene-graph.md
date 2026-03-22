---
title: "LinkNet: Relational Embedding for Scene Graph"
date: 2023-01-18
tags: ['NeurIPS', '2017', 'SGG']
paper: "https://arxiv.org/abs/1707.03718"
issue: 108
issueUrl: "https://github.com/long8v/PTIR/issues/108"
summary: "SGG two-stage initial paper - simple !"
---

![image](https://user-images.githubusercontent.com/46675408/213080672-ab8303f9-c05f-4748-ac9e-9dbcdb669668.png)

[paper](https://arxiv.org/abs/1707.03718)

## TL;DR
- **I read this because.. :** SGG two-stage early papers
- **task :** two-stage SGG
- **problem :** One of the previous studies. Before this paper, I think there was neural motfis, #104, SGG with iterative message passing, etc.
- **idea :** Make each object an enhanced embedding to predict!
- **architecture :** Faster-RCNN + Create an embedding representing the object and use it to classify relation cls for $O(n^2)$ pairs. Global features + embeddings for cls drawn by od + RoI visual features + relative geometric information.
- **objective :** 1) multi-label loss of object class at image level 2) cls loss for each object 3) relation classification loss
- **baseline :**  neural motfis, #104, SGG with iterative message passing 
- **data :** Visual Genome
- **evaluation :** SGdet, SGcls, PredCls
- **result :** sota
- **contribution :** simple !

## Details
### Architecture
![image](https://user-images.githubusercontent.com/46675408/213084978-cd97c25a-3d7f-4183-9e81-c924e216093a.png)

- Global Context Encoding Module
AvgPool for feature followed by FC for multi-label classification

- Relation Embedding Module 
To create an objective feature $O_i$, we use the embedding of OD's predicted cls $l_i$, features drawn from RoI pooling, and the image-wide context feature $c$ to create the embedding, and stack FCNs to predict cls.

![image](https://user-images.githubusercontent.com/46675408/213085357-635b889e-0b3b-46c5-82fc-2705dd5896c9.png)

![image](https://user-images.githubusercontent.com/46675408/213085624-2078a27e-04b5-4b22-910e-9ca6f0b08457.png)

![image](https://user-images.githubusercontent.com/46675408/213085664-2b418863-fde0-428d-a028-1a911dc57920.png)

Include geometric features when getting a relation
![image](https://user-images.githubusercontent.com/46675408/213085699-659b7f28-23b3-47fd-8936-0528bff1bcb6.png)

### Loss
![image](https://user-images.githubusercontent.com/46675408/213085803-edc0d96a-ef81-4129-aaf0-72acd297ce08.png)


### Result 
![image](https://user-images.githubusercontent.com/46675408/213085764-89a5bb0d-691b-4dfc-b2d1-f4c19197fb2c.png)
