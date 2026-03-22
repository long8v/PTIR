---
title: "Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts"
date: 2022-05-13
tags: ['2018', 'MoE', 'KDD']
paper: "https://dl.acm.org/doi/pdf/10.1145/3219819.3220007"
issue: 29
issueUrl: "https://github.com/long8v/PTIR/issues/29"
---
<img width="746" alt="image" src="https://user-images.githubusercontent.com/46675408/168198355-74e7785b-ff9b-46de-8fb1-a78f4c543b4f.png">

[paper](https://dl.acm.org/doi/pdf/10.1145/3219819.3220007)

**idea :** Let's create a multi-gate MoE (MMOE) that can model multi-tasks without having to explicitly specify the relation of each task.

<img width="918" alt="image" src="https://user-images.githubusercontent.com/46675408/168199403-bf8094b0-d3ab-4f40-8847-74053714b0b4.png">

In typical multi-task learning, we have a shared network (shared bottom) and build FCNs for each task on top of it. In this paper, we combine the idea of MoE and use each expert as a shared bottom. In the original MoE, there is a single gating network, but in MMoE, we create a gating network for each task k.

<img width="374" alt="image" src="https://user-images.githubusercontent.com/46675408/168199929-315f47c9-bc6a-492e-8cd6-0527d3b5aea2.png">

Each gating network is a classifier whose simple input_dim is a feature and output_dim is num_experts.

<img width="344" alt="image" src="https://user-images.githubusercontent.com/46675408/168200053-718f7429-9a97-4686-b51d-3c8b3b38c8d8.png">
 
The evaluation of the synthetic data is as follows The higher the task-specific correlation, the more likely it is that the

<img width="1294" alt="image" src="https://user-images.githubusercontent.com/46675408/168200419-bb392094-0c76-40c9-b6db-6cc5e154b142.png">

The evaluation of real data is as follows

<img width="350" alt="image" src="https://user-images.githubusercontent.com/46675408/168200663-d1df9130-d475-47f9-9c4a-96f7446341bf.png">

<img width="350" alt="image" src="https://user-images.githubusercontent.com/46675408/168200715-eadbe3ea-f237-4592-a397-e5223c98d82a.png">


One-line comment: Hmm...is there any way to give some initial values for correlation per classifier?

