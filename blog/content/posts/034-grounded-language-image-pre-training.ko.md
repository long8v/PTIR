---
title: "[29] Grounded Language-Image Pre-training"
date: 2022-06-21
tags: ['multimodal', '2021Q4', 'few-shot', 'zero-shot', 'microsoft', 'object detection']
paper: "https://arxiv.org/abs/2112.03857"
issue: 34
issueUrl: "https://github.com/long8v/PTIR/issues/34"
---
![image](https://user-images.githubusercontent.com/46675408/174726459-a2c9d73e-f8b6-4cf2-929f-380d44bf9db3.png)

[paper](https://arxiv.org/abs/2112.03857), [code](https://github.com/microsoft/GLIP) 

## TL;DR
- **I read this because.. :** 논문모임에서 언급이 많이 되어서 읽음.. 그러나 내가 이걸 읽었었네.. 
- **task :** object detection -> phrase grounding 문제로 치환해서 학습
- **problem :** 이미지 분류 모델은 정해진 카테고리 내에서 분류하기 때문에 real world에 적용하기 어렵다. CLIP이 image-text pair로 이를 해결했지만, 이건 이미지 분류에서의 이야기고 object detection 레벨의 태스크도 그렇게 풀고 싶다!
- **idea :** object detection 문제를 class 들이 prompt 형식으로 주어졌을 때 이미지에서 그 prompt의 단어들과 align을 잘하는 phrase grounding 문제로 바꿔보자.
- **architecture :** 1) Visual Encoder(Swin) + DyHead 2) Pretrained BERT 3) 1과 2를 early fusion. 
- **objective :** cls loss(with alignment score!) + regressor loss
- **baseline :** Faster RCNN, DyHead
- **data :** COCO, LVIS, Flickr30K, Object365, GoldG, OpenImages, Visual Genome, ImageNetBoxes
- **evaluation :** AP
- **result :** 1) 학습 때 주어지지 않은 COCO, LVIS 데이터셋에 대하여 supervised baseline 보다 더 높은 성능 2) COCO에 대해 finetune했을 때 SOTA 달성  3) 13개의 object detection 다운스트림 태스크에서 1-shot GLIP이 supervised Dynamic Head보다 더 높은 성능.
- **contribution :** CLIP in object detection 
- **limitation / things I cannot understand :**

## Details
### preliminaries
  - Dynamic Head : #94 
  - MDETR 
  - visual grounding : https://cvml.tistory.com/4
![image](https://user-images.githubusercontent.com/46675408/207490470-ce2b0cd6-ffcd-4d7b-91be-7f39f2ab0064.png)

  
### Data 
  - COCO : 80개의 object categories, training 118K, valid 5K, test 41K
  - LVIS : long tail object detection. 1000개의 categories.
  - Flickr30K : 이미지와 이에 대한 5 reference sentences. data for image captioning
  - Objects365 : 365 categories, 2 million images, 30 million bounding boxes
  - GoldG : 0.8M의 데이터로 MDETR 논문에서 human annotation 써서 만든 grounding data
  - OpenImages : 15,851,536 boxes on 600 categories, 478,000 crowdsourced images with 6,000+ categories
  - Visual Genome : 108,077 Images, 5.4 M Region Descriptions, 2.3M Relationships
  - ImageNetBoxes : [?](https://image-net.org/download-bboxes.php)
- architecture
object detection은 두개의 loss로 이루어지는데, localization loss와 classification loss의 합임. 이 때, localization에 대한 건 이 논문의 영역이 아님. classification에 대한 문제만 tackle할거임. 

보통의 object detection 문제에서 classification loss는 아래와 같이 정의됨.
![image](https://user-images.githubusercontent.com/46675408/174781550-757c0a65-ae7e-4538-b3c4-b632fe788ae6.png)

여기서 classification 대신 Image Encoder 따로 prompt를 처리하는 Language Encoder를 따로 둔 뒤 이의 내적이 alignment score가 되게함. 이게 classifier logit을 대체하게 됨.
<img width="740" alt="image" src="https://user-images.githubusercontent.com/46675408/174781857-c300edbc-dc62-43b4-90c3-e401a20723ce.png">

그리고 똑같이 loss에 넣으면 되는데 그냥 클래스보다 차원이 추가될 것임.(multiple data, tokenization,`[no_obj]` token). 

loss는 binary sigmoid loss를 사용하면 됨.

![image](https://user-images.githubusercontent.com/46675408/174779487-d003d510-9b7b-4e57-8ec2-ed53130d1b11.png)

detection 모델로는 FasterRCNN, DynamicHead(SOTA), image encoder는 Swin-T, Swin-L를 사용했고 textual encoder는 BERT를 사용했음. 
<img width="804" alt="image" src="https://user-images.githubusercontent.com/46675408/174782448-3e02520e-c10c-4c96-9bc6-dc4c4edc5f07.png">

deep fusion은 별건 아니고 각자의 encoder에서 나온걸 합치는게 아니라(late-fusion이라고 부름.) 레이어 쌓아가면서 정보를 교환하겠다는 취지. 이때 BERT는 이미 있는레이어 위에 새로운 레이어를 쌓아서 그 위의 layer들의 output을 교환함.

### Result
![image](https://user-images.githubusercontent.com/46675408/174773037-3f691cc6-e38b-42d2-ba34-1a3feea8b579.png)


 