---
title: "[135] Multimodal C4: An Open, Billion-scale Corpus of Images Interleaved with Text"
date: 2023-11-23
tags: ['multimodal', 'dataset', 'NeurIPS', '2023Q2']
paper: "https://arxiv.org/abs/2304.06939"
issue: 147
issueUrl: "https://github.com/long8v/PTIR/issues/147"
---
<img width="677" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/38141128-59ee-43b3-858a-83e303fb5969">

[paper](https://arxiv.org/abs/2304.06939), [code](https://github.com/allenai/mmc4)

## TL;DR
- **I read this because.. :** VLM을 할 시간.. 아마 첫 interleaved image-text data. OpenFlamingo에서 사용.
- **task :** data
- **problem :** open interleaved image-text data
- **idea :** common crawl에서 시작해서 이미지 취득. 
- **input/output :** sequence of images, sequence of texts -> text
- **architecture :** OpenFlamingo(3B) https://github.com/long8v/PTIR/issues/118, 
- **objective :** CE loss 
- **baseline :** LAION-2B로만 trained된 Flamingo
- **data :** Multimodal C4(mmc4), Multimodal C4 fewer-faces(mmc4-ff), mmc4-core, mmc4-core-ff -> COCO caption
- **evaluation :** zero-shot captioning, 4-, 8-shot captioning 
- **result :** LAION-2B pretained보다 월등히 좋은 성능 (신기하넹..) 
- **contribution :** first public open interleaved image-text data
- **etc. :**

## Details
### `mmc4`
<img width="755" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7d34b4d4-bf41-4018-bcaa-048ca0883e2f">

### Data Curation Process
- source
Common Crawl의 April 2019(많이 사용되는 dump라고 함) 중에 clean 버전인 c4 사용(365M documents, 156B tokens)
- images
c4에서 original web page 다운 받은 뒤에 이미지 다운로드 
확장명 png / jpeg / jpg만 남기고 logo, button, icon, plugin, widget이란 글자 있으면 제거. 장축 800 pixel로 resize. -> 115M documents / 1.37B images
- dedup + small resolution
  - dedup : https://gitlab.com/opennota/findimagedupes 사용
  - small resolution : 단축이 150이하면 제거. 
  - 장단축 비율이 2 이상이거나 0.5 이하면 제거(banner-like ads를 제거하는데 도움이 되었다고 함)
  - 3.7K의 sample을 뽑아서 확인한 결과 2.5% 정도가 광고인걸로 확인
- NSFW
  - [dataset2metadata](https://github.com/mlfoundations/dataset2metadata/tree/main) 패키지 사용해서 NSFW binary classifier를 사용 
  - LAION-2B에서 분류한 NSFW 이미지로 classifier 학습해서 분류. 
- Aligning images and sentences
  - C4는 전처리된 버전이고 이미지는 전체 다운받았으므로 이미지에 해당하는 텍스트가 없을 수도 있음
  - html의 DOM을 보고 되긴 한데 그렇게 하지 않음 
  - 일단 이미지와 모든 문장 간의 pairwise correlation을 구함. 
  - 이때 한 문장이라도 유사도가 0.15 안넘는 이미지라면 제거
  - 그 뒤에 bipartite matching을 시켜서 각 문장이 가질 수 있는 이미지는 한개가 되도록 assign
<img width="371" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/175a712e-dbdd-4cd7-aa39-90af54bf5f8d">

이렇게 할 경우에 그냥 유사도 max하는 assign 하는 것보다 coverage가 높아진다. 

assign 한 뒤에 Flamingo의 방식에 따라 문장 앞에 두거나 문장 뒤에 둠 
<img width="948" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b49fcba0-ec4c-479a-8dac-8c0f42b5b644">

실제 예시
<img width="782" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e122bfb1-5711-4ad7-8008-b9ab81cf94dd">

### Exploring `mmc4`
- url source
<img width="995" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e07abea3-ca6e-492b-bd4d-47320a0a6ed1">

- topics 
LDA -> top frequent words -> GPT4로 주제  
<img width="780" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0347c786-11ba-431d-badc-a4e5a0a920ec">


### Result
Open Flamingo 사용해서 학습하고 LAION-2B로 학습한 애와 비교 
- Retrieval
<img width="957" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/bebf7be8-575e-450f-b54c-aa07bd4075b4">

- COCO caption 
<img width="571" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7701d36a-55af-47d0-ae34-f70bf752c57e">

15M의 LAION-2B로 학습된 애랑 MSCOCO caption zero-shot / 4-/ 8-shot caption 학습 한 것 비교
빨간색이 zero-shot 성능. 4, 8 shot보다 떨어지는 이유는 LAION-2B가 짧은 텍스트로만 학습되어서 긴 텍스트 나오니까 못하는거 아니냐함
2B로 비교해야되는거 아닌지; 

(from FLAMINGO, coco dev set, 4shot)
<img width="1100" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/79076c34-3757-428c-8516-bde27c389f09">

