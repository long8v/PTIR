---
title: "[163] What You See is What You Read? Improving Text-Image Alignment Evaluation"
date: 2024-07-18
tags: ['google', 'NeurIPS', '2023Q2', 'evaluation']
paper: "https://arxiv.org/abs/2305.10400"
issue: 182
issueUrl: "https://github.com/long8v/PTIR/issues/182"
---
<img width="703" alt="image" src="https://github.com/user-attachments/assets/1d9d6ba8-a1fc-440e-a52c-e07a5f3dc045">

[paper](https://arxiv.org/abs/2305.10400)

## TL;DR
- **I read this because.. :** #169 의 전작. 
- **task :** text-to-image alignment evaluation
- **problem :** text-to-image, image-to-text generation 모델을 평가하는데 두 이미지와 텍스트가 semantic하게 잘 align됐는지 확인하는건 중요하다.
- **idea :** (zs) LLM + VQA 파이프라인 제안 / (finetune) VNLI model
- **input/output :** {image, text} -> score
- **architecture :** VQ^2(spacy, T5-XXL, PALI-17B), VNLI(BLIP2, PALI-17B)
- **baseline :** CLIP, BLIP, BLIP2, PALI, TIFA
- **data :** VNLI 학습용으로 44K 데이터셋 Congen으로 만듦
- **evaluation :** SeeTrue Benchmark(proposed) -> AUC ROC 
- **result :** TIFA보다 좋음 
- **contribution :** VQ^2를 처음 낸듯? TIFA랑 동시대에 나왔나 모르겠음.

## Details
<img width="885" alt="image" src="https://github.com/user-attachments/assets/05a44b5a-cdab-4c76-9cda-d61a5fc53882">

### Proposed SeeTRUE benchmark
<img width="756" alt="image" src="https://github.com/user-attachments/assets/01425432-e5df-4bb4-bf20-e9ef77e95c37">

- EditBench : 여기서 만든 것. COCO caption과 drawbench의 캡션을 가지고 SD v1.4와 2.1로 만듦
- COCO-Con : COCO 캡션에 대해서 아래의 ConGen 방법으로 contradiction caption을 만든 것
- PickaPic-Con : PickaPic image에 BLIP2로 캡션 단것 

### SeeTrue generation
<img width="785" alt="image" src="https://github.com/user-attachments/assets/a0934e31-cd80-404b-aeac-02a27431d841">

- ConGen : PaLM 모델에게 contradict caption을 만들라고 한 뒤에 NLI model을 사용해서 가장 contradiction score가 높은 걸 채택. 

### VQ^2
answer를 먼저 만들고 question generation(QG) model을 사용하고 QA model로 필터링. 이후 VQA model에 질답을 한 뒤에 VQA 대답이 answer의 confidence를 평균을 내서 점수 매김 
<img width="766" alt="image" src="https://github.com/user-attachments/assets/cc3abe42-3f9d-429a-baca-0415deefdfb8">

- answer span만드는건 SpaCy의 POS + dependancy parse tree
- QG는 SQuAD1.1에서 학습된 T5-XXL
- QA 모델은 SQuAD2.0과 Natural Question으로 학습된 T5-XXL
- VQA 모델은 PALI-17B

### E2E VNLI model
BLIP2, PALI-17B를 ConGen으로 생성한 44K의 데이터로 추가학습

## Result
<img width="778" alt="image" src="https://github.com/user-attachments/assets/c1d29a2b-ce77-4184-bd6e-46cb726fd8c0">

- winoground result
<img width="782" alt="image" src="https://github.com/user-attachments/assets/0167dfd4-e917-4c20-8fe9-abfd1452448a">

- human과의 correlation
<img width="753" alt="image" src="https://github.com/user-attachments/assets/6511f0c4-2dfb-4490-9337-58b85e259ce2">

- rerank에도 쓰일 수 있다
<img width="758" alt="image" src="https://github.com/user-attachments/assets/c0a5ffc2-20bf-40f6-a737-cadcf25ccb29">
