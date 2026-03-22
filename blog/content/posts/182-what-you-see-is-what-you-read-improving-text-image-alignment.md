---
title: "What You See is What You Read? Improving Text-Image Alignment Evaluation"
date: 2024-07-18
tags: ['google', 'NeurIPS', '2023Q2', 'evaluation']
paper: "https://arxiv.org/abs/2305.10400"
issue: 182
issueUrl: "https://github.com/long8v/PTIR/issues/182"
summary: "Predecessor of #169. - Like the first VQ^2? I don't know if it came out at the same time as TIFA."
---
<img width="703" alt="image" src="https://github.com/user-attachments/assets/1d9d6ba8-a1fc-440e-a52c-e07a5f3dc045">

[paper](https://arxiv.org/abs/2305.10400)

## TL;DR
- **I read this because.. :** #169's predecessor.
- **task :** text-to-image alignment evaluation
- **problem :** When evaluating text-to-image and image-to-text generation models, it is important to ensure that the two images and text are semantically aligned.
- **idea :** (zs) LLM + VQA pipeline proposal / (finetune) VNLI model
- **input/output :** {image, text} -> score
- **architecture :** VQ^2(spacy, T5-XXL, PALI-17B), VNLI(BLIP2, PALI-17B)
- **baseline :** CLIP, BLIP, BLIP2, PALI, TIFA
- **data :** 44K dataset created with Congen for training VNLI
- **evaluation :** SeeTrue Benchmark(proposed) -> AUC ROC 
- **result :** Better than TIFA
- **contribution :** VQ^2 as if it were the first? I don't know if it came out at the same time as TIFA.

## Details
<img width="885" alt="image" src="https://github.com/user-attachments/assets/05a44b5a-cdab-4c76-9cda-d61a5fc53882">

### Proposed SeeTRUE benchmark
<img width="756" alt="image" src="https://github.com/user-attachments/assets/01425432-e5df-4bb4-bf20-e9ef77e95c37">

- EditBench: created here. Made with SD v1.4 and 2.1 with COCO caption and drawbench's caption
- COCO-Con: A contradiction caption created with the ConGen method below for COCO captions.
- PickaPic-Con: Caption your PickaPic images with BLIP2

### SeeTrue generation
<img width="785" alt="image" src="https://github.com/user-attachments/assets/a0934e31-cd80-404b-aeac-02a27431d841">

- ConGen: Ask the PaLM model to create contradict captions and then use the NLI model to adopt the one with the highest contradiction score.

### VQ^2
Create an answer first, use a question generation (QG) model, and filter with a QA model. Then ask the question to the VQA model, and the VQA answer scores the answer by averaging the confidence of the answer.
<img width="766" alt="image" src="https://github.com/user-attachments/assets/cc3abe42-3f9d-429a-baca-0415deefdfb8">

- answer span is created by SpaCy's POS + dependency parse tree
- QG uses the T5-XXL
- QA model is T5-XXL trained with SQuAD2.0 and Natural Question
- The VQA model is the PALI-17B

### E2E VNLI model
Additional training of BLIP2, PALI-17B with 44K of data generated with ConGen

## Result
<img width="778" alt="image" src="https://github.com/user-attachments/assets/c1d29a2b-ce77-4184-bd6e-46cb726fd8c0">

- winoground result
<img width="782" alt="image" src="https://github.com/user-attachments/assets/0167dfd4-e917-4c20-8fe9-abfd1452448a">

- correlation with human
<img width="753" alt="image" src="https://github.com/user-attachments/assets/6511f0c4-2dfb-4490-9337-58b85e259ce2">

- Can also be used for rerank
<img width="758" alt="image" src="https://github.com/user-attachments/assets/c0a5ffc2-20bf-40f6-a737-cadcf25ccb29">
