---
title: "[114] MaMMUT: A Simple Architecture for Joint Learning for MultiModal Tasks"
date: 2023-05-09
tags: ['multimodal', 'google', '2023Q1']
paper: "https://arxiv.org/pdf/2303.16839.pdf"
issue: 123
issueUrl: "https://github.com/long8v/PTIR/issues/123"
summary: "Multi-modal series. - Fully e2e training without separate image vision encoder pretraining. It is similar to CoCa, but the architecture is relatively simple. video is also said to have the strength of not having to forward the vision encoder several times, but this is... TubeViT's contribution?..."
---
<img width="1102" alt="image" src="https://user-images.githubusercontent.com/46675408/236988463-5eebdcef-80eb-4f9c-80bd-c4829a9ef724.png">

[paper](https://arxiv.org/pdf/2303.16839.pdf)

## TL;DR
- **I read this because.. :** multi-modal series.
- **task :** VLM -> captioning, image2text retreival, text2image retreival, VQAv2, Video QA, Video Captioning, Open-Vocab Detection 
- Problem :** Contrastive learning has the ability to retrieve and captioning learning has the ability to generate text. However, the two learning approaches are conflicting and difficult to combine.
- **idea :** decoder only for language model! do forward twice with different masking because contrastive and captioning need different things
- **input/output :** (pretraining) image / text -> similiarity score / caption text 
- **architecture :** Image Encoder(ViT Huge, 650M) + Lanauge Decoder(1B Transformer)
- **objective :** Image Captioning Loss + Focal Contrastive Loss 
- **baseline :** CoCa, Florence, CLIP, ALIGN, ...
- **data :** (pretaining) only ALIGN -> (finetune) MSCOCO, Flickr30K, VQAv2, ...  
- **result :** In zero-shot image-text retreival, sota. VQAv2 also performs better in terms of parameter size.
- **contribution :** fully e2e training without separate image vision encoder pretraining. CoCa와 비슷한데 architecture가 비교적 간단한데. video도 vision encoder 여러번 forward 안 않아도 되는게 강점이라고 하는데 이건 .. TubeViT의 contribution인 듯?...
- **etc. :** CoCa also used JFT, so why did it beat the retrieval performance? Is it because CoCa has more tasks, so the retrieval performance is somewhat lower? Or the learning method? It would be better to compare the learning with CoCa feeling.

## Details
### Related works
- Video Processing -> TubeViT
  - https://arxiv.org/pdf/2212.03229.pdf
- As if it's a thesis that we can treat images/videos the same way because we've sampled them well.
<img width="582" alt="image" src="https://user-images.githubusercontent.com/46675408/236992950-8dde90db-28c2-4197-bb5d-79157204423d.png">

- To fill in the gap between PE from object detection and PE from pretraining -> Cropped PE / Focal Loss for Constrative loss
- I saw it in Region-Aware Pretraining for Open-Vocabulary Object Detection with Vision Transformers, but I can't find the paper.
 
### Architecture

<img width="1080" alt="image" src="https://user-images.githubusercontent.com/46675408/236991324-73ea28e2-f68e-4ffd-9f6f-4b0000af353e.png">

<img width="1093" alt="image" src="https://user-images.githubusercontent.com/46675408/236991369-931be06a-227b-4939-8ff3-cfa1bf5edc26.png">

<img width="1093" alt="image" src="https://user-images.githubusercontent.com/46675408/236991394-13029f52-7db8-49c8-90ba-521077e2d9c9.png">

The main contribution, two-pass learning
Captioning requires causal masking (requiring a conditioned representation), while contrastive requires a full-text representation.
Just use a different masking with decoder and forward twice! (masking / CA or just this is not an encoder lol)
~CoCa also expressed decoder with text encoder like text encoder, but here it is almost similar to CoCa, so it seems like Unimodal Text Decoder + MultiModal Text Decoder have the same weight!
CoCa added self-attention with causal masking to the text decoder! He only needs to do one forward.
<img width="417" alt="image" src="https://user-images.githubusercontent.com/46675408/236992384-168658ca-3acc-406b-a09b-5a9daaa5d9ae.png">


### Loss
- Captioning loss
<img width="561" alt="image" src="https://user-images.githubusercontent.com/46675408/236991421-9fd9d2a8-290a-4f2e-9c6f-a144475f3cc6.png">

- Focal Constrative Loss
Contrastive learning usually requires large BS. Learn from more challenging data than CE -> use focal loss

<img width="476" alt="image" src="https://user-images.githubusercontent.com/46675408/236991448-102c411d-1316-4744-bb4d-c6e757b6464a.png">
<img width="341" alt="image" src="https://user-images.githubusercontent.com/46675408/236991489-88454d15-ee74-460f-b5f8-9ffb5cdcaa19.png">

### Video Processing
<img width="1128" alt="image" src="https://user-images.githubusercontent.com/46675408/236991611-dd09ca33-b214-4c3d-8280-7c644d204f6f.png">

## Result
<img width="1073" alt="image" src="https://user-images.githubusercontent.com/46675408/236991641-af95e6e8-d0f5-4539-a882-4372b0a43e48.png">
<img width="1061" alt="image" src="https://user-images.githubusercontent.com/46675408/236991666-c00dbbbc-f6bd-4621-bdc2-5bde1d8f8e9c.png">

### Ablations
<img width="1119" alt="image" src="https://user-images.githubusercontent.com/46675408/236991703-9c040188-122d-48fd-83d1-bac7167ced03.png">

- With captioning loss, text2image performs better and image2text performs worse. Generation seems to create a better text representation -> not sure about this... Isn't it a two-way street?!
- CA was good for frequent VQA and not so much for revalidation.

<img width="1157" alt="image" src="https://user-images.githubusercontent.com/46675408/236992873-a4ec70a7-39c6-4282-802d-c31b622d6c11.png">

Small is good.
