---
title: "[133] DataComp: In search of the next generation of multimodal datasets"
date: 2023-10-05
tags: ['dataset', 'CLIP', '2023Q2']
paper: "https://arxiv.org/pdf/2304.14108.pdf"
issue: 145
issueUrl: "https://github.com/long8v/PTIR/issues/145"
---
<img width="680" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/aba06e68-7da7-4150-b0bf-5e6d05ffdbd9">

[paper](https://arxiv.org/pdf/2304.14108.pdf), [page](https://www.datacomp.ai/) 

## TL;DR
- **I read this because.. :** dataset filtering / evaluation에 대해 궁금해서 읽음
- **task :** CLIP
- **problem :** open large image - text set 
- **idea :** common crawl + study 
- **input/output :** image / text -> similiarity score
- **architecture :** CLIP과 동일 
- **objective :** contrastive loss 
- **baseline :** LAION-2B 
- **data :** CommonPool 14B -> (filtered) DataComp 1.4B
- **evaluation :** zero-shot imagenet / imagenet-A/ .. 아래 자세히 서술 + retrieval 
- **result :** LAION-2B보다 더 높은 성능
- **contribution :** 데이터셋 공개. 다양한 filtering 기법 ablation. competition으로 데이터에 집중하는 연구 방향 촉진.
- **etc. :**

## Details
### Evaluation
<img width="648" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3951d1db-dac8-4a4f-a46e-47ebe5830c9a">

- zs-image classifcation 
- CLIP 원래 논문에서 평가한 22개 데이터셋
- 6개의 distrbution shift된 imagenet : ImaeNet-Sketch, ImageNet-V2, ImageNet-A, ImageNet-O, ImageNet-R, ObjectBet
- 13개의 VTAB 데이터 : https://arxiv.org/pdf/1910.04867.pdf
- 3개의 WILDS 데이터: benchmark of 10 datasets reflecting a diverse range of distribution shifts that naturally arise in
real-world applications, such as shifts across hospitals for tumor identification; across camera traps
for wildlife monitoring; and across time and location in satellite imaging and poverty mapping. e.g. WILDS: A benchmark of in-the-wild distribution shifts. iWildCam2020-wilds(야생동물..), Camelyon17-wilds(세포조직..), RxRx1-wilds(RNA...)
- WinoGAViL :  commonsense association task https://paperswithcode.com/dataset/winogavil 봐도 뭔지 이해가 안되넹 
- 마지막으로 fairness 데이터 두개 : FairFace, UTKFace -> 인종 맞추는 classification 

### 몇가지 발견들 
- zs retrieval과 linear probing의 높은 correlation 
<img width="680" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b6bccffa-b1fb-46aa-9ea0-c1b587e4984c">

- 작은 데이터셋으로 한 성능과 큰 데이터셋으로 한 성능의 높은 correlation
<img width="640" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d395fdc0-5bc9-488c-8060-4c58dfcdb45a">

- imagenet과 다른 데이터셋간의 높은 correlation
<img width="575" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ba7f48b3-0dd6-4906-adea-d732f3b1dcee">

correlation이 낮은 애들의 성능이 random guess와 가까웠다.
- 봐도 이해가 안됨 : https://paperswithcode.com/dataset/winogavil
- 야생동물 : https://paperswithcode.com/dataset/iwildcam-2021
- 자율주행 : https://github.com/harshilpatel312/KITTI-distance-estimation
- 이미지넷에서 오분류된 거 모아놓은 것 : https://paperswithcode.com/dataset/imagenet-a
- 인공위성 이미지 : https://paperswithcode.com/dataset/fmow
- 비행기 종류 분류 : ttps://www.robots.ox.ac.uk/~vgg/data/fgvc-aircraft/
- 이 사진이 어느 나라에서 찍혔는지 분류 : https://paperswithcode.com/dataset/country211
- 의료쪽 : https://camelyon17.grand-challenge.org/,  https://patchcamelyon.grand-challenge.org/
- 3d 물건들 관계 : https://paperswithcode.com/dataset/clevr

다 난해하기 짝이 없네..
그나마 여기서 쓸만한건 imagenet-a와 country211 정도?! 
그리고 당연하게도 ocr 쪽 데이터셋 (rendered sst2, svhn)도 correlation이 ㅇ없었다.

c.f. bs과 같은 hparam에 data filtering의 rank는 거의 바뀌지 않았다
<img width="666" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/10c1b986-d4d8-4343-8b8c-0263bb769200">

