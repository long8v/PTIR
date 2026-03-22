---
title: "[15] Quantifying Memorization Across Neural Language Models"
date: 2022-03-24
tags: ['NLP', '2022Q1', 'privacy', 'LM']
paper: "https://arxiv.org/pdf/2202.07646.pdf"
issue: 15
issueUrl: "https://github.com/long8v/PTIR/issues/15"
---
![image](https://user-images.githubusercontent.com/46675408/160091748-b52f560c-9421-468e-9ac0-3e62893efa05.png)
[paper](https://arxiv.org/pdf/2202.07646.pdf)
**problem :**
모델이 커짐에 따라 training data를 외우는 일이 생긴다. 이러한 현상이 1) 모델 크기 2) 데이터 반복 횟수 3) 주어지는 context의 길이에 따라 얼마나 증가하는지를 정량적으로 평가해본다. 

**conclusion :** 
![image](https://user-images.githubusercontent.com/46675408/159837370-b5c2dd4e-d3e3-4a2d-b240-149f93695c81.png)

1. Model scale: Within a model family, larger models memorize 2-5× more data than smaller models. 
2. Data duplication: Examples repeated more often are more likely to be extractable.
3. Context: It is orders of magnitude easier to extract sequences when given a longer surrounding context. -> 좋은 쪽으로 해석하면 그만큼 adversarial attack을 하기 어렵다는 뜻임. Practitioners building language generation APIs could (until stronger attacks are developed) significantly reduce extraction risk by restricting the maximum prompt length available to users.

**details :**
- 이전 논문에서 학습 데이터를 memorization 하는 비율이 학습 데이터의 0.00000015%라고 했지만, 이 논문을 통해 최소 1%의 학습 데이터를 memorization 한 것을 확인했다. 
- memorization을 정의하는 건 대충 세가지가 있는듯 
1) One leading general memorization definition is differential privacy (Dwork et al., 2006), which is formulated around the idea that removing any user’s data from the training set should not change the trained model significantly.
2) counterfactual memorization (Feldman and Zhang, 2020; Zhang et al., 2021)
3) **k개의 context token이 주어졌을 때, greedy decoding을 통해 나오는 string s가 training data내에 있는 경우** <- 본 논문에서 채택한 정의 
if a model’s training dataset contains the sequence “My phone number is 555-6789”, and given the length k = 4 prefix “My phone number is”, the most likely output is “555-6789”, then we call this sequence extractable (with 4 words of context). 
- 전체 sequence를 query로 사용하는것은 사실상 불가능 하므로 5만 쿼리를 뽑았는데 이때, 길이가 50, 100, ... 500인 시퀀스에 대해 반복된 시퀀스의 길이 별로 1000개씩 뽑았다. 
- 모델은 GPT-Neo(125M, 1.3B, 2.7B, 6B), 데이터셋은 Pile dataset(825GB, 책, 웹, 오픈소스 코드)을 사용하였다. 모델과 데이터셋은 공개된 것들 중 가장 큰 것들이다. 이 때, 모델크기 - memorization 관계는 log-linear함.
- beam search(b=100)을 해도 아주 조금 extracted memorization이 늘었다. (평균 2%, 최대 5.6%) 45%의 경우 beam search와 greedy는 같은 결과를 냈다. 
- T5와 C4로도 실험을 진행. 이때는 masked LM을 완벽하게 복구했을 경우 memorization했다고 정의했다. 전체적인 경향은 GPT-Neo와 같았다. 그러나 모델크기 - memorization은 non-linear하지 않았고, 140번 이하로 반복된 시퀀스가 (더 반복된 시퀀스보다) 유의미하게 외워질 확률이 높았다. 그러나 이는 해당 시퀀스에 공백이 많아서 더 쉬워서 그랬다(...)
- 50 토큰 이상의 시퀀스에 대해 반복을 제거한 C4로도 학습을 했는데 외울 확률이 1/3 줄어들었다. 

**next papers :**
- training data extraction attacks (adversarial attack in LM)
- GitHub Copilot: Parrot or crow?
- Membership inference attacks against machine learning models.
- Understanding unintended memorization in federated learning.
- Calibrating noise to sensitivity in private data analysis

**thinkings :**
- GAN과 비슷한 방식으로 extraction을 못하게 하는 모델 왠지 있을 것 같다.
- privacy는 보통 숫자와 관련되어 있지 않을까....
- 결국 augmentation으로 해결할 수 있을 것 같기도 한데..근본적인 해결법을 생각해볼까 
- memorization != overfitting이라고 하네 https://bair.berkeley.edu/blog/2019/08/13/memorization/
- decoding 방식을 바꿈에 따라 tackle할 수 없을까?
- 또는 teacher force를 사용함에 따라 더 memorization?
 