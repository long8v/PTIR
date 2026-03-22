---
title: "MM-SHAP: A Performance-agnostic Metric for Measuring Multimodal Contributions in Vision and Language Models & Tasks"
date: 2024-07-09
tags: ['25min', '2022Q4', 'XAI', 'ACL']
paper: "https://arxiv.org/pdf/2212.08158"
issue: 180
issueUrl: "https://github.com/long8v/PTIR/issues/180"
summary: "Research related to personal studies - - -"
---
<img width="617" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c567aeef-429d-408e-8d76-6295277063e5">

[paper](https://arxiv.org/pdf/2212.08158), [code](https://github.com/Heidelberg-NLP/MM-SHAP)

## TL;DR
- **I read this because... :** Personal Research Related Research
- **task :** Measure if VLM models are too focused on vision or language
- Problem :** Traditional occulsion + accuracy based methodologies do not accurately measure which modality was emphasized.
- **IDEA:** Score your model not on its accuracy, but on how much you influenced the model's predictions.
- **input/output :** {image, text} -> score(positive, negative, neutral) for each modality
- **architecture :** ALBEF, CLIP, LXMERT, 4 VQA models 
- **baseline :** task accuracy
- **data :** VQA, GQA, Image-sentence alignment(VQA, GQA), [VALSE](https://arxiv.org/pdf/2112.07566), FOIL
- **evaluation :** T-SHAP, V-SHAP
- **result :** - 
- **contribution :**
- **etc. :**

## Details
### motivation
<img width="312" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7d57dad7-62be-4193-9512-c2227eba044d">

CLIP cannot give negative points for incorrect words (`keyboard`).
### SHAP
It's called the shapley basis of game theory.
<img width="310" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f5a5aa5b-2edc-48f6-9668-95d044eb13b6">

<img width="311" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1996afb7-30a0-40ee-96de-427d75d52e28">

Similar to occulsion based, but instead of each token, it makes a subset of token combinations to occulde.
Too many combinations, so use subsampling

### why not attention based?
<img width="312" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b8dc6681-f574-4009-9d64-1ded536fb29d">

cheferCAM does not see negatives!

<img width="559" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1036daf4-7b0d-40a5-91ce-5cf37ba7cd40">
