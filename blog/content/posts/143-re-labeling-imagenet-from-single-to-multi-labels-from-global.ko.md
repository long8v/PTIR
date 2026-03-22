---
title: "[131] Re-labeling ImageNet: from Single to Multi-Labels, from Global to Localized Labels"
date: 2023-09-13
tags: ['2021Q1', 'CVPR', 'naver']
paper: "https://arxiv.org/pdf/2101.05022.pdf"
issue: 143
issueUrl: "https://github.com/long8v/PTIR/issues/143"
---
<img width="693" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/69ec2a44-e24f-45d8-b5ec-562e80fbcf0b">

[paper](https://arxiv.org/pdf/2101.05022.pdf)

## TL;DR
- **I read this because.. :** 언급되어. MaskCLIP이 이거 따라한 것 같기도 하고.. 고전인 것 같아서 읽음
- **task :** image classification
- **problem :** ImageNet에서 한개의 클래스를 가지고 있는 걸로 레이블 되어 있지만 실제로는 여러 object를 가지고 있고 특히 crop할 때 문제가 된다
- **idea :** extra data로 학습된 강력한 image classifer로 pixel-wise로 multi-label로 relabel을 하자. 
- **input/output :** (teacher) image -> pixel wise multi label. (student) image -> class 
- **architecture :** RseNet / EfficientNet-L2. (teacher) GAP를 버리고 마지막을 linear layer를 1x1 conv로 classifier로 사용(학습 x) 
- **objective :** cross-entropy loss. (student) crop이 되면 teacher에서 만든 label map을 ROI align 한 뒤에 softmax 이걸 supervision으로 사용 
- **baseline :** one-hot ImageNet label로 학습 / label smoothing / label cleaning
- **data :** ImageNet / teacher는 super-ImageNet scale(JFT-300M or InstagramNet-1B) -> ImageNet으로 finetune 
- **evaluation :** accuracy
- **result :** 성능 개선. 특히 CutMix랑 쓸 때 더 오름
- **contribution :** 이미지넷 레이블이 문제가 있고 개선하려는 시도는 좀 있었으나 그것들보다 성능이 좋고 KD보다는 미리 LabelPool을 계산해놓는 다는 관점에서 더 효율적이라고 함 
- **etc. :**

## Details
### motivation 
<img width="352" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b0dc5759-b096-4fce-892d-3c8e53ea0194">

random crop을 하면 실제 object와 IoU가 0.5이상인 경우가 23.5%밖에 안된다고..

<img width="338" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ca2b7440-8ff5-4a35-9036-a44519717b82">

### Re-Labeling ImageNet 
JFT-300M /InstagramNet-1B으로 학습된 super-ImageNet scale을 ImageNet에 finetune
-> single label이지만 noisy label + cross entropy 일 때 multi-label로 예측하는 성향
가령 한 이미지 x에 대해 Label이 0이기도 하고 1이기도하면 ce loss는 (1/2, 1/2)로 예측하는게 최적

global pooling 없이 w x h에 대해 마지막 classifier를 1x1 conv weight로 사용하면 각 픽셀별로 classifier가 나올 수 있음!
(1 x 1 conv 어렵게 생각하지 말고 그냥 w x h x d -> (GAP) 1 x d -> 1 x C 였던걸 w x h x d -> w x h x c 로 했다고 생각하면 된다)
related work는 Fully Convolutional Networks for Semantic Segmentation / CAM!


그렇게 만든걸 실제 학습 때 사용하는 방법
<img width="342" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ce59087f-5e1b-42b3-b83b-6cf4971d0cc1">

미리 imagenet에 대한 label map은 저장해놓는다.
이미지 crop이 되면 label map에서도 그 부분을 RoI Align을 해서 뽑는다 -> 나온 label에 대해 softmax를 취해서 soft label로 사용한다 (면적 높은 애가 더 높은 class를 가지는 듯?)

### Results
<img width="707" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e60fb024-8121-4fc1-8e4e-4499c6950778">

학습된 backbone으로 다른 task도 해봤는데 image net pretrained 보다 개선 
<img width="344" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ed151d36-60ef-4425-8350-0d93dcea0d7c">

### Ablations
<img width="336" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/27a7698c-9784-4ee1-b7ea-cb68cc5768d6">

요소가 1) multi-label 2) localized인데 GAP를 다시 넣거나 argmax를 하면서 ablation. 둘다 성능에 주요한 요소였다


