---
title: "[8] SimVLM: Simple Visual Language Model Pretraining with Weak Supervision"
date: 2022-01-24
tags: ['multimodal', 'SSL', '2021Q2', 'zero-shot']
paper: ""
issue: 8
issueUrl: "https://github.com/long8v/PTIR/issues/8"
---
![image](https://user-images.githubusercontent.com/46675408/150709165-3c944548-df62-4efa-a1d4-a190eb8b83c4.png)
[**arxiv**](https://arxiv.org/abs/2108.10904)
**Problem :** Vision-Language Pretraining(VLP)를 하기 위해서는 이미지의 bounding box, label을 달아야 하여 annotation의 비용이 많이 들며 zero-shot으로 전환이 쉽지 않음
**Solution :** 이미지는 [CoAtNet](https://arxiv.org/abs/2106.04803)으로 인코딩한걸 텍스트 인코딩된 값을 prefix로 두어서 encoder-decoder 구조로 학습. 이 때의 데이터는 ALIGN(noisy한 이미지-텍스트 페어 데이터)와 C4(text-only)를 사용하였다. finetuning은 image captioning, visual reasoning, VQA, multimodal translation을 진행함
![image](https://user-images.githubusercontent.com/46675408/150711751-e84a36ed-e9b9-4fa9-b546-c2bd174b1c54.png)
**Result :** 다양한 finetuning task에서 SOTA, zero-shot에서도 괜찮은 성능
![image](https://user-images.githubusercontent.com/46675408/150710664-89c6775f-3bc5-42a4-9ca1-4e48b8ed1754.png)
이미지 캡션 태스크에서 finetuning을 안해도(zero-shot), 프리트레이닝 없는 모델과 유사한 성적 
![image](https://user-images.githubusercontent.com/46675408/150712771-935ca1a0-f939-486f-ab7e-7df153d76ee3.png)
Vison-Lanugage 모델을 학습할 때에 텍스트만 있는 corpus를 넣는것이 유용하다는 것을 확인함(decoder의 generation 능력을 강화) 

**etc :**
- VQA를 할 때에 [CIDEr](https://www.cv-foundation.org/openaccess/content_cvpr_2015/papers/Vedantam_CIDEr_Consensus-Based_Image_2015_CVPR_paper.pdf)라는 loss가 따로 있음
- VQA는 이미지를 인코더에 텍스트를 디코더에 넣은 뒤 디코더의 마지막 토큰의 output에 FCN을 붙여 학습됨
- multimodal translation은 이미지가 주어졌을 때의 설명에 대해 언어를 바꾸는 태스크
- 인코더-디코더 구조가 decoder-only 구조보다 좋았다
- PrefixLM은 prefix에 대해서는 bi-direction으로 보고 이후로는 LM으로 보는 특성(prefixLM이란 게 이 논문에서 처음 나온건가?)
