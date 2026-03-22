---
title: "[84] DiffusionDet: Diffusion Model for Object Detection"
date: 2022-11-29
tags: ['object detection', 'generative', '2022Q4']
paper: "https://arxiv.org/abs/2211.09788"
issue: 93
issueUrl: "https://github.com/long8v/PTIR/issues/93"
summary: "The first paper applying diffusion to object detection"
---
<img width="828" alt="image" src="https://user-images.githubusercontent.com/46675408/204419010-28ef23ac-f9de-4fc5-aa02-76522ef5bb51.png">

[paper](https://arxiv.org/abs/2211.09788)

## TL;DR
- **task :** object detection 
- Problem :** Most object detection models rely on predefined object candidates such as anchor boxes, and DETRs have the concept of object queries, so they cannot extract more objects than they train.
- **idea :** use diffusion to pull out the image bbox!
- **architecture :** GT bbox + gaussian noise into encoder (ResNet-50, Swin-b) and pull features with RoI pooling decoder receives features and bbox from previous step and predicts bbox/cls
- **objective :** hungarian loss(=DETR loss)
- **baseline :** DETR, deformable DETR, Sparse R-CNN
- **data :** MS-COCO, LVIS
- **result :** SOTA ?!
- **contribution :** First paper applying diffusion to object detection
- **limitation or part I don't understand :** I don't read the diffusion so I don't understand exactly, but I'm surprised the performance is coming out... even SOTA? Are they using the device to make the results look good?

## Details
### motivation
<img width="525" alt="image" src="https://user-images.githubusercontent.com/46675408/204426794-153190d3-f88e-4801-814d-2594fdea9ced.png">
<img width="508" alt="image" src="https://user-images.githubusercontent.com/46675408/204426808-69d45e0c-eb31-4842-a8a4-27c3ca17d60f.png">

### Preliminaries : diffusion model
<img width="339" alt="image" src="https://user-images.githubusercontent.com/46675408/204426917-866384b2-e3d4-43bc-a989-d606c46c0b6e.png">

- $z_0$ : data sample
- $z_t$ : latent noisy sample
- $t$ : step
- $\bar a_t$ =  
<img width="300" alt="image" src="https://user-images.githubusercontent.com/46675408/204427152-cd223671-0808-4a5c-a4e6-6ae988960687.png">

The loss learned is the output of the neural network $f_\theta$ and the MSE of $z_0$.
<img width="300" alt="image" src="https://user-images.githubusercontent.com/46675408/204427548-c438c9a5-4f5c-4981-9346-c711ac5a3fdf.png">

In this paper, $z_0$ is referred to as GT bbox.

### architecture
<img width="529" alt="image" src="https://user-images.githubusercontent.com/46675408/204426854-dce7af56-9dc7-4552-915c-2ec7e2acaf2a.png">

- encoder 
Applying the feature pyramid to ResNet, Swin
- decoder
Crop the proposal boxes and use them as RoI features similar to sparse R-CNN #58

#### Difference from Sparse R-CNN
(1) Because we start with random bboxes, we can use more bboxes in the infer step than we used in training
(2) Unlike sparse RCNN, it only gets the first RoI pooled feature
(3) Reuse the detector head

### Training
GT + gaussian noise to make it a Noisy bbox and start with that.
<img width="504" alt="image" src="https://user-images.githubusercontent.com/46675408/204427990-043ea095-93f7-4c55-b27b-4caadcce5153.png">

- padding : padding because the number of GT bboxes is different. I tried padding with 1) copy GT bbox 2) random box 3) image size box, etc. but Gaussian random box padding is the best.
- box corruption : noise $a_t$ gets smaller and smaller with step t. The signal-to-noise ratio(?) was important, which should have a higher signal scaling value than image generation.
- training losses : DETR loss wrote

### Inference 
Just start with a random Gaussian bbox
<img width="519" alt="image" src="https://user-images.githubusercontent.com/46675408/204428014-7f15bbfb-e489-4caa-a388-92e2b310905e.png">
 
- ddim : I used DDIM (non-markov, unlike DDPM, which is a model that requires you to give the initial value as well as the previous step) to pull the bbox and pass it to the next step.
- box_renewal : in step t, I filtered the ugly bboxes by score and replaced them with random boxes.
 
### Result
- COCO 2017
<img width="509" alt="image" src="https://user-images.githubusercontent.com/46675408/204426670-ff90f689-43e9-4bf6-9806-2125d9c6bf8a.png">

- LVIS v1.0 val
<img width="524" alt="image" src="https://user-images.githubusercontent.com/46675408/204426742-26838bc1-2e76-4bcd-9872-318400ef0a1c.png">
