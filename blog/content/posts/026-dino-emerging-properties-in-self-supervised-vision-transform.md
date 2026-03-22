---
title: "[24] DINO: Emerging Properties in Self-Supervised Vision Transformers"
date: 2022-04-26
tags: ['ViT', 'SSL', '2021Q2', 'facebook']
paper: "https://arxiv.org/pdf/2104.14294.pdf"
issue: 26
issueUrl: "https://github.com/long8v/PTIR/issues/26"
---
<img width="788" alt="image" src="https://user-images.githubusercontent.com/46675408/165205620-c23a58ca-a094-4012-84e2-cf98cff09faf.png">

[paper](https://arxiv.org/pdf/2104.14294.pdf) [code](https://github.com/facebookresearch/dino)

## Abstract 
Wouldn't there be different characteristics of using SSL over ViT as opposed to convnet?
1) Unlike supervised and convnet, self-supervised ViT features have explicit information about the semantic segmentation of the image.
<img width="1022" alt="image" src="https://user-images.githubusercontent.com/46675408/165208051-5b500bd3-2c0d-4727-9275-f42e306dfad6.png">

2) These features are excellent features for kNN classification, achieving an accuracy of ImageNet top-1 78.3% even on small ViTs.


We also revealed the importance of using 1) momentum encoder* 2) multi-crop training 3) small patches with ViT, and based on these findings, we propose DINO (self-distillation with no labels). In a linear evaluation of DINO + ViT, we achieved an accuracy of ImageNet top-1 80.1%.
*MoCo : Momentum contrast for unsupervised visual representation learning. It just means that the teacher network is updated.


## Introduction
ViT performed comparably to convnet, but its advantages were not clear: It required more computation, required more training data, and ViT's features did not have specialized properties. In this paper, we want to show that Transformer's success in vision lies not in supervised learning, but in self-supervised learning, like NLP.
In vision, SSL methods usually have a similar structure, but with slightly different elements to avoid trivial solutions (=collapse) or to increase performance. We want to apply these studies to ViT features.
<img width="373" alt="image" src="https://user-images.githubusercontent.com/46675408/165209334-21883bd0-8513-450e-938c-8f0f2e7abdc9.png">


After applying it, we found the properties described in the abstract and propose DINO based on them. DINO is a network with a momentum encoder that directly predicts the output of the teacher network and is trained with generalized cross-entropy. DINO generally works well by just centering/sharpening the teacher output, which is very simple and flexible, unlike other networks that use predictors, advanced norms, and contrastive losses.
I've experimented with combining DINO with small patch ViT, and I've experimented with different combinations depending on how much GPU resources I have.

## Approach
### SSL with Knowledge Distillation 
<img width="555" alt="image" src="https://user-images.githubusercontent.com/46675408/165217019-2afa8065-b9c1-4476-9610-46d07249c2ae.png">

DINO follows the overall structure of modern SSL and has some similarities to knowledge distillation (KD).
KD is a method in which, given the output of a teach network, the output of a student network is trained to follow it. Given an input image x, the K-dimensional output probability, P_s, is normalized by softmax.
<img width="439" alt="image" src="https://user-images.githubusercontent.com/46675408/165211594-19e42968-0766-4cd3-a912-8757952317d7.png">

The temperature parameter, \tau_s, determines the sharpness of the output distribution. Given a teacher network, we are trained to minimize cross entropy over the student network.
<img width="488" alt="image" src="https://user-images.githubusercontent.com/46675408/165212527-c4a76837-c327-4f66-b1f3-2173f5ba7f49.png">

We will show the process of transferring this loss to SSL. First, we use a multi-crop approach to create a set of V different images in the form of distorted views or crops. This image set has two global views (full images) and many low-dimensional local view images. The cropped images are trained on the student network, and the global views are passed through the teacher to achieve a "local-to-global" correspondence, i.e., our loss is rewritten,
<img width="477" alt="image" src="https://user-images.githubusercontent.com/46675408/165213145-5dc46003-e4ba-4f9e-8d52-c46a355e8b50.png">

The number of Vs in this case can be any number, even two. We defined a global view of size 224 x 224 and a local view of size 96 x 96, which covers more than 50% of the image. The two networks have the same structure but different parameters, and only the parameters of the student network are trained with SGD.

