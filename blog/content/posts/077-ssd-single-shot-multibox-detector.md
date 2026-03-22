---
title: "SSD: Single Shot MultiBox Detector"
date: 2022-10-12
tags: ['object detection', '2015']
paper: "https://arxiv.org/pdf/1512.02325.pdf"
issue: 77
issueUrl: "https://github.com/long8v/PTIR/issues/77"
summary: "region proposal all at once without !"
---
<img width="927" alt="image" src="https://user-images.githubusercontent.com/46675408/195248934-10fe0cdc-0494-499d-82a0-47fc4237ad7c.png">

[paper](https://arxiv.org/pdf/1512.02325.pdf), [code](https://github.com/weiliu89/caffe/tree/ssd)

## TL;DR
- **task :** real-time object detection 
- **problem :** Unlike other Faster RCNNs that do region proposal + pooling, we want to predict box and cls at once.
- **idea :** Similar to anchor in Faster RCNN, get the relative localization (dx, dy, dw, dh) for default boxes with different size / ratio for each feature map and get the confidence for all classes. Do this for multi-scale features.
- **architecture :** Attach multi-scale feature maps to VGG-16 (so that the feature maps become progressively smaller). For each feature map, attach a head that predicts (num of classes + 4(=coordinates)) * num of default boxes with a head that predicts.
- **objective :** Weighted sum of cross entropy loss and localization loss for class confidence. boxes candidates and gt match all with jaccard > 0.5.
- **baseline :** Faster RCNN, YOLO
- **data :** PASCAL VOC, COCO, ILSVRC
- **result :** Faster RCNN, faster inference and better performance than YOLO
- **contribution :** region proposal all at once, without any !

## Details
### SSD framework
<img width="723" alt="image" src="https://user-images.githubusercontent.com/46675408/195249558-c13cf9e7-15e3-4898-8e78-689c59fefadb.png">

### Architecture
<img width="707" alt="image" src="https://user-images.githubusercontent.com/46675408/195249615-0d30a25c-dc05-41fd-843f-3612b9ce78e0.png">

### loss
<img width="444" alt="image" src="https://user-images.githubusercontent.com/46675408/195250913-33d1888a-1dc3-453e-bccf-67accab7c97b.png">

<img width="575" alt="image" src="https://user-images.githubusercontent.com/46675408/195250932-9cfc84b7-b826-42a4-a10e-eb6ff243cafe.png">

<img width="672" alt="image" src="https://user-images.githubusercontent.com/46675408/195250953-f7ad824d-34df-460b-911b-000905dcab44.png">

### details
- hard negative mining : negative the one with the highest confidence loss in each default box. positive : negative so that negative = 1: 3(=num of default boxes).
- augmentation : random crop so that the jaccard of objects is above a threshold. enter augmentation for small objects.
- faster RCNN : anchor and default boxes are the same concept~! It seems like the motivation of faster RCNN is different because it doesn't use multi-scale feature. There is also a two-stage, one-stage difference.
<img width="481" alt="image" src="https://user-images.githubusercontent.com/46675408/195251785-4201b26d-3a38-41f4-b799-19c8806b0944.png">
<img width="331" alt="image" src="https://user-images.githubusercontent.com/46675408/195251819-9fed1cf2-97d2-4524-bf33-df80d9e5b80e.png">
<img width="878" alt="image" src="https://user-images.githubusercontent.com/46675408/195251971-1e9f40b6-3a74-49a9-b5ab-08b9a98ff2fc.png">
