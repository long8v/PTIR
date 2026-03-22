---
title: "[147] Generic Attention-model Explainability for Interpreting Bi-Modal and Encoder-Decoder Transformers"
date: 2024-02-07
tags: ['ICCV', '2021Q1', 'XAI']
paper: "https://arxiv.org/pdf/2103.15679.pdf"
issue: 159
issueUrl: "https://github.com/long8v/PTIR/issues/159"
---
<img width="800" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4e361620-0bf8-4a65-a970-ce13930e5619">

[paper](https://arxiv.org/pdf/2103.15679.pdf), [code](https://github.com/hila-chefer/Transformer-MM-Explainability)

## TL;DR
- **I read this because.. :** aka. CheferCAM. explainable CLIP score에 관심있어서. 이 논문 레포에서 [colab](https://github.com/hila-chefer/Transformer-MM-Explainability?tab=readme-ov-file)을 공개했는데 토큰별 visualize 결과를 볼 수 있음. 
- **task :** explainability in neural network
- **problem :** 전작 TiBA(https://github.com/long8v/PTIR/issues/158) 에서 self-attention 만 말고 multi-modal 환경의 co-attention, enocder-decoder 구조도 하고 싶다
- **idea :** 이전의 ouput에 대한 gradient(==LRP)가 아니라 attention map에 대한 gradient를 쓰자 
- **input/output :** model // heatmap for text or vision tokens
- **architecture :** ViT, VisualBERT, LXMERT, DETR
- **baseline :** rollout, raw attention, Grad-CAM, Partial LRP, TiBA
- **evaluation :** perturbation(both in image and text token for VisualBERT), weakly, semantic segmentation 
- **result :** 전작 대비 나은 성능
- **contribution :** cross-attention, co-attention 도 explainable하게 한 work. ICCV oral 임
- **etc. :** 앞에 deep taylor decomposition이다 뭐다 피곤했는데 그거 무시하고 이 논문만 읽으면 이론적인 내용도 필요 없고 깔끔한듯.. 그리고 성능이 좋음. 대신 반대로 이론적인 내용이 없어서 좀 주먹구구 느낌. CLIP의 경우 최종 output이 embedding일텐데 그럼 CLIPscore에 대한 시각화는 아닌 것 같기도 함..? colab 자세히 봐야할듯.  

## Details
### some notation
- i는 이미지 토큰
- t는 텍스트 토큰 
- $A^{tt}$는 text끼리의 self-attenion / $A^{ii}$는 image끼리의 self-attenion
- $A^{ti}$는 multi-modal attention interaction

### Relevancy initialization 
relevancy map을 초기화 / 업데이트 할 거임
<img width="204" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/259fbe15-c283-4b4b-b2f4-ea05ac3de234">

SA 전에는 서로 상호작용이 없어서 $R^{ii}$, $R^{tt}$는 identity. $R^{it}$는 zero tensor.

### Relevancy update rules 
attention map A를 가지고 relavancy를 update할 것임
전작에 따라 head 간 평균을 구하고 gradient를 사용 

<img width="191" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/15a4432f-5b48-48b0-a2f0-6e22090b0ced">

여기서 $\delta A$는 우리가 시각화하고 싶은 class t에 대한 output인 $y_t$를 A로 미분한 것. 평균을 취하기 전에 positive만 남겨줌(clamp)(이에 대한 이유는 딱히 없고 전작을 따라줌)
<img width="84" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/abbf39c8-a96e-4630-a0d5-15b00b83395f"> 

<img width="394" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/abbf6034-e02c-4f9a-9c90-a9bee83b37c1">

self attention에 대한 relevance 업데이트 방식은 아래와 같음 
여기서 s는 query token, q는 key token임.

여기서 $R^{xx}$는 두개로 분리할 수 있는데 처음에 초기화한 $I$랑 $I$를 뺀 residual인 $\hat{R}^{xx}$임. 
$\hat{R}^{xx}$는 gradient를 사용하기 때문에 숫자가 절대적으로 작음. 이를 해결하기 위해 row의 합이 1이 되도록 정규화 해줌.
<img width="243" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/90485988-dfe2-4213-888b-aa4308f4be17">

co-attention / cross-attention의 경우 update rule을 아래와 같이 정의해줌
<img width="265" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/eeb97b96-f622-47e0-9e39-4b9f031e7390">

### Obtaining classification relevancies
[CLS] 토큰의 row에 해당하는 relevancy map을 보면 되는데 text 에 대한걸 보려면 $R^{tt}$의 첫번째 row를 보면 되고 image에 대한걸 보려면 $R^{ti}$의 첫번째 row를 보면 됨 

### Adaptation to attention type
<img width="832" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3212fb8c-49f1-4323-b36e-6f4a1f5c1663">


- 두 modality의 토큰이 concat되어 SA에 들어가는 경우: 전체 $R^{(i+t, i+t)}$에서 [cls] token에 해당하는 row($R^{i+t}$)의 Relevancy map으로 만들  수 있음.
- 두 modality가 각각 SA 먼저 하고 서로 CA로 정보교환하는 경우(co-attention): 위에서 설명한 propagation을 다 해야 함. 이후 relavancy map은 분류 모델의 relevancy를 보는 것과 같은 방식으로 보면 됨 
- encoder-decoder구조: cross-attention이 한 방향으로만 이루어지므로 equation 11은 안해도 됨 

## Result
<img width="985" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/07e3b379-abdc-46a0-82b1-422cc600dcaa">

<img width="860" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1fc2e554-0807-4c48-a29b-8e479280c96d">
<img width="862" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/217c53f0-808f-438d-ad84-cc6887cc8ba4">
<img width="839" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/11211d48-c74b-47d2-9888-08656f8e1cb9">
<img width="838" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e6d338ae-adbf-4cc5-a2ce-52dc981913be">
