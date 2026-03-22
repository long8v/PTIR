---
title: "TIFA: Accurate and Interpretable Text-to-Image Faithfulness Evaluation with Question Answering"
date: 2024-07-18
tags: ['ICCV', 'evaluation', '2023Q3']
paper: "https://arxiv.org/abs/2303.11897"
issue: 183
issueUrl: "https://github.com/long8v/PTIR/issues/183"
summary: "Personal research related studies - higher correlation"
---

<img width="689" alt="image" src="https://github.com/user-attachments/assets/e60da583-e89f-4cb1-baca-15e96a0c9c49">

[paper](https://arxiv.org/abs/2303.11897), [page](https://tifa-benchmark.github.io/), [code](https://github.com/Yushi-Hu/tifa)

## TL;DR
- **I read this because... :** Personal Research Related Research
- **task :** faithful T2I evaluation
- Problem :** Shortcomings of CLIPScore to evaluate whether an image was created to fit the prompt
- **idea :** Let's solve it with VQA!
- **input/output :** {image, text} -> score
- **architecture :** GPT-3 + UnifiedQA + VQA(mPLUG-large, BLIP-2.)
- **baseline :** CLIPScore
- **evaluation :** correlation with likert-scaled human preference
- **result :** higher correlation

## Details
### motivation
<img width="381" alt="image" src="https://github.com/user-attachments/assets/18f51f9d-35f8-4b6d-8c93-443b35c147ac">

### TIFA overview 
<img width="749" alt="image" src="https://github.com/user-attachments/assets/6647726d-79e3-40fd-8737-559231ba38fe">

metric is how many answers are correct when VQA'ed
<img width="299" alt="image" src="https://github.com/user-attachments/assets/c1cbe65b-6a8f-4624-afab-46ec8dd06f28">

- GPT-3 prompt
<img width="357" alt="image" src="https://github.com/user-attachments/assets/87f9b184-b9f7-4287-befe-f9d422678649">

### TIFA detailed pipeline
<img width="763" alt="image" src="https://github.com/user-attachments/assets/468befd9-02b5-4f4a-bc56-db3a2c11388a">

Same as #182, but with everything in GPT-3
LLaMA-3 is also retrained to make it deterministic.

Question Filtering is a unified QA
### TIFA v1.0 benchmark
<img width="364" alt="image" src="https://github.com/user-attachments/assets/6814df8e-c8df-4641-a54a-5b6fc48d45e5">

<img width="747" alt="image" src="https://github.com/user-attachments/assets/976782b1-4b22-481e-a521-5d4f7bdff8fd">

- Likert Score guideline
<img width="369" alt="image" src="https://github.com/user-attachments/assets/12d00d9e-49c6-4c23-9ed0-9a1dd397d30e">

<img width="384" alt="image" src="https://github.com/user-attachments/assets/e894f6b5-4455-45a1-905f-301e4dca0ec6">

- correlation between human preference
<img width="377" alt="image" src="https://github.com/user-attachments/assets/5efe2b58-bacf-4455-8675-2bd21d6b84e1">
