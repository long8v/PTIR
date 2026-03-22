---
title: "Estimating and Evaluating Regression Predictive Uncertainty in Deep Object Detectors"
date: 2022-11-24
tags: ['2021Q1', 'ICLR', 'object detection', 'uncertainty', 'later..']
paper: "https://arxiv.org/pdf/2101.05036.pdf"
issue: 91
issueUrl: "https://github.com/long8v/PTIR/issues/91"
summary: "New evaluation suggestions"
---
<img width="719" alt="image" src="https://user-images.githubusercontent.com/46675408/203697708-fc898062-bb5b-41e4-9a1b-2c51223d6ab3.png">

[paper](https://arxiv.org/pdf/2101.05036.pdf), [code](https://github.com/asharakeh/probdet)

## TL;DR
- **task :** probabilistic object detection
- **problem :** bbox prediction distribution based on NLL loss tends to have high entropy regardless of whether the bbox is correct.
- **idea :** use energy score instead of NLL loss -> lower entropy, better calibrated
- **architecture :** RetinaNet, Faster-RCNN, DETR
- **objective :** Energy Score
- **baseline :** NLL loss, Direct Moment Matching(DMM)
- **data :** COCO, Open Images
- **evaluation :** Proposed a new metric to replace mAP. False positive if IoU<0.1 among GT matched bboxes, localization error if 0.1 ~ 0.5, and if there are multiple GT matched bboxes above 0.5, the highest class score is true positive, and the rest are separated into duplicates. Like mAP, the average value is obtained by thesholding from 0.5 ~ 0.95. Mean Calibration Error (MCE) and regression Calibration Error (CE) are also obtained.
- **result :** better calibrated, lower entropy, higher quality predictive distribution
- **contribution :** Propose a new evaluation
- **limitation or something I don't understand :** local-rule? non-local rule? entropy is bad if it's high...

## Details
### Preliminaries
- energy 
Calling E(x) energy when p(x) is proportional to exp(-E(x))
- scoring rule 
A function that measures how good a distribution that predicts a class or bounding box given a feature is given actual observed events.
- variance network 
https://github.com/long8v/PTIR/issues/92

### Negative Log Likelihood as a scoring rule
NLL under Multivariate Gaussian
<img width="587" alt="image" src="https://user-images.githubusercontent.com/46675408/203698706-aba9051b-6ff0-4de8-b437-58dc813b9f8e.png">

### Energy Score(ES)
<img width="495" alt="image" src="https://user-images.githubusercontent.com/46675408/203699940-1c942c10-7179-4223-92cb-81b572d88f84.png">

- $z_n$ : ground truth bounding box
- $z_{n,i}$ : $i^{th}$ samples drawn from $N(\mu(x_n, \theta), \sigma(x_n, \theta))$.

Monte Carlo can be approximated as follows
<img width="516" alt="image" src="https://user-images.githubusercontent.com/46675408/203699956-f00d1520-e287-45d3-a66d-b041bab68018.png">

### Direct Moment Matching
<img width="639" alt="image" src="https://user-images.githubusercontent.com/46675408/203699905-154ea553-33d3-4b35-90b9-3e671b3451c7.png">

### Motivation
<img width="697" alt="image" src="https://user-images.githubusercontent.com/46675408/203699994-8fa64d6f-95e1-4bf0-a9b5-8ae49309ec0e.png">

- NLL or energy score or the value at which the minimum is similar
- NLL and ES are opposite, with NLL penalizing more when entropy is low ($\sigma$ is low) and ES penalizing more when entropy is high.
- So NLL tends to learn high entropy whether bbox is correct or incorrect -> so why is that bad, I think I need to understand variance network.

### Results
<img width="707" alt="image" src="https://user-images.githubusercontent.com/46675408/203700347-9bbf9659-6f84-482f-ad89-6066f29e08dc.png">
