---
title: "[26] Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts"
date: 2022-05-13
tags: ['2018', 'MoE', 'KDD']
paper: "https://dl.acm.org/doi/pdf/10.1145/3219819.3220007"
issue: 29
issueUrl: "https://github.com/long8v/PTIR/issues/29"
---
<img width="746" alt="image" src="https://user-images.githubusercontent.com/46675408/168198355-74e7785b-ff9b-46de-8fb1-a78f4c543b4f.png">

[paper](https://dl.acm.org/doi/pdf/10.1145/3219819.3220007)

**idea :** multi-task를 할 때, 각 task들의 relation명시적으로 주지 않아도 알아서 modeling 할 수 있는 multi-gate MoE(MMOE)를 만들자

<img width="918" alt="image" src="https://user-images.githubusercontent.com/46675408/168199403-bf8094b0-d3ab-4f40-8847-74053714b0b4.png">

일반적인 multi-task learning을 할 때, 공유되는 네트워크(shared bottom)가 있고 위에 각 task 별로 FCN을 쌓는 식으로 되어있다. 이 논문에서는 여기에 MoE 아이디어를 결합하여 각 expert들을 shared bottom으로 사용하도록 한다. 여기에 원래 MoE는 하나의 gating network가 있는데 MMoE에서는 각 task k별로 gating network를 만들도록 한다. 

<img width="374" alt="image" src="https://user-images.githubusercontent.com/46675408/168199929-315f47c9-bc6a-492e-8cd6-0527d3b5aea2.png">

이때 각 gating network는 간단한 input_dim은 feature이고 output_dim은 num_experts인 classifier이다.

<img width="344" alt="image" src="https://user-images.githubusercontent.com/46675408/168200053-718f7429-9a97-4686-b51d-3c8b3b38c8d8.png">
 
synthetic 데이터에 대한 평가는 아래와 같다. 태스크별 correlation이 높을 수록 

<img width="1294" alt="image" src="https://user-images.githubusercontent.com/46675408/168200419-bb392094-0c76-40c9-b6db-6cc5e154b142.png">

real data에 대한 평가는 아래와 같다. 

<img width="350" alt="image" src="https://user-images.githubusercontent.com/46675408/168200663-d1df9130-d475-47f9-9c4a-96f7446341bf.png">

<img width="350" alt="image" src="https://user-images.githubusercontent.com/46675408/168200715-eadbe3ea-f237-4592-a397-e5223c98d82a.png">


한줄 평 : 흠..classifier 별로 correlation 초기값을 좀 줄 수 있는 방법이 있을까?

