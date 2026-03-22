---
title: "RLHF-V: Towards Trustworthy MLLMs via Behavior Alignment from Fine-grained Correctional Human Feedback"
date: 2024-08-30
tags: ['CVPR', 'RL', 'MLLM', '2024Q2']
paper: "https://arxiv.org/abs/2312.00849"
issue: 191
issueUrl: "https://github.com/long8v/PTIR/issues/191"
summary: "VLM + RLHF - Efficient DPO training. Data disclosure"
---
<img width="702" alt="image" src="https://github.com/user-attachments/assets/1331c895-4427-4f7f-baa9-e619afc49d33">

[paper](https://arxiv.org/abs/2312.00849), [data](https://huggingface.co/datasets/openbmb/RLHF-V-Dataset?row=0), [code](https://github.com/RLHF-V)

## TL;DR
- **I read this because.. :** VLM + RLHF
- **task :** MLLM
- Problem :** Hallucination problem in MLLM. In the case of GPT4-V, 45.9% were hallucinations.
- Idea :** Let's learn DPO, but let's make sure to correctly answer which segment is wrong.
- **input/output :** {image, question} -> answer
- **architecture :** The authors' previous work, [Muffin](https://arxiv.org/abs/2310.00653). Model based on BEiT-3 + 13B Vicnuna 1.0
- **objective :** Slightly modified DPO, with slightly different weights for the log-propb part of the DPO loss term.
- **baseline :** QwenVL-Chat, LLaVA, LLaVA1.5, Muffin, InstructBLIP, LLaVA-RLHF
- **data :** human annotated 1.4K data 
- **evaluation :** Object HalBench, MMHAL-Bench, MHumanEval, LLaVA Bench, VQAv2
- **result :** SOTA among open models in terms of hallucination (beats some GPT4Vs). For LLAVA Bench, LLavA-RLHF is better, but tied.
- **contribution :** Efficient DPO learning. Data disclosure
- **etc. :**

## Details
### overall
<img width="879" alt="image" src="https://github.com/user-attachments/assets/c6c28612-1726-4d48-a574-ca80ab0da125">

### underlying challenges in human preference data
1) ambiguity 
There are two answers, each with its own advantages and disadvantages, and the question is which one to favor.
2) learning efficiency 
It is difficult to learn because it needs to give feedback for a long answer with one response, so it requires a lot of data, and this credit misallocation problem leads to problems such as reward hacking.

### fine-grained correctional human preference collection
Human annotation at the segment level. Correcting hallucinated segments. Before/after correction becomes $y_w$, $y_l$.
In this case, the data comes from the instruction data source by making the image description prompt as GPT4 (?) and the answer is received via muffin (??).

The resulting data statistic is 64.4 words with 2.65 corrected segments.
The hallucination types were objects (41.2%), positions (20.3%), numbers (16.5%), attributes (10.0%), actions (5.3%), and misc.

### Dense Direct Preference Optimization
- DPO loss recap
<img width="401" alt="image" src="https://github.com/user-attachments/assets/0819f53a-51f5-4de3-8b23-f8a9ecc80387">

($\beta$ 0.5)

Here, the proposed DDPO is to weight the log-prob part according to whether it belongs to the corrected segment ($y_c$) or not (unchanged, $y_u$).

<img width="547" alt="image" src="https://github.com/user-attachments/assets/76ea3796-7eab-40bf-9cd6-2c00ff38eb94">

- $\gamma$ : 5 
- $N$: len($y_u$) + $\gamma$ len($y_c$)
- 1/N is there to control for a preference for longer responses that are more likely to be longer

### Result 

<img width="1216" alt="image" src="https://github.com/user-attachments/assets/5d949e13-5ac8-4aae-99c5-7667028314d2">

<img width="1091" alt="image" src="https://github.com/user-attachments/assets/3293996f-58c5-4822-bef8-4b8d44b792c3">

<img width="800" alt="image" src="https://github.com/user-attachments/assets/69589a46-f611-4ed8-bae0-1e3e5ae05d45">

<img width="500" alt="image" src="https://github.com/user-attachments/assets/a0083a42-3e45-41db-b520-06d2016843ee">

<img width="500" alt="image" src="https://github.com/user-attachments/assets/35b8e49b-35cd-47fc-87ac-feb4585ba527">


#### Ablations
<img width="607" alt="image" src="https://github.com/user-attachments/assets/44383afc-8028-44b5-9b08-683347eb394f">

<img width="400" alt="image" src="https://github.com/user-attachments/assets/fde462be-8c6c-4037-aa50-39b6ef05ee54">

