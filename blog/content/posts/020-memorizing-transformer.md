---
title: "Memorizing Transformer"
date: 2022-04-07
tags: ['NLP', '2022Q1', 'google', 'ICLR', 'long']
paper: "https://arxiv.org/pdf/2203.08913.pdf"
issue: 20
issueUrl: "https://github.com/long8v/PTIR/issues/20"
---
![image](https://user-images.githubusercontent.com/46675408/162104237-089962f3-c835-45c6-a61b-c2cc3c138fc5.png)
[paper](https://arxiv.org/pdf/2203.08913.pdf)

## TL;DR
Cache the key, value matrix of the previous sequence for long contextual references.
Then, use a kNN lookup (e.g. Faiss, ScaNN) to extract the keys and values that are relevant to the current query and concatenate them into the key and value matrix to get attention. At this time, previous cached memories are not learned.

## background
### long document
A common approach to long sequence lengths in transformers is to truncate the sequence to the maximum sequence length that can fit in memory.
In this case, if the same document is truncated by length, the information before it is not known, and this is called the "context fragment problem".
![image](https://user-images.githubusercontent.com/46675408/162108203-7968c7d5-67e2-4f9e-aa40-9395c563e7ed.png)

This is especially true when you need to reference distant contexts, such as novels or code.
To solve this problem, we have Transformer-XL, longformer, reformer, etc.
![image](https://user-images.githubusercontent.com/46675408/162108330-acb7eab3-2dfd-42e3-b7ab-5b34e2c3134a.png)
The main idea behind Transformer-XL is,
We cache the hidden vector of the nth layer of the previous segments and concatenate it with the hidden vector of the current segment to perform the attention operation.
![image](https://user-images.githubusercontent.com/46675408/162108701-3bc6a782-3c9f-4c58-850b-8e5fd8117915.png)
In this case, cached hidden vectors are not back-propagated.

### kNN lookup
Finding and pulling the k closest data given a query
For example, given a trained word2vec, think of it as having a vector that computes vector(queen) - vector(female) + vector(male), and you want to compute which vector is closest to the vectors of all the words trained on word2vec.
Efficient implementations of this are 1) [faiss](https://github.com/facebookresearch/faiss) 2) [ScaNN](https://ai.googleblog.com/2020/07/announcing-scann-efficient-vector.html)

### retrieval with transformer
Performing a kNN lookup means performing a kind of retrieval, which uses the vectors from the transformer to perform a search, and approaches that apply this to NLP tasks include REALM and RAG.
REALM is a model that e2e learns a model that retrieves documents when a query is given to perform QA and an MRC model that attaches the resulting docuemnt to it.
![image](https://user-images.githubusercontent.com/46675408/162110005-cddf1cfe-b250-4af7-88ab-b8793745c84a.png)

## Memorizing Transformer
As explained in the background, the memorizing transformer is an approach to efficiently tackle long documents that uses a kNN lookup to select the segments with the most similar key values to the query and then appends them to the attention operation.

First, the document is cut in the following order
![image](https://user-images.githubusercontent.com/46675408/162111133-4817372f-61f7-482f-8a35-f0c3af60c495.png)
In the lower layers, we proceed like a normal transformer decoder. We cache the key and value vectors from each segment.
Queue it until it runs out of memory, pull it out when it runs out of memory, and insert the key value of the latest segment.
![image](https://user-images.githubusercontent.com/46675408/162111100-825fd565-9745-4654-9270-ac8a1a66b5c3.png)

Now, given a query, it 1) pays attention to the general local context and 2) performs a kNN lookup on the query in memory, pulls out k keys and values, and creates an attention matrix from these k keys and values. (Think of it as a transformer decoder for k keys and values.)
![image](https://user-images.githubusercontent.com/46675408/162113989-b0ec1809-840f-4579-ae7f-b0f32c95fef2.png)

Then you can do a weighted sum with different scala parameters for 1) and 2) depending on the head.
![image](https://user-images.githubusercontent.com/46675408/162114512-c6521e41-0670-4876-908e-eb6ecfe1705a.png)
In our experiments, we found that almost all heads refer to external memory in most cases.

**Position bias**
Added T5-style position bias.
![image](https://user-images.githubusercontent.com/46675408/162117109-21d62b90-b198-4c0f-9ef5-48c3a9a9f9e7.png)
This seems to be a slightly simplified version of the usual relative position embedding.

**Batching**
Memory is isolated because each batch has a different document, and when the document is finished, its memory is cleared (designed to not refer to other documents).

## Experiment
**Dataset**
- github code, my math-related papers on arXiv, Isabelle, a corpus of math theory proofs, C4, data with token lengths greater than 4096, and PG-19, data from English-language books.

**Parameter**
- 12 layers transformer, 1024 hid dim, 8 heads, FFN dim 4096
- In kNN, k is 32, used in 9th layer of 12 layers
- sentence-piece tokenizer(vocab size 32K)
- Adafactor optimizer, linear warmup scheduler, square root decay, 32 TPU
- JAX implementation

## Result
**Scaling to Larger Model**
![image](https://user-images.githubusercontent.com/46675408/162110640-97e673f3-d931-4efe-9d53-24012bdbe5ff.png)
Our model with 8K tokens in memory can perform similarly to vanilla Transformer, even with a model size 5x smaller.

**Effect of External Memory**
![image](https://user-images.githubusercontent.com/46675408/162110611-4007c233-c9b8-4454-9a2e-07cba0efff6a.png)
XL cache is viewed as Transformer-XL.
External memory improves perplexity for vanilla Transformer, Transformer-XL
In vanilla Transformer, the segment is truncated and the first token is missing information, so the XL cache fills in the localized short-range context and external memory fills in the longer context.
Performance for context length 512 and memory 8192 (arxiv 2.49) is similar to context 2048 and xl cache 2048 (arxiv 2.42).
The fact that memory is non-differentiable, context is differentiable and affects all layers, and performance is similar means that long-range context is not necessarily needed in the layers below the transformer.

**Finetuning a non-memory model to use memory**
![image](https://user-images.githubusercontent.com/46675408/162122760-5eb4a44e-0f12-4ccf-8b9a-f258d8bdd038.png)
Pre-training like this is pretty expensive, so I tried using memory only for fine-tuning and it worked well.

**Information Retrieval Patterns**
Often looked up rare words like definitions, people's names, etc.
![image](https://user-images.githubusercontent.com/46675408/162112281-ac48ec0d-086c-4b5a-b5f2-3b2d904eb02d.png)
Example of context retrieved from the Isabelle dataset

## conclusion
1. the idea is simple and intuitive
2. in our domain, I don't know... the segment is so long that it would only make sense when it goes beyond the segment that transformer XL can cover.
3. truncate the seq_len and make the batch_size much larger to train faster?
4. since it only needs to be applied to finetuning, it should be easy to apply (once implemented).

## etc
**papers**
- relative PE https://arxiv.org/pdf/1803.02155.pdf
- different style or relative PE https://arxiv.org/pdf/2006.15595.pdf