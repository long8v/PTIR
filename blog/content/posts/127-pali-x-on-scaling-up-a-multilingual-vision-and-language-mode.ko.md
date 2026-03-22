---
title: "[118] PaLI-X: On Scaling up a Multilingual Vision and Language Model"
date: 2023-06-08
tags: ['multimodal', 'google', '2023Q2']
paper: "https://arxiv.org/pdf/2305.18565.pdf"
issue: 127
issueUrl: "https://github.com/long8v/PTIR/issues/127"
---
<img width="801" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/28109933-a6f4-4ca3-96d5-57878e17c80b">

[paper](https://arxiv.org/pdf/2305.18565.pdf)

## TL;DR
- **I read this because.. :** 많이 언급되어 
- **task :** object detection, captioning, VQA, text VQA, ...
- **problem :** LLM 한거처럼 VLM도 키우자
- **idea :** vision도 ViT-e(3.9B)에서 ViT(22B)로 키우고 language model도 mT5-xxl(13B)에서 UL2(35B)
- **input/output :** image / text -> text (or visual token for BeiT objective)
- **architecture :** ViT + UL2 like encoder-decoder image patch가 text랑 input으로 같이 들어가는 형태. 
- **objective :** (a) span corruption (b) split-captioning (c) captioning (d) VQA (e) VQG (f) VQA with objective aware (g) captioning on Eposodic WebLI (h) pix2struct objective (i) captioning on short video (j) BeiT-like image-token prediction
- **baseline :** PALI, Flamingo, GIT 
- **data :** CC3M, WebLI(proposed in PaLI), VQ2A-CC3M,  ...
- **evaluation :** 각각..
- **result :** 25+ VLM benchmark에서 finetuning으로 sota.
- **contribution :** scaling PALI
- **etc. :**

## Details
### Related Work
- Mixture of Denoiser
proposed in UL2. https://arxiv.org/pdf/2205.05131.pdf
<img width="1035" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/62d761cd-3b6e-4312-8479-9b0c5e667cbe">

<img width="1010" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6dc35044-54af-4667-ba17-1ad7783e8c8d">

여러 종류의 pretraining task를 한번에 학습할건데 prefix를 주고 모델이 이에 맞게 행동하도록 하는 방법론. MoE처럼 아키텍쳐가 여러개고 그런건 아님

- PALI
https://arxiv.org/abs/2209.06794

일단 multilingual에 좀 집중한 경향이 있는 논문~
<img width="764" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0e29693d-76b6-431b-845e-8992197ba3b7">
그냥 visual token을 input으로 밀어넣는 형태인듯 하다. pooling을 안썼다고?

ViT-e를 학습. ImageNet에서는 scaling 했을 때 성능의 향상이 marginal 했지만 multi-modal에서는 유의미한 성능
<img width="777" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e6e5bc3c-c7d9-42ae-b8b7-751a40436038">

<img width="481" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4cfbdbbf-25be-434a-acf2-9d9e5b879cfe">


PALI 전체 크기는 이러하다다
<img width="556" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/92266117-53a0-4f88-b35e-98cefddccc4d">


같은 크기의 파라미터 증가에서 성능 개선이 language model 보다 visual model 쪽이 효과가 더 좋았다고 함
<img width="571" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1041720d-614f-4145-a1ea-937e8c1dd953">


WebLI는 multi-modal 잘하기 위해서 web에서 만든 이미지. 
- 10 billion images and 12 billion alt-texts
- from English-only datasets to 109 languages
- use publicly available automatic service to extract OCR annotations on all images, resulting in 29 billion image-OCR pairs
결국 alt-text + ocr from image인듯.. m3w style은 아닌걸루

<img width="773" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/cb0f0ca0-5a3d-4f66-8dfb-f50dcf43a4cf">


각 objective에 대한 ablation 
<img width="756" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/38decc86-44bb-43ce-b636-1d7e0cb4575a">

mixing ratio
<img width="911" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/15dec7c3-2f17-4336-beaf-1762cec6e47f">

limitation으로 1) english only로 finetune을 했을 때 multilingual 능력을 일부 벤치마크에서 잃어버리더라 2) benchmark가 english라서 동의어를 잘 평가하고 있는지 잘 모르겠다
<img width="798" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9a8273fb-5a30-46ed-81b3-2ee1b520db1d">


- PreSTU: pretraining for scene-text understanding
https://arxiv.org/pdf/2209.05534.pdf
그냥 m번째 토큰까지 input에 주고 (m+1)번째부터 ocr read해라 하는 'split-ocr' task 제안

- object aware task
https://arxiv.org/pdf/2209.04372.pdf

<img width="451" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0eac3956-0961-415a-98ee-980fe0556a2a">

이 이미지에 특정 object들 있냐?하고 물어봄

<img width="585" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/55979b48-a837-4dc1-841c-28b85cdd1918">

objective-aware를 넣었을 때 전체적인 성능이 향상 됐다. -> Visual Question Answering, visual entailment and captioning.

- VQ2A 방법으로 qa를 만들었다고함 
https://arxiv.org/pdf/2205.01883.pdf
caption으로 QA를 만드는 방법론
<img width="803" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ec973759-fdc0-4447-9f8d-39ffdfc87cd6">

- 구성은 아래와 같음
  -  candidate answer : POS 기반
  - question gerenation : T5-XXL model and further fine-tune it on SQuAD1.1
  - Question-Answer Filtering : If the answer does not match the answer candidate offered as input to the question generation model, the generated question is discarded. / T5-XXL model and further fine-tune it on SQuAD1.1 and Natural Questions.
- least-to-most prompting
<img width="851" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/30d02b3e-b35f-450f-8ef7-1cfa91a0d2e5">

어려운 질문을 작은 단위의 질문으로 나누고 답변을 풀어나가는 과정을 prompt에 넣어주면 잘한다~는 연구
CoT를 위한 tuning을 한건지? decompose 하는걸 학습을 하는건지 어떤건지 잘 모르겠

## Model
<img width="747" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2ea0d219-8b46-46da-891b-01d5f468e37b">
이건 few-shot 예시긴 한데 모델 아키텍쳐는 PALI랑 달라진 건 없다
- language model이 UL2 varaints 32B라고. 일단 language encoder-decoder가 좀 더 커졌네(이전에 13B)
- visual model은 22B 썼다고 Scaling vision transformers to 22 billion parameters. https://arxiv.org/pdf/2302.05442.pdf
- 그리고 밑에 설명할 high-resolution phase가 있는게 다른 것 같음

## Training objectives
<img width="739" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/eba5007d-7c3c-4aa4-bcc2-a9288a0f38e6">

## Training procedure
In stage 1, the visual encoder (after mixed-objective training) is kept frozen, while the rest of the parameters are trained on a total of 2.2B examples at the base resolution 224×224 (native to ViT-22B), using the entire mixture. In stage 2, it continues training using only the OCR-related objectives (pix2struct and split-ocr) plus the object detection objective; this is done in several substages, during which image resolution is gradually increased to 448×448, 672×672 and finally 756×756.

## Result
<img width="785" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2ed59085-c846-48ed-8355-b96a03bfe443">

### Per-task finetuning
<img width="800" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a483cea5-af4b-4ae5-ab10-4139ef1ffd8c">

### Multi-task finetuning
<img width="742" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/00d6ffe8-9e25-44bd-8ebb-6f74a175a4a9">

### Few-shot performance
<img width="733" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5e8665d0-2469-494c-8fea-028188c6bff1">

### zero-shot detection
<img width="764" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/680afc88-af26-4591-9258-f9a4ee981de7">

