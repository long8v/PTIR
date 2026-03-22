---
title: "[140] Improved Baselines with Visual Instruction Tuning"
date: 2023-12-12
tags: ['multimodal', 'LLM', '2023Q3', 'MLLM']
paper: "https://arxiv.org/pdf/2310.03744.pdf"
issue: 152
issueUrl: "https://github.com/long8v/PTIR/issues/152"
summary: "aka LLaVA1.5 / ShareGPT4V for following the LLaVA1.5 recipe - remarkable performance with few resources and open data."
---
<img width="674" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/460f065f-7d42-49d7-ac8f-160f21f350a8">

[paper](https://arxiv.org/pdf/2310.03744.pdf)

see llava https://github.com/long8v/PTIR/issues/128#issue-1749571159 here

## TL;DR
- **I read this because.. :** aka LLaVA1.5 / ShareGPT4V because you followed the LLaVA1.5 recipe
- **task :** LVLM
- **problem :** LLaVA is good at reasoning and real-world instruction following, but it performs poorly on our benchmarks.
- **idea :** do a better job of prompting for short answers like scale up / VQA!
- **input/output :** image + question -> answer 
- **architecture :** ViT-L/14(336 resolution) + LLaMA 13B
- **objective :** ce loss 
- **baseline :** llava, Qwen-VL, Shikra, BLIP-2, IDEFICS, instructBLIP
- **data :** (alignment) LCS-558K(LAION-CC-SBU with BLIP caption) / (end-to-end finetuning) LLaVA instruction data + VQA(OKVQA, A-OKVQA), OCR(OCRVQA, TextCaps), region-level VQA(Visual Genome, RefCOCO) 
- **evaluation :** GQA, MME, MM-Vet, VQA, GQA, VisWiz, SQA, VQA, POPE, ... 
- **result :** Improved by adding VQA when finetuning, improved by adding format prompt, improved by adding 2-layer mlp instead of linear, improved by increasing resolution, improved by adding various data such as ShareGPT (ShareGPT also has multilingual capability)
- **contribution :** Remarkable performance with few resources and open data.
- **etc. :**

## Details
### contribution
<img width="410" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b3bf4b04-e997-476d-9c0f-cc15ffc10f07">

Good performance with minimal tuning (ending in 8 A100 days with 1.2M scale public data)

### Dataset 
- alignment learning
LCS-558K(LAION-CC-SBU with BLIP caption)
In the middle is llava-lightning, which seems to be a variant for faster convergence.
If you look at https://github.com/haotian-liu/LLaVA/issues/86#issuecomment-1533346022, it is said to converge faster because it has roughly the same quantities as CC and a much larger concept converage.
CC and blip caption seem to be very different in text form, but... lol Isn't it an invisible trick to take a little benchmark? It's a pity that llava 1.5 didn't measure performance for conservation, maybe it would have been much lower?

- end-to-end finetuning
LLaVA instruction data + VQA(OKVQA, A-OKVQA), OCR(OCRVQA, TextCaps), region-level VQA(Visual Genome, RefCOCO) 
I didn't realize Visual Genome had VQA....
https://paperswithcode.com/dataset/visual-genome 
<img width="700" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9b9b8922-9e78-4dad-8537-74b22373d253">


### Improved baseline of LLaVA
- Why LLaVA performed so poorly in our benchmarks
VQA requires short answers, one or two words, LLaVA is not trained that way / spring the data a bit
-> "response formatting format" 
When you type something like VQAv2, instead of `Q: {Question} A: {Answer}" instead of `Q: {Question}, prompt `Answer the question using a single word or phrase`. This doubled the performance of simply putting VQAv2 into the training data, especially on a benchmark called MME. 502 -> 1197

<img width="406" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/46dd82ce-094b-430b-a774-87d631c73266">

### Result / Ability 
<img width="815" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7335f01f-f4f9-4706-a73d-dece262215ea">
LLaVA replied strangely

- Answers well for unrelated images
<img width="394" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a0939a79-84bc-41ee-87ce-6f971d85d717">

- JSON can be plucked! (OCR capability)
<img width="401" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5adca21d-40b9-4fc6-a70d-93c74722ded8">
 
- zs multi-lingual 
I'm using data from ShareGPT (https://sharegpt.com/), so it followed the multilingual instructions.
A platform where users can post their chatGPT questions and answers, presumably language only.
In particular, MMBench-CN actually beat Qwen-VL-Chat utilizing chinese instruction data (which is weird).

- computational cost
6 hours for pretraining / 20 hours for visual instruction tuning using 8A100s 
<img width="400" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/68150561-4413-4fc8-a6be-10229787ec55">


- limitation
1) The image seq len increases with resolution. q-former replaces it, but it seems to be slow to converge. We need to study how to train q-former efficiently.
2) Unable to process multi image. No data.
3) You're still limited to your target domain
4) There is a hallucination


- d--etails

<img width="395" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b1276863-f34d-44c3-9295-3998b9c5c201">

