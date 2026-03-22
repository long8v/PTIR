---
title: "[148] I Can't Believe There's No Images! Learning Visual Tasks Using only Language Supervision"
date: 2024-02-11
tags: ['ICCV', '25min', 'CLIP', '2023Q3', 'AI2']
paper: "https://arxiv.org/pdf/2211.09778.pdf"
issue: 160
issueUrl: "https://github.com/long8v/PTIR/issues/160"
---
<img width="793" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/acaab25d-c99b-48b1-b999-aa29bcf5022f">

[paper](https://arxiv.org/pdf/2211.09778.pdf)

## TL;DR
- **I read this because.. :** aka. CLOSE. 카카오 논문 찾으려고 ICCV 탐방기 PPT 보다가 CapDec이랑 되게 비슷해서 뭐가 다른가 하고 읽음.
- **task :** zero-shot cross modal transfer(특정 modality에서 학습한걸 가지고 다른 모달리티로 전환하는 것)
- **problem :** contrastive로 학습되더라도 text와 image의 embedding space는 다르다! 가령 COCO caption에 대해서 positive {image, text} pair의 similiarity는 0.26이고 관련 없는 caption 끼리의 유사도는 0.35이다. 
- **idea :** text embedding space에 gaussian noise를 추가하자!
- **input/output :** (train) text -> text (infer) image, text -> text
- **architecture :** CLIP ViT-L/14 + T5 base 
- **objective :** cross entropy loss
- **baseline :** ESPER, CLIP Cls, TAP-C (zero-shot multimodal transfer models)
- **data :** COCO Captioning, SNLI (->SNLI-VE), VQA (->VQA-E), Visual News, synthetic captions with GPT-J RNG, GPT-J unigram, CURIE
- **evaluation :** 각 벤치마크에 맞게 
- **result :** 기존 text only로 학습된 멀티모달 모델들 중 sota. 
- **contribution :** 간단한 아이디어로 안되던걸 되게 함. 
- **etc. :** 결론적으로 CapDec이랑 매우 비슷함 ㅋㅋ 얘네 related work에도 있고 그래서 이런저런 analysis를 넣게 된 듯. VLM에서 이런 식으로 학습하면 더 scalable하게 학습 할 수 있으려나? 또는 이게 그냥 LLaVA의 방식과 같다고 할 수 있으려나?

## Details
- pipeline
<img width="916" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7ef78e8e-309e-4786-a7e8-0a88d6b86d9f">

텍스트 임베딩도 CLIP에서 나온걸 씀! VQA에서 context라던지, SNLI에서 premise 같은것들은 T5 임베딩 씀. 
어떻게 벡터로 넣어줬는지 좀 애매하게 써져있는데 CLIP에서 나온 임베딩이 2048이고 T5가 받는 임베딩이 512이면 2048 임베딩을 잘라서 4개의 512 벡터로 바꿔서 넣어줬다는 듯

<img width="436" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9fc12ede-f3ef-4851-8c55-c07205e7a2c6">

CLIP의 image / text encoder는 freeze하고 T5만 finetune하는 형태 

- modality adaptor
<img width="980" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/649ac712-d45f-45ae-8001-20288182c50a">

결론적으로 가우시안 노이즈 + training hyperparameter w로 scale을 함. 

<img width="490" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5a9c519d-051d-45f2-ad37-74cd4535728c">

- sensitivitiy 
<img width="496" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/09eb29fb-80d7-47f1-9943-f3fa2be24a78">

text 벡터에 약간의 noise를 주는 건 민감하지 않았고 이미지 방향으로 조금 shift시키는 것(mean)은 VE의 경우 performance가 좋아지기도 했으나 반대 방향으로 가게 하는 것은(-mean) 성능에 악영향을 주었다.

 - learned adpater analysis
<img width="483" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6f5c04e2-545d-4d58-96ed-5dbaad482aae">

zero gaussian이 best는 아니므로 더 나은 adaptor가 있을까 학습. 대신 이건 text-only로 학습이 안되므로 main모델로는 못들어감.
linear는 linear map을 학습하는 방식이고 cov.는 학습 가능한 text와 image의 covariance로 structured noise를 추가하는 방식임 

- training data with language model
<img width="422" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f59913fc-8d17-4190-a1a4-575267c6a1be">

GPT-J등을 써서 coco에 많이 나오는 단어들로 캡션 생성하게 해서 학습할 수 있음

- style caption도 할 수 있음
<img width="675" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8fc0b7d3-20f5-4b50-bb62-710e91e6ce88">


