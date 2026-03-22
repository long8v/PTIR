---
title: "[146] Transformer Interpretability Beyond Attention Visualization"
date: 2024-02-06
tags: ['2020Q1', 'CVPR', 'XAI']
paper: "https://arxiv.org/abs/2012.09838"
issue: 158
issueUrl: "https://github.com/long8v/PTIR/issues/158"
---
<img width="733" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6c23907b-1b41-4d51-bcc8-c09c7ff270ef">

[paper](https://arxiv.org/abs/2012.09838), [code](https://github.com/hila-chefer/Transformer-Explainability)

## TL;DR
- **I read this because.. :** a.k.a TiBA. explainable CLIP score에 관심 있어서. preliminary로 읽음 
- **task :** neural network의 interpertability
- **problem :** 기존의 Layer-wise Relevance Propagation(LRP) 방법을 transformer에 적용하려면 (1) skip-connection과 (2) activation에서 ReLU를 사용하지 않아 negative 가 나와서 문제가 된다. 
- **idea :** (1) positive / negative 둘 다 바꿀 수 있게 바꾸고 (2) normalization term을 추가하고 (3) attention과 relevancy score를 결합하여 점수를 구한다. 
- **input/output :** image -> class // heatmap in image
- **architecture :** ViT-B, BERT
- **baseline :** rollout, raw attention, GradCAM, LRP, partial LRP
- **data :** ImageNet 2012, ImageNext-Segmentation, Movie Reviews
- **evaluation :** AUC(perturbation tests), pixel accuray / mAP / mIoU(segmentation), token-F1(Movie Reviews)
- **result :** 기존 대비 좋은 성능 
- **contribution :** transformer에서 explainabity를 한게 attention flow가 있는데 속도가 느리다는듯
- **etc. :** 읽다보니 예전에 CVPR tutorial에서 설명해주셨던 분! 또 논문 찾다보니 XAI 쪽에 been kim 씨가 있던데 한국인 여성이어서 반가웠다 

## Details
### Method
<img width="487" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ded80395-6445-48fc-bcf7-02d9fda49802">

transformer의 각 attention head에 대해서 LRP-based relevance를 구하고 이걸 gradient랑 결합해서 class-specific visualization을 하는게 목표

#### Relevance and gradients
chain rule로 n번째 레이어의 input x의 index j인 $x_j^{(n)}$의 $y_{t}$ (class t에 대한 model의 output)의 gradient는 아래와 같이 정의됨

<img width="369" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5bf5b064-94f1-4df9-907f-df92dc3114a3">

여기서 $L^{(n)}(X, Y)$를 두개의 텐서 X, Y에 대한 layer operation이라고 정의하면 두 텐서는 feature map / weight가 되고 이걸 Deep Taylor Decomposition을 따르도록 하면 relevance는 아래와 같이 구해진다. 

<img width="387" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4e25c16a-8ffd-4f30-9bd8-b983e482c85c">

deep taylor decomposition은 taylor 근사를 통해 relevance를 구하는 방식 http://arxiv.org/abs/1512.02479
<img width="299" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/73eeb0a5-3f92-4174-b537-7eef77ddc6e6">

걍 gradient로 저 output을 근사한다~ 정도만 이해

conservative rule에 따라 n 번째의 레이어의 relevance의 합과 (n - 1)번째의 relevance의 합은 같아져야함
<img width="226" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a88d1c11-626f-4184-ba0d-03c02f65f0be">

이것도 위의 논문에서 나오는데 f(x)가 relevance의 sum이랑 같아지는걸 의미.
<img width="394" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/68b2a3d6-a404-4acf-98a0-8f3d1e91a1db">

LRP 논문에서는 activation으로 ReLU를 상정했기 때문에 positive value만 보도록 함 
<img width="453" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/45e59250-01e7-428a-82e0-d7515b4c31d4">

- $v^+$ : max(0, v)

그런데 GeLU 같은걸 쓰게 되면 negative도 나올 수 있게 됨
그래서 이걸 걍 postivie subset인 애들에 대해서 구하는걸로 변경 (...? 이게 뭐가 달라지는지 모르겠음)
<img width="392" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f4c11814-6d96-4022-a44d-43e690fa91a4">
<img width="189" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/55ac8076-54fe-42f9-a212-2ea801361179">

그리고 맨 처음 초기화는 class t에 대한 one-hot 벡터로 설정 

### non parametric relevance propagation
transformer에는 두개의 feature map tensor가 mixing되는 두개의 연산이 있음 (<=> 아까는 weight와 feature map이었는데 이와는 다름)
(1) skip connection (2) matrix multiplication임 

두개의 tensor u, v가 있을 때 두 operator를 아래와 같이 정의함 
<img width="540" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/dd348b39-fd03-43fd-bb0a-d6be1c0e1e8c">

앞에껀 u에 대한 relevance score / 뒤에껀 v에 대한 relevance score
skip connection에서 relevance score가 너무 커지는 경향성이 있었음. 이를 해결하기 위해 normalization을 추가해줌

<img width="533" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0f225378-eca5-4367-9ea3-fa1812dd2470">

###  Relevance and gradient diffusion
<img width="521" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/acc4dc19-fbb2-47ae-aee9-5fe5f7c5da83">

self-attention연산에 대해서 위의 절차로 구하게 되면 아래와 같이 됨
<img width="348" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/679b6039-9330-41ba-8da9-69d211cf4018">

$A^{(b)}$ : b번째 block의 attention map
$E_h$: heads dimension 에 대해 평균
gradient의 positive 부분만 남김. 

rollout의 경우 단순히 attention map에 대해서 iterative하게 곱하는 형식 

<img width="479" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/595714b3-0c49-4aa5-ad8a-911eb937d78a">

### Obtaining the image relevance map
결과적으로 나오는건 s x s의 matrix C 
각 row는 해당 토큰이 다른 토큰에 대한 relevance map
이 연구에서는 분류 모델에 대해서만 집중했으니까 `[CLS]`토큰에 대한 relevance score만 구함
ViT의 경우에는 sequence 길이 s에서 `[CLS]` 는 빼고 $\sqrt{s-1} \times \sqrt{s-1}$ 이렇게 resize 한다음에 interpolate해서 구함 

### Result
- qualitative
<img width="689" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9648a00d-ea19-4f8c-912d-807184cd9bc6">


- pertubation
<img width="694" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e282d2f9-bfb8-4aad-866c-caa9ca95863d">

중요도가 높다고 한 애들을 masking하는 방식으로 해서 top-1 accuracy가 어떻게 바뀌는지 확인. positive는 중요한 애들을 점점 지워나가는 것(낮으면 좋음) 

- segmentation
<img width="679" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c882cd7a-85a3-4939-ad7a-87bc5b13b403">


- token-f1
<img width="405" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6f524055-8aa4-4bf7-9da2-b033934e1b03">

