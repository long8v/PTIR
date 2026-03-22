---
title: "[52] Sparse R-CNN: End-to-End Object Detection with Learnable Proposals"
date: 2022-08-19
tags: ['object detection', '2020Q4']
paper: "https://openaccess.thecvf.com/content/CVPR2021/papers/Sun_Sparse_R-CNN_End-to-End_Object_Detection_With_Learnable_Proposals_CVPR_2021_paper.pdf"
issue: 58
issueUrl: "https://github.com/long8v/PTIR/issues/58"
---
![image](https://user-images.githubusercontent.com/46675408/185548035-a23480eb-3150-4c26-b594-52457f8ab039.png)

[paper](https://openaccess.thecvf.com/content/CVPR2021/papers/Sun_Sparse_R-CNN_End-to-End_Object_Detection_With_Learnable_Proposals_CVPR_2021_paper.pdf), [code](https://github.com/PeizeSun/SparseR-CNN)

## TL;DR
- **task :** object detection
- **problem :** 대부분의 OD 문제는 dense하다. 가령 faster R-CNN의 경우 sliding window 하면서 box 후보들을 뽑고 나중에 NMS 같은걸로 박스를 추린다. many-to-one assign label assignment도 문제가 된다. DETR도 object query들은 sparse하지만 결국 global하게 interact 하는 부분이 dense하다!
- **idea :** 100개 이하의 sparse한 box, 그리고 각 box의 feature가 이미지의 모든 feature와 interact하지 않는 OD 모델을 만들어보자!
- **architecture :** 4개의 coord를 나타내는 learnable proposal box들 100개를 던지고, 해당 박스의 RoI를 뽑는 RoIPool또는 RoIAlign 연산을 하고 거기서 feature를 뽑는다. 이 proposal feature가 주어졌을 때, dynamic head라는 연산을 통해 최종 object localization과 classification을 예측하고 이게 다음 레이어에서는 proposal box와 feature를 쓰게 된다.
- **objective :** hungarian loss(gIoU loss + bbox L1 loss + cls cross entropy loss)
- **baseline :** Faster RCNN, DETR, RetinaNet 
- **data :** COCO 2017
- **result :** Faster RCNN, DETR, RetinaNet보다 훨씬 빠른 수렴
- **contribution :** OD 문제를 재밌게 풀었다! DETR이랑 비슷한듯 안 비슷한듯!
- **limitation or 이해 안되는 부분 :** DETR이 모든 픽셀에 대해서 상호작용하는 부분이 dense해서 안좋다는게 이유가 납득은 안됨. DETR가 마찬가지로 아무런 정보가 없이 주어지는 learnable proposal box가 결국은 수렴하면 이미지 없이도 box를 뽑는다는게 신기함....(인퍼런스를 생각해보면 좀 이해가 안되기도 하고.. 100개가 충분해서 하나는 걸리려나..)

## Details
![image](https://user-images.githubusercontent.com/46675408/185552564-409c7b46-4aaf-4239-b301-225001df963f.png)
이미지 내 dense grid에서의 object positional candidate나 global image feature와 상호작용하는 object query가 없는 "purely sparse"한게 특징.
4d로 표현되는 fixed learnable bounding boxes가 주어지고 Region of Interest(RoI)에서 RoI pooling으로 feature를 뽑는데 사용된다. 이때 learnable proposal boxes는 이미지를 보지 않고 뽑기 때문에 이미지 내 통계적인 object location을 의미한다. 
- RoI pool : https://csm-kr.tistory.com/37

![image](https://user-images.githubusercontent.com/46675408/185553565-2a2a467f-baba-4cda-b244-d646d90c76aa.png)

### Learnable proposal feature
4d proposal box가 있지만 localization 정도만 표현하지 더 이상의 정보를 담고 있지 않다. 이를 보강 하기 위해 prosposal box 개수만큼의 높은 차원(256)의 proposal feature도 learnable한 벡터로 만든다.

### Dynamic instance interactive head
N개의 proposal box가 나오면 RoIAlign을 해서 각 box의 feature를 뽑은 뒤에 위의 proposal feature와 1x1 conv붙여서 interaction 시켜서 final object feature C를 만든다. 이 C에서 cls, bbox regression을 한다. 
object feature C는 다음 레이어의 proposal features로 사용되고, bbox도 다음 레이어의 proposal box로 쓰인다.

dynamic head #94 

object feature간의 relationship을 학습하기 위해 set of object feature를 dynamic instance interaction(?)을 하기 전에 self-attention 사용을 해서 성능을 늘렸다. (그림에는 생략됨 -.-;;)


![image](https://user-images.githubusercontent.com/46675408/185553350-2cdfa7cf-eb8d-4b97-81ae-a62d9300e042.png)

### Results
![image](https://user-images.githubusercontent.com/46675408/185553657-47494511-4602-4810-8995-205ad80ca19a.png)

![image](https://user-images.githubusercontent.com/46675408/204690119-c67f6909-746f-4dff-8fb1-34955313ca36.png)

초기 bbox들을 크게크게 잡는듯ㅋㅋ
