---
title: "[141] Alpha-CLIP: A CLIP Model Focusing on Wherever You Want"
date: 2023-12-15
tags: ['multimodal', 'CLIP', '2023Q4']
paper: "https://arxiv.org/pdf/2312.03818.pdf"
issue: 153
issueUrl: "https://github.com/long8v/PTIR/issues/153"
---
<img width="1148" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6c001bf6-f46d-40bf-bc28-cd0d7da48693">

[paper](https://arxiv.org/pdf/2312.03818.pdf), [page](https://aleafy.github.io/alpha-clip/), demo 

## TL;DR
- **I read this because.. :** 성현님 추천. region caption / detailed caption 생성에도 쓰일 것 같고 fine-grained clip에 대한 궁금증이 있어서 봄.
- **task :** CLIP with mask
- **problem :** CLIP은 global하게 정보를 뽑는데 finer understanding을 하고 싶다. 이미지 전체 맥락도 이해하고 이미지 자체도 distort하지 않고 어떻게?
- **idea :** CLIP의 ViT 앞에 conv연산 부착, RGB conv과 alpha conv 따로 해서 아마 feature summation해서 ViT에 넘겨줌
- **input/output :** (clip) image + mask, text -> similarity 
- **architecture :** CLIP
- **objective :** contrastive loss
- **baseline :** (image classification) CLIP, Red Circle(빨간색 동그라미 치는거), MaskCLIP (REC) CPT, ReCLIP, Red Circle (OVD) MaskImageNet, Detic-ImageNet. (MMLM) LLaVA-1.5, BLIP-2 , ... 
- **data :** GRIT-20m + ImageNet 460K에 대해서 추가적인 파이프라인으로 rgba - region text 생성
- **evaluation :** 각 벤치마크에 맞게.. MMLM은 백본만 갈아끼운 경우도 있고(text encoder를 freeze 시켜서 가능함) finetune 시킨 경우도 있음 
- **result :** imagenet 성능 개선, MLLM hallucination 경감 등 
- **contribution :** 간단한 아키텍쳐 + 학습도 별로 안 했는데 문제를 여러 많이 tackle한 듯.  
- **etc. :** 우리도 SAM 써서 뭐 해볼까? region level clip이 hallucination을 줄이긴 하는군 

## Details
### motivation
<img width="700" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2c8a3c51-6ac0-4afa-b2c2-57346ffcef3b">

- image recognition: classification 더 잘함 (imagenet이 single label이지만 사실상 multi-label) / referring expression comprehension(REC)으로도 쓰일 수 있고 / OVD의 data generation 용도로도 쓰일 수 있음
- MLLM의 backbone: hallucination이나 model bias를 줄여준다
- generation: 원하는 부분을 살려서 바꿀 수 있고 multi object일 때의 문제점도 해결

### Region-focusing strategy 
<img width="700" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/72463f30-5412-4f8d-baff-f1dc57cb4b25">

이미지 자체를 distort하거나 전체 context 정보가 생략/삭제 됨

### RGBA Region-Text Pair Generation
<img width="700" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2ca9f3ea-bb2c-4bf9-b92f-22f175d4dfed">
- Grounding data pipeline: GRiT 데이터가 이미 바운딩 박스와 region text. 여기에 SAM 돌려서 mask 확보
- Classification data pipeline: SAM -> crop -> clip score로 할당 -> BLIP으로 caption하고 class도 붙임

### Alpha-CLIP
<img width="700" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a10b888b-13b3-454a-a19b-ae12006bf110">

- text encoder freeze
- RGB conv + alpha conv 추가
- alpha는 0~1 사이인데 초기에 0으로 시작하도록
- 그리고 alpha + rgb conv는 elementwise summation(? 안나와있음)
- 에폭의 10% 샘플은 image - text pair로 학습

### Result
- ImageNet classification
<img width="600" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/051d3e7f-5f4c-45e4-9d3a-790401af636b">

imagenet-s가 imagenet에 semantic segmentation 걸려있는건데 저 gt를 alpha로 줬을 때 성능 개선
또는 bbox로 줬을 때도 개선, 또는 그냥 전체 이미지를 Mask로 보아도 성능이 떨어지지 않음(새로운 데이터로 추가학습해서 인듯)

- REC
<img width="600" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f756e0b3-4bf3-4d73-97a7-b482df53eaf4">

<img width="600" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/73393866-2dc5-4e35-ac30-304973848199">

파이프라인이 좀 신기한데 ㅋㅋㅋ SAM으로 mask들 뽑고 그 후보들 중에 해당 텍스트랑 가장 가까운 mask를 찾으면 그게 정답

- OVD
<img width="600" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b4ccca24-e416-42b1-a1f3-a95b4217f118">

pseudo-labeling 방식 + AlphaCLIP을 백본으로 사용했더니 성능이 더 올랐다

- Region-level captioning 
그냥 backbone만 갈아끼워도 working. 
<img width="600" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4a3e013b-519c-4eca-aff9-c7e50c5a4780">

finetune한 정량 평가 결과는 아래와 같음
<img width="600" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4c59f2df-eea7-4cfa-b4a4-89fda6ed5462">