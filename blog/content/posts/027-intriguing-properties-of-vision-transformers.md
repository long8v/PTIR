---
title: "Intriguing Properties of Vision Transformers"
date: 2022-04-29
tags: ['ViT', 'WIP', '2020Q2', 'NeurIPS']
paper: "https://openreview.net/pdf?id=o2mbl-Hmfgd"
issue: 27
issueUrl: "https://github.com/long8v/PTIR/issues/27"
---
![image](https://user-images.githubusercontent.com/46675408/165873455-776c815a-3658-455f-a294-9518c922ad74.png)

[paper](https://openreview.net/pdf?id=o2mbl-Hmfgd), [code](https://github.com/Muzammal-Naseer/Intriguing-Properties-of-Vision-Transformers)

# Abstract 
ViT's multi-head self-attention flexibly references sequences of image patches. An important question is how this flexibility can be utilized to exploit nuisances in natural images. We have conducted a number of experiments to investigate the properties of ViTs compared to CNNs.
(a) The transform is robust to severe occlusion, perturbation, and domain shift. For example, it achieved top-1 accuracy of 60% even with 80% of the image removed by occlusion.
<img width="953" alt="image" src="https://user-images.githubusercontent.com/46675408/165876514-1aeb93c1-a708-49cd-811b-9e68bfb4b1ed.png">

(b) (a) was not due to a texture bias, but rather because ViT was less biased toward local texture. When trained well to encode shape-based features, ViT was able to recognize shapes to a degree similar to human abilities, which has not been shown in previous studies.
(c) Using ViT to encode the shape representation, we were able to achieve accurate semantic segmentation without pixel-level supervision.
(d) The use of off-the-shelf features in one ViT model could be used to create other feature ensembles, achieving higher accuracy.
We found that ViT's flexible and dynamic receptive field is an effective feature of ViT.

# Intriguing Properties of Vision Transformer
## Are Vision Transformer Robust to Occlusions
###  Occlusion Modeling :
Given an image x and a label y, the image x is represented by a sequence of N patches. We chose a method (called PatchDrop in the paper) that picks M image patches out of these N and replaces them with 0 to create x'. We applied this PatchDrop in the following three ways
<img width="641" alt="image" src="https://user-images.githubusercontent.com/46675408/165878346-fa90971b-7a0f-4cf1-b5cd-f705d04de0ca.png">

### Robust Performance of Transformer Against Occlusions
- Training was done with ImageNet to solve classification problems and evaluated by the accuracy of the validation set.
- Information Loss: IL defined as the percentage of dropped patches out of all patches (= M/N)
- The graph below shows that ViT is much more robust than CNN.
<img width="1089" alt="image" src="https://user-images.githubusercontent.com/46675408/165879176-9a3e22d7-d9a0-4d0b-99c2-c82dc8e3fcea.png">

### ViT Representations are Robust against Information Loss
To better understand the model's response to occlusion, we visualized the attentions of each head in different layers. In the early layers, they attend all regions, but as we go deeper, we can see that they focus on the unoccluded regions of the image.
<img width="1056" alt="image" src="https://user-images.githubusercontent.com/46675408/165879704-9f2c6a30-449a-4a5a-b65c-5224129f6487.png">

We want to check if there is token invariance for the above changes as the layer gets deeper.
We calculated the correlation coefficient between features (or tokens) for the original and occluded images. For ResNet50, we used the features before the logit layer, and for ViT, we took the class token of the last transformer block. Compared to ResNet, the class tokens in ViT were more robust (=higher correlation). This behavior was also true for other datasets with relatively small objects.
<img width="1091" alt="image" src="https://user-images.githubusercontent.com/46675408/165880840-607846ad-3c59-4af7-9614-67591c185caf.png">

## Shape vs Texture: Can Transformer Model Both Characteristic?

## Does Positional Encoding preserve the global image context? 