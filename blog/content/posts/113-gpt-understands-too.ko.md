---
title: "[104] GPT Understands, too"
date: 2023-03-23
tags: ['2021Q1', 'prompt', 'GPT', 'finetuning', 'LLM']
paper: "https://arxiv.org/pdf/2103.10385.pdf"
issue: 113
issueUrl: "https://github.com/long8v/PTIR/issues/113"
---
<img width="857" alt="image" src="https://user-images.githubusercontent.com/46675408/227085867-d5ceaf17-37ad-4409-95f3-18f24783bb53.png">

[paper](https://arxiv.org/pdf/2103.10385.pdf)

## TL;DR
- **I read this because.. :** 허깅페이스의 parameter efficient finetuning 레포의 article 보다가 읽음. p-tuning 많이 들어봤는데 읽어본적이 없었음
- **task :** language model finetuning(Knowledge probing, ...)
- **problem :** LLM을 finetuning 할 때 파라미터가 너무 커서 few-shot 셋팅이나 many-shot setting이나 trasnfer 능력이 떨어진다. GPT-3  에다가 좋은 prompt를 넣으면 되는데 좋은 prompt를 찾는게 공수가 너무 크고, prompt에 따라 성능도 들쭉날쭉하다.
- **idea :** prompt를 discrete하게 찾지 말고 continuous 공간에서 찾자
- **architecture :** BERT / GPT 등 LLM에 template {pseudo-prompt $P_{0:i}$, $\mathbf{x}$, $P_{i+1:m}$, $\mathbf{e(y)}$ }를 넣고 각 psudo-prompt의 임베딩을 학습. 이때 prompt 임베딩이 서로 의존적으로 학습됐으면 해서 bi-LSTM 레이어를 넣어서 임베딩 강화.
- **objective :** MLM loss 
- **baseline :** manual prompt, fiene-tuning, discrete prompt searching, manual prompt + finetuning 
- **data :** LAMA, SuperGLUE
- **evaluation :** accuracy, F1, ... 
- **result :** gpt / bert based model에서 GLUE의 대부분의 태스크에서 더 나은 성능! (finetune도 이김)
- **contribution :** manual한 prompt search를 continuous 영역으로
- **limitation / things I cannot understand :** prompt CIL 이것도 좀 생각나는 것 같고.. MTL 환경에서 p-tuning 적용해보고 싶다는 생각이 드넹

## Details
<img width="845" alt="image" src="https://user-images.githubusercontent.com/46675408/227093898-ffaae65f-7e21-4917-9af0-256667873e82.png">

<img width="428" alt="image" src="https://user-images.githubusercontent.com/46675408/227094093-7c460d2c-c79b-484d-b955-d2d97e42f93c.png">

- $\mathcal{M}$ : pretrained LM

이렇게 학습시킬 때 두가지 문제가 있는데 1) 이미 pretrained LM $\mathcal{M}$의 임베딩 공간 $\mathbf{e}$가 discrete 해서 $h$가 random initialize 되면 small neighborhood 들의 파라미터만 수정되고 local minima에 빠지기 쉽다는 거고 2) prompt 토큰들끼리 dependent 하길 원한다는 점이다.
이를 해결하기 위해 lite한 네트워크 하나를 추가한다.
<img width="527" alt="image" src="https://user-images.githubusercontent.com/46675408/227097887-2d0e476a-ae24-4ff7-8df0-10dab5a386e5.png">

LSTM이 추가되긴 하지만 LM에 비하면 파라미터는 거의 없고 inference 단계에서는 lstm은 그냥 버리고 학습된 임베딩 h만 쓰면 된다.

<img width="383" alt="image" src="https://user-images.githubusercontent.com/46675408/227094364-3b8822e3-6652-4b6e-bf64-93688e6ea510.png">

### Result
<img width="853" alt="image" src="https://user-images.githubusercontent.com/46675408/227094008-ba763425-697d-48d3-b1fc-c991d86abe0a.png">

p-tuning은 language model의 파라미터는 freeze
finetuning을 이기는게 신기하군요

<img width="865" alt="image" src="https://user-images.githubusercontent.com/46675408/227098059-876a8628-9365-430a-96f2-7d4fd30fa332.png">

### 후속연구
P-Tuning v2: Prompt Tuning Can Be Comparable to Fine-tuning Universally Across Scales and Tasks
각 레이어마다 prompt token 넣는걸 기존 p-tuning에서 잘 못했던 hard sequence labeling tasks도 잘하는걸 보임 / 작은 모델에서도 동작하는걸 밝힘
https://arxiv.org/pdf/2110.07602.pdf
<img width="923" alt="image" src="https://user-images.githubusercontent.com/46675408/228109125-5ba4c333-8af1-4c36-b58e-7ebb02c7af4c.png">

