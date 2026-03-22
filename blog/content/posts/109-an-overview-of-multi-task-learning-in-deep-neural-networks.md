---
title: "[100] An Overview of Multi-Task Learning in Deep Neural Networks"
date: 2023-01-26
tags: ['2017', 'survey', 'MTL']
paper: "https://arxiv.org/pdf/1706.05098.pdf"
issue: 109
issueUrl: "https://github.com/long8v/PTIR/issues/109"
summary: ""
---
![image](https://user-images.githubusercontent.com/46675408/214748723-8079957a-c9a2-455a-9b96-fe7b1a87f9ee.png)

[paper](https://arxiv.org/pdf/1706.05098.pdf)

## Details
### Multi-task Learning
Why does it work?
1) prevent overfitting for one task, 2) aggregate data, 3) learn "inductive bias", and 4) learn good features.

### hard parameter sharing vs soft parameter sharing
- hard parameter sharing 
![image](https://user-images.githubusercontent.com/46675408/214749097-c570c580-e4d9-404d-ae4a-c657bb4ee6d6.png)

Common MTL Model Structure

- soft parameter sharing 
![image](https://user-images.githubusercontent.com/46675408/214749186-203a400e-c08d-461c-a7b9-c76d24d0b9fb.png)

Stack networks for each task and impose an L2 norm loss so that the parameters of each network don't vary too much.

## Recent work on MTL for deep learning
- Deep Relationship Networks
Impose a matrix prior on FCNs to allow the model to learn the relationship between tasks
![image](https://user-images.githubusercontent.com/46675408/214749521-71a0e948-a0b6-400c-9294-49c2f7833d3d.png)

- Cross-stitch network
<img width="556" alt="image" src="https://user-images.githubusercontent.com/46675408/214749670-61fe869e-eee4-45df-9621-b888c7ea1411.png">

Have separate networks for each task, with the parameters of each network being a linear combination of trainable $\alpha$.

- Weighting losses with uncertainty 
<img width="812" alt="image" src="https://user-images.githubusercontent.com/46675408/214749829-f1d5ceff-6e8d-4584-9e66-0dfc3cff70af.png">

Measure the uncertainty of each task and add relative weight to the multi-task loss function -> You might also like to read this!

### Auxiliary tasks
- related task
Related tasks are better
- adversarial
Learning by doing the opposite of what you want, e.g., predicting the domain of the input in domain adaptation and reversing the gradient in an adversarial task? Ganin, 2015
- Hint
Use a slightly easier task. For example, learn a task that predicts the sentiment of a sentence by dividing it into positive/negative -> connectivity experiment Remind me!
- Representation learning
Making the representation good can be an auxiliary task, since it's all about making a good representation. For example, language modeling or autoencoders.

### Lesson learned
I feel like BERT is really destructive lol