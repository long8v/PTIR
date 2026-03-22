---
title: "[68] Iterative Scene Graph Generation"
date: 2022-10-05
tags: ['SGG', '2022Q3', 'one-stage']
paper: "https://arxiv.org/pdf/2207.13440.pdf"
issue: 75
issueUrl: "https://github.com/long8v/PTIR/issues/75"
---
<img width="878" alt="image" src="https://user-images.githubusercontent.com/46675408/193985405-1200b030-1a90-4857-8e12-3c9831d6ec64.png">

[paper](https://arxiv.org/pdf/2207.13440.pdf)

## TL;DR
- **task :** one-stage scene graph generation
- **problem :** object 뽑고 그걸 기반으로 relation을 뽑는 factorization이 한계가 있다. relation이 주어졌을 때 subject, object를 더 잘 뽑을 수 있다. 
- **idea :** 1) subject가 주어졌을 때 object를 조건부로, subject, object가 주어졌을 때 predicate를 조건부로 모델링 2) t개의 레이어가 각각 sub, obj, predicate를 output하고 이게 다음 레이어에도 전파됨. 
- **architecture :** CNN backbone + 3개({s, p, o})의 transformer decoder. positional encoding이 subject는 learned PE, object는 subject의 PE와 object PE MHSA한 거, predicate는 subject와 object를 합한것과 MHSA 하는 식으로 conditional PE를 만듦. {s, p, o} 각각의 query도 이전 레이어의 {s, p, o}에 대한 query들을 가져와서 MHSA 해줌. 
- **objective :** ce loss + bbox loss for subject / object / predicate + loss re-weighting for tail  
- **baseline :** MOTIF, HOTR, SGTR
- **data :** Visual Genome, Action Genome 
- **result :** SOTA. mR 성능이 매우 좋넹 
- **contribution :** transformer 구조만으로 좋은 성능! 
- **limitation or 이해 안되는 부분 :** object detection은 그냥 쌩깠음. 그래서 Detr Decoder 없음.

## Details
<img width="364" alt="image" src="https://user-images.githubusercontent.com/46675408/193985710-e268c0a9-bedc-4947-a4f2-2ab336a2700f.png">

### Architecture
<img width="831" alt="image" src="https://user-images.githubusercontent.com/46675408/193986462-84008f02-a96a-4a87-b57d-64272d2bed97.png">

#### Conditional Positional Encodings
<img width="448" alt="image" src="https://user-images.githubusercontent.com/46675408/193987286-72c20333-8514-40ed-b0fb-64b0c34afe90.png">

- $\tilde q^t_{x,i} =q^t_{x,i} +p^t_{x,i}$ ; x는 {s, o, p} 중 하나.

#### Conditional Queries
<img width="538" alt="image" src="https://user-images.githubusercontent.com/46675408/193987506-8ebaa180-6296-4f0c-ae94-58d2b9fde47a.png">

- $q^t_{x,i}$는 t번째 레이어의 i번째 인덱스의 feature representation

### Result
<img width="563" alt="image" src="https://user-images.githubusercontent.com/46675408/193986669-ee0effab-dbcc-4723-98b9-86bc84e23f39.png">

harmonic Recall은 얘네가 제시한 evaluation metric인데 recall, mR 섞은거
AP는 평가를 안했네! 사나이다!

### bipartite matching
ground truth relation을 no relation으로 padding하고 전체 joint matching cost를 최소화하는 그래프를 찾는 것으로 함. (굳이? 흠..)
<img width="357" alt="image" src="https://user-images.githubusercontent.com/46675408/193988653-2de765c9-bcf4-4cdd-a9f4-3e5547c67a48.png">

<img width="687" alt="image" src="https://user-images.githubusercontent.com/46675408/193988669-e68e2af6-ab48-45f6-8912-2ca4abe11c77.png">

우리의 loss! 
<img width="618" alt="image" src="https://user-images.githubusercontent.com/46675408/193988723-e3bd1cf1-a834-42d1-a28c-ffdc7502bc95.png">


### Implementation Details
- ResNet-101
- 6 layers, feature size 256
- 300 queries
- bs = 12, lr=10e-4 gradually decaying
- NMS 사용
  - class 마다 각각 NMS가 붙었고, IoU overlap을 체크하면서 post-NMS bbox랑 붙었다.
- 50 epochs. T4 4장.

### Ablation
#### number of queries
<img width="709" alt="image" src="https://user-images.githubusercontent.com/46675408/193988301-c58e58d2-e688-4669-9d0d-94bd5514b944.png">

생각보다 num_queries 크다고 달라지는게 없네

#### refinement의 효과
<img width="399" alt="image" src="https://user-images.githubusercontent.com/46675408/193988424-d4e0a476-a7fa-4b3f-9ac1-98cd0a5347d9.png">
