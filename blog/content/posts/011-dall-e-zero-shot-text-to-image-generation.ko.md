---
title: "[11] DALL-E : Zero-Shot Text-to-Image Generation"
date: 2022-02-07
tags: ['multimodal', '2021Q1', 'zero-shot', 'openAI']
paper: "https://arxiv.org/pdf/2102.12092.pdf"
issue: 11
issueUrl: "https://github.com/long8v/PTIR/issues/11"
---
![image](https://user-images.githubusercontent.com/46675408/154877540-b65707d5-3324-430b-bf8e-e51fbe4962ce.png)
[paper](https://arxiv.org/pdf/2102.12092.pdf), [article](https://openai.com/blog/dall-e/), [code](https://github.com/openai/dall-e)

## TL;DR
- **task :** zero-shot text-to-image generation
- **problem :** generation 모델들은 모델 사이즈가 커지는데 text-to-image는 데이터가 한정적임 
- **idea :** 인터넷 크롤링으로 겁나 큰 text-image pair(MS-COCO)를 만들고 모델 사이즈도 키우자. 효율적으로 이미지를 인코딩하기 위해 discreteVAE를 사용하자.
- **architecture :** discreteVAE으로 이미지를 코드로 인코딩 + 텍스트 인코딩해서 auto-regressive 하게 
- **objective :** cross-entropy loss
- **baseline :** AttnGAN, DM-GAN, DF-GAN
- **data :** 3.3M MS-COCO
- **result :** [FID](https://wandb.ai/wandb_fc/korean/reports/-Frechet-Inception-distance-FID-GANs---Vmlldzo0MzQ3Mzc)(=Frechet Inception Distance)에서 SOTA. human evaluation에서도 DF-GAN보다 압도적 우위.
- **contribution :** 엄청 큰 이미지 생성모델. 

## Details
- 120억 파라미터, 데이터셋은 2억 5천만 text-image pair 데이터
### Method
- 이미지 픽셀 단위로 학습을 하면 1) 연산이 너무 늘고 2) likelihood를  적용했을 때, short-range 관계에만 집중해 high-frequency detail만 모델링하고, 인간이 식별 가능한 low-frequency를 모델링하지 못한다 
- 이를 해결하기 위해 두단계로 나누었다.
  - 첫번째 단계에서는 discrete VAE(dVAE)를 사용하여 256 x 256 RGB 이미지를 32 x 32 이미지 토큰이 있는 그리드로 나누고, 각각의 요소들이 8192개의 값을 가질 수 있게 한다. 이는 트랜스포머의 이미지 퀄리티의 큰 저하 없이 context size를 192배 줄였다.
    - dVAE로 압축한 뒤 reconstruct한 결과
![image](https://user-images.githubusercontent.com/46675408/152714226-be3a3a23-7377-4515-bef6-d305e0f62982.png)
  - 두번째 단계에서는 256개의 BPE-encoded text를 32 x 32 = 1024 이미지 토큰과 concat하여 텍스트와 이미지를 autoregressive하게 학습하였다.
  - 이러한 전체적인 단계는 이미지 x와 캡션 y, dVAE로 encode된 token z간 joint probability의 evidence lower bound(ELB)를 최대화하는 것으로 볼 수 있다. 
<img width="349" alt="image" src="https://user-images.githubusercontent.com/46675408/162875434-0a95508e-eabf-4579-bc6c-5e3f5f691a1d.png">
 
 - 즉, 위와 같이 factorization을 할 수 있고 이 값의 ELB값을 구하면 아래와 같다. 
<img width="514" alt="image" src="https://user-images.githubusercontent.com/46675408/162875698-fcb01cdd-8ca8-42f9-9431-b79fc1ea7f01.png">
<img width="476" alt="image" src="https://user-images.githubusercontent.com/46675408/162875921-895b7f8b-3910-43a6-8cb0-684dda028027.png">

- 식을 해석하면, `dVAE에서 캡션과 이미지 토큰이 주어졌을 때 이미지의 likelihood`를 최대화하면서, `dVAE에서 이미지가 주어졌을 때 나오는 캡션 텍스트와 이미지 토큰의 확률분포`와 `트랜스포머를 통해 나오는 캡션과 이미지 토큰의 joint 확률` 사이의 KL divergence를 최소화해야 한다.
- 이때 beta는 1이어야 이론적인 ELB이지만 실험 결과 크게 할 때 성능이 좋았다. 

#### Step One: Learning the Visual Codebook
$\phi$와 $\theta$에 대해 ELB를 최대화하는 식으로 dVAE를 학습한다.
code의 크기는 32 x 32이며 $K$=8192고 $p_\psi$는 uniform분포이다.
code가 discrete 해서 미분 불가한 부분은 gumbel softmax를 사용해서 gradient를 흘려줬다.

$p\theta$는 log-laplace(정규 분포 지수 부분에 제곱대신 절대값) 분포로 평가됐다.

#### Stage Two: Learning the Prior
텍스트는 BPE encode해서 최대 256길이로 만들었고, 이미지는 dVAE encoder logit에서 argmax해서 1024개의 토큰을 얻었다. 
두개의 인코딩을 concat해서 트랜스포머 디코더에 넣어줬고, 텍스트가 256보다 작을 경우에는 256개의 position에 따라 각각의 `[PAD]`토큰을 학습시켜줬다. -> OOD catpion에 더 강건했다.
cross-entropy loss를 사용했고 텍스트와 이미지의 loss는 1/8, 7/8로 곱해줬다. 