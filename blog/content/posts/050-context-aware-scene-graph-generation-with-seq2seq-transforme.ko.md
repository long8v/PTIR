---
title: "[44] Context-Aware Scene Graph Generation With Seq2Seq Transformers"
date: 2022-08-02
tags: ['ICCV', '2021Q4', 'SGG', 'graph']
paper: "https://openaccess.thecvf.com/content/ICCV2021/papers/Lu_Context-Aware_Scene_Graph_Generation_With_Seq2Seq_Transformers_ICCV_2021_paper.pdf"
issue: 50
issueUrl: "https://github.com/long8v/PTIR/issues/50"
---
![image](https://user-images.githubusercontent.com/46675408/182299681-48ec68cd-16ff-48cb-be0e-1d605f20b272.png)

[paper](https://openaccess.thecvf.com/content/ICCV2021/papers/Lu_Context-Aware_Scene_Graph_Generation_With_Seq2Seq_Transformers_ICCV_2021_paper.pdf)

## TL;DR
- **task :** two-stage Scene Graph Generator
- **problem :** 기존 연구들은 triplet들이 독립적이라고 가정하고 parallel 하게 예측한다
![image](https://user-images.githubusercontent.com/46675408/182321537-9620b7b3-dd75-44b2-901d-767246932482.png)
- **idea :** 다른 예측된 relations들을 보고 auto-regressive 하게 예측하면 더 잘 할 것이다! (위의 그림 참고)
- **architecture :** 트랜스포머 인코더-디코더 구조인데, 디코더에서 encoder에서 나온 값을 relation에 대한 임베딩과 함께 [S, P, O]로 넣어서 self-attention을 해주고, encoder에서 나온 값을 cross-attention도 해준다.
- **objective :** cross entropy loss + recall, mRecall에 대한 reinforcement learning 접근법 추가
- **baseline :** Graph R-CNN, ... 
- **data :** VRD, Visual Genome
- **result :** SOTA
- **contribution :** SGG에서 처음 보는 auto-regressive 한 접근법
- **limitation or 이해가 안 되는 부분 :** 학습이 되는게 신기함.. -> (토론 후) multi-object detection에도 sequential하게 넣어주는 경우 있었음. (이 사진에 고양이가 있었으면 개도 있을 것이다. 라는걸 학습) 트랜스포머 디코더에서는 input 정보만 보는게 아니라 cross-attention도 걸리고 하니까 input이 꼭 내가 뽑고싶은거랑 관련이 있을 필요는 없는듯.

## Details
### Architecture
![image](https://user-images.githubusercontent.com/46675408/182309482-7226450d-aba3-409d-92fb-52cba8d4fa64.png)

#### Object Encoder
그냥 트랜스포머 인코더. 근데 input으로 뭘 넣어줬다는지 잘 모르겠음. 그냥 visual feature map이려나?
$X_b$는 b번째 트랜스포머 block의 output

#### Relationship Decoder 
contextualized object features $X_B\in \mathbb{R}^{N\times D}$(N은 object 개수고 D는 임베딩 차원인듯)와 그 전 step까지 예측된 relationship $\hat Y_{1:m}$을 받아서 m(+1)번째 relationship을 뽑는 일을 함.

이때 decoder의 input은 subject의 contextualized embedding과 object의 contextualized embedding, 이전에 뽑힌 relation에 대한 임베딩값을 concat해서 들어감. $(X_B[i], E[r], X_B[j])$
그러니까 이전에 예측한 걸 임베딩해서 넣어주면 다음거가 나오는 특이한 구조임. concat한걸 D차원을 ffn 하고 self-attention, cross-attention을 통과함. 처음에는 그냥 D차원짜리 `<SOS>`를 넣어줌. 
cross-attention의 경우에 decoder의 self-attention으로 나온 $Y_k$와 encoder에서 나온 $X_B$랑 걸어줘서 나옴.
![image](https://user-images.githubusercontent.com/46675408/182317261-bf6a0992-c921-47fd-b76d-e3fc03cd4053.png)

마지막 K번째 decoder layer의 output $Y_K$를 가지고 다음 relationship triplet을 예측함. 
모든 남은 pair에 대해서 아래와 같이 예측함. 그리고 softmax가 가장 높은 것이 선택됨.
![image](https://user-images.githubusercontent.com/46675408/182317929-c9517580-c105-454a-b3d8-bfec471a78ed.png)

$i$ : subject indices, $j$ : object indicies

### Training scheme
- triplet 순서는 shuffling 해서 학습함.
- loss가 원래는 positive pair에 대해서만 부가되는데 VRD는 no relation을 예측하는 것도 중요해서 negative pair도 추가함.
![image](https://user-images.githubusercontent.com/46675408/182318147-23727fe6-686a-484c-bc9d-69e982b4921e.png)

### Reinforcement Learning
1) training시에는 input history를 GT로 받지만(teacher-forcing) inference에서는 그렇지 않음 2) cross entropy loss와 recall 사이의 gap이 있음. -> 디코딩 할 때 강화학습 요소를 추가하자.
 recall과 mRecall은 반대로 움직이는 성향이 있음. 그래서 alpha 추가하여 reward로 정의함. 
![image](https://user-images.githubusercontent.com/46675408/182319646-38879f45-4594-48ed-a536-c5629538faf2.png)

![image](https://user-images.githubusercontent.com/46675408/182319766-5d2f29dd-3c4b-498d-b66d-3b6304f71811.png)

여기서 action은 모든 pair에 대해서 logit 값이 나왔을 때 어떤걸 선택할지. state는 m개를 선택한 상태. RL 적용하니 greedy decoding보다 나았다.

### Expreiments
![image](https://user-images.githubusercontent.com/46675408/182318546-1b1748ec-cb5b-4d37-822a-9b83a481bcaa.png)


#### Qualitative Results
![image](https://user-images.githubusercontent.com/46675408/182320660-297c2a54-485e-4aa5-b66b-e72d4e908b7b.png)

independent하게 예측하는 것보다 gt 맞출 확률이 높아졌다.
