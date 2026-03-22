---
title: "Deep Residual Learning for Image Recognition"
date: 2022-12-25
tags: ['fundamental', 'microsoft', '2015']
paper: "https://arxiv.org/abs/1512.03385"
issue: 100
issueUrl: "https://github.com/long8v/PTIR/issues/100"
summary: "Don't know the difference between ResNet50 and 101 ^^ - residual connection"
---
<img width="1203" alt="image" src="https://user-images.githubusercontent.com/46675408/209473234-9800aeb4-2355-44a3-b7b3-12ed70cb235f.png">


[paper](https://arxiv.org/abs/1512.03385)

## TL;DR
- **I read this because.. :** I don't know the difference between ResNet50 and 101 ^^.
- **task :** image classification, object detection
- Problem :** When you have a network with low layers and a deep network with only identity mapping added to it, the training error of the deep network is higher, even though they are virtually the same network. In other words, the deeper the network, the more unstable the training is to find the optimal solution.
- **idea :** residual connection. let's do f(x) + x. This will act like an identity mapping, with f(x)=0 if we don't need a deep layer.
- **architecture:** Following the principles of VGG, we 1) equalized the number of filters in every layer 2) doubled the number of filters when the feature map size was halved, but stacked them deeper instead of smaller than VGG, so the number of parameters and FLOPS is lower than VGG.
- **objective :** CE loss for classification, object detection loss
- **baseline :** VGG-16, GoogLeNet, plain (ResNet minus residual connection)
- **data :** CIFAR-10, COCO 2015m ILSVRC 2015
- **evaluation :** accuracy, mAP, # params, FLOPS
- **result :** 28% performance improvement in sota. object detection in image classification
- **contribution :** residual connection 

## Details
### Motivation
<img width="471" alt="image" src="https://user-images.githubusercontent.com/46675408/209473452-62f3f101-3de2-4a83-bc35-62e0c20a838b.png">

A phenomenon called degradation. The deeper it is, the higher the training error, i.e., it's not overfitting, it's just not learning well.

### Residual learning
<img width="348" alt="image" src="https://user-images.githubusercontent.com/46675408/209473492-edf65025-a834-43e0-90f7-5e9e5e4f925e.png">

The residualizing blocks must be at least two (one is just a linear effect) and of the same dimension.

### Network architecture
<img width="304" alt="image" src="https://user-images.githubusercontent.com/46675408/209473537-fc6ae797-c38d-4990-94e0-36322f738729.png">

### Network variants
<img width="771" alt="image" src="https://user-images.githubusercontent.com/46675408/209473569-747444a1-644a-4638-9dfc-af37ca50a42b.png">

Your questions answered ^^ 101 layers stacked on top of each other

### training error on ImageNet
<img width="587" alt="image" src="https://user-images.githubusercontent.com/46675408/209473551-f30f42fb-1798-4d74-a2d2-d6c32e90c9a7.png">

### Other
Early papers are fun to read
- [Neural Networks: Tricks of the Trade](https://link.springer.com/book/10.1007/978-3-642-35289-8) 
-  Understanding the difficulty of training deep feedforward neural networks https://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf