---
title: "[54] Branch-Train-Merge: Embarrassingly Parallel Training of Expert Language Models"
date: 2022-08-25
tags: ['LM', 'MoE', '2022Q3', '25min']
paper: "https://arxiv.org/pdf/2208.03306.pdf"
issue: 60
issueUrl: "https://github.com/long8v/PTIR/issues/60"
---
![image](https://user-images.githubusercontent.com/46675408/186548736-7d4ffaae-1079-4434-aa4d-677fd8e24fec.png)

[paper](https://arxiv.org/pdf/2208.03306.pdf)

## TL;DR
- **task :** large language modeling, domain incremental learning
- **problem :** 아이디어는 DeMix와 거의 유사! 근데 multi-node synchronize 하는 부분의 커뮤니케이션을 줄이고 싶다.
- **idea :** 도메인 별로 파라미터를 공유하지 않는 expert LM을 만들고(이전 MoE LM들은 FFN만 따로 쓰고 나머지는 공유함) Branch-Train-Merge(BTM)을 사용해서 학습함. BTM의 주요아이디어는 새로운 도메인이 유입됐을 경우 가장 가까운 LM을 찾은뒤 평균을 내서 initialize 하여 branch를 따서 학습이 되고 branch forest에 추가함. inference 시에는 어떤 도메인인지 bayes rule을 통해 posterior를 추정한뒤 weighted sum으로 최종 예측된다.
- **architecture :** vanilla Transformer..
- **objective :** cross-entropy loss 
- **baseline :** Transformer LM(GPT), DeMix 
- **data :** Wikipedia, C4, StackOverflow, JavaScript, ... 등등 
- **result :** out-of-domain에서 더 좋은 perplexity, 64개의 domain에 대해 incremental learning했을 때 2.5배의 크기를 가진 Transformer LM과 비슷한 성능.
- **contribution :** MoE without shared parameters.
- **limitation or 이해 안되는 부분 :**

## Details
### Batch-Train-Merge(BTM)
<img width="903" alt="image" src="https://user-images.githubusercontent.com/46675408/186549445-80d57367-7aaf-4b5a-9e26-90b1334b775b.png">

<img width="931" alt="image" src="https://user-images.githubusercontent.com/46675408/186549806-04ea8c1b-6d91-48ab-aeb5-d48d52e94203.png">


### Inference
<img width="884" alt="image" src="https://user-images.githubusercontent.com/46675408/186549699-f60d1461-a0cc-48a8-9447-f4b1e8d01bee.png">

모든 ELM에 forward 해야하는건 맞지만 선택되는 ELM이 sparse하게 구성됨을 확인할수 있엏음.

### Data..
<img width="888" alt="image" src="https://user-images.githubusercontent.com/46675408/186549911-a17d4fae-dd98-49a7-ab67-8624f759b644.png">

### DeMix
DeMix, 2021
- https://arxiv.org/pdf/2108.05036.pdf
![image](https://user-images.githubusercontent.com/46675408/186549102-b8c3e57a-d286-4c64-b90c-000f937d6791.png)
- problem : 여러 도메인의 corpus를 하나의 LM으로 학습할 때의 perplexity를 낮추고 싶다. 이때 우리는 각 데이터의 도메인을 알고 있다.
- solution : corpus의 도메인 별로 FFN(switch Transformer처럼)을 expert로 두어 학습시킨다. inference 시에 새로운 도메인이 추가 되었을 때,
                1) 모든 FFN을 forward를 하여 베이즈룰로 weighted sum하여 결과를 내거나 2) 해당 도메인을 위한 FFN을 추가할 수 있다. 
- result : 학습 효율을 늘리면서 LM perplexity 개선, 이전 expert들의 forgetting 없이 새로운 도메인을 추가하거나 제거할 수 있음을 보임.

