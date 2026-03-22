---
title: "[10] CLIP: Connecting Text and Images"
date: 2022-01-27
tags: ['multimodal', '2021Q1', 'few-shot', 'SSL', 'zero-shot', 'CLIP']
paper: "https://arxiv.org/abs/2103.00020"
issue: 10
issueUrl: "https://github.com/long8v/PTIR/issues/10"
---
![image](https://user-images.githubusercontent.com/46675408/151471976-80ecc306-5480-4f02-9672-848ca1aec80e.png)
[article](https://openai.com/blog/clip/), [paper](https://arxiv.org/abs/2103.00020), [code](https://github.com/openai/CLIP)
**input :** text-image pair 
**output :** text-image가 올바른 pair일 경우 1, 아니면 0
**problem :** 기존의 이미지 분류 문제는 미리 정의된 카테고리에 대해 학습되어 generality가 떨어지고 새로운 레이블이 들어왔을 때 추가학습을 해야 함. 
**solution :** 웹에 쿼리를 날려 나온 이미지로 쿼리-이미지 페어 데이터셋을 만들고, 이미지와 텍스트를 각각 인코딩한뒤 이 코사인 유사도를 바로 logit으로 사용. loss는 symmetric CrossEntropy사용하여 P(이미지|텍스트)와 P(텍스트|이미지)가 유사하게 학습되도록 함. zero shot trasnfer의 경우 미리 텍스트들을 임베딩해놓고 이미지가 들어왔을 때, 코사인 유사도가 가장 높은 값을 label로 예측 
**result :** zero-shot transfer성능은 fully-supervised model보다 나은 dataset이 있었고, few-shot은 다른 접근법보다 성능이 우위, linear prediction을 했을 때 ResNet보다 성능이 우위인 dataset이 많았으며, data distortion에도 더 강건함을 보임. 
**details :**
- natural language supervision 기반으로 pretraining을 하는 것은 (데이터를 수집하기 용이하므로) 모델을 scaling하기 좋아서 이기도 하지만, zero-shot으로의 전환도 용이하다.
- image-tesxt pair data로 MS-COCO, Visual Genome, YFCC100M가 있지만 MS-COCO와 Visual Genome은 이미지가 한 클래스당 10만으로 매우 적고, YFCC의 경우 인스타그램으로 수집되어있는데 label이 의미없는 숫자 등 매우 noisy하다.
- 데이터셋을 구축하기 위해 50만 쿼리를 인터넷이 날려 400M의 text-image pair를 구축했다. 이를 WebImageText(WIT)라고 이름지었고, 이는 GPT2의 WebText와 비슷한 크기의 데이터셋이다.
- 이전의 exact matching을 통해 학습하는 것은 이미지에 대해 다양한 텍스트 표현이 있을 수 있기 때문에 학습에 비효율적이었고, 이 때문에 Bag of words 접근법에 contrastive loss를 적용하게 되었다.
![image](https://user-images.githubusercontent.com/46675408/151281527-d839370c-2702-4144-ab2d-c4c9aa738f2f.png)
- CLIP은 (text, image)가 주어졌을 때 n**2개의 pair중 맞는 pair를 예측하는 방식으로 학습된다. 이때 텍스트와 이미지가 각각 인코딩 되고 인코딩된 벡터의 코사인 유사도가 맞는 페어면 높게, 아닌경우 낮도록 학습된다.
![image](https://user-images.githubusercontent.com/46675408/151282826-8e3ca31a-1868-49ff-9dc7-6b2e8d025a65.png)
- [Symmetric CrossEntropyLoss](https://openaccess.thecvf.com/content_ICCV_2019/papers/Wang_Symmetric_Cross_Entropy_for_Robust_Learning_With_Noisy_Labels_ICCV_2019_paper.pdf) 가 사용되었다. 이는 P(이미지|텍스트), P(텍스트|이미지)가 같은 것이 더 합리적이므로 이렇게 부과한  것 같음.
![image](https://user-images.githubusercontent.com/46675408/151283945-de0dca01-dac8-4f80-90df-66dfa40bdd2c.png)
- 과적합을 막기 위해서 text encoder, image encoder는 프리트레인된 걸 가져오지 않았고, representation과 contrastive 사이에 non-linear(#9 는 추가)도 추가하지 않았다.
- image encoder는 ResNet, ViT를 사용했다.
  - ResNet에서 attention pooling이라는 것도 사용해봤다고 한다.
- text encoder는 transformer를 사용했고, ResNet과 사이즈를 맞추기 위해 width(hidden_dim등)을 늘리고 depth(layer수)는 늘리지 않았다. 
- zero-shot transfer를 하기 위해서 모든 text에 대한 인코딩을 먼저 해놓고, 코사인 유사도가 가장 높은 값을 label로 한다.
![image](https://user-images.githubusercontent.com/46675408/151295478-678b998b-c359-4119-89f4-a9d10998b682.png)
- 단순히 text를 label로 쓰기엔, text가 다수의 이미지와 연관되어 있는 경우가 있었고, 한 단어가 아닌 여러 단어로 구성된 경우도 있었다. 이를 위해 GPT-3처럼 prompt engineering을 했는데, 가령 `A photo of {lablel}`로 바꾸기만 했더니 ImageNet 성능이 3% 올랐다. 또한 다의적 의미를 표현하기 위해 `A photo of a {label}, a type of pet.`와 같이 표현하는 것도 성능향상에 도움이 되었다. OCR의 경우 숫자나 텍스트에 quote(' 혹은 ")를 넣는 것이 도움이 됐다. 
- **zero-shot transfer**: pretrained ResNet과 비교했을때 성능이 데이터셋에 따라 20%우수하거나 10%나쁜 등 variance가 컸다. 그냥 zero-shot(한번도 보지못한 클래스를 예측)이 아니라 어느 데이터셋에서 학습한걸 다른 데이터셋으로 옮겼을때 다른 데이터셋에 대해 학습하지 않고 성능이 잘 나오냐를 말하는듯.
![image](https://user-images.githubusercontent.com/46675408/151479047-f8d4e671-7af7-4c8a-a6f1-55cc386f2487.png)

- **few-shot** : few-shot 성능이 좋았다.
![image](https://user-images.githubusercontent.com/46675408/151478940-2c73025e-16b7-4fe8-b9c6-93bb2d5b8ac9.png)
- **represnetation** : 좋은 representation learning이 되었는지 확인하기 위해선, linear prediction(representation은 fixed이고 위에 linear만 학습)이 있고 finetuning이 있는데 해당 논문은 zero-shot trasnfer과도 일맥상통하며, hyper-parameter 서치의 범위가 줄어드는 linear prediction으로 성능을 평가했다. 다양한 데이터셋, 다양한 평가방법으로 성능 평가를 했을 때 ResNet의 linear probe보다 성능이 좋았다.
![image](https://user-images.githubusercontent.com/46675408/151481548-a7864241-80f7-47d1-9908-2e6fd16b94bc.png)
또한 데이터셋의 distortion에도 ResNet보다 강건했다.
![image](https://user-images.githubusercontent.com/46675408/151481479-f764bcdb-c038-4b69-ad43-68245ff9867a.png)

 
**related work:**
- Visual N-gram, 이미지의 컨텐츠와 관련된 텍스트들을 학습하는 방법 : https://arxiv.org/abs/1612.09161
- zero shot 분류를 처음 제안한 논문 : https://arxiv.org/abs/1506.00511
- about prompt engineering GPT3 : https://arxiv.org/abs/2005.14165
