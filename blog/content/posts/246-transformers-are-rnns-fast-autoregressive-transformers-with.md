---
title: "[223] Transformers are RNNs:  Fast Autoregressive Transformers with Linear Attention"
date: 2026-04-01
tags: []
paper: "https://arxiv.org/pdf/2006.16236"
issue: 246
issueUrl: "https://github.com/long8v/PTIR/issues/246"
summary: ""
---
<img width="647" height="164" alt="Image" src="https://github.com/user-attachments/assets/7bd2f3ff-bd5b-470d-99b0-fc1adc9b8bb9" />

[paper](https://arxiv.org/pdf/2006.16236),  [blog](https://linear-transformers.com/), [code](https://github.com/idiap/fast-transformers)
## TL;DR
- I read this because.. : April is linear transformer -- first paper
- task : autoregressive sequence modeling, language modeling, machine translation
- problem : self-attention compares all pairs of tokens, time/memory O(N²), inefficient for long sequences
- idea : Replace softmax attention with kernel form $\phi(Q)\phi(K)^T$ and rearrange it as a combinatorial law, which allows cumulative sum
- input/output : token -> token 
- architecture: replaced softmax with kernel with elu function. No other architectural changes
- objective : CE loss 
- baseline : Transformer, RoFormer 
- data : WMT, language modeling benchmark 
- evaluation : BLEU (MT), perplexity (LM)
- Result: large speed/memory improvement on long sequences, slight decrease in performance or similar
- contribution: reinterpreted attention as a kernel, proposed O(N) linear attention, showed that transformer behaves like an RNN
- . etc. : causal masking is naturally embedded in the prefix sum structure, enabling layerwise parallelism

## Details
- conversation with chatGPT: [link](https://chatgpt.com/share/69cc5fbf-78d0-83a9-8ce0-27d5878abf8a)
- X$
### 3.1 Transformer 
<img width="400" height="138" alt="Image" src="https://github.com/user-attachments/assets/14065146-a0cb-4f96-bdc8-113bf1d5f406" />

- f_l(.)$ is just FFN
- $A_l(.)$ self-attnetion

<img width="400" height="223" alt="Image" src="https://github.com/user-attachments/assets/4bd06bf0-53cd-4099-a8b0-3f664fd07017" />

We could have just expressed the softmax term there as the similarity function $sim(\cdot)$

<img width="404" height="130" alt="Image" src="https://github.com/user-attachments/assets/4dee4aab-84f8-47f7-8df0-5aa1a4685f20" />

### 3.2. Linearized attention
This is where I get confused, we're going to use something called a Kernel Trick.
The only constraint on attention is that $sim(\cdot)$ must be "non-negative"
Then, among all kernels , $k(x,y) : \mathbb{R}^{2 \times F} -> \mathbb{R}_{+}$ can be contained.

Suppose we have such an "imagination kernel" ($k$), then rewriting eq (2) for the feature representation $\phi(x)$, we get

<img width="367" height="77" alt="Image" src="https://github.com/user-attachments/assets/92fd85bf-777a-440e-a17e-a56e6c4688d6" />

Above, $\sum _j$ is the value for j, so we can pass over $\phi(Q_i)^T$, which gives us the expression
<img width="412" height="212" alt="Image" src="https://github.com/user-attachments/assets/e8c1acfb-6c0c-4e83-b0fa-20dbe0a6e639" />

In this case, the feature map $\phi(\cdot)$ is computed row-wise on the $Q$, $K$ matrices
The parentheses in eq (6) are $\phi(X)^T\in \mathbb{R}^{D\times N}$, followed by $\phi(X)^T\in \mathbb{R}^{N\times D}$, resulting in a time and space complexity of $O(N)$. (I'm confused about the spatial and temporal complexity...) --
The reason for this is that we will store and reuse KV, K once.
<img width="407" height="62" alt="Image" src="https://github.com/user-attachments/assets/7efdd83c-83ba-4500-ba71-ea65faee9f50" />

### Feature maps and computational cost
Choose the elu function because the computational cost depends on which kernel you use
<img width="384" height="45" alt="Image" src="https://github.com/user-attachments/assets/ca642be0-ad65-4637-a969-f66705b5c133" />

I used relu over elu because I wanted the gradient to flow even when below zero.

### 3.3 Causal Masking
How do I get Transformer's Causal masking here?
This can be accomplished by changing the summation to $i$ instead of doing it for all j

(previous expression)

<img width="509" height="110" alt="Image" src="https://github.com/user-attachments/assets/217a5bb1-5beb-4b3e-98c0-bb665f6a9996" />


(w/ causal masking)
<img width="429" height="475" alt="Image" src="https://github.com/user-attachments/assets/cf7e737b-1ea1-4a04-9a04-fbb02e9ba86f" />

We can calculate $S_{i}$ from $S_{i-1}$. because it is a cumulative sum.
I was confused when I first read this, but it seems like you're using cumulative sums for inference and applying causal masks like the original transformer for actual training.

#### 3.3.1 Gradient Computation
If we solve for the gradient naively, we get another $O(N^2)$ complexity, but we solve nicely and make this one linear as well

<img width="423" height="317" alt="Image" src="https://github.com/user-attachments/assets/2fdcfcbb-ba51-4c02-94ae-723b2e493457" />

#### 3.3.2 Training and Inference
The good thing about Transformer is that you don't need to have QKs for inference, so memory doesn't grow proportional to seq len. In other words, it takes all the good things about train and inference
<img width="654" height="467" alt="Image" src="https://github.com/user-attachments/assets/da071831-893e-4452-8fb4-f0cebe4002b2" />


### 3.4. Transformers are RNNs

<img width="428" height="287" alt="Image" src="https://github.com/user-attachments/assets/a5422cd6-7480-4748-96f2-c1c0d9c97e71" />

## Experiment 
Skip h

