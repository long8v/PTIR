---
title: "[162] CALIP: Zero-Shot Enhancement of CLIP with Parameter-free Attention"
date: 2024-07-11
tags: ['AAAI', '2022Q3', '25min', 'CLIP']
paper: "https://arxiv.org/abs/2209.14169"
issue: 181
issueUrl: "https://github.com/long8v/PTIR/issues/181"
---
<img width="711" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6c122c8a-8924-436d-a655-d6d59fa534e1">

[paper](https://arxiv.org/abs/2209.14169)

## TL;DR
- **I read this because.. :** AAAI CLIP
- **task :** zs classification
- **problem :** 학습없이 CLIP의 zs classification 능력을 높이고 싶음
- **idea :** 학습 없이 중간에 image / text encoder의 feature들을 교환하자 
- **input/output :** {image, text} -> score
- **architecture :** CLIP ResNet variant
- **objective :** 학습 없이 변경 or few-shot finetune한 버전도 있음
- **baseline :** CoOp, CLIP linear probing, CLIP adaptor
- **data :** ImageNet, Caltech101, OxfordPets, StanfordCars, Flower102, ... (CLIP zs)
- **evaluation :** zs, few-shot accuracy 
- **result :** 학습 전혀 없이 더 높은 성능! 
- **contribution :** fine-grained 하게 더 잘 하겠다고 중간 레이어부터 SA를 넣는다던지, 마지막에서 모든 seq을 본다던지 하는 연구들이 많았는데 이 연구는 그렇게 커 보이지 않는 연산으로 성능을 높인게 좋음 
- **etc. :**

## Details
### motivation
<img width="355" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ad9ee477-2e8d-4ee1-b1b4-1ad3cc9f3320">


### architecture
<img width="845" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/60c3cee7-fbde-4b7e-9fbe-91e10a7167b9">

projection 하지 않은 feature에 대해 attention을 한 다음에 feature에 곱해주는 형태
<img width="393" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6cfc0d44-8eac-44a0-a0c2-1bb0e6a93067">

<img width="395" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/bf45a2ca-b6c9-4be6-8ca4-c1251b1326c5">

최종적인 예측은 이렇게 두 modality를 aggregate한 것에 대한 weighted sum
<img width="397" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ec1dc8ab-f342-49e6-bffe-3ab19976f901">


<img width="829" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/78a36ab0-1a81-4614-a4ec-01c708b50f1c">

### Result

<img width="699" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a7a18f8c-5cea-4d18-b093-32da231e8acc">