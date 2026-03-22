---
title: "[116] Data Distributional Properties Drive Emergent In-Context Learning in Transformers"
date: 2023-05-22
tags: ['DeepMind', 'NeurIPS', '2022Q2']
paper: "https://arxiv.org/abs/2205.05055"
issue: 125
issueUrl: "https://github.com/long8v/PTIR/issues/125"
summary: "CS330에서 나옴. Some interpret in-context learning in LLM as meta-learning, and I asked you what you think about it, but I missed it lol This paper seems to be saying that - 1) RNNs should not be used, but Transformer model 2) when there is busrtiness in the data 3) when there is a large set of rare classes"
---
<img width="759" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/39c85c03-a4f7-4f3f-b502-3ebf8c64fba0">

[paper](https://arxiv.org/abs/2205.05055)

## TL;DR
- **I read this because.. :** CS330에서 나옴. LLM's in-context learning is sometimes interpreted as meta learning, but I asked him what he thinks about it, and he said he would have listened to it.
- **problem :** When does in-context learning work? When does the "emergent" ability of the LLM show up?
- Idea :** Natural data, unlike supervised data, is not the same as
- **input/output :** {image, label} sequence + query image -> novel label
- **architecture :** encoder(ResNet) + causal Transformer
- **objective :** ce loss 
- **baseline :** RNN, LSTM  
- **data :** Omniglot
- **evaluation :** Given 8 contexts and 1 test query, classify them well. To evaluate the "holdout image" (an image that has never been seen before), we randomly assign the class of 2 images in a 4-shot 2-way evaluation (e.g., the alphabet "a" was originally labeled 0 in the original evaluation, but 1 in the test).
- **result :** 1) RNN should not be used, but Transformer model 2) when there is busrtiness in the data 3) when there is a large set of rare classes
- **contribution :**
- **etc. :**

## Details
### in-context learning vs in-weight learning
- in-context learning does well when given only a few samples of a new concept without weight updates
- in-weight learning is a gradient update to do a few shots well with supervised learning
In terms of meta-learning, MANN or MAML can be seen as in-context learning. However, in recent LLMs, this in-context learning is not directly taught, but "emergent", so why is this?

### Experimental design
<img width="564" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0b4361e3-f81a-4c2e-9117-c89685831331">

Like the black box meta learning methodology, in-context learning is given an image, label sequence as context and sees how well it does when given a query image.
- BURSTY means that a certain class comes in bunches (AA A comes in bunches in a short period of time)

In this paper, we look at 1) burstiness 2) a large number of rarely occurring classes 3) multiplicity of labels 4) within-class variation

### Burstiness
As shown in the example above, we evaluated with data that intentionally increased the busrtiness, and found that for in-context learning, increasing the burstiness increases the
In contrast, in-weight learning performs poorly as busrtiness increases
<img width="737" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ae27b780-3a51-4525-bcfd-99e2b3c31364">

### a large number of rarely occuring classes
I experimented with increasing the num of classes from 100 to 12800 (original class 1600) while giving omniglot a roatation (each class becomes less frequent and therefore long-tailed).
Once again, the number of classes was reversed: more in context learning was better, but more in weight learning was worse.
<img width="745" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d001758f-d940-4962-9fc1-2aea2313297a">

### Multiplicity of labels
When I tried it with multiple labels for a single class, the performance improved again
<img width="400" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/cad4d01b-721f-49a5-b98d-4291daf1a1c7">


### within-class variation
I tried a lot of variation within classes, and again, for in-context learning, the higher the variation, the better the performance
<img width="731" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/84c346df-d8b3-4cea-8c6b-ccd9f374378a">

### Architecture

<img width="714" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/fe79568e-2a94-4908-b9f7-3006122690d3">

I ran rnn / lstm with all the right number of parameters / depth, etc. but never got in-context learning ability...
For some reason, even the authors don't know why!
we were completely unable to elicit in-context learning in recurrent models, even with the training procedure, number of
parameters, and model architecture otherwise matched to the transformer experiments. 
Emphasized that using a transformer alone does not result in in-context learning, and that the data distribution must have the three characteristics above.