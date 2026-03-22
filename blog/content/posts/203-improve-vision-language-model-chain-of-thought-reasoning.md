---
title: "[184] Improve Vision Language Model Chain-of-thought Reasoning"
date: 2024-10-29
tags: ['CMU', 'MLLM', '2024Q3']
paper: "https://arxiv.org/abs/2410.16198"
issue: 203
issueUrl: "https://github.com/long8v/PTIR/issues/203"
summary: "Reasoning ability in VLM - Improved benchmarks with smaller datasets. More reasoning-related analysis."
---
<img width="990" alt="image" src="https://github.com/user-attachments/assets/7f580442-a1e9-46de-b6b9-b1f639569585">

[paper](https://arxiv.org/abs/2410.16198)

## TL;DR
- **I read this because.. :** reasoning ability in VLM
- **task :** VLM
- Problem :** Most of the VLM instruction data is short
- Idea:** Create CoT data with GPT4-o
- **architecture :** LLaVA-NeXT
- **objective :** CE loss -> DPO loss
- **baseline :** LLaVA-NeXT, GPT4o, Cambrian, (data) RLAIF
- **data :** ShareGPT4-o Reasoning (not yet public)
- **evaluation :** A-OKVQA, DocVQA, ChartQA, AI2D, ScienceQA, ... 
- **result :** Evenly high performance across all benches.
- **contribution :** Improved benchmarks with a small dataset. Lots of reasoning related analysis.

## Details
- motivation
<img width="1228" alt="image" src="https://github.com/user-attachments/assets/4fd38f06-0281-4925-827a-04d08f4527f1">

### Data
- reasoning data distilation 
<img width="396" alt="image" src="https://github.com/user-attachments/assets/5143e33b-5c41-45a3-8a98-3dfa538e47a7">

<img width="511" alt="image" src="https://github.com/user-attachments/assets/6f93ef00-095a-4d4d-bf4f-843ca2dcb4a5">

<img width="1227" alt="image" src="https://github.com/user-attachments/assets/b917283e-f042-4d05-ad19-d4a7ea01b02b">

<img width="1302" alt="image" src="https://github.com/user-attachments/assets/9d903ebe-0b9b-4670-b563-803f62e315be">


### Result
<img width="575" alt="image" src="https://github.com/user-attachments/assets/e0658b2a-d569-4621-a17b-df66c25ad7b1">

Organize your data as above
- (1) format: Configured to the level that only the answer format can be correct. 50 samplings for each of the 9 datasets. 2K on both CoT/direct + LLaVA-pretrain
- (2) direct data: (1) + 193K with the answer right away in Full
- (3) CoT data: (1) + what you put in CoT 193K + additionally GLLaVA-align/QA
- (4) CoT SFT: (1) + direct + whatever you put in both CoT + additionally GLLaVA-align/QA


<img width="1107" alt="image" src="https://github.com/user-attachments/assets/f2d3ec4a-27cb-4d15-8bb4-72db547b94fc">

**CAN REASONING BE IMPLICITLY LEARNED FROM DIRECT PREDICTION?** -- Compare (1) and (2)
-> when trained with only direct answers, CoT inferencing showed little or no improvement (mathvista -1.7)

**HOW EFFECTIVE IS COT REASONING DATA?**
-- (3) Performance improvements on computationally intensive benchmarks such as chartQA and Mathvista, and surprisingly on text-heavy benchmarks such as TextVQA, DocVQA, and InfoVQA.
-- (4) The best average performance was achieved when both CoT and Direct were trained. However, TextVQA, DocVQA, and AI2D performed better on direct. This is likely due to the fact extraction-oriented benchmarks.


**ABLATION TESTS ON DATA COMPOSITION**
<img width="459" alt="image" src="https://github.com/user-attachments/assets/c5f25ed4-64ec-4aa9-8eba-9a9f6ff7e4f0">

Math side data ablation. text only sft was removed because it didn't do much good

<img width="462" alt="image" src="https://github.com/user-attachments/assets/f2610c8b-8a7a-4195-af54-63a89fd8fc35">

ablation for science. They were both good together.

**Comparsion of GPT4o / Cambrian**
<img width="614" alt="image" src="https://github.com/user-attachments/assets/6c883fce-405a-44a9-a4a4-1317f88fa687">

ScienceQA performs well on closed set. Could be a train data problem...

### DPO Result
<img width="1107" alt="image" src="https://github.com/user-attachments/assets/97050261-dad2-4965-b1fb-20661b847416">

<img width="743" alt="image" src="https://github.com/user-attachments/assets/36cb7c26-8f44-4840-b84b-31e97666d928">

<img width="1121" alt="image" src="https://github.com/user-attachments/assets/74198e0e-ed30-447c-a469-18d55fc25f55">

There are more things like BoN, but I'll organize them later.