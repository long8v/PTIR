---
title: "Contrastive Explanations for Model Interpretability"
date: 2024-04-01
tags: ['2021Q1', 'XAI', 'emnlp', 'AI2']
paper: "https://arxiv.org/abs/2103.01378"
issue: 168
issueUrl: "https://github.com/long8v/PTIR/issues/168"
summary: "Regarding personal research. Recommended by Claude AI - seems to be almost pioneering work in the area of contrastive explanation."
---
<img width="676" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8b65eb8c-0135-4943-abfa-e3e675d537c8">

[paper](https://arxiv.org/abs/2103.01378)

## TL;DR
- **I read this because.. :** Personal research related. Recommended by Claude AI
- **task :** contrastive explanation. Explain why you chose B over A
- **problem :** I want the model to be explainable, but I can't enumerate all of the explanations and it's simpler to explain why A over B.
- **idea :** Subtract the rows of weight W used to predict the final model class y, then project it and multiply it with hidden. The multiplied value is then forwarded several times with the text span masked, and the values are compared to highlight the values with the most change.
- **input/output :** text - > class // text span highlighted for why model predicts class y over y'
- **architecture :** RoBERTa
- **objective :** MLM
- **baseline :** - 
- **data :** NLI, BIOS (task to get biographies and categorize occupations)
- **evaluation :** Poorly understood.
- **result :** Poor understanding. Like you only evaluated qualitatively?
- **contribution :** Seems to be almost pioneering work in the area of contrastive explanation.
- **etc. :**

## Details
<img width="338" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/052e273b-3429-4ed5-a6da-7f001fa357d8">

<img width="316" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/27ad5244-d285-4335-bfe3-5a48067bc662">

### method

Once masked, we will do multiple model forwards. We call this the amnesic methodology.

- K : model class
- y : output class 
- enc : neural encoder
- $W \in \mathbb{R}^{K \times d}$ : final linear layer
- $y^*$ : model prediction (fact) / $y'$ : alternative prediction
- $p$ : model probabilities
- $w_{y^*}$, $w_{y'}$ : rows used to predict the two classes in the weight matrix W.

Let $w_{y^*}$, $w_{y'}$ be the two weight rows in one contrasting direction $u$.
<img width="110" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ef30ed52-f8b7-4f66-a64e-028822b870bc">


If the model predicts $y^*$ to be higher, then $u^T*h_x>0$.

<img width="233" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a501f136-4fc9-423b-a464-e395988b9a89">

Use this u to create a projection for the hidden state $h_x$.
The result of this C operation is a matrix that can be interpreted as a contrastive intervention on $h_x$.
Then we do the same operation as before, $q = \text{softmax}(Wh_x)$, and get the coefficient of the text span as shown below.

<img width="244" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d82db45f-e17d-4c6c-be6c-4b752ae5a836">

where p is the model prediction of the value without projection and q is the value with projection.

## result
<img width="325" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/71f8da7c-9409-4f4c-8c1d-165ee87e1112">

Results are hard to interpret...

