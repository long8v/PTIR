---
title: "[13] GPT-3 : Language Models are Few-Shot Learners"
date: 2022-02-21
tags: ['NLP', 'few-shot', 'zero-shot', 'openAI', '2020Q2']
paper: ""
issue: 13
issueUrl: "https://github.com/long8v/PTIR/issues/13"
---

![image](https://user-images.githubusercontent.com/46675408/154879105-531ec05a-a300-43f2-9781-40bc71a7b33a.png)
**problem :** LM으로 few-shot하자. 
**solution :** 엄청 큰 LM 모델을 만들자
**result :** 다양한 NLP task에서 few-shot 성능 SOTA. 
**details :**
- 모델 크기 별 zero-, one-, few-shot 모델의 성능 비교. 모델이 커질수록 in-context learning이 효과적임
![image](https://user-images.githubusercontent.com/46675408/154878914-7077fa07-58fa-4760-8c00-cb03be0cd191.png)
- GPT3에서 용어 설명 
![image](https://user-images.githubusercontent.com/46675408/154878891-19b5e368-e1f8-4797-b2c1-c069286f4bd2.png)
- 모델 아키텍쳐는 GPT2와 매우 유사하나, Sparse Transformer 같은 locally banded sparse한 어텐션으로 바꾸었다. 
- 모델 크기는 이 정도. "GPT-3"라고 보통 부르는 모델의 파라미터는 1750억. 데이터는 3000억 토큰.
<img width="894" alt="image" src="https://user-images.githubusercontent.com/46675408/154883051-a83e1c8d-8071-4a40-9e73-df126553d789.png">

- 데이터는 [Common Crawl](https://commoncrawl.org/the-data/)을 사용했고, 데이터의 질을 올리기 위해 전처리도 하고, 알려진 높은 퀄리티의 corpus와 섞기도 하였다.
- 큰 모델은 batch size를 최대한 크게, 작은 learning rate를 가지도록 하는것이 좋다.
- gradient noise scale을 구한 다음 이를 바탕으로 batch size를 정하였다.([ref](https://arxiv.org/pdf/1812.06162.pdf))
- Downstream Tasks : 
  - [Penn Tree Bank](https://catalog.ldc.upenn.edu/docs/LDC95T7/cl93.html) : 구문분석을 위한 corpus인데 LM 성능 평가로도 하는듯
  - [LAMBADA](https://zenodo.org/record/2630551#.YhL83O5Bz0p) : context 주고 빈칸 추론 corpus. long-range depndencies를 잘 해결해야 함
  - [SuperGLUE](https://w4ngatang.github.io/static/papers/superglue.pdf) : 이것저것 어려운 NLP task 모아 놓은 것  
![image](https://user-images.githubusercontent.com/46675408/154881240-611f7a5b-0348-474f-898c-55d73242ee19.png)
  
  - 산수 : 2~5자리수 더하기/빼기, 2자리수 곱하기, 1자리수 연산( 6+(4*8) 같은 것) 
  - word scrambling and manipulation task
<img width="1072" alt="image" src="https://user-images.githubusercontent.com/46675408/154881612-72d1402e-e4d7-4cf2-938a-270a776c0227.png">
  
  - news article generation : 인간이 직접 쓴 뉴스와 모델이 만든 뉴스 구분하는 annotation 진행. 일부러 구린 모델이랑 비교해서 t-test.
  - learning and using novel words : 딱 한번만 쓰인 단어를 보고 그 단어를 넣은 문장을 만들라고 함. 
<img width="1057" alt="image" src="https://user-images.githubusercontent.com/46675408/154882894-9c22c331-750d-4030-a62b-476fe4e6c0c0.png">
  
 - correcting english grammar : `"Poor English Input: <sentence>\n Good English Output: <sentence>` 이렇게 input을 줌. 
<img width="833" alt="image" src="https://user-images.githubusercontent.com/46675408/154882318-d2c441dd-84c0-47fd-bf2f-c0b99722d3f0.png">

- GPT3 모델의 한계들 
  - 생성을 잘 못함. 단어를 반복적으로 뱉어냄. 
  - 물리학에 대한 common sense가 부족함. 가령, '치즈를 냉장고에 넣으면 녹을까?'와 같은 것에 대답을 잘 못함. 
  - LM obejctive를 사용하기 때문에, bi-LM이 아니고, 어떤 단어가 중요하고 그렇지 않은지에 대한 정보가 부족함.
  - 다른 도메인 가령 비디오나 사진에 대한 것을 학습한적이 없어서 실제 세상에 대한 정보가 부족함
  - 인간이 평생동안 볼 단어들을 다 본 것 같은데 인간보다 학습속도가 떨어짐
