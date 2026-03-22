---
title: "[150] Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization"
date: 2024-02-13
tags: ['2016', '25min', 'XAI']
paper: "https://arxiv.org/pdf/1610.02391.pdf"
issue: 162
issueUrl: "https://github.com/long8v/PTIR/issues/162"
---
<img width="698" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9640ec2a-b398-4d05-a803-1b6bc84a2eca">

[paper](https://arxiv.org/pdf/1610.02391.pdf)

## TL;DR
- **I read this because.. :** explanation 하면 알아야되지 않을까 하고 읽음 
- **task :** explainability in CNN
- **problem :** 모든 종류의 CNN에 적용가능한 interpretable한 모듈을 붙여보자
- **idea :** convolution의 activation map $A^k$을 우리가 시각화하고 싶은 클래스 $y^c$에 대해 미분하고 GAP를 해서 importance를 구한뒤 이걸 $A^k$에 weighted sum + ReLU해서 구한다.
- **input/output :** {image, class or caption or answer} -> activation map
- **architecture :** VGG-16, AlexNet, GoogleNet
- **objective :** X
- **baseline :** CAM, Guided-BackProp, c-MWP
- **data :** ILSVRC-15, PASCAL VOC 2007 
- **evaluation :** wsss, human evaluation, pointing game
- **result :** 성능 저하 없이(CAM은 성능이 저하됨) 훌륭한 설명력. wsss에서 좋은 seed. adversarial sample도 시각화 잘함. 사람 불러서 activate된 애 보고 class 분류하라고 함(trustworthy), Guided-backprop 또는 Deconv랑 사람한테 뭐가 더 낫냐고 물어봄
- **contribution :** 간단한 아이디어로 성능 저하 없는 de-facto method
- **etc. :** negative gradient를 안보는 관습은 여기서 나왔나 보당. guided backprop이랑 Network Dissection 읽어보장. "counterfactual explanation"이란 용어 줍줍

## Details
### proposed
<img width="691" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2e5b15ba-72c9-4539-a67c-a9bf6f01f1de">

우리가 시각화하고 싶은 class c에 대한 logit (softmax 이전) $y^c$를 activation feature map $A_{ij}$에 대해 미분함.
이를 width, height (i, j)에 대해 Global Average Pooling 해서 importance를 구함.
<img width="263" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6d4c4e7a-f854-4557-b180-79f0ddf19571">

이걸 activation map과 다시 weighted sum한 뒤에 ReLU를 취하면 GradCAM
<img width="258" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ca8c4e19-7c43-4204-9f9c-1499df0604fb">

이때 마지막 레이어의 conv feature map (14 x 14 size)를 사용 (이전 레이어 쓰면 성능이 별로 좋지 않음)
여기서 ReLU를 적용한 이유는 negative하게 영향을 주는 pixel은 다른 카테고리에 해당하는 것일테니 그럼. 
ReLU를 적용안하니까 원하는 class $y^c$가 아닌 다른 클래스가 활성화될때가 있었고 localization 성능이 떨어짐. 

- guided grad-cam
14 x 14 feature map이 대충 여길 보고 있다고는 알 수 있는데 구체적으로 이게 왜 "tiger cat"인지에 대한 finegrained한 설명은 못함
그래서 guided backpropagation(Striving for Simplicity: The All Convolutional Net, https://arxiv.org/abs/1412.6806)라는 걸 사용해서 같이 곱해서 시각화 해줌. Deconv를 쓸 수 있는데 실험적으로 guided backprop이 더 좋았다고 함.
Guided backprop에 대해 "negative gradients are supressed"라고 써져있는데 무슨 내용인지 읽어보자 

- counterfactual explanation
<img width="229" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/95e59f8e-1fa5-4448-944c-2554aa3b2e1f">

<img width="341" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/728a6d0c-9497-441f-9622-1114f5610713">

단순히 gradient에 negative를 구해준 뒤 ReLU를 취하면(negative activation만 남을테니) counterfactual explanation이 됨. 이 픽셀이 이 클래스가 왜 아닌지에 대한 설명!

### Result
- classification result  
<img width="359" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/79729cf1-7dff-4baa-ba64-2a01729ce126">


- result on captioning model
<img width="709" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b807afa7-ac8f-415f-9b57-27386e842b78">


- textual explanation on neuron
<img width="705" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/293b3d43-4c0a-4007-bbbc-bf000c2d3ee2">

Network Dissection: Quantifying Interpretability of Deep Visual Representations https://arxiv.org/abs/1704.05796 이거 읽어보장

- result with adversarial noise
<img width="344" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ff46e451-1f66-45d1-b498-90a1c046190b">

이미지에 살짝 perturbationd을 취하면 airliner 0.9999로 예측하는 예시. 근데 이렇게 해도 GradCAM은 잘된다.
