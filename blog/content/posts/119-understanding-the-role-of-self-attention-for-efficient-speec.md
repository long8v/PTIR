---
title: "[110] Understanding the Role of Self Attention for Efficient Speech Recognition"
date: 2023-04-17
tags: ['2022Q1', 'ICLR', '25min', 'transformer']
paper: "https://openreview.net/pdf?id=AvcfxqRy4Y"
issue: 119
issueUrl: "https://github.com/long8v/PTIR/issues/119"
summary: "Presented at a paper meeting. Characterization of SA looks interesting~ - First analysis of SA in ASR! Can this methodology be applied to other domains?"
---
<img width="824" alt="image" src="https://user-images.githubusercontent.com/46675408/232624306-a8454f82-92a0-4e9e-a80b-cb5e9cadbd26.png">

[paper](https://openreview.net/pdf?id=AvcfxqRy4Y)

## TL;DR
- **I read this because.. :** Presented at a thesis meeting. It's a characterization of SA, so it looks interesting~.
- **task :** ASR
- **problem :** transformers are used in ASR, but there is no analysis of the nature of self-attention.
- **idea :** measure diagonality to compare by layer / observe tendency for similar phonemes to attend / phoneme classification task by layer -> attention map could be reused
- **architecture :** Conformer-M + attention map reuse
- **objective :** CTC loss
- **baseline :** Conformer-M w/o reuse
- **data :** LibriSpeech
- **evaluation :** 
- **result :** 1.96 times of speedup in inference and 33% reduced training time
- **contribution :** First SA analysis in ASR! Can this analysis methodology be applied to other domains?
- **limitation / things I cannot understand :** I do not know the details of the architecture

## Details

<img width="666" alt="image" src="https://user-images.githubusercontent.com/46675408/232624567-98d7d7fa-e140-4872-9fcf-2ae31529acc5.png">


- cumulative attention diagonality
<img width="543" alt="image" src="https://user-images.githubusercontent.com/46675408/232624748-0182221a-d459-47e6-803b-ddc13d188896.png">


<img width="682" alt="image" src="https://user-images.githubusercontent.com/46675408/232624601-eab77e7d-29d0-449b-991f-088a62d1d64d.png">

When making audio-to-text transitions, we tend to attend to our neighbors. -> attending a lot of neighbors increases diagonality
But since diagnolatiy is handled in the upper layers, you can see that we are looking at linguistic in the upper layers

And then the layers underneath are responsible for phonemes, which you can see in the two pictures below.
<img width="698" alt="image" src="https://user-images.githubusercontent.com/46675408/232625482-433bdd15-98cd-419d-9469-1cea0076da58.png">

I looked at the attention map on a phoneme-by-phoneme basis, and the tendency for similar pronunciations to attend did not show up in the layer above.

(Formula to measure attention map in phonemes
<img width="527" alt="image" src="https://user-images.githubusercontent.com/46675408/232626282-1db577b0-df83-4176-851c-3341733ad7d5.png"> )

<img width="871" alt="image" src="https://user-images.githubusercontent.com/46675408/232625386-1b94bc1e-5945-49ea-b78e-11b7d8bcd624.png">

The layers below are better at phoneme classification. The layers above are performing worse.

Based on these findings, we propose an architecture for reusing SAs.
<img width="714" alt="image" src="https://user-images.githubusercontent.com/46675408/232625570-2dd562c1-824c-45ac-847f-7503c45de245.png">

The attention map reuse was not proposed here for the first time, but in the NLP field, but they didn't analyze why it was reused. But this paper analyzes it, so it makes sense.

<img width="969" alt="image" src="https://user-images.githubusercontent.com/46675408/232772635-96d856d4-3c64-4614-8402-72e50b3b3cb2.png">

Only V is newly projected per layer
Sharing Attention Weights for Fast Transformer

https://arxiv.org/pdf/1906.11024.pdf

c.f. ConFormer 
conv + SA + conv
<img width="463" alt="image" src="https://user-images.githubusercontent.com/46675408/232773068-ba22c881-892b-4534-8b09-8c89a527112e.png">

