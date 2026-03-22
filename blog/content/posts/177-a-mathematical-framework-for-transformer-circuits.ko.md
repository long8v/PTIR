---
title: "[158] A Mathematical Framework for Transformer Circuits"
date: 2024-05-09
tags: ['2021Q4', 'XAI', 'anthropic']
paper: "https://transformer-circuits.pub/2021/framework/index.html"
issue: 177
issueUrl: "https://github.com/long8v/PTIR/issues/177"
---

<img width="600" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/14eb104a-0764-4c1b-9c51-7cc1e3407dec">

[paper](https://transformer-circuits.pub/2021/framework/index.html)

## TL;DR
- **I read this because.. :** TextSpan(https://github.com/long8v/PTIR/issues/172) 에서 이 논문에서 이용한 OV circuit을 썼다고 하고 mean ablation에서 사용된 것 같은데 내용이 이해가 안돼서 읽음. 
- **problem :** Transformer의 동작 방식을 circuit을 나눠서 생각해보자. 

## Details
### Related Work
"circuit"이란 단어가 뭔가 하고 봤는데 비슷한 저자들이 낸 https://distill.pub/2020/circuits/zoom-in/ 이 논문이 시작이었음.
뉴럴네트워크 내부에서 feature들이 어떻게 연결되어 있는지 sub-graph를 분석하는거라고 함. 음.. 자세히 읽어봐야 알겠지만 분리할 수 있는건 분리하는  방식인 듯 하다.
여기서 시각화는 어떻게 하는건지 궁금했는데 활성화된 layer에 대해서 https://en.wikipedia.org/wiki/DeepDream ([code](https://github.com/google/deepdream/blob/master/dream.ipynb))이란 방법론을 사용한다고 함. 옛날부터 저 LSD 스러운 그림 어떻게 그리는가 궁금했는데 이렇게 오래된 논문이었다니..

### High-Level Architecture
<img width="1019" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/316e9a3c-d3df-4465-9643-27ce9bf60653">

transformer는 대충 보면 이렇게 생겼다
1) token embedding
2) residual stream에 각 head 연산 $h(x_i)$를 더해주는 부분 
3) residual stream에 mlp를 취하고 이를 다시 residual stream에 더해주는 부분
4) word unembedding (=> logit 예측)

여기서 "residual stream"을 분석하기를 channel 간 커뮤니케이션을 하는 곳이라고 분석한다.
<img width="148" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e079bed2-b1b3-4a9a-ac83-ab7b945c4bb6">

residual로 연결되는 부분이 있으니까 각 레이어의 hidden 끼리는 서로 사용 가능하다
<img width="857" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1052130c-44fd-4be4-b555-542b6e48e18b">

<img width="819" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6a8fc506-bbe3-475c-8c1a-f639db175029">


### Attention Heads are independent and additive 
<img width="586" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/eecedcfc-cb49-49b7-b239-24f59d1c0e8e">

요건 그냥 행렬 연산인데 각 head 별로 concat하고 $W_o$를 하는 식으로 되어있지만 실제로 이건 각 head별로 $W_o^{h_i}$를 곱한다음 summation 하는 것과 동치이다. 즉 각 head 별로 residual stream에 정보를 넣었다 뺐다 한다고 볼 수 있다.
 
### Attention Heads as Information Movement
이때 residual stream에서 정보를 읽는 것과 쓰는 것이 완전 분리될 수 있다. 이를 보기 위해 attention 연산을 조금 다르게 써보자.
1. 각 토큰들이 residual stream으로 부터 봅혀져 value vector를 계산한다 $v_i=W_Vx_i$
2. attention score $A_i$를 받고 linear combination 하여 result vector를 구한다 $r_i=\sum_j A_{i,j} v_j$
3. 각 head별로 output vector를 구한다 $h(x)_i=W_Or_i

