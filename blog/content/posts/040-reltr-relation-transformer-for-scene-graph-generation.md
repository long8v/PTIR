---
title: "[35] RelTR: Relation Transformer for Scene Graph Generation"
date: 2022-07-18
tags: ['2022Q1', 'SGG', 'graph', 'one-stage']
paper: "https://arxiv.org/pdf/2201.11460.pdf"
issue: 40
issueUrl: "https://github.com/long8v/PTIR/issues/40"
---
![image](https://user-images.githubusercontent.com/46675408/179435053-1d35238e-8403-45fa-89a2-91bd0984c301.png)

[paper](https://arxiv.org/pdf/2201.11460.pdf), [code](https://github.com/yrcong/RelTR)

## TL;DR
- **task :** Scene Graph Generation. task to pull out objects and relation between objects in the image.
- **problem :** I want to do one-stage SGG without object detector.
- **idea :** I want to get the query idea of DETR. Can't we just predict the set {S, P, O} instead of picking entities and predicting the triplet in the middle?
- **architecture :** Using object queries from DETR. Similarly, we create subject / object queries, pay attention to self-attention, pay attention to visual information, and pay attention to object queries (= entities in this paper) from DETR to get the final subject / object representation. Finding a relation with a heatmap.
- **objective :** Get triplet prediction `<{subject cls, subject bbox}, relation class, {object cls, object bbox}>` and get triplet loss by bipartite matching with GT. Combine this with the entity loss from DETR and calculate.
- **baseline :** two-stage SGG models, FCSGG
- **data :** Visual Genome, Open Image V6
- **result :** Better performance than FCSGG. Some models perform worse than those that use prior information, but performance is acceptable.
- **contribution :** one-stage SGG model with comparable performance! 

## Details
- SGG [first proposed] to retrieve images (https://openaccess.thecvf.com/content_cvpr_2015/papers/Johnson_Image_Retrieval_Using_2015_CVPR_paper.pdf
).
![image](https://user-images.githubusercontent.com/46675408/179462634-381f8751-df76-43bb-9766-edcff498ccd7.png)

- Like we used to do a lot with Object Detector and appending the prior information of objects. Very reasonable...
![image](https://user-images.githubusercontent.com/46675408/179463017-e0b9073f-56eb-488e-a911-0769511b0e50.png)

- graph based methodology
https://arxiv.org/pdf/1808.00191.pdf 📚 

- transformer based SGG
Context-aware scene graph generation with seq2seq transformers
Bgt-net: Bidirectional gruv transformer network for scene graph generation,

- The first one-stage SGG before this work was [FCSGG](https://arxiv.org/pdf/2004.06193.pdf) but with a performance gap. 📚.
- A similar dataset is Human Object Interaction (HOI).
### architecture
![image](https://user-images.githubusercontent.com/46675408/179478089-68ad00f1-011a-4f47-9555-cad94fe24b08.png)

Overall, there are three architectures
A) feature encoder extracting the visual feature context -> Z
B) entity decoder capturing visual feature context -> Q_e
C) triplet decoder with subject and object branches -> Q_s, Q_o, E_t
1) subject and object queries
Something like an object query in DETR. An embedding in d dimensions.
It has nothing to do with triplets at all. There is a separate thing called triplet encoding to represent triplets.

2) Coupled Self-Attention(CSA)
Add subject encoding and object encoding of the same size as triplet encoding. Then use the following operation to get the CSA.
![image](https://user-images.githubusercontent.com/46675408/179478861-53d91541-e10f-4703-b9d2-c419682d6791.png)

3) Decoupled Visual Attention(DVA)
Create a feature context Z that focuses on the visual feature. The word decouple is used here because it doesn't matter whether the object is a subject or an object. The following DVA operations occur on both the subject and object branches.
![image](https://user-images.githubusercontent.com/46675408/179479470-b991b330-8a29-47df-abb0-efbb67d5b3a2.png)

4) Decoupled Entity Attention(DEA)
It bridges the gap between entity detection and triplet detection. The reason for giving entities separately is that there are no constraints on SPO relationships, so we expect better localization.
![image](https://user-images.githubusercontent.com/46675408/179481192-011218e8-6528-4f1c-ad65-dcce914e75b9.png)

The output of the DEA is made into the final desired output via FFN.
The bbox regression predicts the center, width, and height via the FFN below.
![image](https://user-images.githubusercontent.com/46675408/179481675-cca2ebf9-5f41-488e-8732-3181cde33d8c.png)

The subject attention heatmap M_s and object attention heatmap M_o from the DVA layer are concatenated and turned into a spatial feature vector through the convolutional mask head below. -> Get the relation by looking at where the visual encoder looked at each S and O selection.
![image](https://user-images.githubusercontent.com/46675408/179484072-1a672ba7-503c-4efa-b7e5-aff00869abf9.png)

### Set Prediction Loss for Triplet Detection
Make a triplet prediction y_sub, c_prd, y_obj. where y_sub, y_obj are two bboxes and a class.
In this triplet, the matching cost is obtained by bipartite matching with the GT triplet (padded with `<background-no relation-background>`), and the matching cost is
Consists of 1) subject cost 2) object cost 3) predicate cost.
The subjet / object costs are composed of class loss and bbox loss,
class cost looks like this
![image](https://user-images.githubusercontent.com/46675408/179640143-324cbfd8-b855-4db5-a59a-875ea4d61357.png)
bbox cost is equal to
![image](https://user-images.githubusercontent.com/46675408/179640161-ed58d3f6-6517-41c8-b47e-c008b98b7f0d.png)
  - [Generalize IoU](https://arxiv.org/pdf/1902.09630.pdf)
![image](https://user-images.githubusercontent.com/46675408/179643182-89aa6c38-cf9c-49ef-9dda-e8b4b2aa44d7.png)

The triplet prediction cost is obtained by adding the class cost for the predicate to this.
These costs are then used to perform bipartite matching with the hungarian method, and LOSS is obtained.
After learning a few times, it spits out a meaningless triplet like the one below, so we added an additional IoU-based rule to prevent this.
![image](https://user-images.githubusercontent.com/46675408/179640424-d40249be-9b8d-4814-be0d-5f409188d611.png)

When sub / obj class is background and IoU btw. gt and pred are above threshold, don't add loss for subject or object.
![image](https://user-images.githubusercontent.com/46675408/179641129-2df53a44-6b1d-445b-85ff-ef77faf2c592.png)

- In proposal C, the blue box is better off not imposing a loss because it picked bbox well
- In proposal D, the blue and orange boxes are better off not imposing a loss because they picked bbox well

The final loss is calculated by combining the loss for the entity and the triplet loss, which probably came from the DETR.

### Dataset
- Visual Genome
  - 108k images, 150 entities, 50 predicates
  - Predicate classification(PredCLS) : given GT bbox and cls, predict predicates
  - Scene graph classification(SGCLS) : given GT bbox, predict predicates and object class
  - Scene graph detection : predict all!
  - Recall@k, mean RecallR@k 
- Open Image V6
  - 126k images, 288 entities, 30 predicates
- Recall@50, weight mean average precision, phrase detection ?? not sure what it says.

### Implementation Details
- 8 x 2080 Ti, bs=2, AdamW, weight decay 10-4, gradient clipping, Transformer LR 10-4, RestNet LR 10-5, lr dropping 0.1 by 100 epochs
- Using auxiliary loss
It's a loss applied by DETR, but you should read the [original](https://arxiv.org/pdf/1808.04444.pdf).
-> Stack the layers high and create a predictor that is shared by each layer, so that they each predict and sum their losses.
![image](https://user-images.githubusercontent.com/46675408/179665520-48b53343-69dc-48cd-a52a-c9832a2f1165.png)

- 6 layers encoder, 6 triplet decoder layer, 8 head attentions
- num of entities 100, num of queries 200
- IoU threshold 0.7
- When doing inference 2080 ti/eval, time is not included in the learning time.

### Results 
![image](https://user-images.githubusercontent.com/46675408/179643327-d24826ee-50d2-4d24-89e6-95f476ce9eba.png)


## Job thoughts/questions
- Relation can be small or large in nature, but we need to select only the relation that is annotated or that we are targeting.
- Who gets to be an S and who gets to be an O seems a bit arbitrary too. Eye above the nose. Nose under the eye. -> I can't help it.
- I'll have to look up some studies on self-attention graph learn.
- Is it okay to exclude objects without relation in SGG => only objects with relation are in the answer sheet?
- I need to actually see some of this Visual Genome data.
- What is the current metric based on -> Scene graph detection
