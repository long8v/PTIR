---
title: "[51] Structured Sparse R-CNN for Direct Scene Graph Generation"
date: 2022-08-19
tags: ['2020Q2', 'CVPR', 'SGG', 'one-stage']
paper: "https://openaccess.thecvf.com/content/CVPR2022/papers/Teng_Structured_Sparse_R-CNN_for_Direct_Scene_Graph_Generation_CVPR_2022_paper.pdf"
issue: 57
issueUrl: "https://github.com/long8v/PTIR/issues/57"
---
![image](https://user-images.githubusercontent.com/46675408/185518290-086a79a5-3bfe-44ac-99af-4c26c7331792.png)

[paper](https://openaccess.thecvf.com/content/CVPR2022/papers/Teng_Structured_Sparse_R-CNN_for_Direct_Scene_Graph_Generation_CVPR_2022_paper.pdf), [code](https://github.com/MCG-NJU/Structured-Sparse-RCNN)

## TL;DR
- **task :** one-stage Scene Graph Generation
- **problem :** SGG를 보통 풀 때에, object detection, relation graph construction, relation prediction으로 구성되는데 통합된 모델로 한번에 set prediction을 하고 싶다.
- **idea :** region proposal query가 있는 [sparse R-CNN](https://openaccess.thecvf.com/content/CVPR2021/papers/Sun_Sparse_R-CNN_End-to-End_Object_Detection_With_Learnable_Proposals_CVPR_2021_paper.pdf)처럼 triplet queries를 두고 여기에 object pair와 relation에 대한 prior를 주입하도록 하고 이후 triplet detector라는 OD와 relation 을 병렬로 예측하는 triplet detector를 둔다. 
- **architecture :** CNN with FPN을 백본으로 사용. triplet query는 bbox와 obj vec, rel vec으로 구성되어 있는데 box는 ROI align되어 피쳐 뽑고, 나머지들은 MHSA를 통해 피쳐뽑은 뒤에 bbox에 대한 피쳐와 obj vec에 대한 feature는 OD로 rel vec에 대한 feature는 위의 피쳐들과 fusion 되면서 relation 예측.
- **objective :** bbox loss, CE loss for relation and object cls
- **baseline :** IMP, G-RCNN, MOTIF, transformer, vctree ... 
- **data :** Visual Genome, Open Image
- **result :** SOTA. 
- **contribution :** two-stage SGG처럼 보이나 one-stage인듯? one-stage이라고 했을 때, 성능이 아주 좋음.
- **limitation or 이해 안되는 부분 :** siamese sparse R-CNN랑 파라미터 share를 하면 .. 이게 distilation 같이 되는게 맞나? 🤔 
하나의 모델에서 GT object와 매칭해서 object detection loss를 줄 수 있었을텐데에 대한 의문점은 해결이 안됨.. 또는 relation이 없는 object pair끼리 조합해서 triplet 만들 수 있었을텐데?!

## Details
## Sparse R-CNN
https://github.com/long8v/PTIR/issues/58

## Architecture
![image](https://user-images.githubusercontent.com/46675408/185559317-8f24db68-b640-4ae0-b6ef-548479088d3e.png)

### Triplet query
- sparse RCNN의 query들처럼 tiplet의 general한 distribution을 표현하도록 함
- 2 proposal boxes coordinates : 4d
- 2 object content vectors(appearance 표현, sparse RCNN의 proposal features 같은 역할) : 1024, 256
- one relation content vector(structure information between objects) : 1024, 256

### Triplet detection head
- Object pair detection
object vector로 MSA를 할건데 좀 더 잘하기 위해 pair fusion module 적용

![image](https://user-images.githubusercontent.com/46675408/206087486-83a5a82d-8043-47f4-8f73-694144b41b0f.png)

![image](https://user-images.githubusercontent.com/46675408/206087273-b0aa22fc-b5e6-40d3-993b-609d9da9fba7.png)

$X_s'$, $X_o'$를 query, key로 사용. value는 두 개 각각의 object vector 자체가 될듯
여기서 강화된 object feature는 Dynamic Conv에 사용됨.

![image](https://user-images.githubusercontent.com/46675408/206087371-654c3ff7-a560-4580-80ff-155f38e090d9.png)


### Relation recognition
![image](https://user-images.githubusercontent.com/46675408/206087581-e2cabdc6-b964-4f2f-9098-a4c3abd51365.png)

relation도 bbox의 가장 큰 영역으로 해서 DyConv+ 위의 E2R fusion해서 뽑음.
![image](https://user-images.githubusercontent.com/46675408/206088079-472538bb-6fe5-4fc0-b6eb-5574e22a3100.png)


### Learning with Siamese Sparse R-CNN
ground-truth triplet만으로 학습하기에는 object들이 너무 sparse 함.
structured sparse r-cnn과 파라미터를 공유하는 Siamese Sparse R-CNN을 object detector로 사용하여 virtual object pairs를 pseudo-label로 써서 knowledge distilation으로 사용.

![image](https://user-images.githubusercontent.com/46675408/185559605-a296cf91-0e7f-45e4-982c-8ec7c9219973.png)

### two-stage triplet label assignment
1) ground-truth triplet과 예측된 triplet을 매칭함
![image](https://user-images.githubusercontent.com/46675408/187102457-d2729d11-c1ac-40c2-abb2-a99256ed1344.png)

2) gt에 매칭되지 않은 triplet에 대해서 siamese sparse R-CNN이 내 뱉은 object pairs와 매칭을 시킴
남은 triplet에 대해서 box는 그대로 두고 object classification score만 label로 바꿈. 
siamese sparse R-CNN이 내뱉은 pseudo-label과 나머지 triplet의 object에 대해 아래 matching cost로 hungarian을 부과
![image](https://user-images.githubusercontent.com/46675408/187102624-1c320354-ce50-4c1e-9788-2de17874026e.png)

그리고 relation에 대해서는 `background`로 패딩한 뒤 loss 계산
![image](https://user-images.githubusercontent.com/46675408/187102714-4787fd67-9136-401d-818c-97a34990288d.png)

### Imbalance Class Distribution
- Adaptive focusing parameter
object classification에서 너무 major한 클래스에 대한 weight를 줄임.
![image](https://user-images.githubusercontent.com/46675408/187106218-b8a180c6-f095-4212-b698-70ef5315f055.png)

- logit adjustment
![image](https://user-images.githubusercontent.com/46675408/187106185-7091cca5-6fe4-4ace-bc2e-5c42ce9c239e.png)


### Results
<img width="685" alt="image" src="https://user-images.githubusercontent.com/46675408/186424240-689b836a-1830-4788-8b39-3432b2dcbbcb.png">
