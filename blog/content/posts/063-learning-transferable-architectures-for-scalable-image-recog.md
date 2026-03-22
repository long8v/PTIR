---
title: "[57] Learning Transferable Architectures for Scalable Image Recognition"
date: 2022-08-30
tags: ['fundamental', '2017', '25min', 'AutoML']
paper: "https://arxiv.org/pdf/1707.07012.pdf"
issue: 63
issueUrl: "https://github.com/long8v/PTIR/issues/63"
---
![image](https://user-images.githubusercontent.com/46675408/187320072-5e79e4d0-4d4a-4151-b620-09b1b5059211.png)

[paper](https://arxiv.org/pdf/1707.07012.pdf)

## TL;DR
- **task :** image classification, object detection
- **PROBLEM :** Too much architectural engineering to train a neural network well!
- **idea :** Let's find a building block for small data within the network and transfer it for large data.
- **architecture :** The RNN Controller takes the output of the previous two layers and chooses which layer's output to receive, and which convs to stack on that layer. When making the selection, we used reinforcement learning in the previous base NAS study, but in this study we randomized because the performance drop is small even with randomization.
- **objective :** image classification loss, object detection loss
- **baseline :** hand-crafted SOTA models(DenseNet, Shake-Shake,  MobileNet, ShuffleNet), NAS v3
- **data :** CIFAR-10, ImageNet, COCO
- **result :** Image classification / object detection SOTA with smaller computational cost.
- **contribution :** NAS more efficient architecture (random search, trained by ImageNet with architecture selected by CIFAR-10), but better performance
- **Limitations or things I don't understand :**

## Details
### NAS
![image](https://user-images.githubusercontent.com/46675408/187321215-b30e13c3-0c9f-497d-8ce9-6e5e2a29a32e.png)

### 5 predictions the Controller makes
![image](https://user-images.githubusercontent.com/46675408/187323974-271745ed-2ac3-4614-8082-e7abbf04838f.png)

### Layers the Controller can pick from
![image](https://user-images.githubusercontent.com/46675408/187323378-60e5ab9b-0e72-45fb-9266-35176b9d534e.png)

### Architecture 
![image](https://user-images.githubusercontent.com/46675408/187324010-e749cbcf-b95e-4126-b10a-f5cace7154ba.png)
