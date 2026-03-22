---
title: "[160] ALOHa: A New Measure for Hallucination in Captioning Models"
date: 2024-06-15
tags: ['evaluation', '2024Q2', 'NAACL']
paper: "https://arxiv.org/pdf/2404.02904"
issue: 179
issueUrl: "https://github.com/long8v/PTIR/issues/179"
summary: "Personal research Very related research - Proposed pipeline for captioning models for object hallucination"
---
![image](https://github.com/long8v/PTIR/assets/46675408/2eae7a2a-e566-4f78-bda7-fbd82a381126)

[paper](https://arxiv.org/pdf/2404.02904), [code](https://github.com/DavidMChan/aloha)

## TL;DR
- **I read this because.. :** Personal research Very relevant research
- **task :** object hallucination evaluation
- **problem :** The existing CHAIR for measuring hallucination relies on string matching and is limited to COCO objects.
- **idea :** Parsing with LLM, object extraction with DETR, bipartite matching with semantic similarity with S-BERT
- **input/output :** {image, text} -> score (higher is better)
- **baseline :** CHAIR, CLIPScore, RefCLIPScore
- **data :** FOIL, noCaps-FOIL(proposed), HAT(proposed)  
- **evaluation :** AP for task 1, LA for task 2(accuracy)
- **result :** Average Precision performs similar to RefCLIPScore, Localization Accuracy performs similar to CHAIRs but superior to noCaps-FOIL.
- **contribution :** Proposed a pipeline for a captioning model for object hallucinations.
- **etc. :** It's good to see that the limitations are not hidden, and it's good to see that you have created data to show the advantages of the proposed method.

## Details
### motivation
![image](https://github.com/long8v/PTIR/assets/46675408/0d327e2f-ec8f-4860-9a57-6e9ba8722374)

### overall pipeline
![image](https://github.com/long8v/PTIR/assets/46675408/163814a2-1d7e-4f2d-865f-5b6332a1327f)

(1) Extracting objects from candidates, references, and images
- GT Candidates
- DETRs trained with COCO -> object candidates
- Pulled object parsing from referecne caption using ChatGPT
- We also want to pull attributes at the same time
- Singularization (minus s)
- predicted 
- Parsing as LLM as in candidata catpion
  
(2) Object Filtering 
- Sometimes the caption model is uncertain and the caption is written like `fork or knife`.
- In this case, subtract from the candidate caption's class set (but not from referecne)
- Use spaCy to leave only the noun in a referecne noun phrase.
 
(3) Object matching 
Using SBERT for bipartite matching

The final metric is "least matching similarity", as shown below.
![image](https://github.com/long8v/PTIR/assets/46675408/fb1608e8-8f1c-42b6-81b7-f3a4ca7dba77)

### Result
##### HAT
![image](https://github.com/long8v/PTIR/assets/46675408/c96c33b4-1120-473f-b2d6-c28b219e6dcf)

HAT is created directly for COCO images. (TEST 400)
Where CHAIRs is accuracy (can we put AP and accuracy in the same table?)

#### FOIL
![image](https://github.com/long8v/PTIR/assets/46675408/28413040-74f1-405d-91c8-669003ef00d5)

Perform well on no-caps
The baseline here is 50, so I'm not sure if I'm measuring the two comparatively like I would in CLIPScore. If so, I'm not sure if it would be called AP instead of accuracy.

#### Qualitative
![image](https://github.com/long8v/PTIR/assets/46675408/8bdd3c05-2c60-401f-a3af-6a4cea819431)

##### Ablation
![image](https://github.com/long8v/PTIR/assets/46675408/1b451ca5-a034-4750-b77f-d96fecd2809c)
