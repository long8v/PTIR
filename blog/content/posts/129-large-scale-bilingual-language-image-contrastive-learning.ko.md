---
title: "[120] Large-scale Bilingual Language-Image Contrastive Learning"
date: 2023-06-19
tags: ['2022Q1', 'CLIP', 'multilingual']
paper: "https://arxiv.org/pdf/2203.14463.pdf"
issue: 129
issueUrl: "https://github.com/long8v/PTIR/issues/129"
---

<img width="632" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/36493fd1-a8d7-4820-93c9-590f2f9005dc">

[paper](https://arxiv.org/pdf/2203.14463.pdf)

## TL;DR
- **I read this because.. :** multilingual clip
- **task :** multimodal alignment
- **problem :** multilingual clip을 학습하고 싶다. 번역으로 만든 건 그 나라의 문화 / 어휘의 특성을 잡지 못한다
- **idea :** 데이터 모아서 학습
- **input/output :** image + text / similiarity score(for clip)
- **architecture :** image encoder(ViT-B/32) and text encoder(transformer) 
- **objective :** MSE(for MAE) and infoNCE(for CLIP)
- **baseline :** CLIP, UNITER, Visual N-Gram, ImageBERT
- **data :**  web에서 korean {image-text} pair 수집 + 가용한 english {image-text pair} 수집
- **evaluation :** image classification / retrieval
- **result :** clip 보다 영어에서도 더 높은 성능 
- **contribution :** 한국어 CLIP. 학습 관련 몇가지 Finding. result 부분에 diffusion도 하시고 .. 저자가 두명인데 여러 분석 bb
- **etc. :**

## Details

## motivation

- multi-lingual CLIP을 만들고 싶음
- 주로 하는 approach는 그냥 text를 machine translation 돌려서 하는데 이건 그 나라만의 어휘나 문화를 담을 수 없다
- english-korean bilingual 학습
    - 데이터셋 제안
    - training scheme 제안
        - MAE로 1단계로 학습
        - multi crop기법 사용
    - 몇가지 finding
        - 직접 bilingual supervision을 안주더라도 image를 통해서 embedding space가 맞춰지더라
        - SimCLR에서 사용되는 strong augmentation 오히려 방해되더라

## training scheme

- CLIP과 다른 두 가지
- 바로 contrastive로 학습하는게 아니라 MAE로 먼저 vision encoder를 학습
    
<img width="615" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/09a39f2d-931a-4870-80f4-fe05f7483cc8">

    
- multi-crop augmentation 사용
    - standard resolution 224 x 224  / low resolution 96 x 96
- 위 두가지에 대한 ablation
    
<img width="584" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/957f0820-bca1-41c9-91c6-c803812e9f34">


## dataset

- english {image-text} pair
    - CUB200
    - 37.4M의 WIT (108 languages)
    - YFCC15M (clip이 100M에서 filtering한)
    - CC3M
    - CC12M
    - LAION400M
    - LAION이 만든 방식을 따라 cc web dump에서 70M을 추가적으로 만듦
- korea {image - text} pair : 708M 규모
    - 그냥 크롤링 했다고 써져있넹
    - 50M의 연예인 얼굴과 이름 포함
    - korea wikipedia 포함
    - LAION400M이나 CLIP의 WIT 400M보다 훨씬 큼
- 총 합쳐서 ≥ 1B 정도 데이터셋이 될듯

## training detail

- implementation : 다른거 안쓰고 pytorch로만
- text encoder
    - GPT-2 style transformer(?) / 63M / 12 layesr / hid dim 512 / 8 heads
        - gpt-2 style transformer
            
            Layer normalization (Ba et al., 2016) was moved to the input of each sub-block, similar to a pre-activation residual network (He et al., 2016) and an additional layer normalization was added after the final self-attention block. A modified initialization which accounts for the accumulation on the residual path with model depth
            is used. We scale the weights of residual layers at initialization by a factor of 1/
            √N where N is the number of residual layers. 
            
    - tokenizer : 2M의 english / 1.5M korean으로 학습한 BPE 98K vocab size
        - (↔ CLIP은 49K)
        
- visual encoder
    - ViT-B/32
    - 256 x 256 ?

- 기타 hparams

<img width="714" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0946ae42-6466-4952-a172-303f9d472f64">


- training
    - half precision
    - 80개의 A100 → MAE 학습하는데 16시간 / multimodal training하는데 362시간 (15일?)

## Benchmark Dataset

- zs-classification
    - benchmark의 english label을 한국어로 번역해서 사용했음
    - ImageNet / Cifar10 / Cifar100 / CLEVER Counts / Describable Textures Dataset / EuroSAT / FER2013 / Food101 / GTSRB / MNIST / RESIC45 / StanfordCars
    - (in-house data) WebKorean
        - 36,826 images ↔ 428 Korean labels
- zs-retrieval
    - Flickr30k / MSCOCO(english) / MSCOCO(korean)

## result

<img width="716" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/24b7517a-e1c9-470d-8983-b32186ceae07">


- zero-shot classification
    - CLIP보다 평균 3.3% 높은 성능
    - 한국어는 CLIP 성능 처참
        - clip이 a photo of { }랑 가장 가까운 걸로 분류해서 그럼
        - 한국어 데이터가 아예 없었던 건 아닌데 너무 적어서
- zero-shot retrieval
    - 영어 한국어 둘다 성능 굿굿

<img width="659" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/715ac104-3a06-4c59-9f6f-c795118960df">


## findings

- color 왜곡 등 strong augmentation이 classification 등은 더 성능을 높이지만 더 높은 차원의 문제인 retrieval은 더 못하더라

<img width="540" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/083f86d7-cceb-47f0-9668-2304ee94ca7e">

- 두 언어간 직접 contrastive loss를 넣지 않았는데도 image를 같이 보고 있어서 그런지 공간이 맞춰지더라
    
<img width="653" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/fcbf102e-7122-4d57-8c06-1d007ce72ccc">

    
- diffusion을 붙여서 해봤는데 확실히 한국어가 다른 결과를 보이더라?
    - 이건 위의 결과랑 좀 다른거 아닌가 ㅋㅋ similiarity가 1.0은 아니니까 그런건가

<img width="687" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/48f5f095-ee88-4221-a476-d2c03544645d">

