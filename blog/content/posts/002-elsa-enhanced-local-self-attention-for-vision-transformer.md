---
title: "ELSA: Enhanced Local Self-Attention for Vision Transformer"
date: 2022-01-07
tags: ['2021Q4', 'ViT', 'attention']
paper: "https://arxiv.org/pdf/2112.12786v1.pdf"
issue: 2
issueUrl: "https://github.com/long8v/PTIR/issues/2"
---
![image](https://user-images.githubusercontent.com/46675408/148480371-ebd2dd98-e684-4bd6-b527-d03c457da3ea.png)
[paper](https://arxiv.org/pdf/2112.12786v1.pdf)

**Problem :** Swin Transformer's Local Self-Attention (LSA) was better when replaced with Depthwise-Conv (DeConv) or Decoupled Dynamic Filter (DDF).
**Solution :** Expressed DeConv, DDF, and LSA as attention expressions and conducted an ablation study. We found that increasing head and sliding methods are important for performance and proposed hadamard attention, which is more efficient than ghost-head and dot-product.
**Result :** Higher FLOPS with LSA-like parameters, improved performance of SwinTransformer on classification tasks
**I noticed :** neighboring window (=sliding window) performs better than local window... Like the last paper, the more I apply CNN's methodology, the better it gets...
**details :** [paper summary](https://long8v.notion.site/ELSA-ca774c9f790a41cd98b1395576acd85f)
