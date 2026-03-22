---
title: "SimVLM: Simple Visual Language Model Pretraining with Weak Supervision"
date: 2022-01-24
tags: ['multimodal', 'SSL', '2021Q2', 'zero-shot']
paper: ""
issue: 8
issueUrl: "https://github.com/long8v/PTIR/issues/8"
---
![image](https://user-images.githubusercontent.com/46675408/150709165-3c944548-df62-4efa-a1d4-a190eb8b83c4.png)
[**arxiv**](https://arxiv.org/abs/2108.10904)
**Problem :** Vision-Language Pretraining (VLP) requires bounding boxes and labels for images, which makes annotation costly and not easy to switch to zero-shot.
**Solution :** The image was encoded with [CoAtNet](https://arxiv.org/abs/2106.04803) and the text-encoded value was prefixed to learn the encoder-decoder structure. The data used was ALIGN (noisy image-text pair data) and C4 (text-only). finetuning performs image captioning, visual reasoning, VQA, and multimodal translation
![image](https://user-images.githubusercontent.com/46675408/150711751-e84a36ed-e9b9-4fa9-b546-c2bd174b1c54.png)
**Result :** Good performance on SOTA, zero-shot on various finetuning tasks.
![image](https://user-images.githubusercontent.com/46675408/150710664-89c6775f-3bc5-42a4-9ca1-4e48b8ed1754.png)
Performance similar to zero-shot, no-finetuning, no-pretraining model on image caption task
![image](https://user-images.githubusercontent.com/46675408/150712771-935ca1a0-f939-486f-ab7e-7df153d76ee3.png)
Confirmed that it is useful to include a text-only corpus when training the Vison-Lanugage model (enhances the decoder's ability to generate)

**etc :**
- There is a separate loss called [CIDEr](https://www.cv-foundation.org/openaccess/content_cvpr_2015/papers/Vedantam_CIDEr_Consensus-Based_Image_2015_CVPR_paper.pdf) when doing VQA
- VQA is learned by putting the image into the encoder, the text into the decoder, and then appending the FCN to the output of the last token in the decoder
- multimodal translation is the task of changing the language of a description given an image.
- Encoder-decoder structure was better than decoder-only structure
- PrefixLM is a property that sees prefixes as bi-directional and LM afterwards (is this the first time prefixLM has been mentioned in this paper?)
