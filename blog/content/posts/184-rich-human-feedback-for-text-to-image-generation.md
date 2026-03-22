---
title: "[165] Rich Human Feedback for Text-to-Image Generation"
date: 2024-07-19
tags: ['CVPR', '2023Q4', 'evaluation']
paper: "https://arxiv.org/abs/2312.10240"
issue: 184
issueUrl: "https://github.com/long8v/PTIR/issues/184"
summary: "CVPR best paper. personal research related work - datasets, benchmarks, models, model improvements using those models... This should be the best paper...."
---
<img width="700" alt="image" src="https://github.com/user-attachments/assets/9f81142e-2354-4896-abc4-4ad178116633">

[paper](https://arxiv.org/abs/2312.10240)

## TL;DR
- **I read this because.. :** CVPR best paper. personal research related research.
- **task :** evaluation in T2I generation. score with feedback 
- Problem :** Traditional score-based methods are hard to interpret and don't tell you what you're doing wrong.
- Idea :** Given an image and text with human annotation, have human annotators annotate what is wrong, and give an aesthetic / alignment / plausible score in addition. A model trained on this.
- **input/output :** {image, text} -> 3 scores(aesthetic / alignment / plausible), tokens with align label, heatmap for misalignment
- **architecture :** ViT / T5X / SA
- **objective :** MSE (score and heatmap) + CE loss (misaligned token prediction) 
- **baseline :** (score) CLIPScore, PickScore, finetune CLIP, (heatmap) CLIP Gradient, 
- **data :** proposed Rich-hf 18K
- **evaluation :** (image heatmap) MSE(gt=0) or saliency heatmap evaluaton, (misaligned tokens) precision, recall, F1 (scores) spearman, kendall correlation
- **result :** Higher feedback than baseline. We used it to (1) filter data, (2) reward the image model, and (3) give a heatmap and suggest to regenerate it again to show performance improvement in three ways.
- **contribution :** Datasets, benchmarks, models, model improvements using those models... This should be the best paper...
- **etc. :**

## Details
### What to do? 
<img width="473" alt="image" src="https://github.com/user-attachments/assets/52c1c3cf-2829-44a8-ae5c-06bc81968ce2">

### architecture of rich feedback model
<img width="951" alt="image" src="https://github.com/user-attachments/assets/e6765de3-cf8b-4905-92e0-1998a619c8d7">

## Result
### performance of feedback model
<img width="984" alt="image" src="https://github.com/user-attachments/assets/7f93731f-6f33-4655-847a-a32396d0fe33">

<img width="444" alt="image" src="https://github.com/user-attachments/assets/ddd8f9b5-5122-4a66-8eed-34d5f20af263">

## Improved model with feeback model
- Results from a Muse model that ft only high scores / rewards as guidance
<img width="702" alt="image" src="https://github.com/user-attachments/assets/66ec71ae-ead4-4ac6-bf26-dd16de91b6d4">

- I gave them the wrong heatmap and asked them to redraw it.
<img width="972" alt="image" src="https://github.com/user-attachments/assets/d171f4e6-458c-4ca6-9b7b-e3a7f9ace634">

- Before and after finetune comparison
<img width="343" alt="image" src="https://github.com/user-attachments/assets/b262c2bc-cf45-4a08-8db9-7f7676e20324">
