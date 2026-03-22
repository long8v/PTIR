---
title: "[6] Crossing the Format Boundary of Text and Boxes: Towards Unified Vision-Language Modeling"
date: 2022-01-18
tags: ['multimodal', '2021Q4', 'backbone', 'multitask']
paper: ""
issue: 6
issueUrl: "https://github.com/long8v/PTIR/issues/6"
---
Crossing the Format Boundary of Text and Boxes: Towards Unified Vision-Language Modeling
[arxiv](https://arxiv.org/pdf/2111.12085.pdf)
![image](https://user-images.githubusercontent.com/46675408/149867612-4e85cf87-c5ad-45e4-ad57-3f552510523e.png)

![image](https://user-images.githubusercontent.com/46675408/149868133-0b893378-d1a4-4ab5-ab02-e0498adbc823.png)
**problem :** [pix2seq](https://long8v.notion.site/pix2seq-109e93c7ebb54104bbca96f16ddc4127) is a framework for object detection only, let's extend it to a unified framework for various vision-language problems.
**solution :** Very similar to pix2seq, cut the object box into bins and use the generation method to generate a task. The image is put into an image encoder (CNN), task prefix, task input is put into a text encoder, concatenated, and put into a transformer encoder, and then one transformer decoder generates the output. Define output sequence for tasks other than Object Detection
**result :** We were able to solve various tasks such as grounded captioning, VQA, image captioning, and object detection with a single unified model, and several of these tasks benefited from multi-task learning.