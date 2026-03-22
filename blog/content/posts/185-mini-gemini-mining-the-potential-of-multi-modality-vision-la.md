---
title: "Mini-Gemini: Mining the Potential of Multi-modality Vision Language Models"
date: 2024-07-23
tags: ['MLLM', '2024Q1']
paper: "https://arxiv.org/abs/2403.18814"
issue: 185
issueUrl: "https://github.com/long8v/PTIR/issues/185"
summary: "LVLM model after a long time. I was wondering about data curation - information merge interesting. Good data curation. data ablation does a lot."
---
![image](https://github.com/user-attachments/assets/b1ec47b7-bfa0-4f0c-9521-fca5a87bc638)

[paper](https://arxiv.org/abs/2403.18814), [repo](https://github.com/dvlab-research/MGM), [demo](http://103.170.5.190:7860/)

## TL;DR
- **I read this because.. :** LVLM model after a long time. I was curious about data curation, so I used
- **task :** Vision Language Model
- **problem :** I don't have a strong sense of subject matter... my goal is to create a VLM that performs well enough to be taught in an academic setting.
- **idea :** 1) To efficiently handle resolution, let's CA two high resolution and low resolution to extract information 2) Let's do a good job of data curation 3) To do a good job of generation using Stable Diffusion in the middle
- **input/output :** {image, Q} -> {A} (optionally call SD according to answer)
- **architecture :** CLIP ViT-L (for low resolution) + ConvNext-L (high resolution) + mining layer (projection and MLP) + LLM (Gemma-2B, Vicuna-7, 13B, Mixtral-8x7B, Hermes-2-Yi-34B)
- **objective :** CE loss 
- **baseline :** (normal resolution) MobileVLM, InstructBLIP, Qwen-VL, Shikra, IDEFICS-80B, LLaMA-VID, LLaVA-1.5 (high resolution) OtterHD, CogVLM-chat, LLaVA-NeXT, (private models) Gemini Pro, Qwen-VL-Plus, GPT-4V
- **data :** (alignment) 558K from CC3M filtered by llava, 695K ALLaVA, (instruction) 643K LLaVA (except textcaps), 100K from ShareGPT4V, 10K LAION-GPT4V, 700K ALLaVA, 5K text-only multiturn from LIMA and OpenAssistant, 28K OCR related(10K DocVQA, 4K ChartQA, 10K DVQA, 4K AI2D) + (generation-related instruction) 13K configured
- **evaluation :** TextVQA, MMB, MME, MM-Vet, MMMU, MathVista
- **result :** Good performance among given benchmarks
- **contribution :** information merge Interesting. Good data curation. data ablation does a lot.
- **etc. :**

## Details
- thumbnail
![image](https://github.com/user-attachments/assets/46a09652-d51e-48e5-a474-5c2445fe087f)

### architecture
- overall framework
![image](https://github.com/user-attachments/assets/53633083-49b2-4e92-849e-e1fb256edb77)

- proposed patch info mining
![image](https://github.com/user-attachments/assets/535cdecb-0e0f-40c8-843a-ba2f967b3c49)

![image](https://github.com/user-attachments/assets/dca020e2-b7ce-4be0-9680-1e28527fe4c4)


### data 
![image](https://github.com/user-attachments/assets/18c71153-0b3c-49ee-9839-5006aee7d1df)

### Result
![image](https://github.com/user-attachments/assets/e16bc7a2-ab62-450f-96c2-8568113a3259)

- ablation
![image](https://github.com/user-attachments/assets/f5d04bd6-a2a3-4d97-8a31-0bea477b4c87)

![image](https://github.com/user-attachments/assets/07b318f4-9302-49cb-b4d3-231c4fd87bb6)

- qualitative examples
![image](https://github.com/user-attachments/assets/10513f2d-e06e-4182-b743-0d5ef0263d2e)

![image](https://github.com/user-attachments/assets/06f1d022-c1ca-4563-82f0-a2137bc10923)


- play with demo
![image](https://github.com/user-attachments/assets/c4be4572-4a17-4f3b-8631-7be80fb11686)

![image](https://github.com/user-attachments/assets/affc89d4-9c14-4f70-acb4-513e6f2717c3)
![image](https://github.com/user-attachments/assets/e9c4f25d-50ce-4e3a-92d3-461ab80ef62e)

![image](https://github.com/user-attachments/assets/10854252-f63c-4c3f-8c48-15e59f58d32b)
![image](https://github.com/user-attachments/assets/46bd2635-f052-4e58-8e20-69d4921ca54c)
