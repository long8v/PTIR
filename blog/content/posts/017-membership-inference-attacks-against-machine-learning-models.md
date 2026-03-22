---
title: "Membership Inference Attacks Against Machine Learning Models"
date: 2022-03-28
tags: ['privacy', '2016']
paper: "https://arxiv.org/pdf/1610.05820.pdf"
issue: 17
issueUrl: "https://github.com/long8v/PTIR/issues/17"
---
<img width="1035" alt="image" src="https://user-images.githubusercontent.com/46675408/160326216-91b27882-77b0-47e8-bc22-787489ff5482.png">

[paper](https://arxiv.org/pdf/1610.05820.pdf)

- Membership Inference: An attack that determines whether or not the data is present in the model's training data. For example, in the case of medical data, the mere existence of certain data as training data can be a serious privacy breach.
- The assumptions of these attacks are 1) The model you are attacking is a multi-classification model 2) You can get input and output from ML as a Service. 3) You know part of the training dataset of the model you want to attack.
- The algorithm for the Membership Inference Attack is shown below.
<img width="481" alt="image" src="https://user-images.githubusercontent.com/46675408/160327410-fdbeb5a7-2e8b-4b72-b3e7-48808a748c26.png">

(1) Define shadow models that mimic the output of the real model (target model) (or the same if you know the architecture of the target model).
(2) Create non-overlapping subsets of the known training data and train each with shadow models.
(3) Train an attack model for the entire dataset, given the actual label values and the predictions of the shadow model as input, and classify whether the data sample in the shadow model was present (`"in"`, `"out"`).

<img width="634" alt="image" src="https://user-images.githubusercontent.com/46675408/160328455-1c8cdf1a-b74b-4976-bbb1-f0ad629b3182.png">

**results :**
High precision, recall on most data. membership attack works well even in black box environments (when you don't know the model and your prior assumptions about the dataset are wrong).
<img width="1119" alt="image" src="https://user-images.githubusercontent.com/46675408/160329715-41ec5751-8b65-4b39-ae84-d757457492dd.png">

Definitely different when confidence is member, non-member.
<img width="1079" alt="image" src="https://user-images.githubusercontent.com/46675408/160329245-a3b6abdb-176b-4f29-bbb3-788690e7e75d.png">



