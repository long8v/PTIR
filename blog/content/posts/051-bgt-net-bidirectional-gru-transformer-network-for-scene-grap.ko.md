---
title: "[45] BGT-Net: Bidirectional GRU Transformer Network for Scene Graph Generation"
date: 2022-08-03
tags: ['2021Q4', 'SGG', 'graph']
paper: "https://arxiv.org/pdf/2109.05346.pdf"
issue: 51
issueUrl: "https://github.com/long8v/PTIR/issues/51"
---
![image](https://user-images.githubusercontent.com/46675408/182501380-7d17e1f2-c3db-4ef8-bc05-5f4070b520ae.png)

[paper](https://arxiv.org/pdf/2109.05346.pdf)

## TL;DR
- **task :** two-stage SGG
- **problem :** object와 object 간의 관계를 잘 학습하자.
- **idea :** bi-GRU로 object 간의 communication을 하도록 하자.
- **architecture :** FasterRCNN으로 object 뽑고 visual / coordinate / class feature 뽑아서 bi-GRU에 넣음. 각 obj 별의 hidden output을 transformer encoder에 넣음. object들 n(n-1) pair에 대해 지지고 볶아서 relation 예측.
- **objective :** cross-entropy loss
- **baseline :** Neural Motif, IMP, Graph R-CNN
- **data :** Visual Genome
- **result :** SOTA
- **contribution :** 잘 모르겠음. 
- **limitation or 이해 안되는 부분 :** region proposal을 n개 하면 $O(n^2)$만큼

## Details
### Architecture
![image](https://user-images.githubusercontent.com/46675408/182502012-023b78c7-e36f-41f2-9386-999ecf157b93.png)

object proposal 넣어서 relation 예측하는데 예측하는 방식은 3.3 BA부분에 설명되어 있음.
$d = W_p * u_{i,j}$
- $u_{i,j}$ 2048차원의 subjet-object pair의 union feature? 어떻게 만들었는지는 안 써있음

$p_{i,j} = softmax(W_r(o_i'*o_j'*u_{i,j}) + d \odot \tilde p_{i->j}$

- $\odot$은 HadaMard Product
- *은 
![image](https://user-images.githubusercontent.com/46675408/182503496-f50517f8-ce7a-4ab9-8250-53bee9b345d3.png)

결론적으로 argmax해서 relation 구함.
![image](https://user-images.githubusercontent.com/46675408/182503536-099f0952-7028-43fb-a046-d8649797a596.png)
 
#### Frequency Softening 
VG 데이터셋이 long-tail이기 때문에, 마지막 softmax 단의 확률에 log를 취해줌 
![image](https://user-images.githubusercontent.com/46675408/182502545-695d98a1-9ab4-4135-9a9f-d11519a4321e.png)



### Results
![image](https://user-images.githubusercontent.com/46675408/182502220-47f9e0a4-7e3b-4e86-8179-a983f94259ec.png)
