---
title: "[156] Interpreting CLIP's Image Representation via Text-Based Decomposition"
date: 2024-05-06
tags: ['ICLR', 'CLIP', 'XAI', '2023Q4']
paper: "https://arxiv.org/abs/2310.05916"
issue: 172
issueUrl: "https://github.com/long8v/PTIR/issues/172"
---

<img width="590" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/71414178-f410-4c7b-8d37-44ddca680009">

a.k.a TextSpan
[paper](https://arxiv.org/abs/2310.05916), [code](https://github.com/yossigandelsman/clip_text_span) 

## TL;DR
- **I read this because.. :** CLIP spurious cues로 검색하다가 나옴 
- **task :** CLIP ViT의 layer, head의 텍스트 표현 뽑기
- **idea :** human + GPT로 3948개의 일반적인 표현 문장을 만든 뒤에 이미지 표현과의 내적에서 variance가장 높은 row를 고른 뒤 이를 projection에 추가하는 방식 
- **input/output :** {image, model} -> text explanation of ViT layer and heads
- **architecture :** ViT-B-16, ViT-L-14, ViT-H-14
- **baseline :** LRP, Partial-LRP, rollout, raw attention, GradCAM, Chefer2021
- **data :** ImageNet(mean ablation), Waterbirds dataset(reducing spurious cues), ImageNet-Segmentation(zs-segmentation)
- **evaluation :** accuracy(imagenet), worst-group accuracy(waterbird), pixel accuracy/mIoU/mAP (zs-segmenatation)
- **result :** 마지막 4개의 MSA layer만 최종 예측에 영향을 주고 다른 레이어들은 영향을 별로 안 줌, qualitative하게 매우 재밌는 결과, zs-segmentation에서 sota
- **contribution :** CLIP의 각 표현을 text로 설명 가능하게 알고리즘 제안.
- **etc. :**

## Details
### related work 
- Multimodal neurons in artificial neural networks https://openai.com/index/multimodal-neurons
  - CLIP의 레이어, 헤드 별로 학습된 표현이 매우 해석 가능하다는 논문 
- Disentangling visual and written concepts in CLIP
  - 위의 방법론을 활용해서 이미지 표현에 글자를 쓰고 지우고 하는 논문

  
### Preliminary findings
<img width="559" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3f6a8f49-ad97-4738-a368-276fd40b0a67">

last 4 layer의 MSA만 성능에 영향을 주고 MLP나 그전의 MSA 레이어들은 mean ablate를 해도 성능에 큰 영향이 없었다.

### Decomposition to head
<img width="459" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7a531747-1ddf-4856-a8ed-67e627cabce6">

MSA를 위와 같이 표현할 수 있음 $\alpha$는 attention score 

<img width="500" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/033cd112-9154-4ecb-8719-5db617a102fe">

여기에 projection $P$ 까지 포함해서 표현하면 위와 같은 식이 됨. 
즉 레이어, head, patch 별로 projection과 attention 연산 $c_{i, j, h}$를 summation하여 각 레이어, 헤드 등의 표현을 구할 수 있음

### TextSpan algorithm
<img width="754" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/90028fb9-3c34-4541-8ef7-248c89dc28dc">

복잡해 보이는데 별거 없음 
- layer, head 별 attention output $C\in\mathbb{R}${K\times d'}$와 text representation $R\in\mathbb{R}^{M\times d'}$와 행렬 곱 한다음에 가장 분산을 높게 하는 표현 j를 찾은 뒤 이 $\tau$를 projection에 추가함. 그리고 이 표현을 C와 R에 업데이트해주어서 이 표현이 다음 표현과 orthogonal 하게 표현을 바꿔줌 (PCA와 비슷한 느낌)

이렇게 나온 layer / head 별 표현들 
<img width="728" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c816c812-e1ce-4c34-9454-2d3d230a8f49">

## Result
### Quantitative 
<img width="733" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/81595935-8f36-4140-87ad-f94346fcf5bc">

### Qualitative
<img width="766" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/dc248018-e6e7-422d-98ff-6d0b24cbc4bf">

<img width="774" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b54d5729-caf0-4b6f-8312-2db74b512310">

<img width="761" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/af75eefa-ca97-4ec8-b9f9-f48e87562eba">
