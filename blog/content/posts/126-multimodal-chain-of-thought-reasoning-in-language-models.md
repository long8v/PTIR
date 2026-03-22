---
title: "Multimodal Chain-of-Thought Reasoning in Language Models"
date: 2023-06-07
tags: ['multimodal', '2023Q1']
paper: "https://arxiv.org/abs/2302.00923"
issue: 126
issueUrl: "https://github.com/long8v/PTIR/issues/126"
summary: "Seeing flamingo give a demonstration and wondering what tricks can be done in the Infer step in multi-modal, and spring - seems to suggest a CoT that sees visual information for the first time"
---
<img width="1383" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d0810875-33b6-4243-95ee-1fe52d61f84e">

[paper](https://arxiv.org/abs/2302.00923)

## TL;DR
- **I read this because.. :** flamingo gave me a demonstration and I thought, what trick can I do in the Infer step in multi-modal?
- **task :** chain-of-thought
- **problem :** Only the kids with 100B+ parameters were able to CoT. Why did 1B fail? When LLM's chain-of-thought is used for Multi-modal, hallucination appears and the performance gets worse.
- Idea :** Learn two models: one that sees a QCM (question / context / multiple choice) and generates a rationale, and one that receives the rationale and QCM and generates an answer. They have the same architecture but are trained separately. In this case, both models receive the vision feature additionally.
- **input/output :** image, context, question, options -> gold rationale / image, context, question, option, rationale -> answer
- **architecture :** DETR encoder + T5(initialized by unified QA)
- **objective :** cross entropy loss
- **baseline :** No-CoT(one-stage model), CoT w/o visual feature, CoT with caption  
- **data :** ScienceQA
- **evaluation :** RougeL, accuracy
- **result :** language only CoT superior to GPT3.5.
- **contribution :** Looks like you suggested a CoT that sees visual information for the first time.
- **etc. :**

## Details
### Problem
<img width="552" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5dff0b2d-86cf-47a6-b6ed-12775838f228">

When I trained SicenceQA with a text-only model in a one-stage setting (reasoning and answer at once?), the performance was worse than without CoT.
To see why this was the case, I split the performance by QCM -> R / QCMR -> A and got this result

<img width="566" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a60dd92d-20b1-4385-9430-5694e56fd917">

<img width="581" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/cb47651d-48df-4335-8286-3c952570927d">

In other words, we were generating the wrong rationale. In the example below

<img width="1148" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/eb4339f3-8d5a-4077-9f7e-7258dfbaa4f5">

Of course it's obvious... If I don't look at the image and ask to make rataionale, hallucination -> performance drops as if I saw something contrary to the image.

## Framework
<img width="1150" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7d711b7c-407b-4141-a2ab-d815cc17154a">

(i) rationale generation and (ii) answer inference, which have the same architecture but are trained separately (is there a reason for this in the paper?).
In step (i), the input is $X=\{X^1_{language}, X_{vision}\}$ and the output is $R$, which is the rationale.
Step (ii) concatenates the generated $R$ to produce the input X'={concat(X_^1_{language}, R), X_{vision}} and generate the answer $A$.

## Architecture 
- Encoding
<img width="522" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d39dd4c1-d4c4-45bf-b1c2-cda9222bb38f">

VisionExtractor is DETR. $H_{vision}\in\mathbb{R}^{m\times d}$ and dimensioned with (m: # of patches, d: hidden dim) lanugage output.

- Interaction
<img width="346" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/20da5879-1781-478e-ae1c-03a9d512425b">

Q : $H_{language}$
K=V: $H_{vision}$

I did a gated fusion and let it learn how much vision information to look at.

<img width="485" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/68d15375-3d18-45bc-98ce-13623cc5b5d0">

## Result
<img width="1153" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2aea36cc-4abd-4c5e-bd70-ac7b40ac33ed">

Superior to GPT-3.5 performance

<img width="542" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c8d78875-1bb5-4128-a913-6e110cf55372">

For the two-stage baseline (training with two stages without looking at images), performance was good initially, but did not improve as the epoch progressed.
Why is the one-stage baseline getting better? Hmm...

- vision features architecture

<img width="513" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/29d3879b-5e49-45ac-8858-f8e9831feb71">

- language model architecture
<img width="557" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/559625dc-1ac4-4850-a602-b19c87333bfa">

- Multimodal CoT error case study
<img width="531" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0bc77578-e14a-4434-b3c1-a2575fad5f24">
