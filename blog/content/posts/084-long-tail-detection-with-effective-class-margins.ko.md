---
title: "[76] Long-tail Detection with Effective Class-Margins"
date: 2022-11-08
tags: ['2022Q3', 'imbalance', 'ECCV']
paper: "https://www.ecva.net/papers/eccv_2022/papers_ECCV/papers/136680684.pdf"
issue: 84
issueUrl: "https://github.com/long8v/PTIR/issues/84"
---
<img width="649" alt="image" src="https://user-images.githubusercontent.com/46675408/200503141-76c3e6e3-39a1-4df8-b1a6-23b3ac74ed41.png">

[paper](https://www.ecva.net/papers/eccv_2022/papers_ECCV/papers/136680684.pdf), [code](https://github.com/janghyuncho/ECM-Loss)

## TL;DR
- **task :** long-tail object detection 
- **problem :** COCO 데이터는 long-tail로 annotation 되어있고 그에 맞게 학습하는데 평가 metric인 mAP는 AUC여서 간극이 있음 
- **idea :** mAP를 probabilistic하게 바꾸고 이를 detection에서의 class-margin bounds 하의 pairwise ranking error(=negative sample x'가 positive x 보다 더 높게 rank 되는 frequency를 측정)의 weighted version으로 bound해서 이를 최적화. 
- **architecture :** Mask R-CNN, Cascade Mask R-CNN
- **objective :** ECM loss
- **baseline :** CE Loss, Federated Loss, Seesaw Loss, LOCE loss
- **data :** LVIS v1, Open Images
- **result :** SOTA
- **contribution :** no hyper-parameter for long-tail problem
- **limitation or 이해 안되는 부분 :** 수식식을 다 이해하진 못함. duplicate object에 대한 penalty 효과가 없다고 함. DETR류에는 못 쓰이려나?

## Details
### related work
#### Long-tail Detection related work
- 대부분의 선행 연구가 loss를 implicit/explicit 하게 re-weighting하는 접근법. 
- Equalization loss : rare class의 negative gradient를 제거하는 방식
  - 다른 클래스들의 negative gradient들에 의해 rare한 class가 discourage 된다는 가정
- Balanced Group Softmax(BaGS) : training set에 나온 빈도별로 group을 나누고 거기서 softmax + cross-entropy 구함 
- federated loss : 이미지에서 나온 class의 negative gradient만 계산함 
- Equalization Loss V2 : 클래스별로 positive / negative의 누적 비율을 맞추려고 함
- SeeSaw loss : rare class의 negative gradient에 대한 weight를 frequency가 높으면 줄여줌

#### Learning with class-margins
- face-recognition 같은데 많이 쓰인다고 하넹 
- [Learning Imbalanced Datasets with Label-Distribution-Aware Margin Loss](https://arxiv.org/pdf/1906.07413.pdf)

### 주요 전개
- preliminary:  class-margin bound
<img width="377" alt="image" src="https://user-images.githubusercontent.com/46675408/200532714-e033a452-6192-4700-b942-44e0e24b1477.png">

그냥 class loss 구하는 것보다 margin으로 class loss 구하는게 더 loss가 작다는 뜻인듯? 이 수식은 다른 페이퍼에서 증명됨

- Decision Metrics : mAP
<img width="434" alt="image" src="https://user-images.githubusercontent.com/46675408/200532775-dadd1d09-ff25-4266-b6d4-30c74954cf0d.png">

이를 probabilistic하게 바꾸면 아래와 같이 바꿀 수 있음 
<img width="416" alt="image" src="https://user-images.githubusercontent.com/46675408/200533031-5ba032e3-a9c1-4159-a1e1-4dd0c71769b1.png">

이는 class margin bound를 가진 weighted pair-wise ranking error로 bound될 수 있음 
<img width="314" alt="image" src="https://user-images.githubusercontent.com/46675408/200535069-41d3ad42-e005-4846-a614-29a4af09703a.png">

이때 pair-wise ranking error는 negative sample x'가 positive sample x보다 더 높게 rank 되는 frequency 

여기서 ranking loss는 또  threshold를 추가한 binary error로 bound될 수 있음
<img width="310" alt="image" src="https://user-images.githubusercontent.com/46675408/200533923-2eb6f571-b3aa-4be8-b05c-54f56feaa8db.png">

이 식을 어떻게 정리하다보면.. 위의 class-margin bound와 함께 결합하면 가장 tight한 margin을 구할 수 있음
<img width="281" alt="image" src="https://user-images.githubusercontent.com/46675408/200534935-01abcad0-cbf0-47f1-8aa7-2e89981120ee.png">

이를 다시 정리하면, 우리는 margin-based error를 최소화 하고 싶은데 이는 threshold가 0.5가 아닌 margin이 되는 sigmoid를 적용하는 것이고 
<img width="386" alt="image" src="https://user-images.githubusercontent.com/46675408/200534048-4130b117-c996-44d6-bf73-f7c05c927f0b.png">

- 여기서 $m_c$는 ranking error를 bounding 하기 위한 값인데 역시 이도 bound로 표현됨
<img width="487" alt="image" src="https://user-images.githubusercontent.com/46675408/200537875-26ccbb79-b413-455a-9394-a2d701248c59.png">

이때 score function은 가장 tight한 margin으로 weighted sum된 형태임
<img width="355" alt="image" src="https://user-images.githubusercontent.com/46675408/200536374-67c2f07e-25af-46f3-be4a-af8d0273dfeb.png">

### Results
<img width="496" alt="image" src="https://user-images.githubusercontent.com/46675408/200537919-471e9f24-7051-49b9-9bf4-f59ba5ab4afa.png">
