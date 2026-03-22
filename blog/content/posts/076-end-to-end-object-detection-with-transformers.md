---
title: "End-to-End Object Detection with Transformers"
date: 2022-10-07
tags: ['facebook', '2020Q2', 'object detection', 're-read']
paper: "https://arxiv.org/pdf/2005.12872.pdf"
issue: 76
issueUrl: "https://github.com/long8v/PTIR/issues/76"
summary: "transformer based od model without nms!"
---
![image](https://user-images.githubusercontent.com/46675408/194462164-359361b1-881b-440c-b659-d6c27478733c.png)

[paper](https://arxiv.org/pdf/2005.12872.pdf)

## TL;DR
- **task :** object detection 
- **problem :** the need for many hand-designed components like a non-maximum suppression procedure or anchor generation
that explicitly encode our prior knowledge about the task
- **idea :** predict directly object set with bipartite matching  
- **architecture :** CNN + transformer encoder + transformer decoder with object queries(=random PE) + bbox / cls prediction head
- **objective :** IoU loss + CE Loss
- **baseline :** Faster R-CNN
- **data :** COCO
- **result :** SOTA
- **contribution :**  transformer based od model without nms!
- **Limitations or things I don't understand :** longer training time, low performance on small object

## Details
[notion](https://long8v.notion.site/DETR-5810bf27ec954498a3bdd95c15b116b7)