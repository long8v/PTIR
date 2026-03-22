---
title: "ImageBind: One Embedding Space To Bind Them All"
date: 2023-05-16
tags: ['multimodal', '25min', '2023Q2', 'meta']
paper: "http://facebookresearch.github.io/ImageBind/paper"
issue: 124
issueUrl: "https://github.com/long8v/PTIR/issues/124"
summary: "Controversial in many places. I should have read it, but thesis study presented it. - Multiple modality integration. It's good to see the image in the middle. Good performance"
---
<img width="911" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/53b6c9ea-9e5b-40b0-a485-d5923c54f1d5">

[paper](http://facebookresearch.github.io/ImageBind/paper), [blog](https://imagebind.metademolab.com/)

## TL;DR
- **I read this because.. :** Controversial in many places. I read this because... :** Controversy in various places.
- **task :** align many modalities into one embedding space -> image / audio / thermal classification 
- **problem :** getting a pair between all modalities is practically impossible (audio - thermal?!)
- **idea :** wrap everything in the image modality with image as the middle
- **input/output :** image + video / audio / depth / thermal / IMU 
- **architecture :** pretrained CLIP. image text encoder is freeze. encoder for each modality
- **objective :** InfoNCE
- **baseline :** classification sota / supervised for each benchmark
- **data :** AudioSet, SUN RGB-D(depth), LLVIP(thermal), Ego4D(video IMU)
- **evaluation :** zero-shot cross-modal retrieval / zero-shot classification (create class text embedding and classify as closest)
- **result :** good performance for few-shot in audio/depth. "emergent retrieval", I didn't actually use pair for training and measured the performance.
- **contribution :** Integrate multiple modalities. It's nice to see the image in the middle. Good performance
- **etc. :** Completely read-only

## Details
### 
<img width="1058" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b5139b7e-ce59-4567-a706-6d0746726241">

<img width="1060" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9dff7362-8ed3-497b-80b1-3c187c8f7dd8">

<img width="514" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/317a0e00-c704-4735-bfce-3fca974e9fcd">

<img width="1037" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2d7955fb-e539-440f-a984-134f175df9ab">

If there's a text pair, we'll do that as well, so that what we've learned is Text Paired.
Absolute SOTA is a supervised training

<img width="527" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/eb291bbe-1d8d-460a-8764-522bc6bbf3fb">

emergent means we didn't directly use text-audio set

<img width="534" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b7d5b973-428b-48e6-83ce-ceb582866055">

Can be computed like old word embedding lol

<img width="536" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/96c540d5-4be1-4571-a151-8a65928cf150">

OD...

<img width="553" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/858716bc-7be2-454e-bf12-c23c0efc8816">

Of course... I turned on the image encoder. Good.