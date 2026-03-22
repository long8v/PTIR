---
title: "[185] LLaVA-OneVision: Easy Visual Task Transfer"
date: 2024-11-12
tags: ['25min', 'MLLM', '2024Q4']
paper: "https://arxiv.org/pdf/2408.03326"
issue: 204
issueUrl: "https://github.com/long8v/PTIR/issues/204"
summary: "High mathvista performance - take a quick video benchmark."
---

<img width="851" alt="image" src="https://github.com/user-attachments/assets/efbb8140-09f1-440e-9525-85cc02d31429">

[paper](https://arxiv.org/pdf/2408.03326), [code](https://github.com/LLaVA-VL/LLaVA-NeXT), [blog](https://llava-vl.github.io/blog/2024-10-03-llava-critic/)

## TL;DR
- **I read this because.. :** High mathvista performance
- **task :** MLLM
- **problem :** VLM to cover multi-image, video all at once
- **IDEA:** Setting up anyres a little differently for each domain. Collect data and learn!
- **input/output :** {image or images or video, question} -> answer
- **architecture :** SigLIP SO400M + 2 layer MLP + Qwen2 {0.5B, 7.6B, 72.7B}
- **objective :** CE loss
- **baseline :** QwenVL, Gemini-Pro, Claude 3.5 Sonnet, GPT4V, GPT4o, VILA, Cambrian, InternVL
- **data :** stage 1.0 (still LCS-553K), stage 1.5 (3.5M llava recap, UReader, SynDog, chinese ShareGPT4V), stage 2.0 (curated Single Image 3.2M and OneVision 1.6M)
- **evaluation :** AI2D, ChartQA, DocVQA, InfoVQA, Mathverse, Mathvista, MMBench, MME, MMStar, MMMU, MMVet, SeedBench, ScienceQA, ImageDC, RealWorldQA, ... Multi-image benchs(5), Video Benchs(9)
- **result :** It seems that MathVista is the only one that is significantly higher when compared to Intern2-VL-8B on the same scale for single image eval? (63.2), good performance in multi-image, video bench
- **contribution :** Quickly take a video benchmark.
- **etc. :**

## Details
- thumbnail
<img width="743" alt="image" src="https://github.com/user-attachments/assets/56c507fd-1ffc-418d-99a1-5fcbcf8c5f88">

- anyres Changes
<img width="834" alt="image" src="https://github.com/user-attachments/assets/61445855-d031-4608-9ba5-702916bf155a">

- How anyres is applied per modality
<img width="780" alt="image" src="https://github.com/user-attachments/assets/ed80c74b-a7f3-4519-8793-ae956767aa7d">

<img width="809" alt="image" src="https://github.com/user-attachments/assets/b4d8e333-4917-42b9-9417-6730638e05c2">

- stage 1: Still LCS
- stage 1.5 
<img width="752" alt="image" src="https://github.com/user-attachments/assets/916e6843-819c-49df-b55a-a6dd0ac6cea2">

- stage 2
<img width="794" alt="image" src="https://github.com/user-attachments/assets/953188d9-e6a7-46c0-9994-6b27e84685bc">

Do not apply anyres in stage 1
Insert data in an increasingly long sequence length direction

### Result
<img width="533" alt="image" src="https://github.com/user-attachments/assets/46289ea7-25b0-47e3-8623-a04579b5458d">

<img width="544" alt="image" src="https://github.com/user-attachments/assets/92e8df30-4ca6-4687-bbe7-111e1afc192f">

<img width="545" alt="image" src="https://github.com/user-attachments/assets/0ef76d00-4ea6-4caa-8fac-2314f6955890">

