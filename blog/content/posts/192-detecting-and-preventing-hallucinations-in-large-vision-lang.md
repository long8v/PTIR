---
title: "Detecting and Preventing Hallucinations in Large Vision Language Models"
date: 2024-08-30
tags: ['AAAI', 'RL', '2023Q3', 'MLLM', 'ScaleAI']
paper: "https://arxiv.org/pdf/2308.06394"
issue: 192
issueUrl: "https://github.com/long8v/PTIR/issues/192"
summary: "VLM + RLHF - Benchmarks released, seems like a pretty early RLHF on VLM"
---
<img width="643" alt="image" src="https://github.com/user-attachments/assets/48e5a2d4-4639-4ebe-bbf8-6eabdc0c5372">

[paper](https://arxiv.org/pdf/2308.06394)

## TL;DR
- **I read this because.. :** VLM + RLHF
- **task :** LVLM 
- **problem :** hallucination
- **idea :** get human annotation at segment level to measure hallucination + learn like rejection sampling / DPO
- **input/output :** {image, question} -> class(accurate, inaccurate, analysis)
- **architecture :** InstructBLIP 
- **objective :** CE loss or proposed FDPO loss
- **baseline :** InstructBLIP, LLaVA, mPLUG-OWL
- **data :** (proposed) 16K image-prompt-response 
- **evaluation :** RM Score(NLL for true segments), human eval(percent of content that was truthful? Sentence-by-sentence...
- **result :** Improved performance when training the reward model and rejection sampling. The proposed FDPO also improved performance.
- **contribution :** Benchmarks published, pretty early work on RLHF for VLM
- **etc. :** MHALDetect benchmarks are well done, so there are a lot of citations, but something doesn't read well...

## Details

As shown below, the annotation
<img width="715" alt="image" src="https://github.com/user-attachments/assets/0489694d-ff20-42b6-9d6f-3d81c308a5f4">

4000 images - instructBLIP response (10 human annotated)
4 classes: accurate, inaccurate, analysis, and unsure

val split 3200 of them --> this is probably the MHALDetect

### Method
- Multi-Modal Reward Model
Using Instruct BLIP. Learning by attaching a classifier (accurate, inaccurate, analysis) to each sentence level eos token.
For a segment-level reward model, I put a classifier at the end of each segment (which just goes on and on until I look at the data and see a different label). Not sure why I did this..!

- Rejection sampling 
I don't have a proper explanation, but it seems like it's sampling from the inference and then using the negative log likelihood value in the RM model at each sentence level to determine whether there is a hallucination or not.
best-of-n, worst-of-n. where n is 16, 64
<img width="710" alt="image" src="https://github.com/user-attachments/assets/84b4ba8b-2fe2-468a-b3fb-49eb4a934f76">

- fine-grained direct preference optimization 
Unlike DPO, in this case we don't have a pair so we just impose the loss at the segment level

<img width="305" alt="image" src="https://github.com/user-attachments/assets/04293d45-8758-4f07-9b2c-2d0563cedb6a">

- $x$ : tokens before the current segment
- $y$ : generated segment
- $c$ : class of current segment
  - 1 : preferred classs (correct)
- 0: dispreferred class (incorrect, optionally also analysis)

### Result
- Performance of reward models
<img width="439" alt="image" src="https://github.com/user-attachments/assets/9d7b260e-81c9-4d8b-9fa6-516f4415cbc8">

- rejection sampling / finegrained DPO result
<img width="703" alt="image" src="https://github.com/user-attachments/assets/304321ba-f445-4ed2-be86-0f0b3ba56377">

RM Score doesn't cut it.... Improved performance on Human Eval.
No other hallucination benches or VLM benches were taken.
