---
title: "Segment Anything "
date: 2023-09-04
tags: ['segmentation', '2023Q2', 'meta']
paper: "https://arxiv.org/pdf/2304.02643.pdf"
issue: 142
issueUrl: "https://github.com/long8v/PTIR/issues/142"
summary: "I tried not to read it, but... SAM is so powerful that it seems to be used a lot to create VLM datasets - Benchmarks for semantic segmentation seem to be very subjective, but this is solved with dataset + model arch! I created a general semantic segmentation model."
---

<img width="1047" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/61e77ac6-c071-4804-9185-5b5e09bd8610">

[paper](https://arxiv.org/pdf/2304.02643.pdf), [demo](https://segment-anything.com/demo?ref=blog.annotation-ai.com)

## TL;DR
- **I read this because.. :** I wasn't going to read it, but... SAM is so powerful that it seems to be used a lot to create VLM datasets.
- **task :** prompt segmentation 
- **problem :** Given the prompt I want to segment / point, there is disambiguity as to which segment I want.
- **idea :** use a simple prompt encoder and use this as a query in MaskFormer / learn by losing only the most confident ones
- **input/output :** image + prompt(points, box, mask, text) -> mask (no cls) 
- **architecture :** A variation of MaskFormer. First, a strong backbone (ViT-H) + prompt encoder is passed through a pe or text encoder and then added to SA. image -> prompt cross attention (original) prompt -> image cross attention (added). Generating masks internally by pixel upsample and mask embedding. Changed to return IoU score to pick only confident masks.
- **objective :** focal loss + dice loss
- **baseline :** Interactive segmentation model called RITM
- **data:** SA-1B proposal
- **evaluation :** mIoU
- **result :** Almost beats RITM. Doesn't beat semantic segmentation SOTA on the benchmark. Performance on text prompt is not very good.
- **contribution :** Benchmarks for semantic segmentation seem to be very subjective, but I solved this with dataset + model arch! I created a general semantic segmentation model.
- **etc. :** How did you learn about bbox / mask / text, or did you not learn...

## Details
### Preliminaries 
<img width="800" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/164ba76e-ee0d-4bbf-92af-261704bc28d4">

### Disambiguity in interactive segmentation
<img width="507" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4deaddfa-89d0-45c8-a842-c042c033a31a">

### Model
<img width="1026" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d996c7bf-b01d-4059-b429-111357fb2221">

### Result 
<img width="931" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/08e3d352-cd4e-4b30-99cb-ccc6680130a9">
