---
title: "[124] LiT: Zero-Shot Transfer with Locked-image text Tuning"
date: 2023-07-06
tags: ['2021Q4', 'google', 'CLIP']
paper: "https://arxiv.org/pdf/2111.07991.pdf"
issue: 135
issueUrl: "https://github.com/long8v/PTIR/issues/135"
---
<img width="1165" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/226c78db-3477-49ba-8a66-687531bb9e40">

[paper](https://arxiv.org/pdf/2111.07991.pdf)

## TL;DR
- **I read this because.. :** pretrained vision backbone을 가져오고 clip 학습할 때 성능이 어떤지?
- **task :** Contrastive Learning
- **problem :** CLIP의 {image - text} pair 너무 nosiy하지 않은가? 그렇다고 supervised로 하기엔 zero-shot transfer능력이 탐난다. CLIP도 pretrained에서 가져오는데 어떤게 가장 효과적일까? 
- **idea :** vision encoder / text encoder를 pretrained + freeze(lock), pretrained + learnable, randomly initialize 이렇게 6개 경우의 수로 나눠서 실험해보자 
- **data :** CC12M, YFCC100M-CLIP(15M), ALIGN류의 4B 데이터
- **input/output :** image, text -> score
- **architecture :** ViT-g/14 + BERT 
- **result :** CLIP, fine-tuned, from sctrach보다 우위. 특히 OOD에서 zs성능이 좋다. image encoder를 lock 시키는게 성능이 제일 좋다. 이 때 vision encoder는 아키텍쳐도 상관없고 supervised든 unsupervised로 학습되든 상관없다. 즉 비교적 clean 한 데이터로 학습된 비전 인코더를 활용하고 text encoder는 비전 인코더의 정보를 읽어내는 식으로만 학습하고 있다. 
- **objective :** InfoNCE
- **baseline :** CLIP, from0scratch, fine-tuned, ALIGN
- **evaluation :** zs OOD ImageNet classification, 7 [VTAB-natural tasks](https://ai.googleblog.com/2019/11/the-visual-task-adaptation-benchmark.html)
- **contribution :** supervised + contrastive를 탐구한 논문. 
- **etc. :** text encoder 종류. feature aggregates는 cache이 나은지 global로 하는게 나은지. multilingual. text encoder size 등 실험이 방대해서 좋았다. 

## Details
기본 아이디어는 이와 같다. CLIP에서 vision encoder와 text encoder 모두 from scratch로 학습하는데 pretrained를 가지고 오고 싶다.
이때 방법은 아래와 같다. 
<img width="562" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ad5f10b9-3205-4b8a-bbab-304d5ba0f764">

- L : pretained model 가져오고 lock
- U : pretrained model 가져오고 unlock
- u : from scratch

그러면 총 6가지의 경우의 수가 나올텐데 이에 대한 ablation은 아래와 같다 (vision tower, text tower 순서)
<img width="565" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e0172c8e-b6dd-4111-8f2b-3baaa2ecfb3c">

ImageNet zs 기준
- LU best -> proposed LiT 
- LU > UU : image encoder를 아예 freeze 하는게 Uu보다 좋은게 surprsing 하다고 함.
- LU ~ Lu : text encoder는 from srcatch나 from pretrained나 성능이 비슷했다. 
- UU > uu : 둘다 pretrained를 가져오는건 from scratch 보다 성능이 좋다 
- UL, uL, LL 3개 다 하위권 : text encoder를 freeze 시키는건 안좋은 성능이 대개 안좋다. uu가 원래 CLIP 학습일텐데 그것보다 안좋음.

retreival은 또 보니까 UU > Lu넹 

<img width="559" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5a07a79f-811f-41c4-9a04-d77fb3dcddff">

<img width="584" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/159d82de-7b54-49d4-b218-2b3ba7841fcb">


LU > UU : 왜 locked 되는게 더 좋은가?

<img width="544" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/52d32b7a-a48c-4949-982e-aa365dedacae">

첫번째 행은 LiT 학습되는 데이터로 loss를 찍어본건데 image encoder가 lock된게 Loss가 높음
두번째 행은 OOD인 data로 평가한건데 이때 lock된 loss가 가장 낮음 -> 즉 image encoder를 lock을 함으로서 ood에 강건하다. contrastive finetuning을 하는게 visual represntation을 하는데 악영향을 준다는 결론. 
(얼핏 #134 와 반대되는 내용 같아 보인당.. 쟤는 반대로 clip이 이미 contrastive로 학습돼서 ood에 강건하고 supervised set에서 ood 능력을 잃어버린다는 내용. 근데 이건 ㅋㅋ 쟤네는 IN이었고 얘네가 supervised learning으로 학습한 ViT는 JFT로 학습됐기 때문에 그런듯 하다.)
마지막 행은 logit 가지고 few-shot linear regression을 한건데 Lu가 가장 성능이 좋음.

image encoder처음에 lock 시키고 점점 unlock 하는 것도 해봤는데 성능이 그렇게 좋아지지 않았다고 함

얼핏 보면 ViT가 supervised setting으로 학습됐으니 더 잘되는거 아니냐? 라고 할 수 있어서 다른 pretraining 기법으로 학습된 애들도 해봄
<img width="553" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9d83d218-7eba-49b2-848f-def8c77e48c7">

다른 방법으로 학습된 애들도 경향성이 비슷했다.

## Ablations
- text encoder
<img width="508" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d313e6fd-9f71-4ac4-ab80-b1501d259fe4">


(yfccm) BERT > T5 ~ ViT(뭔지 잘 모르겠) > mT5
(ours, in-house data) ViT > BERT

> We consider four possible transformer-based text models [63]—the transformer from ViT-B [21] which also resembles that used in CLIP [46], T5-base [47], mT5-base [67], and the classic

- text / image encoder scale 
<img width="556" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4d5626b0-cb6d-4901-8841-9b628a9fa116">

커지니 좋았다 빗금친게 text 키웠을 때 성능 개선.

- multi-lingual training
english only로 정제하지 않고 다 같이 학습했을 때 english 성능은 나빠지지 않고 다른 애들 성능은 좋아졌다.
<img width="550" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7662d436-b771-4f02-8618-38e6d49f4667">

이때 학습할 때 mT5 tokenizer 쓰고 pretrained multilingual로 시작했어야 성능이 잘 나왔던 것 같다.

- local loss vs global loss

<img width="512" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b0d2a78d-e3ef-43c0-a906-53b318e4111b">

global loss가 좋았고 bs는 무조건 커지는게 더 좋았다.
LiT는 image encoder가 freeze 되어 있기 때문에 image precomputation를 하는게 메모리 효율적이었다.