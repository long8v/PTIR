---
title: "Pick-a-Pic: An Open Dataset of User Preferences for Text-to-Image Generation"
date: 2024-07-24
tags: ['NeurIPS', '2023Q4', 'generation']
paper: "https://arxiv.org/abs/2305.01569"
issue: 186
issueUrl: "https://github.com/long8v/PTIR/issues/186"
summary: "Research on personalized research - huge data release. Open models. Show performance improvements with it."
---
<img width="600" alt="image" src="https://github.com/user-attachments/assets/8768df02-a494-4fcf-93d9-a93551780612">

[paper](https://arxiv.org/abs/2305.01569), [code](https://github.com/yuvalkirstain/PickScore), [dataset](https://huggingface.co/datasets/yuvalkirstain/pickapic_v1)

## TL;DR
- **I read this because.. :** Personal Research Related Research
- **task :** Learn human preference for T2I generation product
- Problem :** Measuring with FIDs is not a good representation of human preference. We need an open source preference dataset.
- Idea :** Create a webpage to collect human preference data
- **input/output :** {image, prompt} -> score
- **architecture :** ViT-H/14 
- **objective :** KL divergence
- **baseline :** Aesthetic score, CLIP-H, ImageReward, HPS, Human Expert
- **data :** Pick-a-Pic data (data used in the paper is 583K of training / 500 / 500 valid and test samples)
- **evaluation :** prefers to report that the difference in scores is above a threshold. spearman correlation with human expert
- **result :** Highest accuracy, correlation. I preferred this to the Classifier-free guidance technique.
- **contribution :** Huge data release. Release the model. Disclose performance improvements with it.
- **etc. :** The neurips paper seems to have a lot of data disclosure.

## Details
<img width="1109" alt="image" src="https://github.com/user-attachments/assets/bfaf0266-b1de-44c8-8835-a56427c91ae4">

## annotation 
<img width="1117" alt="image" src="https://github.com/user-attachments/assets/dfe4f6a3-99f8-4e56-a347-f1e321aa8091">

- prompt is entered by the user
- Image generation is supported by Stable Diffusion 2.1, Dreamlike Photoreal 2.0, and Stable Diffusion XL variants

## Pick-a-Pic Dataset
- Total 968K ranking
- The paper used 583K rankings from 37K prompts and 4K users
- Doing a lot of things to care about data quality (email verification, bot detection...)

## PickScore
- CLIP
<img width="455" alt="image" src="https://github.com/user-attachments/assets/d331a788-3465-4ce6-a580-5c459036e1a4">

- finetuning loss
<img width="533" alt="image" src="https://github.com/user-attachments/assets/0b4ca9fe-c89b-417a-bbdc-be97c3f0497e">

$s$ : score
$x$ : prompt
$y_1, y_2$: image

They tried in-batch negatives, but they didn't perform well.
trainingdms 4000 step, lr 3e-6, bs 128, warmup 500 step
8 Reportedly took less than an hour with the A100.

## Result
- rerank vis CLIP-H vs Pick-a-Pic 
<img width="625" alt="image" src="https://github.com/user-attachments/assets/b594cda2-949c-41aa-8855-4c7c6e35fa71">

- accuracy
<img width="461" alt="image" src="https://github.com/user-attachments/assets/eff4e752-773e-4f19-ae3c-56919c906fa7">

- What we learned with classifier-free guidance
<img width="671" alt="image" src="https://github.com/user-attachments/assets/4310a8df-0128-45c9-86e2-21204ab065cd">

- correlation between human expert 
<img width="433" alt="image" src="https://github.com/user-attachments/assets/206c0c4e-b631-4911-9a1a-5b621b4cb876">

- Comparison to other models
<img width="1087" alt="image" src="https://github.com/user-attachments/assets/f6ab52e2-90e5-42f1-a753-518ccc6d8f16">

- why not COCO?
Image creation with COCO prompts is still the most popular way to generate images
COCO uses a generic object, which is not what you want.
<img width="1100" alt="image" src="https://github.com/user-attachments/assets/81a06a24-7706-46ed-972d-0baa4cacbfbd">

- Just generated vs. reranked with PickScore
<img width="1103" alt="image" src="https://github.com/user-attachments/assets/cfa74189-9351-4546-b0e0-3e7636acc9f1">

