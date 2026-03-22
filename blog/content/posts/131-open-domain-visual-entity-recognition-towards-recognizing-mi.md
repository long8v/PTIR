---
title: "Open-domain Visual Entity Recognition: Towards Recognizing Millions of Wikipedia Entities"
date: 2023-06-23
tags: ['multimodal', 'CLIP', '2023Q1', 'retrieval']
paper: "https://arxiv.org/abs/2302.11154"
issue: 131
issueUrl: "https://github.com/long8v/PTIR/issues/131"
summary: "Much talked about... - New benchmarks and baselines."
---
<img width="829" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4cc07c59-1c9c-4aad-a020-393437777657">


[paper](https://arxiv.org/abs/2302.11154)

## TL;DR
- **I read this because.. :** It's been mentioned a lot and...
- **task :** Open-domain Visual Entity recognition(OVEN). 
- Problem :** VLM can answer questions about generic objects, but can't it pull out finer-grained visual concepts?
- **idea :** Create an entity based on wikipedia and define the problem of finding the entity that answers the query {image, query} given {image, query}.
- **input/output :** context image + text query + knowledge base(wikipedia) -> wiki page 
- **architecture :** For dual-encoder, CLIP. 1) CLIP2CLIP, where weights for cosine similarity for 4 things (context image, query <-> wiki page image, text) are learned. 2) CLIP fusion with two layers of transformers that fuse information on top of image encoder and text encoder. 3) PALI finetune with PALI and then output of PALI to BM25 for retrieval from wikipedia. Specific arch is CLIP based ViT-L14 / PaLI-3B and PaLI-17B.
- **objective :** For dual encoder, since it is similiarity based, InfoNCE or something like that should have been used? PaLI is CE loss.
- **baseline :** I'm proposing a benchmark, so the paper itself is the baseline.
- **data :** 14 benchmark datasets with wiki and mapping. It looks like it's been cleaned up a bit and has some human annotations.
- Prediction with **evaluation :** accuracy. The harmonic mean of the accuracy for seen entities and the accuracy for unseen entities.
- **result :** PALI performs better than I expected, i.e., it keeps entities in the model. In particular, query split (based on VQA) performed well. Even for CLIP Fusion and CLIP2CLIP, the performance is similar to PaLI in terms of number of parameters, so it's a pretty strong baseline!
- **contribution :** Presenting new benchmarks and baselines.
- **etc. :**

## Details

### Task set-up
<img width="1260" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ccd0dbdb-730d-4fc3-9c53-a2949ed396e5">

This is my first suggestion, so the setup itself is important.
If you look closely, there is a context image and a question about it, i.e. it's not just image retrieval!
The problem set is to find the entity page in wikipedia that corresponds to the answer using a combination of image and query.

### Data
There are two ways to do this,
- Entity Setup : Datasets based on classification or retrieval -> Create questions as templated query generation
- Query Setup : VQA-based datasets -> refine if the answer to the question is not for an entity

<img width="1284" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6bac031d-01dc-4eb5-b722-ed82a8d1813e">

And then somebody said, "Oh, we're going to do label disambiguation or something.

### evaluation
Harmonic average of accuracy for seen entity/unseen entity
<img width="622" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/371a958f-6011-487e-aa24-5bd56debb90b">


### Baseline
$x^t$ : input intent
$x^p$ : input content
$p(e)$ : entity images
$t(e)$ : entity text

<img width="401" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/00db5e65-fee5-49af-a6d7-92595b751b14">

- Dual encoder
Using CLIP. What if we rephrase the problem as a retrieval problem?
For CLIP2CLIP, it finds the cosine similiarty of $(x^p, t(e)), (x^t, p(e)), (x^p, p(e)), (x^t, t(e))$ and learns only the four parameters that are its weights.
CLIP Fusion Learn Transformer to fuse two encoders on top of each other.

- Encoder-Decoder model
Just train the oven training dataset with PALI loss. For the output that PALI spits out, I used BM25 as the final output with the wiki page I found.

<img width="617" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0ec5a09d-6fb1-4f25-b184-685d8465872f">

### Result
<img width="1108" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/fe1d6102-9feb-4861-b14d-4124678e5df3">

- For CLIPFusion, seen entity performance for query split was very good, likely due to the inclusion of the VQ2A objective. However, unseen was very poor
- CLIP2CLIP performs well overall.
- PALI was surprisingly better than I expected. Unlike CLIP, it shouldn't be able to access entities in an infer situation, but its performance is good even for Unseen, so it seems to have that information internally.
- The overall performance doubled from CLIP -> CLIP Fusion, even though the parameters were doubled, PALI didn't perform as well.
- It performed much worse than human evaluation.


<img width="576" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/16a683fb-9f26-4e4d-8287-c88922fdfac1">

When comparing the two, PALI understood the question better, but sometimes answered more generically.

<img width="575" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/103c0d96-220b-489c-892e-c7aecc34bfe4">

