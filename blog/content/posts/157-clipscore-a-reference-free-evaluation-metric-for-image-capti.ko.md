---
title: "[145] CLIPScore: A Reference-free Evaluation Metric for Image Captioning"
date: 2024-02-05
tags: ['2021Q2', 'CLIP', 'emnlp', 'evaluation', 'AI2']
paper: "https://arxiv.org/abs/2104.08718"
issue: 157
issueUrl: "https://github.com/long8v/PTIR/issues/157"
---
<img width="764" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a6080f82-cf65-4ead-beb6-bcb23f237fc7">

[paper](https://arxiv.org/abs/2104.08718)

## TL;DR
- **I read this because.. :** clip score에 관심 있어서 
- **task :** evaluation for captioning 
- **problem :** 이전의 reference 기반의 evaluation은 친숙한 단어에 bias되어 있는 경향이 있다
- **idea :** CLIP score 써서 평가하자!
- **input/output :** {image, caption, (optionally) references} -> score
- **architecture :** CLIP ViT-B/32
- **baseline :** BLEU-1, BLEU-4, ROUGE-L, BERT-score, CIDEr, SPICE
- **data :** Flickr8K-Expert, Flickr-CF, Pascal-50S, FOIL hallucination detection,
- **evaluation :** kendall correlation with human judgement(Flickr8K-Expert, Flickr-CF). accuracy(Pascal-50S, FOIL)
- **result :** human judgement와 가장 높은 correlation, 높은 accuracy, captioning score들로 forward selection 했을 때 항상 선택되는 metric들 중 하나. 
- **contribution :** 간단하고 이전 referecne기반의 평가를 개선하는 metric 제안! 분석을 엄청 massive하게 함. 
- **etc. :** 아이디어가 간단하면 이정도 분석은 해야 논문을 낼 수 있구나..

## Details
### motivation
<img width="339" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ca89da34-46d9-442b-913e-a3d46d097a59">

### `CLIPScore`
<img width="293" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/dafccd53-c341-4c9c-b0c6-49e6acfe2c1d">

- c: caption의 CLIP text embedding
- v: image의 CLIP vision embedding
- w is set to 2.5 그냥 해석의 용이성을 위해 추가한 rescaling scalar.
  - cosine은 이론 상 [-1, 1] scale을 가져야하지만 한번도 negative를 본적이 없다고
  - score가 항상 [0, 0.4] 사이에서 위치하는걸로 보여서 [0, 1]로 만드려고 2.5를 곱함
footnote에 region-leval/token-level correspondence models(maybe FILIP?!)이 성능이 더 좋지 않았다고 서술.

### `RefCLIP-s`
referecne caption도 활용하는 버전.

<img width="347" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5589936d-747f-45f7-8a57-5dabf4fbdf3f">

- r: referecnes의 CLIP text embedding

### Caption-level likert judgements
- Flickr8K-Expert 
5664개의 이미지에 대해 17K개의 "expert" human이 caption에 대한 점수를 1점부터 4점으로 매긴 것(1점 unrelated~4점 에러가 없이 잘 평가했다)
<img width="350" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4a310f1e-521b-4d13-93ad-7d5df83c45b8">

[leaderboard]((https://paperswithcode.com/sota/human-judgment-correlation-on-flickr8k-expert))
오 이 벤치마크 1위가 네이버 논문이넹 .. [Mutual Information Divergence: A Unified Metric for Multimodal Generative Models](https://arxiv.org/pdf/2205.13445v1.pdf) 

- Flickr8K-CF
1K의 이미지에 대해 48K의 {image, caption} pair에 대해 binary로 judgement를 crowd sourcing으로 모은 데이터셋 
<img width="354" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/34c0a1d0-befe-4d88-a376-8d2dd48d516f">

- Composite https://arxiv.org/pdf/1511.03292.pdf
MSCOCO, Flickr8K, Flickr30K에 대한 12K의 human judgement  
<img width="363" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/477076a7-4f35-4c2e-b220-dfbaf1cfb844">

### System-level correlation for MSCOCO
COCO captioner들 결과랑 비교하는?
데이터가 12개 밖에 없다고 함

### Sensitivity of CLIP-S to hallucination
사람의 평가가 "speicificity"보다 "correctness"에 더 많은 영향을 준다고 함
이를 평가하기 위해 hallucination 데이터셋인 FOIL(https://arxiv.org/pdf/1705.01359.pdf)로 평가 
MSCOCO에서 single noun phrase에서 명사를 비슷한 단어로 치환을 하는 형태 (e.g., switching “motorcycle" for “bicycle")
32K의 sentence에 대해 치환한 문장이 그렇지 않은 문장보다 더 높은 score를 주었는지로 평가.

<img width="415" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c63c7050-9cb7-4fc9-9652-9426c8bb0e64">

### Sensitivity of CLIP-S to memorization
혹시 CLIP 학습 과정에서 caption을 배운 걸까봐 직접 데이터셋 모아서 함

### Which metrics should I report?
- R2를 기준으로 10개의 Metric에 대해 forward selection 진행.
- BLEU-1, BLEU-4, METEOR, CIDEr, ROUGE-L, SPICE, BERT-S(RoBERTa-F), TIGEr, ViLBERTScore-F, and CLIP-S
<img width="403" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/707a9bb4-4938-4525-afee-e627fb1160d7">

적어도 상위 4개개에서 선택됨을 확인
또한 metric끼리 correlate되어 있지만 redundant하지는 않음을 확인.
 SPICE 같은 reference 기반이랑 같이 쓰는게 더 좋을 것 같다고 함

