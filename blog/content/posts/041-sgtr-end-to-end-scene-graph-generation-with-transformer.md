---
title: "SGTR: End-to-end Scene Graph Generation with Transformer"
date: 2022-07-19
tags: ['2022Q1', 'CVPR', 'SGG', 'graph', 'one-stage']
paper: "https://openaccess.thecvf.com/content/CVPR2022/papers/Li_SGTR_End-to-End_Scene_Graph_Generation_With_Transformer_CVPR_2022_paper.pdf"
issue: 41
issueUrl: "https://github.com/long8v/PTIR/issues/41"
---
![image](https://user-images.githubusercontent.com/46675408/179683280-c3249640-3773-400a-8fa7-e37eccf2dd14.png)

[paper](https://openaccess.thecvf.com/content/CVPR2022/papers/Li_SGTR_End-to-End_Scene_Graph_Generation_With_Transformer_CVPR_2022_paper.pdf), [code](https://github.com/Scarecrow0/SGTR)

## TL;DR
- **task :** one-stage SGG  
- **problem :** N entity proposal -> O(n**2) predicate proposal -> inefficient!
- **idea :** Let's solve the SGG problem as a bipartite graph. Let's represent entities and predicates as nodes and connect them with directed edges!
![image](https://user-images.githubusercontent.com/46675408/179701271-c5dd4052-589d-41f0-9cb1-9e9ab54d5f59.png)
- **architecture :** First, extract visual features with ResNet like DETR and create entity nodes with learnable query. For predicate node, we concatenate the embedding of visual feature and selected entity node to get attention. With these, we cross attention each of predicate/entity indicators with byproducts from above, and then fuse them on top of L-layer, stacking layers as the fusion progresses. For the final output, we recreate it as a bipartite graph and format it into the final output format.
- **objective :** loss for entity(=DETR loss) + loss for predicate. predicate creates a matching matrix and finds in hungarian, localization + categories of entities, localization of objects related to predicate + loss for categories in relation
- **baseline :**  FCSGG, ...
- **data :** Visual Genome, Open Image V6
- **result :** SOTA with more efficient inference
- **contribution :** tackle graph problem with transformer structure? subject / object not split and not O(n**2)? ah but structure is too complex...

## Details
### Architecture
![image](https://user-images.githubusercontent.com/46675408/179873763-283d44b4-fcc3-4439-ab53-564773b46a1b.png)

#### 1) Backbone and Entity Node Generator
Put the features that went through ResNet like DETR into the transformer. viusl feature Z comes out.
Like the DETR decoder, entities are put into a learnable query. Each comes in with a feature map Z, which contains the entity's bbox B and class scores P and
Outputs the associated feature representation H.
<img width="651" alt="image" src="https://user-images.githubusercontent.com/46675408/179874155-8eabe1d6-fe9d-474a-8edb-88388ad27564.png">

#### 2) Predicate Node Generator 
- predicate encoder 
Using a Transformer encoder to extract predicate-specific image features. The result is Z^p.
- predicate query initialization
If you just put a learnable query, you can't put a compositional property, so you need to concatenate the subject and object queries.
<img width="173" alt="image" src="https://user-images.githubusercontent.com/46675408/179874585-c382ac9d-b25b-470b-817f-fc03a185d1a7.png">

And when learning the representation for this query, it pays attention to the feature H and bbox B from 1 together.
<img width="583" alt="image" src="https://user-images.githubusercontent.com/46675408/179874695-836137fb-24f6-470f-98df-42f2e451053d.png">

<img width="638" alt="image" src="https://user-images.githubusercontent.com/46675408/179874879-3877c716-26c0-40ff-a3e1-9ac5e973db1d.png">

#### 3) Structural Predicate Node Generator 
Perform the final attention operation on the matrix received from above
a) predicate sub-decoder 
Extracting predicate expressions from image features
![image](https://user-images.githubusercontent.com/46675408/179881187-51a40e68-dc75-410a-9b72-125fc617b6db.png)

b) entity indicator sub-decoders
Pulling entity indicators for predicate queries
<img width="568" alt="image" src="https://user-images.githubusercontent.com/46675408/179875140-e8e4f91c-62c8-42d0-b783-75dd0600d780.png">

c) predicate indicator fusion 
To connect predicates and indicators so that they can reference each other up the layer.
![image](https://user-images.githubusercontent.com/46675408/179881224-2d10a22e-3883-4a01-a7ee-a23262477a0a.png)


The end result of this process is the output shown below.
<img width="578" alt="image" src="https://user-images.githubusercontent.com/46675408/179875264-8d3a8d36-c611-4a85-b2fa-8f91686aac38.png">

class categorization for the predicate and the bboxes of subject, object associated with the predicate + categories

### Bipartite Graph Assembling
Replace it with a bipartite graph consisting of N entities and N_r predicates. Create an adjacency matrix between entity nodes and predicate nodes, and then create a correspondence matrix.
![image](https://user-images.githubusercontent.com/46675408/179880794-af2711bb-2b16-4320-ac5f-9e0e222fc2bd.png)

As you can see in the figure, we have entity, subject (light green), and object (blue), and these distances are used to create a matching!
For example, for subject?
![image](https://user-images.githubusercontent.com/46675408/179881021-3c67577f-1757-4c30-b8e8-16e0246f514d.png)

Define the distance between entity and subject as below and select only the top K of the distance matrix.
![image](https://user-images.githubusercontent.com/46675408/179880981-1963820e-b3a9-4676-bcb2-1436aee65d47.png)


### Learning and Inference
![image](https://user-images.githubusercontent.com/46675408/179880930-5accd49e-c013-4ace-b7c0-51e3f4ee596d.png)

DETR entity generator loss.
Localization + classification loss for entity indicator,
localization for entities related to the predicate, classification loss for the predicate

### Results
![image](https://user-images.githubusercontent.com/46675408/179887018-ddfc6876-45b8-4237-b462-e6bda0efcd17.png)


## Random thoughts / questions
- I put the visual information and the object's location information in there, but shouldn't I have?