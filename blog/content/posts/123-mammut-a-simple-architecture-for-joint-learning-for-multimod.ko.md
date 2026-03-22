---
title: "[114] MaMMUT: A Simple Architecture for Joint Learning for MultiModal Tasks"
date: 2023-05-09
tags: ['multimodal', 'google', '2023Q1']
paper: "https://arxiv.org/pdf/2303.16839.pdf"
issue: 123
issueUrl: "https://github.com/long8v/PTIR/issues/123"
---
<img width="1102" alt="image" src="https://user-images.githubusercontent.com/46675408/236988463-5eebdcef-80eb-4f9c-80bd-c4829a9ef724.png">

[paper](https://arxiv.org/pdf/2303.16839.pdf)

## TL;DR
- **I read this because.. :** multi-modal 시리즈. 
- **task :** VLM -> captioning, image2text retreival, text2image retreival, VQAv2, Video QA, Video Captioning, Open-Vocab Detection 
- **problem :** contrastive learning는 retreival 능력이 있고 captioning learning은 text generation 능력이 있다. 근데 이 둘의 학습 방식이 상충하여 하나에 담기 어렵다. 
- **idea :** language model에 대해 decoder only로! contrastive랑 captioning이랑 필요한게 다르기 때문에 forward를 masking을 다르게 하여 두 번 함
- **input/output :** (pretraining) image / text -> similiarity score / caption text 
- **architecture :** Image Encoder(ViT Huge, 650M) + Lanauge Decoder(1B Transformer)
- **objective :** Image Captioning Loss + Focal Contrastive Loss 
- **baseline :** CoCa, Florence, CLIP, ALIGN, ...
- **data :** (pretaining) only ALIGN -> (finetune) MSCOCO, Flickr30K, VQAv2, ...  
- **result :** zero-shot image-text retreival에서 sota. VQAv2도 파라미터 크기대비 성능 ㄱㅊ.   
- **contribution :** 별도의 image vision encoder pretraining 없이 fully e2e training. CoCa랑 유사한데 architecture가 비교적 간단. video도 vision encoder 여러번 forward 안해도 되는게 강점이라고 하는데 이건 .. TubeViT의 contribution인듯?..
- **etc. :** CoCa는 JFT도 썼는데 왜 이게 더 retrieval 성능을 이겼을까? CoCa가 더 많은 태스크를 해서 retreival 성능이 다소 낮은거 아닐까? 또는 학습 방법? CoCa 느낌으로 학습해서 비교했으면 더 좋았을텐데 

## Details
### Related works
- Video 처리 -> TubeViT
  - https://arxiv.org/pdf/2212.03229.pdf
  - 뭔가 sampling을 잘해서 image / video를 같은 방식으로 처리할 수 있는 논문인듯
<img width="582" alt="image" src="https://user-images.githubusercontent.com/46675408/236992950-8dde90db-28c2-4197-bb5d-79157204423d.png">

- object detection의 PE와 pretraining의 PE 사이를 채워주기 위해 -> Cropped PE / Focal Loss for Constrative loss
  - Region-Aware Pretraining for Open-Vocabulary Object Detection with Vision Transformers에서 보였다는데 논문을 찾을 수가 없넹
 
### Architecture

<img width="1080" alt="image" src="https://user-images.githubusercontent.com/46675408/236991324-73ea28e2-f68e-4ffd-9f6f-4b0000af353e.png">

<img width="1093" alt="image" src="https://user-images.githubusercontent.com/46675408/236991369-931be06a-227b-4939-8ff3-cfa1bf5edc26.png">

<img width="1093" alt="image" src="https://user-images.githubusercontent.com/46675408/236991394-13029f52-7db8-49c8-90ba-521077e2d9c9.png">

main contribution인 two-pass learning 
captioning은 causal masking을 필요로 하고(conditioned 표현이 필요), contrastive는 text 전체의 표현이 필요.
걍 decoder로 masking 다르게 해서 두번 forward! (masking / CA 아니면 걍 이게 encoder 아니묘 ㅋㅋㅋ) 
~CoCa도 text encoder 같은걸 가지고 decoder라고 표현했는데 여기도 사실상 CoCa랑 거의 유사한데 Unimodal Text Decoder + MultiModal Text Decoder가 같은 weight를 가지는거라 봐도 될듯!~
CoCa는 text decoder에 causual masking이 있는 self-attention을 추가했음! 얘는 forward 한번만 해도 됨.
<img width="417" alt="image" src="https://user-images.githubusercontent.com/46675408/236992384-168658ca-3acc-406b-a09b-5a9daaa5d9ae.png">


### Loss
- Captioning loss
<img width="561" alt="image" src="https://user-images.githubusercontent.com/46675408/236991421-9fd9d2a8-290a-4f2e-9c6f-a144475f3cc6.png">

- Focal Constrative Loss
contrastive learning은 보통 bs가 커야함. CE보다 더 challenging한 데이터로부터 배우자 -> focal loss 사용 

<img width="476" alt="image" src="https://user-images.githubusercontent.com/46675408/236991448-102c411d-1316-4744-bb4d-c6e757b6464a.png">
<img width="341" alt="image" src="https://user-images.githubusercontent.com/46675408/236991489-88454d15-ee74-460f-b5f8-9ffb5cdcaa19.png">

### Video 처리
<img width="1128" alt="image" src="https://user-images.githubusercontent.com/46675408/236991611-dd09ca33-b214-4c3d-8280-7c644d204f6f.png">

## Result
<img width="1073" alt="image" src="https://user-images.githubusercontent.com/46675408/236991641-af95e6e8-d0f5-4539-a882-4372b0a43e48.png">
<img width="1061" alt="image" src="https://user-images.githubusercontent.com/46675408/236991666-c00dbbbc-f6bd-4621-bdc2-5bde1d8f8e9c.png">

### Ablations
<img width="1119" alt="image" src="https://user-images.githubusercontent.com/46675408/236991703-9c040188-122d-48fd-83d1-bac7167ced03.png">

- captioning loss를 사용하니까 text2image는 성능이 더 좋고  image2text는 성능이 더 낮음. generation이 더 나은 text 표현을 만든 듯 -> 이거 잘 모르겠음.. 쌍방 아닌가?!
- CA는 자주 주면 VQA는 좋았고 Retreival은 안 자주 줘도 되었다

<img width="1157" alt="image" src="https://user-images.githubusercontent.com/46675408/236992873-a4ec70a7-39c6-4282-802d-c31b622d6c11.png">

작아도 잘한다.
