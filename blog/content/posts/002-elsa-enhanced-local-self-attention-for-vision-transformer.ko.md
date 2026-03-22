---
title: "[2] ELSA: Enhanced Local Self-Attention for Vision Transformer"
date: 2022-01-07
tags: ['2021Q4', 'ViT', 'attention']
paper: "https://arxiv.org/pdf/2112.12786v1.pdf"
issue: 2
issueUrl: "https://github.com/long8v/PTIR/issues/2"
---
![image](https://user-images.githubusercontent.com/46675408/148480371-ebd2dd98-e684-4bd6-b527-d03c457da3ea.png)
[paper](https://arxiv.org/pdf/2112.12786v1.pdf)

**Problem :** Swin Transformer의 Local Self-Attention(LSA)를 Depthwise-Conv(DeConv) 혹은 Decoupled Dynamic Filter(DDF)로 바꾸었을 때 성능이 더 좋았다 
**Solution :**  DeConv와 DDF와 LSA를 attention 식으로 표현하고 ablation study를 함. head를 늘리는 것과 sliding 방법이 성능에 중요하다는 것을 밝혀냈고 이를 위해 ghost-head, dot-product보다 효율적인 hadamard attention을 제안함. 
**Result :** LSA와 유사한 파라미터로 더 높은 FLOPS, 분류태스크에서 SwinTransformer의 성능 개선 
**느낀 점 :** local window보다는 neighboring window(=sliding window)가 성능이 더 좋다.. 지난 논문때 들었던 느낌처럼 점점 CNN의 방법론을 더 적용하면 적용할 수록 좋아짐... 
**details :** [paper summary](https://long8v.notion.site/ELSA-ca774c9f790a41cd98b1395576acd85f)
