---
title: "Prefix-Tuning: Optimizing Continuous Prompts for Generation"
date: 2023-03-28
tags: ['2021Q1', '25min', 'finetuning', 'LLM', 'ACL']
paper: "https://aclanthology.org/2021.acl-long.353.pdf"
issue: 115
issueUrl: "https://github.com/long8v/PTIR/issues/115"
summary: "Similar ideas to efficient finetuning series water - #113"
---
<img width="778" alt="image" src="https://user-images.githubusercontent.com/46675408/228103645-5a064341-7b31-4142-9051-fbca465348a5.png">

[paper](https://aclanthology.org/2021.acl-long.353.pdf)

## TL;DR
- **I read this because.. :** efficient finetuning series water
- **task :** LLM finetuning
- **problem :** finetuning is inefficient. Finding discrete prompts is inefficient.
- **idea :** precede a continuous prompt.
- **architecture :** BART, GPT-2
- **objective :** ce loss
- **baseline :** finetuning, finetuning top 2 layer, apdapter
- **data :** E2E, WebNLG, DART 
- **result :** slightly lower than finetuning, slightly better than adapter or ft-top2
- **contribution :** An idea similar to #113

## Details
<img width="445" alt="image" src="https://user-images.githubusercontent.com/46675408/228104356-216263dd-6ecd-49c6-9e53-54441e9e602c.png">

PLM separate and with a hidden dimension matrix $P_\theta$ for prefixes
<img width="381" alt="image" src="https://user-images.githubusercontent.com/46675408/228108123-3755df18-6d09-4a19-a258-79fbffd9617f.png">

<img width="858" alt="image" src="https://user-images.githubusercontent.com/46675408/228104383-4744b8ac-5965-42f2-8435-3fdd4baf441b.png">

We found that starting with a smaller matrix $P_\theta '$ and increasing the size with MLP performed better. After learning, we can use the prefix $P_\theta $ directly without $P_\theta '$.

### Results
<img width="821" alt="image" src="https://user-images.githubusercontent.com/46675408/228108486-a27ffbce-c333-4a43-8d82-4f51235e265e.png">


### Ablations
- It was better to init with real words than random initalize in low data situations.
<img width="423" alt="image" src="https://user-images.githubusercontent.com/46675408/228107390-869dd879-7fa7-42aa-bb31-b0a129d8d176.png">

Even task-irrelevant "elephant" was better than random. When full, Initialize was not significantly affected.

- Prompt length had an upward performance curve per task
200 for summary / 10 for table to text
<img width="424" alt="image" src="https://user-images.githubusercontent.com/46675408/228107654-790dec8c-7f18-4c4a-ad5b-c8b88aa706a1.png">

- The prefix form, preceded by prompt, performed better than the infix form, $[x; prompt; y]$.
<img width="392" alt="image" src="https://user-images.githubusercontent.com/46675408/228108578-cf3d8c3b-188f-4df5-ae56-4d795997220c.png">
