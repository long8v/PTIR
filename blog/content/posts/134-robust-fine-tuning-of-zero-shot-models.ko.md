---
title: "[123] Robust fine-tuning of zero-shot models"
date: 2023-07-05
tags: ['openAI', 'google', 'CVPR', '2022Q3', 'CLIP', 'domainshift']
paper: "https://arxiv.org/abs/2109.01903"
issue: 134
issueUrl: "https://github.com/long8v/PTIR/issues/134"
---
<img width="879" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1ed148a8-bf85-445b-a25f-30dfaeec5199">

[paper](https://arxiv.org/abs/2109.01903)

## TL;DR
- **I read this because.. :** CLIP pretrained 능력을 잃어버리지 않으면서 보수적으로 학습하기 위한 method. LiT 관련 논문 찾다가 찾음
- **task :** CLIP 
- **problem :** CLIP에서 reference 도메인에 대해 finetuning을 하면 CLIP에서 원래 학습된 general domain에 대한 지식을 잃어버릴 수도 
- **idea :** CLIP zero-shot 능력과 target domain에 finetune한 모델을 앙상블 하자 -> weight interpolate를 통해 앙상블하자!
- **input/output :** {image, text} -> score
- **architecture :** CLIP, ViT, BASIC-L
- **objective :** InfoNCE
- **baseline :** zs-CLIP, finetuned CLIP. 
- **data :** WIT(clip), JFT-300M(vit) -> ImageNet, ImageNetV2, ImageNet-R, ImageNet sketch, ObjectNet, ImageNet-A
- **evaluation :** 원래 도메인과 shift된 도메인에서의 정확도. 
- **result :** ImageNet 성능을 유지하면서도 domain shift가 있는 애들한테도 성능 개선
- **contribution :** 간단한 아이디어 + implement 하기 쉬우면서도 성능이 좋음
- **etc. :** 

## Details
### Related work 
- Stochastic Weight Averaging
https://arxiv.org/pdf/1803.05407.pdf

<img width="478" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e3f652c4-751c-4d6e-9e21-0746e7e1c53e">

param의 moving average를 쓰는게 일종의 ensemble 효과를 가지고 있다


## domain shift data
<img width="974" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/baf58cdc-073a-4335-8113-9fbe385dd3be">


## Weight-space ensemble for finetuning
너무 간단..
1) pretrianed CLIP을 가지고 와서 target domaind에 대해서 ft. fully ft(end-to-end)할 수도 있고 마지막 classifier만 할수도 있다(LC)
2) mixing coefficient를 두고 각 element-wise로 average를 구한다
<img width="313" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/60c60d4d-c6b2-4ad1-8fd3-23c900554f21">

여기서 alpha는 greedy하게 찾아야 하나 0.5로 설정했을 때 optimum이랑 거의 비슷하게 나왔다.

## Result
<img width="870" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/61e9a158-4897-44be-bf5e-0bf037f3322f">

첫번째 그림 : x축은 ImageNet(reference distribution)이고 y축은 distribution shift가 있는 데이터셋들 
보라색이 zs clip 성능이고 파란색이 그냥 그 데이터로 학습한 애들. 주황색이 그 데이터로 finetune 한 애들 
두번째 그림 : Wise-FT를 하면 reference 정확도 감소 없이 distribution shift 있는 애들 성능을 늘릴 수 있음

<img width="971" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f317d422-5a28-4ba1-babb-85d35507bca1">

finetune 한것들 보면 distribution shift 있는것들 성능이 떨어짐 
제안한 WISE-FT 보면 reference domain에서도 성능이 ft보다 더 좋아지고 (86.2 -> 87.1) distribution shift가 있는 애들도 좋아짐

<img width="963" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0fbc55c9-1d84-4ae1-8952-bf069ac2e40f">

clip자체가 hparam에 따라 성능이 너무 흔들리는 경향성 -> weight-space ensemble 하면 frontier! 

<img width="949" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/157c5619-7883-4b30-a611-d409632ec457">

각각의 도메인에 대해 finetuning 한 것보다 성능이 좋음! 

## Analysis 

<img width="973" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/db5d3e79-b814-4d7c-8b73-ee4b4649ab7b">

zero-shot과 linear classifier는 경향이 달랐고 linear-classifier 끼리는 경향이 비슷했다.  -> 더 큰 앙상블 효과가 있었던 듯 하다 

<img width="988" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5923e0fb-0553-4a4b-9c30-00ff7b266457">

output을 ensemble하는 것보다 weight ensemble하는게 더 성능개선이 좋았다! 
