---
title: "[79] FCOS: Fully Convolutional One-Stage Object Detection"
date: 2022-11-15
tags: ['2019', 'fundamental', 'object detection']
paper: "https://arxiv.org/pdf/1904.01355.pdf"
issue: 87
issueUrl: "https://github.com/long8v/PTIR/issues/87"
summary: "Raises the question, \"Do I really need to use an anchor box?\" and resolves it with awesome performance @pagethecat"
---
<img width="620" alt="image" src="https://user-images.githubusercontent.com/46675408/201833150-6498d183-bb09-40c6-b03c-fa2c2ab140b7.png">

[paper](https://arxiv.org/pdf/1904.01355.pdf), [code](https://github.com/tianzhi0549/FCOS/)
 
## TL;DR
- **task :** anchor-free object detection 
- Problem :** Anchor-based object detection is 1) hyper-parameter sensitive, 2) the scale/aspect ratio of the anchor is fixed (although it does do a relative regression), 3) the anchor boxes are dense in the image (180K anchor boxes in an image with a shortening of 800 or so), and 4) IoUs are involved in matching GT boxes, which complicates the calculation.
- **idea :** Let's do object detection per pixel with fully convolutional network like semantic segmentation
- **architecture :** Create a feature pyramid with P3, P4, P5 with 1 x 1 convolution on C3, C4, C5 of CNN backbone (ResNet-50), and P6, P7 with stride 2 convolution on P5. We train with a 0-1 sigmoid with center-ness as the head, as it is ambiguous which box to predict if the objects overlap too much when making a prediction for each pixel.
- **objective :** focal loss for cls, IoU loss for bbox regression
- **baseline :** Faster R-CNN, YOLOv2, SSD, DSSD, RetinaNet, CornerNet
- **data :** COCO 
- **result :** SOTA!
- **contribution :** raises the question, "Do I really need to use an anchor box?" and solves it with awesome performance @contribution
- **Limitations or things I don't understand :** How is the BPR (upper bound of recall rate that a detector can achieve) measured?

## Details
### Architecture
<img width="735" alt="image" src="https://user-images.githubusercontent.com/46675408/201833270-dff59d03-b9ac-4c4c-aea3-39b3f98aefe0.png">

I found out later that it would have performed better to just separate the center-ness branch lol
<img width="472" alt="image" src="https://user-images.githubusercontent.com/46675408/201835389-48554e37-1d1a-4041-ad02-4519cd5528fa.png">


### Loss
<img width="331" alt="image" src="https://user-images.githubusercontent.com/46675408/201835158-c19c35f8-b73e-4e52-8fd8-03bb8cfa05e0.png">
- L_cls is the focal loss
- L_reg is the IoU loss

### Center-ness
<img width="387" alt="image" src="https://user-images.githubusercontent.com/46675408/201835264-a009d3b0-8337-4dd3-8b67-b32f0c7bbe9c.png">

<img width="469" alt="image" src="https://user-images.githubusercontent.com/46675408/201835297-456c1b14-0089-4c75-80fe-94b4ece22ca1.png">

<img width="997" alt="image" src="https://user-images.githubusercontent.com/46675408/201835957-3bc48478-09f3-4ad5-ade9-f235e0449265.png">

When Center-ness was multiplied by the classification score, the confidence score showed more meaningful results.

### Main Result 
<img width="937" alt="image" src="https://user-images.githubusercontent.com/46675408/201835317-800d6f7f-7dff-4ce5-b9a9-bc705b296425.png">



