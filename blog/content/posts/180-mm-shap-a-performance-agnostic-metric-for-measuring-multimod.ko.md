---
title: "[161] MM-SHAP: A Performance-agnostic Metric for Measuring Multimodal Contributions in Vision and Language Models & Tasks"
date: 2024-07-09
tags: ['25min', '2022Q4', 'XAI', 'ACL']
paper: "https://arxiv.org/pdf/2212.08158"
issue: 180
issueUrl: "https://github.com/long8v/PTIR/issues/180"
---
<img width="617" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c567aeef-429d-408e-8d76-6295277063e5">

[paper](https://arxiv.org/pdf/2212.08158), [code](https://github.com/Heidelberg-NLP/MM-SHAP)

## TL;DR
- **I read this because.. :** 개인 연구 관련 연구
- **task :** VLM 모델들이 vision 또는 language에 너무 치중하지 않는지 측정해보자
- **problem :** 기존의 occulsion + accuracy based 방법론은 어떤 modality에 치중했는지를 정확히 측정하지 못한다. 
- **idea :** 모델의 정확도가 아니라 얼마나 모델 예측에 영향을 미쳤는지에 대한 score를 매기자
- **input/output :** {image, text} -> 각 modality에 대한 score(positive, negative, neutral)
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

CLIP은 틀린 단어(`keyboard`)에 대해 negative 점수를 주지 못한다.
### SHAP
게임이론의 shapley 기반이라고 하넹
<img width="310" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f5a5aa5b-2edc-48f6-9668-95d044eb13b6">

<img width="311" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1996afb7-30a0-40ee-96de-427d75d52e28">

occulsion based랑 비슷한데 각 토큰이 아니라 토큰 조합까지 subset으로 만들어서 occulde 하는 방식.
너무 조합이 많으니까 subsampling해서 사용 

### why not attention based?
<img width="312" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b8dc6681-f574-4009-9d64-1ded536fb29d">

cheferCAM은 negative 못본다! 

<img width="559" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1036daf4-7b0d-40a5-91ce-5cf37ba7cd40">
