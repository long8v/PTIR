---
title: "LiT: Zero-Shot Transfer with Locked-image text Tuning"
date: 2023-07-06
tags: ['2021Q4', 'google', 'CLIP']
paper: "https://arxiv.org/pdf/2111.07991.pdf"
issue: 135
issueUrl: "https://github.com/long8v/PTIR/issues/135"
summary: "How does it perform when importing a pre-trained vision backbone and training on clips? - A paper exploring supervised + contrastive."
---
<img width="1165" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/226c78db-3477-49ba-8a66-687531bb9e40">

[paper](https://arxiv.org/pdf/2111.07991.pdf)

## TL;DR
- **I read this because.. :** What is the performance when importing a pretrained vision backbone and training a clip?
- **task :** Contrastive Learning
- Problem :** Isn't the {image - text} pair in CLIP too noisy, but I want the zero-shot transfer to be supervised. I want to import CLIPs from pretrained as well, but what works best?
- **idea :** experiment with 6 different cases of vision encoder / text encoder: pretrained + freeze(lock), pretrained + learnable, randomly initialize
- data :** CC12M, YFCC100M-CLIP(15M), 4B data of ALIGN type
- **input/output :** image, text -> score
- **architecture :** ViT-g/14 + BERT 
- **result :** Better than CLIP, fine-tuned, from sctrach. zs performance is good, especially in OOD. Locking the image encoder is the best performance. In this case, the vision encoder does not matter the architecture and it does not matter whether it is trained supervised or unsupervised. In other words, we utilize the vision encoder trained with relatively clean data, and the text encoder is only learning by reading the information from the vision encoder.
- **objective :** InfoNCE
- **baseline :** CLIP, from0scratch, fine-tuned, ALIGN
- **evaluation :** zs OOD ImageNet classification, 7 [VTAB-natural tasks](https://ai.googleblog.com/2019/11/the-visual-task-adaptation-benchmark.html)
- **contribution :** A paper exploring supervised + contrastive.
- **etc. :** text encoder type. Feature aggregates are great because there's a lot of experimentation: cache or global. multilingual. text encoder size.

## Details
The basic idea is this I'm learning both a vision encoder and a text encoder from scratch in CLIP, and I want to bring a pretrained one with me.
Here's how to do it
<img width="562" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ad5f10b9-3205-4b8a-bbab-304d5ba0f764">

- L: get pretained model and lock
- U: import and unlock pretrained model
- u : from scratch

This gives us a total of 6 cases, and the ablation for them is as follows (in order of vision tower, text tower)
<img width="565" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e0172c8e-b6dd-4111-8f2b-3baaa2ecfb3c">

By ImageNet zs
- LU best -> proposed LiT 
- LU > UU : Freezing the image encoder at all is surprisingly better than Uu.
- LU ~ Lu: The text encoder performed similarly to from srcatch and from pretrained.
- UU > uu: both importing pretrained performs better than from scratch
- UL, uL, LL all bottom: freezing the text encoder is usually a bad performance. Worse than uu, which is supposed to be CLIP learning.

retreival is UU > luneng

<img width="559" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5a07a79f-811f-41c4-9a04-d77fb3dcddff">

<img width="584" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/159d82de-7b54-49d4-b218-2b3ba7841fcb">


LU > UU: Why is it better to be locked?

<img width="544" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/52d32b7a-a48c-4949-982e-aa365dedacae">

The first row is the loss with LiT trained data, and the loss is high because the image encoder is locked.
The second row is evaluated with data that is OOD, and the locked loss is the lowest -> i.e., the image encoder is OOD-resistant by locking. We conclude that contrastive finetuning is bad for visual representation.
(At first glance, it seems to be the opposite of #134... he was saying that CLIP is already trained as contrastive, so it is robust to OOD and loses OOD ability in supervised set. But this seems to be because they were IN and the ViT they learned with supervised learning was learned with JFT).
The last row is a few-shot linear regression with logit, with Lu performing best.

image encoderI tried locking it at the beginning and gradually unlocking it, but it didn't perform that well.

At first glance, you might say that ViT is better because it was trained in a supervised setting, so we tried it on kids trained with other pretraining techniques.
<img width="553" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9d83d218-7eba-49b2-848f-def8c77e48c7">

Children trained with other methods showed similar trends.

## Ablations
- text encoder
<img width="508" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d313e6fd-9f71-4ac4-ab80-b1501d259fe4">


(yfccm) BERT > T5 to ViT (not sure what it is) > mT5
(ours, in-house data) ViT > BERT

> We consider four possible transformer-based text models [63]—the transformer from ViT-B [21] which also resembles that used in CLIP [46], T5-base [47], mT5-base [67], and the classic

- text / image encoder scale 
<img width="556" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4d5626b0-cb6d-4901-8841-9b628a9fa116">

Improved performance when enlarged text is enlarged.

- multi-lingual training
When they learned together without refining to english only, english's performance didn't get worse, but the other kids' performance improved.
<img width="550" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7662d436-b771-4f02-8618-38e6d49f4667">

I think it would have been better to start with the mT5 tokenizer and pretrained multilingual when learning.

- local loss vs global loss

<img width="512" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b0d2a78d-e3ef-43c0-a906-53b318e4111b">

I like global losses, and I like BS to be big no matter what.
Since LiT has a frozen image encoder, it was more memory efficient to do image precomputation.