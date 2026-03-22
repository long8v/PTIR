---
title: "Sparse R-CNN: End-to-End Object Detection with Learnable Proposals"
date: 2022-08-19
tags: ['object detection', '2020Q4']
paper: "https://openaccess.thecvf.com/content/CVPR2021/papers/Sun_Sparse_R-CNN_End-to-End_Object_Detection_With_Learnable_Proposals_CVPR_2021_paper.pdf"
issue: 58
issueUrl: "https://github.com/long8v/PTIR/issues/58"
---
![image](https://user-images.githubusercontent.com/46675408/185548035-a23480eb-3150-4c26-b594-52457f8ab039.png)

[paper](https://openaccess.thecvf.com/content/CVPR2021/papers/Sun_Sparse_R-CNN_End-to-End_Object_Detection_With_Learnable_Proposals_CVPR_2021_paper.pdf), [code](https://github.com/PeizeSun/SparseR-CNN)

## TL;DR
- **task :** object detection
- Problem :** Most OD problems are dense. For example, faster R-CNN uses a sliding window to select box candidates and later uses something like NMS to select boxes. Many-to-one assign label assignment is also a problem. DETR also has sparse object queries, but the global interactions are dense!
- **idea :** Create an OD model with no more than 100 sparse boxes, where the features in each box do not interact with all the features in the image!
- **architecture :** Throw 100 learnable proposal boxes representing 4 coords, run a RoIPool or RoIAlign operation to get the RoI of the boxes, and get a feature from it. Given this proposal feature, a function called dynamic head is used to predict the final object localization and classification, which is used in the next layer to write the proposal box and feature.
- **objective :** hungarian loss(gIoU loss + bbox L1 loss + cls cross entropy loss)
- **baseline :** Faster RCNN, DETR, RetinaNet 
- **data :** COCO 2017
- **result :** Faster RCNN, DETR, and RetinaNet converge much faster than the others
- **contribution :** OD problems are fun to solve! It's like DETR or not like DETR!
- Limitations or things I don't understand :** I don't understand why DETR is bad because the interaction part is dense for every pixel. It's interesting that DETR can pick a box without an image if the learnable proposal box given without any information eventually converges....(I don't understand a bit considering the reference... 100 is enough, so it takes one...)

## Details
![image](https://user-images.githubusercontent.com/46675408/185552564-409c7b46-4aaf-4239-b301-225001df963f.png)
It is characterized as "purely sparse" with no object positional candidates in the dense grid in the image or object queries interacting with global image features.
Given fixed learnable bounding boxes represented in 4d, they are used to select features from regions of interest (RoI) by RoI pooling. Since the learnable proposal boxes are drawn without looking at the image, they represent statistical object locations in the image.
- RoI pool : https://csm-kr.tistory.com/37

![image](https://user-images.githubusercontent.com/46675408/185553565-2a2a467f-baba-4cda-b244-d646d90c76aa.png)

### Learnable proposal feature
We have a 4d proposal box, but it only represents localization and does not contain any more information. To compensate for this, we create a learnable vector of proposal features with as many dimensions (256) as there are prosposal boxes.

### Dynamic instance interactive head
When N proposal boxes come out, RoIAlign the features of each box, and then interact with the above proposal features with a 1x1 conv to create the final object feature C. In this C, do cls, bbox regression.
The object feature C is used as the proposal features in the next layer, and the bbox is also used as the proposal box in the next layer.

dynamic head #94 

To learn the relationship between object features, we increased performance by using self-attention before dynamic instance interaction(?) with a set of object features. (Not shown -.-;;)


![image](https://user-images.githubusercontent.com/46675408/185553350-2cdfa7cf-eb8d-4b97-81ae-a62d9300e042.png)

### Results
![image](https://user-images.githubusercontent.com/46675408/185553657-47494511-4602-4810-8995-205ad80ca19a.png)

![image](https://user-images.githubusercontent.com/46675408/204690119-c67f6909-746f-4dff-8fb1-34955313ca36.png)

Like grabbing the initial bboxes big time lol
