---
title: "[188] LLaVA-CoT: Let Vision Language Models Reason Step-by-Step"
date: 2024-12-02
tags: ['MLLM', '2024Q4']
paper: "https://arxiv.org/abs/2411.10440"
issue: 207
issueUrl: "https://github.com/long8v/PTIR/issues/207"
---

<img width="1117" alt="image" src="https://github.com/user-attachments/assets/70c99f82-503c-4cec-8ed0-1548b9fa79b9">

[paper](https://arxiv.org/abs/2411.10440), [code](https://github.com/PKU-YuanGroup/LLaVA-CoT), [dataset](https://huggingface.co/datasets/Xkev/LLaVA-CoT-100k)

## TL;DR
- **I read this because.. :** 추천 받아
- **task :** reasoning in LVLM
- **problem :** LVLM도 gpt-o1 처럼 reasoning 길게 하고 싶다
- **idea :** 데이터 넣고 학습하자. 대답의 단계를 나누자. 대답 단계 별로 beam search를 하자
- **architecture :** Llama 3.2V
- **objective :** CE loss (SFT 후 futher SFT)
- **baseline :** Llama 3.2V 
- **data :** Llava-CoT-100k (proposed)
- **evaluation :** mmstar, mmbench, mmvet, mathvista, ai2d, 
- **result :** 개선된 성능.
- **contribution :** 데이터 공개.

## Details
- thumbnail
<img width="506" alt="image" src="https://github.com/user-attachments/assets/24cbd569-106f-4509-b66f-48cad1f7f28f">

- inference examples
<img width="995" alt="image" src="https://github.com/user-attachments/assets/c597592a-c010-4e81-9b9f-fe18bb8f805d">

- 답변 구조화 방식
<img width="499" alt="image" src="https://github.com/user-attachments/assets/a1d31ac1-43a2-4629-98da-56a6ba82cac7">

GPT4o한테 생성시킨 뒤 구조를 안맞추는 것 Filtering. 
`<summary>`, `</summary>` 태그 안에 있는 것들을 Gt answer랑 비교해서 잘 답변한건지 필터링을 또 GPT4o한테 시킴
<img width="369" alt="image" src="https://github.com/user-attachments/assets/b70b6435-f941-434c-b730-770258a830a6">

<img width="375" alt="image" src="https://github.com/user-attachments/assets/19750790-9019-44a4-9b1a-8b9e8f6046d6">

- 생성한 이미지 소스
<img width="360" alt="image" src="https://github.com/user-attachments/assets/20b4d697-7137-4451-904c-7aae1452a53d">

https://github.com/long8v/PTIR/issues/203 얘랑 소스 겹침
<img width="250" alt="image" src="https://github.com/user-attachments/assets/ea6803af-7e51-4ba3-a023-10017eb39ef5">

- 각 구조에 대한 beam search 진행
<img width="758" alt="image" src="https://github.com/user-attachments/assets/a1bd349d-c5ab-4642-8702-0a705dc9c23a">

"beam search"라고 해서 몰랐는데 External verifier를 사용하는 형태인듯. 
이때 사용된 Prompt? 어떤 모델을 사용했는지 못봤음 
<img width="367" alt="image" src="https://github.com/user-attachments/assets/ae50b9cc-0c20-4c0f-a315-5f47c96f319e">

- Training hparam
<img width="327" alt="image" src="https://github.com/user-attachments/assets/df382379-2a97-42dc-bd3f-04847199bee8">


### Result
<img width="753" alt="image" src="https://github.com/user-attachments/assets/58aaeb90-3bbc-4b2a-80d3-eb05a7d158bc">

나름 "Reasoning 벤치마크"라는걸 선정.
direct training은 원래 vqa set으로 further SFT한 것. w/o structured tag는 `<summary>` 같은 태그 사용하지 않은 것
mmstar, mmvet, mathvista는 개선. ai2d는 그냥 Direct로 답변만 학습하는게 더 성능이 좋음

<img width="767" alt="image" src="https://github.com/user-attachments/assets/55498446-89d6-4d46-a3d4-55029dc98df7">

mmstar에서 세부 항목을 보면 reasoning 관련 세부항목과 math, science 등이 오름. perception은 안오르는건 아닌데 미미함.

- stage level beam search
<img width="744" alt="image" src="https://github.com/user-attachments/assets/ced8c521-fc62-4d94-88c9-d047b3e82187">

RM 학습 했다고 하는 얘기 없는데 BoN은 어떻게 한걸까? 
<img width="760" alt="image" src="https://github.com/user-attachments/assets/48418500-d017-47c2-9099-b029b75abe28">

- comparison with other models
<img width="767" alt="image" src="https://github.com/user-attachments/assets/30304e55-936d-40aa-9a33-ff5b838ca83d">
