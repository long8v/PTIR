---
title: "[141] Alpha-CLIP: A CLIP Model Focusing on Wherever You Want"
date: 2023-12-15
tags: ['multimodal', 'CLIP', '2023Q4']
paper: "https://arxiv.org/pdf/2312.03818.pdf"
issue: 153
issueUrl: "https://github.com/long8v/PTIR/issues/153"
summary: "Sunghyun's recommendation. It seems to be used for region caption / detailed caption generation as well and I was curious about fine-grained clips, so I spring for it. - Simple architecture + I didn't learn much, but it seems to have tackled many problems."
---
<img width="1148" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6c001bf6-f46d-40bf-bc28-cd0d7da48693">

[paper](https://arxiv.org/pdf/2312.03818.pdf), [page](https://aleafy.github.io/alpha-clip/), demo 

## TL;DR
- **I read this because.. :** Sunghyun recommended. region caption / detailed caption 생성에도 쓰인 것 같고 fine-grained clip에 대한 궁금증이 있어서 봄.
- **task :** CLIP with mask
- Problem :** CLIP pulls information globally, but I want a finer understanding. How can I understand the full context of the image and not distort the image itself?
- **idea :** attach conv operation before ViT in CLIP, RGB conv and alpha conv separately, maybe feature summarize and pass to ViT
- **input/output :** (clip) image + mask, text -> similarity 
- **architecture :** CLIP
- **objective :** contrastive loss
- **baseline :** (image classification) CLIP, Red Circle, MaskCLIP (REC) CPT, ReCLIP, Red Circle (OVD) MaskImageNet, Detic-ImageNet. (MMLM) LLaVA-1.5, BLIP-2 , ...
- **data :** generate rgba - region text with additional pipeline for GRIT-20m + ImageNet 460K
- **evaluation :** For each benchmark... Sometimes MMLM just swaps the backbone (which is possible by freezing the text encoder), sometimes it's finetuned
- **Result :** Improved imagenet performance, reduced MLLM hallucinations, etc.
- **contribution :** Simple architecture + seems to have tackled a lot of problems without much learning.
- **etc. :** What do we do with SAM? Region level clips do reduce hallucinations.

## Details
### motivation
<img width="700" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2c8a3c51-6ac0-4afa-b2c2-57346ffcef3b">

- image recognition: better classification (imagenet is single-label but actually multi-label) / can be used as referring expression comprehension (REC) / can be used for data generation for OVDs
- The backbone of MLLM: reducing hallucination and model bias
- generation: allows you to cherry-pick the parts you want and fixes problems with multi objects

### Region-focusing strategy 
<img width="700" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/72463f30-5412-4f8d-baff-f1dc57cb4b25">

The image itself is distorted or full contextual information is omitted/deleted

### RGBA Region-Text Pair Generation
<img width="700" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2ca9f3ea-bb2c-4bf9-b92f-22f175d4dfed">
- Grounding data pipeline: GRiT data already has bounding boxes and region text. Run SAM on it to get masks
- Classification data pipeline: SAM -> crop -> assign as clip score -> caption as BLIP and attach class as well

### Alpha-CLIP
<img width="700" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a10b888b-13b3-454a-a19b-ae12006bf110">

- text encoder freeze
- Add RGB conv + alpha conv
- alpha is between 0 and 1, but we want it to initially start at 0, so we use the
- And alpha + rgb conv is elementwise summation (not shown)
- 10% sample of epoxies trained with image - text pairs

### Result
- ImageNet classification
<img width="600" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/051d3e7f-5f4c-45e4-9d3a-790401af636b">

imagenet-s has semantic segmentation hanging on imagenet, but performance improved when I gave that gt to alpha
Or improved when given as a bbox, or just looking at the whole image as a mask, no performance drop (as if it's learning with new data)

- REC
<img width="600" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f756e0b3-4bf3-4d73-97a7-b482df53eaf4">

<img width="600" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/73393866-2dc5-4e35-ac30-304973848199">

The pipeline is kinda weird, lol... SAM picks a bunch of masks and finds the one that's closest to the text, and that's the answer.

- OVD
<img width="600" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b4ccca24-e416-42b1-a1f3-a95b4217f118">

Using a pseudo-labeling approach + AlphaCLIP as a backbone yields better performance

- Region-level captioning 
Just swapping out the backbone is working.
<img width="600" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4a3e013b-519c-4eca-aff9-c7e50c5a4780">

The results of our finetuned quantitative evaluation are as follows
<img width="600" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4c59f2df-eea7-4cfa-b4a4-89fda6ed5462">