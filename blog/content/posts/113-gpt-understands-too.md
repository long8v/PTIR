---
title: "[104] GPT Understands, too"
date: 2023-03-23
tags: ['2021Q1', 'prompt', 'GPT', 'finetuning', 'LLM']
paper: "https://arxiv.org/pdf/2103.10385.pdf"
issue: 113
issueUrl: "https://github.com/long8v/PTIR/issues/113"
summary: "I read the article in huggingface's parameter efficient finetuning repo. I've heard of p-tuning a lot, but never read about it - manual prompt search to continuous zone"
---
<img width="857" alt="image" src="https://user-images.githubusercontent.com/46675408/227085867-d5ceaf17-37ad-4409-95f3-18f24783bb53.png">

[paper](https://arxiv.org/pdf/2103.10385.pdf)

## TL;DR
- **I read this because.. :** I read this while looking at the article in the parameter efficient finetuning repo on huggingface. I've heard of p-tuning a lot, but never read it.
- **task :** language model finetuning(Knowledge probing, ...)
- Problem :** When finetuning LLM, the parameter is too large, and the few-shot setting, many-shot setting, or trasnfer ability is poor. I can use GPT-3 with a good prompt, but finding a good prompt is too laborious, and the performance is jagged depending on the prompt.
- **idea :** don't look for prompt in discrete, but in continuous space
- **architecture :** Put template {pseudo-prompt $P_{0:i}$, $\mathbf{x}$, $P_{i+1:m}$, $\mathbf{e(y)}$ } in LLM such as BERT / GPT and learn the embedding of each psudo-prompt. We want the prompt embeddings to be learned interdependently, so we add a bi-LSTM layer to strengthen the embeddings.
- **objective :** MLM loss 
- **baseline :** manual prompt, fiene-tuning, discrete prompt searching, manual prompt + finetuning 
- **data :** LAMA, SuperGLUE
- **evaluation :** accuracy, F1, ... 
- **result :** better performance on most tasks in GLUE on gpt/bert based model! (finetune also wins)
- **contribution :** manual prompt search to continuous area
- **limitation / things I cannot understand :** prompt CIL This reminds me a bit of this, and I'd like to try p-tuning in an MTL environment.

## Details
<img width="845" alt="image" src="https://user-images.githubusercontent.com/46675408/227093898-ffaae65f-7e21-4917-9af0-256667873e82.png">

<img width="428" alt="image" src="https://user-images.githubusercontent.com/46675408/227094093-7c460d2c-c79b-484d-b955-d2d97e42f93c.png">

- $\mathcal{M}$ : pretrained LM

There are two problems with training this way: 1) the embedding space $\mathbf{e}$ of the pretrained LM $\mathcal{M}$ is discrete, so if $h$ is randomly initialized, only the parameters of small neighborhoods are modified and it is easy to fall into local minima, and 2) we want the prompt tokens to be dependent on each other.
To solve this, we add one lite network.
<img width="527" alt="image" src="https://user-images.githubusercontent.com/46675408/227097887-2d0e476a-ae24-4ff7-8df0-10dab5a386e5.png">

Although an LSTM is added, it has very few parameters compared to LM, and in the inference phase, we can simply discard the LSTM and use the learned embedding h.

<img width="383" alt="image" src="https://user-images.githubusercontent.com/46675408/227094364-3b8822e3-6652-4b6e-bf64-93688e6ea510.png">

### Result
<img width="853" alt="image" src="https://user-images.githubusercontent.com/46675408/227094008-ba763425-697d-48d3-b1fc-c991d86abe0a.png">

p-tuning uses the parameters of the language model as freeze
I'm surprised you beat finetuning.

<img width="865" alt="image" src="https://user-images.githubusercontent.com/46675408/227098059-876a8628-9365-430a-96f2-7d4fd30fa332.png">

### Follow-up
P-Tuning v2: Prompt Tuning Can Be Comparable to Fine-tuning Universally Across Scales and Tasks
Putting a prompt token in each layer is shown to be good at hard sequence labeling tasks that p-tuning was not good at in the past / Shows that it works even on small models
https://arxiv.org/pdf/2110.07602.pdf
<img width="923" alt="image" src="https://user-images.githubusercontent.com/46675408/228109125-5ba4c333-8af1-4c36-b58e-7ebb02c7af4c.png">

