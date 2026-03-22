---
title: "[47] Recovering the Unbiased Scene Graphs from the Biased Ones"
date: 2022-08-05
tags: ['SGG', '25min', '2021Q3', 'imbalance']
paper: "https://arxiv.org/pdf/2107.02112v1.pdf"
issue: 53
issueUrl: "https://github.com/long8v/PTIR/issues/53"
---
![image](https://user-images.githubusercontent.com/46675408/182977423-ff4439ba-2b06-40f5-89c7-058e4b5a1004.png)

[paper](https://arxiv.org/pdf/2107.02112v1.pdf)

## TL;DR
- **task :** Scene Graph Generation
- **problem :** SGG 특성 상, unlabeled 데이터가 많고 특정 relation만 많이 등장하는 long tail distribution.
- **idea :** [Positive-Unlabeled Learning](https://dodonam.tistory.com/370) 관점으로 문제를 바라봐서 logit 값을 전체 클래스 레이블의 frequency로 나눠주자.
- **architecture :** object detector + GNN인듯?
- **objective :** cross entropy loss
- **baseline :** MOTIFS, ...
- **data :** Visual Genome, Visual Genome150
- **result :** 현재 VG150에 대해서 sgdet SOTA인 듯하다. 
- **contribution :** long-tail 문제를 해결
- **limitation or 이해 안되는 부분 :**

## Details
<img width="615" alt="image" src="https://user-images.githubusercontent.com/46675408/182978368-a2bdbdbd-1406-4746-bf91-f52d67377efc.png">

### Recovering the Unbiased Scene Graph
<img width="523" alt="image" src="https://user-images.githubusercontent.com/46675408/182980842-d955cef0-25a8-45bd-8b47-e15ffb4db486.png">

- s: labeled pred
- y : true pred
- r : target pred

unbiased probability 
<img width="357" alt="image" src="https://user-images.githubusercontent.com/46675408/182980885-acedbd82-7199-4840-8af8-c32658f6efd5.png">

이때 label되는 확률이 x에 독립적이라고 가정하면(Selected Completely at Random, SCAR)  아래와 같이 쓸 수 있음 
<img width="326" alt="image" src="https://user-images.githubusercontent.com/46675408/182980898-650b529c-6081-446c-9904-a1e7fb7be2ed.png">

p(s=r|y=r)은 결국 전체 클래스 r에 대해서 label된 example의 비율

### Dynamic Label Frequency Estimation
위의 p(s=r|y=r), 즉 label frequency에 대한 추정치를 구함.
<img width="517" alt="image" src="https://user-images.githubusercontent.com/46675408/182981725-3db13055-f3e4-425c-9fb4-e0111b8f8df4.png">

이 식이 유도된건 
![image](https://user-images.githubusercontent.com/46675408/182981942-34a99c05-cb17-47e2-9ab4-c973fb08969c.png)


결국 전체 데이터의 클래스별로 frequency 로 나눠주는거임 -.-

1) inference 전에 post-training estimation을 구하기 어렵고
2) SGDET의 경우에는 gt bbox가 없으니 valid한 example을 추정하기가 어려움. 

그래서 우리는 tail class에 대해 vaild한 example을 얻기 위해 data augmentation을 할거고, label frequency는 배치별로 추정을 할 것임. 
이러한 아이디어를 Dynamic Label Frequency Estimation(DLFE)라고 할 것임.
<img width="684" alt="image" src="https://user-images.githubusercontent.com/46675408/182981696-ea536cfd-96a4-48ee-92ee-77791c6a9fa6.png">


![image](https://user-images.githubusercontent.com/46675408/182977452-9e3e6f39-2137-4e0e-9c00-af1f773487bf.png)

![image](https://user-images.githubusercontent.com/46675408/182977574-55a1e9a6-0eee-426e-9365-cc63390bb1ee.png)
