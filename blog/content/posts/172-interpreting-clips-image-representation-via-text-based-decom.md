---
title: "Interpreting CLIP's Image Representation via Text-Based Decomposition"
date: 2024-05-06
tags: ['ICLR', 'CLIP', 'XAI', '2023Q4']
paper: "https://arxiv.org/abs/2310.05916"
issue: 172
issueUrl: "https://github.com/long8v/PTIR/issues/172"
summary: "CLIP spurious cues - Proposed algorithm to describe each representation of CLIP as text."
---

<img width="590" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/71414178-f410-4c7b-8d37-44ddca680009">

a.k.a TextSpan
[paper](https://arxiv.org/abs/2310.05916), [code](https://github.com/yossigandelsman/clip_text_span) 

## TL;DR
- **I read this because.. :** Came across this while searching for CLIP spurious cues
- **task :** Extract text representation of layer, head in CLIP ViT
- **idea :** create 3948 common expression sentences with human + GPT, then pick the row with the highest variance from the image expression and add it to the projection.
- **input/output :** {image, model} -> text explanation of ViT layer and heads
- **architecture :** ViT-B-16, ViT-L-14, ViT-H-14
- **baseline :** LRP, Partial-LRP, rollout, raw attention, GradCAM, Chefer2021
- **data :** ImageNet(mean ablation), Waterbirds dataset(reducing spurious cues), ImageNet-Segmentation(zs-segmentation)
- **evaluation :** accuracy(imagenet), worst-group accuracy(waterbird), pixel accuracy/mIoU/mAP (zs-segmenatation)
- **result :** Only the last 4 MSA layers affect the final prediction, other layers have little effect, qualitatively very interesting result, sota in zs-segmentation
- **contribution :** Proposed an algorithm to describe each representation of CLIP as text.
- **etc. :**

## Details
### related work 
- Multimodal neurons in artificial neural networks https://openai.com/index/multimodal-neurons
- Thesis that CLIP's layer-by-layer, head-by-head trained representation is highly interpretable
- Disentangling visual and written concepts in CLIP
- A paper that utilizes the above methodology to write and erase text to represent images.

  
### Preliminary findings
<img width="559" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3f6a8f49-ad97-4738-a368-276fd40b0a67">

Only the MSAs in the last 4 layers affected performance, and mean ablating the MLP or earlier MSA layers did not have a significant impact on performance.

### Decomposition to head
<img width="459" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7a531747-1ddf-4856-a8ed-67e627cabce6">

MSA can be expressed as above $\alpha$ is the attention score

<img width="500" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/033cd112-9154-4ecb-8719-5db617a102fe">

If we include the projection $P$, we get the expression above.
This means that you can get a representation of each layer, head, patch, etc. by summing the projection and attention operations $c_{i, j, h}$ for each layer, head, patch, etc.

### TextSpan algorithm
<img width="754" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/90028fb9-3c34-4541-8ef7-248c89dc28dc">

It looks complicated, but it's not
- Matrix-multiply the attention output $C\in\mathbb{R}${K\times d'}$ and the text representation $R\in\mathbb{R}^{M\times d'}$ by layer, head, and then find the representation j with the highest variance and add this $\tau$ to the projection. Then update C and R with this representation so that it is orthogonal to the following representation (similar to PCA)

These are the layer/head specific expressions
<img width="728" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c816c812-e1ce-4c34-9454-2d3d230a8f49">

## Result
### Quantitative 
<img width="733" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/81595935-8f36-4140-87ad-f94346fcf5bc">

### Qualitative
<img width="766" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/dc248018-e6e7-422d-98ff-6d0b24cbc4bf">

<img width="774" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b54d5729-caf0-4b6f-8312-2db74b512310">

<img width="761" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/af75eefa-ca97-4ec8-b9f9-f48e87562eba">
