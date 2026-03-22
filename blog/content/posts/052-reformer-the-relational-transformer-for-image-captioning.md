---
title: "[46] ReFormer: The Relational Transformer for Image Captioning"
date: 2022-08-03
tags: ['SGG', '2021Q3', 'captioning']
paper: "https://arxiv.org/pdf/2107.14178.pdf"
issue: 52
issueUrl: "https://github.com/long8v/PTIR/issues/52"
---
![image](https://user-images.githubusercontent.com/46675408/182570807-e92c1bbb-479d-4301-9dff-88ba79cd624d.png)

[paper](https://arxiv.org/pdf/2107.14178.pdf)

## TL;DR
- **task :** image captioning and SGG
- **problem :** It is helpful to use scene graph in the image for captioning, so I use external SGG + GCN as input. However, (1) using image captioning loss (=MLE) instead of relation-related loss does not train the encoder well enough, and (2) the encoder is not in a form where the relation can be extracted separately, so it is less universal and less explainable.
- **idea :** image captioning and scene graph generator in one transformer model!
- **architecture :** FasterRCNN with bbox and Transformer encoder with self-attention coarse output to m(m-1) for relation prediction and hidden vector weighted sum of L layer of transformer encoder to decoder for token prediction.
- **objective :** cross-entropy loss for SGG / MLE for captioning. 
- **baseline :** IMP, MOTIFS, VCTree(for SGG)
- **data :** COCO(image captioning), Visual Genome -> There are some images that overlap with COCO and Visual Genome, but they are very few.
- **result :** Both image captioning and SGG are SOTA
- **contribution :** SGG + captioning in one model!
- **limitation :** SGG is also a sota.

## Details
### A Relational Encoding Learning Idea
![image](https://user-images.githubusercontent.com/46675408/182572329-7d286170-18a3-489d-8de4-8a9e7bcc729a.png)

A typical captioning objective might look like this
![image](https://user-images.githubusercontent.com/46675408/182575885-10a20277-73a8-4aec-9b72-75e4274e1e9b.png)

y is the token $x$ is the visual feature of the image.
In order to add scene graph information when captioning, we first put the image feature x into some pretrained SGG to get the graph, then put the graph into GCN to embed it well, and then concatenate the embedding and the image feature and put it into the captioning input.
In this case, the objective is captioning, not SGG, and there are studies that show that the encoder performs somewhat well if the decoder is strong even if the encoder does not extract much information, so it is questionable whether the encoder is trained to extract relation embeddings well.

### Architecture
![image](https://user-images.githubusercontent.com/46675408/182586575-69233f0c-8481-4690-8989-0fe6b81d635b.png)

#### Encoder Architecture
For the Encoder, we took the GloVe vector of the box label from the bbox information and CNN, fired the transformer encoder, concatenated the m(m-1) pairs with the relation vector, and softmaxed the relation.

#### Weighted Decoder for Image Captioning 
When decoding, we replaced the output vector of all layers of the transformer with the token prediction given the weighted sum.
![image](https://user-images.githubusercontent.com/46675408/182587123-3f8624f7-a761-402b-a7ca-5228c8393064.png)

### Sequential Training with Inferred Labels
(i) Faster RCNN training on Visual Genome
(ii) Train Encoder with Faster RCNN trained on Visual Genome
(iii) encoder is trained and then trained as encoder - caption decoder for COCO dataset

I tried caption loss and SGG loss weighted sum, and ablation performed worse than caption loss alone.
![image](https://user-images.githubusercontent.com/46675408/182588768-a249b6b6-65da-49ba-a4ba-5daab02bfae6.png)

### Results
#### SGG
![image](https://user-images.githubusercontent.com/46675408/182742322-9e0c93d4-0cff-45a8-9e3d-388bea856a24.png)

c.f. two-stage SGG comparison
Predicate classification(PredCLS) : given GT bbox and cls, predict predicates
Scene graph classification(SGCLS) : given GT bbox, predict predicates and object class
As if SGDet = SGGen

|SGDet|R@20|R@50|R@100|
|--|--|--|--|
|Reformer(here)|25.4|**33.0**|37.2|
|Seq2Seq https://github.com/long8v/PTIR/issues/50|22.1|30.9|34.4|
|BGT-Net(GRU) https://github.com/long8v/PTIR/issues/51|**25.5**|32.8|**37.3**|
|RTN https://github.com/long8v/PTIR/issues/49|22.5|29.0|33.1|

|SGCls|R@20|R@50|R@100|
|--|--|--|--|
|Reformer(here)|36.6|40.1|41.1|
|Seq2Seq https://github.com/long8v/PTIR/issues/50|34.5|38.3|39.0|
|BGT-Net(GRU) https://github.com/long8v/PTIR/issues/51|41.7|**45.9**|**47.1**|
|RTN https://github.com/long8v/PTIR/issues/49|**43.8**|44.0|44.0|

#### Captioning
![image](https://user-images.githubusercontent.com/46675408/182742392-575d1547-255c-4f9a-b2f1-9be1723079c0.png)

#### Ablation for captioning
![image](https://user-images.githubusercontent.com/46675408/182742504-42e2361c-dfc4-4f74-8e68-b584a53a7c3d.png)
