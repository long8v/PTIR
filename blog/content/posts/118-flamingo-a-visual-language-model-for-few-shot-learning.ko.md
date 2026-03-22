---
title: "[109] 🦩 Flamingo: a Visual Language Model for Few-Shot Learning"
date: 2023-04-10
tags: ['multimodal', 'DeepMind', 'LLM']
paper: "https://arxiv.org/pdf/2204.14198.pdf"
issue: 118
issueUrl: "https://github.com/long8v/PTIR/issues/118"
---
<img width="762" alt="image" src="https://user-images.githubusercontent.com/46675408/230816882-9ca1b993-82ac-4408-b481-5893ff3ab715.png">

[paper](https://arxiv.org/pdf/2204.14198.pdf)

## TL;DR
- **I read this because.. :** #116 읽고 나서 읽고 싶어짐. 예전에 성현님이 소개해주셨는데 디테일 모름. GPT 열풍으로 요즘 다시 많이 언급됨.
- **task :** Vision Language Model in general use! VQA, object detction, VizWiz, HatefulMemes ...
- **input** : text with image/video
- **output** : free form of text
- **problem :** CLIP 류는 image-text pair의 score만 나오므로 이미지 분류와 같은 closed set에 대한 태스크에만 적용이 가능하다. cpationing이나 VQA 같은 open-ended task를 풀 수 있는 generate language 능력이 부족하다. 
- **idea :** LM 방식으로! pretrained LLM 가져오고 visual token을 cross-attention으로 정보를 넣어주자
- **architecture :** LM은 일단 chinchilller(70B). 이미지 인풋은 NFNet에 넣고 마지막 feature flattent 한 뒤 Perceiver resampler로 few latent vector를 뽑음. LM 중간에 cross attention(train from scratch)로 visual 정보를 넣어줌. 안정적인 학습을 위해 0으로 초기화 되는 alpha로 tanh gating함.
- **objective :** NLL loss given image. 각 텍스튼 토큰은 직전의 image만 볼 수 있음. 각 데이터들의 weighted sum. 
- **baseline :** 각 벤치마크의 few-shot / finetune 모델
- **data :** MultiModal MassiveWeb(M3W, 1.8B), ALIGN(312M), Video & Text pairs(VTP, 27M)(딥러닝 학습의 목적으로 annotate된 데이터를 하나도 쓰지 않았다는 것에 의의!) -> 16개의 image/video and language 벤치마크 데이터
- **evaluation :** zero-shot / 32-shot에서 비교
- **result :** 대부분의 few-shot 모델에 대해 flamingo하나로 이기고. finetune 성능도 이긴 벤치마크 다수
- **contribution :** 아마 최초의 token generation 기반 vision & language 모델?
- **limitation / things I cannot understand :**

## Details
- ECCV workshop 때 Jean-Baptiste가 flamingo를 하게 된 이유 / 하면서 느낀 점을 소개해준 적이 있음
<img width="350" alt="image" src="https://user-images.githubusercontent.com/46675408/230821196-a747f1c7-7416-482c-b7c5-caef8a119b6d.png">

introduction에 써있는거랑 비슷한 내용. CLIP류 연구를 했었는데 풀 수 있는 task가 한정적이었다. -> flamingo로 넘어감
결국 어떤 인터페이스가 다양한 태스크를 풀 수 있을 것인가? application에 적합할 것인가?를 문제의식으로 삼은 것 같당
문제 의식을 아키텍쳐가 아니라 풀 수 있는 task 들로 잡은 듯~ 흠 점점 아키텍쳐가 중요한게 아니라 데이터/학습/태스크 등이 중요한 것 같네.. 나는 이제 무얼 쌓아야 하나 

### Preliminaries 
- Normalizer Free ResNet
https://arxiv.org/pdf/2102.06171.pdf
ResNet의 batch norm이 모델이 bs에 민감해지거나, 한 배치 내 이미지의 interaction에 영향을 받게 하는 효과가 있어서 이를 해결하기 위한 모델

- Perceiver
https://arxiv.org/pdf/2103.03206.pdf
<img width="680" alt="image" src="https://user-images.githubusercontent.com/46675408/230818470-037388bc-cec2-465b-8a53-f5350bdfc903.png">

21년도 deep mind에서 image / video 등 다양한 modality를 효율적으로 표현할 수 있게.
비대칭적인 attention 모듈을 사용해서 a small set of latent units으로 점차 CA할 수 있도록(detr이랑 비슷한데 디테일이 좀 다를듯)
image classification / audio / point cloud 등에서 comparable 성능
(c.f. Set Transformer가 most related work라고 하면서 계속 언급)

- Chinchiller
22년 3월에 딥마인드에서 나온 모델. https://arxiv.org/pdf/2203.15556.pdf
전작이 Gopher였는데 모델 사이즈만 커지고 학습 데이터는 그대로 써서 모델이 underfit 됐다고 판단.
`By training over 400 language models ranging from 70 million to over 16 billion
parameters on 5 to 500 billion tokens, we find that for compute-optimal training, the model size and
the number of training tokens should be scaled equally: for every doubling of model size the number
of training tokens should also be doubled.` ... 미친 넘들!
model size를 두배 늘리면 num of tokens도 두배로 늘려야 한다는 발견
Gopher(280B)보다 파라미터 수는 4배 작지만 training data는 4배 늘려서 Gopher의 성능을 이긴 모델

<img width="678" alt="image" src="https://user-images.githubusercontent.com/46675408/231033661-03e0856c-87c8-44b5-9728-1b4e528cefc9.png">


<img width="660" alt="image" src="https://user-images.githubusercontent.com/46675408/231033541-54cb24a3-9551-4fd5-bd35-0cdabb6883f9.png">

학습 중간에 배치 사이즈를 키움 -> 왜? https://arxiv.org/pdf/2112.11446.pdf 120쪽짜리 읽으면 알 수 있을듯..

### Dataset
<img width="703" alt="image" src="https://user-images.githubusercontent.com/46675408/231052318-20b27b3b-17a6-4245-8daa-2e0e35b76e53.png">

- M3W 
43M 웹페이지에서 HTML을 통해 이미지-텍스트를 뽑음. DOM 구조를 통해 상대적인 위치를 뽑음
텍스트 내에 <image> token을 넣어서 이미지의 위치를 넣었고 <EOC>(end of chunk) 토큰을 이미지 전 / 문서 마지막에 넣었음.
각 문서에 대해서 subsequence L=256개(너무 작은데? 각 이미지 앞에서 말하는거겠징?)의 토큰을 랜덤으로 뽑았고 최대 5개의 이미지를 넣었음

- ALIGN
web에 alt text(tag)라는게 있는데 그거 사용해서 구축한 데이터
https://ai.googleblog.com/2021/05/align-scaling-up-visual-and-vision.html
<img width="678" alt="image" src="https://user-images.githubusercontent.com/46675408/231045474-3af6164f-2678-4bf0-9162-c6035845d6e7.png">
<img width="625" alt="image" src="https://user-images.githubusercontent.com/46675408/231045493-392d6dc0-98aa-491c-bddb-a56d2e595df2.png">

### Architecture

<img width="575" alt="image" src="https://user-images.githubusercontent.com/46675408/231044078-f03216c8-43da-4d7c-b9eb-6bb135141de6.png">

<img width="724" alt="image" src="https://user-images.githubusercontent.com/46675408/231052266-64d77f18-20c2-4881-b0ae-9e44ba852967.png">

<img width="716" alt="image" src="https://user-images.githubusercontent.com/46675408/231044741-e2638df8-93c1-428f-b0b1-8debabdb1c66.png">

<img width="544" alt="image" src="https://user-images.githubusercontent.com/46675408/231044117-861a99be-5324-4146-ab80-30721328f7af.png">


<img width="551" alt="image" src="https://user-images.githubusercontent.com/46675408/231044184-e0bfa4c6-6739-4afd-ac7c-2bc128184401.png">


### Objective
<img width="353" alt="image" src="https://user-images.githubusercontent.com/46675408/231044583-c416bd60-0470-4cf1-af84-81369004832e.png">

각 데이터에 대한 gradient를 accumulate하는게 순차적(round-robin)으로 하는것보다 더 좋았음
그리고 per-dataset weights인 $\lambda _m$을 튜닝하는게 성능에 크리티컬했다고 하넹

### Results
<img width="560" alt="image" src="https://user-images.githubusercontent.com/46675408/231044274-37e48e09-85bc-478f-a386-4b39e1f41938.png">
<img width="563" alt="image" src="https://user-images.githubusercontent.com/46675408/231044312-53653372-8656-4fd8-8dcb-9172e7b60d79.png">
<img width="458" alt="image" src="https://user-images.githubusercontent.com/46675408/231044366-840e5959-ccc0-43b3-aad9-5f777fb7ced0.png">


Tanh gating 
<img width="550" alt="image" src="https://user-images.githubusercontent.com/46675408/231044222-32e39014-fbd6-4f10-919d-fd60edf2a71a.png">

### etc.
c.f. x-attn에서 x가 뭐지 하고 검색하다 발견
전체 finetuning 안하고 CA쪽만 해도 성능이 좋다는 논문. domain은 MT
Cross-Attention is All You Need:  Adapting Pretrained Transformers for Machine Translation
https://arxiv.org/pdf/2104.08771.pdf
