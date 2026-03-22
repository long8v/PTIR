---
title: "Perceiver IO: A General Architecture for Structured Inputs & Outputs"
date: 2023-04-24
tags: ['multimodal', '2021Q2', 'ICLR', 'DeepMind', 'MTL']
paper: "https://arxiv.org/pdf/2107.14795.pdf"
issue: 120
issueUrl: "https://github.com/long8v/PTIR/issues/120"
summary: "Mentioned in CS330 lecture. In #118 also mentioned in CS330 lecture, IO attached is not different just because we used Perceiver and spring - test for quite a few modalities. Isn't the way we put task embedding / PE embedding in decoder a contribution point?! The rest of the stuff just feels like it's not new"
---
<img width="612" alt="image" src="https://user-images.githubusercontent.com/46675408/233893986-33a2b0e1-0be8-4621-80c1-324f37170a13.png">

[paper](https://arxiv.org/pdf/2107.14795.pdf)

## TL;DR
- **I read this because.. :** Mentioned in CS330 lecture. In #118, it was also mentioned that using Perceiver doesn't make any difference to IO and spring
- **task :** image classification, language modeling, optical flow, StarCraft II, ...
- **problem :** I have models for each domain/task. Life would be easier if I could handle them with one NN
- **idea :** transformer encoder-decoder structure, but let's use perceiver structure (where input modality goes to CA) + output query
- **input :** (encoder) N x D-dimensional latent array (decoder) positional embedding or task embedding
- **output :** (encoder) context vector (decoder) class(for image classification), token id(for MLM), ... 
- **architecture :** But the encoder is a perceiver (text, image, video, etc. go into the CA) / decoder is a CA between the encoder context vector and the output query.
- **objective :** objective function for each task
- **baseline :** GLUE(BERT), Image Classification(ViT-B), Optical Flow(PWCNet, RAFT), StarCraft(Transformer), AudioSet Classification(Perceiver IO)
- **data :** English Wikipedia + C4, ImageNet, JFT.... 
- **result :** Better performance on GLUE vs. BERT for the same FLOPS. Optical flowbars also perform well against a few metrics compared to baseline. The rest have decent performance, but not the best.
- **contribution :** test. for quite a few modalities. isn't the way you put task embedding/PE embedding in the decoder a contribution point?! The rest of it seems like it's not new
- **etc. :**

## Details
### Architecture
<img width="589" alt="image" src="https://user-images.githubusercontent.com/46675408/233895628-bfc16f01-c231-4e01-aa73-0c381353a332.png">

### Output Queries
<img width="581" alt="image" src="https://user-images.githubusercontent.com/46675408/233895652-0370dc94-0b20-41fb-9497-9c392e603ad0.png">

- Classification, such as image classification, can be done by simply embedding the task in the
- If multi task, multiple task embeddings
- For MLM, 2048 Positional Embeddings

### Architecture Details
<img width="584" alt="image" src="https://user-images.githubusercontent.com/46675408/233895694-1a84bc85-81dc-4b94-9eac-df5dd8519e22.png">


### Result 
- tasks
<img width="1041" alt="image" src="https://user-images.githubusercontent.com/46675408/233896560-049ca9da-f2ee-481f-9e9f-592ec7ddd6af.png">


- GLUE
<img width="577" alt="image" src="https://user-images.githubusercontent.com/46675408/233895675-a9c83357-985b-4adb-ab36-9404c748f5eb.png">

The introduction also emphasizes using UTF-8 bytes, but I don't know if this is a contribution (is there any prior work like BBPE?).
This makes max_len longer than $$O(n**2)$$, and the structural linear increase in complexity seems to be a contribution!
In this table, it has much larger parameters than BERT, but lower FLOPS. The parameter decreases the hidden dim and increases the depth by a lot.
Compared to BERT, max_len was increased from 512 -> 2048 and vocab size was reduced to 256.

- image classification
<img width="588" alt="image" src="https://user-images.githubusercontent.com/46675408/233895750-3bc96675-3cf4-4b04-8ab9-1093b1b8cb20.png">

ViT-B/16ã¨ã"ã¨ã"ã'ˆã£ã¦éžå¸¸ã"ãªã'Šã¾ã-ãŸã€' First of all, it seems worse than ViT Performance
JFT pretraining scored 86.4 points, which is a bit different from ViT-H/14's 88.6 points per viewer (although the number of parameters is 1/3).
In the end, the best performance is the one with Conv.
Other than that, it looks like it's better than its predecessor Perceiver?

- AudioSet Classification
<img width="585" alt="image" src="https://user-images.githubusercontent.com/46675408/233895709-da9aa669-36d3-4689-a7e0-c704f0e2f69a.png">

- StarCraft II
<img width="570" alt="image" src="https://user-images.githubusercontent.com/46675408/233895724-061bea35-a8de-4e82-87fc-8c2ff10ff17a.png">



