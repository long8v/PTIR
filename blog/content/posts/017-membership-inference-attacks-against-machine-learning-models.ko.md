---
title: "[17] Membership Inference Attacks Against Machine Learning Models"
date: 2022-03-28
tags: ['privacy', '2016']
paper: "https://arxiv.org/pdf/1610.05820.pdf"
issue: 17
issueUrl: "https://github.com/long8v/PTIR/issues/17"
---
<img width="1035" alt="image" src="https://user-images.githubusercontent.com/46675408/160326216-91b27882-77b0-47e8-bc22-787489ff5482.png">

[paper](https://arxiv.org/pdf/1610.05820.pdf)

- **Membership Inference** : 해당 데이터가 모델의 training data에 있는지 없는지 확인하는 공격. 가령 의료데이터의 경우에 특정 데이터가 학습 데이터로 존재한다는 것만으로도 심각한 프라이버시 유출이 될 수 있음.
- 이러한 공격의 가정은 아래와 같음. 1) 공격을 하는 모델은 다중 분류 모델이라고 가정 2) ML as Service로 input과 output을 얻을 수 있음. 3) 공격하고자 하는 모델의 트레이닝 데이터셋의 일부를 알고 있음.
- Membership Inference Attack의 알고리즘은 아래와 같음. 
<img width="481" alt="image" src="https://user-images.githubusercontent.com/46675408/160327410-fdbeb5a7-2e8b-4b72-b3e7-48808a748c26.png">

(1) 실제 모델(target model)의 결과값을 따라하는 shadow 모델들을 정의함.(target model의 아키텍쳐를 안다면 똑같이 만듦)
(2) 알고있는 트레이닝 데이터를 겹치지 않게 subset을 만들고, 각각을 shadow 모델들로 학습함.
(3) 전체 데이터셋에 대하여 실제 레이블값, shadow 모델의 예측값을 input으로 주고 해당 shadow 모델의 해당 데이터 샘플이 존재했는지(`"in"`, `"out"`) 분류하는 attack model을 학습함. 

<img width="634" alt="image" src="https://user-images.githubusercontent.com/46675408/160328455-1c8cdf1a-b74b-4976-bbb1-f0ad629b3182.png">

**results :**
대부분의 데이터에서 높은 precision, recall. membership attack은 black box(모델을 모르고, 데이터셋에 대한 prior assumption이 틀렸을 때도) 환경에서도 잘 작동함.  
<img width="1119" alt="image" src="https://user-images.githubusercontent.com/46675408/160329715-41ec5751-8b65-4b39-ae84-d757457492dd.png">

confidence가 member, non-member일 때 확실히 다름.
<img width="1079" alt="image" src="https://user-images.githubusercontent.com/46675408/160329245-a3b6abdb-176b-4f29-bbb3-788690e7e75d.png">



