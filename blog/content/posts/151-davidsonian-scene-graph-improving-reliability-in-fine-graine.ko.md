---
title: "[139] Davidsonian Scene Graph: Improving Reliability in Fine-Grained Evaluation for Text-to-Image Generation"
date: 2023-12-11
tags: ['google', '2023Q4', 'evaluation', 'generation']
paper: "https://google.github.io/dsg/"
issue: 151
issueUrl: "https://github.com/long8v/PTIR/issues/151"
---
<img width="674" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d332ba46-bb1a-4872-8254-e92986331d22">

[paper](https://google.github.io/dsg/), [code](https://github.com/j-min/DSG)

## TL;DR
- **I read this because.. :** 페이스북에서 봤고 CLIP evaluation에 적용해볼 수 있지 않을까? 하고 읽음 
- **task :** evaluating faithfulness of image generation
- **problem :** CLIPScore는 style에 따라 scale이 일정하지 않고 해석가능하지 않음, QG/QA 기반은 복합질문(파란 문이 있니?) no일 때 뭐가 틀린지(문이 없는건지 파란 문이 없는건지) 해석이 어렵고 여러 질문이 있을 때 문은 없다고 해놓고 파란 문은 있다고 하는 등의 VQA model 자체의 error가 있음. 
- **idea :** 각각의 질문을 atomic하게 만들고 이 질문들끼리 graph로 만들어서 이의 parent가 no이면 이 child는 다 no이게 하자. 
- **input/output :** image + text -> graph(questions for node, semantics for its dependancy)
- **baseline :** QA/QG 
- **data :** [TIFA](https://arxiv.org/pdf/2303.11897.pdf) 등의 이전 evaluation data 기반으로 graph를 만든 DSG-1k 공개. 이걸 만든 방식은 image에 해당하는 text를 LLM을 통하여 1)  entity tuple로 만든 뒤 2) 이를 기반으로 question을 만들고 3) 각 tuple의 depedancy도 구함
- **evaluation :** 각 이미지의 question에 맞게 대답을 했는가?
- **result :** 위의 문제를 해결 했다는 듯. VLM 모델 중에서는 PALI가 가장 우수한 성적 
- **contribution :** fine-grained한 evaluation을 좀 더 해석 가능하게 한 QG/A 기반의 evaluation을 개선
- **etc. :** 생각한 것과 좀 다르긴 함ㅋㅋ 별도의 QG / QA 모델을 사용해야된다는 점? 데이터셋이나 한번 살펴봐야되나. 그리고 문득 궁금해졌는데 GPT4-V와 같은 애들한테 "is `<description>` well explained `<img>`?, what is wrong?" 하면 뭐가 나오려나?

## Details
### QA/G based methodology
<img width="669" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f02bdc44-9980-4b2a-8155-bf200f82eee1">


### motivation
- problem of clip score 
<img width="669" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b3ee93d4-d6fb-40a8-90f3-b7c721416728">

- problem of QA/G method
<img width="697" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5778440b-0d2d-477e-8744-9f5ba58f9215">

### Proposed
<img width="657" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/500ee4ad-3912-4137-95af-b871d4416c0f">

### Dataset source
<img width="660" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/60fd4d0c-81e6-4890-bc35-d40ac98a85fb">

<img width="969" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c0d35249-ebfb-4391-a7f5-efe024945859">

뭐 많은데 시간이 없어서 .. 이만..