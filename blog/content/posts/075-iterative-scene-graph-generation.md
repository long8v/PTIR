---
title: "Iterative Scene Graph Generation"
date: 2022-10-05
tags: ['SGG', '2022Q3', 'one-stage']
paper: "https://arxiv.org/pdf/2207.13440.pdf"
issue: 75
issueUrl: "https://github.com/long8v/PTIR/issues/75"
summary: "Good performance with just a transformer structure!"
---
<img width="878" alt="image" src="https://user-images.githubusercontent.com/46675408/193985405-1200b030-1a90-4857-8e12-3c9831d6ec64.png">

[paper](https://arxiv.org/pdf/2207.13440.pdf)

## TL;DR
- **task :** one-stage scene graph generation
- **problem :** Factorization that picks an object and then picks a relation based on it is limited. Given a relation, we can do a better job of picking out subject and object.
- **idea :** 1) Model object conditionally given subject and predicate conditionally given subject, object 2) t layers output sub, obj, predicate respectively and this propagates to the next layer.
- **architecture :** CNN backbone + 3 transformer decoders ({s, p, o}). positional encoding creates a conditional PE where subject is the learned PE, object is the MHSA of subject's PE and object PE, and predicate is the MHSA of subject and object together. Each query for {s, p, o} is also MHSA'd by fetching the queries for {s, p, o} in the previous layer.
- **objective :** ce loss + bbox loss for subject / object / predicate + loss re-weighting for tail  
- **baseline :** MOTIF, HOTR, SGTR
- **data :** Visual Genome, Action Genome 
- **result :** SOTA. mR performance is very good.
- **contribution :** Good performance with just the transformer structure!
- **Limitation or something I don't understand:** Object detection was just snapped. So no Detr Decoder.

## Details
<img width="364" alt="image" src="https://user-images.githubusercontent.com/46675408/193985710-e268c0a9-bedc-4947-a4f2-2ab336a2700f.png">

### Architecture
<img width="831" alt="image" src="https://user-images.githubusercontent.com/46675408/193986462-84008f02-a96a-4a87-b57d-64272d2bed97.png">

#### Conditional Positional Encodings
<img width="448" alt="image" src="https://user-images.githubusercontent.com/46675408/193987286-72c20333-8514-40ed-b0fb-64b0c34afe90.png">

- $\tilde q^t_{x,i} =q^t_{x,i} +p^t_{x,i}$ ; x is one of {s, o, p}.

#### Conditional Queries
<img width="538" alt="image" src="https://user-images.githubusercontent.com/46675408/193987506-8ebaa180-6296-4f0c-ae94-58d2b9fde47a.png">

- $q^t_{x,i}$ is the feature representation of the i-th index of the t-th layer

### Result
<img width="563" alt="image" src="https://user-images.githubusercontent.com/46675408/193986669-ee0effab-dbcc-4723-98b9-86bc84e23f39.png">

harmonic Recall is the evaluation metric that they came up with, which is a combination of recall and mR.
AP didn't rate you! You're a man!

### bipartite matching
Padding the ground truth relation with no relation and finding the graph that minimizes the total joint matching cost. (Why? Hmm..)
<img width="357" alt="image" src="https://user-images.githubusercontent.com/46675408/193988653-2de765c9-bcf4-4cdd-a9f4-3e5547c67a48.png">

<img width="687" alt="image" src="https://user-images.githubusercontent.com/46675408/193988669-e68e2af6-ab48-45f6-8912-2ca4abe11c77.png">

Our loss!
<img width="618" alt="image" src="https://user-images.githubusercontent.com/46675408/193988723-e3bd1cf1-a834-42d1-a28c-ffdc7502bc95.png">


### Implementation Details
- ResNet-101
- 6 layers, feature size 256
- 300 queries
- bs = 12, lr=10e-4 gradually decaying
- Using NMS
- Each class has an NMS attached to it, and it's attached to a post-NMS bbox while checking for IoU overlap.
- 50 epochs. T4 Chapter 4.

### Ablation
#### number of queries
<img width="709" alt="image" src="https://user-images.githubusercontent.com/46675408/193988301-c58e58d2-e688-4669-9d0d-94bd5514b944.png">

Larger num_queries doesn't make a difference.

#### Effect of refinement
<img width="399" alt="image" src="https://user-images.githubusercontent.com/46675408/193988424-d4e0a476-a7fa-4b3f-9ac1-98cd0a5347d9.png">
