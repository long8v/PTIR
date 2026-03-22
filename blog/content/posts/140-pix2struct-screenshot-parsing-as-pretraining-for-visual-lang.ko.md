---
title: "[128] Pix2Struct: Screenshot Parsing as Pretraining for Visual Language Understanding"
date: 2023-08-21
tags: ['ICML', 'google', '2022Q3', 'document']
paper: "https://arxiv.org/pdf/2210.03347.pdf"
issue: 140
issueUrl: "https://github.com/long8v/PTIR/issues/140"
---
<img width="920" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/21d65bd3-3703-41c7-8c40-da08ccef60c5">

[paper](https://arxiv.org/pdf/2210.03347.pdf)

## TL;DR
- **I read this because.. :** document 도메인에서 ViT variable resolution 처리하는 방식이 좀 다르다고 해서 읽음
- **task :** document understanding / UI / image captioning 
- **problem :** 파이프라인 말고 이미지 인풋 받고 바로 처리하고 싶다. 그런데 이미지의 비율이 극단적인 경우가 좀 있다. 그냥 문서 말고도 UI 이런 것도 한번에 처리하고 싶다.
- **idea :** 세상에 웹페이지는 많으니 html을 screenshot으로 render 한 뒤에 원본 html을 generation하게 하자!
- **input/output :** 텍스트가 포함된 웹 이미지 -> text 
- **architecture :** ViT + decoder (12 encoder w/ 768 hidden dim or 18 encoder, w/ 1536 hidden dim) -> Base(282M), Large(1.3B)
- **objective :** contrastive loss(html recontstuction + masked token prediction)
- **baseline :** Donut, UDOP, PaLI, VTP, DQAN, LATr, UIB, VUT
- **data :** C4 corpus에서 URL 다운 받아서 80M의 screen shot 데이터를 만듦 -> DocVQA, InfoGraphicVQA, UIChartQA, AI2D, OCR-VQA, RefExp(자연어로 표현하고 있는 웹 사이트 상 부분을 찾는 문제), Widget Captioning(앱 스크린 샷에서 선택된 버튼 등이 어떤 역할을 하는지 captioning 하는 것(e.g. `find location`), 
- **evaluation :** ANLS for DocVQA/InfoVQA, exact match for AI2D/RefExp/OCR-VQA, relaxed accuracy(RA) for Chart QA, CIDEr for generation task 
- **result :** image input만 받는 애들 중에 sota. 그 외에는 captioning은 PALI에게 DocVQA, InfoVQA는 UDOP한테 밀림. Donut은 다 이김.
- **contribution :** 여러가지 task sota. 특히 UI 쪽을 같이 푼게 아마 처음인 듯하당.
- **etc. :** 이걸 이제 읽다니..

## Details

### variable-resolution 
<img width="928" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/bb32764a-d7bf-4c0c-a64d-c80660ee422f">

보통 ViT는 정사각형으로 resize 해서 학습하는데 그렇게되면 (1) 찌부가 되고 (2) 나중에 high resolution으로 갔을 때 sequence length가 길어졌을 때 성능이 잘 안나옴
여기서 제시하는 방식은 aspect ratio는 유지하되 sequence length가 maximum으로 꽉꽉 채워지도록 이미지를 resize 하는 것 (patch size가 바뀌는건 아님) 

### Pretraining
C4에서 url로 html render해서 사용
이 때 (1) visible element 만 사용하고 (2) visible element가 없는데 child가 있을 경우 grandchild로 child를 대체. 
text + alt-text 와 filename 정도를 사용
이미지에서 파란색으로 박스 친 부분의 html을 recover하라고 알려줌 
<img width="774" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/86c6fa77-6fef-4329-bce1-dd50a358f6bf">

추가로 빨간색으로 박스 치고 맞추게 함. 일종의 이미지에서의 masked language modeling. text의 50% 정도.

### Curriculum learning 
위에걸 scratch로 학습하기엔 학습이 불안정해서 일단 읽기부터 시킴.
Book Corpus로 랜덤 컬러 랜덤 폰트로 렌더링 한 뒤 30K step 정도. (200K in donut)

### Finetuning
GPT에서 그냥 Q를 같이 넣듯이 여기도 이미지에 question 등을 같이 rendered해서 넣어줌
<img width="890" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d80b6ddc-d4b6-4e1a-b242-488aae212b3c">

### Training Details
- 282M / 1.3B (Donut 143M)
- 12 layers 768 hidden dim / 18 layers 1536 hidden dim
- 128 image patches 
- 128 decoder sequence length
- output은 128 characters가 안 넘도록.
- batch size 2048 with 64 TPUs / batch size 1024 with 128 TPUs (196 with 64 A100s in donut)
- BLEU로 validation. 

### Result 
<img width="902" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5088adea-3be4-4eb9-bdf9-c9fd154734af">

PALI한테 captioning 밀리고, text-rich한 DocVQA 같은 경우에도 OCR 등을 쓰는 UDOP한테 밀림. 
아무래도 데이터 자체가 caption 많이 해서 학습한 애들보단 밀릴 수 밖에? 
그 외에는 Donut / GIT을 이기고 특히 UI 쪽은 재패해버림. 엄청난 sota.

### Ablation 
- pretraining component
<img width="441" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/444baf47-628f-423d-8347-d00bd4a5e40b">

Screenshot Parsing이 가장 많이 떨어졌고 warmup이랑 masking은 비슷한 정도로 떨어짐

- variable-resolution
<img width="468" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/609b5335-99ff-4e6f-9cd8-32769e9f326f">

padding이 상당히 안좋은 모습.. stretch가 비율 찌부하는거!