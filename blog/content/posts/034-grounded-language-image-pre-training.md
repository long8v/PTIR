---
title: "[29] Grounded Language-Image Pre-training"
date: 2022-06-21
tags: ['multimodal', '2021Q4', 'few-shot', 'zero-shot', 'microsoft', 'object detection']
paper: "https://arxiv.org/abs/2112.03857"
issue: 34
issueUrl: "https://github.com/long8v/PTIR/issues/34"
---
![image](https://user-images.githubusercontent.com/46675408/174726459-a2c9d73e-f8b6-4cf2-929f-380d44bf9db3.png)

[paper](https://arxiv.org/abs/2112.03857), [code](https://github.com/microsoft/GLIP) 

## TL;DR
- **I read this because.. :** It was mentioned a lot in the thesis meeting. But I read this because...
- **task :** object detection -> phrase grounding problem to learn
- **problem :** Image classification models are difficult to apply in the real world because they classify within fixed categories. CLIP solved this problem with image-text pairs, but that's for image classification, and we want to solve the object detection level task as well!
- **idea :** Replace the object detection problem with a phrase grounding problem where classes are given in the form of prompts and the image is good at aligning with the words in the prompt.
- **architecture :** 1) Visual Encoder(Swin) + DyHead 2) Pretrained BERT 3) Early fusion of 1 and 2.
- **objective :** cls loss(with alignment score!) + regressor loss
- **baseline :** Faster RCNN, DyHead
- **data :** COCO, LVIS, Flickr30K, Object365, GoldG, OpenImages, Visual Genome, ImageNetBoxes
- **evaluation :** AP
- **Results :** 1) Outperformed supervised baseline on COCO, LVIS datasets not given at training 2) Achieved SOTA when finetuned on COCO 3) 1-shot GLIP outperformed supervised Dynamic Head on 13 object detection downstream tasks.
- **contribution :** CLIP in object detection 
- **limitation / things I cannot understand :**

## Details
### preliminaries
  - Dynamic Head : #94 
  - MDETR 
  - visual grounding : https://cvml.tistory.com/4
![image](https://user-images.githubusercontent.com/46675408/207490470-ce2b0cd6-ffcd-4d7b-91be-7f39f2ab0064.png)

  
### Data 
- COCO : 80 object categories, training 118K, valid 5K, test 41K
- LVIS : long tail object detection. 1000 categories.
- Flickr30K: image and 5 reference sentences about it. data for image captioning
  - Objects365 : 365 categories, 2 million images, 30 million bounding boxes
- GoldG : Grounding data created by human annotation in MDETR paper with 0.8M data
  - OpenImages : 15,851,536 boxes on 600 categories, 478,000 crowdsourced images with 6,000+ categories
  - Visual Genome : 108,077 Images, 5.4 M Region Descriptions, 2.3M Relationships
  - ImageNetBoxes : [?](https://image-net.org/download-bboxes.php)
- architecture
Object detection consists of two losses: a localization loss and a classification loss. In this case, localization is out of the scope of this thesis. We will only tackle the classification problem.

For a typical object detection problem, classification loss is defined as
![image](https://user-images.githubusercontent.com/46675408/174781550-757c0a65-ae7e-4538-b3c4-b632fe788ae6.png)

Instead of classification, we have a separate Image Encoder and a separate Language Encoder that handles prompts, and its inner product is the alignment score. This will replace the classifier logit.
<img width="740" alt="image" src="https://user-images.githubusercontent.com/46675408/174781857-c300edbc-dc62-43b4-90c3-e401a20723ce.png">

And you can put the same in LOSS, it will just add a dimension rather than a class: (multiple data, tokenization,`[no_obj]` token).

LOSS can be achieved by using binary sigmoid LOSS.

![image](https://user-images.githubusercontent.com/46675408/174779487-d003d510-9b7b-4e57-8ec2-ed53130d1b11.png)

FasterRCNN and DynamicHead (SOTA) as detection models, Swin-T and Swin-L as image encoders, and BERT as textual encoder.
<img width="804" alt="image" src="https://user-images.githubusercontent.com/46675408/174782448-3e02520e-c10c-4c96-9bc6-dc4c4edc5f07.png">

Deep fusion is not so much about combining the output from different encoders (called late fusion), but about exchanging information as layers are added. In this case, BERT adds a new layer on top of the existing layer and exchanges the output of the layers above it.

### Result
![image](https://user-images.githubusercontent.com/46675408/174773037-3f691cc6-e38b-42d2-ba34-1a3feea8b579.png)


 