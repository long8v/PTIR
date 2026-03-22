---
title: "Long-tail Detection with Effective Class-Margins"
date: 2022-11-08
tags: ['2022Q3', 'imbalance', 'ECCV']
paper: "https://www.ecva.net/papers/eccv_2022/papers_ECCV/papers/136680684.pdf"
issue: 84
issueUrl: "https://github.com/long8v/PTIR/issues/84"
summary: "no hyper-parameter for long-tail problem"
---
<img width="649" alt="image" src="https://user-images.githubusercontent.com/46675408/200503141-76c3e6e3-39a1-4df8-b1a6-23b3ac74ed41.png">

[paper](https://www.ecva.net/papers/eccv_2022/papers_ECCV/papers/136680684.pdf), [code](https://github.com/janghyuncho/ECM-Loss)

## TL;DR
- **task :** long-tail object detection 
- **problem :** COCO data is annotated with long-tail and trained accordingly, but the evaluation metric, mAP, is AUC, so there is a gap.
- **idea :** Optimize this by replacing mAP probabilistically and bounding it by a weighted version of the pairwise ranking error under class-margin bounds in detection (=measuring the frequency with which negative sample x' ranks higher than positive x).
- **architecture :** Mask R-CNN, Cascade Mask R-CNN
- **objective :** ECM loss
- **baseline :** CE Loss, Federated Loss, Seesaw Loss, LOCE loss
- **data :** LVIS v1, Open Images
- **result :** SOTA
- **contribution :** no hyper-parameter for long-tail problem
- **Limitations or things I don't understand :** I don't understand all the formulas. It says there is no penalty effect for duplicate object. Doesn't it work with DETR?

## Details
### related work
#### Long-tail Detection related work
- Approaches that implicitly/explicitly re-weight losses, as most of the literature does.
- Equalization loss: how to remove negative gradients for rare classes
- Assumption that rare classes are discouraged by negative gradients of other classes
- Balanced Group Softmax (BaGS): divides groups by frequency in the training set and gets softmax + cross-entropy from there
- federated loss: computes only the negative gradient of the class from the image
- Equalization Loss V2: Trying to match the cumulative ratio of positive/negative by class
- SeeSaw loss: reduces weight for negative gradients in rare classes with high frequency

#### Learning with class-margins
- It sounds like face-recognition, and it's used a lot.
- [Learning Imbalanced Datasets with Label-Distribution-Aware Margin Loss](https://arxiv.org/pdf/1906.07413.pdf)

### Key Developments
- preliminary:  class-margin bound
<img width="377" alt="image" src="https://user-images.githubusercontent.com/46675408/200532714-e033a452-6192-4700-b942-44e0e24b1477.png">

As if finding the class loss with margin means the loss is smaller than just finding the class loss? This formula is proven in another paper

- Decision Metrics : mAP
<img width="434" alt="image" src="https://user-images.githubusercontent.com/46675408/200532775-dadd1d09-ff25-4266-b6d4-30c74954cf0d.png">

Replace this with probabilistic, which would look like this
<img width="416" alt="image" src="https://user-images.githubusercontent.com/46675408/200533031-5ba032e3-a9c1-4159-a1e1-4dd0c71769b1.png">

This can be bounded by a weighted pair-wise ranking error with a class margin bound
<img width="314" alt="image" src="https://user-images.githubusercontent.com/46675408/200535069-41d3ad42-e005-4846-a614-29a4af09703a.png">

In this case, the pair-wise ranking error is the frequency with which negative sample x' is ranked higher than positive sample x.

where the ranking loss can also be bounded by a binary error with a threshold added
<img width="310" alt="image" src="https://user-images.githubusercontent.com/46675408/200533923-2eb6f571-b3aa-4be8-b05c-54f56feaa8db.png">

How to organize this expression... Combined with the class-margin bounds above, this gives the tightest margin
<img width="281" alt="image" src="https://user-images.githubusercontent.com/46675408/200534935-01abcad0-cbf0-47f1-8aa7-2e89981120ee.png">

To recap, we want to minimize the margin-based error, which means applying a sigmoid whose threshold is the margin rather than 0.5, and the
<img width="386" alt="image" src="https://user-images.githubusercontent.com/46675408/200534048-4130b117-c996-44d6-bf73-f7c05c927f0b.png">

- where $m_c$ is the value for bounding the ranking error, which is also expressed as bound
<img width="487" alt="image" src="https://user-images.githubusercontent.com/46675408/200537875-26ccbb79-b413-455a-9394-a2d701248c59.png">

In this case, the score function is a weighted sum with the tightest margin
<img width="355" alt="image" src="https://user-images.githubusercontent.com/46675408/200536374-67c2f07e-25af-46f3-be4a-af8d0273dfeb.png">

### Results
<img width="496" alt="image" src="https://user-images.githubusercontent.com/46675408/200537919-471e9f24-7051-49b9-9bf4-f59ba5ab4afa.png">
