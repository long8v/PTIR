---
title: "[208] FastCuRL: Curriculum Reinforcement Learning with Progressive Context Extension for Efficient Training R1-like Reasoning Models"
date: 2025-03-27
tags: ['25min', 'RL', '2025Q1']
paper: "https://arxiv.org/abs/2503.17287"
issue: 229
issueUrl: "https://github.com/long8v/PTIR/issues/229"
summary: "Wandering around github and found curriculum - good performance compared to baseline. training cost is 50% of deepscaleR"
---
<img width="923" alt="Image" src="https://github.com/user-attachments/assets/703ab1a8-faf4-4a31-bc3e-23b365e3c2f3" />

[paper](https://arxiv.org/abs/2503.17287)

## TL;DR
- **I read this because.. :** I was wandering around github and saw curriculum.
- **task :** reasoning LLM 
- **problem :** I want to learn curriculum (similar to deepscaleR)
- **idea :** longer prompt would be more complicated
- **architecture :** 
- **objective :** GRPO loss
- **baseline :** DEEPSEEK-R1DISTILL-QWEN-1.5B, STILL-1.5B7, DeepScaleR1.5B-Preview, RSTAR-MATH-7B , QWEN-2.5-MATH-7B-Instruct, QWEN2.5-7B-SimpleRL8, and EURUS-27B-PRIM
- **data :** AIME problems (1984-2023), AMC problems (before 2023), Omni-MATH dataset, Still dataset
- **evaluation :** MATH 500, AIME 2024, AMC 2023, Minerva Math, and OlympiadBench
- **result :** Good performance compared to baseline. training cost is 50% of deepscaleR
- **contribution :** 
- **etc. :**

## Details

<img width="897" alt="Image" src="https://github.com/user-attachments/assets/cba0a598-3f03-4449-b7a0-dc0a2d2fb95c" />

<img width="927" alt="Image" src="https://github.com/user-attachments/assets/d9b38d62-5d44-4fe0-8bc1-56b807c68b9c" />

<img width="922" alt="Image" src="https://github.com/user-attachments/assets/9de75325-3e41-49e4-9b29-73b63505977c" />

<img width="426" alt="Image" src="https://github.com/user-attachments/assets/7a5d3048-b962-43e8-a48b-6d8da889f418" />