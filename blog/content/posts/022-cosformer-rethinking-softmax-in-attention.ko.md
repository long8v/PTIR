---
title: "[21] cosFormer: Rethinking Softmax in Attention"
date: 2022-04-20
tags: ['NLP', 'attention', '2022Q1', 'ICLR', 'long']
paper: "https://arxiv.org/pdf/2202.08791.pdf"
issue: 22
issueUrl: "https://github.com/long8v/PTIR/issues/22"
---
<img width="1234" alt="image" src="https://user-images.githubusercontent.com/46675408/164129350-b160b6e7-1644-4f90-b8a5-637177039da3.png">

[paper](https://arxiv.org/pdf/2202.08791.pdf)

## Introduction
- vanilla Transformer에서 dot product + softmax를 하는 것은 long-range dependencies를 모델링하는데 필요하나, softmax 연산이 특히 sequence length가 길 때 너무 헤비하다. 
  - `Q` (batch_size, query_seq_len, hid_dim) * `transpose(K)` (batch_size, hid_dim, key_seq_len)을 구하면 (batch_size, query_seq_len, key_seq_len) 가 되고 이를 마지막 차원에 대해 softmax 취해서 attenion score를 구함. -> key_seq_len이 길어지면 softmax도 헤비해짐
- 이를 줄이기 위해, SparseTransformer, Random feature attention, ReFormer 등이 제시되었지만 (1) attention matrix에 대한 가정이 있고 (2) approximation을 하기 때문에 가정이 맞지 않거나 approximation error가 늘면 vanilla Transformer보다 성능이 좋지 않았다. 그리고 몇몇 방법론들은 LM을 하기 위한 causal attention에 적용할 수 없었다. 가령 Linformer나 BigBird는 cross attention을 하는데에만 사용할 수 있었다. 
<img width="826" alt="image" src="https://user-images.githubusercontent.com/46675408/164129294-74a48cec-5bee-42f5-a022-83325c66f53d.png">

- 이러한 배경에서 softmax의 주요한 속성들은 유지한 채 linear function으로 대체할 수 있을지 확인해보았다. 
  - (i) attention matrix는 non-negative
  - (ii) non-linear re-weighting scheme이 attention weight를 안정화하는 역할을 함
  - 가령 [linear transformer](https://arxiv.org/abs/2006.16236)의 경우 exponential linear unit을 통해 (i)를 달성했으나 re-weighting을 하지 않아서(?) Long-Range Arena에서 낮은 성적을 보였다.
  - **long-range arena** : [A Benchmark for Efficient Transformers](https://openreview.net/forum?id=qVyeW-grC2k)
- 우리는 위의 속성들을 만족하는 CosFormer를 제안한다. (i) attention score를 구하기 전에 feature map을 ReLU에 통과 시킴 (ii) cos re-weighting scheme을 사용하여 local correlation을 조금 더 확대하여 보도록 했다. 
- 이 어텐션은 linear form으로 정확하게 decompose 된다.
- Long-Range Arena에서 1등 했다.

## Our Method
CosFormer의 아이디어는 non-decomposable non-linear softmax연산을 decomposable non-linear re-weighting mechanism과 linear operation으로 대체하는 것이다. 
<img width="1235" alt="image" src="https://user-images.githubusercontent.com/46675408/164130473-14be81cf-9777-42b6-b815-4a1fcf02fc9e.png">

일반적인 트랜스포머는 O(L**2) 만큼 복잡도가 든다.
이때 주요한 점은 similarity function을 어느 것이나 선택할 수 있다는 점이다. S(Q, K)를 linear하게 하기 위해서 similarity function을 decomposible similarity function으로 만들 수 있다. -> exp(Q KT)가 아니라 \phi(Q)\phi(K)가 similarity가 되는 것
<img width="944" alt="image" src="https://user-images.githubusercontent.com/46675408/164132645-5a48027f-30e0-4f1b-a9b8-d8fe692987dc.png">

그 이후 우리는  matrix property를 통해 KV를 먼저 구해주면 linear complexity O(Nd^2)를 달성할 수 있다. 일반적으로 N >> d 이므로 O(N)으로 표현할 수있다.
![image](https://user-images.githubusercontent.com/46675408/164134693-15ecb53d-3d0c-4843-8c00-6e56df2e6223.png)

<img width="1150" alt="image" src="https://user-images.githubusercontent.com/46675408/164131888-d7f7ba8f-5c55-40b0-94d7-1ac458d4b5f8.png">

<img width="613" alt="image" src="https://user-images.githubusercontent.com/46675408/164140863-becc1ac8-81da-4b4a-b659-6ad89503d21d.png">
우리는 softmax의 특징을 (i) non-negative (ii) non-linear re-weighting으로 보았는데, 이를 확인하기 위해 similarity matrix를 구할 때 다양한 함수를 사용했다. non-negative의 성질 때문에 ReLU > LeakyReLU > Identity 였고, non-linear의 성질 때문에 softmax > ReLU였다.

CosFormer
1) linear projection kernel = ReLU, dot product를 했다. 
<img width="751" alt="image" src="https://user-images.githubusercontent.com/46675408/164141151-dff949af-023a-40d2-a1d0-1b70e01b4663.png">

negtive value를 제거하기 위해 kernel은 ReLU를 사용했다.
<img width="970" alt="image" src="https://user-images.githubusercontent.com/46675408/164141221-06356172-c56c-4887-9a84-2ecef3888f88.png">

similiarity function은 dot product를 row별로 했다.
<img width="1229" alt="image" src="https://user-images.githubusercontent.com/46675408/164141769-80023c75-58f2-4b60-99ad-62ded23a1e5d.png">

2) cos-Based Re-weighting Mechanism
softmax가 하는 non-linear re-weighting이 중요한데, attention weight의 분포에 집중하게 해주고 학습 과정을 안정화시킨다. 우리는 또한 이가 멀리 있는 connection에 대해 패널티를 주고 가까운 곳 대해선 enforce 해주는 효과를 볼 수 있었다. 
<img width="796" alt="image" src="https://user-images.githubusercontent.com/46675408/164142323-0beac77b-2bd5-406b-a665-2e01a4ed49b5.png">

이러한 cosine strategy는 완벽하게 decompose 가능하다 (수식 생략)
<img width="998" alt="image" src="https://user-images.githubusercontent.com/46675408/164142430-bc4f8039-4f7b-45e8-8d3b-8c7d7a229380.png">


## Result
<img width="889" alt="image" src="https://user-images.githubusercontent.com/46675408/164142850-8ab06fb9-8fd0-498c-b8d3-2c8656640cad.png">

<img width="802" alt="image" src="https://user-images.githubusercontent.com/46675408/164142727-b48d5f93-0a92-43a9-84b0-8864914e6f4c.png">


**papers**
- RFA
-  Transformers are rnns: Fast autoregressive transformers with linear attention
- performer
- One-vs-each approximation to softmax for scalable estimation of probabilities
- Stochastic Positional Encoding
- Rotary Position Embedding
