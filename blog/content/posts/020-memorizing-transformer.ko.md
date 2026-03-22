---
title: "[20] Memorizing Transformer"
date: 2022-04-07
tags: ['NLP', '2022Q1', 'google', 'ICLR', 'long']
paper: "https://arxiv.org/pdf/2203.08913.pdf"
issue: 20
issueUrl: "https://github.com/long8v/PTIR/issues/20"
---
![image](https://user-images.githubusercontent.com/46675408/162104237-089962f3-c835-45c6-a61b-c2cc3c138fc5.png)
[paper](https://arxiv.org/pdf/2203.08913.pdf)

## TL;DR
긴 context를 참조할 수 있게 이전 시퀀스들의 key, value matrix를 cache 해놓자.
그리고 kNN lookup(e.g. Faiss, ScaNN)등을 사용해서 현재 쿼리와 관련있는 key, value를 뽑은 뒤 이를 key, value matrix에 concat하여 attention을 구하자. 이때, 이전 cache된 메모리들은 학습되지 않는다.

## background
### long document
트랜스포머에서 시퀀스 길이가 길어지면 보통 하게 되는 접근법은 시퀀스를 메모리에 올릴 수 있는 최대 시퀀스 길이로 자르는 것이다. 
이 때, 같은 문서라도 길이에 의해 잘리게 되면 그 전의 정보를 알 수 없고 이를 "context fragment problem"이라고 한다.
![image](https://user-images.githubusercontent.com/46675408/162108203-7968c7d5-67e2-4f9e-aa40-9395c563e7ed.png)

특히 소설이나 코드 같은 경우에 멀리 있는 context를 참고해야하는 경우에 이러한 문제는 부각된다. 
이를 해결하기 위해 Transrformer-XL, longformer, reformer등이 있는데, 가장 관련있는 Tranformer-XL을 간단히 소개해본다.
![image](https://user-images.githubusercontent.com/46675408/162108330-acb7eab3-2dfd-42e3-b7ab-5b34e2c3134a.png)
Transformer-XL의 주요 아이디어는, 
이전 segment들의 n번째 레이어의 히든벡터로 cache한 뒤, 이를 현재 segment의 히든벡터와 concat하여 attention 연산을 진행한다. 
![image](https://user-images.githubusercontent.com/46675408/162108701-3bc6a782-3c9f-4c58-850b-8e5fd8117915.png)
이때 cache된 히든벡터들은 back-propagation 되지 않는다.

### kNN lookup
query가 주어졌을 때 가장 근접한 k개의 데이터를 찾아 뽑는 것
가령, 학습된 word2vec이 있을 때, vector(queen) - vector(female) + vector(male)을 계산한 벡터가 있을 때, 이 벡터가 word2vec에서 학습된 모든 단어의 벡터들 중 무엇과 가장 가까울까를 계산하고 싶을 때 사용된다고 생각하면 됨.
이를 효율적으로 구현해 놓은 구현체 1) [faiss](https://github.com/facebookresearch/faiss) 2) [ScaNN](https://ai.googleblog.com/2020/07/announcing-scann-efficient-vector.html)

### retrieval with transformer
kNN lookup을 한다는 것은 일종의 retrieval(검색)을 한다는 뜻인데, transformer에서 나온 벡터를 사용하여 검색을 하고 이를 NLP task에 접목한 접근법으로는 REALM, RAG 등이 있음. 
REALM은 QA를 하기 위해서 쿼리가 주어졌을 때 document들을 retrieval하는 모델과 그 결과로 얻어낸 docuemnt를 붙인 MRC 모델을 e2e로 같이 학습 하는 모델이다.
![image](https://user-images.githubusercontent.com/46675408/162110005-cddf1cfe-b250-4af7-88ab-b8793745c84a.png)

## Memorizing Transformer
memorizing transformer는 background에서 설명했듯 긴 문서를 효율적으로 tackle하기 위하여, 쿼리와 가장 유사한 key값을 가진 segment를 kNN lookup으로 뽑은 뒤 이를 attention 연산을 할 때 덧붙이는 접근 방법이다. 

우선 문서는 아래와 같이 순서대로 자른다.
![image](https://user-images.githubusercontent.com/46675408/162111133-4817372f-61f7-482f-8a35-f0c3af60c495.png)
하위 레이어에서는 보통의 transformer decoder처럼 진행을 한다. 그리고 각 segment에서 나온 key 벡터와 value벡터들을 cache로 저장해놓는다. 
메모리가 다 찰 때까지 큐에 저장하고 메모리가 부족하면 빼내고 최근 segment의 key value를 넣는다.  
![image](https://user-images.githubusercontent.com/46675408/162111100-825fd565-9745-4654-9270-ac8a1a66b5c3.png)

이제 쿼리가 주어졌을 때, 1) 일반적인 local context에 대한 attention을 진행하고 2) 해당 쿼리를 저장된 메모리에 kNN lookup을 통해서 k개를 뽑은 뒤 이 k개의 key, value를 통해서 attention matrix를 만든다. (k개의 key, value에 대하여 transformer decoder했다고 생각하면 됨)
![image](https://user-images.githubusercontent.com/46675408/162113989-b0ec1809-840f-4579-ae7f-b0f32c95fef2.png)

그리고 1)과 2)를 head에 따라 다른 scala parameter를 사용하여 weighted sum을 하면 된다. 
![image](https://user-images.githubusercontent.com/46675408/162114512-c6521e41-0670-4876-908e-eb6ecfe1705a.png)
대부분의 경우에 거의 모든 head에서 external memory를 참조함을 실험을 통해 발견했다.

**Position bias**
T5 스타일의 position bias를 추가하였다. 
![image](https://user-images.githubusercontent.com/46675408/162117109-21d62b90-b198-4c0f-9ef5-48c3a9a9f9e7.png)
일반적인 relative position embedding를 조금 간소화시킨 형태인듯 하다.

**Batching**
각 배치가 다른 document를 가지고 있기 때문에 memory는 분리되어 있고, document가 끝나면 그 memory는 지워진다 (다른 document에 대해서는 참조하지 않도록 설계) 

## Experiment
**Dataset**
- github code, arXiv에 내 수학 관련 논문, 수학 이론 증명에 대한 corpus인 Isabelle, C4 내 토큰 길이 4096 이상인 데이터, 영어책 데이터인 PG-19

**Parameter**
- 12 layers transformer, 1024 hid dim, 8 heads, FFN dim 4096
- kNN에서 k는 32, 12레이어 중 9번째 레이어에서 사용
- sentence-piece tokenizer(vocab size 32K)
- Adafactor optimizer, linear warmup scheduler, square root decay, 32 TPU
- JAX implementation

## Result
**Scaling to Larger Model**
![image](https://user-images.githubusercontent.com/46675408/162110640-97e673f3-d931-4efe-9d53-24012bdbe5ff.png)
8K 토큰을 memory를 가진 우리의 모델은 vanilla Transformer와 비교했을 때 모델사이즈가 5배 작아도 비슷한 성능을 낼 수 있음.

**Effect of External Memory**
![image](https://user-images.githubusercontent.com/46675408/162110611-4007c233-c9b8-4454-9a2e-07cba0efff6a.png)
XL cache가 Transformer-XL으로 보면 됨.
vanilla Transformer, Transformer-XL에 대해 external memory가 perplexity를 개선
vanilla Transformer에서 segment가 잘려 첫 토큰에서 정보가 없는 걸 XL cache가 local한 short-range context를 보충해줬고, external memory가 더 long한 context를 보충해줌.
context길이가 512이고 memory가 8192(arxiv 2.49)인 경우에 context 2048이고 xl cache가 2048인 것(arxiv 2.42)과 성능이 유사함.
memory는 differential하지 않고, context는 differential 가능하고 모든 레이어에 영향을 미치는데 성능이 비슷하다는 것은 트랜스포머의 밑의 레이어에서는 long-range context가 반드시 필요하지 않다는것을 의미함.

**Finetuning a non-memory model to use memory**
![image](https://user-images.githubusercontent.com/46675408/162122760-5eb4a44e-0f12-4ccf-8b9a-f258d8bdd038.png)
프리트레이닝을 위와같이 하는 것은 꽤 costly하므로 fine-tuning을 할 때만 memory를 사용하도록 해봤는데 잘 작동했다.

**Information Retrieval Patterns**
정의, 사람 이름 같은 rare한 단어를 look up하는 경우가 많았음. 
![image](https://user-images.githubusercontent.com/46675408/162112281-ac48ec0d-086c-4b5a-b5f2-3b2d904eb02d.png)
Isabelle 데이터셋에서 retrieved 된 context의 예시

## conclusion
1. 아이디어가 심플하고 직관적임
2. 우리 도메인에서는 글쎄.. segment가 너무 길어서 transformer XL이 커버할 수 있는 segment를 벗어날때만 의미 있을 듯. 
3. seq_len을 자르고 batch_size를 훨씬 키워서 빠르게 학습시키는데 의의를 둘수도? 
4. finetuning에만 적용해도 되니 (구현만 되면) 적용은 쉬울듯

## etc
**papers**
- relative PE https://arxiv.org/pdf/1803.02155.pdf
- different style or relative PE https://arxiv.org/pdf/2006.15595.pdf