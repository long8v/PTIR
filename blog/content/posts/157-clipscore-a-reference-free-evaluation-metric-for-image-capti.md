---
title: "[145] CLIPScore: A Reference-free Evaluation Metric for Image Captioning"
date: 2024-02-05
tags: ['2021Q2', 'CLIP', 'emnlp', 'evaluation', 'AI2']
paper: "https://arxiv.org/abs/2104.08718"
issue: 157
issueUrl: "https://github.com/long8v/PTIR/issues/157"
summary: "Interested in clip score - simple, old referecne-based metric suggestion to improve evaluation! Makes analyzing huge."
---
<img width="764" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a6080f82-cf65-4ead-beb6-bcb23f237fc7">

[paper](https://arxiv.org/abs/2104.08718)

## TL;DR
- **I read this because.. :** I'm interested in clip scores.
- **task :** evaluation for captioning 
- **problem :** Previous reference-based evaluations tend to be biased towards familiar words
- **idea :** CLIP score Write and rate!
- **input/output :** {image, caption, (optionally) references} -> score
- **architecture :** CLIP ViT-B/32
- **baseline :** BLEU-1, BLEU-4, ROUGE-L, BERT-score, CIDEr, SPICE
- **data :** Flickr8K-Expert, Flickr-CF, Pascal-50S, FOIL hallucination detection,
- **evaluation :** kendall correlation with human judgement(Flickr8K-Expert, Flickr-CF). accuracy(Pascal-50S, FOIL)
- **result :** One of the metrics that is always selected when forward selection is made with the highest correlation with human judgment, high accuracy, and captioning scores.
- **contribution :** Proposed a metric to improve the evaluation based on simple and old referecne! Makes the analysis massive.
- **etc. :** If the idea is simple, this is the level of analysis I need to do to write a paper.

## Details
### motivation
<img width="339" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ca89da34-46d9-442b-913e-a3d46d097a59">

### `CLIPScore`
<img width="293" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/dafccd53-c341-4c9c-b0c6-49e6acfe2c1d">

- c: CLIP text embedding in caption
- v: CLIP vision embedding in image
- w is set to 2.5 A rescaling scalar added just for ease of interpretation.
- cosine should theoretically have a scale of [-1, 1], but I've never seen negative
- Multiply by 2.5 to make it [0, 1] because score always seems to be between [0, 0.4].
State in footnote that region-leval/token-level correspondence models (maybe FILIP?!) did not perform better.

### `RefCLIP-s`
A version that also utilizes referecne caption.

<img width="347" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5589936d-747f-45f7-8a57-5dabf4fbdf3f">

- r: CLIP text embedding in referecnes

### Caption-level likert judgements
- Flickr8K-Expert 
17K "expert" humans scored the captions on 5664 images on a scale of 1 to 4 (1 unrelated to 4 well rated with no errors)
<img width="350" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4a310f1e-521b-4d13-93ad-7d5df83c45b8">

[leaderboard]((https://paperswithcode.com/sota/human-judgment-correlation-on-flickr8k-expert))
Oh this benchmark #1 is Naver paper... [Mutual Information Divergence: A Unified Metric for Multimodal Generative Models](https://arxiv.org/pdf/2205.13445v1.pdf)

- Flickr8K-CF
Dataset of crowd-sourced judgments in binary for 48K {image, caption} pairs for 1K images
<img width="354" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/34c0a1d0-befe-4d88-a376-8d2dd48d516f">

- Composite https://arxiv.org/pdf/1511.03292.pdf
12K of human judgment on MSCOCO, Flickr8K, and Flickr30K
<img width="363" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/477076a7-4f35-4c2e-b220-dfbaf1cfb844">

### System-level correlation for MSCOCO
How do COCO captioners compare to the results?
You say you only have 12 pieces of data

### Sensitivity of CLIP-S to hallucination
Human evaluation is more influenced by "correctness" than "specificity"
To evaluate this, we use the hallucination dataset, FOIL (https://arxiv.org/pdf/1705.01359.pdf)
In MSCOCO, substituting a noun for a similar word in a single noun phrase (e.g., switching "motorcycle" for "bicycle").
For 32K sentences, evaluated whether the substituted sentence scored higher than the non-substituted sentence.

<img width="415" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c63c7050-9cb7-4fc9-9652-9426c8bb0e64">

### Sensitivity of CLIP-S to memorization
Collecting datasets myself in case I learned captions in the CLIP training course

### Which metrics should I report?
- Forward selection for 10 metrics based on R2.
- BLEU-1, BLEU-4, METEOR, CIDEr, ROUGE-L, SPICE, BERT-S(RoBERTa-F), TIGEr, ViLBERTScore-F, and CLIP-S
<img width="403" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/707a9bb4-4938-4525-afee-e627fb1160d7">

Confirm that at least the top four are selected
It also ensures that metrics are correlated but not redundant.
It would be better to use it with a reference base like SPICE.

