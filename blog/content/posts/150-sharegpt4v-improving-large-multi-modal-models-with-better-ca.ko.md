---
title: "[138] ShareGPT4V: Improving Large Multi-Modal Models with Better Captions"
date: 2023-12-08
tags: ['multimodal', 'dataset', '2023Q4', 'MLLM']
paper: "https://arxiv.org/abs/2311.12793"
issue: 150
issueUrl: "https://github.com/long8v/PTIR/issues/150"
---
<img width="1114" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/09ee2d4b-2176-4a5a-92b2-b919c04f5799">

[paper](https://arxiv.org/abs/2311.12793), [page](https://sharegpt4v.github.io/)

## TL;DR
- **I read this because.. :** GPT4-V를 활용한 데이터로 학습한 모델 
- **task :** VLM 
- **problem :** instruction data가 너무 noisy하다
- **idea :** GPT4-V로 데이터 모으자! 후에 captioner 학습해서 나온 애들을 가지고 얘를 alignment 할 때 쓰자 
- **input/output :** image - (api call) -> GPT4V caption => LLaVA1.5 style로 학습
- **architecture :** LLaVA-1.5
- **objective :** ce loss
- **baseline :** 데이터의 효과를 보기 위해 LLaVA-7B / LLaVA-1.5-7B(13B) / Qwen-VL-Chat-7B에 추가하여 학습, LLaVA 1.5 아키텍쳐 그대로 가져와서 학습 디테일 조금 바꾸고 pretraining - finetuning 했을 때 모든 경우에서 sota
- **data :** image={LAION-400M, COCO, SBU, SAM, TextCaps}, text={GPT4-V call}
- **evaluation :** SEED, VizWiz, VQA-v2, SQA, QBench, MM-Vet, MMBench-CN, MMBench, MME_cog, MME_per, LLaVA-Bench
- **result :** sota~
- **contribution :** 데이터 공개. 모델 공개. 아키텍쳐보다 데이터가 중요하다!!!를 강조 
- **etc. :**

## Details
- thumnail (caption example / performance)
<img width="1092" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/59efaed8-0c71-4394-a3cb-198fec416f4a">

- caption style / error
<img width="1111" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4911091c-371d-4908-ba68-af083da05c03">


### Data 
- dataset statistics
<img width="542" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c45d0a5b-0588-45a3-b918-27f688a673ca">

etc: SAM, TextCaps, WikiArt + 1K images from webcrawled data (split evenly between images of landmarks and images of celebrities). (추가적으로 긁은 듯)

- data collection
<img width="1091" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1e76bb98-85c4-4331-9734-1a81238f4e3e">

<img width="417" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/014d2cc1-68e4-4cd7-af56-4b0dfd2f47f6">

데이터 종류별로 prompt를 다르게 줬다고 함
<img width="930" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a87fccd7-1dfe-499e-ab1e-0a0d26c634f6">


이렇게 100K수집 

- ShareGPT4V-PT
ShareCaptioner라는 모델을 따로 만들어서 1.2M 데이터셋을 만듦.   
44 A100 GPU days 걸렸다고 함. 모델에 대한 정보가 없는걸 봐서 ShareGPT4V-7B 모델이랑 같은것 아닐까?
자세하게 추가로 정제했다던지 하는 정보는 없음.

이때 사용한 데이터 
<img width="414" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ba079be9-9d89-43c5-bdce-7bffb0c0e1af">

3개에 대한 human evaluation
<img width="327" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d309a6f2-0543-4eb7-9a06-9773273d0558">

more analysis
<img width="335" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0d413c43-7308-434c-8c6b-646fa0554678">

<img width="328" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a624e730-8411-48ff-a6e9-89f9c83c7afa">

- 이 데이터셋에 대한 모델 성능 개선 
<img width="673" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4c67c78f-3a94-459f-b7f6-481f1c9aec6a">

공정한 비교를 위해 원래 쟤네 학습할 때 있었던 data recipe 중에 'detailed caption'에 해당하는 100K의 데이터를 빼고 이 데이터를 넣음

### ShareGPT4V-7B model
- LLaVA-1.5
- ViT-L/14 336x336 / Vicuna-v1.5 7B 
- training
  - pretraining:
    - w/ ShareGPT4V-PT
    - image encoder(latter half만 학습) + projector + llm all finetune 
    - bs 256 / 4700 steps
  - supervised finetuning:
    - LLaVA에서 detailed caption 23k가 들어가는데 이걸 ShareGPT4V에서 샘플링해서 사용
    - vision encoder freeze / projector와 llm finetune

<img width="1093" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/145cbcf0-c99c-45cd-bc63-16cd97f8a276">

### Ablations 
각 데이터를 넣어서 학습하는 것의 효과 

<img width="416" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/65c5a3d3-6f98-4b3a-b7b9-6962a397d406">

latter half만 학습한 것의 효과 
<img width="342" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3cf18820-8cbf-4d30-9827-b6fc422c9d17">

<img width="415" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6a4d03bf-36f0-49da-9cff-1830af32dc5e">


