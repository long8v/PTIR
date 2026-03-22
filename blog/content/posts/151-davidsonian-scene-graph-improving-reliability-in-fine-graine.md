---
title: "[139] Davidsonian Scene Graph: Improving Reliability in Fine-Grained Evaluation for Text-to-Image Generation"
date: 2023-12-11
tags: ['google', '2023Q4', 'evaluation', 'generation']
paper: "https://google.github.io/dsg/"
issue: 151
issueUrl: "https://github.com/long8v/PTIR/issues/151"
summary: "I saw it on Facebook and thought, \"Can we apply it to CLIP evaluation? and read - Improving QG/A-based evaluation by making fine-grained evaluation more interpretable"
---
<img width="674" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d332ba46-bb1a-4872-8254-e92986331d22">

[paper](https://google.github.io/dsg/), [code](https://github.com/j-min/DSG)

## TL;DR
- **I read this because.. :** I saw it on Facebook and wondered if it could be applied to CLIP evaluation? and read
- **task :** evaluating faithfulness of image generation
- **problem :** CLIPScore is not consistent in scale and interpretable depending on the style, QG/QA based is difficult to interpret what is wrong (no door or no blue door) when it is a compound question (is there a blue door?) no, and there are errors in the VQA model itself, such as saying there is no door but there is a blue door when there are multiple questions.
- **idea :** Make each question atomic and graph them together so that if its parent is no, then all its children are no.
- **input/output :** image + text -> graph(questions for node, semantics for its dependancy)
- **baseline :** QA/QG 
- **data :** DSG-1k released with graph based on previous evaluation data such as [TIFA](https://arxiv.org/pdf/2303.11897.pdf). The way it was created is that the text corresponding to the image is 1) made into an entity tuple through LLM, 2) a question is created based on it, and 3) the depedancy of each tuple is also found.
- **evaluation :** Did you answer the question for each image?
- **result :** Seems to have solved the above problem. Among VLM models, PALI is the best performing
- **contribution :** Improved QG/A-based evaluation to make fine-grained evaluation more interpretable.
- And I was wondering, if you ask a kid like GPT4-V "is `<description>` well explained `<img>`?, what is wrong?" what would come up?

## Details
### QA/G based methodology
<img width="669" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f02bdc44-9980-4b2a-8155-bf200f82eee1">


### motivation
- problem of clip score 
<img width="669" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b3ee93d4-d6fb-40a8-90f3-b7c721416728">

- problem of QA/G method
<img width="697" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5778440b-0d2d-477e-8744-9f5ba58f9215">

### Proposed
<img width="657" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/500ee4ad-3912-4137-95af-b871d4416c0f">

### Dataset source
<img width="660" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/60fd4d0c-81e6-4890-bc35-d40ac98a85fb">

<img width="969" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c0d35249-ebfb-4391-a7f5-efe024945859">

It's a lot, but I don't have time... Goodbye.