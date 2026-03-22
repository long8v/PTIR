---
title: "[31] GIT: A Generative Image-to-text Transformer for Vision and Language"
date: 2022-06-26
tags: ['multimodal', 'microsoft', '2022Q2']
paper: "https://arxiv.org/pdf/2205.14100.pdf"
issue: 36
issueUrl: "https://github.com/long8v/PTIR/issues/36"
---
![image](https://user-images.githubusercontent.com/46675408/175830566-0182206a-d8fa-4fdb-a8c6-02f8499a4f9c.png)
[paper](https://arxiv.org/pdf/2205.14100.pdf)

## TL;DR
- **problem :** MLM, Image-Text Matching류의 프리트레이닝은 다운스트림 태스크와 다르다. 이 때문에 통합된 generative 모델로 푸는 접근들이 있는데, 보통 multi-modal encoder와 text decoder를 가지고 있다. 
- **idea :** 한개의 이미지 인코더와 텍스트 디코더로만 generative하게 학습되도록 하자. image classification도 closed vocabulary가 아니라 generative model이 결과를 내도록 하자. 이때 Swin류의 encoder를 contrastive 하게 학습하자.
- **result :** image/video captioning, question answering에서 SOTA.
![image](https://user-images.githubusercontent.com/46675408/175831072-2632c3f4-e75f-48d4-9cdc-ea054f5b9458.png)
- **contribution :** cross attention 없이 seq2seq 단순한 구조로 captioning, QA에서 SOTA라는 점. 

## Details
### Architecture 
![image](https://user-images.githubusercontent.com/46675408/175831699-f1f83fd3-0faf-4177-bff3-3413172303e1.png)
- pre-training
image encoder는 contrastive pre-trained model(Florence)를 기반으로 하고, 이미지는 2D feature map에서 flatten되고, linear layer와 layernorm layer을 거쳐 D 차원으로 project된다. 텍스트 디코더는 그냥 트랜스포머다. 이미지 피쳐는 텍스트 임베딩과 concat되어 트랜스포머 인풋으로 들어간다. image 토큰과 텍스트 토큰은 아래와 같이 마스킹되어 이미지 토큰끼리는 서로 attend 하고 text는 모든 이미지 토큰과 이전의 텍스트 토큰만 볼 수 있게 한다. 
![image](https://user-images.githubusercontent.com/46675408/175831875-aedb862e-03ef-4ae5-9888-67948496297a.png)

각각의 이미지-텍스트 pair에서 이미지가 주어졌을 때, 텍스트 토큰을 LM으로 예측하는 방식으로 진행된다. 이때 loss는 cross-entropy loss이다. 
- finetuning
똑같이 LM 태스크로 finetune하는데 input만 조금씩 달라진다.
- image captioning은 pretrain과 똑같이 학습된다.
- VQA는 question과 GT asnwer를 concat하여 special caption처럼 넣어주고, loss는 answer에만 토큰에만 부과하도록 한다. 
- 이미지 분류 태스크에서는 classifier를 두는게 아니라 class name을 이미지 캡셔닝처럼 두고 auto-regressive하게 학습되도록 한다. 이러한 generation based 모델은 새로운 카테고리가 추가되거나 삭제될 때 더 용이하다.

### Data
- COCO
- Conceptual Captions(CC3M)
- SBU
- Visual Genome(VG)
- ALT200M

### Related works
- CoCa와 다른점은 둘다 contrastive, generation task를 하지만 CoCa는 loss를 결합했지만 이 모델은 순차적으로 했다는 점.
- Flamingo는 둘다 하나의 이미지 인코더, 텍스트 디코더를 가지고 있지만, 다른 점은 별도의 decoder에서 cross-attention이 추가되지 않고 단순 이미지 인코더의 표현과 텍스트 디코더의 표현을 concat해서 디코더에 넣어줬다는 점이다. 또한 Flamingo는 이미지/텍스트의 pretrained weight를 freeze하고 cross attention만 finetune했는데 GIT은 다 finetune함.
- Florence: A New Foundation Model for Computer Vision
- ALIGN