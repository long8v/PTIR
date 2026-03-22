---
title: "[112] RoFormer: Enhanced Transformer with Rotary Position Embedding"
date: 2023-04-26
tags: ['PE', '2021Q2']
paper: "https://arxiv.org/pdf/2104.09864.pdf"
issue: 121
issueUrl: "https://github.com/long8v/PTIR/issues/121"
---
<img width="697" alt="image" src="https://user-images.githubusercontent.com/46675408/234446326-fdae413a-b4a2-41a4-a6b9-7971452c1e3e.png">

[paper](https://arxiv.org/pdf/2104.09864.pdf), [code](https://github.com/huggingface/transformers/blob/v4.28.1/src/transformers/models/roformer/modeling_roformer.py#L318-L343)

## TL;DR
- **I read this because.. :** 논문 스터디. 발제하신 분의 motivation은 사용하시는 모델에 efficient transformer를 사용하고 싶은데 RPE를 사용하는데 이에 대한 kernel 구현체가 없으셨다고.
- **task :** positional embedding 
- **problem :** absolute PE는 학습한 max_len보다 더 긴게 들어왔을 때 일반화가 잘 안됨. relative PE는 additive하게 들어가서 LinFormer 같은 trick이 적용이 안됨
- **idea :** d 차원의 임베딩을 복소공간으로 옮겨서 크기와 공간을 갖는 벡터로 보고 PE를 weight 형태의 affine transformation으로 바꾸자 
- **input/output :** token / token
- **architecture :** transformer 
- **objective :** MLE 
- **baseline :** BERT 
- **data :** English Corpus, WMT-14(MT), CAIL2019-SCM(
- **evaluation :** GLUE,  
- **result :** 빠른 수렴. GLUE에서 BERT보다 더 나은 성능.
- **contribution :** RPE 계열들을 한번 정리해줌

## Details
### Related Work : PEs
- absolute PE 
<img width="222" alt="image" src="https://user-images.githubusercontent.com/46675408/234451063-df929fc9-b744-4214-98b9-7a16a4f59e58.png">

- Shaw et al.
 
<img width="184" alt="image" src="https://user-images.githubusercontent.com/46675408/234451116-c4f86e1e-676b-4581-8b32-fd65dcc6b04a.png">

clipping

- Transformer-XL
<img width="447" alt="image" src="https://user-images.githubusercontent.com/46675408/234451164-0c1dfd0c-f1e5-4498-a79d-b281fc9d8ea6.png">

<img width="481" alt="image" src="https://user-images.githubusercontent.com/46675408/234451219-e8f46794-0df8-4b4e-9e69-b280216bb007.png">

- T5
<img width="212" alt="image" src="https://user-images.githubusercontent.com/46675408/234451420-b1f03e86-523a-48c3-87f0-ae6d28ea9841.png">
 

### Proposed
<img width="567" alt="image" src="https://user-images.githubusercontent.com/46675408/234448733-8a6b90d4-f358-4627-baaa-72f4870b557b.png">

<img width="411" alt="image" src="https://user-images.githubusercontent.com/46675408/234448759-113fd429-1cff-44cf-af25-5b945ebe285a.png">

<img width="163" alt="image" src="https://user-images.githubusercontent.com/46675408/234449790-7ecb27e6-75dc-497b-afea-e97b45c9c3d9.png">


그림은 d=2일 때
 
<img width="488" alt="image" src="https://user-images.githubusercontent.com/46675408/234448787-4ac10ae5-ec4b-459d-8a8d-46fe68f6777d.png">

<img width="350" alt="image" src="https://user-images.githubusercontent.com/46675408/234450333-14835e5e-3ad3-4bba-9943-d0031aa483cd.png">

<img width="560" alt="image" src="https://user-images.githubusercontent.com/46675408/234501720-2cc5d0dc-1f99-463c-92c6-c473f432006c.png">

- f : token embedding + PE
- g : attention score

각자 position idx * angle 만큼 회전시키고 나면 attention score를 구했을 때 relative position embedding을 구하는게 됨
Specifically, incorporating the relative position embedding is straightforward: simply rotate the affine-transformed word embedding vector by amount of angle multiples of its position index and thus interprets the intuition behind Rotary Position Embedding.

d차원으로 늘리면 
<img width="559" alt="image" src="https://user-images.githubusercontent.com/46675408/234448561-15a9fe7f-20f8-43e2-86e7-f34f14bfb127.png">

### Result
<img width="560" alt="image" src="https://user-images.githubusercontent.com/46675408/234447244-64fc7f0a-6469-480a-a1cf-55d82a94ee8d.png">

<img width="710" alt="image" src="https://user-images.githubusercontent.com/46675408/234447389-f4f2f7e7-55ef-45d8-b5c0-8b1ddf88600e.png">

<img width="688" alt="image" src="https://user-images.githubusercontent.com/46675408/234446867-01ca0c99-6714-463e-8a0f-d9059575b7a0.png">

