---
title: "FOIL it! Find One mismatch between Image and Language caption"
date: 2024-03-03
tags: ['dataset', '2017', 'XAI', 'evaluation']
paper: "https://arxiv.org/pdf/1705.01359.pdf"
issue: 163
issueUrl: "https://github.com/long8v/PTIR/issues/163"
summary: "I wanted to see how the data was created / how it was evaluated - later used as a hallucination measure, etc."
---

<img width="839" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0bc0c5c1-8b30-48a2-8eb3-bda6649943ee">

[paper](https://arxiv.org/pdf/1705.01359.pdf)

## TL;DR
- **I read this because.. :** I want to see how the data was created / how it was evaluated.
- **task :** proposed. (1) FOIL Detection (2) FOIL word detection (3) FOIL word correction 
- **problem :** Do VLM models like captioning, VQA models, etc. really understand both modalities well?
- **idea :** replace word in caption with another similar word
- **input/output :** {image, caption} -> (1) whether it's FOIL or not (2) where the FOIL word is (3) FOIL word correction
- **objective :** ce loss 
- **baseline :** sota VQA at the time, Caption model / LSTM that only saw captions, CNN LSTM
- **data :** 65K (train) / 32K (test) images, 197K (train) / 99K (test) captions utilizing COCO's captions.
- **evaluation :** (1) accuracy (2) Did I find the word well in the FOIL caption. evaluate as a noun only / evaluate as a full noun (3) Given a FOIL word, does it change to the original word?
- **contribution :** later used as hallucination measure, etc.
- **etc. :** 
- Make it the most reasonable way you can in '17
- Not a very popular evaluation set -> you might be better off with the latest LVLM benchmarks
- Changing a single noun is a bit of a disadvantage.

## Details
### Task
<img width="417" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/83d6a138-ce4a-402b-895b-2bdb99b59da6">

### num samples
<img width="758" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2a375e8b-9dd3-4949-a3b8-80e925ccf1a1">


### How data is created
<img width="804" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b8fc1f83-261e-45e5-9282-1b5b0107626b">

1) Create a pair with objects with the same supercategory in MS-COCO
- Remove those with more than one word. e.g. traffic light
2) Split the train / test category
- The targe::foil pair used in training will not be used in testing
3) Create a foil caption
- Replace the words in the caption with
- And replace for objects that don't exist in the image
- e.g., in "A dog and a cat eat," you don't replace the dog with the cat because you have a cat
4) Using a captioning model called Neuraltalk to select the most difficult captions

### Evaluation
- T1 is just a classification
- T2 finds the foil word given {image, FOIL caption}.
- T3 is good at fixing the foil word when given {image, FOIL caption, FOIL word}.

<img width="409" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/267fea78-4857-4ba1-b41e-57a9f00862b3">

For T1, the captioner model was asked to generate a caption with each word removed from the original caption, and then compare the caption with the word replaced with the model's higher prediction to the original caption, and if the model's prediction was higher, the caption with the word replaced was determined to be FOIL.

<img width="414" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/039819c4-e4a0-48cf-8f0b-a48be7308666">

For T2, read Towards Transparent AI Systems: Interpreting Visual Question Answering Models (https://arxiv.org/pdf/1608.08974.pdf)
<img width="877" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3c14e33e-d32f-47fb-998d-b9d153bf5b02"> 에서 사용된 occulsion 방법을 사용.
This is measured by how much the score changes from the original predicted answer after masking and forwarding the words in the question one by one.

<img width="329" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/21f7f90f-6d26-430c-bdb0-24f0653bd5bf">

For T3, do a linear regression on target word (as if he's the only one learning new?)

### Analysis
<img width="869" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/54c5543d-f8ea-46a4-b536-a71ee880a5cb">


Badly created datasets
<img width="396" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/01d2b1f5-ea7f-4bee-ae0c-071e0e6438a0">
