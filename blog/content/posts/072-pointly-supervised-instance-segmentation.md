---
title: "Pointly-Supervised Instance Segmentation"
date: 2022-09-20
tags: ['2022Q2', '25min', 'ECCV', 'annotation', 'segmentation']
paper: "https://arxiv.org/pdf/2104.06404.pdf"
issue: 72
issueUrl: "https://github.com/long8v/PTIR/issues/72"
---
![image](https://user-images.githubusercontent.com/46675408/191143191-0224bb30-7f49-4382-90d6-db7146af2929.png)

[paper](https://arxiv.org/pdf/2104.06404.pdf)

## TL;DR
- **task :** instance segmentation 
- **problem :** segmentation annotation cost is too high! weakly-supervised performs only 85% of supervised
- **idea :** Let's do point level annotation! Annotate the bbox first, then take 10 random dots and let the annotator binary label them as background or object.
- **architecture :** mask RCNN
- **objective :** bi-linear interpolate the prediction for 10 points and then cross entropy loss
- **baseline :** fully supervised mask RCNN
- **data :** ImageNet, COCO
- **result :** ImageNet performs about 97% of supervised, COCO performs 99%.
- **contribution :** The original segmentation takes about 79 seconds per piece, but this methodology allows for annotation in 7 seconds.
- **Limitation or part not understood :** PointRend model part not read

## Details
![image](https://user-images.githubusercontent.com/46675408/191144175-80c0c22a-f799-4c9a-9174-bcc0dacadcd0.png)

![image](https://user-images.githubusercontent.com/46675408/191144189-5783160c-375c-46e5-8804-203d14cc2eef.png)

- augmentation
Use normal image augmentations + randomly sample 5 out of 10 at each training epoch and use only those.

- Difference between dice loss and IoU
https://stackoverflow.com/questions/60268728/why-dice-coefficient-and-not-iou-for-segmentation-tasks
![image](https://user-images.githubusercontent.com/46675408/191143910-54752029-a47a-46f6-8bf0-771423ab54ea.png)

It's like using dice for segmentation and iou for object detection. As if there is no particular reason for this?