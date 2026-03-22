---
title: "Attention Augmented Convolutional Networks"
date: 2023-02-16
tags: ['attention', '2019', '25min']
paper: "https://arxiv.org/pdf/1904.09925.pdf"
issue: 111
issueUrl: "https://github.com/long8v/PTIR/issues/111"
summary: "DETR quoted. The FFN of the transformer looks like a 1x1 convolution, so I was curious to read that the encoder can be viewed as \"attention augmented convolutional networks\" through FFN. - When I applied it to ImageNet / ResNet50, it increased by 1.3%, and when I applied it to COCO / RetinaNet, it increased by 1.4 mAP."
---

<img width="754" alt="image" src="https://user-images.githubusercontent.com/46675408/219295954-7447626c-4fce-4cd9-baff-c94d8ff9694c.png">

[paper](https://arxiv.org/pdf/1904.09925.pdf)

## TL;DR
- **I read this because.. :** Quoted by DETR. The FFN of the transformer looks like a 1x1 convolution, so I was curious to read that the encoder can be viewed as "attention augmented convolutional networks" via FFN.
- **task :** image classification / object detection
- Problem :** CNN can only see local information, but self-attention can see long-range.
- **IDEA :** Let's combine the two!
- **architecture :** As the image comes in, apply MSA (hidden vector = channel dimension) on the (h, w) dimension. For each pixel, relative poisitonal embedding. Concat this with the Conv result to get the Attention-augmented convolution
- **baseline :** ResNet50, RetinaNet50, channel wise reweighing(Squeeze-and-Excitation, Gather-Excite), channel / spatial reweighing independently(BAM, CBAM)
- **data :** ImageNet, COCO 
- **evaluation :** accuracy / mAP
- **result :** ImageNet / ResNet50 increased by 1.3%, and COCO / RetinaNet increased by 1.4 mAP.
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
