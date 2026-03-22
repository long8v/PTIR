---
title: "Linearly Mapping from Image to Text Space"
date: 2023-08-17
tags: ['multimodal', 'ICLR', '2023Q1']
paper: "https://arxiv.org/abs/2209.15162"
issue: 139
issueUrl: "https://github.com/long8v/PTIR/issues/139"
summary: "Is CLIP pretrained better when glued to LM? Is a vision backbone trained with image only better in VLM? - Ablation for multiple vision backbones."
---
<img width="548" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/de8b07ca-5693-44c6-baa0-e692fbb7fa10">

[paper](https://arxiv.org/abs/2209.15162)

## TL;DR
- **I read this because.. :** Is CLIP pretrained better when attached to LM? Is a vision backbone trained with image only better in VLM?
- **task :** image captioning, VQA
- **problem :** Which pretrained vision backbone is good in VLM?
- **idea :** Let's learn only linear maps, which is a harsher setting than Frozen and MAGMA, and extract the performance -> LIMBeR
- **input/output :** image, task query, (optional) question 
- **architecture :** (vision) CLIP RN50x16, NFRN50, BEiT-Large (language) GPT-J(6billion) (linear map) 4096 dim projection
- **objective :** language model loss 
- **baseline :** tuning MAGMA, Blind (image security), NFRN50
- **data :** (train) CC3M -> (eval) NoCaps, COCO, VQAv2
- **evaluation :** CIDEr-D, CLIP-S, Ref-S, {0,1,2,4}-shot accuracy
- **result :** Often performs better than more trained MAGMA. freeze is sufficient.
- **contribution :** ablation for multiple vision backbones.
- **etc. :**

## Details

- The architecture itself is simple! vision backbone coarse feature map with linear projection and prefix it like a soft prompt in lm to learn vlm. The point is to learn only linear projection.
<img width="553" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4c4dd5d4-e13d-4603-be8d-052d19cbebba">

- This is where performance analysis is fun
<img width="600" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/75d11a61-d1d1-41ac-8b5e-d869effe22c7">

1) MAGMA trains adapters on vision backbone + LM with similar architecture, but the proposed LiMBER often performs better than this.
2) Among the vision backbone, CLIP has language supervision, BEiT has no language supervision at all (self-supervision), and NFRNet50 is ImageNet22K, so it can be said that it is in the middle (classification, but after all, the classification is based on WordNet (?), so it can be said that it has language supervision indirectly), and CLIP is the best.
3) BEiT is the most interesting, especially for VQA {1,2,4}-shot, which performs worse than blind (VQA without seeing any images). It's better than random NFRNet, but hardly helpful.
4) However, if you attach BEiT to the decoder and attach BEiT-FT with additional training to image classification (what data did you use?), it may outperform CLIP -> After all, self-supervision systems such as MAE or BEiT need to be finetuned to the downstream task.

c.f. 
<img width="627" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7fe10ace-98f7-4746-86ba-ba6006e3c6c5">

In the MAE paper, linear probing performed worse than MoCo trained with InfoNCE loss, which is slightly closer to classification.
-> but it gets even better when finetuning layers
but... [Masked Autoencoding Does Not Help Natural Language Supervision at Scale](https://openaccess.thecvf.com/content/CVPR2023/papers/Weers_Masked_Autoencoding_Does_Not_Help_Natural_Language_Supervision_at_Scale_CVPR_2023_paper.pdf) This paper also. In CLIP, doing MAE helps at million scale, but makes it worse at billion
-> In the end, self-supervision shines for small amounts of data, but when you have a large corpus like clips, why not?

BEiT failure cases
<img width="815" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/04d74bd3-1409-437d-8daa-c238a64c12e8">


<img width="678" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ed91e167-b849-4b55-b298-01ded0779b51">

There are multiple caption metrics, but the dominance of vision backbone is consistent

