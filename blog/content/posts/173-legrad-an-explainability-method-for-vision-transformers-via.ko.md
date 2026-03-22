---
title: "[157] LeGrad: An Explainability Method for Vision Transformers via Feature Formation Sensitivity"
date: 2024-05-06
tags: ['CLIP', 'XAI', '2024Q2']
paper: "https://arxiv.org/pdf/2404.03214"
issue: 173
issueUrl: "https://github.com/long8v/PTIR/issues/173"
---

<img width="456" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4a1d0df5-c763-4096-b497-413d3b1c21dd">

[paper](https://arxiv.org/pdf/2404.03214), [code](https://github.com/WalBouss/LeGrad)

## TL;DR
- **I read this because.. :** Chefer를 scholar에서 follow 하니까 메일을 보내줌 (되게 편하네!)
- **task :** explainability in CLIP
- **problem :** CLIP 모델에서의 설명력
- **idea :** 모든 레이어의 hidden representation에 대해 미분을 구해서 
- **input/output :** {image, text} -> layer explainability maps
- **architecture :** CLIP ViT-B/16, -L/14, -H/14, -BigG/14, SigLIP
- **baseline :** LRP, Partial-LRP, rollout, Raw attention, GradCAM, CheferCAM, TextSpan
- **data :** ImageNet-S, OpenImage V7, ImageNet(perturbation)
- **evaluation :** segmentation (pixel acc, mIoU, mAP), ov segmentation(p-mIoU), perturbation test(neg, pos accuracy)
- **result :** SOTA.
- **contribution :** 모든 레이어를 잘 사용한 모델. 모델 스케일 레이어별로 모델 양상이 다른걸 보임.
- **etc. :** 대충 읽어서 그런가? sensitivity가 제목에 왜 들어간질 모르겠네

## Details
<img width="659" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/08a3d3a2-4f62-49fc-aded-962d968318e2">

### Methodology 
ViT의 최종 output을 아래와 같이 표현 
<img width="146" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c9fcb65a-bb2f-4d4c-b42b-a2e7c5b58d2d">

여기서 $\bar{z}$은 pooled representaion (cls pool, attention pool) 
이 중 우리의 target class $c$에 대한 activation을 $s$라고 함. 
이에 대한 attention map을 $A$라고 할 때 attention map에 대하여 미분하여 아래와 같은 map을 만듦
<img width="286" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b28b3aaf-40a5-4f03-b28d-a75a2fa46835">

ReLU를 취하고 layer / head / patch(n) 별로 평균을 구함.
<img width="408" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/88c7caee-97a5-4e1c-9717-91b7ca301013">
 
cls 토큰을 제외하고 다시 reshape을 하고 min-max normalization을 해줌
<img width="367" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8915f440-0a78-4bf0-b983-a6f83213d6de">

이런 식으로 모든 레이어의 $s^{l}$를 구하고 이에 대한 미분으로 map을 만들어줌 
<img width="500" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c321b21c-e4d3-43bf-ae8b-3b7f2f63b82f">

<img width="432" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/584944f6-ce6e-4050-a3e9-b762116dfa9d">

이걸 레이어별로 matrix multiplication이 아니라 summation을 해줌 
<img width="326" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/734b8cdc-6e88-47b4-8cd3-2a0cc50cd35e">

Chefer 21과 뭐가 다른가? https://github.com/long8v/PTIR/issues/159#issuecomment-1933470637
- 최종 Output에 대해 미분하는게 아니라 그 레이어의 representation과 내적을 한 뒤 미분을 함! (가장 메이저한)
- image_relevance = R[:, 0, 1:] : 이 친구는 CLS 토큰을 오히려 마지막에 지우는데, chefer는 CLS 토큰에 대한 표현을 사용함. $n \times n$에서 LeGrad는 마지막 모든 row에 대해 summation을 해서 쓰고, Chefer는 CLS에 걸린 걸 씀
- chefer는 residual connection을 표현하기 위해 identity matrix로 초기화해주는 부분이 있는데 그런거 없음 


### Result 
<img width="501" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8dc2afef-c520-46f1-83ed-381678b10b23">

#### Perturbation result 
<img width="488" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/982ff1e2-9e27-4907-b94f-64ae8501c9c8">

### Layer Ablation
<img width="578" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1d35783a-5137-4366-bfc9-5feb8d3a2c1b">

작은 모델의 경우 마지막 소수의 레이어만 쓰는게 좋았는데 모델 규모가 커질 수록 더 많은 레이어를 사용해야 함

<img width="595" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5bd8d595-b174-43b8-9f4c-90410b9fea70">

#### ReLU ablation
<img width="758" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a14eafbb-7cfa-4d0d-a222-4c4b0b48cfdc">

ReLU를 키는게 좋았음. 안킨다고 엄청 나빠지진 않음.

#### Qualitative 
<img width="652" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/cde7599a-aef0-433b-983b-e3ab537ca989">

