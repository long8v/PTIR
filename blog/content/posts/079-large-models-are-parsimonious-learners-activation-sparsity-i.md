---
title: "Large Models are Parsimonious Learners: Activation Sparsity in Trained Transformers"
date: 2022-10-17
tags: ['25min', 'sparse', '2022Q4', 'transformer']
paper: "https://arxiv.org/pdf/2210.06313.pdf"
issue: 79
issueUrl: "https://github.com/long8v/PTIR/issues/79"
summary: "Measuring the sparsity of a transformer"
---
<img width="800" alt="image" src="https://user-images.githubusercontent.com/46675408/196067709-544bd5dc-df20-4649-aa43-24622af55f7f.png">

[paper](https://arxiv.org/pdf/2210.06313.pdf)

## TL;DR
- **task :** Let's see how sparse our transformer is and under what circumstances it is sparse
- **architecture :** T5, ViT-B16
- **data :** C4, ImageNet-21K
- **contribution :** measure sparsity of transformer

## Details
- ViT, T5 encoder decoder, sparsity is high regardless of the encoder decoder. All but the first layer are within 10%.
<img width="975" alt="image" src="https://user-images.githubusercontent.com/46675408/196067945-eb992f53-f641-4aae-bb14-3055e95b105c.png">

This shows that it is not because some neurons are not active. The probability of a neuron being active was
<img width="356" alt="image" src="https://user-images.githubusercontent.com/46675408/196067989-f122a952-5cc6-404a-b738-b892b097b22e.png">

- The deeper the layer, the wider it is, the higher the sparsity.
<img width="985" alt="image" src="https://user-images.githubusercontent.com/46675408/196068023-db5ba729-df52-49dd-ac57-e12588fbf3f2.png">

- 1) Is there a human annotation bias in the label? 2) Is it because the natural image has a bias? 3) Is it because the model has a higher capacity than the data?
<img width="969" alt="image" src="https://user-images.githubusercontent.com/46675408/196068054-71c6b163-fff7-4f55-a38b-2bf856deb18f.png">

To verify the above three points, the sparsity did not change noticeably when we 1) randomized the labels, 2) randomized the images, and 3) made the data infinite, meaning that sparsity is an inherent property of transformers.

- FLOPs drop thanks to sparsity
<img width="978" alt="image" src="https://user-images.githubusercontent.com/46675408/196068189-f0964861-614a-4a43-b6d4-c29480178442.png">

- When limiting sparsity to top-K, performance is just like Transformer, with better performance for robustness and confidence.
- 
<img width="1004" alt="image" src="https://user-images.githubusercontent.com/46675408/196068272-8a4a9bad-7a03-4bd2-8b09-657abb181043.png">

<img width="439" alt="image" src="https://user-images.githubusercontent.com/46675408/196068299-37487799-c4f2-43b9-aa29-a9a1e4ec1f1f.png">

ECE: expected calibration error. The difference between the probability of a model prediction and whether that prediction was actually correct.



