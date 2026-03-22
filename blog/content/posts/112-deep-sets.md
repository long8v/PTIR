---
title: "[103] Deep Sets"
date: 2023-03-20
tags: ['NeurIPS', '2017']
paper: "https://arxiv.org/pdf/1703.06114.pdf"
issue: 112
issueUrl: "https://github.com/long8v/PTIR/issues/112"
summary: "I often see it mentioned in other papers such as https://github.com/long8v/PTIR/issues/82. Two-word title Ganji - theoretical characterization of set input output, checking its performance in various applications"
---
<img width="661" alt="image" src="https://user-images.githubusercontent.com/46675408/226218804-5a30ac66-5794-4a12-b862-6d9aae85dbef.png">

[paper](https://arxiv.org/pdf/1703.06114.pdf)

## TL;DR
- **I read this because.. :** https://github.com/long8v/PTIR/issues/82 I often see it mentioned in other articles like this one. Two-word headings
- **task :** Tasks whose input or output is an unordered set. 1) estimate the distribution parameter of a parameter 2) list and sum numbers 3) point cloud classification 4) find words close to a concept / cluster of a set of words 5) find all tags related to an image
- **problem :** What are the characteristics that a deep network that solves permutation invariant tasks should have?
- **architecture :** $f(x)=\sigma(\lambda I \mathbf{x} + \gamma \text{maxpool}(\mathbf{x})1)$
- **Result :** Similar or better performance than models characterized by one arch each
- **Contribution :** Theoretical characterization of set input output, verifying its performance in various applications.
- **limitation / things I cannot understand :** 

## Details
### Permutation Invariance and Equivarnce
**Problem Definition**

The function f must be permutation invariant regardless of the order of the set.

<img width="279" alt="image" src="https://user-images.githubusercontent.com/46675408/226219598-2bc457f8-655e-4c9d-9c8e-820c07b0eb99.png">

- $\pi$ : permutation

**Structure**

A function f(X) that takes a set $X$ is pemutation invariant when it decomposes into the following form
<img width="105" alt="image" src="https://user-images.githubusercontent.com/46675408/226221330-995fb348-634a-48c3-b5ef-50576852ea70.png">

For any function $f_\theta : \mathbb{R}^M \rightarrow \mathbb{R}^M$,
- $\sigma$ : nonlinearity function
- $\theta \in \mathbb{R}^{M\times M}$
If $f_\theta(\mathbf{x})=\sigma(\theta\mathbf{x})$, the diagonal elements of $\theta$ are equal and the non-diagonal elements are tied, then the permutation is equivalent.
<img width="597" alt="image" src="https://user-images.githubusercontent.com/46675408/226221400-0674052a-a274-4884-9535-a6ec40b5da9c.png">

I looked at the formula, and it looks like it's just the same value except for diagonal, and the same value between diagnoal.
lambda * torch.eyes(5) + gamma * torch.ones(5,5)

If you put $\mathbf{x}$ up to
$f(x)=\lambda Ix \mathbf{(11^T)x})$
The summation of inputs Ix and x plus nonlinearity is permutation invariant (since the summation is independent of the permutation)

### Deep Sets
We can replace the above properties with a universal approximator, i.e., we can approximate $\phi$ and $\rho$ by polynomials
That is, 1) each instance $x_m$ is replaced by some representation $\phi(x_m)$ and 2) the representations are processed according to the $\rho$ network and then added.
Given some meta-information $z$, the above networks are represented by a conditional mapping $\phi(x_m|z)$.

**Equivariant model**
<img width="125" alt="image" src="https://user-images.githubusercontent.com/46675408/226222009-7e3e7ba0-5e68-467a-8cc2-4659ee0bb339.png">


If we replace this with another operation, we can get something like this

<img width="237" alt="image" src="https://user-images.githubusercontent.com/46675408/226221930-4e3a1b7d-dbdd-4be5-8883-7a40bea5c1c5.png">

This is because max-pool has a commutative law similar to sum. In practice, we found that Max performed better than sum.

### Applications and Empirical Results
- Show Normally Distributed Random Numbers and Estimate Parametric Statistics
<img width="749" alt="image" src="https://user-images.githubusercontent.com/46675408/226503764-0aca5e4d-bf48-4b1f-a022-31783e8c8da7.png">

- Show a list of numbers and ask for their summation
text / mnist image
<img width="373" alt="image" src="https://user-images.githubusercontent.com/46675408/226503814-0fb31e45-c747-4af2-8f21-a338b07c7ffe.png">

Shows up to 10 when learning and 100 when testing
Deep sets generalize well, unlike RNNs

- point cloud classification
<img width="379" alt="image" src="https://user-images.githubusercontent.com/46675408/226503995-fd502f23-216e-463c-9aac-80142b99e874.png">

The points measured by LiDAR are in no particular order.

- text set expansion
Given a cheetah, a tiger, a task to draw a puma with a similar concept. unsupervised
<img width="744" alt="image" src="https://user-images.githubusercontent.com/46675408/226504270-af1e67a9-bba1-4ae9-9fbd-30a0c34d95f2.png">

- image tagging
Tagging all of the text that corresponds to a specific image
For training, we gave them a few tags and asked them to predict the rest of the tags, and for testing, we gave them only images and asked them to predict the tags.
One network to encode each element (image and tag), and one network to sum the elements to get the score of the set.
-> Does it then score all the combinations of the set and pick the best? I don't know
<img width="304" alt="image" src="https://user-images.githubusercontent.com/46675408/226504360-4fbbfd79-24ab-4818-a221-e54191d8ce19.png">

- anomaly detection
I have a CelebA with images and tags corresponding to those images, and I want to organize the images by tag and pull one image from a different group.
Take a sequence of images and try to predict which one is the wrong image in the last softmax layer.
With Deep sets, I got 70% of the tests right, while the baseline with FCN performed at random guess level.
<img width="755" alt="image" src="https://user-images.githubusercontent.com/46675408/226504493-cf2812fc-f630-418a-9bbd-55ef1a2b8198.png">


- A follow-up study?
http://proceedings.mlr.press/v97/lee19d/lee19d.pdf
With attention operations instead of pooling!

