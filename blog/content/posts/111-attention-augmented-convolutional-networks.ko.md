---
title: "[102] Attention Augmented Convolutional Networks"
date: 2023-02-16
tags: ['attention', '2019', '25min']
paper: "https://arxiv.org/pdf/1904.09925.pdf"
issue: 111
issueUrl: "https://github.com/long8v/PTIR/issues/111"
---

<img width="754" alt="image" src="https://user-images.githubusercontent.com/46675408/219295954-7447626c-4fce-4cd9-baff-c94d8ff9694c.png">

[paper](https://arxiv.org/pdf/1904.09925.pdf)

## TL;DR
- **I read this because.. :** DETR이 인용. transformer의 FFN은 1x1 convolution 같아서 encoder가 FFN을 통해 "attention augmented convolutional networks"로 볼 수 있다고 얘기해서 궁금해서 읽음.
- **task :** image classification / object detection
- **problem :** CNN은 local한 정보밖에 못보나 self-attention은 long-range를 볼 수 있다.
- **idea :** 둘이 결합해보자!
- **architecture :** 이미지가 들어오면 (h, w) 차원에서 MSA (hidden vector = channel 차원) 적용. 각 pixel에 대해서는 relative poisitonal embedding. 이걸 Conv 결과랑 Concat 하는게 Attention-augmented convolution
- **baseline :** ResNet50, RetinaNet50, channel wise reweighing(Squeeze-and-Excitation, Gather-Excite), channel / spatial reweighing independently(BAM, CBAM)
- **data :** ImageNet, COCO 
- **evaluation :** accuracy / mAP
- **result :** ImageNet / ResNet50에 적용하니 1.3%올랐고, COCO / RetinaNet에 올리니 1.4 mAP 올랐다. 
- **contribution :**
- **limitation / things I cannot understand :**

## Details

### Architecture 
<img width="869" alt="image" src="https://user-images.githubusercontent.com/46675408/219297303-27d0cd40-5d48-427b-abf4-e29b99b8e762.png">

<img width="375" alt="image" src="https://user-images.githubusercontent.com/46675408/219301764-18891cc7-e977-41a0-8ba6-5fac5a766295.png">


### Result
<img width="440" alt="image" src="https://user-images.githubusercontent.com/46675408/219297272-7d964276-b1a0-4a53-86d9-9e1b9ca12436.png">

<img width="459" alt="image" src="https://user-images.githubusercontent.com/46675408/219301504-ad3e2305-31a8-4877-9aa1-770b25fea167.png">

<img width="437" alt="image" src="https://user-images.githubusercontent.com/46675408/219301548-6da0190f-d6a3-4814-9de9-65d69eb2ff21.png">

<img width="437" alt="image" src="https://user-images.githubusercontent.com/46675408/219301594-3a81dfb1-9056-406e-88da-9b6d1929e9a0.png">

<img width="438" alt="image" src="https://user-images.githubusercontent.com/46675408/219301622-e1ecc9a4-bf4a-400e-aeab-edb3e6aa4fa9.png">

<img width="913" alt="image" src="https://user-images.githubusercontent.com/46675408/219301703-8f6c60a9-c16e-4871-8820-47a9f8dd61c2.png">
