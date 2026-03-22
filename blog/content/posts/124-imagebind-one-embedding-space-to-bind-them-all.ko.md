---
title: "[115] ImageBind: One Embedding Space To Bind Them All"
date: 2023-05-16
tags: ['multimodal', '25min', '2023Q2', 'meta']
paper: "http://facebookresearch.github.io/ImageBind/paper"
issue: 124
issueUrl: "https://github.com/long8v/PTIR/issues/124"
---
<img width="911" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/53b6c9ea-9e5b-40b0-a485-d5923c54f1d5">

[paper](http://facebookresearch.github.io/ImageBind/paper), [blog](https://imagebind.metademolab.com/)

## TL;DR
- **I read this because.. :** 여러 곳에서 논란. 읽어야지~ 했는데 논문스터디에서 발제해주심.
- **task :** align many modalities into one embedding space -> image / audio / thermal classification 
- **problem :** 모든 modality간 pair를 얻는것은 사실상 불가능(audio - thermal?!)
- **idea :** image를 중간으로 해서 image modality에 모든걸 엮자
- **input/output :** image + video / audio / depth / thermal / IMU 
- **architecture :** pretrained CLIP. image text encoder는 freeze. 각 modality에 대한 encoder 
- **objective :** InfoNCE
- **baseline :** 각 benchmark의 classification sota / supervised 
- **data :** AudioSet, SUN RGB-D(depth), LLVIP(thermal), Ego4D(video IMU)
- **evaluation :** zero-shot cross-modal retrieval  / zero-shot classifcation(class text embedding 만들고 가장 가까운 걸로 분류)
- **result :** audio / depth 에서 few-shot 좋은 성능. "emergent retrieval"이라고 실제로 학습엔 pair를 안 넣고 성능 측정했는데 성능 ㄱㅊ.
- **contribution :** 여러 modality 통합. image가 중간에 들어가는게 좋은걸 보임. 좋은 성능
- **etc. :** 완전 대충 읽음

## Details
### 
<img width="1058" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b5139b7e-ce59-4567-a706-6d0746726241">

<img width="1060" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9dff7362-8ed3-497b-80b1-3c187c8f7dd8">

<img width="514" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/317a0e00-c704-4735-bfce-3fca974e9fcd">

<img width="1037" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2d7955fb-e539-440f-a984-134f175df9ab">

text pair가 있을 경우 그것도 같이 해서 학습한게 Text Paired.
Absolute SOTA는 supervised training 한 거 

<img width="527" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/eb291bbe-1d8d-460a-8764-522bc6bbf3fb">

emergent는 직접적으로 text-audio set을 안썼다는 뜻 

<img width="534" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b7d5b973-428b-48e6-83ce-ceb582866055">

옛날 word embedding 스럽게 연산 가능 ㅋㅋ

<img width="536" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/96c540d5-4be1-4571-a151-8a65928cf150">

OD도 되네..

<img width="553" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/858716bc-7be2-454e-bf12-c23c0efc8816">

당연히.. image encoder 키우니 잘됐다