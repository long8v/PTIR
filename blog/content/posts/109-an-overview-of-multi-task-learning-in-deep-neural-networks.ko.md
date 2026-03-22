---
title: "[100] An Overview of Multi-Task Learning in Deep Neural Networks"
date: 2023-01-26
tags: ['2017', 'survey', 'MTL']
paper: "https://arxiv.org/pdf/1706.05098.pdf"
issue: 109
issueUrl: "https://github.com/long8v/PTIR/issues/109"
---
![image](https://user-images.githubusercontent.com/46675408/214748723-8079957a-c9a2-455a-9b96-fe7b1a87f9ee.png)

[paper](https://arxiv.org/pdf/1706.05098.pdf)

## Details
### Multi-task Learning
왜 잘되는가?
1) 한 태스크에 대한 오버피팅을 막으며 2) 데이터 어그멘테이션 효과 3) "inductive bias"를 학습 4) 좋은 feature를 학습 

### hard parameter sharing vs soft parameter sharing
- hard parameter sharing 
![image](https://user-images.githubusercontent.com/46675408/214749097-c570c580-e4d9-404d-ae4a-c657bb4ee6d6.png)

보통 생각하는 MTL 모델 구조

- soft parameter sharing 
![image](https://user-images.githubusercontent.com/46675408/214749186-203a400e-c08d-461c-a7b9-c76d24d0b9fb.png)

각각 태스크에 맞는 네트워크를 쌓고 각 네트워크의 파라미터가 너무 달라지지 않도록 L2 norm loss를 부과

## Recent work on MTL for deep learning
- Deep Relationship Networks
FCN에 matrix prior를 부과해서 모델이 태스크 간의 relationship을 학습할 수 있게 함 
![image](https://user-images.githubusercontent.com/46675408/214749521-71a0e948-a0b6-400c-9294-49c2f7833d3d.png)

- Cross-stitch network
<img width="556" alt="image" src="https://user-images.githubusercontent.com/46675408/214749670-61fe869e-eee4-45df-9621-b888c7ea1411.png">

태스크별로 별도의 네트워크가 있고 각 네트워크의 파라미터가 학습 가능한 $\alpha$만큼 linear combination 되도록 

- Weighting losses with uncertainty 
<img width="812" alt="image" src="https://user-images.githubusercontent.com/46675408/214749829-f1d5ceff-6e8d-4584-9e66-0dfc3cff70af.png">

각 task의 Uncertainty를 측정하고 multi-task loss function에 상대적인 weight 추가 -> 이거 읽으면 좋을듯!

### Auxiliary tasks
- related task
관련 있는 태스크면 더 좋음
- adversarial
갖고 싶은 것의 반대를 통해서 학습. 가령 Domain adaptation에서 인풋의 도메인을 예측하고 adversarial task의 그래디언트를 Reverse해서 사용하는 연구? Ganin, 2015
- 힌트
조금 더 쉬운 태스크를 사용. 가령 문장의 감정 예측을 하는 태스크를 긍정/부정으로 나눠서 학습 -> connectivity 실험 생각나넹!
- Representation learning
결국 좋은 표현을 만들기 위함이니 Representation을 잘만드는 것도 auxiliary task가 될 수 있음. 가령 language modeling이나 autoencoder가 그 예시.

### 걍 느낀 점
BERT가 정말 파괴적이구나 느낌 ㅋㅋ 