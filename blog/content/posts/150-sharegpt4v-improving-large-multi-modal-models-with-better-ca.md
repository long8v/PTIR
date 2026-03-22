---
title: "ShareGPT4V: Improving Large Multi-Modal Models with Better Captions"
date: 2023-12-08
tags: ['multimodal', 'dataset', '2023Q4', 'MLLM']
paper: "https://arxiv.org/abs/2311.12793"
issue: 150
issueUrl: "https://github.com/long8v/PTIR/issues/150"
summary: "Models trained with data using GPT4-V - Data release. Model disclosure. Emphasizing that data is more important than architecture!!!"
---
<img width="1114" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/09ee2d4b-2176-4a5a-92b2-b919c04f5799">

[paper](https://arxiv.org/abs/2311.12793), [page](https://sharegpt4v.github.io/)

## TL;DR
- **I read this because.. :** Models trained with data using GPT4-V
- **task :** VLM 
- **problem :** instruction data is too noisy
- **idea :** Let's collect data with GPT4-V! Later, we'll use the captioner training to align her with the kids that came out.
- **input/output :** image - (api call) -> GPT4V caption => Learn with LLaVA1.5 style
- **architecture :** LLaVA-1.5
- **objective :** ce loss
- **baseline :** To see the effect of the data, I trained by adding to LLaVA-7B / LLaVA-1.5-7B(13B) / Qwen-VL-Chat-7B, taking the LLaVA 1.5 architecture as it is, changing some training details and pretraining - finetuning, in all cases sota
- **data :** image={LAION-400M, COCO, SBU, SAM, TextCaps}, text={GPT4-V call}
- **evaluation :** SEED, VizWiz, VQA-v2, SQA, QBench, MM-Vet, MMBench-CN, MMBench, MME_cog, MME_per, LLaVA-Bench
- **result :** sota~
- **contribution :** Data disclosure. Model disclosure. Emphasize that data is more important than architecture!!!
- **etc. :**

## Details
- thumnail (caption example / performance)
<img width="1092" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/59efaed8-0c71-4394-a3cb-198fec416f4a">

- caption style / error
<img width="1111" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4911091c-371d-4908-ba68-af083da05c03">


### Data 
- dataset statistics
<img width="542" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c45d0a5b-0588-45a3-b918-27f688a673ca">

etc: SAM, TextCaps, WikiArt + 1K images from webcrawled data (split evenly between images of landmarks and images of celebrities). (scratched)

- data collection
<img width="1091" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1e76bb98-85c4-4331-9734-1a81238f4e3e">

<img width="417" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/014d2cc1-68e4-4cd7-af56-4b0dfd2f47f6">

Different types of data prompted differently
<img width="930" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a87fccd7-1dfe-499e-ab1e-0a0d26c634f6">


Collect 100K like this

- ShareGPT4V-PT
Create a separate model called ShareCaptioner to create a 1.2M dataset.
44 A100 GPU days said to have taken. There is no information about the model, so I wonder if it is the same as the ShareGPT4V-7B model?
No information about further refinement.

The data we used
<img width="414" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ba079be9-9d89-43c5-bdce-7bffb0c0e1af">

Human evaluation of 3
<img width="327" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d309a6f2-0543-4eb7-9a06-9773273d0558">

more analysis
<img width="335" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0d413c43-7308-434c-8c6b-646fa0554678">

<img width="328" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a624e730-8411-48ff-a6e9-89f9c83c7afa">

- Improving model performance for this dataset
<img width="673" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4c67c78f-3a94-459f-b7f6-481f1c9aec6a">

To make a fair comparison, we subtracted 100K of data for "detailed caption" from the original data recipe they were training on and put this data in

### ShareGPT4V-7B model
- LLaVA-1.5
- ViT-L/14 336x336 / Vicuna-v1.5 7B 
- training
  - pretraining:
    - w/ ShareGPT4V-PT
- image encoder (only learn the latter half) + projector + llm all finetune
    - bs 256 / 4700 steps
  - supervised finetuning:
- LLaVA contains 23k of detailed captions, which we sample from ShareGPT4V.
- vision encoder freeze / projector with llm finetune

<img width="1093" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/145cbcf0-c99c-45cd-bc63-16cd97f8a276">

### Ablations 
The effect of training with each piece of data

<img width="416" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/65c5a3d3-6f98-4b3a-b7b9-6962a397d406">

The effect of learning only the latter half
<img width="342" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3cf18820-8cbf-4d30-9827-b6fc422c9d17">

<img width="415" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6a4d03bf-36f0-49da-9cff-1830af32dc5e">


