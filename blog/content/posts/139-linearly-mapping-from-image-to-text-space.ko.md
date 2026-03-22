---
title: "[127] Linearly Mapping from Image to Text Space"
date: 2023-08-17
tags: ['multimodal', 'ICLR', '2023Q1']
paper: "https://arxiv.org/abs/2209.15162"
issue: 139
issueUrl: "https://github.com/long8v/PTIR/issues/139"
---
<img width="548" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/de8b07ca-5693-44c6-baa0-e692fbb7fa10">

[paper](https://arxiv.org/abs/2209.15162)

## TL;DR
- **I read this because.. :** CLIP pretrained가 LM에 붙일 때 더 좋은게 맞나? image only로 학습된 vision backbone이 VLM에서 더 좋을까?
- **task :** image captioning, VQA
- **problem :** VLM에서 어느 pretrained vision backbone이 좋은가?
- **idea :** Frozen, MAGMA 보다 더 harsh한 셋팅인 linear map만 학습해서 성능을 뽑아보자 -> LIMBeR
- **input/output :** image, task query, (optional) question 
- **architecture :** (vision) CLIP RN50x16, NFRN50, BEiT-Large (language) GPT-J(6billion) (linear map) 4096 dim projection
- **objective :** language model loss 
- **baseline :** MAGMA, Blind(이미지 안보는), NFRN50을 tuning
- **data :** (train) CC3M -> (eval) NoCaps, COCO, VQAv2
- **evaluation :** CIDEr-D, CLIP-S, Ref-S, {0,1,2,4}-shot accuracy
- **result :** 더 많이 trained한 MAGMA보다 성능이 더 좋은 경우가 많음. freeze해도 충분하다. 
- **contribution :** 여러 vision backbone에 대한 ablation.
- **etc. :**

## Details

- 아키텍쳐 자체는 간단! vision backbone 거친 feature map에 linear projection 거치고 이를 lm의 soft prompt처럼 prefix로 넣어서 vlm 학습. 이때 linear projection만 학습하는게 포인트
<img width="553" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4c4dd5d4-e13d-4603-be8d-052d19cbebba">

- 이 때 성능 분석한게 재밌다
<img width="600" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/75d11a61-d1d1-41ac-8b5e-d869effe22c7">

1) MAGMA가 비슷한 아키텍쳐로 vision backbone + LM에 adaptor training하는 건데, 이것보다 제안한 LiMBER가 성능이 더 좋은 경우가 많다.
2) vision backbone 중에 CLIP은 language supervision이 들어간것, BEiT는 전혀 안들어간 것(self-supervision), NFRNet50은 ImageNet22K로 되어있어서 중간 정도 들어가 있다고 볼 수 있는데(classification이지만 결국 분류가 WordNet 기반으로 있어서(?) indirect하게 language supervision이 들어가 있다고 할 수 있을듯) CLIP이 가장 좋았다
3) 특히 BEiT가 가장 재밌는데, VQA {1,2,4}-shot을 보면 blind(이미지 아예 안보고 VQA)보다 성능이 안 좋다. random NFRNet 보단 좋지만 거의 도움이 안된다고 볼 수 있다.
4) 근데 BEiT를 decoder에 붙여서 image classification(데이터 뭐썼는지는?)에 추가학습한 BEiT-FT를 가지고 붙이면 오히려 CLIP보다 성능을 넘는 것도 있다 -> 결국 MAE나 BEiT같은 self-supervision 계통은 downstream task에 맞게 좀 finetune을 하는 과정이 필요한듯.

c.f. 
<img width="627" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7fe10ace-98f7-4746-86ba-ba6006e3c6c5">

MAE 논문에서도 linear probing할 때는 classification이랑 조금 더 가까운 InfoNCE loss로 학습된 MoCo보다 성능이 안좋았음 
-> but layer finetune할 때는 더 좋아지기도 
but... [Masked Autoencoding Does Not Help Natural Language Supervision at Scale](https://openaccess.thecvf.com/content/CVPR2023/papers/Weers_Masked_Autoencoding_Does_Not_Help_Natural_Language_Supervision_at_Scale_CVPR_2023_paper.pdf) 이런 논문도. CLIP에서 million scale에서는 MAE를 하는게 도움 되지만 billion에서는 오히려 악화시킨다 
-> 결국 적은 양의 데이터에 대해서는 self-supervision이 빛을 발하지만 clip 같이 large corpus가 있는 경우에는 굳이 안해도 되는? 

BEiT의 failure case들
<img width="815" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/04d74bd3-1409-437d-8daa-c238a64c12e8">


<img width="678" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ed91e167-b849-4b55-b298-01ded0779b51">

여러 caption metric이 있는데 vision backbone 의 우위는 일관적으로 나온다

