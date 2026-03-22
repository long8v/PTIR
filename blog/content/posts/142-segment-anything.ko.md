---
title: "[130] Segment Anything "
date: 2023-09-04
tags: ['segmentation', '2023Q2', 'meta']
paper: "https://arxiv.org/pdf/2304.02643.pdf"
issue: 142
issueUrl: "https://github.com/long8v/PTIR/issues/142"
---

<img width="1047" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/61e77ac6-c071-4804-9185-5b5e09bd8610">

[paper](https://arxiv.org/pdf/2304.02643.pdf), [demo](https://segment-anything.com/demo?ref=blog.annotation-ai.com)

## TL;DR
- **I read this because.. :** 안 읽으려고 했으나.. SAM이 너무 강력해서 VLM dataset 만드는데 많이 사용되는듯 
- **task :** prompt segmentation 
- **problem :** prompt가 주어졌을 때 segmentation 하고 싶다 / point의 경우 어떤 segment를 원하는지에 대한 disambiguity가 있음. 
- **idea :** 간단한 prompt encoder 사용하여 이걸 MaskFormer의 query로 사용 / 가장 confident한 것만 loss 구해서 학습 
- **input/output :** image + prompt(points, box, mask, text) -> mask (no cls) 
- **architecture :** MaskFormer의 변형. 우선 강--력한 backbone(ViT-H) + prompt encoder는 pe 혹은 text encoder 통과시켜준 뒤 더해준 뒤 SA. image -> prompt cross attention (원래 있던 거) prompt -> image cross attention(추가된 거). pixel upsample한거랑 mask embedding이라 내적해서 mask 생성. Confident mask만 뽑으려고 IoU score도 return하도록 변경.
- **objective :** focal loss + dice loss
- **baseline :** RITM이라는 Interactive segmentation 모델 
- **data :** SA-1B 제안
- **evaluation :** mIoU
- **result :** RITM을 거의 다 이김. 벤치마크에서 semantic segmentation sota를 이기진 못함. text prompt에 대한 성능은 별로 
- **contribution :** semantic segmentation의 벤치마크는 매우 주관적인 것 같은데 이걸 데이터셋 + 모델 arch로 해결! general한 semantic segmentation 모델을 만들었당.
- **etc. :** bbox / mask / text에 대해 어떻게 학습한건지? 학습을 안한건지?..

## Details
### Preliminaries 
<img width="800" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/164ba76e-ee0d-4bbf-92af-261704bc28d4">

### Disambiguity in interactive segmentation
<img width="507" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4deaddfa-89d0-45c8-a842-c042c033a31a">

### Model
<img width="1026" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d996c7bf-b01d-4059-b429-111357fb2221">

### Result 
<img width="931" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/08e3d352-cd4e-4b30-99cb-ccc6680130a9">