각 step은 matrix multiply로 적을 수 있는데, 왜 하나의 matrix로 합치지 않냐면, $x$는 (seq_len, head_dim)의 2차원 텐서인데, $W_v$, $W_o$를 곱하는건 head_dim 차원에서 일어나고 $A$를 곱하는건 seq_len 에서 일어나기 때문이다.
위의 연산을 [Tensor product](https://transformer-circuits.pub/2021/framework/index.html#notation-tensor-product) 로 표현하면 아래와 같다.
<img width="571" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/80f34245-0d57-403a-8cf7-30190483732c">

contextualized embedding $x$를 V로 만들고 attention score A랑 곱하고 이를 outputrhk rhqgksek.
이를 정리하면 아래와 같이 되고 $W_oW_V$는 하나로 합칠 수 있다.

<img width="341" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ca42272e-3225-4e4c-b36a-40f20ae145ab">

### Observation about attention heads
- attention head는 residual stream에서 token이 다른 토큰으로 옮겨가는 역할을 한다. residual vector space를 "contextualized word embedding"이라고 볼 수 있다. 
- 이때 $A$와 $W_OW_V$ 두개의 linear operation으로 볼 수 있는데 두개가 다른 역할을 하며 움직인다.
  - $A$는 "어떤 token"의 정보가 어디서 어디로 가는지를 관장한다
  - $W_OW_V$는 source token에서 "어떤 정보"가 읽히고 작성되는지를 정한다. 
- 이때 $A$만 softmax가 있어서 nonlinear하고 $A$를 고정하면 linear연산으로 볼 수있다. 
- $W_Q$, $W_K$는 항상 같이 움직이고 그래서 우리는 $W_OW_V$, $W_Q^TW_V$를 하나의 low rank matrix처럼 생각할 수 있다.

### Zero-Layer Transformer
mhsa가 없는 그냥 zero-layer transformer는 일종의 bigram을 학습하는 역할을 한다.
<img width="151" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7ea2edfe-9f2c-4194-941d-887ba0b01ab2">


### One-Layer Attention-Only Transformer
<img width="754" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5e9bd685-cfd4-4cc4-8000-bc74e43a49fb">

아래와 같이 정리될 수 있다. h는 각 head별 연산이고 sum으로 구할 수 있다 (위의 섹션에서 정리했듯이)
이걸 tensor notation으로 바꾸면 
<img width="725" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/732979fb-c111-47d9-b4fa-d3660f25399e">

이렇고 이걸 다시 바꾸면
<img width="690" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/53452059-a9a1-4b21-8b83-8307579f477c">


이렇게 두개로 분리된다. 앞의 term은 zero-layer transformer의 bigram statistics를 전달하는 역할 뒤의 항은 attention head

### Splitting Attention Head terms into Query-Key and Output-Value Circuits
두번째 항을 또 분리할 수 있다. 
<img width="709" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a653d3c0-0171-41be-b939-c171bfd8b9bc">

<img width="768" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d041864d-bafa-40fb-b9be-a99c593389c8">

앞에 설명했듯이 OV cirtcuit은 how to attend 이고 QK circuit은 어떤 token을 attend 할 것이냐 이다.

### OV AND QK INDEPENDENCE (THE FREEZING ATTENTION PATTERNS TRICK)
이거 보려고 내가 읽음..
결론은 두번 forward해서 QK circuit을 저장해 놓고 이걸 고정된 값으로 보고 OV circuit을 분석하면 linear 하므로 여러 재밌는 분석을 할 수 있다는 것 ! 

> Thinking of the OV and QK circuits separately can be very useful, since they're both individually functions we can understand (linear or bilinear functions operating on matrices we understand).
But is it really principled to think about them independently? One thought experiment which might be helpful is to imagine running the model twice. The first time you collect the attention patterns of each head. This only depends on the QK circuit. 14 The second time, you replace the attention patterns with the "frozen" attention patterns you collected the first time. This gives you a function where the logits are a linear function of the tokens! We find this a very powerful way to think about transformers.

사실 이 뒤에 부터가 더 재밌는 것 같은데... 지쳐서 여기까지만 읽는다. 