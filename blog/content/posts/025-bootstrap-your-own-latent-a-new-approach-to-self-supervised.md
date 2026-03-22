---
title: "Bootstrap Your Own Latent: A New Approach to Self-Supervised Learning"
date: 2022-04-25
tags: ['SSL', '2020Q2', 'google', 'DeepMind']
paper: "https://arxiv.org/pdf/2006.07733.pdf"
issue: 25
issueUrl: "https://github.com/long8v/PTIR/issues/25"
---
<img width="1315" alt="image" src="https://user-images.githubusercontent.com/46675408/165007714-be3ba72c-c55f-46d2-99cf-5ca149c3517e.png">

[paper](https://arxiv.org/pdf/2006.07733.pdf), [code](https://github.com/deepmind/deepmind-research/tree/master/byol) 

## Introduction
Bootstrap* Your Own Latent (BYOL) is designed so that two networks, the online network and the target network, interact and learn from each other. The online network is trained to represent an image when it is aggregated and the target network is trained to represent the same image when it is aggregated differently. At the same time, we train the target network with the slow-moving average of the online network. Current SOTA models use negative pairs, but BYOL achieves a new SOTA without them.
> *bootstrap is not an ML term, but rather its own meaning: `to improve your situation or become more successful, without help from others or without advantages that others have`.

<img width="500" alt="image" src="https://user-images.githubusercontent.com/46675408/165009094-da1b237f-2879-4daf-9335-61346bb0520c.png">

- While previous work has used pseudo-labels, cluster indicators, or handful labels, our work bootstraps the representation directly.
- Our work is robust to image augmentation by not using negative pairs.
- Methodologies such as #9 were trained by predicting the same image as the image and the agglomerated image as the same image, which leads to representation collapse when the prediction problem is given in the representation space. To avoid this, we applied a methodology that predicts the difference between the same image and the other image, but it has the limitation that it requires a very large number of negative samples.
- To avoid collapse without negative samples, a simple solution is to make a fixed randomized network the target for our prediction. While this prevents collapse, the performance is low, but surprisingly, linear evaluation of a random initialized network has an accuracy of 1.4%, while predicting the output of a fixed random initialized network has an accuracy of 18.8%. This experiment was the motivation for BYOL.
- Given a representation (=target network), we can train a new online network to predict the target representation. From there, we can learn higher quality representations as we repeat this procedure, and set the next online network as the new target network to learn more. In practice, we bootstrap using the moving exponential average of the online network.

## BYOL 
<img width="879" alt="image" src="https://user-images.githubusercontent.com/46675408/165012396-ef00bab5-064a-4b98-89e0-55e12284a161.png">
 
- The online network consists of an encoder, a projector, and a predictor and has weight \theta.
- The target network has the same structure as online, but has a different weight, \psi, and serves to provide targets for the online network. In this case, the parameter \psi is the moving average of the online parameter \theta.

<img width="793" alt="image" src="https://user-images.githubusercontent.com/46675408/165014337-6a8913bc-2fb8-4c36-abe3-521db0705175.png">

Create \nu, \nu' aggregated over one image and burn each network. Then compare the output of online's last prediction with target's projection and MSE.
<img width="802" alt="image" src="https://user-images.githubusercontent.com/46675408/165014437-5da700e3-c2ea-4d46-a4ae-0805a109bded.png">

Then we reverse the \nu, \nu' aggregation back into the online network and find the loss. Then sum the losses and minimize only on \theta.
<img width="1028" alt="image" src="https://user-images.githubusercontent.com/46675408/165014961-53b8bc5f-0484-4bac-a0af-c2854aaed725.png">

## Implementation details
- Image Augmentation
Use the same augmentation set as #9. select 224 x 224 random horizontal flip with random patch ...
- Architecture
ResNet-50 for encoder, average pooling for representaion layer, MLP(4096 -> ReLU -> 256) for prediction layer. no batch norm.
- Optimization : LARS, cosine decay, ...

## Result
- linear evaluation in ImageNet
<img width="1012" alt="image" src="https://user-images.githubusercontent.com/46675408/165015701-fceebd10-8615-4393-a66e-ea470835a151.png">

- Finetuning(=Semi-supervised training) in ImageNet
<img width="1038" alt="image" src="https://user-images.githubusercontent.com/46675408/165015748-678b2a8b-7e21-48d1-899f-7a5927ebc51d.png">

- Transfer to other classification task
<img width="1073" alt="image" src="https://user-images.githubusercontent.com/46675408/165015814-1f3070e9-5ec7-4cf7-87ae-d3443fe2c3df.png">

- Transfer to other vision task
<img width="1055" alt="image" src="https://user-images.githubusercontent.com/46675408/165015891-55ef4c91-c591-4bfd-bb89-17547cb61c14.png">

## Ablation
<img width="981" alt="image" src="https://user-images.githubusercontent.com/46675408/165017025-34705ec0-ac1e-4516-9f40-7e2d0b0d7489.png">

Compared to simCLR, there was less of a performance drop as we reduced the batch_size and augmentation.

<img width="514" alt="image" src="https://user-images.githubusercontent.com/46675408/165017069-2b81d97e-ac95-4eb9-8938-78589078d74e.png">

It made sense to use a moving average.

<img width="468" alt="image" src="https://user-images.githubusercontent.com/46675408/165017130-2ed391bf-0fda-4b3c-ac3d-bf96a61351e3.png">

It made sense to have a target network.
