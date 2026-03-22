---
title: "[16] Counterfactual Memorization in Neural Language Models"
date: 2022-03-25
tags: ['NLP', '2021Q4', 'privacy', 'LM']
paper: "https://arxiv.org/pdf/2112.12938.pdf"
issue: 16
issueUrl: "https://github.com/long8v/PTIR/issues/16"
---
<img width="754" alt="image" src="https://user-images.githubusercontent.com/46675408/160056323-1d6ad0f0-105f-45b3-8e63-a578d6613cb4.png">

[paper](https://arxiv.org/pdf/2112.12938.pdf)
**problem :** 단순히 트레이닝 데이터에 있는 글귀를 모델이 외웠다고 문제일까? 많이 나온 문구라면 그럴수 있지 않나? 문제는 잘 나오지 않는(rare)한 데이터를 외웠을 때다. 
**solution :** 데이터를 subset으로 나누고 특정 샘플이 해당 sample에 있고 없고에 따라 모델 성능이 많이 바뀌면 그걸 나쁜 memorization을 했다고 정의하자
**Counterfactual memorization measures the expected change in a model’s prediction when a particular example is excluded from the training set.** 
<img width="604" alt="image" src="https://user-images.githubusercontent.com/46675408/160054417-e8db1a2a-83f4-4329-ab64-2faf01459b66.png">
이를 구하기 위해서, 전체 트레이닝 데이터를 샘플링 한뒤 독립적으로 학습 시킨다. 각 모델들에 대해 특정 샘플 x가 있는 모델(이하 IN 모델)에서 next token prediction을 한 정확도와 샘플 x가 없는 모델(이하 OUT 모델)에서 같은 태스크를 했을 때의 정확도 차이를 측정한다.

More formally, we say a training example x is counterfactually memorized, when the model predicts x accurately if and only if the model was trained on x. 
1. We define counterfactual memorization in neural LMs which gives us a principled **perspective to
distinguish “rare” (episodic) memorization from “common” (semantic) memorization in neural LMs**
(Section 2).
2. We estimate counterfactual memorization on several standard text datasets, and confirm that rare
memorized examples exist in all of them. We study common patterns across memorized text in all
datasets and the memorization profiles of individual internet domains. (Section 3).
3. We extend the definition of counterfactual memorization to counterfactual influence, and study
the impact of memorized examples on the test-time prediction of the validation set examples and
generated examples (Section 4).

Generation-Time Memorization을 측정하기 위해서 generated 된 시퀀스가 training data에 있는지 확인하거나 training data를 구하기 어려우면 LM의 perplexity를 비교한다. 이러한 memorization과 우리가 제시하는 Counterfactual memorization의 다른 점은, 트레이닝 데이터에  near-duplicate 데이터가 많다면, 우리의 training set에서 subset을 제거하고 나서도 많이 남아있을 것이기 때문에 memorization으로 측정되지 않는다는 점이다.
![image](https://user-images.githubusercontent.com/46675408/160090448-83d21bf7-0999-479c-b2c6-f920b2f1674f.png)
counterfactual memorization이 낮게 측정된 트레이닝 샘플의 경우 반복되는 문구(마지막 block에서 노란색 highlight를 제외한 text들)가 많은 것을 확인 할 수 있었음. 

In summary, generation-time memorization measures how likely a trained model would directly copy from the training examples, while counterfactual memorization aims to discover rare information that is memorized.

모델은 T5을 사용했고, C4, RealNews, Wiki를 사용했다. training data의 25%씩 subset으로 모델을 만들었다. 
<img width="863" alt="image" src="https://user-images.githubusercontent.com/46675408/160056001-c948a599-c42b-4149-be40-be8e6589454f.png">
실험 결과는 위와 같다. 그냥 줄글보다 특수한 텍스트들(전체 대문자, table, bullet list,  multilingual texts)에서 더 많이 외우는 성향이 있었다. 

memorization과 유사하게 한 sample이 모델에 얼마나 영향을 미쳤나 측정할 수 있는데 Counterfactual Influence라고 한다.
이를 측정하기 위해선 
![image](https://user-images.githubusercontent.com/46675408/160085482-e7d14c13-07a1-44b4-833e-74600cfdfe7c.png)
이렇게 하면 된다. 위의 수식과 다른점은, x가 x'에 끼친 영향을 측정하기 위해서 x가 있는 subset과 x가 없는 subset에 대해 x'에 대해 측정한다는 점이다. 즉 위의 memorization은 x가 x에 스스로 influence를 주는 것을 측정했다고 볼 수 있다.

보통의 경우 memorization이 높으면 influence도 높았으나, 모두가 그렇진 않았는데, 0.4이상의 memorization을 가진 데이터에 대해서는 influence가 눈에 띄게 낮아졌다. 그 이유는 높은 memorization을 가진 데이터 중 높은 비율이 쓰레기 텍스트 데이터(의미없는 으꺅꺅붑쟞 이런거 말하는듯?) 이기 때문에 학습을 하기 위해선 외워야했지만 흥미로운 정보를 배우지 않아서 influence할 정보가 없었던 것이다. 

infl이 클수록 train(x가 있는 subset)에 있는 문장이 그대로 valid(x가 없는 subset)에 있는 경향을 볼 수 있었음. 즉 valid에 똑같은 셋이 있었기 때문에, train에 대한 influence가 컸을 것임.
![image](https://user-images.githubusercontent.com/46675408/160087330-e8e25958-c46f-4f85-a37c-6e490ec1e681.png)

실제로 influence와 memorization 이 큰 sample에 대한 generation 결과를 보니 아래와 같았음. 
![image](https://user-images.githubusercontent.com/46675408/160091391-fd059123-4dfd-468d-a2b9-4f7f215ddbc3.png)

