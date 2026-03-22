---
title: "Robust fine-tuning of zero-shot models"
date: 2023-07-05
tags: ['openAI', 'google', 'CVPR', '2022Q3', 'CLIP', 'domainshift']
paper: "https://arxiv.org/abs/2109.01903"
issue: 134
issueUrl: "https://github.com/long8v/PTIR/issues/134"
summary: "CLIP A method for learning conservatively without losing pretrained abilities. Looking for a paper on LiT and found it - simple idea + easy to implement, yet performs well."
---
<img width="879" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1ed148a8-bf85-445b-a25f-30dfaeec5199">

[paper](https://arxiv.org/abs/2109.01903)

## TL;DR
- **I read this because.. :** CLIP A way to learn conservatively without losing pretrained abilities. LiT related articles found while searching
- **task :** CLIP 
- **problem :** When CLIP finetunes for a reference domain, CLIP may lose knowledge of the general domain that it was originally trained on.
- **idea :** Ensemble CLIP zero-shot capabilities with a model finetuned to the target domain -> ensemble via weight interpolate!
- **input/output :** {image, text} -> score
- **architecture :** CLIP, ViT, BASIC-L
- **objective :** InfoNCE
- **baseline :** zs-CLIP, finetuned CLIP. 
- **data :** WIT(clip), JFT-300M(vit) -> ImageNet, ImageNetV2, ImageNet-R, ImageNet sketch, ObjectNet, ImageNet-A
- **evaluation :** Accuracy in the original domain and the shifted domain.
- **Result :** Improved performance for kids with domain shifts while maintaining ImageNet performance.
- **contribution :** simple idea + easy to implement, yet performs well
- **etc. :** 

## Details
### Related work 
- Stochastic Weight Averaging
https://arxiv.org/pdf/1803.05407.pdf

<img width="478" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e3f652c4-751c-4d6e-9e21-0746e7e1c53e">

Using a moving average of params has some sort of ensemble effect


## domain shift data
<img width="974" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/baf58cdc-073a-4335-8113-9fbe385dd3be">


## Weight-space ensemble for finetuning
So simple...
1) Take a pretrianed CLIP and do ft. fully ft(end-to-end) for target domaind or just the last classifier(LC)
2) Average each element-wise with mixing coefficient
<img width="313" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/60c60d4d-c6b2-4ad1-8fd3-23c900554f21">

Here, alpha should be found greedily, but I set it to 0.5 and it came out pretty close to optimum.

## Result
<img width="870" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/61e9a158-4897-44be-bf5e-0bf037f3322f">

First figure: Datasets with ImageNet (reference distribution) on x-axis and distribution shift on y-axis
Purple is zs clip performance, blue is just training with that data. Orange are the ones we finetuned with that data.
Second figure: Wise-FT increases performance for kids with distribution shifts without reducing reference accuracy

<img width="971" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f317d422-5a28-4ba1-babb-85d35507bca1">

If you look at the finetuned ones, the ones with distribution shift are not performing as well.
The proposed WISE-FT shows better performance than ft even in the reference domain (86.2 -> 87.1), and the kids with distribution shift are also better.

<img width="963" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0fbc55c9-1d84-4ae1-8952-bf069ac2e40f">

clip itself tends to have too much performance wiggle room depending on hparam -> weight-space ensemble makes frontier!

<img width="949" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/157c5619-7883-4b30-a611-d409632ec457">

Better performance than finetuning for each domain!

## Analysis 

<img width="973" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/db5d3e79-b814-4d7c-8b73-ee4b4649ab7b">

zero-shot and linear classifier had different trends, and linear-classifier had similar trends.  -> there seemed to be a larger ensemble effect

<img width="988" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5923e0fb-0553-4a4b-9c30-00ff7b266457">

Ensembling weights rather than ensembling outputs was a better performance improvement!
