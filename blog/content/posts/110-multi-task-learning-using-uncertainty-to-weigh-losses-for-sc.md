---
title: "Multi-Task Learning Using Uncertainty to Weigh Losses for Scene Geometry and Semantics"
date: 2023-01-31
tags: ['2017', 'uncertainty', 'MTL']
paper: "https://arxiv.org/pdf/1705.07115.pdf"
issue: 110
issueUrl: "https://github.com/long8v/PTIR/issues/110"
summary: "Multi-task learning with uncertainty! - This is the first time a model has ever been trained with 3 tasks."
---

![image](https://user-images.githubusercontent.com/46675408/215653791-b58ffbc0-85d6-4b18-941e-994821a91bf3.png)

[paper](https://arxiv.org/pdf/1705.07115.pdf)

## TL;DR
- **I read this because.. :** multi-task learning with uncertainty!
- **task :** semantic segmentation, instance segmentation, pixel-wise metric depth
- Problem :** The previous multitask approach is a weighted sum of losses, and performance is very sensitive to this weighting.
- Idea :** Assuming a Gaussian for output y and estimating according to MLE, we can get the weight relative to the noise of each task itself by $\sigma$, i.e., optimize the model weight $W$ and the task dependent $\sigma_{task}$ together.
- **architecture :** DeepLab V3 (ResNet101 -> Atrous Spatial Pyramid Pooling) + decoder for 3 tasks
- **objective :** CE(semantic segmentation), L1(instance segmentation, depth estimation)
- **baseline :** task specific model, weighted multi-task model
- **data :** CityScapes benchmark, depth image uses pseudo-label with model named SGM
- **evaluation :** IoU, Instance Mean Error, Inverse Depth Mean Error
- **result :** sota in crab segmentation, depth prediction where 3 tasks were trained. sota in instance segmentation where 2 tasks were trained. sota in depth prediction where 2 tasks were trained.
- **contribution :** This is the first time the model has been trained with 3 tasks.
- **limitation/things I can't understand :** Roughly speaking, I added a learnable weight and added a regularization term to make sure it doesn't jump around, but it's beautiful to look at because it's interpreted from the MLE perspective.

## Details
### motivation
<img width="846" alt="image" src="https://user-images.githubusercontent.com/46675408/215655493-2142014e-58e0-4cd1-b600-fa86a5321bc2.png">

Performance is choppy depending on multi-task loss weight

### Architecture 
<img width="1054" alt="image" src="https://user-images.githubusercontent.com/46675408/215655442-7f6f61e5-3faf-4b82-bc8f-f2a944e28382.png">

### Homoscedastic uncertainty as task-dependent uncertainty
- Epistemic uncertainty 
- Uncertainty due to model, uncertainty due to lack of training data
- Aleatroic uncertainty
- Uncertainty caused by the data, uncertainty about information that the data cannot represent.
    - Data-dependent, Hetroscedatic 
- Uncertainty determined by input data and model output
    - Task-dependent, Homoscedastic
- Uncertainty that does not depend on input data

I don't understand... Anyway, in this paper we will measure the last task-dependent uncertainty.

### Multi-task likelihoods 
Let the output of the neural network be $f^W(x)$. In a regression problem, we can assume that the output follows a Gaussian
<img width="257" alt="image" src="https://user-images.githubusercontent.com/46675408/215656416-377887fb-7340-4a6e-84ae-721638cf510d.png">

where $\sigma$ is the noise scalar

For classification problems, take softmax and turn it into a probability distribution
<img width="275" alt="image" src="https://user-images.githubusercontent.com/46675408/215656530-321eaa70-88b3-4db3-857b-6ed76b06a058.png">

For multiple-model output, this can be expressed by factorizing.
<img width="385" alt="image" src="https://user-images.githubusercontent.com/46675408/215656673-738cca2d-b5ea-4c36-a86f-69de95c05679.png">

According to maximum likelihood estimation, Log likelihood can be written as
<img width="361" alt="image" src="https://user-images.githubusercontent.com/46675408/215656721-42f2d8cf-34b4-45fd-bf2c-f612cad95376.png">

For the log likelihood of the model output following two gaussians, we can write
<img width="421" alt="image" src="https://user-images.githubusercontent.com/46675408/215656841-4eca4df1-6229-41eb-9b66-1658bbb68ac4.png">

This can now be viewed as a minimization problem for $\mathcal{L}(W, \sigma_1, \sigma_2)$
<img width="415" alt="image" src="https://user-images.githubusercontent.com/46675408/215657073-9c4987a1-d418-4f47-a98e-e0e42fb9d6fa.png">

In this case, $\sigma_1$, $\sigma_2$ will be the relative weights of losses 1 and 2 respectively, and the last term, $log\sigma_1\sigma_2$, will be the regularization term.

For the classification problem, let's extend this to softmax scaled by the scalar $\sigma$.
<img width="304" alt="image" src="https://user-images.githubusercontent.com/46675408/215657323-111469cb-108c-40b0-a991-8f4e378acb63.png">

The log likelihood would then look like this,
<img width="376" alt="image" src="https://user-images.githubusercontent.com/46675408/215657358-935f3fed-93cc-4028-bbf4-19722e72f407.png">

This again looks like learning the joint loss.
<img width="421" alt="image" src="https://user-images.githubusercontent.com/46675408/215657402-20df2c11-c00e-4c7f-b9d2-98b23951e4d2.png">

Again, $\sigma_1$, $\sigma_2$ can be seen as the relative weights of the model.

### Result
<img width="861" alt="image" src="https://user-images.githubusercontent.com/46675408/215657662-2d77eb5f-2412-4207-8e8b-f6e97df8e5f5.png">

<img width="863" alt="image" src="https://user-images.githubusercontent.com/46675408/215657679-715a60ec-ab07-4932-a971-de186588a2ea.png">

