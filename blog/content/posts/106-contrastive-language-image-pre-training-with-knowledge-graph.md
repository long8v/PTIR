---
title: "Contrastive Language-Image Pre-Training with Knowledge Graph"
date: 2023-01-12
tags: ['multimodal', 'NeurIPS', 'graph', '2022Q4', 'CLIP']
paper: "https://arxiv.org/pdf/2210.08901.pdf"
issue: 106
issueUrl: "https://github.com/long8v/PTIR/issues/106"
summary: "NeurIPS 2023, graph - formulation for CLIP learning of triplet-shaped data."
---
<img width="877" alt="image" src="https://user-images.githubusercontent.com/46675408/211960424-46599d7f-f26e-4512-b607-8643ad8699c5.png">

[paper](https://arxiv.org/pdf/2210.08901.pdf)

## TL;DR
- **I read this because.. :** NeurIPS 2023, graph 
- **task :** multi-modal training -> image retrieval, VQA, Visual Entailment, Image Classification, GLUE
- Problem :** CLIP is too simple with only two labels, "match" and "not matched", which does not contain any semantic information between text and image.
- idea :** CLIP + knowlege graph. takes a {head, relation, tail} triplet as input, not a text-image pair. Head or Tail can be either image or text.
- **architecture :** Take the CLIP architecture, but without pooling, concat + Transformer Encoder stack to pull features
- **objective :** Remove relation or tail (or head) from a triplet and make a prediction. 1) When removing relation, it is just a classification problem (E2R loss) 2) When removing tail, the representation of tail, head, and relation should be close to the same triplet (E2E Loss) 3) GNN is attached so that the representation of tail is similar to the representation of transformer after GNN (E2G Loss) 4) KL divergence with CLIP teacher leads to KD (KD Loss)
- **baseline :** CLIP, UNITER, OSCAR, ViLT, ... and more
- **data :** VisualSem(WordNet + ImageNet), Visual Genome, ConceptNet, COCO Caption, CC3M
- **result :** SOTA. 
- **contribution :** formulate data in the form of a triplet so that it can be CLIP trained.

## Details
### Motivation
<img width="835" alt="image" src="https://user-images.githubusercontent.com/46675408/211961885-63b95840-cd79-4ce6-8641-af2dbf9cf52b.png">

### Dataset
<img width="839" alt="image" src="https://user-images.githubusercontent.com/46675408/211961950-28b1b1bf-d432-4c3e-9743-bdf34515ebfb.png">

Additionally, for image-text pairs, you can arbitrarily specify a relation, such as `is a image of`, `is a caption of`, to make it a triplet.

### Architecture
<img width="838" alt="image" src="https://user-images.githubusercontent.com/46675408/211961912-5c0d14a0-8c6f-4125-b54a-4a867b3369a0.png">

<img width="415" alt="image" src="https://user-images.githubusercontent.com/46675408/211962089-2f62a308-b9fb-4664-acdb-0da003e24fa6.png">

- f$ is a text or image encoder
<img width="486" alt="image" src="https://user-images.githubusercontent.com/46675408/211962067-af2d7b97-7aa2-4b11-9b7e-3995ce115ff0.png">

<img width="396" alt="image" src="https://user-images.githubusercontent.com/46675408/211962200-dda25450-f7a9-4323-8ace-d49503078d78.png">

<img width="464" alt="image" src="https://user-images.githubusercontent.com/46675408/211962243-1ec14f2e-5454-46c8-a01c-e4a93e65c834.png">

Just index the representation for the relation

### Loss
- Triplet based loss
Like mlm, we're going to cover up some of the triplet elements and ask you to guess
#### E2E loss
If the entity (head or tail) is masked, estimate the loss as below
<img width="549" alt="image" src="https://user-images.githubusercontent.com/46675408/211962354-e64ae389-a947-45b4-91d4-0dc1faf4d482.png">

Masking is just a 0 vector cat format
![image](https://user-images.githubusercontent.com/46675408/212609518-9bdb555c-0770-4504-937e-bcca388c3415.png)

To make the representation of a tail and the representation of a head, relation that is part of the same triplet as that tail, closer together.

#### E2R loss
Matching relation is just a matter of categorization
<img width="680" alt="image" src="https://user-images.githubusercontent.com/46675408/211962569-41599d64-bf6e-4c51-af6f-85286d268f29.png">

- Graph-based loss
To make the entity representation similar between the GNN and transformer passes, we'll use the
<img width="547" alt="image" src="https://user-images.githubusercontent.com/46675408/211962628-fb105f96-2db4-42a8-a2d0-d91d469cae88.png">

#### Continuous Learning
KL Divergence with Results from Pretrained CLIPs
<img width="319" alt="image" src="https://user-images.githubusercontent.com/46675408/211962751-d47d70be-029d-4818-88d8-487b73c965c4.png">

### Experiement setup
<img width="827" alt="image" src="https://user-images.githubusercontent.com/46675408/211962833-f1566f63-98ea-47ee-96d3-95ae32518d1f.png">

## Result
### Image Retrieval
<img width="817" alt="image" src="https://user-images.githubusercontent.com/46675408/211962882-2ffb9c79-e506-4801-8f59-7c9848a099a3.png">
 
### VQA, SNLI_VE
<img width="504" alt="image" src="https://user-images.githubusercontent.com/46675408/211962919-fa1fedc0-394a-4bd5-9d9c-2e50cfe4be46.png">

snli_ve is said to be this data.
<img width="932" alt="image" src="https://user-images.githubusercontent.com/46675408/211962957-d42401c7-429d-42a2-a392-22b04fd23d6a.png">
https://github.com/necla-ml/SNLI-VE

### GLUE
<img width="843" alt="image" src="https://user-images.githubusercontent.com/46675408/211963018-d63a2d3e-219a-4056-be22-d553e7fcf4df.png">

### Image Classification
<img width="258" alt="image" src="https://user-images.githubusercontent.com/46675408/211963030-cab368b5-aff9-44ea-bfbf-026dbbe02ea2.png">

### Ablation
![image](https://user-images.githubusercontent.com/46675408/212609593-486fbaf6-37a4-41b8-bb4b-af7dbd66e9f1.png)

- Better than CLIP + KG

### Did you solve the problem from motivation?
![image](https://user-images.githubusercontent.com/46675408/212616863-98e8f00a-b3ea-472d-a508-c146ae791738.png)

We reran the evaluation only for VQAs with properties like color in VQA, and it performed better.