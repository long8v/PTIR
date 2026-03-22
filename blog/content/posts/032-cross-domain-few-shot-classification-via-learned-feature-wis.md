---
title: "[27] Cross-Domain Few-Shot Classification via Learned Feature-Wise Transformation"
date: 2022-05-23
tags: ['few-shot', '2020Q1', 'ICLR']
paper: "https://arxiv.org/pdf/2001.08735.pdf"
issue: 32
issueUrl: "https://github.com/long8v/PTIR/issues/32"
---
<img width="847" alt="image" src="https://user-images.githubusercontent.com/46675408/169812425-e2791252-5faa-4709-a7fe-cc71509fcb5f.png">


[paper](https://arxiv.org/pdf/2001.08735.pdf), [code](https://github.com/hytseng0509/CrossDomainFewShot)

## TL;DR 
**problem :** Few-shot classification works well in the same domain (= predicting unseen labels within ImageNet), but not well when doing few-shot with different domains (trained with ImageNet does not work well when doing few-shot test with CUB data).
**solution :** Added a feature-wise transformation layer (affine transformation) to the feature encoder, where the hyperparameters are learned using the learning-to-learn methodology.
**result :** Good generalization performance when applying the above feature-wise transformation to MatchingNet, RelationNet, and Graph Neural Network.

## details 
- The difference between domain adaptation / generalization is that for generalization, you need to generalize without using an unseen domain in the learning phase.
- We turn the domain generalization problem into a problem of classifying novel classes in a few-shot setting.

### 3.1. Preliminaries
- few-shot terms
  - N_w : # of categories
  - N_s : # of labeled examples for each categories
- The figure below shows an example of a 3 way 3 shot few shot
<img width="813" alt="image" src="https://user-images.githubusercontent.com/46675408/169812728-1c1dc722-3752-48da-9607-1f66aa0ca7b1.png">

- The algorithm of metric-based consists of a feature encoder E and a metric function M.
- At each iteration, N_w categories are drawn and a task T is created. Let X be the input image and Y the corresponding label. Task T consists of a support set S={(X_s, T_s)} and a query set {(X_q, Y_q)}.
- The feature encoder E extracts features from the support and query images and feeds them into the metric function M to predict the category of the query image based on the label of the support image.
<img width="326" alt="image" src="https://user-images.githubusercontent.com/46675408/169816949-89019fb0-b3af-4ba5-bc43-fb24b3ab5152.png">

- The learning objective function is the classification loss of the images for the query set.
<img width="251" alt="image" src="https://user-images.githubusercontent.com/46675408/169816998-b546aedb-6ff3-46ae-926a-34608093d151.png">

- The main difference between the various metric-based algorithms is the architecture of E from which the image features are drawn. For example, MatchingNet uses LSTM, RelationNet uses CNN, GNN uses GCN, etc.
- We trained with seen domains and evaluated against unseen domains.

### 3.2. feature-wise transformation layer
<img width="251" alt="image" src="https://user-images.githubusercontent.com/46675408/169821093-45bd57ed-8478-48f3-805d-369e391578ab.png">


- Our goal is to get better generalization over unseen data, which we need to prevent since the metric function M is prone to overfitting the seen domain.
- Intuitively, it seems that applying an affine transformation to the feature encoder E would allow us to represent more diverse distributions.
- hyper parameter means standard dev for sampling affine transformation parameters.
<img width="536" alt="image" src="https://user-images.githubusercontent.com/46675408/169819651-da38dd31-7527-4743-8f21-2ffba623de0b.png">

- After the batch norm, apply the feature-wise transformation layer below.
<img width="324" alt="image" src="https://user-images.githubusercontent.com/46675408/169819934-5fd871b7-12fe-47ba-a991-bf2a5224bb5b.png">

### 3.3 Learning the feature-wise transformation layers(=FT layer)
- We could choose the above hyperparameters empirically, but we want to make them learnable. We designed a learning-to-learn algorithm for this purpose. The main idea is to apply the FT layer so that what it learns on the seen domain performs better on the unseen domain.
<img width="831" alt="image" src="https://user-images.githubusercontent.com/46675408/170910374-2a36a16f-8e54-461d-9728-8b0c80dd2e21.png">

At each training iteration t, create a pseudo-seen domain (ps) and a pseudo-unseen domain (pu) by sampling from the seen domain. Apply the feature encoder and metric function with parameters for the FT layer and find the loss for the seen domain task only.
<img width="450" alt="image" src="https://user-images.githubusercontent.com/46675408/170921839-e16365e7-7359-4574-b078-142357c40f6b.png">

To measure generalization, we 1) remove the FT layer of the model and 2) calculate the classification loss of the updated model for the pseudo-unseen task. In other words,
<img width="605" alt="image" src="https://user-images.githubusercontent.com/46675408/170922450-6d65d6c9-4ef6-468b-b244-6d0db1910012.png">

Finally, since the loss above reflects the efficiency of the FT layer, we update the hyper parameter as follows
<img width="294" alt="image" src="https://user-images.githubusercontent.com/46675408/170922563-608e0e1a-5fcc-4ef0-b85e-1df3da9cc456.png">

In other words, the metric-based model and the feature-wise transformation layer (FT) are trained together in the training phase.

## Experimental Results
- FT: As a rule of thumb, when setting up an FT layer with even hyperparameters, you should use
<img width="1080" alt="image" src="https://user-images.githubusercontent.com/46675408/171078324-a96382aa-1e30-4448-afff-0b3295e38d9a.png">

- LFT: When the hyperparameters of the FT layer are learnable,
<img width="636" alt="image" src="https://user-images.githubusercontent.com/46675408/171078350-8228ce11-c3f5-4cde-adfa-da052a1d8d24.png">

- tSNE results by domain. Domains are well mixed -> cross-domain adaptation is good.
<img width="651" alt="image" src="https://user-images.githubusercontent.com/46675408/171078811-8db8f500-c099-456f-b2be-222492a377b0.png">
