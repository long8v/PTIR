---
title: "[136] Visually-Situated Natural Language Understanding with Contrastive Reading Model and Frozen Large Language Models"
date: 2023-11-28
tags: ['multimodal', 'naver', '2021Q3', 'document', 'emnlp']
paper: "https://arxiv.org/pdf/2305.15080.pdf"
issue: 148
issueUrl: "https://github.com/long8v/PTIR/issues/148"
summary: "aka cream. A colleague's paper - suggesting how to better utilize ocr tokens in the document domain. Proposal for a CL method to ensure that performance doesn't falter when ocr is unstable."
---
<img width="713" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/78ac8841-6bdb-4454-ad1e-f942a5984ad3">

[paper](https://arxiv.org/pdf/2305.15080.pdf)

## TL;DR
- **I read this because.. :** aka cream. A colleague's paper
- **task :** DocVQA
- **problem :** VQA without OCR has performance limitations, and using OCR as input eats up too many tokens.
- Idea :** Use OVD and OCR, feature extraction with an auxiliary encoder, and then use it as a CA.
- **input/output :** image, ocr result (box and text), ovd result (box and class text), question -> answer
- **architecture :** Vision Encoder(CLIP ViT-L /LAION-2B), Auxiliary encoder(mBART), decoder(mBART, standalone mode), LLM(Vicuna).
- **objective :** text read, masked text prediction, captioning, qa, qg /  CL loss + LM loss -> qa / LM loss 
- **baseline :** Pushing the results of OCR into LLM, BLIP, UDOP, Pix2Struct, MatCha, Donut, T5
- **data :** (text read adn masked text prediction) IIT-CDIP, Webvicob, (captioning) CC3M, (QA + QG) WKVVQA, SquadVQA, TydiVQA (proposed in this paper)
- **evaluation :** (ChartQA) Accuracy, ANLS, nED, BERTScore, PPL
- **result :** It is much better than putting ocr in a simple LLM, and it is the best among multi-task models except InfoVQA for document-specific models. performance wise, sota is better than UDOP.
- **contribution :** Suggestions for how to better utilize ocr tokens in the document domain. Suggestions for CL methods to ensure performance doesn't falter when ocr is unstable.
- **etc. :** appendix is really full

## Details
### Architecture 
<img width="677" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e0c10e36-c304-4880-b25a-2202fd5d4818">

The overall structure is similar to BLIP-2
<img width="525" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5dd8f271-8608-4e61-a642-63b363d45f35">

In addition to the vision encoder output, we also use an auxiliary encoder! The vision encoder output and the aux encoder output are concatenated and enter the decoder with cross-attention.

The motivation for using CA was that text-rich images have too many OCR results, which eats up too many tokens!
<img width="341" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/bc9cee24-ae76-469a-ae01-59adcfcea06a">


<img width="336" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/19a29c8a-a7bb-4a81-bee7-66e8f04489c9">

<img width="679" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f98f7cf9-eace-4105-89af-235b05bca1be">

The picture is a bit confusing (as if it's cropped), but the postivie pair that is the target of contrastive seems to be contrasting the aux output from the above picture with the output of the corresponding (coordinate overlapping) patch.
The explanation for why we did this is that it is advantageous when the OCR output is noisy or the results are limited.
<img width="352" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2fc35dfc-e9b4-4d16-843e-57c7950c48c7">

<img width="345" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f6ca88a1-7fc4-466f-868c-b85e0d6f31d0">


<img width="355" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0237f0f0-4609-4664-9dbb-a067a7dd8b7b">

Like saying that a patch to the vision encoder makes it closer to the ocr token encoder output, so it performs well even if it misses some ocr results?
On the other hand, OVD uses Owl-ViT (with coco 80 classes), and DocVQA says that the performance is almost the same without OVD (81.2 -> 80.9, A.2.) I wonder if it's because of DocVQA.

### Dataset 
<img width="333" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/127e2c5d-5eac-4e96-8630-d3910ea2256f">

### Training 
 details 
- LM : CL = 1: 0.5
- The number of learnble queries is 224
- When putting an image into the vision encoder, use the variable resolution in the pix2struct (https://github.com/long8v/PTIR/issues/140)
<img width="340" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f464231f-ff20-4c31-8eb2-c162006a05d2">


### Result
<img width="690" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/01c66af3-419c-4b32-837c-c3ab7176659c">
<img width="322" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b09d5c70-a255-4aae-9b0b-d2ec7692515a">
<img width="335" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f5d15477-70c6-492d-b00b-4cdd7c7ce9f6">

Arithmetic improvements

<img width="691" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ccf5c425-b4eb-4c1a-b7cf-e4c865f7a82b">

LLM makes you better at math, but also produces bad text
<img width="704" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1598695f-6e91-43be-8d1d-03e6fc1ca646">
