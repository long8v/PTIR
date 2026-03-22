---
title: "[95] Pixels to Graphs by Associative Embedding"
date: 2023-01-04
tags: ['NeurIPS', '2017', 'SGG', 'one-stage']
paper: "https://arxiv.org/pdf/1706.07365.pdf"
issue: 104
issueUrl: "https://github.com/long8v/PTIR/issues/104"
---
<img width="907" alt="image" src="https://user-images.githubusercontent.com/46675408/210468311-d07824b8-34b1-4eaf-9bde-e064aeef3045.png">

[paper](https://arxiv.org/pdf/1706.07365.pdf), [code](https://github.com/princeton-vl/px2graph)

## TL;DR
- **I read this because.. :** SGG 초기 논문 
- **task :** one-stage SGG
- **problem :** RPN 없이 object 뽑고 relation도 뽑아보자
- **idea :** multiperson pose estimation의 associate embeddings 아이디어 차용. body joint에서 비슷한 임베딩을 가진 애들끼리 같은 사람으로 묶는 네트워크. 
- **architecture :** hourglass + CNN + 1D CNN으로 object와 relation이 있을 것 같은지 각각의 heatmap 생성. train 때는 GT, infer에는 top k activation 된 픽셀에 대해 object는 anchor based box regressor, cls id 예측. relation은 relation class, subject object id를 예측. 
- **objective :** bbox regression loss + sigmoid loss for heatmap + ce for subject / object id +pull together loss + push apart loss 
- **baseline :** [VRD with lanugage prior](https://arxiv.org/abs/1608.00187), [Scene Graph Generation by Iterative Message Passing](https://arxiv.org/pdf/1701.02426.pdf)
- **data :** Visual Genome
- **evaluation :** SGGen, SGCls, PredCls
- **result :** SOTA
- **contribution :** first one-stage SGG
- **limitation / things I cannot understand :** feature vector가 예측도 해야되고 자기들끼리 가까워지고 멀고 하는 loss도 추가적으로 있는 것 같은데 상이한 방향인 것 같은데 한 공간에서 학습하는게 신기하네

## Details
<img width="870" alt="image" src="https://user-images.githubusercontent.com/46675408/210469355-3aaa50ae-d7dd-42c8-a1ad-be4e6780fd50.png">

그냥 그림이 귀여워서 한 컷

### Preliminaries : Hourglass network
https://deep-learning-study.tistory.com/617
<img width="986" alt="image" src="https://user-images.githubusercontent.com/46675408/210469154-38b9a17a-c4df-4167-9d7e-2883712ce4cb.png">

u-net이랑 비슷한 느낌의 네트워크. pose estimation할 때 local과 global 정보 모두 필요해서 쓰임.

### Architecture
<img width="890" alt="image" src="https://user-images.githubusercontent.com/46675408/210469524-e01c380d-db5b-409b-8e83-384cfdc2cb3d.png">

- Detecting graph elements
image -> hourglass network -> CNN -> 1 x 1 conv + sigmoid로 object와 relation(sbj, obj의 중앙값으로 bbox 정의)에 대한 heatmap을 뽑도록 함 -> (학습 시에는) GT vertex, edge를 가지고 feature를 뽑은 뒤에 1) obj는 faster RCNN 방식으로 anchor 기반 offset regression, cls, id 예측 2) rel은 rel cls, sbj(논문에서 src) id, obj(논문에서 dest) id 예측 

- Connecting elements with associative embeddings
위에는 object, relation id들만 뽑았었고 이제 그 조합을 하는걸 해야됨. 각 vertex에 대해 vector embedding이 나오는데 그 vector embedding이 vertice끼리는 다양하게 학습되어야 하고 edge의 경우 subject와 object의 id를 표현할 수 있는 임베딩이 되어야 함
그래서 pull together, push apart loss를 추가
 #### pull together loss
<img width="422" alt="image" src="https://user-images.githubusercontent.com/46675408/210471614-8f127cbc-065a-4cdd-ad8b-61b05b6e4dcb.png">

$h_i\in\mathbb{R}^d$ : vertex $v_i$의 임베딩
$h_{ik}'$ : vertex $v_i$에 연결되어 있는 모든 edge의 임베딩. $k=1,...K_i$.

#### push apart loss
<img width="437" alt="image" src="https://user-images.githubusercontent.com/46675408/210471889-a4c482ce-68b1-4a52-ae66-d82fa8936ca4.png">

서로 다른 Node가 다른 embedding을 갖도록

### Result
<img width="956" alt="image" src="https://user-images.githubusercontent.com/46675408/210472235-b1ae0edc-0199-4b5a-ad2b-81ed16ee33f8.png">
