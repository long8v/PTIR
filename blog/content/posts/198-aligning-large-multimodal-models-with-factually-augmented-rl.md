---
title: "Aligning Large Multimodal Models with Factually Augmented RLHF"
date: 2024-09-25
tags: ['25min', 'RL', '2023Q3', 'MLLM', 'Berkley']
paper: "https://arxiv.org/abs/2309.14525"
issue: 198
issueUrl: "https://github.com/long8v/PTIR/issues/198"
summary: "VLM RL Early Work. By PPO. - Almost the first study to attach RLHF to VLM."
---

<img width="648" alt="image" src="https://github.com/user-attachments/assets/4c2d8b52-6625-4961-b507-281693a33f54">

[paper](https://arxiv.org/abs/2309.14525), [code](https://github.com/llava-rlhf/LLaVA-RLHF)

## TL;DR
- **I read this because.. :** VLM RL early work. PPO 써서.
- **task :** VLM + RL
- Problem :** hallucination in VLM
- **idea :** Let's apply PPO! One difference is to add human annotations (captions, etc.) to the reward model.
- **input/output :** {image, question} -> answer
- **architecture :** LLaVA 7B (vicuna) 
- **objective :** PPO loss 
- **baseline :** OpenFlamingo, MiniGPT-4, InstructBLIP, LLaVA-SFT
- **data :** Create 10K samples with LLaVA SFT model and then create Human annotated preference data
- **evaluation :** MMBench, LLaVA-w, POPE, MMHal (proposed)
- **result :** Improved MMBench (finegrained perception)
- **contribution :** Almost the first study to attach RLHF to VLM
- **etc. :**

## Details

### Proposed
<img width="678" alt="image" src="https://github.com/user-attachments/assets/70830c97-2116-4e72-a909-0aec02087542">

- humna preference data collection
Create 10K of LLaVA held-out data for SFT model with temperature 0.7 (image source?)
When receiving human preference annotations, the Instruction
<img width="702" alt="image" src="https://github.com/user-attachments/assets/d21f4201-12d2-41b3-8339-5c228815360c">

Prompts to the RM model. additional captions, etc. do not factually augment augmented rlhf
<img width="663" alt="image" src="https://github.com/user-attachments/assets/5fe4c1d4-7bdc-4ee7-bde5-5f6d83beb043">

### MMHal-Bench 
Create 12 questions with 96 quantities and 8 categories (object attribute, adversairal object, comparison, counting, spatial relation, environment, holistic, others).
The image source is OpenImages and we give text-only GPT4 a human-generated answer about the image content, along with the category (presumably of Object) within the image. GPT4's evaluation results show 94% agreement with human.

### Result
- LLaVA bench
<img width="693" alt="image" src="https://github.com/user-attachments/assets/c4d1d9e1-e5ee-4bbb-8ab6-0bd38a319862">

- mmhal bench
<img width="665" alt="image" src="https://github.com/user-attachments/assets/bd47e34c-e12f-4fc9-b7a2-8597a6967acd">

- mmbench 
 
<img width="680" alt="image" src="https://github.com/user-attachments/assets/d2cd9e6c-bca3-41ee-a48c-1683d2b7a7ca">

### Qualitative result 
<img width="661" alt="image" src="https://github.com/user-attachments/assets/3b7b1234-9cf6-45e2-86ca-0d1c5a4d078d">


### Ablation
- SFT data ablation
<img width="674" alt="image" src="https://github.com/user-attachments/assets/1b6cfab8-2fc8-40bd-b352-946982bde3f1">

VQA data helps improve POPE