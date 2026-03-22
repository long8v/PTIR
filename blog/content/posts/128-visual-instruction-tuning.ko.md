---
title: "[119] Visual Instruction Tuning"
date: 2023-06-09
tags: ['multimodal', 'NeurIPS', '2023Q2']
paper: "https://arxiv.org/abs/2304.08485"
issue: 128
issueUrl: "https://github.com/long8v/PTIR/issues/128"
---
<img width="594" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/534c85ad-90d1-40e2-9097-ed2d205e1170">


[paper](https://arxiv.org/abs/2304.08485)

## TL;DR
- **I read this because.. :** llava 1.5를 읽기 위해 
- **task :** chatting VLM
- **problem :** chatGPT처럼 multi-modal에서도 instruction-following하게 해보자 
- **idea :** language only GPT에 bbox와 caption을 넣고 QA를 만들게 함
- **input/output :** image + Q -> A
- **architecture :** LLaMA 13B + CLIP + projection
- **objective :** ce loss 
- **baseline :** GPT-4, BLIP-2, OpenFlamingo
- **data :** (feature alignment) CC3M 중에 filtering한 것 (e2e learning) COCO 이미지에 대해 캡션 및 bbox를 넣고 GPT4 혹은 chatGPT로 만든 insturction data or SicenceQA
- **evaluation :** coco에서 sampling 하여 question을 작성하고 GPT-4가 bbox랑 caption이랑 question 받았을 때 내뽑은 answer를 GPT-4한테 다시 평가하라고 함. 
- **result :** Science QA에서 좋은 성능, BLIP-2 / OpenFlamingo / GPT-4가 못하는 상위 reasoning(유머 해석 등)을 잘함 
- **contribution :** assist하기 위해 instruct 데이터를 만든 아마 최초의 work.  오픈소스화를 잘해서 널리 쓰임 
- **etc. :**

## Details
### Instruction following data 
- COCO 이미지에 대해 caption과 bbox넣고 만듦
- converstaion(58K) / detailed description(23K) / complex reasoning(77K)
<img width="500" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6b096002-2370-4f65-8538-06f25683523a">

<img width="500" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5dd53143-8c24-4400-b2ab-048d3231b9bd">

이에 대한 ablation. 
detailed caption을 넣으면 chatbot 쪽 성능이 오른다. reasoning에 도움을 주는 듯 하다. 

### Training 
input sequence

<img width="696" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/de4a7e3e-1884-48bb-83f1-02818648b5e0">

<img width="641" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8f9d6b64-b5eb-4295-9930-274a20a7e974">

첫번째 question은 이미지가 먼저 나올 수도 있고 question이 먼저 나올 수도 있고 순서는 랜덤 

<img width="448" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ad5a59e1-8bad-4081-b467-9e10d8b4bba9">

<img width="867" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7ff9dafe-f9ca-4b53-9072-d8cc3909be8f">


- pre-training feature alignment
CC3M에서 595K image text만 Filtering + linear projection만 학습 
caption을 그대로 사용하되 간단하게 instruction following 포맷으로 맞춤(single turn, image를 briefly 설명해달라고 요구)
이때 filtering 방법은 아래와 같음 (noun frequency별로 uniform하게 맞춤)

<img width="705" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/eb673bd0-9954-480d-ac20-ed84b1283d3b">

<img width="678" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4028fd16-6ad9-44a0-a5ba-191a09feade4">

- finetuning end-to-end
vision encoder만 freeze 시키고 나머지 projection + LM을 학습 

### Ability 
<img width="1500" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1e600282-57ab-464f-9c7b-b93e88408dec">

complex reasoning에 대해 만드는 방법이 궁금한데 아래와 같이 [system prompt](https://github.com/haotian-liu/LLaVA/blob/main/playground/data/prompts/complex_reasoning/system_message.txt) 넣었다고 하네
```
You are an AI visual assistant that can analyze a single image. You receive five sentences, each describing the same image you are observing. In addition, specific object locations within the image are given, along with detailed coordinates. These coordinates are in the form of bounding boxes, represented as (x1, y1, x2, y2) with floating numbers ranging from 0 to 1. These values correspond to the top left x, top left y, bottom right x, and bottom right y.

The task is to use the provided caption and bounding box information, create a plausible question about the image, and provide the answer in detail.

Create complex questions beyond describing the scene.
To answer such questions, one should require first understanding the visual content, then based on the background knowledge or reasoning, either explain why the things are happening that way, or provide guides and help to user's request.  Make the question challenging by not including the visual content details in the question so that the user needs to reason about that first.

Instead of directly mentioning the bounding box coordinates, utilize this data to explain the scene using natural language. Include details like object counts, position of the objects, relative position between the objects.  

When using the information from the caption and coordinates, directly explain the scene, and do not mention that the information source is the caption or the bounding box.  Always answer as if you are directly looking at the image.
```

### Ablations 
<img width="343" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2475db52-a066-45b0-976f-a5c540ee46e7">

- ViT 마지막 레이어 vs 이전 레이어 -> 이전 레이어가 더 좋음
- CoT 적용 즉 answer 다음 reasoning / Reasoning 다음 answer -> 수렴은 reasoning - answer가 더 빨랐으나 최종적인 성능은 그렇지 않았음
- alignment learning 단계 없이 바로 학습 -> 성능 악화
- LLM 13B에서 7B -> 성능 악화


### Play with demo 
https://llava.hliu.cc/
demo랑 놀아보았다
<img width="960" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/431de7ba-f0fb-4d4b-a975-256cbb154bda">

일반적인 설명 잘한다

scene graph generation 시켜보았다.
<img width="971" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7d755617-be67-441d-9fea-89889657586f">

<img width="972" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/fc82b08f-4ddc-4494-b74b-e21eb02a9493">

<img width="981" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ccd16297-657b-4625-b6af-cb93551ffeee">

predicate가 더이상 동사가 아님..
<img width="984" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7803f163-bbf8-4db4-b1c2-2f5ac454469e">

거짓말 시작..

예시를 잘못 줘도 그냥 답변에 포함. 그래도 대충 말은 되는 triplet을 만드는군
<img width="959" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1ae11635-62cd-400e-93a6-8b63f007bd17">

<img width="932" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f06bd7d4-18fa-4177-84d5-e28c7811f10d">

여기도 hallucination이 ..  visual genome은 아마 학습 데이터에 있었을 것 같으니 다른 데이터 가져와보자
내가 대만에서 찍은 이 사진 ..

<img width="490" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b4bf4bf5-fe6b-4c2c-ad68-81ecf107df2e">

<img width="951" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7bde0a9b-8376-4a76-b8bb-294f00991332">

child가 어딨는지 모르겠지만 대충 맞다

<img width="975" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d5a72445-4aeb-4742-8bdb-461d44b7491f">

<img width="300" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d775d09b-4f96-4d2d-b9ce-dd0cae1f6097">

나름 clear한 sample인데

<img width="980" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d36c4342-071f-47b2-a6f2-efeee2a4ad88">

점점 맛가기 시작 ㅜㅜ

<img width="965" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b2e1b227-7cfd-4ee1-9d25-a4350eab306d">

prompt를 바꾸니 갑자기 또 바른 말 하기 시작...

예시를 잘 주니 나름 잘 동작 그러나 애기는 어디있는가?
<img width="958" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/26035797-a5dc-49b7-8e3a-db317f950df7">

relation이 아주 뚜렷한 ㅋㅋ 벤치마크에 있어도 이상하지 않을 부산에서 찍은 아이 사진을 올려본다 
<img width="300" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/34a009b5-799e-4249-b37f-b17a839880a6">


<img width="954" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/27d3b6cb-90bb-4d0e-8d86-9cebc6cd468c">

완벽하네
<img width="973" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/98e7557c-e455-4c50-8081-7b6ca7aa32f1">

약간 동어 반복이긴 하지만 틀린 말은  안하네

<img width="956" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/43308a72-acf5-4df8-9fdc-b8d0d5f6d650">

감성적인 말까지 ..

<img width="979" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ea9670aa-4d69-42bf-8ff3-7a039f63b5f4">
<img width="967" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d966a85b-a618-4fc7-9b7a-f3cf361310da">

3절 4절 뇌절해도 잘받아줌..
