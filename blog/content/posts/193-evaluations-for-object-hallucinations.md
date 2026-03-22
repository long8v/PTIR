---
title: "[174] Evaluations for Object Hallucinations "
date: 2024-09-02
tags: ['survey', 'evaluation', 'MLLM']
paper: ""
issue: 193
issueUrl: "https://github.com/long8v/PTIR/issues/193"
summary: ""
---
<img width="961" alt="image" src="https://github.com/user-attachments/assets/dab5544c-498b-4ef5-a9a3-e79a1c82ff7c">


## CHAIR (== Object HalBench)
[18'EMNLP] Object Hallucination in Image Captioning https://arxiv.org/abs/1809.02156
- COCO caption & semantic segmentation label -- Measure hallucination in captioning model using synonyms
- The denominator of CHAIR_i is the count of all objects mentioned // CHAIR_s is the count of sentences
- COCO karpathy / robust test set  
<img width="316" alt="image" src="https://github.com/user-attachments/assets/62d6208b-1b0e-4649-81c4-f99022a1c190">

- What we wanted to say in this paper is that even if captioning performance is high, such as CIDEr, the actual hallucination performance is not proportional to it.
- LVLM gives 8 prompts to make the descriptive statement created by RLHF-V, obtains the gt segment and CHAIR, and reports this to Object Halbench

## POPE
[24'EMNLP] Evaluating Object Hallucination in Large Vision-Language Models https://arxiv.org/pdf/2305.10355
- A paper measuring object hallucinations like the CHAIR above by bringing them into LVLM
<img width="367" alt="image" src="https://github.com/user-attachments/assets/f7aa2e0f-f8a0-4e4c-bcc8-ba43666207cb">

- But the performance is choppy depending on what you do with the prompt. And it requires a complex human parsing rule to pull the object and match it with the GT object
- So the suggestion was to use POPE
<img width="783" alt="image" src="https://github.com/user-attachments/assets/c6cd2e06-ca5c-46e5-8b28-ff6fdd526c4a">

- Instead of creating a caption and looking for hallucinated objects, create a question that can be answered with yes or no and use Measure
- gt labels enrich object pools by pulling in semantic labels like SEEM
- Create three negative sets here
  - random : random object class  
- popular : object class that appeared a lot in the training data
- adversarial: an object class that has emerged a lot, such as the current object
- The set you used created 500 subsets with at least 3 objects in COCO.
- The paper found that 1) object hallucinations, which were highly prevalent in COCO, and 2) object hallucinations, which were highly frequent in COCO, were severe.

<img width="646" alt="image" src="https://github.com/user-attachments/assets/807aa545-5c16-4f9e-b46c-98efef24f9bb">

## HallusionBench
[CVPR'24] HallusionBench: An Advanced Diagnostic Suite for Entangled Language Hallucination and Visual Illusion in Large Vision-Language Models https://arxiv.org/abs/2310.14566

## AMBER
[arxiv'24] AMBER: An LLM-free Multi-dimensional Benchmark for MLLMs Hallucination Evaluation
https://arxiv.org/abs/2311.07397

<img width="738" alt="image" src="https://github.com/user-attachments/assets/f072b352-e7e2-43b5-8564-04be806f6d9f">

![image](https://github.com/user-attachments/assets/56e7a701-6f17-42d3-8f82-663acaadd7bd)

![image](https://github.com/user-attachments/assets/837d6646-8446-4682-a718-ea83e8f7b0d4)


There are two 1) generative 2) discriminative
generative is designed for object existence, while discriminative can find objects, relations, and attributes
Annotate the image and all the object, attribute, and relation labels that appear on it beforehand, and then just set the discriminative to yes and no.
generative parse nouns for generated captions and then just pretend it's CHAIR.... Hmmm.