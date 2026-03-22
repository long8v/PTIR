---
title: "DataComp: In search of the next generation of multimodal datasets"
date: 2023-10-05
tags: ['dataset', 'CLIP', '2023Q2']
paper: "https://arxiv.org/pdf/2304.14108.pdf"
issue: 145
issueUrl: "https://github.com/long8v/PTIR/issues/145"
summary: "Reading curiously about dataset filtering / evaluation - dataset disclosure. Different filtering techniques ablation. competition promotes data-focused research directions."
---
<img width="680" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/aba06e68-7da7-4150-b0bf-5e6d05ffdbd9">

[paper](https://arxiv.org/pdf/2304.14108.pdf), [page](https://www.datacomp.ai/) 

## TL;DR
- **I read this because.. :** I read this because I was curious about dataset filtering / evaluation
- **task :** CLIP
- **problem :** open large image - text set 
- **idea :** common crawl + study 
- **input/output :** image / text -> similiarity score
- architecture :** Same as CLIP
- **objective :** contrastive loss 
- **baseline :** LAION-2B 
- **data :** CommonPool 14B -> (filtered) DataComp 1.4B
- **evaluation :** zero-shot imagenet /imagenet-A/ .. detailed below + retrieval
- **result :** Higher performance than LAION-2B
- **contribution :** Making datasets publicly available. Various filtering techniques ablation. competition to stimulate research directions that focus on data.
- **etc. :**

## Details
### Evaluation
<img width="648" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3951d1db-dac8-4a4f-a46e-47ebe5830c9a">

- zs-image classifcation 
- 22 datasets evaluated in the original CLIP paper
- 6 distrbution shifted imagenets : ImaeNet-Sketch, ImageNet-V2, ImageNet-A, ImageNet-O, ImageNet-R, ObjectBet
- 13 VTAB data: https://arxiv.org/pdf/1910.04867.pdf
- 3 WILDS data: benchmark of 10 datasets reflecting a diverse range of distribution shifts that naturally arise in
real-world applications, such as shifts across hospitals for tumor identification; across camera traps
for wildlife monitoring; and across time and location in satellite imaging and poverty mapping. e.g. WILDS: A benchmark of in-the-wild distribution shifts. iWildCam2020-wilds(wildlife..), Camelyon17-wilds(cellular tissue..), RxRx1-wilds(RNA...)
- WinoGAViL : commonsense association task https://paperswithcode.com/dataset/winogavil I don't understand what it is even when I look at it.
- Finally, two fairness data: FairFace, UTKFace -> race-matched classification

### Some discoveries
- High correlation between zs retrieval and linear probing
<img width="680" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b6bccffa-b1fb-46aa-9ea0-c1b587e4984c">

- High correlation between performance with small datasets and performance with large datasets
<img width="640" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d395fdc0-5bc9-488c-8060-4c58dfcdb45a">

- High correlation between imagenet and other datasets
<img width="575" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ba7f48b3-0dd6-4906-adea-d732f3b1dcee">

Children with low correlations performed closer to random guesses.
- I don't understand even looking at it: https://paperswithcode.com/dataset/winogavil
- Wildlife: https://paperswithcode.com/dataset/iwildcam-2021
- Autonomous driving: https://github.com/harshilpatel312/KITTI-distance-estimation
- A collection of misclassifications from ImageNet: https://paperswithcode.com/dataset/imagenet-a
- Satellite image: https://paperswithcode.com/dataset/fmow
- Airplane type classification: ttps://www.robots.ox.ac.uk/~vgg/data/fgvc-aircraft/
- Categorize which country this photo was taken in: https://paperswithcode.com/dataset/country211
- Medical: https://camelyon17.grand-challenge.org/, https://patchcamelyon.grand-challenge.org/
- 3D objects relationship: https://paperswithcode.com/dataset/clevr

It's all so esoteric...
The only thing useful here is imagenet-a and country211?!
And unsurprisingly, the OCR side datasets (rendered SST2, SVHN) were also uncorrelated.

c.f. hparam like bs has little change in rank for data filtering
<img width="666" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/10c1b986-d4d8-4343-8b8c-0263bb769200">

