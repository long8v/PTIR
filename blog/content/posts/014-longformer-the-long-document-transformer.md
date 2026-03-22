---
title: "Longformer: The Long-Document Transformer"
date: 2022-02-22
tags: ['NLP', 'AllenAI', '2020Q1', 'long']
paper: "https://arxiv.org/pdf/2004.05150.pdf"
issue: 14
issueUrl: "https://github.com/long8v/PTIR/issues/14"
---
<img width="476" alt="image" src="https://user-images.githubusercontent.com/46675408/155048272-139cfd7f-a3e4-4319-9eb4-44b0e73b5d77.png">

[paper](https://arxiv.org/pdf/2004.05150.pdf), [code](https://github.com/allenai/longformer)
**problem :** Transformers grow in complexity quadratically with the length of the sentence.
**solution :** Get attention with a sliding window (+dilated) and stack it. Add global attention to tokens in the right places for specific tasks.
**Results :** SOTA on text8, enwik8, and outperforms RoBERTa on the long document tasks WikiHop and TriviaQA. Encoder-decoder model is effective on the arXiv summary dataset.
**details :**
- Windowed local-context self-attention is used to learn contextual representations, while global attention is used to create a representation of the entire sequence for prediction.
- Not only did we evaluate it with an auto-regressive task, but we also trained it on an objective like MLM and confirmed that it was SOTA.
- We also propose an encoder-decoder model, the LED model.
- There are two approaches to long-document transformers: 1) left-to-right approach, which learns in chunks while moving from left to right, which has unstable performance when applied to different tasks. 2) The sparse attention approach, typified by the Sparse Transformer.
<img width="1101" alt="image" src="https://user-images.githubusercontent.com/46675408/155049664-090c68e4-6546-441c-98ce-eded06d8ac5f.png">

- The typical way to deal with long sentences is to truncate the document to the maximum token count of 512, or to combine them after truncation. Alternatively, the method used in multihop or open QA is to first retrieve the relevant documents and then pass them on for answer extraction.
- Attention Pattern 
- Sliding Window: Since local context is important, we use a fixed size of window attention and stack them (like a CNN) to be viewed in a larger receptive field. The receptive field of the entire model will be window size(=w) * # of layers(=l).
- Dilated Sliding Window: To increase the receptive field without increasing the computation, the sliding window can be dilated (as in [dilated CNN](https://zzsza.github.io/data/2018/02/23/introduction-convolution/)). With dilated, the receptive field of the model becomes w * l * d. In multi-head attention, we found that varying the dilated size d for each head is effective for performance.
- Global Attention : Depending on the task, the optimal input is different (`[CLS]` token for classification, question + docuemnt concatenation for QA, etc.), but since the above attitudes are not appropriate for various tasks, we added global attention for tokens in the right place for a specific task.
- Linear Projecton for Global Attention: Taking the linear projection of the sliding window and the linear projection of global attention differently helped to improve performance. The global projection was initialized to the projection of the sliding window.
 