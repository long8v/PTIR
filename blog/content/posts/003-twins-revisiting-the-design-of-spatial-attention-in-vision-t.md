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

**Problem :** SwinTransformer's shifted window method is rather complicated and not optimized for deep learning frameworks (like TensorRT).
**Solution :** Cut into m by n sub-windows like Swin, perform local self-attention, pool the resulting values into one value for each sub-window (e.g. strided CNN), and repeat the LSA+GSA operation to seek attention from other sub-windows with this m by n matrix as the key value. + Apply conditional positional encoding.
**Result :** Better performance than SwinTransformer with simpler/optimized operations. Adding conditional positional encoding to PVT performs better than Swin
**What I thought :** CNN is taking a lot of ideas from me. It's good that it's simpler than Swin but performs well... I'll read CPVT as my next paper.
**details :** [paper summary](https://long8v.notion.site/Twins-c7bacd2f5cfa4491a1c1b8684834fff0)