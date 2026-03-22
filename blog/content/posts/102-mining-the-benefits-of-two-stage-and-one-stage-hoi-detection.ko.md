---
title: "[93] Mining the Benefits of Two-stage and One-stage HOI Detection"
date: 2022-12-29
tags: ['2021Q2', 'NeurIPS', '25min', 'HOI']
paper: "https://arxiv.org/pdf/2108.05077.pdf"
issue: 102
issueUrl: "https://github.com/long8v/PTIR/issues/102"
---
<img width="740" alt="image" src="https://user-images.githubusercontent.com/46675408/209899558-d0dea062-46f7-4b65-ac63-deae8201fb23.png">

[paper](https://arxiv.org/pdf/2108.05077.pdf)

## TL;DR
- **I read this because.. :** NeurIPS 2022의 RLIP을 읽으려다가 이게 선행연구여서 읽음. 
- **task :** Human Object Interaction(HOI)
- **problem :** two-stage HOI의 단점 1) M개의 사람과 N개의 object의 M x N pair를 넣고 action 분류를 하니 시간 복잡도가 높음  2) M x N개 중에 실제 relation이 있는게 적어서 imbalance 3) bounding box를 뽑는 feature는 object의 내용보다는 edge에 집중해서 relation이 예측하는데 쓰면 성능이 별로 <-> one-stage HOI의 단점 : 두개의 상이한 task를 하나의 feature 표현으로 해결하려니 generalize가 힘듦
- **idea :** one-stage로 가되 decoder를 분리. object query 던지고 `human-object-interaction score`를 뽑게 하는 Human-Object Pair Decoder가 하나. 그리고 그 decoder에서 나온 output 표현을 갖고 action class를 분류하는 Interaction Decoder 하나.
- **architecture :** DETR
- **objective :** detr loss + bce for interaction score(관계가 있으면 1, 없으면 0) 
- **baseline :** QPIC, AS-Net, HOTR, ATL, ...
- **data :** HICO-Det, V-COCO
- **evaluation :** mAP for triplet(IoU 0.5 이상이어야 맞는 box로)
- **result :** SOTA. HICO-Det에서 9.32% 개선
 
## Details

<img width="1442" alt="image" src="https://user-images.githubusercontent.com/46675408/209900098-1236e8c4-41c6-45f2-9b68-bb159c1917d6.png">

<img width="756" alt="image" src="https://user-images.githubusercontent.com/46675408/209900121-f3603fa4-6de4-491c-9395-0bef4a99d71f.png">

### Result
<img width="753" alt="image" src="https://user-images.githubusercontent.com/46675408/209900145-b72f6c26-3f62-47a8-b59e-ca3828f620d5.png">
