---
title: "[74] “This is my unicorn, Fluffy”: Personalizing frozen vision-language representations"
date: 2022-11-04
tags: ['dataset', '2022Q3', '25min', 'ECCV', 'nvidia', 'CLIP']
paper: "https://arxiv.org/pdf/2204.01694.pdf"
issue: 82
issueUrl: "https://github.com/long8v/PTIR/issues/82"
summary: "New task proposal. Efficient architecture!"
---
<img width="700" alt="image" src="https://user-images.githubusercontent.com/46675408/199869384-2af5d03d-5f98-4fc2-b30e-4b862cad9529.png">

[paper](https://arxiv.org/pdf/2204.01694.pdf)

## TL;DR
- **task :** personalized vision and language => personalized image retrieval/object detection/segmentation 
- **problem :** We want to learn user-specific objects efficiently, and adding adaptors to CLIP has the effect of worsening the performance of previous classes.
- **idea :** Let's learn a new concept by adding it as a new vocab! To do this, 1) learn an inverse function that finds the input word embedding given an image, 2) initialize the word embedding of the new concept by passing a few images of the new concept through the inverse function, and 3) refine it with the textual information of the new concept.
- **architecture :** CLIP
- **objective :** Learn to make the embedding of `A photo of a [new vocab]` closer to the embedding of `A photo of a [new vocab]` that passed through the image encoder, and farther away from the embedding of the super-concept of the new concept.
- **baseline :** Adapter, text-only CLIP, COLLIE 
- **data :** Youtube-VOS, DeepFashion2(both introduced in this paper)
- **result :** SOTA
- **contribution :** Propose a new task. Efficient architecture!
- **Limitation or something I don't understand:** CLIP looks like it needs to be re-read? Deep Sets?

## Details
### new setup, personalized vision & language
<img width="600" alt="image" src="https://user-images.githubusercontent.com/46675408/200228860-b6f1697d-391b-4591-8733-37284323564d.png">

- A new sentence S and image I are fed into the pretrained model h(S, I).
- You want a new concept, C, to enter so that it can be trained as V' = V U C
- Students are given a few images of concept C and descriptive text about the new concept (e.g., "mug," "short sleeve top")

### Adaptor vs add new vocab
<img width="600" alt="image" src="https://user-images.githubusercontent.com/46675408/200228887-06682e8f-1452-4b0e-b2cf-7b19d0946e6a.png">


If we don't add new vocab, the encoder output for the old class will be crushed. The model starts with the assumption that our text embeddings are large enough to hold new concepts.

### Architecture
<img width="600" alt="image" src="https://user-images.githubusercontent.com/46675408/200228555-647a2d9a-2ebe-4f1e-a309-9b09778f31ca.png">

Learn inverse mapping functions with a network called DeepSets

### Loss
<img width="600" alt="image" src="https://user-images.githubusercontent.com/46675408/200228607-2a01a20e-9a1e-49c8-9e76-9c2145d4c023.png">
