---
title: "[223] Transformers are RNNs:  Fast Autoregressive Transformers with Linear Attention"
date: 2026-04-01
tags: []
paper: "https://arxiv.org/pdf/2006.16236"
issue: 246
issueUrl: "https://github.com/long8v/PTIR/issues/246"
---
<img width="647" height="164" alt="Image" src="https://github.com/user-attachments/assets/7bd2f3ff-bd5b-470d-99b0-fc1adc9b8bb9" />

[paper](https://arxiv.org/pdf/2006.16236),  [blog](https://linear-transformers.com/), [code](https://github.com/idiap/fast-transformers)
## TL;DR
- I read this because.. : 4월은 linear transformer -- 첫번째 논문 
- task : autoregressive sequence modeling, language modeling, machine translation
- problem : self-attention이 모든 토큰 쌍을 비교해서 시간/메모리 O(N²), 긴 시퀀스에서 비효율적
- idea : softmax attention을 kernel 형태 $\phi(Q)\phi(K)^T$로 바꿔서 결합법칙으로 재배열, cumulative sum을 통해 개선 
- input/output : token -> token 
- architecture : softmax 대신 kernel with elu function으로 바꿈. 그 외 아키텍쳐 상 변경점은 없음 
- objective : CE loss 
- baseline : Transformer, RoFormer 
- data : WMT, language modeling benchmark 
- evaluation : BLEU (MT), perplexity (LM)
- result : 긴 시퀀스에서 큰 속도/메모리 개선, 성능은 약간 감소하거나 유사한 수준
- contribution : attention을 kernel로 재해석, O(N) linear attention 제안, transformer가 RNN처럼 동작함을 보임
- etc. : causal masking이 prefix sum 구조에 자연스럽게 포함됨, layerwise parallelism 가능

## Details
- conversation with chatGPT: [link](https://chatgpt.com/share/69cc5fbf-78d0-83a9-8ce0-27d5878abf8a)

### 3.1 Transformer 
<img width="400" height="138" alt="Image" src="https://github.com/user-attachments/assets/14065146-a0cb-4f96-bdc8-113bf1d5f406" />

- $f_l(.)$은 그냥 FFN
- $A_l(.)$ self-attnetion

<img width="400" height="223" alt="Image" src="https://github.com/user-attachments/assets/4bd06bf0-53cd-4099-a8b0-3f664fd07017" />

저기서 softmax term을 그냥 유사도 함수 $sim(\cdot)$로 표현할 수 있음

<img width="404" height="130" alt="Image" src="https://github.com/user-attachments/assets/4dee4aab-84f8-47f7-8df0-5aa1a4685f20" />

### 3.2. Linearized attention
여기가 갑자기 헷갈리는데, Kernel Trick이란 걸 쓸거임. 
attention에서 $sim(\cdot)$은 "non-negative"여야 한다는 제약 밖에 없음
그렇다면 모든 kernel 중에 , $k(x,y) : \mathbb{R}^{2 \times F} -> \mathbb{R}_{+}$ 를 포함할 수 있게 됨 

그런 "imaginery kernel"($k$)이 있다 치고, feature 표현 $\phi(x)$에 대해 eq (2)를 다시 쓰면

<img width="367" height="77" alt="Image" src="https://github.com/user-attachments/assets/92fd85bf-777a-440e-a17e-a56e6c4688d6" />

위에서 $\sum _j$는 j에 대한 값이기 때문에 $\phi(Q_i)^T$를 넘길 수 있고, 그러면 아래와 같이 식이 됨
<img width="412" height="212" alt="Image" src="https://github.com/user-attachments/assets/e8c1acfb-6c0c-4e83-b0fa-20dbe0a6e639" />

이 때 feature map $\phi(\cdot)$은 $Q$, $K$ 행렬에 row-wise로 연산됨
eq (6)의 괄호 안은 $\phi(X)^T\in \mathbb{R}^{D\times N}$, $\phi(X)^T\in \mathbb{R}^{N\times D}$ 이어서 $O(N)$의 시간, 공간 복잡도를 가지게 됨. (공간 복잡도와 시간 복잡도가 헷갈리네..) -- 
그 이유는 우리가 KV, K를 한번 저장하고 재사용할 것이기 때문.
<img width="407" height="62" alt="Image" src="https://github.com/user-attachments/assets/7efdd83c-83ba-4500-ba71-ea65faee9f50" />

### Feature maps and computational cost
Kernel을 어떤 것을 사용하냐에 따라 computational cost가 달라지기 때문에 elu 함수를 선택
<img width="384" height="45" alt="Image" src="https://github.com/user-attachments/assets/ca642be0-ad65-4637-a969-f66705b5c133" />

relu over elu를 사용한 것은 0 이하일 때도 gradient가 흘렀으면 좋겠어서

### 3.3 Causal Masking
Transformer의 Causal masking을 여기선 어떻게 구할 수 있냐
이것은 summation을 모든 j에 대해 하는게 아니라 $i$까지 하도록 바꾸면 됨 

(이전의 식)

<img width="509" height="110" alt="Image" src="https://github.com/user-attachments/assets/217a5bb1-5beb-4b3e-98c0-bb665f6a9996" />


(w/ causal masking)
<img width="429" height="475" alt="Image" src="https://github.com/user-attachments/assets/cf7e737b-1ea1-4a04-9a04-fbb02e9ba86f" />

우리는 $S_{i-1}$로 부터 $S_{i}$를 계산할 수 있음. 왜냐하면 누적합이기 때문에.
~(즉 transformer와 달리 시간 축 N 에 대해 병렬화 하지는 않음)~

#### 3.3.1 Gradient Computation
gradient를 나이브하게 구하면 또 $O(N^2)$ 복잡도가 되지만 잘 구해서 얘도 Linear하게 ㄱ함

<img width="423" height="317" alt="Image" src="https://github.com/user-attachments/assets/2fdcfcbb-ba51-4c02-94ae-723b2e493457" />

#### 3.3.2 Training and Inference
Transformer 대비 좋은 점은 Inference 시에 QK를 안가지고 있어도 되어서 메모리가 seq len에 비례하여 늘어나지 않음. 즉 train, inference의 좋은 점을 다 가져옴
<img width="654" height="467" alt="Image" src="https://github.com/user-attachments/assets/da071831-893e-4452-8fb4-f0cebe4002b2" />


### 3.4. Transformers are RNNs

<img width="428" height="287" alt="Image" src="https://github.com/user-attachments/assets/a5422cd6-7480-4748-96f2-c1c0d9c97e71" />

## Experiment 
스킵 ㅎ

