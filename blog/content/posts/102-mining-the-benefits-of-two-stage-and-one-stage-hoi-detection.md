---
title: "Mining the Benefits of Two-stage and One-stage HOI Detection"
date: 2022-12-29
tags: ['2021Q2', 'NeurIPS', '25min', 'HOI']
paper: "https://arxiv.org/pdf/2108.05077.pdf"
issue: 102
issueUrl: "https://github.com/long8v/PTIR/issues/102"
summary: "I was going to read the RLIP of NeurIPS 2022, but this is a preliminary study, so I read it. - SOTA. 9.32% improvement on HICO-Det"
---
<img width="740" alt="image" src="https://user-images.githubusercontent.com/46675408/209899558-d0dea062-46f7-4b65-ac63-deae8201fb23.png">

[paper](https://arxiv.org/pdf/2108.05077.pdf)

## TL;DR
- **I read this because.. :** I was going to read the RLIP of NeurIPS 2022, but this is a preliminary study.
- **task :** Human Object Interaction(HOI)
- **problem :** Disadvantages of two-stage HOI 1) Time complexity is high because M x N pairs of M people and N objects are used for action classification 2) Imbalance because few of M x N have actual relation 3) The feature that draws the bounding box focuses on the edge rather than the content of the object, so the performance is not good if the relation is used to predict <-> Disadvantages of one-stage HOI : It is difficult to generalize because it tries to solve two different tasks with one feature representation.
- **idea :** go one-stage but separate the decoders. One Human-Object Pair Decoder that asks an object query and gets a `human-object-interaction score`, and one Interaction Decoder that takes the output representation from that decoder and categorizes the action class.
- **architecture :** DETR
- **objective :** detr loss + bce for interaction score (1 if relationship exists, 0 if not)
- **baseline :** QPIC, AS-Net, HOTR, ATL, ...
- **data :** HICO-Det, V-COCO
- **evaluation :** mAP for triplet (must be IoU 0.5 or higher to fit box)
- **result :** 9.32% improvement on SOTA. HICO-Det
 
## Details

<img width="1442" alt="image" src="https://user-images.githubusercontent.com/46675408/209900098-1236e8c4-41c6-45f2-9b68-bb159c1917d6.png">

<img width="756" alt="image" src="https://user-images.githubusercontent.com/46675408/209900121-f3603fa4-6de4-491c-9395-0bef4a99d71f.png">

### Result
<img width="753" alt="image" src="https://user-images.githubusercontent.com/46675408/209900145-b72f6c26-3f62-47a8-b59e-ca3828f620d5.png">
