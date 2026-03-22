---
title: "CALIP: Zero-Shot Enhancement of CLIP with Parameter-free Attention"
date: 2024-07-11
tags: ['AAAI', '2022Q3', '25min', 'CLIP']
paper: "https://arxiv.org/abs/2209.14169"
issue: 181
issueUrl: "https://github.com/long8v/PTIR/issues/181"
summary: "AAAI CLIP - There have been a lot of studies that have tried to do fine-grained better by putting SA in the middle layer, or looking at all seqs at the end, but this is a nice performance boost with a computation that doesn't seem that big."
---
<img width="711" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6c122c8a-8924-436d-a655-d6d59fa534e1">

[paper](https://arxiv.org/abs/2209.14169)

## TL;DR
- **I read this because.. :** AAAI CLIP
- **task :** zs classification
- **problem :** I want to increase CLIP's zs classification ability without training
- **idea :** swap image / text encoder features in the middle without learning
- **input/output :** {image, text} -> score
- **architecture :** CLIP ResNet variant
- **objective :** change without learning or have a few-shot refined version
- **baseline :** CoOp, CLIP linear probing, CLIP adaptor
- **data :** ImageNet, Caltech101, OxfordPets, StanfordCars, Flower102, ... (CLIP zs)
- **evaluation :** zs, few-shot accuracy 
- **Result :** Higher performance with zero learning!
- **contribution :** There have been a lot of studies that have tried to do fine-grained better by putting SA in the middle layer, or looking at all seqs at the end, but this study shows that it is possible to improve performance with computations that don't seem that big.
- **etc. :**

## Details
### motivation
<img width="355" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ad9ee477-2e8d-4ee1-b1b4-1ad3cc9f3320">


### architecture
<img width="845" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/60c3cee7-fbde-4b7e-9fbe-91e10a7167b9">

Attention to features that are not projected and then multiplying them by the feature
<img width="393" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6cfc0d44-8eac-44a0-a0c2-1bb0e6a93067">

<img width="395" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/bf45a2ca-b6c9-4be6-8ca4-c1251b1326c5">

The final prediction is the weighted sum of these two modalities aggregated together.
<img width="397" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ec1dc8ab-f342-49e6-bffe-3ab19976f901">


<img width="829" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/78a36ab0-1a81-4614-a4ec-01c708b50f1c">

### Result

<img width="699" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a7a18f8c-5cea-4d18-b093-32da231e8acc">