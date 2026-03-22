---
title: "[88] Relation Networks for Object Detection"
date: 2022-12-11
tags: ['2017', 'microsoft', 'object detection']
paper: "https://arxiv.org/pdf/1711.11575.pdf"
issue: 97
issueUrl: "https://github.com/long8v/PTIR/issues/97"
summary: "Mentioned in #58. I feel like the name is related to SGG - first fully end-to-end object detector (without NMS)"
---
<img width="882" alt="image" src="https://user-images.githubusercontent.com/46675408/206889321-305e953d-21cd-4a18-b01a-7e476a227b45.png">

[paper](https://arxiv.org/pdf/1711.11575.pdf)

## TL;DR
- **I read this because.. :** Mentioned in #58. I have a feeling the name is related to SGG
- **task :** object detection
- **problem :** There was intuition that modeling the relation within an object would improve object recognition, but no research proved it. The SOTA object detection study models each instance individually.
- **idea :** Use the attention module to get the relation between objects and do a weighted sum to strengthen the vector
- **architecture :** CNN -> RPN -> RoI -> FC -> object relation module -> fc -> object relation module -> cls / bbox prediction -> duplicate removal network 
- **objective :** bce for duplicate removal network, cross entropy loss
- **baseline :** fasterRCNN, feature pyramid network(FPN), deformable convolutional network(DCN) 
- **data :** COCO
- **evaluation :** mAP, mAP50, mAP75 
- **result :** SOTA. best on mAP, mAP50 best if trained with threshold 0.5, mAP75 best if trained with 0.75
- **contribution :** first fully end-to-end object detector (without NMS)
- **limitation / things I cannot understand :** duplicate removal network 

## Details

<img width="587" alt="image" src="https://user-images.githubusercontent.com/46675408/206889763-634f8f44-e026-461d-b341-8eeebe69f742.png">


### Object Relation Module

<img width="573" alt="image" src="https://user-images.githubusercontent.com/46675408/206889765-dc3186a6-c6dd-446a-8e09-5020e62a9e65.png">


<img width="363" alt="image" src="https://user-images.githubusercontent.com/46675408/206889783-3f6b7fa2-b597-4701-9963-2e5d01c326d3.png">

- $f_R$ : relation feature
- $f_G$ : geometric feature
- $f_A$ : appearance feature 
- $w_{mn}$ : How much does the mth object affect the nth object?

<img width="320" alt="image" src="https://user-images.githubusercontent.com/46675408/206889917-fd3c9baf-78d3-46e6-8f1b-87861c6f6b54.png">

w_A^{mn}$ is just like scaled dot attention
<img width="320" alt="image" src="https://user-images.githubusercontent.com/46675408/206890005-c27114f0-213b-46a5-aee8-bb118c7471ee.png">

w_G^{mn}$ is obtained by extracting the features (combining them into $\varepsilon_G$), embedding with sine/cosine, multiplying by $W_g$, and taking ReLU
<img width="366" alt="image" src="https://user-images.githubusercontent.com/46675408/206890055-5782b4b1-2397-429c-b109-0deaa409bfcb.png">

Pull features
<img width="488" alt="image" src="https://user-images.githubusercontent.com/46675408/206890035-1a00f7f4-1234-4b8e-be49-23883210e26d.png">

In the end, $f^n_a$ is the concatenation of the nm object relations we picked.

### Relation for Instance Recognition
<img width="589" alt="image" src="https://user-images.githubusercontent.com/46675408/206890153-0c154814-ef2e-4573-859b-4e4539eae289.png">

### Relation for Duplicate Removal 
<img width="550" alt="image" src="https://user-images.githubusercontent.com/46675408/206890161-7adaf234-65a5-47e6-9459-1c49d2ab2780.png">

No big deal, just predict {0, 1} to predict. But since we have a relation module, we can remove the duplicates well.
- rank feature : It was better to get and embed rank than to predict directly with score.
- Depending on the threshold, correct and duplicate are given as labels, and depending on what theshold is given, the best is different for AP50, AP75...

## Result
<img width="1024" alt="image" src="https://user-images.githubusercontent.com/46675408/206890236-e04f1516-b3cf-4b7f-ac09-a6b4197779e6.png">

<img width="384" alt="image" src="https://user-images.githubusercontent.com/46675408/206890241-8f28d971-ab27-491b-9845-c90aefd987ce.png">


<img width="568" alt="image" src="https://user-images.githubusercontent.com/46675408/206890228-85e23fb2-2ab7-4c9c-aac2-5e76d86ba90d.png">
