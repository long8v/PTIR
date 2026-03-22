---
title: "[42] DETRs with Hybrid Matching"
date: 2022-08-01
tags: ['object detection', '2022Q3', '25min', 'DETR']
paper: "https://arxiv.org/pdf/2207.13080.pdf"
issue: 48
issueUrl: "https://github.com/long8v/PTIR/issues/48"
---
![image](https://user-images.githubusercontent.com/46675408/182053331-52075198-7268-4eb9-9f2b-b4bffae820f3.png)

[paper](https://arxiv.org/pdf/2207.13080.pdf), [code](https://github.com/HDETR)

## TL;DR
- **task :** object detection, pose estimation, object tracking, label assignment
- **problem :** Due to the part of DETR that does hungarian one-to-one matching (which saved me from having to do NMS and stuff), there are too many positive pairs to learn efficiently.
- **idea :** hybrid matching. do one-to-one matching and also do one-to-many matching (just copy gt multiple times). Do this for all layers like auxiliary loss.
- **architecture :** deformable DETR 
- **objective :** objective function for each task
- **baseline :** deformable DETR, PETR, 3DETR...
- **data :** ...
- **result :** Performance gain. The learning speed was about 65 minutes per epoch with one-to-one matching, and 85 minutes with hybrid matching.
- **contribution :** Improved performance with a simple trick.

## Details
### Different ways to do hybrid matching
![image](https://user-images.githubusercontent.com/46675408/182053840-433d8bdf-3ca3-45f1-b06d-f8c1b2e5c267.png)

### Results
![image](https://user-images.githubusercontent.com/46675408/182053914-072ce5da-ffbf-4656-9321-b492fd56b9ab.png)

![image](https://user-images.githubusercontent.com/46675408/182053941-8988aab6-e68d-45fd-b5b0-20bbac4c7bf2.png)

### related works 
[Group DETR: Fast Training Convergence with Decoupled One-to-Many Label Assignment](https://arxiv.org/pdf/2207.13085.pdf)
![image](https://user-images.githubusercontent.com/46675408/182054024-ba0dac94-7829-49a6-be48-d3df08f4d5cf.png)

When embedding query embeddings, you can divide them into K groups and allow queries to interact only within those groups.
