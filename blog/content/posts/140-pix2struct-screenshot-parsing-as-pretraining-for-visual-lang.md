---
title: "Pix2Struct: Screenshot Parsing as Pretraining for Visual Language Understanding"
date: 2023-08-21
tags: ['ICML', 'google', '2022Q3', 'document']
paper: "https://arxiv.org/pdf/2210.03347.pdf"
issue: 140
issueUrl: "https://github.com/long8v/PTIR/issues/140"
summary: "I read that the way ViT variable resolution is handled in the document domain is a bit different - various task sota. Especially the UI side, which is probably the first time I've solved it together."
---
<img width="920" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/21d65bd3-3703-41c7-8c40-da08ccef60c5">

[paper](https://arxiv.org/pdf/2210.03347.pdf)

## TL;DR
- **I read this because.. :** I read that the document domain handles ViT variable resolution a little differently.
- **task :** document understanding / UI / image captioning 
- **problem :** I want to process the image input immediately without a pipeline, but there are some cases where the image ratio is extreme. I want to process not only documents but also UI at once.
- **IDEA :** There are a lot of webpages in the world, let's render the html as a screenshot and then generate the original html!
- **input/output :** web image with text -> text
- **architecture :** ViT + decoder (12 encoder w/ 768 hidden dim or 18 encoder, w/ 1536 hidden dim) -> Base(282M), Large(1.3B)
- **objective :** contrastive loss(html recontstuction + masked token prediction)
- **baseline :** Donut, UDOP, PaLI, VTP, DQAN, LATr, UIB, VUT
- **data :** Download URLs from C4 corpus and create 80M of screen shot data -> DocVQA, InfoGraphicVQA, UIChartQA, AI2D, OCR-VQA, RefExp (finding parts of a website that are expressed in natural language), Widget Captioning (captioning what a selected button does in an app screenshot, e.g. `find location`),
- **evaluation :** ANLS for DocVQA/InfoVQA, exact match for AI2D/RefExp/OCR-VQA, relaxed accuracy(RA) for Chart QA, CIDEr for generation task 
- **result :** Sota among those who only take image input. Otherwise, captioning loses to PALI for DocVQA and InfoVQA to UDOP. Donut wins all.
- **contribution :** Various task sota, especially the UI side, which is probably the first time I've solved it together.
- **etc. :** I can't believe I'm reading this now.

## Details

### variable-resolution 
<img width="928" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/bb32764a-d7bf-4c0c-a64d-c80660ee422f">

Usually, ViT is trained by resizing it to a square, which (1) makes it chunky and (2) performs poorly when the sequence length increases later when going to high resolution.
The idea here is to resize the image so that the aspect ratio is preserved, but the sequence length is maximally packed (this does not change the patch size).

### Pretraining
Using html render to url in C4
In this case, (1) use only visible elements and (2) replace child with grandchild if there is no visible element and child is present.
Use text + alt-text and filename or so
Tells me to recover the HTML in the blue-boxed portion of the image
<img width="774" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/86c6fa77-6fef-4329-bce1-dd50a358f6bf">

Additionally boxed in red to make it match. Sort of masked language modeling on images. about 50% of the text.

### Curriculum learning 
I'm not sure I'd be able to learn it from scratch, so I started by reading it.
Rendered with Book Corpus in a random color random font, then 30K steps or so. (200K in donut)

### Finetuning
Just like in GPT, we just put Q together, here we render the image with the question, etc.
<img width="890" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d80b6ddc-d4b6-4e1a-b242-488aae212b3c">

### Training Details
- 282M / 1.3B (Donut 143M)
- 12 layers 768 hidden dim / 18 layers 1536 hidden dim
- 128 image patches 
- 128 decoder sequence length
- The output should be no more than 128 characters long.
- batch size 2048 with 64 TPUs / batch size 1024 with 128 TPUs (196 with 64 A100s in donut)
- Validation with BLEU.

### Result 
<img width="902" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5088adea-3be4-4eb9-bdf9-c9fd154734af">

PALI loses out to captioning, and UDOP loses out to OCR, etc. for text-rich DocVQA.
Maybe the data itself is captioned a lot, so I'm behind the kids who learned it?
Other than that, it beats Donut / GIT and loses, especially on the UI side. Huge sota.

### Ablation 
- pretraining component
<img width="441" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/444baf47-628f-423d-8347-d00bd4a5e40b">

Screenshot Parsing dropped the most, followed by warmup and masking to a similar degree.

- variable-resolution
<img width="468" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/609b5335-99ff-4e6f-9cd8-32769e9f326f">

Padding looks pretty bad... stretch is out of proportion!