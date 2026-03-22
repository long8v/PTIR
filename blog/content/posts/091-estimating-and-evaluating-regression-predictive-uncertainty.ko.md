---
title: "[82] Estimating and Evaluating Regression Predictive Uncertainty in Deep Object Detectors"
date: 2022-11-24
tags: ['2021Q1', 'ICLR', 'object detection', 'uncertainty', 'later..']
paper: "https://arxiv.org/pdf/2101.05036.pdf"
issue: 91
issueUrl: "https://github.com/long8v/PTIR/issues/91"
---
<img width="719" alt="image" src="https://user-images.githubusercontent.com/46675408/203697708-fc898062-bb5b-41e4-9a1b-2c51223d6ab3.png">

[paper](https://arxiv.org/pdf/2101.05036.pdf), [code](https://github.com/asharakeh/probdet)

## TL;DR
- **task :** probabilistic object detection
- **problem :** NLL loss에 기반한 bbox prediction distribution은 bbox가 맞는지와는 관계없이 높은 entropy를 갖는 경향성
- **idea :** NLL loss 대신에 energy score를 사용하자 -> lower entropy, better calibrated 
- **architecture :** RetinaNet, Faster-RCNN, DETR
- **objective :** Energy Score
- **baseline :** NLL loss, Direct Moment Matching(DMM)
- **data :** COCO, Open Images
- **evaluation :** mAP를 대체하는 새로운 metric 제안. GT 매칭 된 bbox 들 중 IoU<0.1이면 False Positive, 0.1 ~ 0.5이면 localization error, 0.5 이상인데 GT와 매칭된게 여러개면 class score 제일 높은걸 True Positive, 나머지를 Duplicate로 분리. mAP처럼 0.5 ~ 0.95로 thesholding해서 평균값 구함. Mean Calibration Error(MCE), regression Calibration Error(CE)도 구함. 
- **result :** better calibrated, lower entropy, higher quality predictive distribution
- **contribution :** 새로운 evaluation 제안
- **limitation or 이해 안되는 부분 :** local-rule? non-local rule? entropy가 높으면 안좋은건가.. 

## Details
### Preliminaries
- energy 
p(x)가 exp(-E(x))에 비례한다고 할 때 E(x)를 energy라 부름
- scoring rule 
feature가 주어졌을 때 class 또는 bounding box를 예측하는 분포가 실제 관측된 사건이 주어졌을 때 얼마나 좋은지를 측정하는 함수
- variance network 
https://github.com/long8v/PTIR/issues/92

### Negative Log Likelihood as a scoring rule
Multivariate Gaussian 하에서 NLL
<img width="587" alt="image" src="https://user-images.githubusercontent.com/46675408/203698706-aba9051b-6ff0-4de8-b437-58dc813b9f8e.png">

### Energy Score(ES)
<img width="495" alt="image" src="https://user-images.githubusercontent.com/46675408/203699940-1c942c10-7179-4223-92cb-81b572d88f84.png">

- $z_n$ : ground truth bounding box
- $z_{n,i}$ : $N(\mu(x_n, \theta), \sigma(x_n, \theta))$에서 뽑은 $i^{th}$ 샘플 

Monte Carlo로 아래와 같이 근사할 수 있음
<img width="516" alt="image" src="https://user-images.githubusercontent.com/46675408/203699956-f00d1520-e287-45d3-a66d-b041bab68018.png">

### Direct Moment Matching
<img width="639" alt="image" src="https://user-images.githubusercontent.com/46675408/203699905-154ea553-33d3-4b35-90b9-3e671b3451c7.png">

### Motivation
<img width="697" alt="image" src="https://user-images.githubusercontent.com/46675408/203699994-8fa64d6f-95e1-4bf0-a9b5-8ae49309ec0e.png">

- NLL이나 energy score이나 최소점이 되는 값이 비슷 
- NLL과 ES가 반대방향인데 NLL은 entropy가 낮을 때( $\sigma$ 가 낮을 때) 더 penalty를 많이 주고 ES는 더 높을 때 penalty를 많이 줌
- 그래서 NLL이 bbox가 맞던 틀리던 entropy가 높게 학습되는 경향성이 있음 -> 그래서 그게 왜 안좋은건지는 variance network를 이해해야될 듯..

### Results
<img width="707" alt="image" src="https://user-images.githubusercontent.com/46675408/203700347-9bbf9659-6f84-482f-ad89-6066f29e08dc.png">
