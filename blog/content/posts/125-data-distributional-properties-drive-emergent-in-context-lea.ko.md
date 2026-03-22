---
title: "[116] Data Distributional Properties Drive Emergent In-Context Learning in Transformers"
date: 2023-05-22
tags: ['DeepMind', 'NeurIPS', '2022Q2']
paper: "https://arxiv.org/abs/2205.05055"
issue: 125
issueUrl: "https://github.com/long8v/PTIR/issues/125"
---
<img width="759" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/39c85c03-a4f7-4f3f-b502-3ebf8c64fba0">

[paper](https://arxiv.org/abs/2205.05055)

## TL;DR
- **I read this because.. :** CS330에서 나옴. LLM의 in-context learning을 meta learning과 연관지어 해석하기도 하는데 어떻게 생각하냐고 물어봤었는데 첨들었음 ㅋㅋ 이 논문이 그 내용인듯
- **problem :** in-context learning이 어떨 때 동작하는가? LLM의 "emergent" 능력이 언제 나타나는가?
- **idea :** natural data는 supervised data와 달리 
- **input/output :** {image, label} sequence + query image -> novel label
- **architecture :** encoder(ResNet) + causal Transformer
- **objective :** ce loss 
- **baseline :** RNN, LSTM  
- **data :** Omniglot
- **evaluation :** 8개의 context가 주어지고 1개의 test query가 주어질 때 잘분류했는지. 이때 "holdout image"(한번도 본 적 없는 이미지)에 대한 평가를 하기 위해서 4-shot 2-way 평가에서 이미지 2개의 class를 random으로 assign을 함(e.g. "a"라는 알파벳이 원래 label이 0으로 되어있었는데 test에는 1로 하는 그런 방식)
- **result :** 1) RNN은 안되고 Transformer model 일 때 2) 데이터에 busrtiness가 있을 때 3) a large set of rare classes일 때 등장한다
- **contribution :**
- **etc. :**

## Details
### in-context learning vs in-weight learning
- in-context learning은 weight update없이 새로운 개념의 몇개의 sample만 주어져도 잘하는 것 
- in-weight learning은 gradient update를 해서 supervised learning으로 few shot 잘하는거
meta learning의 관점에서 MANN이나 MAML이 in-context learning이라고 볼 수 있음. 근데 최근의 LLM에서 이런 in-context learning이 직접적으로 학습되지 않았는데 "emergent"했는데 이게 왜 때문일까?

### Experimental design
<img width="564" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0b4361e3-f81a-4c2e-9117-c89685831331">

black box meta learning 방법론 처럼 image, label 시퀀스가 context로 주어지고 쿼리 이미지가 들어왔을 때 잘 하는지 보는게 in-context learning. 
- bursty는 특정 class가 뭉쳐서 들어오는거 (aa a 가 짧은 기간 내에 뭉쳐서 나옴)

이 논문에서는 1) burstiness 2) a large number of rarely occuring classes 3) multiplicity of labels 4) within-class variation으로 보았음

### Burstiness
위의 예시처럼 일부러 busrtiness를 늘린 데이터로 평가해보니 in-context learning의 경우 burstiness가 늘어나면 
반대로 in-weight learning은 busrtiness가 늘어나면 성능이 안좋아짐
<img width="737" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ae27b780-3a51-4525-bcfd-99e2b3c31364">

### a large number of rarely occuring classes
omniglot을 roatation을 줘가면서 num of classes를 100에서 12800(원래 클래스 1600)까지 늘려가면서 (각 class의 frequency는 줄어서 long-tail 해지는)실험을 해보았다. 
number of classes가 또 역시 반대로 in context learning은 많을 수록 좋았는데 반대로 in weight learning은 많을 수록 안좋았다.
<img width="745" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d001758f-d940-4962-9fc1-2aea2313297a">

### Multiplicity of labels
한 클래스에 대한 label을 여러개로 주면서 해봤을 때 역시 성능이 좋아졌다
<img width="400" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/cad4d01b-721f-49a5-b98d-4291daf1a1c7">


### within-class variation
classs내의 variation을 많이 줘봤는데 이것도 in-context learning 의 경우 variation이 높을 수록 성능이 좋았다
<img width="731" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/84c346df-d8b3-4cea-8c6b-ccd9f374378a">

### Architecture

<img width="714" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/fe79568e-2a94-4908-b9f7-3006122690d3">

파라미터 수 / depth 등등 다 맞춰서 rnn / lstm 돌렸는데 절대로 in-context learning ability가 나타나지 않았다고.. 
왠지는 저자들도 모르겠다 함!
we were completely unable to elicit in-context learning in recurrent models, even with the training procedure, number of
parameters, and model architecture otherwise matched to the transformer experiments. 
transformer만 쓴다고 in-context learning이 되는건 아니고 data distribution이 위의 저 3개의 특성을 가져야만 나타난다고 강조.