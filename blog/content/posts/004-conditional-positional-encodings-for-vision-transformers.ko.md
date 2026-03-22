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

**Problem :** 기존의 positional embedding은 학습된 길이보다 더 긴 길이가 나왔을 때 성능 저하를 일으키며, translation-invariant하지 않음. relative PE는 계산상 복잡하며 이미지 분류 문제에서는 absolute position 정보가 없어 성능이 저하됨.
**Solution :** 인풋 토큰의 인접한 토큰들을 input으로 하는 position embedding을 학습하여 input에 따라 position embedding이 바뀌도록 함. 구체적으로는 ViT 인코더를 거친 토큰을 N x W x H x C로 원복한 뒤 이를 zero padded CNN을 거쳐 position embedding으로 사용함. 
**Result :** ViT, DeiT보다 좋은 성능. 기존의 트랜스포머 구조에 seamless하게 적용 가능. `[CLS]` 토큰을 없애고 GAP를 사용하여 분류 문제에서 SOTA
**details :**[paper summary](https://long8v.notion.site/conditional-PE-52d9b49f39e944d4aaacb322a93e1252)
 