### Teacher Network 
Unlike KD, we don't have a teacher because we don't have private knowledge. Therefore, we learn from the past student network. We experimented with different ways to update the teacher network and found that freezing it for an epoch performed surprisingly well. We used an exponential moving average (EMA). (like #25 )
<img width="200" alt="image" src="https://user-images.githubusercontent.com/46675408/165214132-03a1a7fa-807d-44c5-a6e7-f6f48a26bff4.png">

In this case, \lambda was scheduled to cosine from 0.996 up to 1. This EMA methodology had the effect of ensembling like Polyak-Ruppert Averaging(?).

### Network architecture
NN g consists of a backbone f (ViT or ResNet) and a projection head h. The features used in the downstream task are the outputs of the backbone f. h is a 3-layer MLP with hid_dim of 2048 and l2 norm (called SwAV-like structure). h is a 3-layer MLP with hid_dim of 2048 and l2 norm (called SwAV-like structure). ViT does not use batch norm anywhere.

### Avoiding collapse.
SSL methodologies take different approaches to avoid collapse. DINO can also be stabilized with norms, but centering + sharpening the momentum of teacher output was enough to prevent model collapse. Centering prevents one dimension from dominating and encourages collapse to a uniform distribution, while sharpening does the opposite. Together, the two operations provide a balance that prevents collapse.
<img width="174" alt="image" src="https://user-images.githubusercontent.com/46675408/165216641-48b1ebb1-d0ff-4938-adc0-2b98c3b30ec1.png">
centering can be interpreted as adding a bias term c to teacher. The center c is learned together with the EMA.

<img width="387" alt="image" src="https://user-images.githubusercontent.com/46675408/165216708-318b0c44-d940-4312-bd6b-c5baa7a0b6d6.png">

## Result
### Main Result 
<img width="441" alt="image" src="https://user-images.githubusercontent.com/46675408/165216986-23c05bc9-41ba-45b0-9fbb-9565cf54437c.png">

- BYOL, MoCov2, SwAV wins.
- When applying ViT to DINO, the results are almost as good as linear probing or KNN alone (74.5 vs 77.0), which is not seen in DINO + Convnet, which is a characteristic of the ViT architecture.
- We found that a patch size of 8 performed better than a patch size of 16.

### Properties of ViT trained with SSL
We evaluated the properties of DINO features for nearest neighbor search, information about object location, and transferability to other downstream tasks.
- image retrieval 
task to retrieve an image given query, image
<img width="540" alt="image" src="https://user-images.githubusercontent.com/46675408/165217962-9a9b2fce-b46d-4551-9292-2377af9c6110.png">

- copy detection  
A task to recognize images that have been crushed by blur, insertion, print and scan.
<img width="543" alt="image" src="https://user-images.githubusercontent.com/46675408/165217986-cf728db3-2ecd-4d05-b68a-389392b28c5f.png">

- segmentation
<img width="466" alt="image" src="https://user-images.githubusercontent.com/46675408/165218514-9bf03ac5-896d-401f-85aa-347da6435031.png">

For the model trained with DINO for each ViT/s, we visualize the self-attention of `[cls]` tokens of each head in the last layer, and we have the segmentation information as shown below.
<img width="461" alt="image" src="https://user-images.githubusercontent.com/46675408/165218490-52a5c7b5-d321-4f17-944d-ffcb78968dec.png">
 
DINO performs better segmentation than the one trained with supervised ViT. Below is the top 60% of the self attention map
<img width="561" alt="image" src="https://user-images.githubusercontent.com/46675408/165218277-63ad721d-2e6b-46cd-8194-54fcdece26b8.png">

- transfer learning 
<img width="525" alt="image" src="https://user-images.githubusercontent.com/46675408/165218241-2d7630a9-96b2-477a-af1d-fb0252cc2abe.png">

## Ablation 
### Importance of components
<img width="454" alt="image" src="https://user-images.githubusercontent.com/46675408/165219492-d4598c8a-b8ca-451e-a45c-968f5f5a4cc2.png">


### Effect of patch size
<img width="452" alt="image" src="https://user-images.githubusercontent.com/46675408/165219463-c3dfb085-8daa-4386-b513-2bc16502d044.png">

As the patch size gets smaller, the parameters stay the same, but the throughput increases. The smaller the patch size, the better the performance.

### Analyzing training dynamic
<img width="436" alt="image" src="https://user-images.githubusercontent.com/46675408/165219434-47c15262-57a2-4a1d-8093-c39c72993efc.png">

### Avoiding Collapse
<img width="426" alt="image" src="https://user-images.githubusercontent.com/46675408/165219184-2834b4c7-da14-4fa7-b3dd-95ed06264abc.png">

Cross Entropy is divided into two terms, KL divergence and entropy, and plotted. Without either sharpening or centering, the KL divergence goes to zero, which means that the output is always constant, so collapse occurs,
On the other hand, entropy converges to zero for sharpening alone and to -log(1/K) for centering alone, which means that they collapse in different directions, which means that the two operations must be balanced against each other.

<img width="418" alt="image" src="https://user-images.githubusercontent.com/46675408/165218923-15242e35-1325-4a98-855f-6fc4e3772928.png">

