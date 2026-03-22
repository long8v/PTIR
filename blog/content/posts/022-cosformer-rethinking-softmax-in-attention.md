---
title: "cosFormer: Rethinking Softmax in Attention"
date: 2022-04-20
tags: ['NLP', 'attention', '2022Q1', 'ICLR', 'long']
paper: "https://arxiv.org/pdf/2202.08791.pdf"
issue: 22
issueUrl: "https://github.com/long8v/PTIR/issues/22"
---
<img width="1234" alt="image" src="https://user-images.githubusercontent.com/46675408/164129350-b160b6e7-1644-4f90-b8a5-637177039da3.png">

[paper](https://arxiv.org/pdf/2202.08791.pdf)

## Introduction
- In vanilla Transformer, doing dot product + softmax is necessary to model long-range dependencies, but the softmax operation is too heavy, especially for long sequence lengths.
- `Q` (batch_size, query_seq_len, hid_dim) * `transpose(K)` (batch_size, hid_dim, key_seq_len) gives us (batch_size, query_seq_len, key_seq_len) and we take the softmax of the last dimension to get the attenion score. -> as key_seq_len gets longer, softmax also gets heavier
- To reduce this, SparseTransformer, Random feature attention, ReFormer, etc. were proposed, but they (1) make assumptions about the attention matrix and (2) make approximations, so if the assumptions do not hold or the approximation error increases, they do not perform as well as vanilla Transformer. Also, some methodologies could not be applied to causal attention for LM. For example, Linformer and BigBird could only be used for cross attention.
<img width="826" alt="image" src="https://user-images.githubusercontent.com/46675408/164129294-74a48cec-5bee-42f5-a022-83325c66f53d.png">

- Against this backdrop, we wanted to see if we could replace softmax with a linear function while preserving its key properties.
- (i) the attention matrix is non-negative
- (ii) non-linear re-weighting scheme acts to stabilize attention weights
- For example, [linear transformer](https://arxiv.org/abs/2006.16236) achieved (i) with exponential linear units, but did not re-weight (?), which is why it performed poorly in the Long-Range Arena.
  - **long-range arena** : [A Benchmark for Efficient Transformers](https://openreview.net/forum?id=qVyeW-grC2k)
- We propose a CosFormer that satisfies the above properties: (i) passes the feature map through ReLU before obtaining the attention score; and (ii) uses the cos re-weighting scheme to amplify the local correlation a bit more.
- This attribute decomposes exactly into a linear form.
- Took first place in the Long-Range Arena.

## Our Method
The idea of CosFormer is to replace the non-decomposable non-linear softmax operation with a decomposable non-linear re-weighting mechanism and a linear operation.
<img width="1235" alt="image" src="https://user-images.githubusercontent.com/46675408/164130473-14be81cf-9777-42b6-b815-4a1fcf02fc9e.png">

A typical transformer can be as complex as O(L**2).
The important thing to note is that you can choose any similarity function. To make S(Q, K) linear, we can make the similarity function a decomposable similarity function. -> \phi(Q)\phi(K) is the similarity, not exp(Q KT)
<img width="944" alt="image" src="https://user-images.githubusercontent.com/46675408/164132645-5a48027f-30e0-4f1b-a9b8-d8fe692987dc.png">

After that, we can achieve linear complexity O(Nd^2) by first finding KV via the matrix property. In general, since N >> d, we can express it in O(N).
![image](https://user-images.githubusercontent.com/46675408/164134693-15ecb53d-3d0c-4843-8c00-6e56df2e6223.png)

<img width="1150" alt="image" src="https://user-images.githubusercontent.com/46675408/164131888-d7f7ba8f-5c55-40b0-94d7-1ac458d4b5f8.png">

<img width="613" alt="image" src="https://user-images.githubusercontent.com/46675408/164140863-becc1ac8-81da-4b4a-b659-6ad89503d21d.png">
We characterized softmax as (i) non-negative and (ii) non-linear re-weighting, and used different functions to find the similarity matrix to verify this. We found that ReLU > LeakyReLU > Identity due to its non-negative nature, and softmax > ReLU due to its non-linear nature.

CosFormer
1) linear projection kernel = ReLU, dot product.
<img width="751" alt="image" src="https://user-images.githubusercontent.com/46675408/164141151-dff949af-023a-40d2-a1d0-1b70e01b4663.png">

To remove negative values, the kernel used ReLU.
<img width="970" alt="image" src="https://user-images.githubusercontent.com/46675408/164141221-06356172-c56c-4887-9a84-2ecef3888f88.png">

The similarity function did a dot product by row.
<img width="1229" alt="image" src="https://user-images.githubusercontent.com/46675408/164141769-80023c75-58f2-4b60-99ad-62ded23a1e5d.png">

2) cos-Based Re-weighting Mechanism
The non-linear re-weighting that softmax does is important, as it focuses the distribution of attention weights and stabilizes the learning process. We also saw that it penalizes distant connections and enforces close ones.
<img width="796" alt="image" src="https://user-images.githubusercontent.com/46675408/164142323-0beac77b-2bd5-406b-a665-2e01a4ed49b5.png">

This cosine strategy is fully decomposable (formula omitted)
<img width="998" alt="image" src="https://user-images.githubusercontent.com/46675408/164142430-bc4f8039-4f7b-45e8-8d3b-8c7d7a229380.png">


## Result
<img width="889" alt="image" src="https://user-images.githubusercontent.com/46675408/164142850-8ab06fb9-8fd0-498c-b8d3-2c8656640cad.png">

<img width="802" alt="image" src="https://user-images.githubusercontent.com/46675408/164142727-b48d5f93-0a92-43a9-84b0-8864914e6f4c.png">


**papers**
- RFA
-  Transformers are rnns: Fast autoregressive transformers with linear attention
- performer
- One-vs-each approximation to softmax for scalable estimation of probabilities
- Stochastic Positional Encoding
- Rotary Position Embedding
