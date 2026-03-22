---
title: "[70] SSD: Single Shot MultiBox Detector"
date: 2022-10-12
tags: ['object detection', '2015']
paper: "https://arxiv.org/pdf/1512.02325.pdf"
issue: 77
issueUrl: "https://github.com/long8v/PTIR/issues/77"
---
<img width="927" alt="image" src="https://user-images.githubusercontent.com/46675408/195248934-10fe0cdc-0494-499d-82a0-47fc4237ad7c.png">

[paper](https://arxiv.org/pdf/1512.02325.pdf), [code](https://github.com/weiliu89/caffe/tree/ssd)

## TL;DR
- **task :** real-time object detection 
- **problem :** region proposal + pooling을 하는 다른 Faster RCNN류와 달리 한번에 box와 cls 예측을 하자 
- **idea :** Faster RCNN의 anchor와 비슷하게 각 feature map에 대해 다른 size / ratio를 가진 default box들에 대해서 상대적인 localization(dx, dy, dw, dh)를 구하고 모든 class에 대한 confidence를 구한다. 이걸 multi-scale feature에 대해서 한다. 
- **architecture :** VGG-16에 multi-scale feature map을 붙임(점점 feature map이 작아지도록). 각각의 feature map에 대해 (num of classes + 4(=coordinates)) * num of default box 을 예측하는 head를 붙임. 
- **objective :** class confidence에 대한 cross entropy loss와 localization loss의 가중합. boxes 후보들과 gt는 jaccard가 0.5이상인걸 다 매칭함.
- **baseline :** Faster RCNN, YOLO
- **data :** PASCAL VOC, COCO, ILSVRC
- **result :** Faster RCNN, YOLO보다 inference도 빠르고 성능도 좋음
- **contribution :** region proposal 따로 없이 한번에 ! 

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
- hard negative mining : 각 default box에서 가장 높은 confidence loss를 가지는 것을 negative로. positive : negative = 1: 3(=num of default boxes)가 되도록
- augmentation : object들의 jaccard가 threshold 이상이 될 수 있도록 random crop. small object에 대한 augmentation 들어감. 
- faster RCNN : anchor랑 default boxes랑 같은 개념인듯~! faster RCNN의 motivation이 multi-scale feature를 쓰지 않는다여서 그게 다른듯. two-stage, one-stage 차이도 있고.
<img width="481" alt="image" src="https://user-images.githubusercontent.com/46675408/195251785-4201b26d-3a38-41f4-b799-19c8806b0944.png">
<img width="331" alt="image" src="https://user-images.githubusercontent.com/46675408/195251819-9fed1cf2-97d2-4524-bf33-df80d9e5b80e.png">
<img width="878" alt="image" src="https://user-images.githubusercontent.com/46675408/195251971-1e9f40b6-3a74-49a9-b5ab-08b9a98ff2fc.png">
