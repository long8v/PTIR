---
title: "Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization"
date: 2024-02-13
tags: ['2016', '25min', 'XAI']
paper: "https://arxiv.org/pdf/1610.02391.pdf"
issue: 162
issueUrl: "https://github.com/long8v/PTIR/issues/162"
summary: "I read it as shouldn't I know if I explain - simple idea, no performance penalty, de-facto method"
---
<img width="698" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9640ec2a-b398-4d05-a803-1b6bc84a2eca">

[paper](https://arxiv.org/pdf/1610.02391.pdf)

## TL;DR
- **I read this because.. :** I read this because.. :** I thought I should know if I explain it.
- **task :** explainability in CNN
- **problem :** How do we attach an interpretable module that can be applied to any kind of CNN?
- **idea :** Differentiate the activation map $A^k$ of the convolution over the class $y^c$ we want to visualize, GAP it to get the importance, and then weighted sum $A^k$ + ReLU it.
- **input/output :** {image, class or caption or answer} -> activation map
- **architecture :** VGG-16, AlexNet, GoogleNet
- **objective :** X
- **baseline :** CAM, Guided-BackProp, c-MWP
- **data :** ILSVRC-15, PASCAL VOC 2007 
- **evaluation :** wsss, human evaluation, pointing game
- **result :** Good descriptive power without performance degradation (CAM is degraded). good seed in wsss. good visualization of adversarial samples. Get a human to look at activated kids and classify them (trustworthy), Guided-backprop or Deconv and ask human what's better?
- **contribution :** Simple idea, de-facto method with no performance penalty
- **etc. :** This is where the convention of not looking at negative gradients comes from. Read guided backprop and Network Dissection. The term "counterfactual explanation".

## Details
### proposed
<img width="691" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2e5b15ba-72c9-4539-a67c-a9bf6f01f1de">

Differentiate the logit (before softmax) $y^c$ for the class c we want to visualize with respect to the activation feature map $A_{ij}$.
We pool the global average over width, height (i, j) to get the importance.
<img width="263" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6d4c4e7a-f854-4557-b180-79f0ddf19571">

This is then weighted-summed back to the activation map and ReLU is taken, and the GradCAM
<img width="258" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ca8c4e19-7c43-4204-9f9c-1499df0604fb">

Use the conv feature map (14 x 14 size) from the last layer (using earlier layers doesn't perform very well)
The reason for using ReLU here is that the pixels that negatively affect it would be in a different category.
When ReLU was not applied, there were times when a class other than the desired class $y^c$ was activated and localization performance was poor.

- guided grad-cam
A 14 x 14 feature map can tell us that we're looking at something, but it doesn't give us a fine-grained explanation of why it's a "tiger cat".
So I used guided backpropagation (Striving for Simplicity: The All Convolutional Net, https://arxiv.org/abs/1412.6806) to multiply them together and visualize them. You can use Deconv, but experimentally guided backprop is better.
For the Guided backdrop, it says "negative gradients are supressed", let's read what it means.

- counterfactual explanation
<img width="229" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/95e59f8e-1fa5-4448-944c-2554aa3b2e1f">

<img width="341" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/728a6d0c-9497-441f-9622-1114f5610713">

Simply taking the negative of the gradient and then taking the ReLU (which would leave only negative activation) would be a counterfactual explanation. An explanation for why this pixel is not of this class!

### Result
- classification result  
<img width="359" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/79729cf1-7dff-4baa-ba64-2a01729ce126">


- result on captioning model
<img width="709" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b807afa7-ac8f-415f-9b57-27386e842b78">


- textual explanation on neuron
<img width="705" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/293b3d43-4c0a-4007-bbbc-bf000c2d3ee2">

Network Dissection: Quantifying Interpretability of Deep Visual Representations https://arxiv.org/abs/1704.05796 Read this

- result with adversarial noise
<img width="344" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ff46e451-1f66-45d1-b498-90a1c046190b">

An example where a slight perturbationd to the image predicts an airliner of 0.9999. But GradCAM works fine with this.
