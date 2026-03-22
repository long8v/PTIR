---
title: "[113] BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models"
date: 2023-04-27
tags: ['multimodal', '2023Q1', 'salesforce']
paper: "https://arxiv.org/pdf/2301.12597.pdf"
issue: 122
issueUrl: "https://github.com/long8v/PTIR/issues/122"
---
<img width="1093" alt="image" src="https://user-images.githubusercontent.com/46675408/234770095-d4373ad9-a39b-4582-91e6-d9b9593bfe9e.png">

[paper](https://arxiv.org/pdf/2301.12597.pdf), [code](https://github.com/salesforce/LAVIS/tree/main/projects/blip2)

## TL;DR
- **I read this because.. :** aka BLIP2, 소문이 자자하여
- **task :** Vision Language Pretraining -> zero-shot VQA, captioning, image-text retrieval, 
- **problem :** Vision language pretraining 너무 비싸다
- **idea :** Vision model / language model freeze 시키고 중간의 가교 역할을 하는 Q former를 학습하자
- **input :** image, text
- **output :** text
- **architecture :** ViT + OPT(decoder only) or FLAN-T5(encoder-decoder) + Querying Transformer 
- **objective :** Image-Text Matching(ITM), Image-Grounded Text Generation(ITG), Image-Text Contrastive Learning(ITC)
- **baseline :** SimVLM, BeiT-3, Flamingo, Frozen, VL-T5, VLKD, OSCAR, VinVL, Florence, ALBEF, ...
- **data :** COCO, Visual Genome, CC3M, CC12M, SBI, LAION400M -> [NoCaps](https://nocaps.org/), COCO Caption, [Flickr30K](https://paperswithcode.com/dataset/flickr30k)
- **evaluation :** 알아서..
- **result :** trainable 파라미터가 훨씬 작은데 성능이 sota.
- **contribution :** vision - language의 효율적인 학습 방법 제안.
- **etc. :** flamingo 같은건 weight 공개를 안했는데 얘는 weight 공개까지하고 hf에도 업로드 해놔서 사람들이 많이 쓰는 듯하다 

## Details
<img width="507" alt="image" src="https://user-images.githubusercontent.com/46675408/234770875-ecc135fd-dc4c-44d8-88aa-af291312d399.png">

### Querying-TransFormer(Q-Former)
frozen image encoder / frozen LLM을 연결시킬 거 찾음
image resolution과 상관없이 같은 개수의 output feature를 뽑음.

learnable query embedding을 학습. SA + CA with visual encoder로 학습. pretrained $BERT_{base}$를 가져왔고 CA는 새로 학습 시킴. 188M 크기.
32 query, 768 hidden dim. output query를 $Z$ 표현. $Z$의 차원 32 $\times$ 768은 frozen image feature의 차원보다 훨씬 작음(257 $\times$ 1024 for ViT-L/14). 

### Pretraining
- first stage : Vision-Language Representation Learning from a Frozen Image Encoder
<img width="984" alt="image" src="https://user-images.githubusercontent.com/46675408/234771853-d0dd2357-2c0f-4bcb-8b4a-cab81d6de999.png">

- Image-Text Contrastive Learning(ITC)
image 표현과 text 표현 사이의 mutual information이 잘 align 되도록. positive pair의 similiarity는 높게, negative pair의 similiarity는 낮게 
image transformer에서 나온 query 표현인 $Z$와 텍스트 트랜스포머에서 나온 `[CLS]` 토큰에 대한 표현 $t$ 사이의 pair-wise 유사도를 구하고 learned queries 개수만큼의 $Z$에서 가장 높은 거 하나만 고름. query와 text가 서로 볼 수 없게 unimodal self-attention mask를 사용.

- Image-Grounded Text Generation(ITG) 
이미지가 주어졌을 때 Text를 생성할 수 있게 하는 loss. Q-Former구조 자체가 image encoder와 text token 사이의 직접적인 interaction이 없기 때문에 query들이 text에 대한 모든 정보를 가지는 visual feature를 뽑도록 학습됨. Multi-modal Causal Self-Attention Mask이 적용됨. 이미지는 텍스트를 못보고 텍스트는 casual masking인 듯. UniLM 방식이랑 비슷하다고 하네)

- Image-Text Matching(ITM)
이미지와 텍스트 사이의 fine-grained alignment를 학습. image-text pair가 matched 냐 아니냐를 binary classification으로. query와 text가 전부 attend함. two class FCN에 모든 쿼리에 대한 logit을 평균으로 내서 output matching score로 사용.
Flamingo 처럼 negative hard mining 기법 사용

- second stage: Generative Learning from a Frozen LLM
Q-Former와 LLM을 사용해서 generative lanugage capability를 늘림.
ouput query embedding $Z$를 LLM의 text embedding hidden dimension으로 project해서 input text embedding 앞에넣음.

<img width="965" alt="image" src="https://user-images.githubusercontent.com/46675408/234771821-54e02233-02f7-498f-a6ba-e9cea5cd3cc2.png">

### Experiment
데이터는 위에 정리.
CapFilt + $BLIP_{large}$를 사용해서 web image에 synthetic caption을 만들었고 CLIP ViT-L/14를 사용해서 rank를 매겨서 top-2r만 남겨서 training-data로 사용했다

<img width="509" alt="image" src="https://user-images.githubusercontent.com/46675408/234776135-9e27e6b5-68eb-4830-88ed-68dfab71bef1.png">

<img width="521" alt="image" src="https://user-images.githubusercontent.com/46675408/234776179-89aa7e2f-b182-4364-92b3-d98eb4af19b8.png">


### Result
<img width="1031" alt="image" src="https://user-images.githubusercontent.com/46675408/234774435-b3055fed-6b0e-4980-a90d-11de74c2b02e.png">

<img width="1030" alt="image" src="https://user-images.githubusercontent.com/46675408/234774460-c8c93660-0e42-46c2-a18e-c7f66e490832.png">

- strong encoder 가 중요. ViT-G > ViT-L, Larger LLM better
- FlanT5(instruction tuned) > OPT(unsuperviesd) in VQA


<img width="1001" alt="image" src="https://user-images.githubusercontent.com/46675408/234774484-ba1e8ec6-ca77-490c-9688-c58e02b2e57c.png">


<img width="490" alt="image" src="https://user-images.githubusercontent.com/46675408/234774503-076a42bc-82ed-447a-ae29-4a46cd237fd1.png">

<img width="496" alt="image" src="https://user-images.githubusercontent.com/46675408/234776924-be3bb722-324d-4e4d-a6d8-a66b4b943745.png">

vision-language represntation learning을 안하면 generative learning잘 못하더라. modality gap을 bridge를 못함. 