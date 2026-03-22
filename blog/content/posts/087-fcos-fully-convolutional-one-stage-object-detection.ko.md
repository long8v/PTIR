---
title: "[79] FCOS: Fully Convolutional One-Stage Object Detection"
date: 2022-11-15
tags: ['2019', 'fundamental', 'object detection']
paper: "https://arxiv.org/pdf/1904.01355.pdf"
issue: 87
issueUrl: "https://github.com/long8v/PTIR/issues/87"
---
<img width="620" alt="image" src="https://user-images.githubusercontent.com/46675408/201833150-6498d183-bb09-40c6-b03c-fa2c2ab140b7.png">

[paper](https://arxiv.org/pdf/1904.01355.pdf), [code](https://github.com/tianzhi0549/FCOS/)
 
## TL;DR
- **task :** anchor-free object detection 
- **problem :** anchor 기반의 object detection들은 1) 하이퍼 파라미터에 민감하고 2) (상대적인 regression을 하긴 하지만) anchor의 scale / aspect ratio가 고정되어 있고 3) anchor box들이 image 내에 dense하게 있으며(단축이 800 정도인 이미지에 180K의 anchor box들) 4) GT box와 matching 하는 부분에 IoU가 들어가서 계산이 복잡해진다.
- **idea :** semantic segmentation 처럼 fully convolution network로 pixel 별로 object detection을 해보자
- **architecture :** CNN backbone(ResNet-50)의 C3, C4, C5에 1 x 1 conv한 P3, P4, P5, 그리고 P5에 stride 2 conv를 한 P6, P7로 feature pyramid를 만든다. 각 픽셀로 예측을 할 때 object들이 너무 겹쳐있으면 어떤 box를 예측해야하는지 애매하기 때문에 center-ness를 head를 따로 두어서 0~1 sigmoid로 학습한다. 
- **objective :** focal loss for cls, IoU loss for bbox regression
- **baseline :** Faster R-CNN, YOLOv2, SSD, DSSD, RetinaNet, CornerNet
- **data :** COCO 
- **result :** SOTA!
- **contribution :** anchor box를 꼭 써야하는건가?하는 의문을 제기하고 멋진 성능으로 해결 ㅍㅑㅍㅑ 
- **limitation or 이해 안되는 부분 :** BPR(upper bound of recall rate that a detector can achieve)는 어떻게 측정되는가?

## Details
### Architecture
<img width="735" alt="image" src="https://user-images.githubusercontent.com/46675408/201833270-dff59d03-b9ac-4c4c-aea3-39b3f98aefe0.png">

center-ness 브랜치를 그냥 따로 분리하는게 더 성능이 좋았음을 나중에 확인함 ㅋㅋ 
<img width="472" alt="image" src="https://user-images.githubusercontent.com/46675408/201835389-48554e37-1d1a-4041-ad02-4519cd5528fa.png">


### Loss
<img width="331" alt="image" src="https://user-images.githubusercontent.com/46675408/201835158-c19c35f8-b73e-4e52-8fd8-03bb8cfa05e0.png">
- L_cls는 focal loss
- L_reg는 IoU loss

### Center-ness
<img width="387" alt="image" src="https://user-images.githubusercontent.com/46675408/201835264-a009d3b0-8337-4dd3-8b67-b32f0c7bbe9c.png">

<img width="469" alt="image" src="https://user-images.githubusercontent.com/46675408/201835297-456c1b14-0089-4c75-80fe-94b4ece22ca1.png">

<img width="997" alt="image" src="https://user-images.githubusercontent.com/46675408/201835957-3bc48478-09f3-4ad5-ade9-f235e0449265.png">

Center-ness를 classification score에 곱했을 때 confidence score가 더 의미 있는 결과를 냈음을 보였음

### Main Result 
<img width="937" alt="image" src="https://user-images.githubusercontent.com/46675408/201835317-800d6f7f-7dff-4ce5-b9a9-bc705b296425.png">



