---
title: "[202] s1: Simple test-time scaling"
date: 2025-02-10
tags: ['25min', 'test-time-scaling', 'reasoning', '2025Q1']
paper: "https://arxiv.org/pdf/2501.19393"
issue: 223
issueUrl: "https://github.com/long8v/PTIR/issues/223"
summary: "Mentioned - 1) confirmation that SFT alone is test-time-scaling 2) filtering-related ablation"
---
<img width="689" alt="Image" src="https://github.com/user-attachments/assets/5751e883-620f-47fd-ac8c-4f4c2a223ef8" />

[paper](https://arxiv.org/pdf/2501.19393), [code](https://github.com/simplescaling/s1)

## TL;DR
- **I read this because.. :** because it mentions
- **task :** reasoning in LLM
- **problem :** How can we make test time scaling simple?
- **idea :** Let's filter the data well. When inferring, let's add `wait` if it's not up to the desired length, and eot if it's too long (Budget Forcing)
- **architecture :** Qwen2.5-32B-Instruct
- **objective :** ce loss (SFT only)
- **baseline :** OpenAI o1 series, DeepSeek r1 series, QwQ-32B-preview, Sky-T1-32B-Preview, Bespoke-32B, Google Gemini 2.0 Flash Thinking Experimental // 
- **data :** s1K (proposed) -- NuminaMATH, AIME, OlympicArena, OmniMath, AGIEval + additionally crawled from [Stanford Statistics Department PhD Qualifying Exam] (https://statistics.stanford.edu/) and [PuzzledQuant] (https://www.puzzledquant.com/) homepages.
- **evaluation :** AIME24, MATH500, GPQA diamond 
- **result :** Good performance relative to the number of training samples. Good performance when quality, difficulty, and diverse criteria are all used. Suggested
- **contribution :** 1) Confirmed that SFT alone is test-time-scaling 2) Filtering related ablation
- **etc. :**

## Details
- thumbnail
<img width="684" alt="Image" src="https://github.com/user-attachments/assets/942cb71f-972c-47ef-97b8-023ac07ce0da" />

<img width="1317" alt="Image" src="https://github.com/user-attachments/assets/8921eac0-0f21-438d-b552-26f54ad26fb5" />

### reasoning data curation to create s1k
  - inital collection of 59K
- NuminaMATH, AIME, OlympicArena, OmniMath, AGIEval + additionally crawl [Stanford Statistics PhD Qualifying Exam] (https://statistics.stanford.edu/) and [PuzzledQuant] (https://www.puzzledquant.com/) from their homepages
- Deduplicate to 8-gram
  - final selection of 1K sample
- quality: api error, formatting issue(e.g. scii art diagram, non-existent image reference, inconsistent question numbering) --> 51K remaining
- difficulty: Solved using Qwen2.5-7B/32B-Instruct and evaluated with Claude 3.5 sonnet. Filtered by Qwen 2.5 tokenizer assuming long as hard. --> 25K left
- diversity : Claude 3.5 Sonnet divides math and science (biology, physics, economics) into categories (geometry, dynamic system, ... ) --> 24K left
- Additionally, following the philosophy of difficulty, we picked one problem per domain as a longerreasoning trace
- That leaves us with 50 domains
      - <img width="1209" alt="Image" src="https://github.com/user-attachments/assets/ec3fe146-2fe7-409d-9861-158b73fbab00" />


###  proposed budget forcing

<img width="654" alt="Image" src="https://github.com/user-attachments/assets/1e7cb8d0-db67-4bf3-835f-af6a2cf00aa1" />

### Result
- overall

<img width="600" alt="Image" src="https://github.com/user-attachments/assets/fe0b4253-b2d2-4214-8586-ab4afd55dc64" />

Performance is better than w/o BF, and QwQ-32B seems to have similar overall performance.
AIME is relatively weak, and MATH500 is almost o1-level in performance. GPQA diamond and AIME seem to have ambiguous performance, but they are better than sky-t1 and weaker than bespoke and MATH. Overall, sample efficient, then contribution.

- budget forcing
<img width="597" alt="Image" src="https://github.com/user-attachments/assets/4ee742db-29fb-4132-b9fa-96649b58b80e" />

- filtering ablation 
<img width="577" alt="Image" src="https://github.com/user-attachments/assets/c42fb0e0-fd01-40ea-85e2-b9f3ce5a34f4" /> 

- w/ parallel scaling
<img width="1342" alt="Image" src="https://github.com/user-attachments/assets/0dadc20d-0902-40f3-92f2-7187804274f8" />

<img width="598" alt="Image" src="https://github.com/user-attachments/assets/08807b43-b02d-4b9f-afa3-4ad9bee1d6b8" />