---
title: "Variance Networks: When Expectation Does Not Meet Your Expectations"
date: 2022-11-25
tags: ['2018', 'ICLR', 'uncertainty', 'later..', 'bayesian']
paper: "https://arxiv.org/abs/1803.03764"
issue: 92
issueUrl: "https://github.com/long8v/PTIR/issues/92"
summary: "?"
---
<img width="1020" alt="image" src="https://user-images.githubusercontent.com/46675408/203890454-09882ec3-c607-476c-bac2-2bd428cf0bb1.png">

[paper](https://arxiv.org/abs/1803.03764)

## TL;DR
- **task :** stochastic DNN => image classification, reinforcement learning, adversarial example
- **IDEA :** What if we create a stochastic layer where only the variance is learned, not the mean?
- **architecture :** LeNet-5-Caffe
- **objective :** objective for each task
- **baseline :**VGG-like architecture, Deterministic Policy
- **data :** CIFAR-10, CIFAR-100
- **result :** ? 
- **contribution :** ?
- **limitation or something I didn't understand :** I'll have to reread this later when I have more time.

## Details
### DNN in stochastic setting
- Methods include stochastic layer, stochastic optimization texhinques, etc.
- Used to reduce overfitting, estimate uncertainty, more efficient exploration for reinforcement learning
- Learning a stochastic model can be interpreted as a kind of Bayesian model
- One way to do this is to replace the deterministic weight $w_{ij}$ with $\hat w_{ij} \sim q(\hat w_{ij}|\phi_{ij})$. Then, during training, we are learning about the distribution of weights rather than a single point estimate of this weight.
- However, the test ends up averaging over the distribution of these weights, which is where things like "mean propagation" and "weight scaling rule" come into play.

### Stochastic Neural Network
DNNs are ultimately about predicting target T given object x and weights W.
Consider a stochastic neural network whose weights W are sampled from the parametric distribution $q(W|\phi)$.
As training progresses, $\phi$ is trained by the training data (X, T) and a regularization term $R(\phi)$ is added, which can be written as
<img width="488" alt="image" src="https://user-images.githubusercontent.com/46675408/203891750-81f1df66-e643-4848-871d-f877d127520a.png">
To train this model, techniques such as binary dropout, variational dropout, and dropout-connection are used, where finding the exact $E_{q(W|\phi)}p(t|x,W)$ is usually intractable. So we usually approximate by taking K samples and averaging them, which is called "test-time averaging".
<img width="762" alt="image" src="https://user-images.githubusercontent.com/46675408/203891763-5dc136b6-44cb-4868-9aaa-f2319c55bd7f.png">
To make the calculation a bit more efficient, we find $E_qW$ instead of $\hat W_k$, which is called the "weight scaling rule".
<img width="391" alt="image" src="https://user-images.githubusercontent.com/46675408/203891773-6112d056-8f91-4bf2-8083-864ce555f8fb.png">
In this paper, we want to consider layers with $E_qW=0$, which means that p(t|x, EW=0), so using a weight scaling rule every time would result in a random guess (which is why they don't use weight scaling rules, right?). We want to call these layers "variance layers" and define them as "variance network" because the mean value does not store any information, only the variance.

### Variance Layer
The activation does not depend on $\mu_{ij}$, only on the variance.
<img width="755" alt="image" src="https://user-images.githubusercontent.com/46675408/203892552-bd1a0006-ecd3-4b1e-a3d3-bb691e95794a.png">

### Result
Good results in classification / reinforcement learning / adversarial example
<img width="505" alt="image" src="https://user-images.githubusercontent.com/46675408/203892704-b40111c4-040e-41b0-90f2-44c5c076696c.png">
<img width="416" alt="image" src="https://user-images.githubusercontent.com/46675408/203892717-fdd8c58c-7dfe-40f5-9837-f8ca98e89c7f.png">
<img width="426" alt="image" src="https://user-images.githubusercontent.com/46675408/203892728-9d240e17-182c-478e-be50-b7b0ad69f7be.png">
