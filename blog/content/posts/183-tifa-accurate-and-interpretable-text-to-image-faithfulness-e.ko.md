---
title: "[164] TIFA: Accurate and Interpretable Text-to-Image Faithfulness Evaluation with Question Answering"
date: 2024-07-18
tags: ['ICCV', 'evaluation', '2023Q3']
paper: "https://arxiv.org/abs/2303.11897"
issue: 183
issueUrl: "https://github.com/long8v/PTIR/issues/183"
---

<img width="689" alt="image" src="https://github.com/user-attachments/assets/e60da583-e89f-4cb1-baca-15e96a0c9c49">

[paper](https://arxiv.org/abs/2303.11897), [page](https://tifa-benchmark.github.io/), [code](https://github.com/Yushi-Hu/tifa)

## TL;DR
- **I read this because.. :** 개인 연구 관련 연구 
- **task :** faithful T2I evaluation
- **problem :** prompt에 맞게 이미지가 생성되었는가를 평가하기 위해 CLIPScore의 단점이 있음
- **idea :** VQA로 풀어보자!
- **input/output :** {image, text} -> score
- **architecture :** GPT-3 + UnifiedQA + VQA(mPLUG-large, BLIP-2.)
- **baseline :** CLIPScore
- **evaluation :** likert로 매겨진 human preference와 correlation
- **result :** 더 높은 correlation

## Details
### motivation
<img width="381" alt="image" src="https://github.com/user-attachments/assets/18f51f9d-35f8-4b6d-8c93-443b35c147ac">

### TIFA overview 
<img width="749" alt="image" src="https://github.com/user-attachments/assets/6647726d-79e3-40fd-8737-559231ba38fe">

metric은 VQA로 했을 때 정답을 몇개 맞췄는가
<img width="299" alt="image" src="https://github.com/user-attachments/assets/c1cbe65b-6a8f-4624-afab-46ec8dd06f28">

- GPT-3 prompt
<img width="357" alt="image" src="https://github.com/user-attachments/assets/87f9b184-b9f7-4287-befe-f9d422678649">

### TIFA detailed pipeline
<img width="763" alt="image" src="https://github.com/user-attachments/assets/468befd9-02b5-4f4a-bc56-db3a2c11388a">

#182 와 대동소이함! 다만 모든걸 GPT-3로 함 
deterministic하게 하기 위해 LLaMA-3도 재학습함.

Question Filtering은 unified QA
### TIFA v1.0 benchmark
<img width="364" alt="image" src="https://github.com/user-attachments/assets/6814df8e-c8df-4641-a54a-5b6fc48d45e5">

<img width="747" alt="image" src="https://github.com/user-attachments/assets/976782b1-4b22-481e-a521-5d4f7bdff8fd">

- Likert Score guideline
<img width="369" alt="image" src="https://github.com/user-attachments/assets/12d00d9e-49c6-4c23-9ed0-9a1dd397d30e">

<img width="384" alt="image" src="https://github.com/user-attachments/assets/e894f6b5-4455-45a1-905f-301e4dca0ec6">

- correlation between human preference
<img width="377" alt="image" src="https://github.com/user-attachments/assets/5efe2b58-bacf-4455-8675-2bd21d6b84e1">
