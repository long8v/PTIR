---
title: "[90] Neural Collaborative Graph Machines for Table Structure Recognition"
date: 2022-12-22
tags: ['2021Q4', 'CVPR', 'graph', 'document']
paper: "https://arxiv.org/abs/2111.13359"
issue: 99
issueUrl: "https://github.com/long8v/PTIR/issues/99"
summary: "Researching table related stuff. Reading through SGG for any ideas. - sota"
---
<img width="674" alt="image" src="https://user-images.githubusercontent.com/46675408/209046093-50aac421-d0fb-4fc8-a301-13574c1b8242.png">

[paper](https://arxiv.org/abs/2111.13359)

## TL;DR
- **I read this because.. :** table related research. wondering if SGG has any ideas for me.
- **task :** Table Structure Recognition(TSR)
- **problem :** There are three modalities for representing tables: coordinates, images, and content. Usually coordinates are the most important feature, but if the image is distorted, we need to utilize other modalities rather than coordinates. How can we learn to make these modalities help each other?
- An architecture that's not early fusion, not late fusion... where you do each and then put them back together and iterate over multiple blocks.
- **architecture :** bboxes in the image as nodes and all connections as edges. For each modality, extract features with an MHA where Q is the feature and K=V is the edge representation (Ego Context Extractor), followed by three Cross Context Synthesizers that query each modality and write the other modality as K,V.
- **objective :** For every node i, j, check if there is an edge to it and if it is connected by a row, column, or cell, for each bce
- **baseline :** FLAG-Net, TabStr, DGCNN
- **data :** ICDAR-2013, ICDAR-2019, WTW, UNLV, SciTSR, SciTSR-COMP
- **evaluation :** Tree Edit Distance(TED), BLEU
- **result :** sota

## Details
### Motivation 
<img width="495" alt="image" src="https://user-images.githubusercontent.com/46675408/209047141-31befe01-6d06-4cd7-a153-4f743dae3818.png">

### Architecture
<img width="952" alt="image" src="https://user-images.githubusercontent.com/46675408/209047167-0df96a38-ac1a-4f1d-aa44-f36a777e1782.png">

<img width="542" alt="image" src="https://user-images.githubusercontent.com/46675408/209048074-f28842e2-c0d3-4f73-b6a9-22376624a620.png">
Use Compressed MHA (CMHA) from [Pyramid ViT](https://arxiv.org/abs/2102.12122) because MHA math is too complex

### Result
<img width="296" alt="image" src="https://user-images.githubusercontent.com/46675408/209047685-d4dfc678-1fdb-4769-8f40-4ddf2989eaa0.png">

<img width="561" alt="image" src="https://user-images.githubusercontent.com/46675408/209047708-e4ba58ec-2237-42ce-a9e1-5236f63241fb.png">

