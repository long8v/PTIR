---
title: "[95] Pixels to Graphs by Associative Embedding"
date: 2023-01-04
tags: ['NeurIPS', '2017', 'SGG', 'one-stage']
paper: "https://arxiv.org/pdf/1706.07365.pdf"
issue: 104
issueUrl: "https://github.com/long8v/PTIR/issues/104"
summary: "SGG initial paper - first one-stage SGG"
---
<img width="907" alt="image" src="https://user-images.githubusercontent.com/46675408/210468311-d07824b8-34b1-4eaf-9bde-e064aeef3045.png">

[paper](https://arxiv.org/pdf/1706.07365.pdf), [code](https://github.com/princeton-vl/px2graph)

## TL;DR
- **I read this because.. :** SGG Early Papers
- **task :** one-stage SGG
- **problem :** Retrieve object without RPN and also retrieve relation
- **IDEA :** Borrowing the idea of associate embeddings from multiperson pose estimation. A network that associates children with similar embeddings at body joints as the same person.
- **architecture :** hourglass + CNN + 1D CNN to generate a heatmap of each likely object and likely relation. for GT for train and top k activated pixels for infer. object predicts anchor based box regressor, cls id. relation predicts relation class, subject object id.
- **objective :** bbox regression loss + sigmoid loss for heatmap + ce for subject / object id +pull together loss + push apart loss 
- **baseline :** [VRD with lanugage prior](https://arxiv.org/abs/1608.00187), [Scene Graph Generation by Iterative Message Passing](https://arxiv.org/pdf/1701.02426.pdf)
- **data :** Visual Genome
- **evaluation :** SGGen, SGCls, PredCls
- **result :** SOTA
- **contribution :** first one-stage SGG
- **limitation/things I cannot understand :** It seems that the feature vector has to predict and has additional losses that are close and far from each other, but they seem to be in different directions. It's interesting to learn in one space.

## Details
<img width="870" alt="image" src="https://user-images.githubusercontent.com/46675408/210469355-3aaa50ae-d7dd-42c8-a1ad-be4e6780fd50.png">

A cut just because the picture is cute

### Preliminaries : Hourglass network
https://deep-learning-study.tistory.com/617
<img width="986" alt="image" src="https://user-images.githubusercontent.com/46675408/210469154-38b9a17a-c4df-4167-9d7e-2883712ce4cb.png">

A network similar to u-net. Used because both local and global information is needed for pose estimation.

### Architecture
<img width="890" alt="image" src="https://user-images.githubusercontent.com/46675408/210469524-e01c380d-db5b-409b-8e83-384cfdc2cb3d.png">

- Detecting graph elements
image -> hourglass network -> CNN -> 1 x 1 conv + sigmoid to draw heatmap for object and relation (define bbox as median of sbj, obj) -> (for training) GT vertices, edges to draw features and then 1) obj predicts anchor based offset regression, cls, id with faster RCNN method 2) rel predicts rel cls, sbj (src in paper) id, obj (dest in paper) id

- Connecting elements with associative embeddings
Above, we only picked out object and relation ids, now we need to combine them. For each vertex, we get a vector embedding, which needs to be learned to vary from vertex to vertex, and for edges, it needs to be an embedding that can represent the ids of subject and object.
So I added a pull together, push apart loss
 #### pull together loss
<img width="422" alt="image" src="https://user-images.githubusercontent.com/46675408/210471614-8f127cbc-065a-4cdd-ad8b-61b05b6e4dcb.png">

$h_i\in\mathbb{R}^d$: embedding of vertex $v_i$
$h_{ik}'$ : embedding of all edges connected to vertex $v_i$. For $k=1,...K_i$.

#### push apart loss
<img width="437" alt="image" src="https://user-images.githubusercontent.com/46675408/210471889-a4c482ce-68b1-4a52-ae66-d82fa8936ca4.png">

To allow different Nodes to have different embeddings, you can use the

### Result
<img width="956" alt="image" src="https://user-images.githubusercontent.com/46675408/210472235-b1ae0edc-0199-4b5a-ad2b-81ed16ee33f8.png">
