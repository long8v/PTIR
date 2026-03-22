---
title: "[154] Mismatch Quest: Visual and Textual Feedback for Image-Text Misalignment"
date: 2024-04-03
tags: ['google', 'XAI', 'evaluation', '2024Q2']
paper: "https://arxiv.org/pdf/2312.03766.pdf"
issue: 169
issueUrl: "https://github.com/long8v/PTIR/issues/169"
---
<img width="1612" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/dcef1f5b-0a5f-4199-9d53-5ab08cd0967c">

[paper](https://arxiv.org/pdf/2312.03766.pdf), [page](https://mismatch-quest.github.io/), [dataset](https://huggingface.co/datasets/mismatch-quest/SeeTRUE-Feedback)

## TL;DR
- **I read this because.. :** 개인연구 관련. DSG에서 타고옴 
- **task :** image / text alignment with score!
- **problem :** 기존의 alignment를 측정하는 방법론은 설명을 같이 제공하지 않는다. 
- **idea :** 데이터 및 벤치마크 제작
- **input/output :** {image, text} -> score, misaligned text span, misaligned visual span, feedback
- **objective :** zs or CE loss 
- **baseline :** PALI, mPLUG-Owl, miniGPT-2, LLaVA1.5, finetuned PALI
- **data :** proposed TV Feedback //  test는 AMT로 human 정제까지 함. 
- **evaluation :** binary accuracy(정확한 pair인지), text span(precision, exact match로 한건지 어떤지 잘 모르겠네), feedback이 정확한지는 NLI(BART-NLI 모델 사용), IoU .75
- **result :** finetune PALI가 가장 성능이 좋았고 ood 데이터셋에서도 잘 동작함을 확인함 
- **contribution :** 내가 원하던 연구! 데이터셋 공개! 
- **etc. :**

## Details
<img width="366" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8fc818e1-1ef9-4671-9fd5-345becd263c6">


<img width="1353" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e02cdfc6-0e5b-4582-b213-65b4dc012a06">

<img width="1419" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/11b51f6d-2451-42b0-8cd3-ab434c54dd39">

### Image source
<img width="736" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/683beef9-8301-4a2f-8c7c-0698d9875ed1">

### Proposed ConGen 
- 1) Spcay로 POS를 뽑음. object(noun), attribute(adjective), action(verb), spatial relations 이렇게 4개의 분류로 나눔
- 2) PaLM2를 사용해서 (a) contradiction caption을 만들고 (b) 왜 contradiction인지 detailed caption을 만들고 (c) 캡션 내에 어떤 요소가 틀린지 pinpoint하라고 하고 (d) visual bounding box를 뽑으라고 함. 
- 3) 생성된 contradiction caption이 정말 원래 캡션과 다른지 구분하기 위해서 Textual Entailment model을 사용해서 
- 4) GroundingDINO를 사용해서 PALM2가 뽑은 bounding box의 textual label과 bounding box를 뽑음 
이렇게 뽑은 셋을 Textual Visual Feedback 데이터라고 부름

### SeeTrue-Feedback benchmark
SeeTrue dataset에 기반해서 위의 ConGen과 비슷한 방식으로 뽑은 뒤에 AMT에 태워서 2008개의 샘플을 인간이 검수함. 

<img width="369" alt="image" src="https://github.com/user-attachments/assets/8b7f7a3e-af69-43cc-ad8b-f9074d09743d">

### Evaluation metrics
- Image-text Alignment : binary accuracy
- Textual Feeback Quality : BART NLI로 gt가 premise, prediction이 hypothesis
- Misalignment in text : BART NLI를 사용해서 text segment가 맞는지 확인 (위의 방식과 비슷하겠지?)
- Visual Misalignment Detection: F1-Score@0.75 로 잼
Alignment는 8100개의 SeeTRUE dataset에 포함되어있고 다른 metric은 SeeTrue-Feedback에 포함되어 있음.

<img width="511" alt="image" src="https://github.com/user-attachments/assets/ff8cba95-322e-4f47-a5ef-98bcfa6bc853">


### Result
최신 VLM모델들에게 아래와 같이 질의 
<img width="375" alt="image" src="https://github.com/user-attachments/assets/5b3edaa8-abcd-485e-9edc-cdda3bb7d3bc">

<img width="387" alt="image" src="https://github.com/user-attachments/assets/16fbb984-4817-4ddc-a947-4585b993f910">

<img width="759" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6fb5ac36-1487-4553-984b-a58f240e1d7c">

<img width="783" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a231293a-25fc-4ab0-befd-ee4f1d8828e2">

## limitation of model prediction 
<img width="396" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3d9c5be3-c420-424b-9149-423ce2e4f5e2">

- 이미지의 부재에 대한 Visual Feedback 주기 어려움
- Multiple misalignment 일때 feedback 주기 어려움
- bounding box가 너무 루즈함