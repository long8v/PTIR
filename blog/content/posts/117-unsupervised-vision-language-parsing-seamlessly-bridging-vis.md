---
title: "Unsupervised Vision-Language Parsing: Seamlessly Bridging Visual Scene Graphs with Language Structures via Dependency Relationships"
date: 2023-04-04
tags: ['2022Q1', 'dataset', 'CVPR', 'graph']
paper: "https://arxiv.org/abs/2203.14260"
issue: 117
issueUrl: "https://github.com/long8v/PTIR/issues/117"
summary: "What else can you do with SG? SG annotation has its limitations. Is it possible to parsing scene graphs from captions or image - text pairs? - Suggest new datasets/baselines"
---
<img width="674" alt="image" src="https://user-images.githubusercontent.com/46675408/229678142-edfc0956-350f-4961-9400-2a71a1979c22.png">

[paper](https://arxiv.org/abs/2203.14260), [code](https://github.com/LouChao98/VLGAE)

## TL;DR
- **I read this because.. :** What else can you do with SG? SG annotation has its limitations. Is it possible to parsing a scene graph from a caption or image - text pair?
- **task :** Given a (proposed) image and caption, create a dependency tree for the caption and predict bboxes for the objects in the tree.
- **idea :** encoder - decoder form
- architecture :** text is word embedding + pos embedidng concat, image is object first, then attribute/relation prediction, then attention to create context encoding. Given the context encoding, generate a parse tree and tag sequence.
- **objective :** EM + contrastive loss with MLE (representation of each node and whether image I is positive or negative)
- **baseline :** DMV(dependancy structure induction), MAF(Visual Grounding)
- **data :** (proposed) VLParse
- **evaluation :** Directed / Undirected Dependency Accuracy (DDA/UDA), Zero-Order Alignment Accuracy (is "a table" in the caption well matched with bbox?, IoU + attribute), First/Second-Order Alignment Accuracy (first is the text in the caption and second is the relationship of the caption text to the object bbox = zero + first combined)
- **result :** Better performance compared to Language Structure Induction / Evaluation on Visual Phrase Grounding task
- **contribution :** Propose a new dataset/baseline
- **limitation / things I cannot understand :** What do you mean by decoder architecture?
 
## Details
<img width="634" alt="image" src="https://user-images.githubusercontent.com/46675408/229679674-7554c4c0-25d8-4faf-b316-45610d2c70ed.png">

This is an illustration in the introduction, but it doesn't actually create a Scene Graph. It just utilizes the scene graph data when creating it.

### proposed data: `VLParse`
<img width="630" alt="image" src="https://user-images.githubusercontent.com/46675408/229679768-cba2c477-6c2e-4bad-a65b-c2d0218dbbfa.png">

<img width="604" alt="image" src="https://user-images.githubusercontent.com/46675408/229679812-9ce154e0-806d-4fda-a332-cea676616fe3.png">

Built with heuristics + human refinement

## proposed task: Unsupervised Vision-Language Parsing

input : image $\mathbf{I}$, sentence $\mathbf{w} = {w_1, w_2, ... w_N}$
output : parse tree $\mathbf{pt}$. Each object should also predict the box region. In this paper, we use faster rcnn to select candidates and map them.

<img width="1245" alt="image" src="https://user-images.githubusercontent.com/46675408/229680304-361d43e5-2fa0-498a-b577-1df74b47eb36.png">

### architecture
 **Feature Extraction**
- Visual Feature
- Faster RCNN -> RoI -> $\\{ V_i^o \\}^M_{i=1}$ is the feature of node `OBJECT`
- Each `OBJECT` node is tagged with an `ATTRIBUTE`. This is created by $v_i^a= MLP(v_i^o)$.
- For the two `OBJECTs' we add a zero-order node called $RELATIONSHIP$ $v^img_{i->j,0}%$
- All but the features of `OBJECT` are random initialize
- Textual Feature
- For each word $w_i$, use POS tag embedding and pretrained word embedding in cat for each word $w_i$.
- Biaffine score for the representation $w_{i->j}$ between two words
<img width="320" alt="image" src="https://user-images.githubusercontent.com/46675408/232656235-443c2f1e-6ce0-43d5-a25f-91bb0d79d9ce.png">
 
**Structure Construction**
- encoder 
- Create a contextual encoding c by performing attention operations on the text feature and visual feature.
- Perform attention operations on the tokens $\\{w_i\\}$ in the caption and the scene graph representation $\\{v_i, v_{i->j}\\}$$ and add them together to create a context vector $c_i$.
- As if $Q=v_i, K=w_i, V=w_i$.
<img width="133" alt="image" src="https://user-images.githubusercontent.com/46675408/232657783-d6ea9ed2-2d39-4305-9e21-b30e728093db.png">

- Create a global context vector $s$ by averaging pooling over all $c_i$ to create an overall context vector $s$
- decoder 
- Create a tag sequence $t$ and a parse tree $\mathbf{pt}$. Use dynamic programming to create the parse tree

**Cross-Modality Matching**
-  matching score
<img width="245" alt="image" src="https://user-images.githubusercontent.com/46675408/232660242-1ddc2d69-e76c-467f-a849-32a6bbda2480.png">

<img width="282" alt="image" src="https://user-images.githubusercontent.com/46675408/232660275-54123eb8-7f5c-4394-85fc-4739bb4b9a6b.png">

You can get posterior with the above
<img width="302" alt="image" src="https://user-images.githubusercontent.com/46675408/232660293-23d6cbd5-98a4-451b-a698-41466aea0f69.png">


### Learning

**MLE loss**
<img width="517" alt="image" src="https://user-images.githubusercontent.com/46675408/229680481-17f3bac6-c138-485d-8510-739c1b8c941f.png">

- $t_i$ : tag sequence. 
- $\mathbf{pt}$ : parse tree.
In this case, MLE loss is trained with the EM algorithm without targets!
E step: generate parse trees given $\theta$
M step: learn $\theta$ by gradient descent in terms of likelihood given a parse tree

where tag is a methodology for expressing dependency parsing as a tag.

<img width="453" alt="image" src="https://user-images.githubusercontent.com/46675408/232661643-90e22b0f-2c1e-44ea-ba90-bbae3c7b28d4.png">

c.f. [Parsing as Tagging](https://aclanthology.org/2020.lrec-1.643.pdf)

<img width="404" alt="image" src="https://user-images.githubusercontent.com/46675408/232658588-d9d2cad4-bde6-4db7-8e71-a917311fd9cf.png">


**Contrastive loss**
<img width="545" alt="image" src="https://user-images.githubusercontent.com/46675408/229680403-17b63e62-7c41-4353-a65a-6e11e9b5ad2b.png">

 - $\mathbf{\hat{I}}$ : negative image 
 - $c$ : contextual encoding. $c_i = \sum Attn(w_i, v_i)w_i$
- $w_i$ : the i-th token in the caption
- $v_i$: image feature of the object.
- The sim function is just defined internally

**Inference**
<img width="319" alt="image" src="https://user-images.githubusercontent.com/46675408/229680977-15be1390-d29c-4679-a65e-1910add3f551.png">

Create all possible parse trees and find the most likely one
And if we find the closest $v$ to each contextual encoding c, we can also create a scene graph (the relation is the one in the caption, right?)

<img width="347" alt="image" src="https://user-images.githubusercontent.com/46675408/229681043-ed7087af-ea77-4356-9a50-d70186de38b6.png">


### Result 
<img width="1286" alt="image" src="https://user-images.githubusercontent.com/46675408/229681274-4f84b297-ce67-4d2e-8326-0c257c812f41.png">

- Since there is no gt structure for caption, I made it an external parser and used Visually Grounded Neural Syntax Acquisition https://arxiv.org/pdf/1906.02890.pdf

etc.
- Finish reading and cleaning up the model part
- Is SGG used for visual grounding?
        - https://github.com/TheShadow29/awesome-grounding
- Just as the dataset Flickr30k Entities / RefCOCO/RefCOCO+/RefCOCOg has a lot of VGs, so does the dataset Flickr30k Entities / RefCOCO+/RefCOCOg.
- There is a study called scene-graph grounding, which does object location when given sgg + image, but what is it used for...
            - https://openaccess.thecvf.com/content/WACV2023/papers/Tripathi_Grounding_Scene_Graphs_on_Natural_Images_via_Visio-Lingual_Message_Passing_WACV_2023_paper.pdf
- As if it wasn't.
