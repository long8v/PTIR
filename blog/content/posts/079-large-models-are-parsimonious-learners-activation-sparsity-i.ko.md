---
title: "[71] Large Models are Parsimonious Learners: Activation Sparsity in Trained Transformers"
date: 2022-10-17
tags: ['25min', 'sparse', '2022Q4', 'transformer']
paper: "https://arxiv.org/pdf/2210.06313.pdf"
issue: 79
issueUrl: "https://github.com/long8v/PTIR/issues/79"
---
<img width="800" alt="image" src="https://user-images.githubusercontent.com/46675408/196067709-544bd5dc-df20-4649-aa43-24622af55f7f.png">

[paper](https://arxiv.org/pdf/2210.06313.pdf)

## TL;DR
- **task :** transformer가 얼마나 sparse한지, 어떤 상황일 때 sparse한지 살펴보자
- **architecture :** T5, ViT-B16
- **data :** C4, ImageNet-21K
- **contribution :** transformer의 sparsity 측정

## Details
- ViT, T5 encoder decoder 상관없이 sparsity가 높음 첫 레이어말고는 다 10%내외.
<img width="975" alt="image" src="https://user-images.githubusercontent.com/46675408/196067945-eb992f53-f641-4aae-bb14-3055e95b105c.png">

이는 몇몇 neuron들이 활성화되지 않았기 때문이 아님을 보임. 뉴런들이 활성화될 확률은 아래와 같았음
<img width="356" alt="image" src="https://user-images.githubusercontent.com/46675408/196067989-f122a952-5cc6-404a-b738-b892b097b22e.png">

- 레이어가 더 깊을수록, 넓을 수록 sparsity가 높아짐.
<img width="985" alt="image" src="https://user-images.githubusercontent.com/46675408/196068023-db5ba729-df52-49dd-ac57-e12588fbf3f2.png">

- 1) label에 human annotation bias가 있어서인지? 2) natural image에 bias가 있어서 인지? 3) 모델이 데이터보다 capacity 높아서인지?
<img width="969" alt="image" src="https://user-images.githubusercontent.com/46675408/196068054-71c6b163-fff7-4f55-a38b-2bf856deb18f.png">

위의 세가지를 확인하기 위해 1) label을 random으로 만들고 2) 이미지를 random으로 주고 3) 데이터를 무한대로 만들었을때의 sparsity는 눈에띄게 변화하지 않았음. 즉 sparsity는 transformer가 내재하고 있는 본성임.

- sparsity 덕분에 FLOP이 떨어짐
<img width="978" alt="image" src="https://user-images.githubusercontent.com/46675408/196068189-f0964861-614a-4a43-b6d4-c29480178442.png">

- sparsity를 top-K로 제한했을 때, 성능이 그냥 트랜스포머와 비슷하며 robustness와 confidence에 대한 성능이 좋아짐.
- 
<img width="1004" alt="image" src="https://user-images.githubusercontent.com/46675408/196068272-8a4a9bad-7a03-4bd2-8b09-657abb181043.png">

<img width="439" alt="image" src="https://user-images.githubusercontent.com/46675408/196068299-37487799-c4f2-43b9-aa29-a9a1e4ec1f1f.png">

ECE : expected calibration error. model prediction에 대한 확률과 실제 그 prediction이 맞았는지에 대한 차이



