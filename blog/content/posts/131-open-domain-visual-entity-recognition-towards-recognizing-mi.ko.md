---
title: "[121] Open-domain Visual Entity Recognition: Towards Recognizing Millions of Wikipedia Entities"
date: 2023-06-23
tags: ['multimodal', 'CLIP', '2023Q1', 'retrieval']
paper: "https://arxiv.org/abs/2302.11154"
issue: 131
issueUrl: "https://github.com/long8v/PTIR/issues/131"
---
<img width="829" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4cc07c59-1c9c-4aad-a020-393437777657">


[paper](https://arxiv.org/abs/2302.11154)

## TL;DR
- **I read this because.. :** 많이 언급되어..
- **task :** Open-domain Visual Entity recognition(OVEN). 
- **problem :** VLM은 general한 object에 대한 질답은 할 수 있지만 좀 더 fine-grained한 visual concepts을 뽑아낼 수 없을까?
- **idea :** wikipedia 기반으로 entity를 만들고 {image, query}가 주어졌을 때, 이 query의 answer 해당하는 Entity를 찾는 문제를 정의하자. 
- **input/output :** context image + text query + knowledge base(wikipedia) -> wiki page 
- **architecture :** dual-encoder의 경우 CLIP. 1) 4가지(context image, query <-> wiki page image, text)에 대한 cosine similiarity에 대한 가중이 학습되는 CLIP2CLIP. 2) image encoder와 text encoder 위에 정보를 fusion하는 두 레이어의 Transformer를 한 CLIP fusion 3) PALI로 finetune 한 뒤에 PALI의 output을 BM25로 wikipedia에서 retrieval. 구체적인 arch는 CLIP based ViT-L14 / PaLI-3B와 PaLI-17B
- **objective :** dual encoder의 경우 similiarity기반이니까 InfoNCE 같은게 쓰였을 듯? PaLI는 CE loss.
- **baseline :** 벤치마크를 제안한거라 이 논문자체가 베이스라인
- **data :** 14개의 벤치마크 데이터셋을 가지고 wiki랑 mapping을 해서 만듦. 정제도 좀 거치고 human annotation도 좀 쓴듯
- **evaluation :** 정확도로 예측. seen entity에 대한 정확도와 unseen entity에 대한 정확도의 조화평균.
- **result :** PALI가 생각보다 성능이 매우 좋다. 즉 모델 안에 entity를 잘 담고 있다. 특히 query split(VQA 기반으로 만든거)가 성능이 좋았다. CLIP Fusion이나 CLIP2CLIP의 경우에도 성능이 파라미터수 대비 PaLI랑 비슷하니 꽤 강력한 basline이다!
- **contribution :** 새로운 벤치마크 및 베이스라인 제시.
- **etc. :**

## Details

### Task set-up
<img width="1260" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ccd0dbdb-730d-4fc3-9c53-a2949ed396e5">

처음 제안한거라 setup자체가 중요한데
잘보면 context image와 이에 대한 질문이 있음. 즉 걍 image retrieval이 아님! 
image와 query를 잘 조합해서 wikipedia에서 답에 해당되는 entity page를 찾아내는게 문제 셋업임.

### Data
두 가지로 나눌 수 있는데,
- Entity Setup : 분류나 retrieval 기반의 데이터셋들 -> 질문을 templated query generation으로 만듦
- Query Setup : VQA 기반의 데이터셋들 -> 질문에 대한 답이 entity에 대한게 아니면 정제함

<img width="1284" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6bac031d-01dc-4eb5-b722-ed82a8d1813e">

그리고  뭐 사람 써서 label disambiguation 같은걸 했다고 하넹 

### evaluation
seen entity / unseen entity에 대한 정확도의 조화평균 
<img width="622" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/371a958f-6011-487e-aa24-5bd56debb90b">


### Baseline
$x^t$ : input intent
$x^p$ : input content
$p(e)$ : entity images
$t(e)$ : entity text

<img width="401" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/00db5e65-fee5-49af-a6d7-92595b751b14">

- Dual encoder
CLIP 사용. 걍 retrieval 문제로 바꿔서 풀면?
CLIP2CLIP의 경우 $(x^p, t(e)), (x^t, p(e)), (x^p, p(e)), (x^t, t(e))$의 cosine similiarty를 구한 뒤에 이의 가중치인 4개의 파라미터만 학습하는 형태. 
CLIP Fusion 두개의 encoder위에 이걸 잘 fusion 하는 Transformer를 학습.

- Encoder-Decoder model
그냥 oven training dataset을 PALI loss로 학습. PALI가 내뱉는 output에 대해 BM25로 wiki page 찾은걸로 최종 output으로

<img width="617" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0ec5a09d-6fb1-4f25-b184-685d8465872f">

### Result
<img width="1108" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/fe1d6102-9feb-4861-b14d-4124678e5df3">

- CLIPFusion의 경우 query split에 대한 seen entity 성능이 아주 좋았다. 이는 VQ2A objective가 들어있어서 그런 것 같았다. 그러나 unseen이 매우 안좋음
- CLIP2CLIP은 전반적으로 성능이 좋음. 
- PALI가 놀랍게도 생각보다 아주 잘했다. 얘는 CLIP과 달리 entity에 대한 접근이 infer 상황에선 안되는건데 성능이 Unseen에도 좋은걸보니 안에 내부적으로 그런 정보를 잘 담고 있는 것 같았다. 
- overall 성능이 CLIP -> CLIP Fusion으로 가면서 파라미터가 2배 늘었지만 성능이 2배정도 됐는데 PALI는 그만큼 성능이 훅 늘지는 않았다.
- human evaluation 보다는 성능이 많이 못미쳤다. 


<img width="576" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/16a683fb-9f26-4e4d-8287-c88922fdfac1">

두개를 비교해보면 PALI는 질문을 더 잘 이해하지만 더 generic하게 답변하는 경우가 있었다.

<img width="575" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/103c0d96-220b-489c-892e-c7aecc34bfe4">

