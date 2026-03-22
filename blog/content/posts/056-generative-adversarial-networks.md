---
title: "[50] Generative Adversarial Networks"
date: 2022-08-13
tags: ['fundamental', 'generative', 're-read', '2014']
paper: "https://arxiv.org/abs/1406.2661"
issue: 56
issueUrl: "https://github.com/long8v/PTIR/issues/56"
---
![image](https://user-images.githubusercontent.com/46675408/184517292-daf88e97-b4ff-49c7-a01b-d92faa5d5635.png)

[paper](https://arxiv.org/abs/1406.2661)

## TL;DR
- **task :** generative model
- Problem :** Compared to discriminative models, generative has limited performance because it is difficult to approximate intractable probabilities with maximum likelihood via a back-prop.
- Idea :** Introduce a discriminator to learn adversarially.
- **architecture :** generator neither MLP discriminator neither MLP
- **objective :** Train the discriminator to be good at discriminating between generated and real data, while the generator creates data that the discriminator is not good at discriminating.
- **baseline :** restricted Boltzmann machines(RBM), deep Boltzmann Machines(DBM), deep Belief network(DBN)
- **data :** mnist, Toronto Face Database, CIFAR10
- **result :** Paren window-based log-likelihood estimates based on SOTA
- **contribution :** Unlike RBM, it does not use markov chains, but only gradients to learn.
- **Limitations or things I don't understand:** 4.2. Convergence of Algorithm 1 doesn't make sense to me

## Details
[notion](https://long8v.notion.site/GAN-0f05e9a5f3ca4435b27b6405073538c2)
