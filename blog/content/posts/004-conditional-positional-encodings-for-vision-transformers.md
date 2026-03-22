---
title: "[4] Conditional Positional Encodings for Vision Transformers"
date: 2022-01-12
tags: ['ViT', '2021Q1', 'PE']
paper: "https://arxiv.org/pdf/2102.10882.pdf"
issue: 4
issueUrl: "https://github.com/long8v/PTIR/issues/4"
---
![image](https://user-images.githubusercontent.com/46675408/149097792-8264c306-148e-44b5-8c5f-257ec78078b7.png)
[paper](https://arxiv.org/pdf/2102.10882.pdf), [code](https://github.com/Meituan-AutoML/Twins/blob/main/gvt.py#L305-L325)

**Problem :** Traditional positional embedding degrades performance when the length is longer than the trained length, and is not translation-invariant. Relative PE is computationally complex and performs poorly in image classification problems due to lack of absolute position information.
**Solution :** Learn the position embedding of the neighboring tokens of the input token as input so that the position embedding changes depending on the input. Specifically, the tokens passed through the ViT encoder are reconstructed as N x W x H x C, which is then passed through a zero-padded CNN and used as the position embedding.
**Result :** Better performance than ViT, DeiT. Can be seamlessly adapted to existing transformer structures. Eliminates `[CLS]` tokens and uses GAPs to solve the SOTA
**details :**[paper summary](https://long8v.notion.site/conditional-PE-52d9b49f39e944d4aaacb322a93e1252)
 