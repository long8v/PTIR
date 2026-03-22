---
title: "[149] Noise-aware Learning from Web-crawled Image-Text Data for Image Captioning"
date: 2024-02-12
tags: ['ICCV', '25min', '2022Q4', 'kakao']
paper: "https://arxiv.org/pdf/2212.13563.pdf"
issue: 161
issueUrl: "https://github.com/long8v/PTIR/issues/161"
---

<img width="708" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ba1962ff-1e13-49b0-b298-cca7b8085223">

[paper](https://arxiv.org/pdf/2212.13563.pdf), [code](https://github.com/kakaobrain/noc)

## TL;DR
- **I read this because.. :** aka noc. 뭔가 CLIP score에 대해 분석을 잘 했을 것 같아서 읽음.
- **task :** captioning with noisy image-text label
- **problem :** COCO, Visual Genome 같은 데이터는 scalable하지 않음. 그렇다고 web-crawled pair를 쓰자니 noisy할 수 있고 이걸 CLIP score로 filtering 하자니 또 데이터의 상당수가 사라짐. 
- **idea :** CLIP score를 binning 한 뒤 임베딩하여 captioning할 때 제공하게 하고 inference 단계에서는 가장 잘 align 된 score를 주고 추론하게 함
- **input/output :** image, clip score of {image, text} pair -> text 
- **architecture :** CLIP ViT-L/14 + 6-layer transformer(94.5M)
- **objective :** cross-entropy loss 
- **baseline :** no filtering, filtering(clip score 0.3), loss reweighting(loss에 clip score를 곱해줌), ZeroCap, Socratic Model, DeCAP
- **data :** CC3M (noisy한 축에 속하는 구나.!), ablation으로 COYO도 해봄 
- **evaluation :** COCO, nocaps에 대해 BLEU, METEOR, CIDEr, SPICE, CLIPScore // self-retrieval R@1(특정 이미지로 생성한 caption으로 retrieval 했을 때 그 이미지가 나오는지)
- **result :** BLEU 빼고 sota
- **contribution :** 간단하고 직관적임~
- **etc. :** 원하는 건 못 얻었지만 재밌게 읽었다~ 가장 비슷한건 BLIP이라는데 생각해보니까 그럼.. BLIP 참 선구적인 연구인듯

## Details
- motivation 
<img width="349" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/53490c39-a188-4b73-8b80-6000d4c0aa81">
<img width="706" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/308dc477-a934-4572-a6c7-16aabb4caec2">

<img width="349" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9333897c-ae45-45ac-bae4-9a6767981115">


- architecture 
<img width="698" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6fd72080-5343-4319-a711-7e69aaba204f">

- results
<img width="670" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5279a976-ded6-4659-92ae-dc084ba490c2">

- ablations 
<img width="685" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ce21f97b-739d-4602-be49-253681bf2a32">

- qualitative 
<img width="702" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6b8e46db-b9b6-415a-93e1-7b19fa4f297f">
