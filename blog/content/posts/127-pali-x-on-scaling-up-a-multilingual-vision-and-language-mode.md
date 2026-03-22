---
title: "PaLI-X: On Scaling up a Multilingual Vision and Language Model"
date: 2023-06-08
tags: ['multimodal', 'google', '2023Q2']
paper: "https://arxiv.org/pdf/2305.18565.pdf"
issue: 127
issueUrl: "https://github.com/long8v/PTIR/issues/127"
summary: "Much talked about - scaling PALI"
---
<img width="801" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/28109933-a6f4-4ca3-96d5-57878e17c80b">

[paper](https://arxiv.org/pdf/2305.18565.pdf)

## TL;DR
- **I read this because.. :** It's been mentioned a lot, so I thought I'd give it a try.
- **task :** object detection, captioning, VQA, text VQA, ...
- **problem :** Let's grow VLMs like we did LLMs.
- **idea :** raise vision from ViT-e (3.9B) to ViT (22B), language model from mT5-xxl (13B) to UL2 (35B)
- **input/output :** image / text -> text (or visual token for BeiT objective)
- **architecture :** ViT + UL2 like encoder-decoder image patch with text as input.
- **objective :** (a) span corruption (b) split-captioning (c) captioning (d) VQA (e) VQG (f) VQA with objective aware (g) captioning on Eposodic WebLI (h) pix2struct objective (i) captioning on short video (j) BeiT-like image-token prediction
- **baseline :** PALI, Flamingo, GIT 
- **data :** CC3M, WebLI(proposed in PaLI), VQ2A-CC3M,  ...
- **evaluation :** each...
- **result :** sota with finetuning on 25+ VLM benchmarks.
- **contribution :** scaling PALI
- **etc. :**

## Details
### Related Work
- Mixture of Denoiser
proposed in UL2. https://arxiv.org/pdf/2205.05131.pdf
<img width="1035" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/62d761cd-3b6e-4312-8479-9b0c5e667cbe">

<img width="1010" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6dc35044-54af-4667-ba17-1ad7783e8c8d">

A methodology to give prefixes to multiple pretraining tasks to be trained at once and have the model act on them. Not necessarily multiple architectures like MoE.

- PALI
https://arxiv.org/abs/2209.06794

Papers that tend to focus a bit more on multilingual~.
<img width="764" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0e29693d-76b6-431b-845e-8992197ba3b7">
It looks like it's just pushing a visual token as input. No pooling?

Learning ViT-e. Performance gains were marginal when scaling on ImageNet, but significant on multi-modal.
<img width="777" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e6e5bc3c-c7d9-42ae-b8b7-751a40436038">

<img width="481" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4cfbdbbf-25be-434a-acf2-9d9e5b879cfe">


PALI full size is this
<img width="556" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/92266117-53a0-4f88-b35e-98cefddccc4d">


For the same size parameter increase, performance improvement was better for the visual model than the language model
<img width="571" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1041720d-614f-4145-a1ea-937e8c1dd953">


WebLI is multi-modal to do well with images created on the web.
- 10 billion images and 12 billion alt-texts
- from English-only datasets to 109 languages
- use publicly available automatic service to extract OCR annotations on all images, resulting in 29 billion image-OCR pairs
It's like alt-text + ocr from image... not m3w style after all.

<img width="773" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/cb0f0ca0-5a3d-4f66-8dfb-f50dcf43a4cf">


ablation for each objective
<img width="756" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/38decc86-44bb-43ce-b636-1d7e0cb4575a">

mixing ratio
<img width="911" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/15dec7c3-2f17-4336-beaf-1762cec6e47f">

As a limitation 1) I lost multilingual ability in some benchmarks when I finetune with english only 2) I'm not sure if I'm evaluating synonyms well since the benchmarks are in english
<img width="798" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9a8273fb-5a30-46ed-81b3-2ee1b520db1d">


- PreSTU: pretraining for scene-text understanding
https://arxiv.org/pdf/2209.05534.pdf
Propose a 'split-ocr' task that just feeds input up to the mth token and ocr read from the (m+1)th

- object aware task
https://arxiv.org/pdf/2209.04372.pdf

<img width="451" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0eac3956-0961-415a-98ee-980fe0556a2a">

Asking "Are there specific objects in this image?

<img width="585" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/55979b48-a837-4dc1-841c-28b85cdd1918">

Adding objective-aware improved overall performance. -> Visual Question Answering, visual entailment and captioning.

- Said to have created qa with the VQ2A method
https://arxiv.org/pdf/2205.01883.pdf
How to create QA with captions
<img width="803" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ec973759-fdc0-4447-9f8d-39ffdfc87cd6">

- The configuration looks like this
- Candidate answer: POS-based
  - question gerenation : T5-XXL model and further fine-tune it on SQuAD1.1
  - Question-Answer Filtering : If the answer does not match the answer candidate offered as input to the question generation model, the generated question is discarded. / T5-XXL model and further fine-tune it on SQuAD1.1 and Natural Questions.
- least-to-most prompting
<img width="851" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/30d02b3e-b35f-450f-8ef7-1cfa91a0d2e5">

Research shows that students thrive when you break down a difficult question into smaller chunks and prompt them to work through the answer.
I'm not sure if it's tuning for CoT, learning to decompose, or something else.

## Model
<img width="747" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2ea0d219-8b46-46da-891b-01d5f468e37b">
This is a few-shot example, but the model architecture hasn't changed from PALI
- The language model is UL2 variants 32B. First, the language encoder-decoder is a bit bigger (previously 13B)
- visual model wrote 22B Scaling vision transformers to 22 billion parameters. https://arxiv.org/pdf/2302.05442.pdf
- And there seems to be a high-resolution phase, which I'll explain below.

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

