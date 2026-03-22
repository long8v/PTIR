---
title: "Noise-aware Learning from Web-crawled Image-Text Data for Image Captioning"
date: 2024-02-12
tags: ['ICCV', '25min', '2022Q4', 'kakao']
paper: "https://arxiv.org/pdf/2212.13563.pdf"
issue: 161
issueUrl: "https://github.com/long8v/PTIR/issues/161"
summary: "AKA NOC. read it because it seemed to have done some good analysis on CLIP score. - Simple and intuitive~."
---

<img width="708" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ba1962ff-1e13-49b0-b298-cca7b8085223">

[paper](https://arxiv.org/pdf/2212.13563.pdf), [code](https://github.com/kakaobrain/noc)

## TL;DR
- **I read this because.. :** aka noc. something seemed to have done a good job analyzing the CLIP score.
- **task :** captioning with noisy image-text label
- Problem :** Data like COCO and Visual Genome are not scalable. But using web-crawled pairs can be noisy, and filtering them by CLIP score makes a lot of data disappear.
- **idea :** Binning and embedding CLIP scores to provide when captioning, and giving the best aligned score in the inference step.
- **input/output :** image, clip score of {image, text} pair -> text 
- **architecture :** CLIP ViT-L/14 + 6-layer transformer(94.5M)
- **objective :** cross-entropy loss 
- **baseline :** no filtering, filtering(clip score 0.3), loss reweighting(loss multiplied by clip score), ZeroCap, Socratic Model, DeCAP
- **data:** CC3M (on the noisy axis.!), also tried COYO with ablation
- **evaluation :** BLEU, METEOR, CIDEr, SPICE, CLIPScore for COCO, nocaps // self-retrieval R@1 (does the image come up when retrieved with a caption created for a specific image)
- **result :** BLEU minus sota
- **contribution :** Simple and intuitive~.
- **etc. :** I didn't get what I wanted, but I enjoyed reading it~ The most similar thing is BLIP, but I thought about it, so.... BLIP seems to be a pioneering study

## Details
- motivation 
<img width="349" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/53490c39-a188-4b73-8b80-6000d4c0aa81">
<img width="706" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/308dc477-a934-4572-a6c7-16aabb4caec2">

<img width="349" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9333897c-ae45-45ac-bae4-9a6767981115">


- architecture 
<img width="698" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6fd72080-5343-4319-a711-7e69aaba204f">

- results
<img width="670" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5279a976-ded6-4659-92ae-dc084ba490c2">

- ablations 
<img width="685" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ce21f97b-739d-4602-be49-253681bf2a32">

- qualitative 
<img width="702" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6b8e46db-b9b6-415a-93e1-7b19fa4f297f">
