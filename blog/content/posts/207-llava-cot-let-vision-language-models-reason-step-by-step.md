---
title: "LLaVA-CoT: Let Vision Language Models Reason Step-by-Step"
date: 2024-12-02
tags: ['MLLM', '2024Q4']
paper: "https://arxiv.org/abs/2411.10440"
issue: 207
issueUrl: "https://github.com/long8v/PTIR/issues/207"
summary: "Get featured - make your data public."
---

<img width="1117" alt="image" src="https://github.com/user-attachments/assets/70c99f82-503c-4cec-8ed0-1548b9fa79b9">

[paper](https://arxiv.org/abs/2411.10440), [code](https://github.com/PKU-YuanGroup/LLaVA-CoT), [dataset](https://huggingface.co/datasets/Xkev/LLaVA-CoT-100k)

## TL;DR
- **I read this because.. :** Recommended by
- **task :** reasoning in LVLM
- **problem :** I want LVLM to have longer reasoning like gpt-o1
- Idea :** Put in data and learn. Break down the steps of the answer. Let's do a beam search for each step of the answer
- **architecture :** Llama 3.2V
- **objective :** CE loss (SFT after future SFT)
- **baseline :** Llama 3.2V 
- **data :** Llava-CoT-100k (proposed)
- **evaluation :** mmstar, mmbench, mmvet, mathvista, ai2d, 
- **result :** Improved performance.
- **contribution :** Data disclosure.

## Details
- thumbnail
<img width="506" alt="image" src="https://github.com/user-attachments/assets/24cbd569-106f-4509-b66f-48cad1f7f28f">

- inference examples
<img width="995" alt="image" src="https://github.com/user-attachments/assets/c597592a-c010-4e81-9b9f-fe18bb8f805d">

- How to structure your answers
<img width="499" alt="image" src="https://github.com/user-attachments/assets/a1d31ac1-43a2-4629-98da-56a6ba82cac7">

GPT4o to generate and then mismatch the structure Filtering.
Have GPT4o filter the things inside the `<summary>`, `</summary>` tags against the Gt answer to see if it's a good answer.
<img width="369" alt="image" src="https://github.com/user-attachments/assets/b70b6435-f941-434c-b730-770258a830a6">

<img width="375" alt="image" src="https://github.com/user-attachments/assets/19750790-9019-44a4-9b1a-8b9e8f6046d6">

- Generated image source
<img width="360" alt="image" src="https://github.com/user-attachments/assets/20b4d697-7137-4451-904c-7aae1452a53d">

https://github.com/long8v/PTIR/issues/203 overlap source with this
<img width="250" alt="image" src="https://github.com/user-attachments/assets/ea6803af-7e51-4ba3-a023-10017eb39ef5">

- Run a beam search for each structure
<img width="758" alt="image" src="https://github.com/user-attachments/assets/a1bd349d-c5ab-4642-8702-0a705dc9c23a">

I didn't realize it was called "beam search", but it looks like it uses an external verifier.
Prompt used? Didn't see which model you used
<img width="367" alt="image" src="https://github.com/user-attachments/assets/ae50b9cc-0c20-4c0f-a315-5f47c96f319e">

- Training hparam
<img width="327" alt="image" src="https://github.com/user-attachments/assets/df382379-2a97-42dc-bd3f-04847199bee8">


### Result
<img width="753" alt="image" src="https://github.com/user-attachments/assets/58aaeb90-3bbc-4b2a-80d3-eb05a7d158bc">

I chose my own "Reasoning Benchmark".
direct training is the original vqa set further SFTed with the original vqa set. w/o structured tags is without tags like `<summary>`.
mmstar, mmvet, and mathvista improved. ai2d performs better just learning the answer with direct

<img width="767" alt="image" src="https://github.com/user-attachments/assets/55498446-89d6-4d46-a3d4-55029dc98df7">

If you look at the details in mmstar, reasoning related details, math, science, etc. go up. perception does not go up, but it is insignificant.

- stage level beam search
<img width="744" alt="image" src="https://github.com/user-attachments/assets/ced8c521-fc62-4d94-88c9-d047b3e82187">

How did BoN do it without mentioning RM learning?
<img width="760" alt="image" src="https://github.com/user-attachments/assets/48418500-d017-47c2-9099-b029b75abe28">

- comparison with other models
<img width="767" alt="image" src="https://github.com/user-attachments/assets/30304e55-936d-40aa-9a33-ff5b838ca83d">
