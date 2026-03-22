---
title: "[171] CLIP-DPO: Vision-Language Models as a Source of Preference for Fixing Hallucinations in LVLMs"
date: 2024-08-30
tags: ['ECCV', 'RL', 'MLLM', '2024Q3']
paper: "https://www.arxiv.org/abs/2408.10433"
issue: 190
issueUrl: "https://github.com/long8v/PTIR/issues/190"
summary: "Recommended by google scholar - create DPO data on the cheap."
---
<img width="800" alt="image" src="https://github.com/user-attachments/assets/ebe72de4-8626-4297-9ef5-3d5853cef631">

[paper](https://www.arxiv.org/abs/2408.10433)

## TL;DR
- **I read this because.. :** recommended by google scholar
- **task :** VLM + RLHF
- **problem :** I want to solve the hallucination of VLM, but can't I create data for DPO training on the cheap?
- **idea :** CLIP score to create with?
- **input/output :** {image, question} -> score
- **architecture :** MobileVLM-v2), LLaVA 1.5
- **objective :** DPO loss 
- **baseline :** BLIP-2, InstructBLIP, Shira, OpenFlamingo, Qwn-VL ... ShareGPT4V, HA-DPO as DPO technique
- **data :** Image source is SFT, created with MobileVLM-v2, filtered by CLIP score and heuristics. Create win / lose pairs based on CLIP score of 2 or more.
- **evaluation :** [AMBER](https://github.com/junyangwang0410/AMBER), classification evaluated by CLIP (tell it to generate captions, then do zero-shot classification with siglip), VLM benchs (GQA, SQA, VQA, MME, MMB)
- **result :** AMBER improvement. Not QwenVL, GPT4V, but AMBER sota. Other benchmarks don't worsen performance, and SQA and MMB don't improve?
- **contribution :** Create DPO data on the cheap.
- **etc. :**

## Details
- why CLIP?
Create a hallucination as shown below and then compare CLIP vs LLaVA 1.5 logit
<img width="500" alt="image" src="https://github.com/user-attachments/assets/d3ca114a-89bf-45a2-b6c0-e41dfdf88594">

<img width="300" alt="image" src="https://github.com/user-attachments/assets/6840772b-d3ad-418c-bfb0-0b7da038af28">

bar = logit assigned larger for hallucinated caption (dark blue llava 1.5 / light blue CLIP)

CLIP pulls out hallucinated objects, attributes, and relations better than VLM!

- `CLIP-DPO`
No change to the DPO algorithm, just the data pool
<img width="590" alt="image" src="https://github.com/user-attachments/assets/7b8e10d4-2f4d-428a-a8a9-7ceaa5340dde">

- data
<img width="648" alt="image" src="https://github.com/user-attachments/assets/068998e0-8cb3-466a-a549-80ab70f3cdb9">

1) generation: created in two forms using lightweight VLM (MobileVLM-v2 family in the paper)
- generic caption
Asking Mobile VLM v2 models to create a caption. Use 5 prompts

- per-image QA
<img width="634" alt="image" src="https://github.com/user-attachments/assets/d9dff43b-195f-413d-a5a7-12c256b2c653">

Ask Mistral 7B to create questions and correct and incorrect answers from images

2) data annotation
- CLIP ranking: CLIPScore in a nutshell
- Global filtering : 
- Remove an image containing text because it has a high CLIPScore
- Remove below CLIPScore threshold
- Remove long captions
- Remove low CLIPScore for questions (e.g. "what is the main object in the image?")
<img width="630" alt="image" src="https://github.com/user-attachments/assets/f73732cc-0f56-42bd-83f6-b402b1a2fab1">

- Pair filtering : 
- For QA, subtract the description of the image from Q with a regex, concat with the answer, and filter out the low CLIPScore (?)
- Only those with a CLIPScore difference of 2 or more
- As long as the caption lengths are not too different

We end up with 750K pairs -- 50K of which are QA and 700K of which are captioned

<img width="634" alt="image" src="https://github.com/user-attachments/assets/76a77d41-7de4-4a02-b4e1-5a5c42399d91">

#### Result 

<img width="644" alt="image" src="https://github.com/user-attachments/assets/8196d514-f547-4cb1-bd75-a246a482a8f7">

<img width="620" alt="image" src="https://github.com/user-attachments/assets/9865fec5-8865-4936-a5dc-7eb5c50b6cdb">

<img width="623" alt="image" src="https://github.com/user-attachments/assets/61eb1f33-a0f4-4860-ac2d-b11b9d12ecfc">
