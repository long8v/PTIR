---
title: "[153] Contrastive Explanations for Model Interpretability"
date: 2024-04-01
tags: ['2021Q1', 'XAI', 'emnlp', 'AI2']
paper: "https://arxiv.org/abs/2103.01378"
issue: 168
issueUrl: "https://github.com/long8v/PTIR/issues/168"
---
<img width="676" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8b65eb8c-0135-4943-abfa-e3e675d537c8">

[paper](https://arxiv.org/abs/2103.01378)

## TL;DR
- **I read this because.. :** 개인 연구 관련. Claude AI가 추천해줌 
- **task :** contrastive explanation. A 대비해서 B를 선택한 이유가 무엇인지 설명 
- **problem :** 모델이 설명 가능했으면 좋겠는데, 그 설명을 모두 열거할 수는 없고 A over B인 이유를 설명하면 간단해짐. 
- **idea :** 최종 모델 class y를 예측할 때 쓰이는 weight W의 row에 대해서 뺀 다음에 이걸 projection 해서 hidden 이랑 곱해줌. 이렇게 곱해준 값을 text span을 masking해서 forward를 여러번 한 다음에 그 값들을 비교해서 가장 변화가 큰 값을 highlight함. 
- **input/output :** text - > class // text span highlighted for why model predicts class y over y'
- **architecture :** RoBERTa
- **objective :** MLM
- **baseline :** - 
- **data :** NLI, BIOS(biography를 받고 직업을 분류하는 task)
- **evaluation :** 이해를 잘 못함. 
- **result :** 이해를 잘 못함. 정성적으로만 평가한듯?
- **contribution :** contrastive explanation이라는 영역의 거의 선구 work인 듯.
- **etc. :**

## Details
<img width="338" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/052e273b-3429-4ed5-a6da-7f001fa357d8">

<img width="316" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/27ad5244-d285-4335-bfe3-5a48067bc662">

### method

일단 masking하고 모델 forward 를 여러번 할 것임. 이런 방법을 여기서는 amnesic 방법론이라고 부름.

- K : model class
- y : output class 
- enc : neural encoder
- $W \in \mathbb{R}^{K \times d}$ : final linear layer
- $y^*$ : model prediction (fact) / $y'$ : alternative prediction
- $p$ : model probabilities
- $w_{y^*}$, $w_{y'}$ : weight matrix W에서 두 클래스를 예측데 쓰인 row.

$w_{y^*}$, $w_{y'}$ 이 두개의 weight row를 하나의 contrastive direction $u$로 만듦. 
<img width="110" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ef30ed52-f8b7-4f66-a64e-028822b870bc">


만약에 모델이 $y^*$를 더 높게 예측한다면 $u^T*h_x>0$ 일 것임.

<img width="233" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a501f136-4fc9-423b-a464-e395988b9a89">

이 u를 사용하여 hidden state $h_x$에 대한 projection을 만듦.
이 C연산의 결과값은 $h_x$에서 contrastive intervention로 해석될 수 있는 행렬이 됨. 
이후 이전과 같이 $q = \text{softmax}(Wh_x)$와 같은 연산을 한 뒤 아래와 같은 방식으로 text span의 계수를 구함.

<img width="244" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d82db45f-e17d-4c6c-be6c-4b752ae5a836">

이때 p는 projection을 안한 값의 model prediction이고 q는 한 값. 

## result
<img width="325" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/71f8da7c-9409-4f4c-8c1d-165ee87e1112">

결과 해석이 잘 안됨 ..

