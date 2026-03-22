---
title: "Mismatch Quest: Visual and Textual Feedback for Image-Text Misalignment"
date: 2024-04-03
tags: ['google', 'XAI', 'evaluation', '2024Q2']
paper: "https://arxiv.org/pdf/2312.03766.pdf"
issue: 169
issueUrl: "https://github.com/long8v/PTIR/issues/169"
summary: "Personal research related. Ride on DSG - the study I wanted! Dataset release!"
---
<img width="1612" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/dcef1f5b-0a5f-4199-9d53-5ab08cd0967c">

[paper](https://arxiv.org/pdf/2312.03766.pdf), [page](https://mismatch-quest.github.io/), [dataset](https://huggingface.co/datasets/mismatch-quest/SeeTRUE-Feedback)

## TL;DR
- **I read this because.. :** Personal research related. Ride from DSG
- **task :** image / text alignment with score!
- **problem :** The existing methodology for measuring alignment does not come with an explanation.
- Idea:** Create data and benchmarks
- **input/output :** {image, text} -> score, misaligned text span, misaligned visual span, feedback
- **objective :** zs or CE loss 
- **baseline :** PALI, mPLUG-Owl, miniGPT-2, LLaVA1.5, finetuned PALI
- **data :** proposed TV Feedback // test is AMT to human refinement.
- **evaluation :** binary accuracy (is it an exact pair), text span (precision, not sure if it's an exact match or not), feedback is NLI (using BART-NLI model), IoU .75
- **Result :** Confirmed that finetune PALI performed the best and works well on the ood dataset
- **contribution :** The research I wanted! Dataset released!
- **etc. :**

## Details
<img width="366" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8fc818e1-1ef9-4671-9fd5-345becd263c6">


<img width="1353" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e02cdfc6-0e5b-4582-b213-65b4dc012a06">

<img width="1419" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/11b51f6d-2451-42b0-8cd3-ab434c54dd39">

### Image source
<img width="736" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/683beef9-8301-4a2f-8c7c-0698d9875ed1">

### Proposed ConGen 
- 1) Spcay picked POS. Divide into 4 categories: object(noun), attribute(adjective), action(verb), and spatial relations.
- 2) Using PaLM2, ask students to (a) create a contradiction caption, (b) create a caption detailing why it is a contradiction, (c) pinpoint which element within the caption is incorrect, and (d) draw a visual bounding box.
- 3) To distinguish if the generated contradiction caption is indeed different from the original caption, we use the Textual Entailment model to determine whether the
- 4) Use GroundingDINO to ground the textual label and bounding box of the bounding box drawn by PALM2
We'll call this set the Textual Visual Feedback data.

### SeeTrue-Feedback benchmark
Based on the SeeTrue dataset, 2008 samples were drawn in a similar fashion to ConGen above, burned on an AMT, and human reviewed.

<img width="369" alt="image" src="https://github.com/user-attachments/assets/8b7f7a3e-af69-43cc-ad8b-f9074d09743d">

### Evaluation metrics
- Image-text Alignment : binary accuracy
- Textual Feeback Quality: BART NLI with gt is premise, prediction is hypothesis
- Misalignment in text: Use BART NLI to check if text segments are aligned (similar to above, right?)
- Visual Misalignment Detection: Jam with F1-Score@0.75
Alignment is included in the 8100 SeeTRUE dataset and the other metrics are included in SeeTrue-Feedback.

<img width="511" alt="image" src="https://github.com/user-attachments/assets/ff8cba95-322e-4f47-a5ef-98bcfa6bc853">


### Result
Ask the latest VLM models the following query
<img width="375" alt="image" src="https://github.com/user-attachments/assets/5b3edaa8-abcd-485e-9edc-cdda3bb7d3bc">

<img width="387" alt="image" src="https://github.com/user-attachments/assets/16fbb984-4817-4ddc-a947-4585b993f910">

<img width="759" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6fb5ac36-1487-4553-984b-a58f240e1d7c">

<img width="783" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a231293a-25fc-4ab0-befd-ee4f1d8828e2">

## limitation of model prediction 
<img width="396" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3d9c5be3-c420-424b-9149-423ce2e4f5e2">

- Difficulty giving visual feedback for the absence of images
- Difficult to give feedback when there are multiple misalignments
- Bounding box is too loose