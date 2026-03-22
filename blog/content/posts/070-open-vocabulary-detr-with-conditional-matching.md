---
title: "Open-Vocabulary DETR with Conditional Matching"
date: 2022-09-16
tags: ['2022Q1', 'object detection', 'ECCV', 'OV']
paper: "https://arxiv.org/pdf/2203.11876.pdf"
issue: 70
issueUrl: "https://github.com/long8v/PTIR/issues/70"
---
![image](https://user-images.githubusercontent.com/46675408/190539295-4c529608-d944-41af-a00a-0141fca1e64e.png)

[paper](https://arxiv.org/pdf/2203.11876.pdf)

## TL;DR
- **task :** open vocab object detection
- **problem :** Existing object detection models predict with a closed set, which is difficult to scale. To solve this problem, open vocab object detection uses PRN first and then class prediction, making it difficult to predict bboxes for new classes.
- **idea :** Let's use DETR to do object detection with end2end! Let's use it as a class and send it as a text embed using CLIP.
- **architecture :** image and text(=class) are embedded through CLIP and then combined with object queries to create a conditional query. Since there can be multiple objects in one image, we copy N objects. Afterward, bipartite matching is done with `[matched]`, `[not matched]` when given the input image and conditional query, not `[obj]`, `[no obj]`.
- **objective :** bce(match / not match) + bbox loss(gIoU, L1) + embedding reconstruction loss(L1)
- **baseline :** OVR-CNN, ViLD
- **data :** COCO, ELVIS
- **result :** OV OD model vs just AP, AP for novel class both SOTA
- **contribution :** end2end open vocab object detection
- **Limitations or things I don't understand :** I already have embeddings for all base classes/novel classes (R in the paper), and I'm supposed to match all of them to make predictions? Confused. So I'm supposed to do in batch negative or something like that for training?

## Details
![image](https://user-images.githubusercontent.com/46675408/190544655-18a54b9b-0a8b-4e92-83df-d871f59bd1f7.png)

![image](https://user-images.githubusercontent.com/46675408/190543790-fe5390a2-b60e-4d7a-a3f0-7b4d0c577703.png)

![image](https://user-images.githubusercontent.com/46675408/190545375-38c5a12c-9ec0-45a3-a212-bc675309e0bb.png)

![image](https://user-images.githubusercontent.com/46675408/190544759-af96aa73-b4e7-4105-8bdf-05e5cba854f4.png)

