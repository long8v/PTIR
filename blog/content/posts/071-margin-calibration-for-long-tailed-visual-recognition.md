---
title: "[65] Margin Calibration for Long-Tailed Visual Recognition"
date: 2022-09-19
tags: ['2021Q4', '25min', 'imbalance', 'ECCV']
paper: "https://arxiv.org/pdf/2112.07225.pdf"
issue: 71
issueUrl: "https://github.com/long8v/PTIR/issues/71"
---
![image](https://user-images.githubusercontent.com/46675408/190935677-3709e24a-25d0-453c-a2b2-f1c70106f44a.png)

[paper](https://arxiv.org/pdf/2112.07225.pdf)

## TL;DR
- **task :** long-tail visual recognition
- **PROBLEM :** When the number of data per class is unbalanced on training and balanced on testing, the problem is that the long-tail.
- **idea :** The margin of the classifier is larger where there are more counts per class. Multiply beta by beta and add gamma to adjust the margin. We could just train on the full imbalance data and then retrain on just beta and gamma.
- **architecture :** ResNet32, ResNeXt50, ResNet152, ResNet50
- **objective :** cross entropy loss + loss re-weighting
- **baseline :** softmax, data re-sampling, loss function engineering, decision Boundary Adjustment ... 
- **data :** CIFAR-LT, ImageNet-LT, Places-LT, iNaturalist-LT
- **result :** SOTA!
- **contribution :** With a very simple implementation, SOTA!
- **LIMITATION OR WHAT I DON'T UNDERSTAND:** I don't know if it performs better when test also has the same class distribution as train!

## Details
### Related Work
- data re-sampling
Undersampling the head class and oversampling the tail class
- loss function engineering
reweighting losses so that losses are more balanced across classes. or adjusting logit
- decision boundary adjustment
Analytics show that learning from the original data distribution produces a good representation, but the classifier part is the bottleneck in performance.
There are methodologies that leave the training as it is and tune the classifier, or use methods like Platt scaling.

### Paper details
- margin
![image](https://user-images.githubusercontent.com/46675408/190936476-6f06e81c-6a8f-463d-9270-dab41c0b58be.png)

- margin can be expressed as
![image](https://user-images.githubusercontent.com/46675408/190936484-ce945e4c-18c2-4685-ad13-09fdcdb47c96.png)

- logit can be expressed as an expression for margin -> as n gets bigger, margin gets bigger, logit gets bigger
![image](https://user-images.githubusercontent.com/46675408/190936491-c72aa33c-e351-475c-84d4-6f7f2a26c133.png)

- pseudo-code of the proposed methodology (MARC)
![image](https://user-images.githubusercontent.com/46675408/190936503-749c8090-be4c-4f2d-829a-8f5a37cc5e71.png)

- loss re-weighting was also applied
![image](https://user-images.githubusercontent.com/46675408/190936518-3cace0c6-3d2f-417e-84b3-97fc2062b368.png)

- pseudo-code for the whole course
![image](https://user-images.githubusercontent.com/46675408/190936526-a13a49bc-a7f9-4042-a097-908522a33951.png)

### Result 
![image](https://user-images.githubusercontent.com/46675408/190936466-b2e9db11-3a30-4ad1-91cf-66fff7291065.png)
