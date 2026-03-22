---
title: "[25] Intriguing Properties of Vision Transformers"
date: 2022-04-29
tags: ['ViT', 'WIP', '2020Q2', 'NeurIPS']
paper: "https://openreview.net/pdf?id=o2mbl-Hmfgd"
issue: 27
issueUrl: "https://github.com/long8v/PTIR/issues/27"
---
![image](https://user-images.githubusercontent.com/46675408/165873455-776c815a-3658-455f-a294-9518c922ad74.png)

[paper](https://openreview.net/pdf?id=o2mbl-Hmfgd), [code](https://github.com/Muzammal-Naseer/Intriguing-Properties-of-Vision-Transformers)

# Abstract 
ViT의 multi-head self-attention은 이미지 패치들의 시퀀스들을 유연하게 참조한다. 중요한 점은 그러 유연함이 자연이미지에서의 nuisances(방해물)을 어떻게 잘 이용하냐이다. 우리는 다양한 실험들을 통해 CNN과 비교하여 ViT류들이 어떤 특성을 가지고 있는지 실험해보았다. 
(a) 트랜스포머는 심한 occlusion, perturbation, domain shift에 강하다. 가령 이미지의 80%를 occlusion으로 제거해도 60%의 top-1 accuracy를 달성했다. 
<img width="953" alt="image" src="https://user-images.githubusercontent.com/46675408/165876514-1aeb93c1-a708-49cd-811b-9e68bfb4b1ed.png">

(b) (a)는 texture bias때문이 아니고, ViT가 local texture에 덜 bias 되었기 때문이라고 보았다. shape-based feature를 encode하도록 잘 학습하면, 이전 연구에서 밝혀지지 않았지만 인간의 능력과 유사한 정도의 shape recognition 능력이 있었다. 
(c) ViT를 shape 표현을 encode하게 사용하면, pixel-level의 supervision 없이도 정확한 semantic segmentation을 할 수 있었다.
(d) 하나의 ViT모델에서 Off-the-shelf 피쳐를 사용하는 것은 다른 피쳐 앙상블을 만드는데 사용될 수 있었고, 더 높은 정확도를 달성했다.  
우리는 ViT의 유연하고 다이나믹한 receptive field가 ViT의 효과적인 feature임을 밝혔다.

# Intriguing Properties of Vision Transformer
## Are Vision Transformer Robust to Occlusions
###  Occlusion Modeling :
이미지 x가 주어지고 label y가 들어오면 이미지 x는 N개의 patch sequence로 표현된다. 우리는 이 N개중에 M개의 이미지 패치를 골라서 0으로 바꾸어 x'를 만드는 방법(논문에서 PatchDrop로 부름)을 선택했다. 이 PatchDrop을 아래 세개의 종류로 적용을 했다.
<img width="641" alt="image" src="https://user-images.githubusercontent.com/46675408/165878346-fa90971b-7a0f-4cf1-b5cd-f705d04de0ca.png">

### Robust Performance of Transformer Against Occlusions
- 학습은 ImageNet으로 분류 문제를 풀었고, validation set의 정확도로 평가했다. 
- Information Loss : 전체 패치중 드랍된 패치의 비율을 IL로 정의 (= M / N)
- 아래 그래프를 보면 CNN보다 ViT가 훨씬 강건하다. 
<img width="1089" alt="image" src="https://user-images.githubusercontent.com/46675408/165879176-9a3e22d7-d9a0-4d0b-99c2-c82dc8e3fcea.png">

### ViT Representations are Robust against Information Loss
occlusion에 대한 모델의 반응을 더 잘 파악하기 위하여, 다른 레이어의 각 헤드들의 어텐션을 시각화해보았다. 초반의 레이어에서는 모든 영역을 attend하지만 깊어질 수록 이미지에서 occlude되지 않은 영역에 집중하는 것을 볼 수 있었다. 
<img width="1056" alt="image" src="https://user-images.githubusercontent.com/46675408/165879704-9f2c6a30-449a-4a5a-b65c-5224129f6487.png">

위에서 말한 레이어가 깊어질 때 달라지는 변화에 대해 token invariance가 있는지 확인 해보고자 한다.
우리는 원래 이미지와 occlude된 이미지에 대해 feature(또는 token)간의 correlation coefficient를 계산하였다. ResNet50의 경우에, logit 레이어 전의 feature를 사용했고, ViT의 경우 마지막 transformer block의 class 토큰을 가져왔다. ResNet에 비해 ViT의 class token은 더 강건했다.(=correlation이 높았다) 이러한 성향은 비교적 작은 object를 가진 다른 데이터셋에서도 동일했다. 
<img width="1091" alt="image" src="https://user-images.githubusercontent.com/46675408/165880840-607846ad-3c59-4af7-9614-67591c185caf.png">

## Shape vs Texture: Can Transformer Model Both Characteristic?

## Does Positional Encoding preserve the global image context? 