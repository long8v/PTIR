---
title: "[165] Rich Human Feedback for Text-to-Image Generation"
date: 2024-07-19
tags: ['CVPR', '2023Q4', 'evaluation']
paper: "https://arxiv.org/abs/2312.10240"
issue: 184
issueUrl: "https://github.com/long8v/PTIR/issues/184"
---
<img width="700" alt="image" src="https://github.com/user-attachments/assets/9f81142e-2354-4896-abc4-4ad178116633">

[paper](https://arxiv.org/abs/2312.10240)

## TL;DR
- **I read this because.. :** CVPR best paper. 개인 연구 관련 연구 
- **task :** evaluation in T2I generation. score with feedback 
- **problem :** 기존의 score 기반의 방법은 해석이 어렵고, 어떤 부분이 틀렸는지 알려줄 수 없다
- **idea :** human annotation으로 이미지와 텍스트가 주어졌을 때 틀린 부분을 annotate, 외에 aesthetic / alignment / plausible score를 매기게 함. 이를 학습한 모델.
- **input/output :** {image, text} -> 3 scores(aesthetic / alignment / plausible), tokens with align label, heatmap for misalignment
- **architecture :** ViT / T5X / SA
- **objective :** MSE (score and heatmap) + CE loss (misaligned token prediction) 
- **baseline :** (score) CLIPScore, PickScore, finetune CLIP, (heatmap) CLIP Gradient, 
- **data :** proposed Rich-hf 18K
- **evaluation :** (image heatmap) MSE(gt=0) or saliency heatmap evaluaton, (misaligned tokens) precision, recall, F1 (scores) spearman, kendall correlation
- **result :** baseline보다 더 높은 피드백. 이를 활용하여 (1) data filtering 에 사용 (2) image model의 reward로 사용 (3) heatmap을 준 뒤 다시 생성하라고 제안 세가지로 성능 개선을 나타냄.
- **contribution :** 데이터셋, 벤치마크, 모델, 그 모델을 사용한 모델 개선.. 이정도는 써야 best paper..
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

## feeback model로 개선된 모델
- 높은 score만 남겨서 ft 한 Muse 모델 / reward를 guidance로 준 모델 결과
<img width="702" alt="image" src="https://github.com/user-attachments/assets/66ec71ae-ead4-4ac6-bf26-dd16de91b6d4">

- 틀린 heatmap 주고 다시 뽑아보라고 한 결과
<img width="972" alt="image" src="https://github.com/user-attachments/assets/d171f4e6-458c-4ca6-9b7b-e3a7f9ace634">

- finetune 전 후 비교한 결과
<img width="343" alt="image" src="https://github.com/user-attachments/assets/b262c2bc-cf45-4a08-8db9-7f7676e20324">
