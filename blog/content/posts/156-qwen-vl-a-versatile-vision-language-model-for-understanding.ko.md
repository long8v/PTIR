---
title: "[144] Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond"
date: 2023-12-26
tags: ['multilingual', 'alibaba', '2023Q3', 'MLLM', 'qwen']
paper: "https://arxiv.org/pdf/2308.12966.pdf"
issue: 156
issueUrl: "https://github.com/long8v/PTIR/issues/156"
---
<img width="1348" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a4c10265-a52e-4487-9050-f9129ff71490">

[paper](https://arxiv.org/pdf/2308.12966.pdf), [code](https://github.com/QwenLM/Qwen-VL) 

## TL;DR
- **I read this because.. :** 생계형 논문 읽기..
- **task :** MLLM
- **problem :** chinese도 되는 multi-lingual MLLM. finegrained task(grounding)도 하자 
- **idea :** training 단계를 세개로 나눠서 학습. 
- **input/output :** image, text -> text
- **architecture :** ViT-G/14 + Q-former + Qwen-7B
- **objective :** CE loss
- **baseline :** Flamingo, UnifiedIO, Kosmos, BLIP-2, InstrcutBLIP, Shikra, Pix2Struct, ...
- **data :** captioning(LAION-en/zh, Datacomp, COYO, CC, SBU, COCO, in-house data), VQA(GQA, VGQA, VQAv2, DVQA, OCR-VQA, DocVQA, TextVQA, ChartQA, AI2D), Grounding(GRIT, VG, RefCOCO(+, g), OCR(synthDoG, Common Crawl...)), Pure-text (in-house)
- **evaluation :** benchmarks, instruction-following benchmarks(TouchStone, SEED, MME)
- **result :** sota
- **contribution :** multi-lingual lvlm 
- **etc. :** filtering 전략이 중요한건가? text only data도 썼는데 학습이 다 완료된걸 안가져와서.. 아닌가 그게 오히려 성능 더 좋아지는데 기여했나.. 여러모로 뭔가 ablation이 잘안돼서 어렵군 

## Details
- performance
<img width="1360" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/dce053f6-876d-4807-a2fc-fcc744436c05">

### architecture
<img width="486" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/87638c4d-0d1d-4deb-9838-b72fa6fed0e4">

256이 가장 좋았다고 함 
<img width="982" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5fd10d6e-7840-4f88-8ff6-775cc0be1f3a">

### Inputs / Outputs

<img width="766" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8eaa7b28-fe55-4f46-8c65-f3a47077f764">

별도의 instruction이 크게 안쓰였군.
`<ref>`나 `<box>`같은 special token이 쓰였고 안에 bbox 좌표 같은건 따로 스페셜 토큰 안썼다고 함 


### training pipeline
<img width="942" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4c43711f-2ab0-46ca-8e5d-0e5b006576b0">


- 달라지는 hparam
<img width="922" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3b4d687b-ba6c-45e4-b05c-7dc31d31e8ae">

resolution up / seq len up 

- stage마다 달라지는 데이터셋 
#### pre-training stage
<img width="988" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/713333ff-6522-4963-9d4e-e76fffb353f4">

COYO가 alt-text류 중에 가장 살아남은 비율이 높은게 흥미롭군
딱 이미지 한번씩만 봤다고 함 ㅋㅋ
이 filtering rule은 자세하게 안적혀있는데 appendix에서 아래와 같이 

<img width="757" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c073005a-f536-452b-a426-2af8f6d7b473">

clip score를 아주 강하게 남겼다고 하넹..

#### Multi-task Pre-training

<img width="692" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a851c79d-0640-44f2-91e6-0e90c2fe9f26">

#### Supervised Finetuning
이것도 자세히 안나와 있는데 manual annotation, model generation, 벤치마크 데이터 concat해가지고 multi-turn으로 만들었다고 함 (중요한 것 같은데.. ㅜㅜ)
<img width="757" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/568f9da9-4210-40a2-9646-5b58e3905965">

## Result
벤치마크 성능들은 생략 

### instruction following benchmark 
<img width="578" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e2a7a0b8-cfad-4d4a-9adc-7c4d2c5530d8">

### Few-shot ability 
<img width="757" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/697b1bde-999a-4caa-ad63-dcee9db2a1d8">



### text only benchmark
<img width="766" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/baa7b4cf-ccae-468b-a956-a5350aa3d1c9">

Qwen LM을 학습된 중간 껄 썼는데 다른 이유는 없고 그냥 둘이 거의 동시에 개발중이었다고 ㅋㅋ 