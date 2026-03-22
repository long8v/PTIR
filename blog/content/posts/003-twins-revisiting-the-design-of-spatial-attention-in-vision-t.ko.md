---
title: "[3] Twins: Revisiting the Design of Spatial Attention in Vision Transformers"
date: 2022-01-10
tags: ['ViT', 'backbone', '2021Q1']
paper: "https://arxiv.org/pdf/2104.12753.pdf"
issue: 3
issueUrl: "https://github.com/long8v/PTIR/issues/3"
---
![image](https://user-images.githubusercontent.com/46675408/148724469-e3f3ac90-0fe8-4765-bde0-f7a788875616.png)
[paper](https://arxiv.org/pdf/2104.12753.pdf)

**Problem :** SwinTransformer의 shifted window 방법은 다소 복잡하고 딥러닝 프레임워크(TensorRT 등)에 최적화되어 있지 않음
**Solution :** Swin처럼 m by n개의 sub-window로 자르고 local self-attention을 한 뒤에, 그 결과값들에 대해 각 sub-window에 대해 하나의 value로 pooling(e.g. strided CNN)을 한 뒤, 이 m by n matrix를 key값으로 하여 다른 sub-window들과 attention을 구하는 LSA+GSA연산을 반복 진행한다. + conditional positional encoding 적용. 
**Result :** SwinTransformer보다 더 간단/최적화된 연산으로 더 좋은 성능. PVT에 conditional positional encoding 추가하면 Swin보다 성능이 좋음
**느낀 점 :** CNN에서 아이디어를 참 많이 가져오네. Swin보다 간단한데 성능이 좋다니 좋다.. CPVT를 다음 논문으로 읽어봐야겠다. 
**details :** [paper summary](https://long8v.notion.site/Twins-c7bacd2f5cfa4491a1c1b8684834fff0)