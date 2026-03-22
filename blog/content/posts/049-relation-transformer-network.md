---
title: "Relation Transformer Network"
date: 2022-08-01
tags: ['2020Q2', 'SGG', 'graph']
paper: "https://arxiv.org/pdf/2004.06193.pdf"
issue: 49
issueUrl: "https://github.com/long8v/PTIR/issues/49"
---
<img width="682" alt="image" src="https://user-images.githubusercontent.com/46675408/182097267-efbad1f2-3431-49f1-9d4e-f9249f9372cb.png">

[paper](https://arxiv.org/pdf/2004.06193.pdf)

## TL;DR
- **task :** Generate a Scene Graph given a bbox
- **PROBLEM :** I want to better model the relationship between pairs of objects.
- **idea :** It's helpful to learn the context between objects, and it's even better if all other objects are referenced when predicting a predicate, not just the object in question.
- **architecture :** Model the relationship between nodes as self-attention and the relationship between edges as cross-attention, following the transformer encoder-decoder example.
- Given a bbox, 1) extract visual features with Faster RCNN, 2) put it into the transformer encoder to extract self-attention output and predict the class in bbox, 3) put Edge Query into the transformer decoder to cross-attention with features from 1 and 2, and 4) burn FCN to predict subject, object, and relation.
- **objective :** cross entropy loss of subject, object, relation
- **baseline :** IMP, ... etc. two-stage models.
- **data :**  Visual Genome, CQA, VRD
- **result :** SOTA
- **contribution :** Hard use of the Transformer structure.
 
## Details
### why two-stage?
Unlike the one-stage we read about before, bbox goes to input!
That is, the difference between having a bbox in the final output or not.

### Architecture
<img width="666" alt="image" src="https://user-images.githubusercontent.com/46675408/182113783-89769ac1-46b1-4302-acdb-4e2ba0ada45b.png">

#### Problem Decomposition
- We can express the conditional probability of going from an image I to the scene graph G we want. (R is a relation, O is an object class, B is a bbox, I is an image)
$P(R|O,B,I)P(O|B,I)P(B|I)$
- Subtracting $P(B|I)$ where $P(B|I)$ is what object detection does
- To draw $P(O|B,I)$, we use the N2N module, which can learn context between objects.
- The $P(R|O,B,I)$ part is where the E2N module creates undirected edges to the entities and query, picks candidates, and the RPM gets the edge direction and relation type.
- Assumed a unique relation type between the two objects.

#### Object Detection
We'll use Faster RCNN on the VGG16 backbone.
Given a node $n_i$, extract the bbox coordinate, which is the spatial embodiment, and extract the feature map $I_{feature}$ from the top layer of VGG16 to extract the 4096-dimensional feature vector $v_i$.
For $o_i^{init}\in\mathbb{R}^C$ (where C is the # of classes), we initialized it using a GloVE embedding.

#### Encoder N2N Attention 
Learning the context of objects is not only helpful for object detection, but also for relation classification.
For this purpose, objects are put into a transformer encoder. The inputs are as follows v_i$ is the image feature vector $s_i$ is the GloVe vector for the class label from the object detection $b_i$ is the bounding box.
<img width="153" alt="image" src="https://user-images.githubusercontent.com/46675408/182112453-be6998be-cd4b-433a-a8cf-a4b470c85354.png">

Then we burn the network below, and in the last layer we do the categorization for that bbox.
<img width="224" alt="image" src="https://user-images.githubusercontent.com/46675408/182112464-71825dc6-8047-47f1-921b-15be1d08caaf.png">

Also, $f_i^{final}$ enters the decoder cross-attention.

#### Decoder Edge Positional Encoding
I want to put an edge query in the transformer decoder, but it's tricky to put a PE because there is no ordering over edges.
<img width="333" alt="image" src="https://user-images.githubusercontent.com/46675408/182115288-7278589e-f580-440d-9401-39730597e050.png">

So, if we do the above, we know what is subject and what is object. (?? Actually, the expression doesn't make sense)

#### Decoder E2N Attention
The $e_{ij}$ in Edge Queries and the collateral vectors above
<img width="172" alt="image" src="https://user-images.githubusercontent.com/46675408/182116604-3d13b040-70f6-4d3f-ba87-07f9f94aac13.png">

<img width="243" alt="image" src="https://user-images.githubusercontent.com/46675408/182116572-6b922922-faa1-4cf4-9640-6b3a525807d1.png">

Self-attention between edges didn't help performance, so we went straight to cross-attention.

#### Directed Relation Prediction Module(RPM)
relation is directional, so I took the rich embeddings from above and created a directional relational embedding like below.
<img width="545" alt="image" src="https://user-images.githubusercontent.com/46675408/182117015-64375cad-f035-4048-8be5-7dc4f087e1fe.png">

We then put the above embedding into a module called RPM (relation prediction module) to predict the final relation.

<img width="264" alt="image" src="https://user-images.githubusercontent.com/46675408/182117900-9f010692-7863-41fb-be13-7eb5dc5e6f3a.png">

LayerNorm -> Linear -> ReLU -> Linear(final relation categories) -> Take softmax

I also added a value for frequency.
<img width="468" alt="image" src="https://user-images.githubusercontent.com/46675408/182118011-fc72d855-857f-483b-b6ba-c9ae4600e4e2.png">

### Implementation Details
We used the top 64 object labels from NMS (IoU > 0.3) in the object detector and only considered node pairs with overlapping bounding boxes to reduce the computational cost of relation classification (huge inductive bias..)

### Result
#### Visual Genome
![image](https://user-images.githubusercontent.com/46675408/182268663-01f0840e-40af-49d6-b1be-d5274f8e0cd1.png)

#### Qualitative 
 
![image](https://user-images.githubusercontent.com/46675408/182268694-1e1f6ea3-0557-476d-b7fc-2a19eb1b46d3.png)

(b) is the N2N attention heatmap, which shows how much one object influenced another.
(c) is the E2N attention heatmap. How much did the objects affect the relation.

I often mistake on for of, but of is more natural, like `Face, of, Woman`. -> multi-predict is needed for this reason.

![image](https://user-images.githubusercontent.com/46675408/182270554-369e8f4d-f6c6-411f-80c3-09a13e050f49.png)

It was better to use our own decoder than to just use the transformer one (with self-attention).

![image](https://user-images.githubusercontent.com/46675408/182270212-8d2990f8-2605-47d1-b228-bf3b4a762690.png)

The performance drop when each feature was subtracted from the decoder was as follows. The frequency is a bit high.

The authors' explanation of each
![image](https://user-images.githubusercontent.com/46675408/182270446-a32a687c-35c9-4347-8046-0e817e3b9dfa.png)
