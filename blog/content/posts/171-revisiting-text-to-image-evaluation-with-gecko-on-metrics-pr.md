---
title: "[155] Revisiting Text-to-Image Evaluation with Gecko: On Metrics, Prompts, and Human Ratings"
date: 2024-05-03
tags: ['google', 'evaluation', 'generation', '2024Q2']
paper: "https://arxiv.org/pdf/2404.16820"
issue: 171
issueUrl: "https://github.com/long8v/PTIR/issues/171"
summary: "I read that it's a T2I evaluation and there's word-level stuff. - Data suggestions. word-level annotation."
---

<img width="660" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4f0a737d-6668-4dda-9281-b0c1666af9f1">

[paper](https://arxiv.org/pdf/2404.16820), [code](https://github.com/google-deepmind/gecko_benchmark_t2i)

## TL;DR
- **I read this because.. :** T2I evaluation and word-level blah blah blah.
- **task :** T2I evaluation
- **problem :** Existing DSG, QG2 methodology causes hallucination of LLM. changes the way skill behaves.
- **IDEA:** A slightly different way of calling skill.
- **input/output :** {image, text} -> score 
- **architecture :** PALM (QA) + PALI (VQA)  
- **baseline :** METEOR, SPICE, CLIP, TIFA, DSG
- **data :** proposed Gecko2k
- **evaluation :** proposed Gecko
- **result :** Human correlation is higher than other metrics.
- **contribution :** Data suggestions. word-level annotation.
- **etc. :** I'm not sure how I did after getting the word-level annotation. Is it just that it was better than the likert (absolute score) annotation?

## Details

### problems in DSG 

<img width="685" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1dce9e46-d2f7-4e91-8f65-050eebe25171">

<img width="652" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/489d0c1d-21f1-4a56-ba5e-8048684e9b1a">

### proposed 
<img width="869" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ff7fb2a9-ae8f-414c-9722-279460a2e59c">

### result
<img width="662" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/241b0f5d-2729-436d-8ae9-5b06b22fe20b">

I was really curious about how you measured WL in CLIP here, so I read the paper... and I saw that the metric was Spearman.
We did word-level annotation, and then we did something like a score average with that, and then we scored {image, caption}, and then we just saw how close it was to human preference.

### word-level annotation 
<img width="677" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3bc0dff0-3a7e-4320-bbc1-860fc7b5e76a">

<img width="677" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4be56ae2-dda6-47f2-8124-5c0dbbd7df9d">

### Evaluate performance for different CLIP models
<img width="671" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e5e99846-70a0-4514-b935-eee569c39803">

SigLIP is nice.
For the same model, the data view was better
Not in all cases, but the larger models were better.

For a pyramid CLIP, it looks like this
<img width="549" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0be17af5-15ca-4952-ab9e-027c83a2b600">


