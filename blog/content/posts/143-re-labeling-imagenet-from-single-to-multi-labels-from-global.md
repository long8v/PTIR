---
title: "Re-labeling ImageNet: from Single to Multi-Labels, from Global to Localized Labels"
date: 2023-09-13
tags: ['2021Q1', 'CVPR', 'naver']
paper: "https://arxiv.org/pdf/2101.05022.pdf"
issue: 143
issueUrl: "https://github.com/long8v/PTIR/issues/143"
summary: "MaskCLIP seems to have copied this, and it seems to be a classic, so I read it - Imaginet labels are problematic and there have been some attempts to improve them, but this is better than them and more efficient in terms of pre-calculating LabelPool rather than KD."
---
<img width="693" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/69ec2a44-e24f-45d8-b5ec-562e80fbcf0b">

[paper](https://arxiv.org/pdf/2101.05022.pdf)

## TL;DR
- **I read this because.. :** mentioned. MaskCLIP seems to have copied this, and it seems to be a classic.
- **task :** image classification
- **problem :** In ImageNet, it is labeled as having one class, but it actually has multiple objects, which is especially problematic when cropping.
- **idea :** relabel pixel-wise to multi-label with a powerful image classifier trained with extra data.
- **input/output :** (teacher) image -> pixel wise multi label. (student) image -> class 
- **architecture :** RseNet / EfficientNet-L2. (teacher) discard GAP and use linear layer at the end as classifier with 1x1 conv (training x)
- **objective :** cross-entropy loss. (student) crop, ROI align the label map created by teacher, and then use softmax as supervision.
- **baseline :** learn with one-hot ImageNet labels / label smoothing / label cleaning
- **data :** ImageNet / teacher is finetune with super-ImageNet scale(JFT-300M or InstagramNet-1B) -> ImageNet
- **evaluation :** accuracy
- **result :** Improved performance, especially when used with CutMix
- **contribution :** Imaginet labels are problematic and there have been some attempts to improve them, but this is better than them and more efficient in terms of pre-calculating LabelPool rather than KD.
- **etc. :**

## Details
### motivation 
<img width="352" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b0dc5759-b096-4fce-892d-3c8e53ea0194">

If I randomly crop, only 23.5% of the time the real object and IoU are above 0.5...

<img width="338" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ca2b7440-8ff5-4a35-9036-a44519717b82">

### Re-Labeling ImageNet 
Finetune super-ImageNet scale trained with JFT-300M /InstagramNet-1B to ImageNet
-> propensity to predict with multi-label when single label but noisy label + cross entropy
For example, for an image X, if the Label is both 0 and 1, the CE LOSS is optimally predicted to be (1/2, 1/2).

If we use the last classifier as a 1x1 conv weight for w x h without global pooling, we can get a classifier for each pixel!
(1 x 1 conv Don't overthink it, just think of it as w x h x d -> (GAP) 1 x d -> 1 x C instead of w x h x d -> w x h x c)
For related work, see Fully Convolutional Networks for Semantic Segmentation / CAM!


How to use it for real-world learning
<img width="342" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ce59087f-5e1b-42b3-b83b-6cf4971d0cc1">

Save the label map for imagenet in advance.
When the image is cropped, RoI Align that part in the label map -> take the softmax for the label that came out and use it as a soft label (higher area has a higher class?)

### Results
<img width="707" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e60fb024-8121-4fc1-8e4e-4499c6950778">

I tried other tasks with the trained backbone and it is better than image net pretrained.
<img width="344" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ed151d36-60ef-4425-8350-0d93dcea0d7c">

### Ablations
<img width="336" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/27a7698c-9784-4ee1-b7ea-cb68cc5768d6">

If the element is 1) multi-label 2) localized, either re-gap or ablation with argmax. Both were major performance factors


