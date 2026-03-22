---
title: "[67] Deformable DETR: Deformable Transformers for End-to-End Object Detection"
date: 2022-09-21
tags: ['2020Q3', 'ICLR', 'long', 'object detection', 'SenseTime']
paper: "https://arxiv.org/abs/2010.04159"
issue: 73
issueUrl: "https://github.com/long8v/PTIR/issues/73"
---
<img width="625" alt="image" src="https://user-images.githubusercontent.com/46675408/191400328-e6a48a25-6e6f-42cc-8f95-b05be108787b.png">

[paper](https://arxiv.org/abs/2010.04159), [code](https://github.com/fundamentalvision/Deformable-DETR)

## TL;DR
- **task :** object detection, efficient transformer
- **problem :** DETR Poor performance for small objects, inefficient $O(n^2)$ operation
- **idea :** Inspired by deformable convolution, define a deformable attention module that determines how far away from a point in a given input feature map (=sampling offset) pixels should be given attention.
- **architecture :** Replace the encoder part of DETR with a deformable attention module, and in the decoder part, replace CA with deformable, leaving SA as it is. This is also called multi-scale. Furthermore, we propose a 2-staged deformable DETR, where the deformable DETR encoder is used for region proposal first and the decoder is stacked on top to predict the cls.
- **objective :** Follow DETR loss but apply focal loss for bbox cls (DETR just uses NLL loss)
- **baseline :** DETR, Faster-RCNN
- **data :** COCO 2017
- **result :** Performance SOTA. 10x faster convergence speed compared to DETR. Similar FLOPS as DETR-DC5 with Faster RCNN + FPN, but 1.6x faster runtime.
- **contribution :** efficient DETR + DETR with FPN

## Details
<img width="502" alt="image" src="https://user-images.githubusercontent.com/46675408/191400394-6c76b7c4-82e3-4fd9-bd5c-6df2455d8569.png">

### Deformable Attention Module 
<img width="552" alt="image" src="https://user-images.githubusercontent.com/46675408/191400443-75b8a21b-8d52-48c9-bd36-13ddaf3604c9.png">

<img width="559" alt="image" src="https://user-images.githubusercontent.com/46675408/191400507-0eae8a8a-3956-4015-8f24-a3f8d96dced0.png">

### Multi-scale Deformable Attention Module
<img width="738" alt="image" src="https://user-images.githubusercontent.com/46675408/191416123-bf72d457-2b50-4eb5-8413-64e305bd7bbb.png">

- L is the feature scale
- normalize multi-scale because it can handle it all at once -> no need for separate design to exchange information with each other like a feature pyramid network!

#### Deformable Transformer Encoder
- The reference point is the center of every query pixel.
- Added scale-level embedding to 2D PE to give information about which scale the feature is normalized by w and h.
- There, the sampling offset, $\Delta p_{mqk}$, and attention weight, $A_{mqk}$, are created by linearly burning the query feature $z_q$.
- Write ResNet's stage C3 to C5 feature map and use 1x1 conv for channel size 256
- C6 conforms to C5 by 3 x 3 conv stride 2!
![image](https://user-images.githubusercontent.com/46675408/202976101-554abb00-7878-4fc1-8b36-271099d12bd1.png)
- It's confusing because the picture is only drawn for one pixel, but when you do it for all the pixels, you get attention and it's the size of the original feature map, and it keeps updating as it's layered!


#### Deformable Transformer Decoder
- Since deformable attention itself was created to utilize convolutional features, we left SA as it is and only used CA in the
- The reference point tells the object query to predict linear + sigmoid, and then the Deformable Attention operation
- In this case, feature map writes the output feature maps from the encoder.
- Let bbox be the relative offset of the reference point to predict. The reference point is used as the initial value for the box center, meaning that bbox regression solves the problem of predicting dx, dy, w, and h from the reference point!
![image](https://user-images.githubusercontent.com/46675408/191904394-28a2e484-f580-4990-be0f-84a72e66a184.png)
- It's like a query feature that keeps getting updated as layers are stacked! As many query features as object queries are stacked, they keep going up as layers are stacked.

### Additional Improvements and Variants for deformable DETR
#### Iterative Bounding Box Refinement
Need to refine the bbox prediction of the dth layer with the bbox prediction of the (d - 1)th layer
![image](https://user-images.githubusercontent.com/46675408/191907763-5c3deec3-734c-4b5f-aa27-b18a71f080ff.png)

We set the initial values to x, y to the reference point, qw, and wh = 0.1.
The center coordinate of the bbox in the (d - 1)th layer becomes the reference point for the dth layer. The box size is also used to go along with $\Delta$, again using $\Delta$.
The $sigma^{(-1)}$ part is not gradient smoothing.

#### Two-Stage Deformable DETR
The original detr realized that the object query had nothing to do with the image, so it made a region proposal first and threw it into the object query!
The region proposal uses only the encoder of the deformable DETR and the feature for every pixel becomes the object query to predict the bbox. => trained with Hungarian Loss.
The top scored bboxes are picked and used as initial values for the DETR decoder's iterative bounding box refinement, and the PEs of their coordinates are thrown into the object query.

![image](https://user-images.githubusercontent.com/46675408/191908950-09fb073c-5fa9-446e-b9a6-71aafc2b0db4.png)

### Result
<img width="766" alt="image" src="https://user-images.githubusercontent.com/46675408/191415998-b96160f7-cf16-4257-8d92-6569e3f84ac4.png">

<img width="754" alt="image" src="https://user-images.githubusercontent.com/46675408/191416067-40e82c43-8346-47a0-893f-9406ebf2834b.png">

### Training details
- 50 epochs
- backbone : ImageNet pretrained ResNet-50
- M(=# of attention head) : 8, K(=# of sampled key in each feature level for each attention head) : 6
- lr = 2e-4, learning decay 0.1 40th epoch
- bbox classification loss weight 2 
- linear projection for query reference points and sampling offsets 0,1
<img width="553" alt="image" src="https://user-images.githubusercontent.com/46675408/199367568-3c1e1ba1-122b-4f3d-b7f8-0a8720dc40f3.png">
