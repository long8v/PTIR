---
title: "[14] Longformer: The Long-Document Transformer"
date: 2022-02-22
tags: ['NLP', 'AllenAI', '2020Q1', 'long']
paper: "https://arxiv.org/pdf/2004.05150.pdf"
issue: 14
issueUrl: "https://github.com/long8v/PTIR/issues/14"
---
<img width="476" alt="image" src="https://user-images.githubusercontent.com/46675408/155048272-139cfd7f-a3e4-4319-9eb4-44b0e73b5d77.png">

[paper](https://arxiv.org/pdf/2004.05150.pdf), [code](https://github.com/allenai/longformer)
**problem :** 트랜스포머는 문장의 길이에 quadratic하게 복잡도가 늘어난다.
**solution :**  sliding window(+dilated)로 attention을 구하고 이를 stack을 쌓는다. 특정 태스크에 맞는 위치의 token들에 대해 global attention을 추가한다. 
**result :** text8, enwik8에서 SOTA, 긴 문서 task인 WikiHop이나 TriviaQA에서 RoBERTa보다 성능이 좋으며 SOTA . 인코더 디코더 모델은 arXiv 요약 데이터셋에서 효과적임을 확인.
**details :**
- windowed local-context self-attention은 문맥적인 표현을 학습하기 위해 사용되고, global attention은 예측을 위해 전체 시퀀스의 표현을 만드는데 사용된다.
- auto-regressive 태스크로 평가했을 뿐 아니라, MLM 같은 objective로 학습하고 SOTA임을 확인했다.
- encoder-decoder 모델인 LED 모델도 제안한다. 
- long-document transformers 접근론으로 1) left-to-right 접근법이 있는데, 왼쪽에서 오른쪽으로 움직이면서 chunk로 학습하는 것. 이건 다른 태스크에 적용할때 성능이 불안정함. 2) sparse attention을 하는 접근법이 있는데, Sparse Transformer가 대표적.  
<img width="1101" alt="image" src="https://user-images.githubusercontent.com/46675408/155049664-090c68e4-6546-441c-98ce-eded06d8ac5f.png">

- 긴 문장을 다루는 대표적인 방법은 문서를 최대 토큰 개수인 512로 자르거나, 자른 뒤 결합하는 방법이 있다. 또는 multihop이나 open QA에서 사용되는 방법인데, 먼저 관련있는 문서를 retrieve하고 그 뒤에 answer extraction을 위해 전달하는 방법이다. 
- Attention Pattern 
  - Sliding Window : local context가 중요하기 때문에 고정된 크기의 window attention을 사용하고, 이를 stack하여 (마치 CNN처럼) 더 큰 receptive field에서 볼 수 있게 한다. 전체 모델의 receptive field는 window size(=w) * # of layers(=l)가 되게 된다.
  - Dilated Sliding Window : 계산의 증가 없이 더 receptive field를 늘리기 위해서, (마치 [dilated CNN](https://zzsza.github.io/data/2018/02/23/introduction-convolution/)처럼) sliding window가 dilated 될 수 있다. dilated를 통해 모델의 receptive field는 w * l * d 가 되게 된다. multi-head attention에서 각 head별로 dilated size d를 다르게 하는게 성능에 효과적임을 확인했다.
  - Global Attention : task에 따라 어떤 input이 들어가야 최적인지가 다른데 (분류에선 `[CLS]` 토큰, QA에서는 question + docuemnt concat한 형태 등) 위의 어텐션들이 다양한 task에 알맞는 표현이 아니기 때문에 특정 태스크에 맞는 위치에 있는 token들에 대해 global attention을 추가하였다. 
  - Linear Projecton for Global Attention : sliding window의 linear projection과 global attention의 linear projection을 다르게 가져가는 것이 성능 향상에 도움이 되었다. global projection은 sliding window의 projection으로 초기화 되었다.
 