---
title: "[136] Visually-Situated Natural Language Understanding with Contrastive Reading Model and Frozen Large Language Models"
date: 2023-11-28
tags: ['multimodal', 'naver', '2021Q3', 'document', 'emnlp']
paper: "https://arxiv.org/pdf/2305.15080.pdf"
issue: 148
issueUrl: "https://github.com/long8v/PTIR/issues/148"
---
<img width="713" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/78ac8841-6bdb-4454-ad1e-f942a5984ad3">

[paper](https://arxiv.org/pdf/2305.15080.pdf)

## TL;DR
- **I read this because.. :** aka cream. 동료의 논문
- **task :** DocVQA
- **problem :** OCR없이 VQA 하는데는 성능의 제한이 있고, OCR을 사용해서 input으로 넣어주기엔 토큰 수를 많이 먹는다
- **idea :** OVD와 OCR을 사용하고 auxiliary encoder로 feature 뽑은 뒤에 CA로 이를 활용 
- **input/output :** 이미지, ocr 결과(box and text), ovd 결과(box and class text), 질문 -> answer 
- **architecture :** Vision Encoder(CLIP ViT-L /LAION-2B), Auxiliary encoder(mBART), decoder(mBART, standalone 모드), LLM(Vicuna). 
- **objective :** text read, masked text prediction, captioning, qa, qg /  CL loss + LM loss -> qa / LM loss 
- **baseline :** ocr의 결과를 LLM에 밀어넣는 것, BLIP, UDOP, Pix2Struct, MatCha, Donut, T5 
- **data :** (text read adn masked text prediction) IIT-CDIP, Webvicob, (captioning) CC3M,  (QA + QG) WKVVQA, SquadVQA, TydiVQA(이 논문에서 제안) 
- **evaluation :** (ChartQA) Accuracy, ANLS, nED, BERTScore, PPL
- **result :** 단순 LLM에 ocr 넣는 것보단 월등히 좋고 document 특화 모델에 대해서 InfoVQA 빼고는 multi-task model 중에서는 sota. 성능상 sota는 UDOP. 
- **contribution :** document 도메인에서 ocr token을 어떻게 잘 활용할지 방안 제안. ocr이 불안정할 때도 성능이 흔들리지 않게 하는 CL 방법 제안.
- **etc. :** appendix가 참 알차다 

## Details
### Architecture 
<img width="677" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e0c10e36-c304-4880-b25a-2202fd5d4818">

전체적인 구조는 BLIP-2랑 비슷하다
<img width="525" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5dd8f271-8608-4e61-a642-63b363d45f35">

그런데 여기에 추가적으로 vision encoder output말고도 auxiliary encoder를 사용하는게 차이점! vision encoder output과 aux encoder output은 concat해서 cross-attention으로 decoder에 들어간다

이렇게 CA를 사용하게된 motivation은 text-rich한 이미지는 ocr 결과가 너무 많아서 토큰수를 너무 많이 먹는다는 점! 
<img width="341" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/bc9cee24-ae76-469a-ae01-59adcfcea06a">


<img width="336" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/19a29c8a-a7bb-4a81-bee7-66e8f04489c9">

<img width="679" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f98f7cf9-eace-4105-89af-235b05bca1be">

그림이 좀 헷갈리게(마치 crop되어 있는 것처럼) 그려져 있는데 contrastive의 대상이 되는 postivie pair는 위의 그림에서 나온 aux output과 이에 해당(좌표가 겹치는)하는 patch의 output을 contrastive 하는 것 같다.
이걸 왜 했냐고 설명하냐면 ocr output이 noisy하거나 결과가 한정되어 있을 때 유리하다고 설명하고 있다. 
<img width="352" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2fc35dfc-e9b4-4d16-843e-57c7950c48c7">

<img width="345" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f6ca88a1-7fc4-466f-868c-b85e0d6f31d0">


<img width="355" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0237f0f0-4609-4664-9dbb-a067a7dd8b7b">

vision encoder의 패치가 ocr token encoder output이랑 가까워지도록 하니까 ocr 결과가 좀 누락되도 성능이 좋다고 서술하는듯? 
반면에 OVD는 Owl-ViT를 사용했는데 (with coco 80 classes) DocVQA에서 OVD를 안써도 성능이 거의 안떨어진다고 말한다(81.2 -> 80.9, A.2.) 이건 DocVQA여서 그런거 아닐까 싶기도 하다 

### Dataset 
<img width="333" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/127e2c5d-5eac-4e96-8630-d3910ea2256f">

### Training 
 details 
- LM : CL = 1: 0.5
- learnble queries 개수는 224
- vision encoder에 이미지 넣을 때 pix2struct(https://github.com/long8v/PTIR/issues/140)의 variable resolution 
<img width="340" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f464231f-ff20-4c31-8eb2-c162006a05d2">


### Result
<img width="690" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/01c66af3-419c-4b32-837c-c3ab7176659c">
<img width="322" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b09d5c70-a255-4aae-9b0b-d2ec7692515a">
<img width="335" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f5d15477-70c6-492d-b00b-4cdd7c7ce9f6">

Arithmetic이 개선됨 

<img width="691" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ccf5c425-b4eb-4c1a-b7cf-e4c865f7a82b">

LLM을 붙이면서 산술을 더 잘하지만 잘못된 text를 만들어내기도 한다고 함 
<img width="704" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1598695f-6e91-43be-8d1d-03e6fc1ca646">
