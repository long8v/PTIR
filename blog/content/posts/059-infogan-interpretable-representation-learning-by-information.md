---
title: "InfoGAN: Interpretable Representation Learning by Information Maximizing Generative Adversarial Nets"
date: 2022-08-20
tags: ['openAI', '2016', 'fundamental', 'generative']
paper: "https://arxiv.org/abs/1606.03657"
issue: 59
issueUrl: "https://github.com/long8v/PTIR/issues/59"
---
<img width="834" alt="image" src="https://user-images.githubusercontent.com/46675408/185729655-502f78c2-cd8e-4b1d-b6f7-ca84cfb26737.png">

[paper](https://arxiv.org/abs/1606.03657)

## TL;DR
- **task :** unsupervised learning 
- **problem :** I want to do representation learning in an unsupervised manner, where I want to disentangle important features (numbers, eye color). Generative models are often perfect for generating the model, but the representation is a mess.
- **idea :** Add to the loss such that the mutual information (=MI) of some structured latent variable $c$ and generator distribution $G(z, c)$ is high. MI has a lower bound like ELBO, where the posterior is approximated by a neural network.
- **architecture :** The generative model shares a DCGAN and a CNN, with one more FCN on top to give $Q(c|x)$.
- **objective :** GAN loss - mutual information loss
- **baseline :** vanilla GAN
- **data :** MNIST, DC-IGN, Street View House Number(SVHN), CelebA
- **result :** By changing the code, we see that the output is also interpretable. Simply letting GAN learn about c does not maximize mutual information as much as InfoGAN.
- **contribution :** GAN with interpretable latent vector! 
- **Limitations or things I don't understand :**
> 1. how can one index be related to one digit if it's randomized when putting in category c. For example, if 1 image comes in and c is 3 or 5, it restores it the same whether c is 3 or 5, and vice versa, if 1 comes in or 2 comes in and c is 5, is it possible because it's a generation that considers c anyway?

-> In other words, it does not reconstruct like VAE, but it learns while distinguishing whether a given image is fake or real. Therefore, if some latent code c is entered as 3, it seems to put mutual information so that a picture like 3 comes out.

> 2. You can decide how many categories and continuations go into c, but you can't decide what each one learns in the first place, right?? Why is it done as if you can?? It's not something you find out after the fact....

-> undecidable is right. As if the resultant interpretation is that the code is a good representation of the features we think we have.

## Details
### mutual information
<img width="384" alt="image" src="https://user-images.githubusercontent.com/46675408/185787557-74f38e2c-176f-4810-95a6-05a05d6e812a.png">

If X and Y are independent so that $P_{X,Y}(x,y)=P_X(x)P_Y(y)$,
<img width="410" alt="image" src="https://user-images.githubusercontent.com/46675408/185787349-d01a4bc2-f105-40f1-8a4c-33d06971e3fd.png">

When written as an expression for entropy
<img width="529" alt="image" src="https://user-images.githubusercontent.com/46675408/185787340-e72cb18d-a088-4750-b335-314a9006a4a9.png">


### Variatitonal Mutual Information Maximization
<img width="779" alt="image" src="https://user-images.githubusercontent.com/46675408/185787402-648ef165-f596-4f86-871d-3b0041e277b2.png">

Here is where we need to sample for posterior Q, but the lemma below shows that we don't even need to sample.

<img width="887" alt="image" src="https://user-images.githubusercontent.com/46675408/185787485-587b5579-552a-452a-85e6-743e4907643d.png">

Interpreted, finding the expected value of a function f(x, y) given x and y given x is equivalent to finding the expected value of f(x' y) given x and y given x, and f(x' y) given x' (x given y).

Our lower bound is defined as
<img width="606" alt="image" src="https://user-images.githubusercontent.com/46675408/185787503-05b27562-e5ed-4b2e-b7f1-845a85c5fdae.png">

The final loss is the GAN loss minus the mutual information lower bound (the higher the MI, the better).
<img width="518" alt="image" src="https://user-images.githubusercontent.com/46675408/185787518-4dde4981-eb61-4a18-ac40-58dfd21c1889.png">
