---
title: "Equalization Loss for Long-Tailed Object Recognition"
date: 2022-11-22
tags: ['2020Q1', 'object detection', 'SenseTime', 'imbalance']
paper: "https://arxiv.org/pdf/2003.05176.pdf"
issue: 90
issueUrl: "https://github.com/long8v/PTIR/issues/90"
summary: "Probably the first paper on class imbalance in the foreground?"
---
<img width="697" alt="image" src="https://user-images.githubusercontent.com/46675408/203190570-22561a0c-3712-460e-8c9f-d4356b9482ca.png">

[paper](https://arxiv.org/pdf/2003.05176.pdf), [code](https://github.com/tztztztztz/eql.detectron2) 

## TL;DR
- **task :** long-tail object recognition
- Previous studies only focused on foreground - background and did not address class imbalance within the foreground! Rare classes, whether sigmoid or softmax, are affected by the gradient due to negative samples of frequent classes.
- **IDEA :** Give the $log(p_j)$ term of sigmoid / softmax a frequency-based weight before the $log(p_j)$ term.
- **architecture :** ResNet-50 Mask R-CNN
- **objective :** equalization loss(proposed in this paper)
- **baseline :** sigmoid, softmax, class-aware sampling, class balanced loss, focal loss 
- **data :** LVIS v0.5, CIFAR-100-LT, ImageNet-LT
- **result :** Overall performance improvement for AP, AP50 over baseline. Performance for rare, frequent is worse than baseline and common is very good.
- **contribution :** Probably the first paper on class imbalance in foreground?

## Details
### Motivation
![image](https://user-images.githubusercontent.com/46675408/203194015-52368b45-41a5-4171-b7a4-3a9e87f9c3fb.png)

To the right, the rarer classes have the effect of making the gradient of negative samples higher than positive

### Equalization Loss Formulation
![image](https://user-images.githubusercontent.com/46675408/203194122-c763aaaa-23ec-4dcb-bd47-e3a6ac1f24ca.png)

![image](https://user-images.githubusercontent.com/46675408/203194165-9a09a42c-15be-40c3-8f46-80e3c5a9b8e3.png)

- $E(r)$ : 1 or 0 if foreground
- $f_j$: frequency of class j
- Tresholding $T_\lambda$ : 0 or 1 if $x < \lambda$ tresholding

In this case, $\lambda$ looks at the Tail Ratio (TR) below and realizes that pus => pus => pus is not better or worse in absolute terms, it's just that frequent <=> rare performs differently depending on the value.
![image](https://user-images.githubusercontent.com/46675408/203194213-25f04ee2-93f8-4493-98f8-3d7192939f3c.png)

### Softmax Equalization Loss Formulation
![image](https://user-images.githubusercontent.com/46675408/203195125-46b56296-64a5-4ee7-b39e-248851c9d7ff.png)
![image](https://user-images.githubusercontent.com/46675408/203195170-3fe75245-eaf5-4158-bd70-a8a16e23e146.png)
- multiply weight by the denominator only

![image](https://user-images.githubusercontent.com/46675408/203195201-3fb45f04-5aea-4265-89f2-2a38a279e95c.png)

- $\beta$: Random variable that is 1 with probability $\gamma$ and 0 with probability $1-\gamma

### Result
![image](https://user-images.githubusercontent.com/46675408/203195414-b56c2cea-2ca3-4936-b558-1e19679fe395.png)

Adding it improves performance across the board!

![image](https://user-images.githubusercontent.com/46675408/203195563-dc753038-602c-4838-b42a-c814425d738e.png)

Better overall compared to other long-tail losses, but worse than sampling methods for rare, frequent cases
Definitely better than Focal!

### Ablation
![image](https://user-images.githubusercontent.com/46675408/203195493-a2b4ccf4-4747-4737-b83c-00b32c98c0c2.png)
Higher tail ratio means better for frequent classes and worse for rare -> $\lambda$ is fully hyperparametric

![image](https://user-images.githubusercontent.com/46675408/203196236-f37fb0d5-8d48-4850-9482-6cd3ac3a8b35.png)

Ablation for E(r), replacing 1 if background. rare becomes bad.