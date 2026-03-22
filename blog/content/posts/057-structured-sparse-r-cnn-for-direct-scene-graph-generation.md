---
title: "[51] Structured Sparse R-CNN for Direct Scene Graph Generation"
date: 2022-08-19
tags: ['2020Q2', 'CVPR', 'SGG', 'one-stage']
paper: "https://openaccess.thecvf.com/content/CVPR2022/papers/Teng_Structured_Sparse_R-CNN_for_Direct_Scene_Graph_Generation_CVPR_2022_paper.pdf"
issue: 57
issueUrl: "https://github.com/long8v/PTIR/issues/57"
---
![image](https://user-images.githubusercontent.com/46675408/185518290-086a79a5-3bfe-44ac-99af-4c26c7331792.png)

[paper](https://openaccess.thecvf.com/content/CVPR2022/papers/Teng_Structured_Sparse_R-CNN_for_Direct_Scene_Graph_Generation_CVPR_2022_paper.pdf), [code](https://github.com/MCG-NJU/Structured-Sparse-RCNN)

## TL;DR
- **task :** one-stage Scene Graph Generation
- **problem :** When solving SGG, I want to make a set prediction at once with an integrated model consisting of object detection, relation graph construction, and relation prediction.
- **idea :** Have triplet queries like [sparse R-CNN](https://openaccess.thecvf.com/content/CVPR2021/papers/Sun_Sparse_R-CNN_End-to-End_Object_Detection_With_Learnable_Proposals_CVPR_2021_paper.pdf) with region proposal query, inject a prior for object pair and relation into it, and then have a triplet detector called triplet detector that predicts OD and relation in parallel.
- **architecture :** CNN with FPN as backbone. The triplet query consists of bbox, obj vec, and rel vec. The box is ROI aligned to extract features, and the rest of the features are extracted through MHSA, and then the features for bbox and obj vec are OD, and the features for rel vec are fused with the above features to predict relation.
- **objective :** bbox loss, CE loss for relation and object cls
- **baseline :** IMP, G-RCNN, MOTIF, transformer, vctree ... 
- **data :** Visual Genome, Open Image
- **result :** SOTA. 
- **contribution :** Looks like a two-stage SGG, but is it one-stage? If it's one-stage, it performs very well.
- **limitation or something I don't understand :** When I do a parameter share with siamese sparse R-CNN... is this like distilation? 🤔?
The question of whether we could have matched GT objects in one model and lost object detection is not resolved... or could we have combined unrelated object pairs to create a triplet?!

## Details
## Sparse R-CNN
https://github.com/long8v/PTIR/issues/58

## Architecture
![image](https://user-images.githubusercontent.com/46675408/185559317-8f24db68-b640-4ae0-b6ef-548479088d3e.png)

### Triplet query
- Express the general distribution of tiplets like queries in a sparse RCNN
- 2 proposal boxes coordinates : 4d
- 2 object content vectors (representing appearance, acting like proposal features in a sparse RCNN) : 1024, 256
- one relation content vector(structure information between objects) : 1024, 256

### Triplet detection head
- Object pair detection
I'm doing MSA with object vectors, but I want to do it better by applying pair fusion module

![image](https://user-images.githubusercontent.com/46675408/206087486-83a5a82d-8043-47f4-8f73-694144b41b0f.png)

![image](https://user-images.githubusercontent.com/46675408/206087273-b0aa22fc-b5e6-40d3-993b-609d9da9fba7.png)

Using $X_s'$, $X_o'$ as query, key. value will be the two object vectors themselves, just as
Here, the enhanced object feature is used for Dynamic Conv.

![image](https://user-images.githubusercontent.com/46675408/206087371-654c3ff7-a560-4580-80ff-155f38e090d9.png)


### Relation recognition
![image](https://user-images.githubusercontent.com/46675408/206087581-e2cabdc6-b964-4f2f-9098-a4c3abd51365.png)

The relation was also taken from the largest region of the bbox and fused with E2R on top of DyConv+.
![image](https://user-images.githubusercontent.com/46675408/206088079-472538bb-6fe5-4fc0-b6eb-5574e22a3100.png)


### Learning with Siamese Sparse R-CNN
The objects are too sparse to learn with ground-truth triplets alone.
Siamese Sparse R-CNN with parameters shared with structured sparse R-CNN as object detector and virtual object pairs as pseudo-labels for knowledge distillation.

![image](https://user-images.githubusercontent.com/46675408/185559605-a296cf91-0e7f-45e4-982c-8ec7c9219973.png)

### two-stage triplet label assignment
1) Matching ground-truth triplets with predicted triplets
![image](https://user-images.githubusercontent.com/46675408/187102457-d2729d11-c1ac-40c2-abb2-a99256ed1344.png)

2) For triplets not matched by gt, match them with object pairs spit out by siamese sparse R-CNN
For the remaining triplets, leave the box as is and replace only the object classification score with label.
impose hungarian on the pseudo-label spouted by siamese sparse R-CNN and the object of the rest of the triplet with the following matching cost
![image](https://user-images.githubusercontent.com/46675408/187102624-1c320354-ce50-4c1e-9788-2de17874026e.png)

And padding with `background` for relation, then calculating loss
![image](https://user-images.githubusercontent.com/46675408/187102714-4787fd67-9136-401d-818c-97a34990288d.png)

### Imbalance Class Distribution
- Adaptive focusing parameter
Reduce weight for classes that are too major in object classification.
![image](https://user-images.githubusercontent.com/46675408/187106218-b8a180c6-f095-4212-b698-70ef5315f055.png)

- logit adjustment
![image](https://user-images.githubusercontent.com/46675408/187106185-7091cca5-6fe4-4ace-bc2e-5c42ce9c239e.png)


### Results
<img width="685" alt="image" src="https://user-images.githubusercontent.com/46675408/186424240-689b836a-1830-4788-8b39-3432b2dcbbcb.png">
