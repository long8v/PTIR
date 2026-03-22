---
title: "Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond"
date: 2023-12-26
tags: ['multilingual', 'alibaba', '2023Q3', 'MLLM', 'qwen']
paper: "https://arxiv.org/pdf/2308.12966.pdf"
issue: 156
issueUrl: "https://github.com/long8v/PTIR/issues/156"
summary: "Read a living paper... - multi-lingual lvlm"
---
<img width="1348" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a4c10265-a52e-4487-9050-f9129ff71490">

[paper](https://arxiv.org/pdf/2308.12966.pdf), [code](https://github.com/QwenLM/Qwen-VL) 

## TL;DR
- **I read this because.. :** Read thesis for a living...
- **task :** MLLM
- **problem :** multi-lingual MLLM that is also chinese. let's also do finegrained task(grounding)
- **IDEA:** Divide the training into three phases.
- **input/output :** image, text -> text
- **architecture :** ViT-G/14 + Q-former + Qwen-7B
- **objective :** CE loss
- **baseline :** Flamingo, UnifiedIO, Kosmos, BLIP-2, InstrcutBLIP, Shikra, Pix2Struct, ...
- **data :** captioning(LAION-en/zh, Datacomp, COYO, CC, SBU, COCO, in-house data), VQA(GQA, VGQA, VQAv2, DVQA, OCR-VQA, DocVQA, TextVQA, ChartQA, AI2D), Grounding(GRIT, VG, RefCOCO(+, g), OCR(synthDoG, Common Crawl...)), Pure-text (in-house)
- **evaluation :** benchmarks, instruction-following benchmarks(TouchStone, SEED, MME)
- **result :** sota
- **contribution :** multi-lingual lvlm 
- **etc. :** Is the filtering strategy important? I also used text only data, but it didn't import the training finished. Or maybe that contributed to better performance... It's hard because it's not ablated well in many ways.

## Details
- performance
<img width="1360" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/dce053f6-876d-4807-a2fc-fcc744436c05">

### architecture
<img width="486" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/87638c4d-0d1d-4deb-9838-b72fa6fed0e4">

256 was best
<img width="982" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5fd10d6e-7840-4f88-8ff6-775cc0be1f3a">

### Inputs / Outputs

<img width="766" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8eaa7b28-fe55-4f46-8c65-f3a47077f764">

That's a lot of extra instructions.
A special token like `<ref>` or `<box>` is used, and no special token is used for bbox coordinates.


### training pipeline
<img width="942" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4c43711f-2ab0-46ca-8e5d-0e5b006576b0">


- Changing hparam
<img width="922" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3b4d687b-ba6c-45e4-b05c-7dc31d31e8ae">

resolution up / seq len up 

- Datasets that vary by stage
#### pre-training stage
<img width="988" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/713333ff-6522-4963-9d4e-e76fffb353f4">

Interesting that COYO has the highest survival rate among alt-text types.
He said he only looked at the image once lol
This filtering rule is documented in detail in the appendix, but you can find it in the appendix as follows

<img width="757" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c073005a-f536-452b-a426-2af8f6d7b473">

You've left a very strong clip score.

#### Multi-task Pre-training

<img width="692" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a851c79d-0640-44f2-91e6-0e90c2fe9f26">

#### Supervised Finetuning
This is also not detailed, but it is said that manual annotation, model generation, benchmark data concatenation, and multi-turn are done (I think it's important...)
<img width="757" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/568f9da9-4210-40a2-9646-5b58e3905965">

## Result
Benchmark performance is omitted

### instruction following benchmark 
<img width="578" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e2a7a0b8-cfad-4d4a-9adc-7c4d2c5530d8">

### Few-shot ability 
<img width="757" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/697b1bde-999a-4caa-ad63-dcee9db2a1d8">



### text only benchmark
<img width="766" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/baa7b4cf-ccae-468b-a956-a5350aa3d1c9">

I used Qwen LM as a learned interim, for no other reason than they were both being developed at about the same time lol.