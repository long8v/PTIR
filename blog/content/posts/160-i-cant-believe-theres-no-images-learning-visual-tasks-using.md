---
title: "I Can't Believe There's No Images! Learning Visual Tasks Using only Language Supervision"
date: 2024-02-11
tags: ['ICCV', '25min', 'CLIP', '2023Q3', 'AI2']
paper: "https://arxiv.org/pdf/2211.09778.pdf"
issue: 160
issueUrl: "https://github.com/long8v/PTIR/issues/160"
summary: "aka. CLOSE. ICCV explorer PPT to find Kakao paper, but it's very similar to CapDec, so I read it thinking what's the difference. - Simple ideas make things work."
---
<img width="793" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/acaab25d-c99b-48b1-b999-aa29bcf5022f">

[paper](https://arxiv.org/pdf/2211.09778.pdf)

## TL;DR
- **I read this because.. :** aka. CLOSE. I read this because.. :** aka. CLOSE. ICCV explorer PPT to find Kakao paper, but it's very similar to CapDec, so I read it thinking, what's the difference?
- **task :** zero-shot cross modal transfer (taking what you've learned in one modality and transferring it to another)
- Problem :** Text and images have different embedding spaces, even when trained as contrastive! For example, for the COCO caption, the similarity of a positive {image, text} pair is 0.26, while the similarity between unrelated captions is 0.35.
- **IDEA :** Let's add gaussian noise to the text embedding space!
- **input/output :** (train) text -> text (infer) image, text -> text
- **architecture :** CLIP ViT-L/14 + T5 base 
- **objective :** cross entropy loss
- **baseline :** ESPER, CLIP Cls, TAP-C (zero-shot multimodal transfer models)
- **data :** COCO Captioning, SNLI (->SNLI-VE), VQA (->VQA-E), Visual News, synthetic captions with GPT-J RNG, GPT-J unigram, CURIE
- **evaluation :** For each benchmark, create an
- **result :** Among the existing multimodal models trained with text only, sota.
- **contribution :** A simple idea that makes something work.
- **etc. :** In conclusion, it's very similar to CapDec lol I'm in their related work, so I guess they put some analysis. Is learning this way in VLM more scalable, or is this just the same as LLaVA's approach?

## Details
- pipeline
<img width="916" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7ef78e8e-309e-4786-a7e8-0a88d6b86d9f">

Text embeddings are also from CLIP: things like context in VQA and premise in SNLI use T5 embeddings.
It's a little vague on how it's put into vectors, but it seems like if the embedding from CLIP is 2048 and the embedding that T5 receives is 512, it cuts the 2048 embedding and replaces it with four 512 vectors.

<img width="436" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9fc12ede-f3ef-4851-8c55-c07205e7a2c6">

Freeze CLIP's image/text encoder and only finetune T5

- modality adaptor
<img width="980" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/649ac712-d45f-45ae-8001-20288182c50a">

In conclusion, we scale with Gaussian noise + training hyperparameter w.

<img width="490" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5a9c519d-051d-45f2-ad37-74cd4535728c">

- sensitivitiy 
<img width="496" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/09eb29fb-80d7-47f1-9943-f3fa2be24a78">

Adding some noise to the text vector was insensitive, and shifting it slightly in the direction of the image (mean) improved performance for VE, while shifting it in the opposite direction (-mean) hurt performance.

 - learned adpater analysis
<img width="483" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6f5c04e2-545d-4d58-96ed-5dbaad482aae">

Learning that zero gaussian is not the best, so there is a better adaptor. Instead, it can't learn text-only, so it can't go into the main model.
linear is a way to train a linear map and cov. is a way to add structured noise as the covariance of the trainable text and image

- training data with language model
<img width="422" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f59913fc-8d17-4190-a1a4-575267c6a1be">

You can learn by using GPT-J, etc. to generate captions with words that appear frequently in coco.

- Can also do style captions
<img width="675" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8fc0b7d3-20f5-4b50-bb62-710e91e6ce88">


