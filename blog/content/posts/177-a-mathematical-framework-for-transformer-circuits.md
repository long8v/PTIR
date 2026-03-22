---
title: "[158] A Mathematical Framework for Transformer Circuits"
date: 2024-05-09
tags: ['2021Q4', 'XAI', 'anthropic']
paper: "https://transformer-circuits.pub/2021/framework/index.html"
issue: 177
issueUrl: "https://github.com/long8v/PTIR/issues/177"
summary: "I read in TextSpan (https://github.com/long8v/PTIR/issues/172) that they wrote the OV circuit used in this paper and it seems to be used in mean ablation, but I don't understand what it is."
---

<img width="600" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/14eb104a-0764-4c1b-9c51-7cc1e3407dec">

[paper](https://transformer-circuits.pub/2021/framework/index.html)

## TL;DR
- **I read this because.. :** TextSpan(https://github.com/long8v/PTIR/issues/172) wrote the OV circuit used in this paper, and it seems to be used in mean ablation, but I don't understand the content.
- **problem :** Let's think about how Transformer works by breaking it down into circuits.

## Details
### Related Work
The word "circuit" did something to me, and this paper by similar authors https://distill.pub/2020/circuits/zoom-in/ was a starting point.
It is called sub-graph analysis of how features are connected inside the neural network. Hmm... I'll have to read more about it, but it seems like it's the way you can separate them.
I was wondering how the visualization is done here, but it seems to use a methodology called https://en.wikipedia.org/wiki/DeepDream ([code](https://github.com/google/deepdream/blob/master/dream.ipynb)) for the active layer. I've always wondered how to draw those LSD-like pictures, but I can't believe it's this old.

### High-Level Architecture
<img width="1019" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/316e9a3c-d3df-4465-9643-27ce9bf60653">

A transformer looks roughly like this
1) token embedding
2) The part that adds each head operation $h(x_i)$ to the residual stream
3) The part that takes the mlp in the residual stream and adds it back to the residual stream
4) word unembedding (=> logit prediction)

We analyze the "residual stream" as the place where communication between channels takes place.
<img width="148" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e079bed2-b1b3-4a9a-ac83-ab7b945c4bb6">

Each layer's hidden gaps are available to each other because they are connected by a residual
<img width="857" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1052130c-44fd-4be4-b555-542b6e48e18b">

<img width="819" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6a8fc506-bbe3-475c-8c1a-f639db175029">


### Attention Heads are independent and additive 
<img width="586" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/eecedcfc-cb49-49b7-b239-24f59d1c0e8e">

The requirement is just a matrix operation, concatenating $W_o$ for each head, but it is actually equivalent to multiplying $W_o^{h_i}$ for each head and summing it. In other words, you can think of it as adding and subtracting information from the residual stream for each head.
 
### Attention Heads as Information Movement
In this case, reading and writing information from the residual stream can be completely decoupled. To see this, let's write the attention operation a little differently.
1. each token is viewed from the residual stream to compute the value vector $v_i=W_Vx_i$
2. take the attention score $A_i$ and linearly combine it to get the result vector $r_i=\sum_j A_{i,j} v_j$
3. find the output vector for each head $h(x)_i=W_Or_i

Each step can be written as a matrix multiply, why not combine them into one matrix, because $x$ is a two-dimensional tensor in (seq_len, head_dim), where multiplying $W_v$, $W_o$ happens in the head_dim dimension and multiplying $A$ happens in seq_len.
The above operation can be expressed as [Tensor product](https://transformer-circuits.pub/2021/framework/index.html#notation-tensor-product).
<img width="571" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/80f34245-0d57-403a-8cf7-30190483732c">

Make the contextualized embedding $x$ a V, multiply it with the attention score A, and outputrhk rhqgksek.
We can summarize this as follows and combine $W_oW_V$ into one.

<img width="341" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ca42272e-3225-4e4c-b36a-40f20ae145ab">

### Observation about attention heads
- The attention head is responsible for moving a token from one token to another in the residual stream. The residual vector space can be thought of as "contextualized word embedding".
- In this case, $A$ and $W_OW_V$ can be viewed as two linear operations, where $A$ and $W_OW_V$ play different roles.
- A$ governs where the information of "which token" goes and where it comes from
- The $W_OW_V$ determines "what information" is read and written from the source token.
- In this case, only $A$ is nonlinear because it has a softmax, and if we fix $A$, it can be seen as a linear operation.
- Since $W_Q$ and $W_K$ always move together, we can think of $W_OW_V$ and $W_Q^TW_V$ as a single low rank matrix.

### Zero-Layer Transformer
A plain zero-layer transformer without MHSA is a kind of bigram learner.
<img width="151" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7ea2edfe-9f2c-4194-941d-887ba0b01ab2">


### One-Layer Attention-Only Transformer
<img width="754" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5e9bd685-cfd4-4cc4-8000-bc74e43a49fb">

It can be summarized as follows where h is the operation for each head and can be found by sum (as summarized in the section above)
If we replace this with the tensor notation
<img width="725" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/732979fb-c111-47d9-b4fa-d3660f25399e">

If we change this and this again
<img width="690" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/53452059-a9a1-4b21-8b83-8307579f477c">


It is split into two terms. The first term carries the bigram statistics of the zero-layer transformer, while the second term carries the attention head

### Splitting Attention Head terms into Query-Key and Output-Value Circuits
The second term can be further separated.
<img width="709" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a653d3c0-0171-41be-b939-c171bfd8b9bc">

<img width="768" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d041864d-bafa-40fb-b9be-a99c593389c8">

As explained earlier, the OV circuit is how to attend and the QK circuit is which token to attend.

### OV AND QK INDEPENDENCE (THE FREEZING ATTENTION PATTERNS TRICK)
I read this to see...
The bottom line is that if you save the QK circuit with two forwards and view it as a fixed value and analyze the OV circuit, you can do a lot of interesting analysis because it is linear!

> Thinking of the OV and QK circuits separately can be very useful, since they're both individually functions we can understand (linear or bilinear functions operating on matrices we understand).
But is it really principled to think about them independently? One thought experiment which might be helpful is to imagine running the model twice. The first time you collect the attention patterns of each head. This only depends on the QK circuit. 14 The second time, you replace the attention patterns with the "frozen" attention patterns you collected the first time. This gives you a function where the logits are a linear function of the tokens! We find this a very powerful way to think about transformers.

Actually, I think it gets more interesting from here on out... I'm tired, so I stop reading here.