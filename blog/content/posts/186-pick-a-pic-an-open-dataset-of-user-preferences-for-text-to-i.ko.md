---
title: "[167] Pick-a-Pic: An Open Dataset of User Preferences for Text-to-Image Generation"
date: 2024-07-24
tags: ['NeurIPS', '2023Q4', 'generation']
paper: "https://arxiv.org/abs/2305.01569"
issue: 186
issueUrl: "https://github.com/long8v/PTIR/issues/186"
---
<img width="600" alt="image" src="https://github.com/user-attachments/assets/8768df02-a494-4fcf-93d9-a93551780612">

[paper](https://arxiv.org/abs/2305.01569), [code](https://github.com/yuvalkirstain/PickScore), [dataset](https://huggingface.co/datasets/yuvalkirstain/pickapic_v1)

## TL;DR
- **I read this because.. :** 개인연구 관련 연구
- **task :** T2I generation 생성물에 대해 human preference 학습 
- **problem :** FID로 측정하는것은 human preference를 잘 나타내지 못한다. open source preference dataset이 필요하다.
- **idea :** 웹페이지 만들어서 human preference data 모음
- **input/output :** {image, prompt} -> score
- **architecture :** ViT-H/14 
- **objective :** KL divergence
- **baseline :** Aesthetic score, CLIP-H, ImageReward, HPS, Human Expert
- **data :** Pick-a-Pic data (논문에서 사용된 데이터는 583K의 training / 500 / 500 valid and test samples) 
- **evaluation :** score의 차이가 threshold 이상인걸 더 prefer한다고 보고 정확도. human expert와의 spearman correlation
- **result :** 가장 높은 accuracy, correlation. 이걸 사용하여 Classifier-free guidance 기법을 사용했더니 더 결과물이 prefer되었다.
- **contribution :** 엄청 큰 데이터 공개. 모델도 공개. 이걸로 성능 개선도 공개. 
- **etc. :** neurips 논문은 데이터 공개가 참 많은듯 

## Details
<img width="1109" alt="image" src="https://github.com/user-attachments/assets/bfaf0266-b1de-44c8-8835-a56427c91ae4">

## annotation 
<img width="1117" alt="image" src="https://github.com/user-attachments/assets/dfe4f6a3-99f8-4e56-a347-f1e321aa8091">

- prompt를 사용자가 입력
- 이미지 생성은 Stable Diffusion 2.1, Dreamlike Photoreal 2.0, Stable Diffusion XL variants

## Pick-a-Pic Dataset
- 총 968K ranking
- 논문에서 사용된건 583K ranking from 37K prompts and 4K users
- 데이터 퀄리티를 신경쓰려고 여러가지 함(이메일 인증, 봇 탐지...)

## PickScore
- CLIP
<img width="455" alt="image" src="https://github.com/user-attachments/assets/d331a788-3465-4ce6-a580-5c459036e1a4">

- finetuning loss
<img width="533" alt="image" src="https://github.com/user-attachments/assets/0b4ca9fe-c89b-417a-bbdc-be97c3f0497e">

$s$ : score
$x$ : prompt
$y_1, y_2$: image

in-batch negative도 해봤는데 별로 성능이 안좋았다고 함
trainingdms 4000 step, lr 3e-6, bs 128, warmup 500 step
8 A100으로 1시간도 안걸렸다고 함. 

## Result
- rerank vis CLIP-H vs Pick-a-Pic 
<img width="625" alt="image" src="https://github.com/user-attachments/assets/b594cda2-949c-41aa-8855-4c7c6e35fa71">

- accuracy
<img width="461" alt="image" src="https://github.com/user-attachments/assets/eff4e752-773e-4f19-ae3c-56919c906fa7">

- classifier-free guidance로  학습한 것
<img width="671" alt="image" src="https://github.com/user-attachments/assets/4310a8df-0128-45c9-86e2-21204ab065cd">

- correlation between human expert 
<img width="433" alt="image" src="https://github.com/user-attachments/assets/206c0c4e-b631-4911-9a1a-5b621b4cb876">

- 다른 모델들과 비교
<img width="1087" alt="image" src="https://github.com/user-attachments/assets/f6ab52e2-90e5-42f1-a753-518ccc6d8f16">

- why not COCO?
아직도 가장 많이 사용되는 게 COCO prompt를 사용한 이미지 생성이라고 함 
COCO는 일반적인 object를 사용하는데 그게 사용자가 바라는것과는 상이하다.
<img width="1100" alt="image" src="https://github.com/user-attachments/assets/81a06a24-7706-46ed-972d-0baa4cacbfbd">

- 그냥 생성한 것 vs PickScore로 rerank한 것 
<img width="1103" alt="image" src="https://github.com/user-attachments/assets/cfa74189-9351-4546-b0e0-3e7636acc9f1">

